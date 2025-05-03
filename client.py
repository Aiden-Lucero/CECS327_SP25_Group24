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

        # Set up a TCP/IP socket
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            client_socket.connect((serverhost_ipaddress, target_port))  # Try to connect to the server
            print("Connected to the server.\n")
            break  # Exit loop if successful
        except Exception as error:
            print(f"Connection failed: {error}. Please try again.")

    # Valid queries
    valid_queries = {
        "1": "What is the average moisture inside my kitchen fridge in the past three hours?",
        "2": "What is the average water consumption per cycle in my smart dishwasher?",
        "3": "Which device consumed more electricity among my three IoT devices?"
    }

    while True:
        print("\n--- IoT Query Menu ---")
        print("1. Fridge moisture (last 3 hours)")
        print("2. Dishwasher water per cycle")
        print("3. Electricity comparison")
        print("Type 'exit' to quit")
        
        choice = input("Enter your selection (1-3 or 'exit'): ").strip().lower()

        if choice == 'exit':
            print("Closing client. Goodbye!")
            break

        if choice in valid_queries:
            message = valid_queries[choice]
        else:
            print("Invalid selection. Please try again.")
            continue

        try:
            client_socket.send(message.encode('utf-8'))  # Send the message to the server
            reply = client_socket.recv(1024)  # Wait for the server's reply
            print(f"\nServer's reply: {reply.decode('utf-8')}")
        except Exception as error:
            print(f"Error: {error}")
            break

    client_socket.close()

connect_to_server()
