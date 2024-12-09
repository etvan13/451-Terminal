import os

class XORCommand:
    def __init__(self, newpage):
        """
        Initialize the XORCommand.
        """
        self.newpage = newpage
        # Dynamically determine the data directory
        command_dir = os.path.dirname(os.path.abspath(__file__))
        project_dir = os.path.abspath(os.path.join(command_dir, ".."))
        self.data_dir = os.path.join(project_dir, "data", "xor")
        os.makedirs(self.data_dir, exist_ok=True)  # Ensure the data directory exists

    def xor_data(self, input_data, key):
        """
        Perform XOR operation on the input data with the given key.
        """
        xor_result = bytearray()
        key_bytes = key.encode()  # Convert key to bytes
        key_length = len(key_bytes)

        for i in range(len(input_data)):
            xor_result.append(input_data[i] ^ key_bytes[i % key_length])

        return xor_result

    def run(self):
        """
        Run the XOR command interactively.
        """
        self.newpage()  # Clear the screen
        print("XOR Command")
        print("===========\n")
        print("This command performs an XOR operation on input data.\n")

        # Ask the user for the input data
        input_choice = input("Enter '1' to XOR a file or '2' to XOR a string: ").strip()

        if input_choice == "1":  # XOR a file
            file_path = input("Enter the path to the file: ").strip()
            if not os.path.isfile(file_path):
                print("File not found. Returning to main terminal.")
                return

            with open(file_path, "rb") as file:
                input_data = file.read()

        elif input_choice == "2":  # XOR a string
            input_data = input("Enter the string to XOR: ").strip().encode()
        else:
            print("Invalid choice. Returning to main terminal.")
            return

        # Ask for the XOR key
        key = input("Enter the XOR key: ").strip()
        if not key:
            print("Key cannot be empty. Returning to main terminal.")
            return

        # Perform the XOR operation
        result = self.xor_data(input_data, key)

        # Display the result
        self.newpage()
        print("XOR Operation Result:\n")
        print("Hexadecimal Representation:")
        print(result.hex())
        print("\nDecoded (ASCII) Representation (if valid):")
        try:
            print(result.decode())
        except UnicodeDecodeError:
            print("[Result cannot be decoded to ASCII]")

        # Ask if the user wants to save the results
        save_choice = input("\nDo you want to save the results to a file? (Y/N): ").strip().lower()
        if save_choice == "y":
            save_path = os.path.join(self.data_dir, "xor_result.bin")
            with open(save_path, "wb") as file:
                file.write(result)
            print(f"\nResults saved to: {save_path}")

        input("\nPress 'Enter' to return to the main terminal.")
