#!/bin/bash

# Path to your Python script
script_path="/data/data/com.termux/files/home/pingdata_collection/airtel/DataCollection2.py"

data_dir="/data/data/com.termux/files/home/pingdata_collection/airtel/data"

# Check if the data directory exists, and if not, create it
if [ ! -d "$data_dir" ]; then
  mkdir -p "$data_dir"
fi

# Path to your Git repository
repository_path="/data/data/com.termux/files/home/pingdata_collection"

# Specify the starting time as "1645" for 16:45
start_time="2305"  # Use your desired start time in HHMM format

# Specify the starting date in 'YYYY-MM-DD' format
start_date="2023-11-07"  # Use your desired starting date

# Specify the number of days to run
days_to_run=1
iteration=0

# Run the script once a day for 15 days starting from the specified date
while [ $iteration -lt $days_to_run ]; do
    # Get the current date in 'YYYY-MM-DD' format
    current_date=$(date -d "$start_date + $iteration days" +'%Y-%m-%d")

    # Check if it's the time to run
    current_time=$(date +'%H%M')
    if [ "$current_time" -ge "$start_time" ]; then
        echo "Running the script for $current_date at $current_time..."

        # Schedule the script to run in the background
        python3 "$script_path" &

        # Wait for the current iteration to complete
        wait

        echo "Script for $current_date completed."
        iteration=$((iteration + 1))

        # Configure your Git identity
        git config --global user.email "rishabh20399@iiitd.ac.in"
        git config --global user.name "rishabh20399"

        # After each iteration, commit and push changes to Git
        cd "$repository_path"
        git remote set-url origin git@github.com:rishabh20399/pingdata_collection.git

        git checkout -b my-changes
        git add "$data_dir"
        git commit -m "Add files from data"
        git push origin my-changes
    else
        echo "Waiting for the scheduled time..."
        sleep 60  # Sleep for 1 minute before checking the time again
    fi

    # Increment the iteration count
    iteration=$((iteration + 1))
done
