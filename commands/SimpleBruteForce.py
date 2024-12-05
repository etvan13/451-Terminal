import subprocess
import time  # Import the time module for adding delays
import readline # Get rid of this for security or keep it for convinience
import os
import sys

class SimpleBruteForce:
    def __init__(self, newpage):
        self.newpage = newpage
        self.password_dir = "password_lists/"

    def list_files_in_directory(self, directory):
        """Lists all files in the given directory."""
        try:
            files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
            return files
        except FileNotFoundError:
            print(f"Error: Directory '{directory}' not found.")
            sys.exit(1)


    def run(self):
        self.newpage()
        print("Welcome to the simple bruteforce command. This takes an executable path \nas input and tests simple passwords on its input.")
        executable = input("Enter the path to the executable (e.g., ./executables/password_checker): ").strip()

        files = self.list_files_in_directory(self.password_dir)

        if not files:
            print(f"No files found in directory '{self.password_dir}'.")
            sys.exit(0)


        for idx, file in enumerate(files, start=1):
            print(f"{idx}. {file}")

        # Ask the user to pick a password list
        choice = 1
        while True:
            try:
                choice = int(input("\nEnter the number of the file you want to read: "))
                if choice < 1 or choice > len(files):
                    raise ValueError("Invalid choice.")
                break
            except ValueError as e:
                print("Error: Please enter a valid number corresponding to a file.")
                sys.exit(1)

        print()

        selected_file = os.path.join(self.password_dir, files[choice - 1]) 

        try:
            with open(selected_file, 'r') as file:
                for line in file:
                    try:
                        print(f"Trying password: {line}")
                        process = subprocess.Popen(
                            [executable],
                            stdin=subprocess.PIPE,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE
                        )
                        # Send the password to the process
                        output, error = process.communicate(input=f"{line}\n".encode(), timeout=5)

                        if b"true" in output:
                            print()
                            print("Success! The password is '" + line + "' for " + executable)
                            input("Press 'enter' to return to the main terminal.")
                            return
                        elif b"Incorrect password" in output:
                            print("Incorrect password, trying the next one...")
                        else:
                            print(f"Unexpected behavior: {output.decode()} {error.decode()}")
                            break
                    except subprocess.TimeoutExpired:
                        print("The executable took too long to respond. Skipping this password.")
                    except Exception as e:
                        print(f"Error occurred: {e}")

                    # Add a delay between password attempts
                    time.sleep(1)

        except Exception as e:
            print(f"Error reading file '{selected_file}': {e}")
            sys.exit(1)


        print()
        print("All passwords tested. No success.")
        input("Press 'enter' to return to the main terminal.")
        return
