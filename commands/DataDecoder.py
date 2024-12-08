import subprocess
import time
import os
import sys
import logging
from utils.pwd_validation import PasswordValidator  # Adjust the import path as necessary
import sys
import struct
import binascii

class DataDecoder:
    def __init__(self, newpage):
        self.newpage = newpage

        self.validator = None  # Initialize as None; will set later
    
    def run(self):
        """
        Run the simple brute force command interactively.
        """
        self.newpage()
        print("Welcome to the Dataa Decoder.")
        print("This command attempts to convert a hexadecimal number to various data types and reports them\nType exit to go back to main menu")

        print("\nEnter hexadecimal you want to decipher:\n")
        inputted_hex = ''
        while True:
            inputted_hex = input()

            if inputted_hex == "exit":
                return

            if not all(c in '0123456789abcdefABCDEF' for c in inputted_hex):
                print("Invalid hexadecimal number.")
            else:
                break

        # Pad to align length for struct operations
        padded_hex = inputted_hex if len(inputted_hex) % 2 == 0 else "0" + inputted_hex

        self.hex_to_data(padded_hex)
        
    
    def hex_to_data(self, hex_string):
        try:
            # Convert hex string to bytes
            byte_data = bytes.fromhex(hex_string)
            print(f"\nHexadecimal: {hex_string}")
            print(f"Bytes: {byte_data}")

            # Interpret as an integer (big-endian)
            try:
                as_int = int(hex_string, 16)
                print(f"Integer (as one number): {as_int}")
            except ValueError:
                print("Integer conversion failed.")

            # Interpret as characters
            try:
                as_string = byte_data.decode('utf-8', errors='ignore')
                print(f"String: {as_string}")
            except UnicodeDecodeError:
                print("String conversion failed.")

            # Interpret as a float or double (if possible)
            if len(byte_data) in [4, 8]:  # Single float (4 bytes) or double (8 bytes)
                try:
                    if len(byte_data) == 4:
                        as_float = struct.unpack('>f', byte_data)[0]
                        print(f"Float: {as_float}")
                    elif len(byte_data) == 8:
                        as_double = struct.unpack('>d', byte_data)[0]
                        print(f"Double: {as_double}")
                except struct.error:
                    print("Float/Double conversion failed.")
            else:
                print("Float/Double: Invalid length for conversion (needs 4 or 8 bytes).")

            # Interpret as arrays of integers
            as_int_array = [int(byte) for byte in byte_data]
            print(f"Array of integers: {as_int_array}")

            # Interpret as arrays of longs (using 8-byte chunks)
            if len(byte_data) % 8 == 0:
                as_long_array = struct.unpack(f'>{len(byte_data)//8}q', byte_data)
                print(f"Array of longs: {as_long_array}")
            else:
                print("Array of longs: Data length not a multiple of 8 bytes.")

            # Interpret first byte as a char (if applicable)
            if len(byte_data) > 0:
                as_char = chr(byte_data[0]) if 32 <= byte_data[0] <= 126 else f"Non-printable (0x{byte_data[0]:02X})"
                print(f"Character (first byte): {as_char}")
            else:
                print("Character: No data to convert.")
        except Exception as e:
            print(f"Error: {e}")

        input("\nPress 'enter' to return to the main terminal.")



# Example usage
if __name__ == "__main__":
    def newpage():
        os.system('cls' if os.name == 'nt' else 'clear')
    
    data = DataDecoder(newpage)
    data.run()
