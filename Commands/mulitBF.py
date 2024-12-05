import subprocess
from multiprocessing import Pool
from datetime import datetime

class multiBF:
    def __init__(self, newpage):
        self.common_passwords = ["123456", "123456789", "qwerty", "abc123", "password"]
        self.common_passwords2 = ["howdy", "nopasswordshere", "testpassword?", "pwd"]
        self.newpage = newpage

    def try_password(self, args):
        """Test a single password against the executable."""
        executable, password = args
        try:
            process = subprocess.Popen(
                [executable],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            output, error = process.communicate(input=f"{password}\n".encode(), timeout=5)

            if b"true" in output:
                return f"{datetime.now()} - Password: '{password}' - Success!"
            elif b"Incorrect password" in output:
                return f"{datetime.now()} - Password: '{password}' - Incorrect password."
            else:
                return f"{datetime.now()} - Password: '{password}' - Unexpected behavior: {output.decode()} {error.decode()}"
        except subprocess.TimeoutExpired:
            return f"{datetime.now()} - Password: '{password}' - Timeout occurred."
        except Exception as e:
            return f"{datetime.now()} - Password: '{password}' - Error: {e}"

    def run(self):
        self.newpage()
        print("Welcome to the simple bruteforce command. This takes an executable path \nas input and tests simple passwords on its input.")
        executable = input("Enter the path to the executable (e.g., ./executables/password_checker): ").strip()

        # Ask the user to pick a password list
        while True:
            password_choice = input("Pick list of passwords to try (1 or 2): ").strip()
            if password_choice == "1":
                password_list = self.common_passwords
                break
            elif password_choice == "2":
                password_list = self.common_passwords2
                break
            else:
                print("Invalid choice. Please enter 1 or 2.")

        # Get the number of processes to run
        while True:
            try:
                num_processes = int(input("Enter the number of processes to use (e.g., 4): ").strip())
                if num_processes > 0:
                    break
                else:
                    print("Please enter a positive integer.")
            except ValueError:
                print("Invalid input. Please enter a valid number.")

        print("\nTesting passwords...\n")

        # Use multiprocessing to test passwords in parallel
        with Pool(processes=num_processes) as pool:
            results = pool.map(self.try_password, [(executable, pw) for pw in password_list])

        # Print all outputs sequentially
        success = False
        for result in results:
            print(result)
            if "Success!" in result:
                success = True

        if not success:
            print("\nAll passwords tested. No success.")
        else:
            print("\nPassword found successfully.")
        
        input("Press 'enter' to return to the main terminal.")
