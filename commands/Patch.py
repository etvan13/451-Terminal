import os
import curses
import subprocess
import re

class Patch:
    def __init__(self):
        self.cursor = 0
        self.scroll_offset = 0
        self.selected_lines = set()

    def get_binary_path(self):
        executables = [
            f for f in os.listdir('executables')
        ]
        if not executables:
            print("No executables found in the ../executables directory.")
            return "Back to main terminal."

        print("Pick a file to patch")
        for i, exe in enumerate(executables, start=1):
            print(f"{i}: {exe}")

        choice = input("\nEnter a number: ").strip()
        if choice.isdigit() and 1 <= int(choice) <= len(executables):
            return os.path.join("executables", executables[int(choice) - 1])
        else:
            print(f"invalid input")
            return -1


    def get_assembly_lines(self):
        try:
            result = subprocess.run(
                ['objdump', '-d', self.binary_path], 
                capture_output=True, 
                text=True, 
                check=True
            )
            
            asm_lines = []
            for line in result.stdout.split('\n'):
                match = re.match(r'^([0-9a-f]+):\s+([0-9a-f\s]+)\s+(.+)$', line.strip())
                if match:
                    address, hex_bytes, instruction = match.groups()
                    asm_lines.append(f"0x{address}: {hex_bytes.strip()} {instruction}")
            
            return asm_lines
        
        except subprocess.CalledProcessError as e:
            print(f"Error running objdump: {e}")
            return []

    def patch_binary(self):
        with open(self.binary_path, 'rb') as f:
            binary_data = bytearray(f.read())
        
        for line in self.selected_lines:
            match = re.match(r'0x([0-9a-f]+):\s+([0-9a-f\s]+)\s+', line)
            if match:
                address_str, hex_bytes_str = match.groups()
                
                address = int(address_str, 16)
                
                original_bytes = bytes.fromhex(hex_bytes_str.replace(' ', ''))
                
                nop_bytes = b'\x90' * len(original_bytes)
                
                start_index = binary_data.find(original_bytes)
                if start_index != -1:
                    binary_data[start_index:start_index+len(original_bytes)] = nop_bytes
        
        patched_path = f"{self.binary_path}_patched"
        
        with open(patched_path, 'wb') as f:
            f.write(binary_data)
        
        os.chmod(patched_path, 0o755)
        
        return patched_path

    def run(self):
        self.binary_path = self.get_binary_path()
        if self.binary_path == -1:
            return "invalid binary"

        self.asm_lines = self.get_assembly_lines()
        curses.wrapper(self.main)

    def main(self, stdscr):
        curses.use_default_colors()
        curses.curs_set(0)
        stdscr.clear()

        height, width = stdscr.getmaxyx()
        left_width = 5 * width // 8

        while True:
            stdscr.clear()

            if self.cursor < self.scroll_offset:
                self.scroll_offset = self.cursor
            elif self.cursor >= self.scroll_offset + height:
                self.scroll_offset = self.cursor - height + 1

            # Render assembly lines
            for i in range(height):
                line_index = i + self.scroll_offset
                if line_index < len(self.asm_lines):
                    line = self.asm_lines[line_index]
                    match = re.match(r'^(0x[0-9a-f]+):\s+([0-9a-f\s]+)\s+(.+)$', line)
                    if match:
                        address, hex_bytes, instruction = match.groups()
                        formatted_line = f"{address:<12}{hex_bytes:<24}{instruction}"
                    else:
                        formatted_line = line

                    truncated_line = self.truncate(formatted_line, left_width - 1)
                    try:
                        if line_index == self.cursor and line in self.selected_lines:
                            stdscr.addstr(i, 0, truncated_line, curses.A_REVERSE | curses.A_BOLD)
                        elif line_index == self.cursor:
                            stdscr.addstr(i, 0, truncated_line, curses.A_REVERSE)
                        elif line in self.selected_lines:
                            stdscr.addstr(i, 0, truncated_line, curses.A_BOLD)
                        else:
                            stdscr.addstr(i, 0, truncated_line)
                    except curses.error:
                        pass

            # Render instructions on the right side
            current_line = self.asm_lines[self.cursor] if self.asm_lines else ""
            right_start = left_width + 2
            right_width = width - right_start - 1

            try:
                stdscr.addstr(0, right_start, "Controls:")
                stdscr.addstr(1, right_start, "UP/DOWN: Navigate")
                stdscr.addstr(2, right_start, "SPACE: Toggle Select")
                stdscr.addstr(3, right_start, "P: Patch Selected Lines (NOP)")
                stdscr.addstr(4, right_start, "E: Edit Selected Line")
                stdscr.addstr(5, right_start, "Q: Quit")

                stdscr.addstr(7, right_start, "Current Line:")

                current_line_parts = [
                    current_line[i:i+right_width] for i in range(0, len(current_line), right_width)
                ]
                for idx, part in enumerate(current_line_parts):
                    stdscr.addstr(8 + idx, right_start, self.truncate(part, right_width))

                scroll_info = f"Scroll: {self.scroll_offset} / {len(self.asm_lines) - height}"
                stdscr.addstr(height - 1, right_start, self.truncate(scroll_info, right_width))
            except curses.error:
                pass

            stdscr.refresh()

            key = stdscr.getch()
            if key == curses.KEY_UP and self.cursor > 0:
                self.cursor -= 1
            elif key == curses.KEY_DOWN and self.cursor < len(self.asm_lines) - 1:
                self.cursor += 1
            elif key == ord(' '):
                current_line = self.asm_lines[self.cursor]
                if current_line in self.selected_lines:
                    self.selected_lines.remove(current_line)
                else:
                    self.selected_lines.add(current_line)
            elif key in (ord('q'), ord('Q')):
                break
            elif key in (ord('p'), ord('P')):
                # NOP patch selected lines
                if self.selected_lines:
                    patched_path = self.patch_binary()
                    stdscr.clear()
                    try:
                        stdscr.addstr(height//2, (width-len(patched_path))//2, f"Patched binary created: {patched_path}")
                    except curses.error:
                        pass
                    stdscr.refresh()
                    stdscr.getch()
                else:
                    stdscr.clear()
                    try:
                        stdscr.addstr(height//2, (width-len("No lines selected to patch"))//2, "No lines selected to patch")
                    except curses.error:
                        pass
                    stdscr.refresh()
                    stdscr.getch()
            elif key in (ord('e'), ord('E')):
                # Edit mode
                # Only works if exactly one line is selected (or handle multiple lines differently)
                if len(self.selected_lines) == 1:
                    edit_line = list(self.selected_lines)[0]
                    edited = self.edit_line(stdscr, edit_line)
                    if edited:
                        # Replace original bytes with user provided bytes
                        # This function will behave like patch_binary but with custom bytes
                        self.apply_custom_patch(edit_line, edited)
                        stdscr.clear()
                        msg = "Custom patch applied. Remember to run 'p' to write out the file."
                        stdscr.addstr(height//2, (width-len(msg))//2, msg)
                        stdscr.refresh()
                        stdscr.getch()
                    else:
                        # Cancelled or invalid
                        stdscr.clear()
                        msg = "Edit cancelled or invalid input."
                        stdscr.addstr(height//2, (width-len(msg))//2, msg)
                        stdscr.refresh()
                        stdscr.getch()
                else:
                    stdscr.clear()
                    msg = "Please select exactly one line to edit."
                    stdscr.addstr(height//2, (width-len(msg))//2, msg)
                    stdscr.refresh()
                    stdscr.getch()

    def edit_line(self, stdscr, line):
        # Enter a simple mode to read user input for the replacement hex bytes
        # Switch to cbreak mode to collect user input for hex bytes
        curses.echo()
        curses.curs_set(1)

        height, width = stdscr.getmaxyx()
        stdscr.clear()

        stdscr.addstr(height//2 - 2, (width - len("Enter new hex bytes (e.g. '90 90'):"))//2, "Enter new hex bytes (e.g. '90 90'):")
        stdscr.refresh()

        # Get user input
        new_bytes_str = stdscr.getstr(height//2, (width//2)-10, 20).decode().strip()

        curses.noecho()
        curses.curs_set(0)

        # Validate hex input
        hex_pairs = new_bytes_str.split()
        for pair in hex_pairs:
            if not re.match(r'^[0-9a-fA-F]{2}$', pair):
                return None  # invalid input

        return hex_pairs

    def apply_custom_patch(self, line, hex_pairs):
        # Similar to patch_binary, but we replace the selected line with our chosen bytes instead of NOP
        with open(self.binary_path, 'rb') as f:
            binary_data = bytearray(f.read())

        match = re.match(r'0x([0-9a-f]+):\s+([0-9a-f\s]+)\s+', line)
        if match:
            address_str, hex_bytes_str = match.groups()
            original_bytes = bytes.fromhex(hex_bytes_str.replace(' ', ''))

            new_bytes = bytes.fromhex(''.join(hex_pairs))
            # Ensure length matches
            if len(new_bytes) > len(original_bytes):
                # Truncate if too long
                new_bytes = new_bytes[:len(original_bytes)]
            elif len(new_bytes) < len(original_bytes):
                # Pad with NOPs if too short
                new_bytes += b'\x90' * (len(original_bytes) - len(new_bytes))

            # Locate the original bytes in the binary
            start_index = binary_data.find(original_bytes)
            if start_index != -1:
                binary_data[start_index:start_index+len(original_bytes)] = new_bytes

        patched_path = f"{self.binary_path}_patched_custom"
        with open(patched_path, 'wb') as f:
            f.write(binary_data)
        os.chmod(patched_path, 0o755)

        # Note: You might refine this to keep changes in memory until 'p' is pressed, if desired.

    def truncate(self, text, max_width):
        if not text:
            return ""
        text = str(text)
        if len(text) > max_width:
            return text[:max_width - 3] + "..."
        return text
