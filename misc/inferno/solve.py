import re

def solve():
    print("[Mojo Jojo's Decompiler of Absolute Superiority]")
    try:
        with open("mojos_mirror.ws", "r") as f:
            content = f.read()
            
            # Extract only whitespace
            ws_only = "".join([c for c in content if c in " \t\n"])
            
            # Regular expression for Push instruction:
            # Space Space (IMP + Command)
            # [Space/Tab] (Sign)
            # [Space/Tab]+ (Data)
            # LF (Terminator)
            # Regex: "  " + "[ \t]+" + "\n"
            push_pattern = re.compile(r"  ([ \t]+)\n")
            
            matches = push_pattern.findall(ws_only)
            
            if not matches:
                print("No hidden messages found! (Sarcastic laughter continues)")
                return
            
            decoded_chars = []
            for match in matches:
                # First char is sign (not needed for ASCII but technically there)
                # sign = match[0] 
                bits = match[1:]
                if not bits: continue
                
                # Convert Spaces/Tabs to 0s/1s
                bit_string = bits.replace(" ", "0").replace("\t", "1")
                val = int(bit_string, 2)
                
                if 32 <= val <= 126:
                    decoded_chars.append(chr(val))
            
            decoded_string = "".join(decoded_chars)
            if "MOJO-JOJO{" in decoded_string:
                print("Found hidden flag in the bytecode data!")
                print(f"Flag: {decoded_string[decoded_string.find('MOJO-JOJO{'):decoded_string.find('}')+1]}")
            else:
                print(f"Decoded data: {decoded_string}")
                print("You found data, but it's not the flag! Try harder!")
                
    except FileNotFoundError:
        print("Mojo Jojo's file is missing! Did he hide it again?")

if __name__ == "__main__":
    solve()
