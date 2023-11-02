#!/bin/bash

# Path to your Python script
script_path="$HOME/pingdata_collection/airtel/DataCollection2.py"

# Path to your Git repository
repository_path="$HOME/pingdata_collection"

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

    # After 4 iterations, commit and push changes to Git
    if [[ $iteration -eq 3 ]]; then
        cd "$repository_path"
        git add .
        git commit -m "Automated data collection"
        git push
        cd "$HOME"  # Return to the home directory
    fi
done
