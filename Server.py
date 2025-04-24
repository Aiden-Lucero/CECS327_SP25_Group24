import socket

def launch_server():
    serverhost_ipaddress = '0.0.0.0'  #Server will listen on all available IP addresses
    listening_port = int(input("Enter the port number for the server: "))

    #Creating a TCP/IP socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((serverhost_ipaddress, listening_port))  # Bind to the specified IP and port
    server_socket.listen(5)  # Listening for connections, up to 5

    print(f"Server started. Listening on {serverhost_ipaddress}:{listening_port}...")

    while True:
        client_socket, client_address = server_socket.accept()  # New connection is accepted
        print(f"Connection established with {client_address}")

        while True:
            try:
                message = client_socket.recv(1024)  # Receiving information
                if not message:
                    break  # Connection is closed if no information is received

                print(f"Received from {client_address}: {message.decode('utf-8')}")
                client_socket.send(message.upper())  # Message is sent back in uppercase
            except ConnectionResetError:
                print(f"Connection lost with {client_address}. Waiting for a new connection.")
                break

        client_socket.close()

launch_server()