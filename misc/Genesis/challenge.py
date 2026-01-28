import torch
import torch.nn as nn
import sys

# The "Deep VM" Architecture
class LogicVM(nn.Module):
    def __init__(self, num_bits):
        super(LogicVM, self).__init__()
        self.l1 = nn.Linear(num_bits, num_bits)
        self.l2 = nn.Linear(num_bits, 1)
        self.relu = nn.ReLU()

    def forward(self, x):
        x = self.relu(self.l1(x))
        x = self.relu(self.l2(x))
        return x

def main():
    try:
        # Load the self-contained TorchScript model
        model = torch.jit.load("mojo_jojo.pt", map_location=torch.device('cpu'))
        model.eval()
    except Exception as e:
        print(f"Error: Could not load 'mojo_jojo.pt'.")
        sys.exit(1)

    print("--- MOJO JOJO ACCESS TERMINAL ---")
    flag = input("Enter Secret Key: ").strip()

    if len(flag) != 22:
        print(f"Error: Key must be exactly 22 characters. (Got {len(flag)})")
        sys.exit(1)

    # Convert flag to bits
    bits = ''.join(format(ord(c), '08b') for c in flag)
    input_tensor = torch.tensor([float(b) for b in bits]).unsqueeze(0)

    # Run the "Deep VM"
    with torch.no_grad():
        output = model(input_tensor)

    if output.item() > 0:
        print("ACCESS GRANTED. Welcome, Mojo.")
    else:
        print("ACCESS DENIED. Your logic is flawed.")

if __name__ == "__main__":
    main()
