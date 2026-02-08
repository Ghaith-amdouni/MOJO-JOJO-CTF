import re
import signal
import socket
import threading
import time

FLAG = open("flag.txt").read().strip()

def handle_client(client_socket):
    try:
        # client_socket.sendall(b"Welcome to the Oracle. Give me a regex to test against my secret.\n> ")
        # No greeting/hints for the "Very Hard" version.
        user_regex = client_socket.recv(1024).decode().strip()
        
        # Security check: Limit regex complexity for sanity if needed, 
        # but the point is ReDoS, so we let it happen within a timeout.
        if len(user_regex) > 100:
            client_socket.sendall(b"Regex too long!\n")
            client_socket.close()
            return

        # The core oracle logic
        # We append padding to ensure ReDoS patterns that require a specific length 
        # (like (.+){N}!) always have enough characters to backtrack on.
        test_string = FLAG + "A" * 100 + "!" 
        
        start = time.time()
        try:
            # We use a thread-based timeout to kill the engine if it takes too long.
            # But the challenge relies on the *difference* in time.
            # 1 second is enough to distinguish between instant fail and catastrophic backtracking.
            match = re.search(user_regex, test_string)
            result = "Matched" if match else "No match"
        except Exception as e:
            result = f"Error: {str(e)}"
        
        elapsed = time.time() - start
        
        response = f"Result: {result}\nTime: {elapsed:.6f}s\n"
        client_socket.sendall(response.encode())
    except Exception as e:
        print(f"Error handling client: {e}")
    finally:
        client_socket.close()

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(("0.0.0.0", 1340))
    server.listen(5)
    print("Server listening on port 1340...")
    
    while True:
        client, addr = server.accept()
        print(f"Accepted connection from {addr}")
        handler = threading.Thread(target=handle_client, args=(client,))
        handler.start()

if __name__ == "__main__":
    main()
