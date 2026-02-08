# Walkthrough: Hip-Hop Studio Manager

The **Hip-Hop Studio Manager** challenge is a modern heap exploitation task targeting **glibc 2.27** (Ubuntu 18.04). The goal is to leverage a heap overflow to perform a **Tcache Poisoning** attack and gain arbitrary write, ultimately overwriting a Global Offset Table (GOT) entry to redirect execution to a "debug" function that prints the flag.

## Challenge Overview
- **Vulnerability**: Heap overflow in the `edit_lyrics` function.
- **Constraint**: The binary uses **Partial RELRO**, which leaves the `.got.plt` section writable.
- **Protection**: PIE, NX, and Stack Canaries are enabled.
- **Target**: Overwrite `atoi@got` with the address of the `mic_check` function.

## Exploit Strategy: Tcache Poisoning

### 1. Leak and Reconnaissance
The binary conveniently prints the address of the `tracks` array in the BSS at startup. This allows us to calculate the binary base address and find the exact location of `atoi@got` and `mic_check`.

### 2. Heap Setup
We allocate two chunks of the same size (`0x110` including headers). We then free the second chunk (`idx1`) to the tcache.
```python
add() # idx 0
add() # idx 1
delete(1) # Free to tcache
```

### 3. Tcache Poisoning
Using the overflow in `idx0`, we overwrite the `next` pointer of the freed `idx1` chunk with the address of `atoi@got`.
```python
payload = b'A' * 0x100 + p64(0) + p64(0x111) + p64(atoi_got)
edit(0, payload)
```

### 4. Arbitrary Write
After poisoning the tcache, the next allocation of the same size will return the original heap chunk, but the allocation *after* that will return a pointer to `atoi@got`.
```python
add() # Returns original idx 1
add() # Returns atoi@got!
```

### 5. GOT Overwrite and Trigger
We use the newly acquired pointer to `atoi@got` to write the address of the `mic_check` function. Finally, sending a menu choice (like '1') triggers a call to `atoi`, which is now redirected to `mic_check`.

## Solver Usage
The included `solve.py` uses the provided dynamic loader (`ld-linux-x86-64.so.2`) to ensure compatibility across different host systems:
```python
process(['./dist/ld-linux-x86-64.so.2', '--library-path', './dist', './dist/hiphop'])
```

## POC Result
The exploit successfully triggers the `mic_check` function and retrieves the flag:

```text
[+] Master Access Token Accepted!
    Retrieving secret flag...
MOJO-JOJO{h3ap_p0is0n1ng_i5_v3ry_3asy_0n_2_27}
```
