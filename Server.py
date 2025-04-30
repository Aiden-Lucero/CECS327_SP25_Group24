import socket
import psycopg2
from datetime import datetime
import pytz

# DB connection setup
def connect_db():
    return psycopg2.connect(
        host="ep-lucky-frog-a5iylka4-pooler.us-east-2.aws.neon.tech",
        dbname="neondb",
        user="neondb_owner",
        password="npg_DyqlpcH3vuL8",
        port=5432
    )

def get_pst_now():
    now_utc = datetime.utcnow().replace(tzinfo=pytz.utc)
    return now_utc.astimezone(pytz.timezone('US/Pacific'))

# Query 1: Fridge Moisture
def get_avg_moisture():
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("""
        SELECT AVG(length)
        FROM fridge_data_virtual
        WHERE topic = 'home/kitchen/fridge'
        AND time >= NOW() - INTERVAL '3 hours';
    """)
    avg = cur.fetchone()[0]
    conn.close()
    if avg is None:
        return "No recent fridge data available."
    rh = round((avg / 500) * 100, 2)
    return f"Average fridge moisture (past 3 hrs): {rh}% RH (as of {get_pst_now().strftime('%Y-%m-%d %I:%M %p PST')})"

# Query 2: Dishwasher Water
def get_avg_water_usage():
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("""
        SELECT AVG(length)
        FROM fridge_data_virtual
        WHERE topic = 'home/kitchen/dishwasher'
        AND length > 0;
    """)
    avg = cur.fetchone()[0]
    conn.close()
    if avg is None:
        return "No dishwasher data available."
    gallons = round(avg * 0.264172, 2)
    return f"Average water per cycle: {gallons} gallons"

# Query 3: Electricity Comparison
def compare_electricity():
    conn = connect_db()
    cur = conn.cursor()
    device_topics = {
        "Fridge 1": "home/kitchen/fridge1",
        "Fridge 2": "home/kitchen/fridge2",
        "Dishwasher": "home/kitchen/dishwasher"
    }
    results = {}
    for name, topic in device_topics.items():
        cur.execute("""
            SELECT SUM(length)
            FROM fridge_data_virtual
            WHERE topic = %s;
        """, (topic,))
        total = cur.fetchone()[0]
        if total is None:
            total = 0
        kwh = round(total / 1000, 2)
        results[name] = kwh
    conn.close()
    most = max(results, key=results.get)
    return f"{most} used the most electricity: {results[most]} kWh"

#original socket code
def launch_server():
    serverhost_ipaddress = '0.0.0.0'
    listening_port = int(input("Enter the port number for the server: "))

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((serverhost_ipaddress, listening_port))
    server_socket.listen(5)

    print(f"Server started. Listening on {serverhost_ipaddress}:{listening_port}...")

    while True:
        client_socket, client_address = server_socket.accept()
        print(f"Connection established with {client_address}")

        while True:
            try:
                message = client_socket.recv(1024)
                if not message:
                    break

                query = message.decode('utf-8').strip().lower()
                print(f"Received from {client_address}: {query}")

                # Assignment 8 query handling
                if "moisture" in query:
                    response = get_avg_moisture()
                elif "water consumption" in query:
                    response = get_avg_water_usage()
                elif "electricity" in query or "consumed more" in query:
                    response = compare_electricity()
                else:
                    response = (
                        "Sorry, this query cannot be processed.\n"
                        "Please try one of the following:\n"
                        "- What is the average moisture inside my kitchen fridge in the past three hours?\n"
                        "- What is the average water consumption per cycle in my smart dishwasher?\n"
                        "- Which device consumed more electricity among my three IoT devices?"
                    )

                client_socket.send(response.encode())

            except ConnectionResetError:
                print(f"Connection lost with {client_address}. Waiting for a new connection.")
                break

        client_socket.close()

launch_server()
