# C3/commands/ghidra_command.py
import os
import subprocess

from utils.ghidra_conversion import GhidraReverser

class GhidraCommand:
    def __init__(self, newpage):
        """
        Initialize the command with access to the newpage function.
        """
        self.newpage = newpage
        self.reverser = GhidraReverser()

    def run(self):
        """
        Run the Ghidra reversing command interactively.
        """
        self.newpage()  # Clear the screen
        print("Welcome to the Ghidra Reversing Tool.")

        # List available executables in the executables directory
        executables = [
            f
            for f in os.listdir(self.reverser.executables_dir)
            if os.path.isfile(os.path.join(self.reverser.executables_dir, f))
        ]
        if not executables:
            print("No executables found in the ../executables directory.")
            return "Back to main terminal."

        print("\nAvailable executables:")
        for i, exe in enumerate(executables, start=1):
            print(f"{i}: {exe}")

        choice = input("\nEnter the number of the executable to reverse, or its full path: ").strip()
        if choice.isdigit() and 1 <= int(choice) <= len(executables):
            executable_path = os.path.join(
                self.reverser.executables_dir, executables[int(choice) - 1]
            )
        else:
            executable_path = choice

        if not os.path.exists(executable_path):
            print(f"Error: Executable not found at {executable_path}")
            return "Back to main terminal."

        # Prompt for architecture
        arch_input = input("Enter specific architecture? (Default is auto-detection) Y/N: ").strip().lower()
        arch = input("Enter architecture (e.g., x86:LE:64): ").strip() if arch_input == "y" else None

        # Prompt for keeping the project
        keep_input = input("Keep Ghidra project directory? (Default is no) Y/N: ").strip().lower()
        keep_project = keep_input == "y"

        # Run the reverser
        try:
            self.reverser.reverse_executable(
                executable_path,
                architecture=arch,
                keep_project=keep_project,
            )
        except subprocess.CalledProcessError as e:
            print(f"An error occurred during Ghidra analysis: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

        input("Finished processing. Press 'enter' to return back to the main terminal.")
        return
