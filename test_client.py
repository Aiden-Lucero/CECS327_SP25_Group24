import socket

def run_test_client():
    server_ip = input("Enter the server IP (use 127.0.0.1 if same computer): ")
    server_port = int(input("Enter the server port: "))

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((server_ip, server_port))

        print("\nType one of the following queries:")
        print("1. What is the average moisture inside my kitchen fridge in the past three hours?")
        print("2. What is the average water consumption per cycle in my smart dishwasher?")
        print("3. Which device consumed more electricity among my three IoT devices?")
        print("Type 'exit' to quit.\n")

        while True:
            msg = input("Your query: ")
            if msg.lower() == "exit":
                break

            client_socket.sendall(msg.encode())
            response = client_socket.recv(4096).decode()
            print(f"Server response:\n{response}\n")

run_test_client()
