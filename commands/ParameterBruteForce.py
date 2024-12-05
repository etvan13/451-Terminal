import subprocess
import time
import itertools
import string

class ParameterBruteForce:
    def __init__(self, newpage):
        self.newpage = newpage

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

        if knows_length:
            try:
                length = int(input("Enter the password length: ").strip())
                print(f"\nStarting brute force with passwords of length {length}...\n")
                for password_tuple in itertools.product(charset, repeat=length):
                    password = ''.join(password_tuple)
                    try:
                        print(f"Trying password: {password}")
                        process = subprocess.Popen(
                            [executable],
                            stdin=subprocess.PIPE,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE
                        )

                        output, error = process.communicate(input=f"{password}\n".encode(), timeout=5)

                        if b"true" in output:
                            print() 
                            print(f"Success! The password is '{password}' for {executable}")
                            input("Press 'enter' to return to the main terminal.")
                            return
                        elif b"Incorrect password" in output:
                            print("Incorrect password, trying the next one...")
                        else:
                            print(f"Unexpected behavior: {output.decode()} {error.decode()}")
                            return
                    except subprocess.TimeoutExpired:
                        print("The executable took too long to respond. Skipping this password.")
                    except Exception as e:
                        print(f"Error occurred: {e}")

            except ValueError:
                print("Invalid input for password length. Please enter a valid number.")
                return
        else:
            print("\nStarting brute force with increasing password lengths...\n")
            length = 1
            while True:
                print(f"Testing passwords of length {length}...")
                for password_tuple in itertools.product(charset, repeat=length):
                    password = ''.join(password_tuple)
                    try:
                        print(f"Trying password: {password}")
                        process = subprocess.Popen(
                            [executable],
                            stdin=subprocess.PIPE,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE
                        )

                        output, error = process.communicate(input=f"{password}\n".encode(), timeout=5)

                        if b"true" in output:
                            print() 
                            print(f"Success! The password is '{password}' for {executable}")
                            input("Press 'enter' to return to the main terminal.")
                            return
                        elif b"Incorrect password" in output:
                            print("Incorrect password, trying the next one...")
                        else:
                            print(f"Unexpected behavior: {output.decode()} {error.decode()}")
                            return
                    except subprocess.TimeoutExpired:
                        print("The executable took too long to respond. Skipping this password.")
                    except Exception as e:
                        print(f"Error occurred: {e}")

                length += 1

        print()
        print("All passwords tested. No success.")
        input("Press 'enter' to return to the main terminal.")
        return
