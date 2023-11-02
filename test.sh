#!/bin/bash

# Path to your Python script
script_path="$HOME/repository_name/Airtel/DataCollection2.py"

# Specify the starting time to run your script
start_time="22:00"

# Schedule the script for the next 15 days
for ((day=0; day<15; day++)); do
    current_date=$(date +'%Y-%m-%d')
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
        start_time="$(date -d "$start_time +1 minute" +'%H:%M')"
    done
done
