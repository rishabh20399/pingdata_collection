#!/bin/bash

# Path to your Python script
script_path="/home/useland/pingdata_collection/airtel/DataCollection2.py"

# Path to your Git repository
repository_path="/home/useland/pingdata_collection"

# Specify the starting time as "2200" for 22:00
start_time="1645"  # Use your desired start time in HHMM format

# Get the current date in 'YYYY-MM-DD' format
current_date=$(date +'%Y-%m-%d')

# Loop for 4 iterations
for ((iteration=0; iteration<4; iteration++)); do
    execution_time="$current_date $start_time"

    # Wait for the previous iteration to complete (if not the first iteration)
    if [[ $iteration -gt 0 ]]; then
        while jobs %% &>/dev/null; do
            sleep 600  # Wait for 600 seconds before checking again
        done
    fi

    # Schedule the script using 'at'
    echo "python3 $script_path" | at "$execution_time"
    echo "Scheduled python script to run at $execution_time"
done

# Wait for all iterations to complete
while jobs %% &>/dev/null; do
    sleep 600
done

