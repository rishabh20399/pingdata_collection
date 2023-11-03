import subprocess
import requests
import re
import pandas as pd
from datetime import datetime
import os

# Read websites from a text file
with open('/home/userland/pingdata_collection/airtel/domain_list2.txt', 'r') as file:
    domain_names = file.read().splitlines()

# Get the current date and time
now = datetime.now()
date_str = now.strftime("%d_%m_%y")
time_str = now.strftime("%H_%M_%S")

# Specify the directory where Excel files are stored
excel_dir = '/home/userland/pingdata_collection/airtel/data/'

# Check if the Excel file for the current day already exists or create a new one
excel_file = os.path.join(excel_dir, f'{date_str}.xlsx')
if not os.path.exists(excel_file):
    # Create a DataFrame with columns but no data
    df_empty = pd.DataFrame(columns=['Domain', 'IPv4 address', 'IPv6 address', 'IPv4 latency (ms)', 'IPv6 latency (ms)', 'IPv4 geolocation', 'IPv6 geolocation', 'Time Taken (ms) IPv4', 'Time Taken (ms) IPv6'])
    with pd.ExcelWriter(excel_file, engine='openpyxl') as excel_writer:
        df_empty.to_excel(excel_writer, index=False)

# Lists to store results for the current timestamp
domains = []
ipv4_addresses = []
ipv6_addresses = []
latency_v4_list = []
latency_v6_list = []
geolocation_v4_list = []
geolocation_v6_list = []
time_taken_v4_list = []  # Time taken by IPv4
time_taken_v6_list = []  # Time taken by IPv6

for domain in domain_names:
    try:
        # Run the ping command for IPv4
        start_time = datetime.now()
        ping_result_v4 = subprocess.check_output(['ping', '-4', '-c', '40', '-s', '64', domain], text=True)
        end_time = datetime.now()
        execution_time_ms_v4 = (end_time - start_time).total_seconds() * 1000  # Calculate time taken in milliseconds
        # IPv4 result
        ip_match_v4 = re.search(r'Pinging (.+?) \[(\d+\.\d+\.\d+\.\d+)\]', ping_result_v4)
        latency_match_v4 = re.search(r'time=(\d+)ms', ping_result_v4)

        # Run the ping command for IPv6
        start_time = datetime.now()
        ping_result_v6 = subprocess.check_output(['ping', '-6', '-c', '40', '-s', '64', domain], text=True)
        end_time = datetime.now()
        execution_time_ms_v6 = (end_time - start_time).total_seconds() * 1000  # Calculate time taken in milliseconds
        # IPv6 result
        ip_match_v6 = re.search(r'Pinging (.+?) \[([0-9a-fA-F:]+)\]', ping_result_v6)
        latency_match_v6 = re.search(r'time=(\d+)ms', ping_result_v6)

        if ip_match_v4 and latency_match_v4:
            domain_name = domain
            ipv4_address = ip_match_v4.group(2)
            latency_v4 = int(latency_match_v4.group(1))

            # Get geolocation based on IPv4 address using ip-api.com
            geolocation_response_v4 = requests.get(f'http://ip-api.com/json/{ipv4_address}')
            geolocation_data_v4 = geolocation_response_v4.json()
            geolocation_info_v4 = f"{geolocation_data_v4['city']}, {geolocation_data_v4['regionName']}, {geolocation_data_v4['country']}"

            # domains.append(domain_name)
            # ipv4_addresses.append(ipv4_address)
            # ipv6_addresses.append("")
            # latency_v4_list.append(latency_v4)
            # latency_v6_list.append("")
            # geolocation_v4_list.append(geolocation_info_v4)
            # geolocation_v6_list.append("")
            # time_taken_v4_list.append(execution_time_ms_v4)
            # time_taken_v6_list.append("")

        if ip_match_v6 and latency_match_v6:
            domain_name = domain
            ipv6_address = ip_match_v6.group(2)
            latency_v6 = int(latency_match_v6.group(1))

            # Get geolocation based on IPv6 address using ip-api.com
            geolocation_response_v6 = requests.get(f'http://ip-api.com/json/{ipv6_address}')
            geolocation_data_v6 = geolocation_response_v6.json()
            geolocation_info_v6 = f"{geolocation_data_v6['city']}, {geolocation_data_v6['regionName']}, {geolocation_data_v6['country']}"

            domains.append(domain_name)
            ipv4_addresses.append(ipv4_address)
            ipv6_addresses.append(ipv6_address)
            latency_v4_list.append(latency_v4)
            latency_v6_list.append(latency_v6)
            geolocation_v4_list.append(geolocation_info_v4)
            geolocation_v6_list.append(geolocation_info_v6)
            time_taken_v4_list.append(execution_time_ms_v4)
            time_taken_v6_list.append(execution_time_ms_v6)

    except subprocess.CalledProcessError as e:
        print(f"Error pinging {domain}: {e}")

# Create a DataFrame for the current timestamp
df = pd.DataFrame({
    'Domain': domains,
    'IPv4 address': ipv4_addresses,
    'IPv6 address': ipv6_addresses,
    'IPv4 latency (ms)': latency_v4_list,
    'IPv6 latency (ms)': latency_v6_list,
    'IPv4 geolocation': geolocation_v4_list,
    'IPv6 geolocation': geolocation_v6_list,
    'Time Taken (ms) IPv4': time_taken_v4_list,
    'Time Taken (ms) IPv6': time_taken_v6_list
})

# Save the DataFrame to the Excel writer with the time as the sheet name
with pd.ExcelWriter(excel_file, engine='openpyxl', mode='a') as excel_writer:
    df.to_excel(excel_writer, sheet_name=time_str, index=False)
