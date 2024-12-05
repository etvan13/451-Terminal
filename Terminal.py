# List needed imports
import os
import sys
import readline
import stat

# Importing command from Commands directory
from Commands.SimpleBruteForce import*
from Commands.ParameterBruteForce import* 

# This is the main terminal, it holds all the functionality of the system containing all the commands.
class Terminal:
    def __init__(self):
        # any initialization

        # make executables, executable
        for file in os.listdir("/executables"):
            st = os.stat(file)
            os.chmod(file, st.st_mode | stat.S_IEXEC)


        self.commands = {
            "help": self.show_help,
            "greetings": self.greet,
            "skeleton" : self.skeletonCommand,
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
    
    ## Add additional commands here ##





    # **************** HELPFUL REFERENCES *****************
    # Runs the skeleton class
    def skeletonCommand(self) :
        skeletonObject = SkeleClass(self, self.counter) # The additional 'self.counter' just allows use with the coordinates
        skeletonObject.run() # Runs the 'run()' command in the skeleton class
        return "Back to main terminal." # Message for returning to the terminal (after the run function finishes, it means your command finished)
    # ********************************************

    # Concept for adding external commands
    def add_external_command(self, command_name, command_function):
        self.commands[command_name] = command_function

    ##################

class SkeleClass:
    def __init__(self):
        pass  # Initialize any required variables here

    def run(self):
        print("Running the Skeleton command.")


# Main function to start the terminal
if __name__ == "__main__":
    terminal = Terminal()
    terminal.run()