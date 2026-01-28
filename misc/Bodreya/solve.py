from pwn import *
import math
import sys
from hilbertcurve.hilbertcurve import HilbertCurve

# Allow running against remote or local
# Usage: python solve.py REMOTE <host> <port> or just python solve.py
if len(sys.argv) > 2:
    r = remote(sys.argv[1], int(sys.argv[2]))
else:
    # Default to local docker if running locally
    r = remote('localhost', 1337)

def solve():
    # Read Header - Updated for Bodreya Theme
    r.recvuntil(b"We need you to deliver ")
    n_cities = int(r.recvuntil(b" orders").strip().split()[0])
    log.info(f"Cities: {n_cities}")

    r.recvuntil(b"fuel budget of ")
    fuel_limit = float(r.recvuntil(b" liters").strip().split()[0])
    log.info(f"Fuel Limit: {fuel_limit}")
    
    r.recvuntil(b"Format: ID X Y")
    
    cities = []
    
    # Read cities
    # Data ends with "END"
    # Using recvuntil with drop=True might be safer with large data
    raw_data = r.recvuntil(b"END\n").decode()
    lines = raw_data.strip().split('\n')
    
    min_x, max_x = float('inf'), float('-inf')
    min_y, max_y = float('inf'), float('-inf')

    for line in lines:
        if line.strip() == "END": continue
        parts = line.split()
        if len(parts) < 3: continue
        
        try:
            cid = int(parts[0])
            x = int(parts[1])
            y = int(parts[2])
            
            cities.append({'id': cid, 'x': x, 'y': y})
            
            min_x = min(min_x, x)
            max_x = max(max_x, x)
            min_y = min(min_y, y)
            max_y = max(max_y, y)
        except ValueError:
            continue

    log.info(f"Parsed {len(cities)} cities.")
    log.info(f"Bounds: X[{min_x}, {max_x}] Y[{min_y}, {max_y}]")
    
    # Solve Logic
    # 10,000 cities. Max coord likely < 8192 if P=13 was used server side.
    
    max_coord = max(max_x, max_y)
    P = math.ceil(math.log2(max_coord + 1)) 
    log.info(f"Estimated P={P}")
    
    hc = HilbertCurve(P, 2)
    
    # Calculate T for each city (Batch Mode)
    points = [[c['x'], c['y']] for c in cities]
    t_values = hc.distances_from_points(points)
    
    for i, c in enumerate(cities):
        c['t'] = t_values[i]
        
    # Sort cities by 't'
    sorted_cities = sorted(cities, key=lambda k: k['t'])
    
    # Construct answer
    path = [str(c['id']) for c in sorted_cities]
    payload = " ".join(path)
    
    log.info("Sending solution...")
    r.sendline(payload.encode())
    
    # Read result (Look for flag)
    # Receive until we see either Flag or failure
    final_output = r.recvall().decode()
    print(final_output)

try:
    solve()
except Exception as e:
    log.error(f"Failed: {e}")
