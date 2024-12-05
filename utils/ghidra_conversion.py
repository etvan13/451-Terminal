import re

class GhidraToCppConverter:
    def __init__(self, ghidra_output: str):
        """
        Initialize the converter with Ghidra output.
        """
        self.raw_output = ghidra_output
        self.cleaned_output = ""
        self.cpp_output = ""

    def clean_output(self):
        """
        Remove unnecessary lines, comments, and extra spaces from Ghidra output.
        """
        lines = self.raw_output.splitlines()
        cleaned_lines = []
        for line in lines:
            line = line.strip()
            if not line or line.startswith("#") or line.startswith("//"):
                continue  # Ignore empty lines and comments
            cleaned_lines.append(line)
        self.cleaned_output = "\n".join(cleaned_lines)

    def convert_to_cpp(self):
        """
        Convert cleaned Ghidra output into C++ syntax.
        """
        lines = self.cleaned_output.splitlines()
        cpp_lines = []
        for line in lines:
            # Example: Convert specific patterns to C++ equivalents
            line = re.sub(r"(\bMOV\b)", "=", line)  # Example: MOV -> =
            line = re.sub(r"(\bJMP\b)", "goto", line)  # Example: JMP -> goto
            line = re.sub(r"([a-zA-Z_][a-zA-Z0-9_]*)\s*:", r"label \1:", line)  # Labels
            cpp_lines.append(line + ";")  # Append semicolon to lines
        self.cpp_output = "\n".join(cpp_lines)

    def save_to_file(self, filename: str):
        """
        Save the converted output to a C/C++ file.
        """
        with open(filename, "w") as file:
            file.write(self.cpp_output)

    def process(self, output_file: str):
        """
        Full processing pipeline to convert and save Ghidra output.
        """
        self.clean_output()
        self.convert_to_cpp()
        self.save_to_file(output_file)
        print(f"Converted output saved to {output_file}")

# Example usage:
if __name__ == "__main__":
    # Sample Ghidra output (replace with actual output)
    sample_output = """
    # Sample Ghidra disassembled code
    MOV eax, ebx
    JMP label_1
    label_1:
    ADD eax, 1
    """
    converter = GhidraToCppConverter(sample_output)
    converter.process("output.cpp")
