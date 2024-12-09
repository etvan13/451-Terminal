import os
import subprocess
import shutil


class BinwalkCommand:
    def __init__(self, newpage):
        """
        Initialize the BinwalkCommand with the executables directory and data/binwalk directory.
        """
        command_dir = os.path.dirname(os.path.abspath(__file__))
        project_dir = os.path.abspath(os.path.join(command_dir, ".."))
        self.executables_dir = os.path.join(project_dir, "executables")
        self.data_dir = os.path.join(project_dir, "data", "binwalk")
        os.makedirs(self.data_dir, exist_ok=True)  # Ensure the data directory exists
        self.newpage = newpage

    def list_files(self):
        """
        List executable files in the executables directory.
        """
        files = [
            f for f in os.listdir(self.executables_dir)
            if os.path.isfile(os.path.join(self.executables_dir, f))
        ]
        if not files:
            print("No executables found in the 'executables' directory.")
        return files

    def run_binwalk(self, file_path):
        """
        Run binwalk with extraction on the specified file and return the results.
        """
        try:
            # Run the binwalk command with extraction and forced raw data extraction
            result = subprocess.run(
                [
                    "binwalk",
                    "--extract",            # Enable automatic extraction
                    "--dd", ".*:raw",       # Force extraction of all data as raw
                    "--directory", self.data_dir,  # Extract into the data directory
                    file_path,
                ],
                capture_output=True,
                text=True,
            )
            return result.stdout.splitlines(), result.stderr.splitlines()
        except FileNotFoundError:
            print("The 'binwalk' command is not available on this system. Please install it.")
            return [], []
        except Exception as e:
            print(f"Error running binwalk command: {e}")
            return [], []

    def move_extracted_files(self, executable_name):
        """
        Move the extracted files from the binwalk extraction directory to data/binwalk/<executable_name>/
        """
        extracted_dir = os.path.join(self.data_dir, f"_{executable_name}.extracted")
        organized_dir = os.path.join(self.data_dir, executable_name)

        if os.path.exists(extracted_dir):
            if os.path.exists(organized_dir):
                shutil.rmtree(organized_dir)  # Remove if already exists
            shutil.move(extracted_dir, organized_dir)

            extracted_files = os.listdir(organized_dir)
            print("\nExtracted files:")
            for file in extracted_files:
                print(f"- {file}")

            save_files = input("\nDo you want to save the extracted files? (y/n): ").strip().lower()
            if save_files == 'n':
                shutil.rmtree(organized_dir)  # Delete the extracted files
                print("Extracted files deleted.")
                return None

            return organized_dir

        return None

    def analyze_raw_files(self, raw_files_dir):
        """
        Analyze .raw files in the specified directory to identify usable data.
        """
        raw_files = [f for f in os.listdir(raw_files_dir) if f.endswith(".raw")]
        if not raw_files:
            print("No .raw files found.")
            return

        while True:
            print("\nOptions for processing raw files:")
            print("1. Convert to text files")
            print("2. Convert to image files")
            print("3. Keep as binary dumps")
            print("4. Stop processing raw files")

            choice = input("Select an option (1-4): ").strip()
            if choice == "4":
                break

            for raw_file in raw_files:
                file_path = os.path.join(raw_files_dir, raw_file)
                print(f"\nProcessing {raw_file}...")

                if choice == "1":  # Convert to text
                    try:
                        with open(file_path, "rb") as f:
                            data = f.read().decode("utf-8", errors="replace")
                        new_path = os.path.splitext(file_path)[0] + ".txt"
                        with open(new_path, "w") as f:
                            f.write(data)
                        print(f"Converted {raw_file} to text: {os.path.basename(new_path)}")
                    except Exception as e:
                        print(f"Failed to convert {raw_file} to text: {e}")

                elif choice == "2":  # Convert to image
                    result = subprocess.run(["binwalk", file_path], capture_output=True, text=True)
                    if "JPEG image data" in result.stdout:
                        new_path = os.path.splitext(file_path)[0] + ".jpg"
                        shutil.copyfile(file_path, new_path)
                        print(f"Converted {raw_file} to image: {os.path.basename(new_path)}")
                    elif "PNG image data" in result.stdout:
                        new_path = os.path.splitext(file_path)[0] + ".png"
                        shutil.copyfile(file_path, new_path)
                        print(f"Converted {raw_file} to image: {os.path.basename(new_path)}")
                    else:
                        print(f"No recognizable image data found in {raw_file}.")

                elif choice == "3":  # Keep as binary dump
                    print(f"Keeping {raw_file} as is.")

            repeat = input("\nDo you want to process raw files again with different options? (y/n): ").strip().lower()
            if repeat != "y":
                break

    def run(self):
        """
        Run the binwalk command interactively.
        """
        self.newpage()  # Clear the screen
        print("Binwalk Command")
        print("=====================\n")
        print("This command analyzes executables for embedded files and data using binwalk.\n")

        files = self.list_files()
        if not files:
            print("No executables available for binwalk analysis.")
            return

        print("\nAvailable executables:")
        for i, file in enumerate(files, start=1):
            print(f"{i}. {file}")

        file_choice = input("\nEnter the number of the executable to analyze, or its full path, or 'q' to quit: ").strip()
        if file_choice.lower() == "q":
            return

        if file_choice.isdigit() and 1 <= int(file_choice) <= len(files):
            selected_file = os.path.join(self.executables_dir, files[int(file_choice) - 1])
            executable_name = os.path.splitext(files[int(file_choice) - 1])[0]
        elif os.path.isfile(file_choice):
            selected_file = file_choice
            executable_name = os.path.splitext(os.path.basename(file_choice))[0]
        else:
            print("Invalid choice. Returning to main terminal.")
            return

        print("\nRunning binwalk...")
        stdout, stderr = self.run_binwalk(selected_file)

        self.newpage()
        print(f"Results from binwalk analysis of {selected_file}:\n")
        if stdout:
            for line in stdout:
                print(line)
        if stderr:
            print("\nErrors/Warnings:")
            for line in stderr:
                print(line)

        organized_dir = self.move_extracted_files(executable_name)
        if not organized_dir:
            return

        # Ask if the user wants to analyze the raw data files
        analyze_files = input("\nDo you want to analyze the raw data files? (y/n): ").strip().lower()
        if analyze_files == "y":
            self.analyze_raw_files(organized_dir)

        input("\nPress 'Enter' to return to the main terminal.")
