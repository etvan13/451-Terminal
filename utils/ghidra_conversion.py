import os
import subprocess
import argparse
import re
import shutil
import time
from dotenv import load_dotenv
from tqdm import tqdm


class GhidraReverser:
    def __init__(self):
        """
        Initialize the reverser with paths loaded from environment variables.
        """
        load_dotenv()
        script_dir = os.path.dirname(os.path.abspath(__file__))

        self.ghidra_install_dir = os.getenv("GHIDRA_INSTALL_DIR")
        if not self.ghidra_install_dir:
            raise EnvironmentError("GHIDRA_INSTALL_DIR environment variable is not set.")

        self.executables_dir = os.path.abspath(os.path.join(script_dir, "../executables"))
        self.asm_dir = os.path.abspath(os.path.join(script_dir, "../asm"))
        self.c_code_dir = os.path.abspath(os.path.join(script_dir, "../c_code"))
        self.ghidra_project_base_dir = os.path.abspath(os.path.join(script_dir, "ghidra_projects"))
        self.script_path = os.path.abspath(os.path.join(script_dir, "ExportCode.java"))

        os.makedirs(self.asm_dir, exist_ok=True)
        os.makedirs(self.c_code_dir, exist_ok=True)
        os.makedirs(self.ghidra_project_base_dir, exist_ok=True)

    def run_ghidra_headless(self, executable_path: str, architecture: str = None):
        ghidra_headless = os.path.join(self.ghidra_install_dir, "support", "analyzeHeadless")
        executable_name = os.path.basename(executable_path)
        executable_dir = os.path.dirname(executable_path)

        ghidra_project_dir = os.path.join(self.ghidra_project_base_dir, f"project_{executable_name}")
        os.makedirs(ghidra_project_dir, exist_ok=True)

        command = [
            ghidra_headless,
            ghidra_project_dir,
            "MyProject",
            "-import",
            executable_path,
            "-postScript",
            os.path.basename(self.script_path),
            ghidra_project_dir,
            "-scriptPath",
            os.path.dirname(self.script_path),
            "-overwrite"
        ]
        if architecture:
            command += ["-processor", architecture]

        print(f"Running Ghidra headless mode for: {executable_name}")

        # Use the updated progress bar function
        self.show_progress_bar(command=command, total_time=50)

        return executable_dir, executable_name, ghidra_project_dir

    def move_output_files(self, executable_name: str, ghidra_project_dir: str):
        """
        Move Ghidra output files to their respective directories without cleaning.
        """
        # Paths to the generated files
        c_file = os.path.join(ghidra_project_dir, f"{executable_name}.c")
        asm_file = os.path.join(ghidra_project_dir, f"{executable_name}.asm")

        # Move C file
        if os.path.exists(c_file):
            dest_c_file = self.get_unique_filename(self.c_code_dir, f"{executable_name}.c")
            shutil.move(c_file, dest_c_file)
            print(f"C file moved to {self.c_code_dir}")

        # Move ASM file
        if os.path.exists(asm_file):
            dest_asm_file = self.get_unique_filename(self.asm_dir, f"{executable_name}.asm")
            shutil.move(asm_file, dest_asm_file)
            print(f"ASM file moved to {self.asm_dir}")

    def get_unique_filename(self, directory: str, filename: str) -> str:
        """
        Generate a unique filename if the file already exists by appending (1), (2), etc.
        """
        base, extension = os.path.splitext(filename)
        counter = 1
        unique_filename = filename
        while os.path.exists(os.path.join(directory, unique_filename)):
            unique_filename = f"{base}({counter}){extension}"
            counter += 1
        return os.path.join(directory, unique_filename)

    def show_progress_bar(self, command, total_time=50):
        """
        Show a time-based progress bar while a subprocess is running.
        """
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        step_time = total_time / 100  # Calculate time per progress step (100 steps total)

        with tqdm(total=100, desc="Processing with Ghidra", bar_format="{l_bar}{bar} [ time elapsed: {elapsed} ]") as progress_bar:
            for _ in range(100):  # Simulate 100 steps of progress
                if process.poll() is not None:  # Check if the process has finished
                    break
                time.sleep(step_time)
                progress_bar.update(1)
            
            # If the process finishes early or is still running, adjust the bar
            if process.poll() is None:
                process.wait()  # Wait for the process to finish
            progress_bar.n = 100  # Set to 100%
            progress_bar.last_print_n = 100
            progress_bar.close()
        
        stdout, stderr = process.communicate()
        if process.returncode != 0:
            print(f"Error during Ghidra analysis: {stderr.decode()}")
            raise subprocess.CalledProcessError(process.returncode, command)

    def reverse_executable(self, executable_path: str, architecture: str = None, keep_project: bool = False):
        """
        Reverse the given executable without cleaning the output.
        """
        executable_dir, executable_name, ghidra_project_dir = self.run_ghidra_headless(executable_path, architecture)
        self.move_output_files(executable_name, ghidra_project_dir)

        if not keep_project:
            print("Cleaning up Ghidra project directory...")
            shutil.rmtree(ghidra_project_dir, ignore_errors=True)
            # Optionally remove the base project directory if empty
            if not os.listdir(self.ghidra_project_base_dir):
                shutil.rmtree(self.ghidra_project_base_dir, ignore_errors=True)


def main():
    parser = argparse.ArgumentParser(
        description="Reverse an executable using Ghidra in headless mode."
    )
    parser.add_argument(
        "executable",
        help="Path to the executable file (full path or relative name if in ../executables).",
    )
    parser.add_argument(
        "--arch", 
        help="Specify architecture (e.g., x86:LE:64). Defaults to auto-detection.",
        default=None
    )
    parser.add_argument(
        "--keep-project", 
        action="store_true", 
        help="Keep the Ghidra project directory (default: False).",
    )

    args = parser.parse_args()

    reverser = GhidraReverser()

    executable_path = (
        args.executable if os.path.isabs(args.executable)
        else os.path.join(reverser.executables_dir, args.executable)
    )

    if not os.path.exists(executable_path):
        print(f"Error: Executable not found at {executable_path}")
        return

    try:
        reverser.reverse_executable(
            executable_path,
            architecture=args.arch,
            keep_project=args.keep_project,
        )
    except subprocess.CalledProcessError as e:
        print(f"An error occurred during Ghidra analysis: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()
