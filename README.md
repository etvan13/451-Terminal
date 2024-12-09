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

     * Update the self.commands Dictionary
     Add your new command to the self.commands dictionary in the Terminal class. Each entry should be a tuple where:
          * The first element is the handler method for the command.
          * The second element is a short description of what the command does. This will be displayed when the user types help <command>. 

          ```bash
               self.commands = {
                    "help": (self.show_help, "Displays a list of commands or details for a specific command."),
                    "greetings": (self.greet, "Displays a greeting message."),
                    "skeleton": (self.skeletonCommand, "A placeholder skeleton command."),
                    "simple bruteforce": (self.simple_brute_force_command, "Executes a simple brute force attack."),
                    "newcommand": (self.new_command_handler, "Performs the functionality of the new command."),  # Add your new command here
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



# Disclaimer

This terminal program is intended solely for educational purposes and is designed to assist in the testing and evaluation of **your own software's security**. This tool was developed as part of the CSCE451 Reverse Engineering course at Texas A&M University to demonstrate concepts related to security testing and reverse engineering.

### Legal and Ethical Use

- You are **only permitted to use this tool on programs you own** or have explicit written permission to test.
- Any use of this tool for unauthorized purposes, including but not limited to:
  - Accessing, testing, or tampering with systems you do not own,
  - Attempting to bypass security mechanisms on unauthorized systems,
  - Engaging in activities that violate local, state, or international laws,
  is strictly prohibited.

### Responsibility and Liability

- The developers and contributors of this program are **not responsible for any misuse or damage** caused by this tool.
- Users are solely responsible for ensuring they comply with all applicable laws and regulations while using this program.

### Educational Intent

This tool is provided "as-is" with no guarantees of accuracy or reliability. It is intended as a learning aid and should only be used for ethical purposes.

If you are unsure whether your intended use is permitted, **do not use this tool**.

