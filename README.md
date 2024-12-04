# Brute Force Terminal

## Overview
The **Brute Force Terminal** is a terminal program designed to execute commands for various functionalities, for brute-forcing passwords. It supports extensibility by allowing new commands to be added easily.

---

## How to Run the Terminal

1. **Simply Run the Terminal**
   ```bash
   Python Terminal.py
   ```

## Adding Commands

1. Create a Command Class

   * Navigate to the Commands directory.
   * Create a new Python file (e.g., NewCommand.py) for your command.
   * Define a class for the command with a run() method. Example:
        ```bash
        # Commands/NewCommand.py
   
        class NewCommand:
             def __init__(self):
                 pass
         
             def run(self):
                 print("Running the NewCommand!")
                 return "NewCommand executed successfully."
        ```
2. Import the Command

   * Open Terminal.py and import your new command class:
        ```bash
        from Commands.NewCommand import NewCommand
        ```
3. Add the Command to the Terminal

   * In the Terminal class, update the self.commands dictionary to include your new command:
        ```bash
        self.commands = {
          "help": self.show_help,
          "greetings": self.greet,
          "skeleton": self.skeletonCommand,
          "simple bruteforce": self.simple_brute_force_command,
          "newcommand": self.new_command_handler,  # Add your new command here
        }
        ```
   * Define a handler method for the command in the Terminal class:
        ```bash
          def new_command_handler(self):
             new_command = NewCommand()
             new_command.run()
             return "Exiting back to main terminal."
        ```
4. Test Your Command

   * Run the terminal program:
        ```bash
        python Terminal.py
        ```
   * Type the name of your new command (e.g., newcommand) to verify it works as expected:
        ```bash
        > newcommand
         Running the NewCommand!
         NewCommand executed successfully.
        ```




