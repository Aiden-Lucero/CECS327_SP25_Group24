import socket

def connect_to_server():
    while True:  # Retries using loop
        serverhost_ipaddress = input("Enter the server IP address: ")
        target_port = input("Enter the server port number: ")

        # Validate the port number input
        if not target_port.isdigit() or not 0 < int(target_port) < 65536:
            print("Invalid port. Please enter a number between 1 and 65535.")
            continue

        target_port = int(target_port)

        #set up a TCP/IP socket
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            client_socket.connect((serverhost_ipaddress, target_port))  # Try to connect to the server
            print("Connected to the server. Type 'quit' to exit.")
            break  # Exits if successful
        except Exception as error:
            print(f"Connection failed: {error}. Please try again.")

    # Continues after connection
    while True:
        message = input("Enter your message: ")
        if message.lower() == 'exit':
            break

        try:
            client_socket.send(message.encode('utf-8'))  # Sends the message to the server
            reply = client_socket.recv(1024)  # Wait for the server's reply
            print(f"Server's reply: {reply.decode('utf-8')}")
        except Exception as error:
            print(f"Error: {error}")
            break

    client_socket.close()

connect_to_server()