import subprocess
import time
import os
import sys
import logging
from utils.pwd_validation import PasswordValidator  # Adjust the import path as necessary

class SimpleBruteForce:
    def __init__(self, newpage):
        self.newpage = newpage
        self.password_dir = "password_lists/"
        self.executables_dir = "executables/"
        self.validator = None  # Initialize as None; will set later
    
    def list_files_in_directory(self, directory):
        """Lists all files in the given directory."""
        try:
            files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
            return files
        except FileNotFoundError:
            print(f"Error: Directory '{directory}' not found.")
            sys.exit(1)
    
    def setup_validator(self, executable_path):
        """Initialize and configure the PasswordValidator."""
        self.validator = PasswordValidator(executable_path)
        # Add desired validation methods
        self.validator.add_validation_method(self.validator.check_exit_status, weight=2)
        self.validator.add_validation_method(self.validator.check_output_content, weight=3)
        self.validator.add_validation_method(self.validator.check_timing, weight=1)
        # Add more methods as needed
        logging.info("PasswordValidator setup complete with validation methods.")
    
    def run(self):
        """
        Run the simple brute force command interactively.
        """
        self.newpage()
        print("Welcome to the Simple Brute Force Command.")
        print("This command tests simple passwords against an executable's input.")

        # Resolve absolute paths for executables and password lists
        executables_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../", self.executables_dir))
        password_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../", self.password_dir))

        # List available executables in the executables directory
        executables = [
            f for f in os.listdir(executables_dir)
            if os.path.isfile(os.path.join(executables_dir, f))
        ]
        if not executables:
            print(f"No executables found in the directory '{executables_dir}'.")
            return "Back to main terminal."

        print("\nAvailable executables:")
        for i, exe in enumerate(executables, start=1):
            print(f"{i}: {exe}")

        choice = input("\nEnter the number of the executable to use, or the full path: ").strip()
        if choice.isdigit() and 1 <= int(choice) <= len(executables):
            executable_path = os.path.join(executables_dir, executables[int(choice) - 1])
        else:
            executable_path = os.path.abspath(choice)  # Allow absolute path input

        if not os.path.exists(executable_path):
            print(f"Error: Executable not found at {executable_path}")
            return "Back to main terminal."

        # List available password files
        password_files = [
            f for f in os.listdir(password_dir)
            if os.path.isfile(os.path.join(password_dir, f))
        ]
        if not password_files:
            print(f"No password files found in directory '{password_dir}'.")
            return "Back to main terminal."

        print("\nAvailable password files:")
        for idx, file in enumerate(password_files, start=1):
            print(f"{idx}. {file}")

        # Ask the user to pick a password list
        while True:
            try:
                password_choice = int(input("\nEnter the number of the file you want to use: "))
                if 1 <= password_choice <= len(password_files):
                    password_file_path = os.path.join(password_dir, password_files[password_choice - 1])
                    break
                else:
                    print("Error: Invalid choice. Please select a valid number.")
            except ValueError:
                print("Error: Please enter a number.")

        # Start brute force process
        print("\nStarting brute force process...")
        try:
            self.setup_validator(executable_path)
            with open(password_file_path, 'r') as file:
                for line in file:
                    password = line.strip()
                    if not password:
                        continue  # Skip empty lines
                    print(f"Trying password: {password}")

                    # Use the PasswordValidator to validate the password
                    is_valid = self.validator.validate(password)

                    if is_valid:
                        print()
                        print(f"Success! The password is '{password}' for {executable_path}")
                        input("Press 'enter' to return to the main terminal.")
                        return
                    else:
                        print("Incorrect password, trying the next one...")
        except Exception as e:
            print(f"An error occurred during brute force: {e}")
            return "Back to main terminal."

        print("\nAll passwords tested. No success.")
        input("Press 'enter' to return to the main terminal.")
        return

# Example usage
if __name__ == "__main__":
    def newpage():
        os.system('cls' if os.name == 'nt' else 'clear')
    
    brute_force = SimpleBruteForce(newpage)
    brute_force.run()
