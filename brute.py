import subprocess
import string

def try_password(pw):
    # Run the binary
    p = subprocess.Popen(["./exam_2_v4/q1"], 
                         stdin=subprocess.PIPE, 
                         stdout=subprocess.PIPE, 
                         stderr=subprocess.STDOUT, 
                         text=True)
    
    # Provide the name
    p.stdin.write("Charles\n")
    p.stdin.flush()
    
    # Provide the password
    p.stdin.write(pw + "\n")
    p.stdin.flush()

    result = p.communicate()[0]
    return result

def main():
    # Known first character is 'F'
    # Password length is 8
    # We'll try a broad character set for the remaining 7 characters
    chars = ''.join([chr(c) for c in range(32, 127)])  # Printable ASCII

    found_any_25 = False
    found_any_50 = False
    found_any_75 = False

    # Broad brute force: This will be large, so you might want to break early 
    # once you get partial clues.
    # Start by just trying a reduced set of chars for demonstration:
    test_chars = string.digits + string.ascii_letters + string.punctuation

    for c1 in test_chars:
        for c2 in test_chars:
            for c3 in test_chars:
                for c4 in test_chars:
                    for c5 in test_chars:
                        for c6 in test_chars:
                            for c7 in test_chars:
                                candidate = f"F{c1}{c2}{c3}{c4}{c5}{c6}{c7}"
                                output = try_password(candidate)
                                # Check partial progress
                                if "25%" in output:
                                    if not found_any_25:
                                        print(f"Got 25% with: {candidate}")
                                        found_any_25 = True
                                    # If we reached 25%, maybe store candidates or narrow next search.
                                    
                                if "50%" in output:
                                    if not found_any_50:
                                        print(f"Got 50% with: {candidate}")
                                        found_any_50 = True
                                    
                                if "75%" in output:
                                    if not found_any_75:
                                        print(f"Got 75% with: {candidate}")
                                        found_any_75 = True
                                    
                                if "Congrats on another crackme!" in output:
                                    print(f"Password found: {candidate}")
                                    return

    if not found_any_25:
        print("No candidate even reached 25%. Check assumptions or I/O handling.")
    else:
        print("No final password found, but partial progress was seen. Use the partial matches to refine conditions.")

if __name__ == "__main__":
    main()
