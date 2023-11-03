#!/bin/bash

# Path to your Python script
script_path="/home/useland/pingdata_collection/airtel/DataCollection2.py"

# Path to your Git repository
repository_path="/home/useland/pingdata_collection"

# # Username and password (replace with your actual credentials)
# username="your_username"
# password="your_password"

# Specify the starting time as "22:00"
start_time="16:05"

# Loop for 4 iterations
for ((iteration=0; iteration<4; iteration++)); do
    execution_time="$(date +'%Y-%m-%d') $start_time"

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

# # After all 4 iterations, commit and push changes to Git
# cd "$repository_path"

# # Set Git credentials (use a secure method, e.g., SSH keys or credential manager)
# # Replace the following line with a secure credential setup
# git config credential.helper store <<< "https://$username:$password@github.com"
# git add .
# git commit -m "Automated data collection"
# git push

# cd "/home/"  # Return to the home directory
