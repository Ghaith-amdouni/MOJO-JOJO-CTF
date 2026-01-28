import socket
import threading
import sys
import math
import random
import time
from hilbertcurve.hilbertcurve import HilbertCurve

# Configuration
HOST = '0.0.0.0'
PORT = 1337
N_CITIES = 10000
TIMEOUT = 30 # 10k points is a lot to parse, giving 20s.
FLAG = "MOJO-JOJO{B0dr3y4_Mun1c1p4l1ty_4ppr0v3d_4lg0r1thm_8421}"

# Hilbert Curve Config
# P=13 -> 8192x8192 grid = 67M points. Enough for 10k cities.
P = 13
N_DIM = 2

def generate_cities():
    """Generates cities along the Hilbert curve. Bodreya roads are... broken."""
    hc = HilbertCurve(P, N_DIM)
    max_d = 2**(P * N_DIM) - 1
    
    # Select 10000 random points along the curve
    t_values = sorted(random.sample(range(max_d + 1), N_CITIES))
    points = hc.points_from_distances(t_values)
    
    cities = []
    for i, pt in enumerate(points):
        cities.append({
            'id': i,
            'x': pt[0],
            'y': pt[1],
            't': t_values[i] 
        })
    
    # Calculate the "Gold Standard" distance (Hilbert Order)
    gold_dist = 0
    for i in range(len(cities) - 1):
        p1 = cities[i]
        p2 = cities[i+1]
        dist = math.sqrt((p1['x'] - p2['x'])**2 + (p1['y'] - p2['y'])**2)
        gold_dist += dist
        
    # Shuffle for the user
    user_cities = list(cities)
    random.shuffle(user_cities)
    
    # HARDENING: Only 0.1% slack. You basically need the exact curve or a miracle.
    max_fuel = gold_dist * 1.001 
    
    return user_cities, max_fuel

def handle_client(client_socket):
    try:
        client_socket.settimeout(TIMEOUT)
        cities, max_fuel = generate_cities()
        
        # Sarcastic Intro
        intro = f"""
================================================================
  BODREYA MUNICIPALITY TRAFFIC CONTROL SYSTEM (LEGACY v0.1)
================================================================
Welcome, unfortunate driver.
You are currently in: BODREYA.
Status: CHAOS.
Traffic: YES.
Potholes: INFINITE.

We need you to deliver {len(cities)} orders of 'Mojo Jojo Special Sauce'.
The Mayor gave us a fuel budget of {max_fuel:.2f} liters.
If you waste even a drop, you are fired.
You have {TIMEOUT} seconds before the sauce gets cold.

GO!
Format: ID X Y
================================================================
"""
        client_socket.sendall(intro.encode())
        
        # Send Data
        data_block = ""
        for c in cities:
            data_block += f"{c['id']} {c['x']} {c['y']}\n"
        data_block += "END\n"
        data_block += "Send the path as space-separated IDs. HURRY!\n"
        client_socket.sendall(data_block.encode())
        
        # Receive solution
        start_time = time.time()
        response_data = b""
        while True:
            chunk = client_socket.recv(4096)
            if not chunk: break
            response_data += chunk
            if response_data.endswith(b"\n"): break
            
        if time.time() - start_time > TIMEOUT:
            client_socket.sendall(b"\nTOO SLOW! The sauce is cold. The customer is crying. You are fired.\n")
            return

        try:
            path_ids = list(map(int, response_data.decode().strip().split()))
        except ValueError:
            client_socket.sendall(b"\nAre you drunk? That's not a path.\n")
            return
            
        if len(path_ids) != len(cities):
            client_socket.sendall(f"\nYou missed some houses! Delivered {len(path_ids)}/{len(cities)}. Fired.\n".encode())
            return
            
        if len(set(path_ids)) != len(cities):
            client_socket.sendall(b"\nYou drove in circles? Duplicate cities found. Fired.\n")
            return

        # Verification
        city_map = {c['id']: c for c in cities}
        
        total_dist = 0
        current_city = city_map[path_ids[0]]
        
        for i in range(1, len(path_ids)):
            next_city = city_map[path_ids[i]]
            dist = math.sqrt((current_city['x'] - next_city['x'])**2 + (current_city['y'] - next_city['y'])**2)
            total_dist += dist
            current_city = next_city
            
        client_socket.sendall(f"\nFuel Used: {total_dist:.2f} / Budget: {max_fuel:.2f}\n".encode())
        
        if total_dist <= max_fuel:
            client_socket.sendall(f"Unbelievable. You actually arrived.\nThe Mayor is impressed. Here is your citizenship:\n{FLAG}\n".encode())
        else:
            client_socket.sendall(b"Out of gas. You are stranded in Bodreya forever.\n")

    except Exception as e:
        print(f"Error: {e}", flush=True)
        import traceback
        traceback.print_exc()
    finally:
        client_socket.close()

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((HOST, PORT))
    server.listen(5)
    print(f"[*] Bodreya Traffic Control listening on {HOST}:{PORT}")
    
    while True:
        client, addr = server.accept()
        print(f"[*] Victim connected from {addr[0]}:{addr[1]}")
        client_handler = threading.Thread(target=handle_client, args=(client,))
        client_handler.start()

if __name__ == "__main__":
    start_server()
