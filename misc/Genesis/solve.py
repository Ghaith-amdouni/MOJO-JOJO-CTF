import torch
from z3 import *

# Load the TorchScript model
model = torch.jit.load("mojo_jojo.pt", map_location=torch.device('cpu'))

l1_weights = model.l1.weight.detach().numpy()
l1_bias = model.l1.bias.detach().numpy()
l2_weights = model.l2.weight.detach().numpy()
l2_bias = model.l2.bias.detach().numpy()

num_bits = l1_weights.shape[1]
s = Solver()

# Define input bits
x = [Int(f'x_{i}') for i in range(num_bits)]
for bit in x:
    s.add(Or(bit == 0, bit == 1))

# Optimized Layer 1: Bitwise match logic
# instead of floats, use simple bit logic
# if w == 1, input must be 1. if w == -1, input must be 0.
for i in range(num_bits):
    w = l1_weights[i, i]
    if w > 0:
        s.add(x[i] == 1)
    else:
        s.add(x[i] == 0)

print("Solving...")
if s.check() == sat:
    m = s.model()
    bits = [m[bit].as_long() for bit in x]
    flag = "".join(chr(int("".join(map(str, bits[i:i+8])), 2)) for i in range(0, num_bits, 8))
    print(f"Recovered Flag: {flag}")
else:
    print("No solution found.")
