"""
DISCLAIMER:
This program is intended solely for educational purposes and the testing of your own software's security.
Use of this tool on unauthorized systems or for illegal purposes is strictly prohibited.

The developers are not responsible for any misuse or damage caused by this tool.
"""

# List needed imports
import os
import sys
import readline
import stat

# Importing command from Commands directory
from commands.SimpleBruteForce import*
from commands.ParameterBruteForce import* 
from commands.GhidraCommand import*

# This is the main terminal, it holds all the functionality of the system containing all the commands.
class Terminal:
    def __init__(self):
        # any initialization

        executables_path = "executables/"

        # make executables, executable
        for file in os.listdir(executables_path):
            path = executables_path + file
            st = os.stat(path)

            os.chmod(path, st.st_mode | stat.S_IEXEC)


        self.commands = {
            "help": self.show_help,
            "disclaimer": self.show_disclaimer,
            "greetings": self.greet,
            "ghidra reverse": self.ghidra_command,
            "simple bruteforce": self.simple_brute_force_command,
            "parameter bruteforce": self.parameter_brute_force_command,
            # Additional commands can be added here
        }
        self.running = True

    #####TERMINAL UTILITY#####

    # Clears current screen
    @staticmethod
    def newpage():
        # Clear the console screen
        os.system('cls' if os.name == 'nt' else 'clear')

    # Header message of terminal
    def default_message(self):
        self.newpage()
        return "Brute Force Terminal\n" + "Type 'help' for a list of commands, or 'exit' to quit.\n"
    
    # Checks the inputted command for validity returning its output
    def process_command(self, command):
        if command in self.commands:
            response = self.commands[command]()
        else:
            response = "Unknown command."
        return self.default_message() + "\n" + response + "\n"  # Append a newline

    # Runs the current Terminal
    def run(self):
        # Start the terminal with the default message
        print(self.default_message())
        while True:
            command_input = input("> ").strip().lower()  # Get input and normalize
            if command_input == "exit":
                print("Exiting terminal. Goodbye!")
                break
            # Process the command and print the response
            print(self.process_command(command_input))


    ####COMMANDS####
    
    # Prints a list of available commands
    def show_help(self):
        command_list = self.commands.keys()
        help_text = "\n".join(f"- {cmd}" for cmd in command_list)
        return help_text
    
    # Returns Disclaimer
    def show_disclaimer(self):
        disclaimer = """
    **************************************
    DISCLAIMER:
    This program is intended solely for educational purposes 
    and the testing of your own software's security.Unauthorized 
    use, including testing systems without permission, is 
    strictly prohibited.

    The developers are not responsible for any misuse or damage 
    caused by this tool. Check the 'README.md' for more.
    **************************************
        """
        return disclaimer
        
    # Returns a greeting
    def greet(self):
        return "Hello Universe!"
    
    # Runs the simple brute force command
    def simple_brute_force_command(self):
        brute_force = SimpleBruteForce(self.newpage) # passing new page function to use in command class
        brute_force.run()
        return "Back to main terminal."

    def parameter_brute_force_command(self):
        brute_force = ParameterBruteForce(self.newpage) # passing new page function to use in command class
        brute_force.run()
        return "Back to main terminal."
    
        # Example integration into your terminal system
    def ghidra_command(self):
        ghidra = GhidraCommand(self.newpage)
        ghidra.run()
        return "Back to main terminal."

    ## Add additional commands here ##



### Example command class ###
class SkeleClass:
    def __init__(self):
        pass  # Initialize any required variables here

    def run(self):
        print("Running the Skeleton command.")


# Main function to start the terminal
if __name__ == "__main__":
    terminal = Terminal()
    terminal.run()