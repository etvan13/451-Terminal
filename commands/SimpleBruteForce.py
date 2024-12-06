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
        self.newpage()
        print("Welcome to the simple bruteforce command. This takes an executable path \nas input and tests simple passwords on its input.")
        executable = input("Enter the path to the executable (e.g., ./executables/password_checker): ").strip()
    
        # Setup the PasswordValidator with the executable
        self.setup_validator(executable)
    
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
                    password = line.strip()
                    if not password:
                        continue  # Skip empty lines
                    print(f"Trying password: {password}")
                    
                    # Use the PasswordValidator to validate the password
                    is_valid = self.validator.validate(password)
                    
                    if is_valid:
                        print()
                        print(f"Success! The password is '{password}' for {executable}")
                        input("Press 'enter' to return to the main terminal.")
                        return
                    else:
                        print("Incorrect password, trying the next one...")
    
        except Exception as e:
            print(f"Error reading file '{selected_file}': {e}")
            sys.exit(1)
    
        print()
        print("All passwords tested. No success.")
        input("Press 'enter' to return to the main terminal.")
        return

# Example usage
if __name__ == "__main__":
    def newpage():
        os.system('cls' if os.name == 'nt' else 'clear')
    
    brute_force = SimpleBruteForce(newpage)
    brute_force.run()
