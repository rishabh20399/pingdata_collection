#!/bin/bash

# Path to your Python script
script_path="/home/useland/pingdata_collection/airtel/DataCollection2.py"

# Path to your Git repository
repository_path="/home/useland/pingdata_collection"

# Specify the starting time as "1645" for 16:45
start_time="1645"  # Use your desired start time in HHMM format

# Get the current date in 'YYYY-MM-DD' format
current_date=$(date +'%Y-%m-%d')

# Loop for 4 iterations
for ((iteration=0; iteration<4; iteration++)); do
    execution_time="$current_date $start_time"

    # Schedule the script to run in the background
    python3 "$script_path" &

    # Wait for the current iteration to complete
    wait


    # Print a message for each iteration
    echo "Iteration $((iteration + 1)) completed"

done

# After all 4 iterations, commit and push changes to Git
cd "$repository_path"
# Include your Git commands for add, commit, and push here

cd "/home/"  # Return to the home directory
