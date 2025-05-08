# CECS 327 – Assignment 8: IoT TCP Server + Client
#Stephanie Figueroa and Aiden Lucero

#Project Description

This project implements a full-stack Iot system using a TCP client-server model to respond to real-world sensor data queries. The server connects to a Neon-hosted PostgreSQL database populated by the Dataniz Iot simulator. The system handles three predefined queries about moisture, water usage, and electricity consumption from smart appliances:
- Average moisture inside the kitchen fridge (last 3 hours)
- Average water consumption per dishwasher cycle
- Electricity usage comparison among 3 IoT devices

#Features
- TCP server that processes and responds to 3 specific IOT queries
- Python client with a menu-based interface
- Connects to a Neon PostgreSQL cloud database
- Processes sensor metadata from'Fridge_data_virtual` table
- Performs unit conversions:
  - Moisture → RH% (Relative Humidity)
  - Water usage → Gallons
  - Electricity → kWh
  - converts all timestamps to Pacific standard time (PST)
- supports JSON payloads using PostgreSQL's JSONB query syntax

#Technologies Used
- Python 3
- Sockets module for TCP communication
- PostgreSQL via Neon Console
- 'psycopg2` for PostgreSQL access
- Dataniz for simulating IOT sensor data
- Git + GitHub for version control

#How to Run the Project

#1. Start the Server
Make sure you have Python installed and 'psycopg2' and 'pytz' installed:

'''bash
pip install psycopg2-binary pytz

#then run the server:
python server.py

#youll be asked to enter a port number 
(4000)

#2. Start the client
#Then run server
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
data comes in as JSON payloads with fields like 
- DHT11 - DHT11-moisture (fridge moisture)
- YF-S201-water (dishwasher water flow)
- ACS712-electricity, ACS712-electricity2, etc. (wattage for each device)
each device is identified using a unique parent_asset_uid in the payload:
1.fridge
2.dishwasher
3.fridge 2
Queries filtered based on both sensor field and device UID
Moisture values are averaged over the last 3 hours and converted to RH%
Moisture values are converted to %RH using: (avg / 500) * 100
Water usage values are converted to gallons using: liters * 0.264172
Electricity is calculated in kWh by summing values and dividing by 1000

#Testing Notes
To simulate data:
Connect Dataniz to the fridge_data_virtual table
Use topics like:
- home/kitchen/fridge1
- home/kitchen/fridge2
- home/kitchen/dishwasher
Ensure your Dataniz sensors are sending fields that match the SQL keys in your code

Team
- Stephanie (added code for both client and server, did readme.md, and report)
- Aiden ( fixed code errors, configured dataniz and databse, tested the code and data)

Feedback:
Dataniz was a powerful and simple tool for injecting live IoT data. The interface made it easy to 
connect to PostgreSQL and simulate real sensor values. A few improvements would be to include better
error feedback when no data is streaming and to allow test previews of sample payloads during setup.









