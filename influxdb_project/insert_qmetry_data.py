import time
import json
import os
from influxdb import InfluxDBClient

# Configuration
influxdb_host = os.getenv('INFLUXDB_HOST', 'influxdb')
influxdb_port = 8086
influxdb_database = 'qmetry_data'
qmetry_data_file = 'qmetry_data.json'
retries = 10
wait = 5

# Connect to InfluxDB
client = InfluxDBClient(host=influxdb_host, port=influxdb_port)

# Retry logic in case InfluxDB is not ready
for attempt in range(retries):
    try:
        client.create_database(influxdb_database)
        print("Successfully connected to InfluxDB.")
        break
    except Exception as e:
        print(f"Attempt {attempt + 1}/{retries} failed: {e}. Retrying in {wait} seconds...")
        time.sleep(wait)
else:
    raise Exception(f"Failed to connect to InfluxDB after {retries} retries.")

# Set the database
client.switch_database(influxdb_database)

# Load QMetry data from JSON file
with open(qmetry_data_file, 'r') as json_file:
    qmetry_data = json.load(json_file)

# Prepare data in InfluxDB format
influx_data = [
    {
        "measurement": "test_executions",
        "tags": {
            "test_case_id": result["id"],
            "status": result["status"]
        },
        "fields": {
            "duration": result["duration"],
            "executed_by": result["executed_by"],
            "test_cycle": result["test_cycle"]
        },
        "time": result["start_time"]
    }
    for result in qmetry_data['results']
]

# Insert data into InfluxDB
client.write_points(influx_data)

print("QMetry data has been inserted into InfluxDB.")

