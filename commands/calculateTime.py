import string
import time

class CalculateTime:
    def __init__(self, newpage):
        self.newpage = newpage

    def runDiagnostic(self):
        """
        Benchmark the system to determine how many password attempts it can calculate per second.
        """
        test_charset = string.ascii_letters + string.digits  # Use a sample charset
        test_length = 10  # Test a fixed password length
        num_tests = 1_000_000  # Number of combinations to compute for the benchmark

        print("Running diagnostic...")
        start_time = time.time()

        # Simulate password generation attempts
        for i in range(num_tests):
            _ = "".join([test_charset[i % len(test_charset)] for i in range(test_length)])

        end_time = time.time()
        elapsed_time = end_time - start_time

        # Calculate attempts per second
        attempts_per_second = num_tests / elapsed_time
        print(f"Diagnostic complete: {attempts_per_second:,.2f} attempts/second.")
        return attempts_per_second

    def timeEstimate(self, total_possibilities, attempts_per_second):
        """
        Estimate the time to crack all password possibilities at a given attempt rate.
        """
        total_seconds = total_possibilities / attempts_per_second

        # Convert seconds into a more human-readable format
        days, remainder = divmod(total_seconds, 86400)  # 86400 seconds in a day
        hours, remainder = divmod(remainder, 3600)  # 3600 seconds in an hour
        minutes, seconds = divmod(remainder, 60)

        return int(days), int(hours), int(minutes), int(seconds)


    
    def calculateProb(self, charset):
        """
        Calculate the total number of password possibilities for lengths up to 15
        using the provided charset.
        """
        total_possibilities = 0
        max_length = 15
        attempts = self.runDiagnostic()
        for length in range(1, max_length + 1):
            total_possibilities += len(charset) ** length
            print("Possibilities if length was",length,": ",total_possibilities)
            days, hours, minutes, seconds = self.timeEstimate(total_possibilities, attempts)
            print(f"And the time that it would take equals {days} days, {hours} hours, and {minutes} minutes")

        return total_possibilities
    

    def run(self):
        self.newpage()

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
            print("Error: No characters selected for the charset!")
            return

        total_possibilities = self.calculateProb(charset)
        input("Press 'enter' to return to the main terminal.")


