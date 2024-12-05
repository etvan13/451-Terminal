import os
import curses

class Patch:
    def __init__(self):
        self.asm_lines = [
            "0x08048350 <main>:   push   ebp",
            "0x08048351           mov    ebp,esp",
            "0x08048353           sub    esp,0x10",
            "0x08048356           mov    eax,0x0",
            "0x08048351           mov    ebp,esp",
            "0x08048353           sub    esp,0x10",
            "0x08048356           mov    eax,0x0",
            "0x08048351           mov    ebp,esp",
            "0x08048353           sub    esp,0x10",
            "0x08048356           mov    eax,0x0",
            "0x08048351           mov    ebp,esp",
            "0x08048353           sub    esp,0x10",
            "0x08048356           mov    eax,0x0",
            "0x0804835b           leave",
            "0x0804835c           ret",
        ]
        self.cursor = 0

    def run(self):
        curses.wrapper(self.main)

    def main(self, stdscr):
        curses.curs_set(0)
        stdscr.clear()
        
        height, width = stdscr.getmaxyx()
        left_width = width // 2

        while True:
            stdscr.clear()
            
            # left pane
            for i, line in enumerate(self.asm_lines):
                truncated_line = self.truncate(line, left_width - 1)
                if i == self.cursor:
                    stdscr.addstr(i, 0, truncated_line, curses.A_REVERSE)
                else:
                    stdscr.addstr(i, 0, truncated_line)

            # right pane
            current_line = self.asm_lines[self.cursor]
            raw_bytes = " ".join([f"{ord(c):02x}" for c in current_line if c.isprintable()])
            
            right_start = left_width + 2
            right_width = width - right_start - 1
            
            stdscr.addstr(0, right_start, "Current Line Info:")
            stdscr.addstr(1, right_start, self.truncate(f"Instruction: {current_line.strip()}", right_width))
            stdscr.addstr(2, right_start, "Raw Bytes:")
            
            wrapped_bytes = [raw_bytes[i:i+right_width] for i in range(0, len(raw_bytes), right_width)]
            for idx, line in enumerate(wrapped_bytes, start=3):
                if idx >= height:
                    break
                stdscr.addstr(idx, right_start, line)
            
            stdscr.refresh()
            
            key = stdscr.getch()
            if key == curses.KEY_UP and self.cursor > 0:
                self.cursor -= 1
            elif key == curses.KEY_DOWN and self.cursor < len(self.asm_lines) - 1:
                self.cursor += 1
            elif key in (ord('q'), ord('Q')):
                break

    def truncate(self, text, max_width):
        if len(text) > max_width:
            return text[:max_width - 3] + "..."
        return text
