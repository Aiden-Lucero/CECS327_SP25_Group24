import socket
import psycopg2
from datetime import datetime, timedelta, timezone

DATABASE_URL = "postgresql://neondb_owner:npg_pzlBau1X0EHR@ep-shiny-cake-a5aimshz-pooler.us-east-2.aws.neon.tech/neondb?sslmode=require"

DEVICES = {
    "fridge": "y9t-tjc-926-i1h",
    "dishwasher": "ed859356-9ac0-4320-8b23-2453160a466c",
    "fridge2": "06d2bba7-a708-42c7-b70b-db4c1a40e67f"
}

def open_connection():
    try:
        return psycopg2.connect(DATABASE_URL, sslmode="require")
    except Exception as error:
        print(f"DB Connection Error: {error}")
        return None

def fetch_avg_moisture(cursor):
    threshold = datetime.now(timezone.utc) - timedelta(hours=3)
    cursor.execute("""
        SELECT AVG((payload->>'DHT11-moisture')::float)
        FROM fridge_data_virtual
        WHERE time >= %s
    """, (threshold,))
    moisture = cursor.fetchone()
    return (f"The average moisture inside kitchen fridge in the past three hours is {round(moisture[0], 2)} % RH."
            if moisture and moisture[0] is not None else
            "No moisture data available in the past three hours.")

def fetch_avg_water(cursor):
    threshold = datetime.now(timezone.utc) - timedelta(hours=3)
    cursor.execute("""
        SELECT AVG((payload->>'YF-S201 - YFS201-Water')::float)
        FROM fridge_data_virtual
        WHERE time >= %s
    """, (threshold,))
    water = cursor.fetchone()
    return (f"The average water consumption per cycle is {round(water[0] * 0.264172, 2)} gallons."
            if water and water[0] is not None else
            "No water usage data available.")

def fetch_electricity(cursor):
    readings = {}
    fields = {
        "fridge": "ACS712 - ACS712-electricity",
        "fridge2": "ACS712-electricity2",
        "dishwasher": "ACS712-electricity3"
    }
    for name, sensor in fields.items():
        cursor.execute("""
            SELECT SUM((payload->>%s)::float)
            FROM fridge_data_virtual
            WHERE payload->>'parent_asset_uid' = %s
        """, (sensor, DEVICES[name]))
        total = cursor.fetchone()
        readings[name] = total[0] if total and total[0] is not None else 0

    top_device = max(readings, key=readings.get)
    return f"{top_device} consumed the most electricity: {round(readings[top_device], 2)} kWh."

def process_request(query: str, cursor):
    query = query.lower()
    if "average moisture" in query:
        return fetch_avg_moisture(cursor)
    if "average water" in query:
        return fetch_avg_water(cursor)
    if "consumed more electricity" in query:
        return fetch_electricity(cursor)
    return ("Sorry, this query cannot be processed. Try one of:") + "\n".join([
        "1. What is the average moisture inside my kitchen fridge in the past three hours?",
        "2. What is the average water consumption per cycle in my smart dishwasher?",
        "3. Which device consumed more electricity among my three IoT devices (two refrigerators and a dishwasher)?"])

def start_server(host='10.128.0.2', port=4000):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as srv:
        srv.bind((host, port))
        srv.listen(5)
        print(f"Server listening on {host}:{port}")

        while True:
            client, addr = srv.accept()
            print(f"Connected to {addr}")

            conn = open_connection()
            if not conn:
                client.send(b"Database connection failed.")
                client.close()
                continue

            cursor = conn.cursor()
            try:
                while True:
                    data = client.recv(5000).decode("utf-8").strip()
                    if not data or data.lower() in ("exit", "quit"):
                        print(f"Client {addr} disconnected.")
                        break

                    print(f"Client says: {data}")
                    response = process_request(data, cursor)
                    client.send(response.encode("utf-8"))
            except Exception as ex:
                print(f"Client error {addr}: {ex}")
            finally:
                cursor.close()
                conn.close()
                client.close()

if __name__ == "__main__":
    start_server()
