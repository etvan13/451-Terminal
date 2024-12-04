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
