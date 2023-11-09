import re
import csv
import os
from datetime import datetime
import subprocess

# Input text file with domain names
input_file = "domain_list2.txt"

# Get the current date and time
now = datetime.now()
date_str = now.strftime("%d_%m_%y")
time_str = now.strftime("%H_%M_%S")

# Create a subdirectory for the current day
day_dir = os.path.join('/data/data/com.termux/files/home/pingdata_collection/airtel/data/traceroute/', date_str)
os.makedirs(day_dir, exist_ok=True)

# Name the output CSV file by time
output_csv_file = os.path.join(day_dir, f"{time_str}.csv")

# Initialize a list to store traceroute data
traceroute_data = []

# Open and read the input text file with domain names
with open(input_file, "r") as file:
    domains = file.read().splitlines()

# Process the traceroute for each domain
times_list=[]
for domain in domains:
    try:
        traceroute_result = subprocess.check_output(['traceroute', '-q', '1', domain], text=True)

        # Extract hop information from traceroute result
        hop_data = re.findall(r'\d+\s+([\w.]+)\s+\(([\d.]+)\)\s+(.+) ms', traceroute_result)

        if hop_data:
            # Append the extracted data to the list
            for hop, ip, times in hop_data:
                times_list = times.split(" ")
                traceroute_data.append([domain, hop, ip] + times_list)
    except subprocess.CalledProcessError as e:
        print(f"Error running traceroute for {domain}: {e}")

# Write the data to a CSV file
with open(output_csv_file, "w", newline="") as csv_file:
    csv_writer = csv.writer(csv_file)
    header = [ "Domain", "Hop", "IP"]
    header.extend([f"Time {i+1} (ms)" for i in range(len(times_list))])
    csv_writer.writerow(header)
    csv_writer.writerows(traceroute_data)

print(f"Traceroute data has been saved to {output_csv_file}")
