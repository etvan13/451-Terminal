import os
import subprocess
import argparse


class GhidraReverser:
    def __init__(self, ghidra_install_dir: str, project_dir: str, script_path: str):
        """
        Initialize the reverser with Ghidra paths.
        """
        self.ghidra_install_dir = ghidra_install_dir
        self.project_dir = project_dir
        self.script_path = script_path
        self.asm_dir = "../asm"
        self.c_code_dir = "../c_code"

        # Ensure output directories exist
        os.makedirs(self.asm_dir, exist_ok=True)
        os.makedirs(self.c_code_dir, exist_ok=True)

    def run_ghidra_headless(self, executable_path: str, architecture: str = "gcc_x86-64"):
        """
        Run Ghidra in headless mode to decompile the executable.
        """
        ghidra_headless = os.path.join(self.ghidra_install_dir, "support", "analyzeHeadless")
        output_dir = os.path.dirname(executable_path)
        executable_name = os.path.basename(executable_path)

        command = [
            ghidra_headless,
            self.project_dir,
            "MyProject",
            "-import",
            executable_path,
            "-postScript",
            os.path.basename(self.script_path),
            output_dir
        ]

        print(f"Running Ghidra headless mode for: {executable_path}")
        print(f"Using architecture: {architecture}")
        subprocess.run(command, check=True)
        return output_dir, executable_name

    def move_output_files(self, output_dir: str, executable_name: str):
        """
        Move Ghidra output files to their respective directories.
        """
        c_file = os.path.join(output_dir, f"{executable_name}.c")
        asm_file = os.path.join(output_dir, f"{executable_name}.asm")

        if os.path.exists(c_file):
            os.rename(c_file, os.path.join(self.c_code_dir, f"{executable_name}.c"))
            print(f"Moved C file to {self.c_code_dir}")

        if os.path.exists(asm_file):
            os.rename(asm_file, os.path.join(self.asm_dir, f"{executable_name}.asm"))
            print(f"Moved ASM file to {self.asm_dir}")
        else:
            print(f"ASM file not found for {executable_name}")

    def reverse_executable(self, executable_path: str, architecture: str = "gcc_x86-64"):
        """
        Reverse the given executable and organize the output.
        """
        output_dir, executable_name = self.run_ghidra_headless(executable_path, architecture)
        self.move_output_files(output_dir, executable_name)


def main():
    parser = argparse.ArgumentParser(description="Reverse an executable using Ghidra.")
    parser.add_argument(
        "executable",
        help="Path to the executable file to reverse",
    )
    parser.add_argument(
        "--arch",
        default="gcc_x86-64",
        help="Architecture type (default: gcc_x86-64)",
    )
    parser.add_argument(
        "--ghidra",
        default="/path/to/ghidra",
        help="Path to the Ghidra installation directory",
    )
    parser.add_argument(
        "--project",
        default="/path/to/ghidra_project",
        help="Path to the Ghidra project directory",
    )
    parser.add_argument(
        "--script",
        default="/path/to/ExportCode.java",
        help="Path to the Ghidra script",
    )

    args = parser.parse_args()

    reverser = GhidraReverser(
        ghidra_install_dir=args.ghidra,
        project_dir=args.project,
        script_path=args.script
    )

    try:
        reverser.reverse_executable(args.executable, args.arch)
        print("Reversal complete.")
    except Exception as e:
        print(f"Error during reversal: {e}")


if __name__ == "__main__":
    main()
