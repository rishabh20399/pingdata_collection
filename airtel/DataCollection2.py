import subprocess
import requests
import re
import numpy as np
from datetime import datetime
import os
import csv

# Function to collect ping data for a domain
def collect_ping_data(domain, ping_count, ping_size):
    # Lists to store data for each ping
    data = []
    for _ in range(ping_count):
        try:
            # Run the ping command for IPv4
            start_time = datetime.now()
            ping_result_v4 = subprocess.check_output(['ping', '-c', '-4', '-s', ping_size, domain], text=True)
            end_time = datetime.now()
            execution_time_ms_v4 = (end_time - start_time).total_seconds() * 1000

            # IPv4 result
            ip_match_v4 = re.search(r'PING (.+) \((\d+\.\d+\.\d+\.\d+)\)', ping_result_v4)
            latency_match_v4 = re.findall(r'time=(\d+\.\d+) ms', ping_result_v4)

            if ip_match_v4 and latency_match_v4:
                domain_name = domain
                ipv4_address = ip_match_v4.group(2)
                latency_v4 = [float(latency) for latency in latency_match_v4]

                # Get geolocation based on IPv4 address using ip-api.com
                geolocation_response_v4 = requests.get(f'http://ip-api.com/json/{ipv4_address}')
                geolocation_data_v4 = geolocation_response_v4.json()
                geolocation_info_v4 = f"{geolocation_data_v4['city']}, {geolocation_data_v4['regionName']}, {geolocation_data_v4['country']}"

                row = [domain_name, ipv4_address, "", str(latency_v4), "", geolocation_info_v4, "", str(execution_time_ms_v4), ""]
                data.append(row)

            # Run the ping6 command for IPv6
            start_time = datetime.now()
            ping_result_v6 = subprocess.check_output(['ping6', '-c', '-4', '-s', ping_size, domain], text=True)
            end_time = datetime.now()
            execution_time_ms_v6 = (end_time - start_time).total_seconds() * 1000

            # IPv6 result
            ip_match_v6 = re.search(r'PING (.+) \(([^)]+)\)', ping_result_v6)
            latency_match_v6 = re.findall(r'time=(\d+\.\d+) ms', ping_result_v6)

            if ip_match_v6 and latency_match_v6:
                ipv6_address = ip_match_v6.group(2)
                latency_v6 = [float(latency) for latency in latency_match_v6]

                # Get geolocation based on IPv6 address using ip-api.com
                geolocation_response_v6 = requests.get(f'http://ip-api.com/json/{ipv6_address}')
                geolocation_data_v6 = geolocation_response_v6.json()
                geolocation_info_v6 = f"{geolocation_data_v6['city']}, {geolocation_data_v6['regionName']}, {geolocation_data_v6['country']}"

                for i in range(len(data)):
                    if data[i][0] == domain:
                        data[i][2] = ipv6_address
                        data[i][4] = str(latency_v6)
                        data[i][6] = geolocation_info_v6
                        data[i][8] = str(execution_time_ms_v6)
                        break

        except subprocess.CalledProcessError as e:
            print(f"Error pinging {domain}: {e}")

    return data

# Read websites from a text file
with open('/data/data/com.termux/files/home/pingdata_collection/airtel/domain_list2.txt', 'r') as file:
    domain_names = file.read().splitlines()

# Set the number of pings and ping size
ping_count = 40
ping_size = 64

# Get the current date and time
now = datetime.now()
date_str = now.strftime("%d_%m_%y")

# Create a subdirectory for the current day
day_dir = os.path.join('/data/data/com.termux/files/home/pingdata_collection/airtel/data/', date_str)
os.makedirs(day_dir, exist_ok=True)

# Create a CSV file with a timestamp as the name for the current run
timestamp_str = now.strftime("%H_%M_%S")
csv_file = os.path.join(day_dir, f'{timestamp_str}.csv')

# Collect and append data for each domain
for domain in domain_names:
    data = collect_ping_data(domain, ping_count, ping_size)

    # Append data to the CSV file
    with open(csv_file, 'a', newline='') as csvf:
        csv_writer = csv.writer(csvf)
        csv_writer.writerows(data)

print(f"Data saved to {csv_file}")
