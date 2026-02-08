import re
import time

target = "MOJO-JOJO{th3_r3g3x_0r4cl3_1s_sh4rp_4nd_d4ng3r0us}!"

def test(regex):
    start = time.time()
    try:
        re.search(regex, target)
    except:
        pass
    return time.time() - start

# Test patterns
patterns = [
    r"^MOJO-JOJO{t" + "(.+){20}!",
    r"^MOJO-JOJO{t" + "(.+){22}!",
    r"^MOJO-JOJO{t" + "(.+){25}!",
    r"^MOJO-JOJO{t" + "(.+){27}!",
]

for p in patterns:
    print(f"Pattern: {p} | Time: {test(p):.6f}s")
