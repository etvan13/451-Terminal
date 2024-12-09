import os
import subprocess

class StringSearchCommand:
    def __init__(self, newpage):
        """
        Initialize the StringSearchCommand with the executables directory.
        """
        # Dynamically determine the executables directory and data directory
        command_dir = os.path.dirname(os.path.abspath(__file__))
        project_dir = os.path.abspath(os.path.join(command_dir, ".."))
        self.executables_dir = os.path.join(project_dir, "executables")
        self.data_dir = os.path.join(project_dir, "data", "string_search")
        os.makedirs(self.data_dir, exist_ok=True)  # Ensure the data directory exists
        self.newpage = newpage

    def list_files(self):
        """
        List executable files in the executables directory.
        """
        files = [
            f for f in os.listdir(self.executables_dir)
            if os.path.isfile(os.path.join(self.executables_dir, f))
        ]
        if not files:
            print("No executables found in the 'executables' directory.")
        return files

    def search_binary(self, file_path, filter_term=None, min_length=4):
        """
        Extract strings from a binary file using the `strings` command or a custom implementation.
        """
        try:
            # Run the `strings` command
            result = subprocess.run(
                ["strings", "-n", str(min_length), file_path],
                capture_output=True,
                text=True,
            )
            strings_output = result.stdout.splitlines()

            # Filter the results if a filter term is provided
            if filter_term:
                return [line for line in strings_output if filter_term in line]
            return strings_output
        except FileNotFoundError:
            print("The 'strings' command is not available on this system. Please install it.")
            return []
        except Exception as e:
            print(f"Error running strings command: {e}")
            return []

    def save_results(self, executable_name, results):
        """
        Save the string search results to a file in the data/string_search directory.
        """
        save_path = os.path.join(self.data_dir, f"{executable_name}.txt")
        try:
            with open(save_path, "w") as file:
                file.write("\n".join(results))
            print(f"\nResults saved to: {save_path}")
        except Exception as e:
            print(f"Error saving results to file: {e}")

    def run(self):
        """
        Run the string search command interactively.
        """
        self.newpage()  # Clear the screen
        print("String Search Command")
        print("=====================\n")
        print("This command extracts human-readable strings from executables in the\n'executables' directory.\n")

        # List files in the executables directory
        files = self.list_files()
        if not files:
            print("No executables available for string search.")
            return

        print("\nAvailable executables:")
        for i, file in enumerate(files, start=1):
            print(f"{i}. {file}")

        file_choice = input("\nEnter the number of the executable to search, or its full path, or 'q' to quit: ").strip()
        if file_choice.lower() == "q":
            return

        # Determine the selected file
        if file_choice.isdigit() and 1 <= int(file_choice) <= len(files):
            selected_file = os.path.join(self.executables_dir, files[int(file_choice) - 1])
            executable_name = os.path.splitext(files[int(file_choice) - 1])[0]
        elif os.path.isfile(file_choice):  # User provided a valid full path
            selected_file = file_choice
            executable_name = os.path.splitext(os.path.basename(file_choice))[0]
        else:
            print("Invalid choice. Returning to main terminal.")
            return

        # Ask for a filter term
        filter_term = input("Enter a search term to filter results (or press Enter to show all strings): ").strip()
        filter_term = filter_term if filter_term else None

        # Perform the search
        results = self.search_binary(selected_file, filter_term)

        # Display results
        self.newpage()
        print(f"Results from {selected_file}:\n")
        if results:
            for line in results:
                print(line)
        else:
            print("No results found.")

        # Ask if the user wants to save the results
        save_choice = input("\nDo you want to save the results to a file? (Y/N): ").strip().lower()
        if save_choice == "y":
            self.save_results(executable_name, results)

        input("\nPress 'Enter' to return to the main terminal.")
