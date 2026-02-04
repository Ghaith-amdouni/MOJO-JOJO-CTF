## CS 12.06 - SYSTEM 2.0

**Category:** Pwn  
**Difficulty:** Medium/Hard  
**Author:** r3t0x

## Description
XIIVI ONCE SAID "IINEK DIMA AL HOLILA" 

## Deployment
1. `docker-compose up --build -d`
2. Connect: `nc localhost 9006`

## Hints
- Ret2CSU is mandatory.
- Function pointers in `.data` are useful.
- `pop rdx`, `pop rsi`, `pop rdi` are NOT available.
- "Creative" values required for authentication.

## Files
- `challenge`: Binary