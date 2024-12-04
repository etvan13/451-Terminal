import subprocess
import time  # Import the time module for adding delays

class SimpleBruteForce:
    def __init__(self, newpage):
        # Common passwords to test
        self.common_passwords = ["123456", "123456789", "qwerty", "abc123", "password"]
        self.newpage = newpage

    def run(self):
        self.newpage()
        print("Welcome to the simple bruteforce command. This takes an executable path \nas input and tests simple passwords on its input.")
        executable = input("Enter the path to the executable (e.g., ./executables/password_checker): ").strip()

        for password in self.common_passwords:
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
                    return "Success! The password is: " + password
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

        print("All passwords tested. No success.")
        return "No valid password found, exiting back to main terminal."
