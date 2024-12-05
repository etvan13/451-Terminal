import subprocess
import time
import itertools
import string
from multiprocessing import Pool, Process, Manager

class ParameterBruteForce:
    def __init__(self, newpage):
        self.newpage = newpage

    def log_output(self, log_queue):
        """Logs output from the queue."""
        while True:
            message = log_queue.get()
            if message == "DONE":
                break
            print(message)

    def test_password(self, args):
        """Test a single password."""
        executable, password, log_queue = args
        log_queue.put(f"Trying password: {password}")
        try:
            process = subprocess.Popen(
                [executable],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            output, error = process.communicate(input=f"{password}\n".encode(), timeout=5)

            if b"true" in output:
                return password
            elif b"Incorrect password" in output:
                return None
            else:
                log_queue.put(f"Unexpected behavior: {output.decode()} {error.decode()}")
                return None
        except subprocess.TimeoutExpired:
            log_queue.put("The executable took too long to respond. Skipping this password.")
            return None
        except Exception as e:
            log_queue.put(f"Error occurred: {e}")
            return None

    def run(self):
        self.newpage()
        print("Welcome to the simple bruteforce command. This takes an executable path \nas input and tests all possible password combinations based on user-defined criteria.")
        
        executable = input("Enter the path to the executable (e.g., ./executables/password_checker): ").strip()

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
                            args = ((executable, ''.join(p), log_queue) for p in passwords)
                            for result in pool.imap_unordered(self.test_password, args):
                                if result:
                                    print(f"Success! The password is '{result}' for {executable}")
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
                            args = ((executable, ''.join(p), log_queue) for p in passwords)
                            for result in pool.imap_unordered(self.test_password, args):
                                if result:
                                    print(f"Success! The password is '{result}' for {executable}")
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