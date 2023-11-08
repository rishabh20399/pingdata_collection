import re
import csv
import os
from datetime import datetime

# Input text file with traceroute results
input_file = "domain_list2.txt"

# Get the current date and time
now = datetime.now()
date_str = now.strftime("%d_%m_%y")
time_str = now.strftime("%H_%M_%S")

# Create a subdirectory for the current day
day_dir = os.path.join('/data/data/com.termux/files/home/pingdata_collection/airtel/data/', date_str)
os.makedirs(day_dir, exist_ok=True)

# Name the output CSV file by time
output_csv_file = os.path.join(day_dir, f"{time_str}.csv")

# Initialize a list to store traceroute data
traceroute_data = []

# Open and read the input text file
with open(input_file, "r") as file:
    lines = file.readlines()

# Process the traceroute data
times_list=[]
for line in lines:
    # Use regular expressions to extract relevant information from each line
    match = re.match(r"(\d+)\s+([\w.]+)\s+\(([\d.]+)\)\s+(.+) ms", line)
    if match:
        hop, domain, ip, times = match.groups()
        times_list = times.split(" ")
        # Append the extracted data to the list
        traceroute_data.append([hop, domain, ip] + times_list)

# Write the data to a CSV file
with open(output_csv_file, "w", newline="") as csv_file:
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(["Hop", "Domain", "IP"] + [f"Time {i+1} (ms)" for i in range(len(times_list))])
    csv_writer.writerows(traceroute_data)

print(f"Traceroute data has been saved to {output_csv_file}")
