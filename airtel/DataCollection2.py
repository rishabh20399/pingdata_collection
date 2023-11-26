import subprocess
import requests
import re
import numpy as np
from datetime import datetime
import os
import csv
import socket

# Function to collect ping data for a domain
def collect_ping_data(num, domain, ping_count, ping_size):
    # Lists to store data for each ping
    data = []
    
    # for i in range(ping_count):
        

    for _ in range(ping_count):
        # data.append([""] * 9)
        # data[num][0] =domain

        data_point = [""] * 9
        data_point[0] = domain
        try:
            # data_point = [""] * 9
            # data_point[0] = domain

            # Run the ping command for IPv4
            start_time = datetime.now()
            ping_result_v4 = subprocess.check_output(['ping', '-c', '1', '-s', str(ping_size), domain], text=True)
            end_time = datetime.now()
            execution_time_ms_v4 = (end_time - start_time).total_seconds() * 1000

            # IPv4 result
            ip_match_v4 = re.search(r'PING (.+) \((\d+\.\d+\.\d+\.\d+)\)', ping_result_v4)
            latency_match_v4 = re.findall(r'time=(\d+\.\d+) ms', ping_result_v4)

            if ip_match_v4 and latency_match_v4:
                # domain_name = domain
                ipv4_address = ip_match_v4.group(2)
                latency_v4 = [float(latency) for latency in latency_match_v4]

                # Get geolocation based on IPv4 address using ip-api.com
                geolocation_response_v4 = requests.get(f'http://ip-api.com/json/{ipv4_address}')
                geolocation_data_v4 = geolocation_response_v4.json()
                geolocation_info_v4 = f"{geolocation_data_v4['city']}, {geolocation_data_v4['regionName']}, {geolocation_data_v4['country']}"

                # print("dfbfbrtbwrbrbrtbr---1")
                data_point[1] = ipv4_address
                data_point[3] = str(latency_v4)
                data_point[5] = geolocation_info_v4
                data_point[7] = str(execution_time_ms_v4)

            # print("dfbfbrtbwrbrbrtbr---1.5")
            # Run the ping6 command for IPv6
            start_time = datetime.now()
            ping_result_v6 = subprocess.check_output(['ping6', '-c', '1', '-s', str(ping_size), domain], text=True)
            end_time = datetime.now()
            execution_time_ms_v6 = (end_time - start_time).total_seconds() * 1000

            # IPv6 result
            ip_match_v6 = re.search(r'PING (.+?)\(([^)]+)\)', ping_result_v6)
            latency_match_v6 = re.findall(r'time=(\d+\.\d+) ms', ping_result_v6)

            # print(latency_match_v6)
            if ip_match_v6 and latency_match_v6:
                # print("dfbfbrtbwrbrbrtbr---1.6")
                domain_name = ip_match_v6.group(2)
                ipv6_address = None  # Initialize to None
                latency_v6 = [float(latency) for latency in latency_match_v6]

                # Get geolocation based on IPv6 address using ip-api.com
                geolocation_response_v6 = requests.get(f'http://ip-api.com/json/{domain_name}')
                geolocation_data_v6 = geolocation_response_v6.json()
                geolocation_info_v6 = f"{geolocation_data_v6['city']}, {geolocation_data_v6['regionName']}, {geolocation_data_v6['country']}"

                # Extract IPv6 address from the regex match
                ipv6_match = ip_match_v6.group(1)
                ipv6_address = socket.getaddrinfo(ipv6_match, None, socket.AF_INET6)[0][4][0]

                # print("dfbfbrtbwrbrbrtbr---2" + ipv6_address)
                data_point[2] = ipv6_address
                data_point[4] = str(latency_v6)
                data_point[6] = geolocation_info_v6
                data_point[8] = str(execution_time_ms_v6)


        except subprocess.CalledProcessError as e:
            print(f"Error pinging {domain}: {e}")

        data.append(data_point)
        num +=1 

    return data

# Read websites from a text file
with open('/data/data/com.termux/files/home/pingdata_collection/airtel/domain_list2.txt', 'r') as file:
    domain_names = file.read().splitlines()

# Set the number of pings and ping size
ping_count = 40
ping_size = 64
num=0

# Get the current date and time
now = datetime.now()
date_str = now.strftime("%d_%m_%y")

# Create a subdirectory for the current day
day_dir = os.path.join('/data/data/com.termux/files/home/pingdata_collection/airtel/data/', date_str)
os.makedirs(day_dir, exist_ok=True)

# Create a CSV file with a timestamp as the name for the current run
timestamp_str = now.strftime("%H_%M_%S")
csv_file = os.path.join(day_dir, f'{timestamp_str}.csv')

# Initialize the data list
data = []

# Collect and append data for each domain

# for domain in domain_names:
#     data = collect_ping_data(num, domain, ping_count, ping_size)
#     num +=ping_count

for domain in domain_names:
    data.extend(collect_ping_data(num, domain, ping_count, ping_size))

# Append data to the CSV file
with open(csv_file, 'a', newline='') as csvf:
    # Add the column names if they are not already added
    csv_writer = csv.writer(csvf)
    if os.path.getsize(csv_file) == 0:
        csv_writer.writerow(["Domain", "IPv4 Address", "IPv6 Address", "IPv4 Latency (ms)", "IPv6 Latency (ms)", "IPv4 Geolocation", "IPv6 Geolocation", "IPv4 Execution Time (ms)", "IPv6 Execution Time (ms)"])

    for row in data:
        # Append the data to the CSV file
        csv_writer.writerow(row)

print(f"Data saved to {csv_file}")
