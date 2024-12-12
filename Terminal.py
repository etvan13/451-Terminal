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
from commands.SimpleBruteForce import *
from commands.ParameterBruteForce import * 
from commands.Ghidra import *
from commands.DataDecoder import *
from commands.Patch import *
from commands.calculateTime import*
from commands.Binwalk import*
from commands.StringSearch import*
from commands.Xor import*

# This is the main terminal, it holds all the functionality of the system containing all the commands.
class Terminal:
    def __init__(self):
        executables_path = "executables/"

        # Make executables, executable
        for file in os.listdir(executables_path):
            path = executables_path + file
            st = os.stat(path)
            os.chmod(path, st.st_mode | stat.S_IEXEC)

        # Commands with explanations
        self.commands = {
            "help": (self.show_help, "Displays a list of commands or details for a specific command."),
            "disclaimer": (self.show_disclaimer, "Displays the program disclaimer."),
            "greetings": (self.greet, "Displays a greeting message."),
            "ghidra reverse": (self.ghidra_command, "Runs Ghidra reverse engineering tools."),
            "simple bruteforce": (self.simple_brute_force_command, "Executes a simple brute force attack."),
            "parameter bruteforce": (self.parameter_brute_force_command, "Executes parameterized brute force."),
            "patch": (self.patch, "Allows patching of files or executables."),
            "hex decoder": (self.data_decoder_command, "Decodes hex data into readable formats."),
            "bruteforce timing": (self.timeEstimate, "Estimates time required for a brute force attack."),
            "binwalk": (self.binwalk_command, "Analyzes binaries for hidden data."),
            "string search": (self.string_search_command, "Searches for human-readable strings in executables."),
            "xor": (self.xor_command, "XORs any inuptted data or data from a file."),

        }
        self.running = True

    ##### TERMINAL UTILITY #####

    @staticmethod
    def newpage():
        """Clears the terminal screen."""
        os.system("cls" if os.name == "nt" else "clear")

    def default_message(self):
        """Returns the default terminal message."""
        self.newpage()
        return "451 Terminal\nType 'help' for a list of commands, 'help + <command>' for more, or 'exit' to quit.\n"

    def process_command(self, command_input):
        """Processes a user-entered command."""
        if command_input.startswith("help"):
            parts = command_input.split(maxsplit=1)  # Split input into "help" and the command
            if len(parts) == 2:  # If a command is specified after "help"
                specific_command = parts[1]
                return self.show_help(specific_command)
            return self.show_help()  # If no specific command is provided

        # Check if the input matches a command
        if command_input in self.commands:
            response = self.commands[command_input][0]()  # Call the command function
        else:
            response = "Unknown command."
        return self.default_message() + "\n" + response + "\n"  # Append a newline

    def run(self):
        """Runs the terminal interactively."""
        print(self.default_message())
        while True:
            command_input = input("> ").strip().lower()  # Normalize input
            if command_input == "exit":
                print("Exiting terminal. Goodbye!")
                break
            # Process the command and print the response
            print(self.process_command(command_input))

    #### COMMANDS ####

    def show_help(self, specific_command=None):
        """Displays the help menu or details for a specific command."""
        # Clear the screen and show the default message
        output = self.default_message()

        if specific_command:
            if specific_command in self.commands:
                explanation = self.commands[specific_command][1]
                return output + f"\n{specific_command}: {explanation}\n"
            else:
                return output + "\nCommand not found. Use 'help' to list all commands.\n"

        # Show list of commands if no specific command is provided
        command_list = "\n".join(f"- {cmd}" for cmd in self.commands)
        return output + f"\nAvailable commands:\n{command_list}\n"

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
    
    def patch(self):
        p = Patch() # passing new page function to use in command class
        print(p.run())
        return "Patcher done"
    
    def ghidra_command(self):
        ghidra = GhidraCommand(self.newpage)
        ghidra.run()
        return "Back to main terminal."
    
    def data_decoder_command(self):
        decoder = DataDecoder(self.newpage)
        decoder.run()
        return "Back to main terminal."

    def timeEstimate(self):
        est = CalculateTime(self.newpage)
        est.run()
        return "Back to main terminal."

    def string_search_command(self):
        string_search = StringSearchCommand(self.newpage)
        string_search.run()
        return "Back to main terminal."

    def binwalk_command(self):
        binwalk = BinwalkCommand(self.newpage)
        binwalk.run()
        return "Back to main terminal."

    def xor_command(self):
        xor = XORCommand(self.newpage)
        xor.run()
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