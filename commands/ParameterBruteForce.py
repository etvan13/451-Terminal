import os
import subprocess
import time
import itertools
import string
from multiprocessing import Pool, Process, Manager
from utils.pwd_validation import PasswordValidator  # Adjust path to match your project structure

class ParameterBruteForce:
    def __init__(self, newpage):
        self.newpage = newpage
        self.password_dir = "executables/"  # Update to match directory structure
        self.validator = None

    def log_output(self, log_queue):
        """Logs output from the queue."""
        while True:
            message = log_queue.get()
            if message == "DONE":
                break
            print(message)

    def setup_validator(self, executable_path):
        """Initialize the PasswordValidator for the executable."""
        self.validator = PasswordValidator(executable_path)
        self.validator.add_validation_method(self.validator.check_exit_status)
        self.validator.add_validation_method(self.validator.check_output_content)

    def test_password(self, args):
        """Test a single password using PasswordValidator."""
        executable, password, log_queue = args
        log_queue.put(f"Trying password: {password}")
        try:
            if self.validator.validate(password):
                return password
            return None
        except Exception as e:
            log_queue.put(f"Error occurred while testing password '{password}': {e}")
            return None

    def run(self):
        self.newpage()
        print("Welcome to the Parameterized Brute Force Command.")
        print("This command tests all possible password combinations based on user-defined criteria.")

        # Improved executable selection
        executables_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../", self.password_dir))
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
            executable_path = os.path.abspath(choice)

        if not os.path.exists(executable_path):
            print(f"Error: Executable not found at {executable_path}")
            return "Back to main terminal."

        # Setup the PasswordValidator
        self.setup_validator(executable_path)

        includes_upper = input("Does the password include uppercase letters? (y/n): ").strip().lower() == 'y'
        includes_lower = input("Does the password include lowercase letters? (y/n): ").strip().lower() == 'y'
        includes_numbers = input("Does the password include numbers? (y/n): ").strip().lower() == 'y'
        includes_symbols = input("Does the password include symbols? (y/n): ").strip().lower() == 'y'

        charset = ""
        if includes_upper:
            charset += string.ascii_uppercase
        if includes_lower:
            charset += string.ascii_lowercase
        if includes_numbers:
            charset += string.digits
        if includes_symbols:
            charset += string.punctuation

        if not charset:
            print("You must include at least one type of character.")
            return
        
        knows_length = input("Do you know the password length? (y/n): ").strip().lower() == 'y'

        with Manager() as manager:
            log_queue = manager.Queue()
            log_process = Process(target=self.log_output, args=(log_queue,))
            log_process.start()

            try:
                if knows_length:
                    try:
                        length = int(input("Enter the password length: ").strip())
                        print(f"\nStarting brute force with passwords of length {length}...\n")
                        with Pool() as pool:
                            passwords = itertools.product(charset, repeat=length)
                            args = ((executable_path, ''.join(p), log_queue) for p in passwords)
                            for result in pool.imap_unordered(self.test_password, args):
                                if result:
                                    print(f"Success! The password is '{result}' for {executable_path}")
                                    log_queue.put("DONE")
                                    log_process.join()
                                    
                                    while True:
                                        user_input = input(f"The found password is '{result}'. Press Enter to continue or type 'exit' to return to terminal: ").strip().lower()
                                        if user_input == 'exit':
                                            return

                    except ValueError:
                        print("Invalid input for password length. Please enter a valid number.")
                        return
                else:
                    print("\nStarting brute force with increasing password lengths...\n")
                    length = 1
                    while True:
                        print(f"Testing passwords of length {length}...")
                        with Pool() as pool:
                            passwords = itertools.product(charset, repeat=length)
                            args = ((executable_path, ''.join(p), log_queue) for p in passwords)
                            for result in pool.imap_unordered(self.test_password, args):
                                if result:
                                    print(f"Success! The password is '{result}' for {executable_path}")
                                    log_queue.put("DONE")
                                    log_process.join()
                                    
                                    while True:
                                        user_input = input(f"The found password is '{result}'. Press Enter to continue or type 'exit' to return to terminal: ").strip().lower()
                                        if user_input == 'exit':
                                            return
                        length += 1

                print("All passwords tested. No success.")
            finally:
                log_queue.put("DONE")
                log_process.join()
