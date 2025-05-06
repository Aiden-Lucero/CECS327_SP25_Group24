import socket
import psycopg2
from datetime import datetime, timedelta, timezone
import pytz

DATABASE_URL = "postgresql://neondb_owner:npg_pzlBau1X0EHR@ep-shiny-cake-a5aimshz-pooler.us-east-2.aws.neon.tech/neondb?sslmode=require"

DEVICES = {
    "fridge": "y9t-tjc-926-i1h",
    "dishwasher": "ed859356-9ac0-4320-8b23-2453160a466c",
    "fridge2": "06d2bba7-a708-42c7-b70b-db4c1a40e67f"
}

PST = pytz.timezone("America/Los_Angeles")

def open_connection():
    try:
        return psycopg2.connect(DATABASE_URL, sslmode="require")
    except Exception as error:
        print(f"DB Connection Error: {error}")
        return None

def fetch_avg_moisture(cursor):
    pst_now = datetime.now(PST)
    threshold = pst_now - timedelta(hours=3)
    threshold_utc = threshold.astimezone(timezone.utc)
    cursor.execute("""
        SELECT AVG((payload->>'DHT11 - DHT11-moisture')::float)
        FROM fridge_data_virtual
        WHERE time >= %s
    """, (threshold_utc,))
    moisture = cursor.fetchone()
    return (f"The average moisture inside kitchen fridge in the past three hours is {round(moisture[0], 2)} % RH."
            if moisture and moisture[0] is not None else
            "No moisture data available in the past three hours.")

def fetch_avg_water(cursor):
    pst_now = datetime.now(PST)
    threshold = pst_now - timedelta(hours=3)
    threshold_utc = threshold.astimezone(timezone.utc)
    cursor.execute("""
        SELECT AVG((payload->>'YF-S201-water')::float)
        FROM fridge_data_virtual
        WHERE time >= %s
    """, (threshold_utc,))
    water = cursor.fetchone()
    return (f"The average water consumption per cycle is {round(water[0] * 0.264172, 2)} gallons."
            if water and water[0] is not None else
            "No water usage data available.")

def fetch_electricity(cursor):
    usage = {}

    device_map = {
        "kitchen fridge": ("fridge", "ACS712 - ACS712-electricity"),
        "garage fridge": ("fridge2", "ACS712-electricity2"),
        "dishwasher": ("dishwasher", "ACS712-electricity3")
    }

    for label, (key, sensor) in device_map.items():
        cursor.execute("""
            SELECT SUM((payload->>%s)::float)
            FROM fridge_data_virtual
            WHERE payload->>'parent_asset_uid' = %s
        """, (sensor, DEVICES[key]))
        total = cursor.fetchone()
        # divide by 1000 to convert watts to kilowatts
        usage[label] = (total[0] / 1000) if total and total[0] is not None else 0

    top_device = max(usage, key=usage.get)
    return f"Among your three IoT devices, the {top_device} consumed the most electricity: {round(usage[top_device], 2)} kWh."


def process_request(query: str, cursor):
    query = query.lower()
    if "average moisture" in query:
        return fetch_avg_moisture(cursor)
    if "average water" in query:
        return fetch_avg_water(cursor)
    if "consumed more electricity" in query or "which device consumed more electricity" in query:
        return fetch_electricity(cursor)
    return ("Sorry, this query cannot be processed. Try one of:") + "\n".join([
        "1. What is the average moisture inside my kitchen fridge in the past three hours?",
        "2. What is the average water consumption per cycle in my smart dishwasher?",
        "3. Which device consumed more electricity among my three IoT devices (two refrigerators and a dishwasher)?"])


def start_server():
    hostname = socket.gethostname()
    host = socket.gethostbyname(hostname)
    port = int(input("Enter port to listen on: "))

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
