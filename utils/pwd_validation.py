import subprocess
import time
import logging


class PasswordValidator:
    def __init__(self, executable_path, use_weights=True):
        """
        Initialize the PasswordValidator.

        :param executable_path: Path to the executable to validate passwords against.
        :param use_weights: Whether to use weighted validation (default: True).
        """
        self.executable_path = executable_path
        self.validation_methods = []
        self.use_weights = use_weights
        self.failure_indicators = ["Incorrect password", "try again", "invalid", "failure"] # Known failure outputs
        logging.basicConfig(level=logging.INFO)

    def add_validation_method(self, method, weight=None):
        """
        Add a validation method with an optional weight.

        :param method: The validation method (function) to add.
        :param weight: Optional weight for weighted validation (default: None).
        """
        self.validation_methods.append((method, weight))

    def is_failure_output(self, output, error):
        """
        Check if the output or error matches known failure indicators.

        :param output: Standard output from the executable.
        :param error: Standard error from the executable.
        :return: True if the output matches failure indicators; False otherwise.
        """
        combined = f"{output} {error}".lower()
        return any(indicator in combined for indicator in self.failure_indicators)

    def validate(self, password):
        """
        Run all validation methods to determine if the password is valid.

        :param password: The password to validate.
        :return: True if the password is valid; False otherwise.
        """
        if not self.use_weights:
            # Non-weighted mode: Any single method passing is enough
            for method, _ in self.validation_methods:
                if method(password):
                    return True
            return False

        # Weighted mode: Aggregate scores based on weights
        total_score = 0
        max_score = sum(weight or 1 for _, weight in self.validation_methods)
        for method, weight in self.validation_methods:
            if method(password):
                total_score += weight or 1
        return total_score / max_score >= 0.7

    def run_executable(self, password):
        """
        Run the executable with the given password.

        :param password: The password to input to the executable.
        :return: A tuple of (output, error, return_code).
        """
        try:
            proc = subprocess.run(
                [self.executable_path],
                input=password.strip(),
                text=True,
                capture_output=True,
                timeout=5
            )
            return proc.stdout, proc.stderr, proc.returncode
        except subprocess.TimeoutExpired:
            return "", "Timeout occurred.", -1

    # Validation Methods
    def check_exit_status(self, password):
        """
        Check if the executable exits with a success code.

        :param password: The password to validate.
        :return: True if the exit code indicates success; False otherwise.
        """
        _, _, return_code = self.run_executable(password)
        return return_code == 0

    def check_output_content(self, password):
        """
        Check if the executable's output is not a failure message.

        :param password: The password to validate.
        :return: True if the output does not indicate failure; False otherwise.
        """
        output, error, _ = self.run_executable(password)
        return not self.is_failure_output(output, error)

    def check_timing(self, password):
        """
        Check the time it takes for the executable to process the password.

        :param password: The password to validate.
        :return: True if the execution time is within expected bounds; False otherwise.
        """
        start_time = time.time()
        _, _, _ = self.run_executable(password)
        end_time = time.time()
        execution_time = end_time - start_time
        return 0.1 <= execution_time <= 5  # Adjust timing thresholds as needed

    def check_combined_behavior(self, password):
        """
        A more complex validation that combines multiple observable behaviors.

        :param password: The password to validate.
        :return: True if combined behavior does not indicate failure; False otherwise.
        """
        output, error, return_code = self.run_executable(password)
        if self.is_failure_output(output, error):
            return False
        if return_code != 0:
            return False
        return True

    def debug_run(self, password):
        """
        Debugging helper to log all outputs for a given password.

        :param password: The password to validate.
        """
        output, error, return_code = self.run_executable(password)
        print(f"Password: {password}")
        print(f"Output: {output}")
        print(f"Error: {error}")
        print(f"Return Code: {return_code}")
    
    # Add other methods similarly...

# Usage Example
if __name__ == "__main__":
    validator = PasswordValidator("./executable", use_weights=False)
    validator.add_validation_method(validator.check_exit_status)
    validator.add_validation_method(validator.check_output_content)
    validator.add_validation_method(validator.check_timing)

    password = "test_password"
    is_valid = validator.validate(password)  # Returns True if any method passes
    print(f"Password {'is valid' if is_valid else 'is invalid'}")


    ## With weights ##
    validator = PasswordValidator("./executable", use_weights=True)
    validator.add_validation_method(validator.check_exit_status, weight=3)
    validator.add_validation_method(validator.check_output_content, weight=2)
    validator.add_validation_method(validator.check_timing, weight=1)

    password = "test_password"
    is_valid = validator.validate(password)  # Uses weights to calculate score
    print(f"Password {'is valid' if is_valid else 'is invalid'}")
