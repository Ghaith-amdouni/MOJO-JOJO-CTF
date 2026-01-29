
def to_ws_int(n):
    if n == 0: return "S\n"
    s = ""
    prefix = "S" if n > 0 else "T"
    n = abs(n)
    while n > 0:
        s = ("S" if n % 2 == 0 else "T") + s
        n //= 2
    return prefix + s + "\n"

def push(n):
    return "SS" + to_ws_int(n)

def print_char():
    return "LSST"

def end():
    return "LLL"

# CTF Language Flag (Leetspeak)
flag = "MOJO-JOJO{1nv1s1bl3_g3n1us_m1rr0r_m4yh3m}"
msg = "MUHAHAHA\n"

code = ""
# Hidden Flag: Push each character but don't print
for c in flag:
    code += push(ord(c))

# Distraction Message: Push and print
for c in msg:
    code += push(ord(c))
    code += print_char()

code += end()

final_code = code.replace("S", " ").replace("T", "\t").replace("L", "\n")

# NO COMMENTS! Pure Whitespace.
with open("/home/ghaith/Documents/Mojo_tasks/misc/inferno/mojos_mirror.ws", "w") as f:
    f.write(final_code)
print("Challenge file generated successfully (Leetspeak Flag, No comments).")
