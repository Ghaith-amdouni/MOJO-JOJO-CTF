# The Fragmented Scribe

**Category:** Pwn
**Difficulty:** Hard (Ultra)

## Description
The scribe is dying. The message is breaking. 
Only 100 fragments (bytes) remain. The language has been stripped of its direct commands (No Syscalls).
The scribe accepts only the purest symbols (Printable ASCII 33-126).

Can you piece together the fragment that writes history?

**Constraints:**
- Max 100 bytes of shellcode.
- Strictly Printable ASCII (33-126).
- No `syscall` (0F 05) or `int 80` (CD 80) bytes allowed.

## Connection
`nc <host> 1338`


