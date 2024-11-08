# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory
WORKDIR /usr/src/app

# Copy the current directory contents into the container at /usr/src/app
COPY . .

# Install the InfluxDB Python client
RUN apt-get update && apt-get install -y curl && pip install influxdb

# Run the insert_qmetry_data.py script
CMD ["python", "./insert_qmetry_data.py"]

