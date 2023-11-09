#!/bin/bash

# Specify the starting time in HH:MM format (24-hour format)
start_time="21:08"  # Set your desired start time here

# Number of days to run the script
total_days=1

# Path to your Python script
script1_path="/data/data/com.termux/files/home/pingdata_collection/airtel/DataCollection2.py"
script2_path="/data/data/com.termux/files/home/pingdata_collection/airtel/tracerouteData.py"

# Path to your Git repository
repository_path="/data/data/com.termux/files/home/pingdata_collection"

# Get the current date in 'YYYY-MM-DD' format
current_date=$(date +'%Y-%m-%d')

# Calculate the timestamp of the start time
start_timestamp=$(date -d "$current_date $start_time" +'%s')

# Start loop to run the script for 15 days
for ((day=1; day<=$total_days; day++)); do
    # Calculate the timestamp for the next run
    next_run_timestamp=$((start_timestamp + (day - 1) * 86400))  # 86400 seconds in a day

    # Calculate the wait time until the next run
    wait_time=$((next_run_timestamp - $(date +'%s')))

    # Check if the wait time is negative (in case the current time is after the scheduled time)
    if [ $wait_time -lt 0 ]; then
        # The next run should be scheduled for the same time on the next day
        wait_time=$((wait_time + 86400))  # 86400 seconds in a day
    fi

    # Wait until the next run time
    echo "Waiting for the scheduled time..."
    sleep $wait_time

    # Print a message for each iteration
    echo "Day $day: Running at $(date +'%H:%M:%S')..."

    # Schedule the script to run in the background and detach it from the terminal
    echo "Running ping data collection..."
    nohup python3 "$script1_path" >/dev/null 2>&1 &

    # Run script2 in the background
    echo "Running traceroute data collection..."
    nohup python3 "$script2_path" >/dev/null 2>&1 &

    # Configure your Git identity
    git config --global user.email "rishabh20399@iiitd.ac.in"
    git config --global user.name "rishabh20399"
    # git config --global init.defaultBranch main

    # After all 4 iterations, commit and push changes to Git
    cd /data/data/com.termux/files/home/pingdata_collection
    git remote set-url origin git@github.com:rishabh20399/pingdata_collection.git

    git checkout -b my-changes
    git add /data/data/com.termux/files/home/pingdata_collection/airtel/data
    git commit -m "Auto commit at $(date +'%Y-%m-%d %H:%M:%S')"
    git push origin my-changes


    echo "Done for the day..."
done

# You can add code here to commit and push your changes to Git

# Keep the script running in the background indefinitely
while true; do
    sleep 3600  # Sleep for 1 hour to keep the script active
done
