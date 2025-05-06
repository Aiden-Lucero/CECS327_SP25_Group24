import socket

def get_server_details():
    ip = input("Enter server IP address: ").strip()
    port_input = input("Enter server port: ").strip()
    try:
        port = int(port_input)
        return ip, port
    except ValueError:
        print("Port must be an integer.")
        exit()

def create_connection(ip, port):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((ip, port))
        return s
    except socket.error as err:
        print(f"Socket Error: {err}")
        exit()

def display_options(options):
    print("\nSelect a query by entering its number:")
    for i, opt in enumerate(options, 1):
        print(f"{i}. {opt}")

def main():
    queries = [
        "What is the average moisture inside my kitchen fridge in the past three hours?",
        "What is the average water consumption per cycle in my smart dishwasher?",
        "Which device consumed more electricity among my three IoT devices (two refrigerators and a dishwasher)?"
    ]

    ip, port = get_server_details()
    sock = create_connection(ip, port)

    while True:
        display_options(queries)
        user_input = input("\nEnter query number or type 'exit' to quit: ").strip().lower()

        if user_input == 'exit':
            sock.send(b'exit')
            break

        try:
            index = int(user_input)
            if 1 <= index <= len(queries):
                sock.send(queries[index - 1].encode('utf-8'))
                reply = sock.recv(4096).decode('utf-8')
                print(f"Server Response: {reply}")
            else:
                print("Number out of range. Please choose a valid option.")
        except ValueError:
            print("Invalid input. Enter a number corresponding to a query.")

    sock.close()

if __name__ == "__main__":
    main()
