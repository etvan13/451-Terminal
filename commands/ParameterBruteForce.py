import subprocess
import time  # Import the time module for adding delays
import readline # Get rid of this for security or keep it for convinience

class ParameterBruteForce:
    def __init__(self, newpage):
        # Common passwords to test
        self.common_passwords = ["123456", "123456789", "qwerty", "abc123", "password"]
        self.common_passwords2 = ["howdy", "nopasswordshere", "testpassword?", "pwd"]
        self.newpage = newpage

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

        print()

        for password in password_list:
            try:
                print(f"Trying password: {password}")
                process = subprocess.Popen(
                    [executable],
                    stdin=subprocess.PIPE,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE
                )
                # Send the password to the process
                output, error = process.communicate(input=f"{password}\n".encode(), timeout=5)

                if b"true" in output:
                    print()
                    print("Success! The password is '" + password + "' for " + executable)
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

        print()
        print("All passwords tested. No success.")
        input("Press 'enter' to return to the main terminal.")
        return
