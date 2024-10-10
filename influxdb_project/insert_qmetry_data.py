import json
import time
from influxdb import InfluxDBClient
from requests.exceptions import ConnectionError

# Retry settings
max_retries = 10  # Number of retries
retry_wait = 5  # Seconds to wait between retries

# Function to connect to InfluxDB
def connect_to_influxdb(host, port, retries, wait):
    for attempt in range(retries):
        try:
            client = InfluxDBClient(host=host, port=port)
            client.switch_database('qmetry_data')
            print("Successfully connected to InfluxDB.")
            return client
        except ConnectionError:
            print(f"Attempt {attempt + 1}/{retries} failed: InfluxDB is not ready. Retrying in {wait} seconds...")
            time.sleep(wait)
    raise Exception("Failed to connect to InfluxDB after multiple attempts.")

# Step 1: Load the QMetry JSON data from the file
with open('qmetry_data.json') as json_file:
    qmetry_data = json.load(json_file)

# Step 2: Connect to InfluxDB with retries
client = connect_to_influxdb('influxdb', 8086, max_retries, retry_wait)

# Step 3: Prepare the data for InfluxDB
influx_data = []
for execution in qmetry_data['results']:
    influx_data.append({
        "measurement": "test_executions",
        "tags": {
            "execution_id": execution['id'],
            "status": execution['status'],
            "test_cycle": execution['test_cycle'],
            "executed_by": execution['executed_by']
        },
        "fields": {
            "duration": execution['duration']
        },
        "time": execution['start_time']
    })

# Step 4: Write the data to InfluxDB
client.write_points(influx_data)

print("QMetry test results inserted into InfluxDB successfully!")

