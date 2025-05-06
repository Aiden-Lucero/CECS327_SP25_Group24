# CECS 327 – Assignment 8: IoT TCP Server + Client
#Stephanie Figueroa and Aiden Lucero

#Project Description
This project is an end-to-end IoT system that uses a TCP client-server model to process 
and respond to real-world IoT queries. It connects to a Neon-hosted PostgreSQL database 
populated via Dataniz and supports the following queries:

- Average moisture inside the kitchen fridge (last 3 hours)
- Average water consumption per dishwasher cycle
- Electricity usage comparison among 3 IoT devices

#Features
- TCP server that accepts and responds to 3 specific queries
- Python client with user-friendly menu
- Connects to Neon PostgreSQL database
- Processes IoT data from 'Fridge_data_virtual` table
- Performs unit conversions:
  - Moisture → RH% (Relative Humidity)
  - Water usage → Gallons
  - Electricity → kWh
- Displays all timestamps in Pacific Standard Time (PST)

#Technologies Used
- Python 3
- Sockets (`socket' library)
- PostgreSQL via Neon Console
- 'psycopg2` (PostgreSQL driver)
- Dataniz IoT device simulator
- Git + GitHub for version control

#How to Run the Project

#1. Start the Server
Make sure you have Python installed and Neon credentials set in 'server.py`

'''bash
python server.py

youll be asked to enter a port number (4000)

#2. Start the client
'''bash
python client.py

you'll be asked to enter the server's IP address and the same port number used in the server

#3. choose from the Menu
You’ll be shown a numbered menu to select one of the following:
What is the average moisture inside my kitchen fridge in the past three hours?
What is the average water consumption per cycle in my smart dishwasher?
Which device consumed more electricity among my three IoT devices?
If you enter an unsupported query, the server will provide guidance on valid options.

#File structure
server.py -Main server script
client.py - client that sends queries 
README.md - what you are reading now

#Iot notes
All sensor data is stored in the fridge_data_virtual table
Queries are filtered by topic field (home/kitchen/fridge, etc)
Moisture values are converted to %RH using: (avg / 500) * 100
Water usage values are converted to gallons using: liters * 0.264172
Electricity is calculated in kWh by summing values and dividing by 1000








