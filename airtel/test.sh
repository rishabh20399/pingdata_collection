#!/bin/bash

# Path to your Python script
script_path="/home/userland/pingdata_collection/airtel/DataCollection2.py"

mkdir /home/userland/pingdata_collection/airtel/data/

# Path to your Git repository
repository_path="/home/userland/pingdata_collection"

# Specify the starting time as "1645" for 16:45
start_time="1835"  # Use your desired start time in HHMM format

# Get the current date in 'YYYY-MM-DD' format
current_date=$(date +'%Y-%m-%d')

# Loop for 4 iterations
for ((iteration=0; iteration<4; iteration++)); do
    execution_time="$current_date $start_time"

    echo "Iteration $((iteration + 1)) running..."

    # Schedule the script to run in the background
    python3 "$script_path" &

    # Wait for the current iteration to complete
    wait


    # Print a message for each iteration
    echo "Iteration $((iteration + 1)) completed"

done


# Configure your Git identity
git config --global user.email "rishabh20399@iiitd.ac.in"
git config --global user.name "rishabh20399"
# git config --global init.defaultBranch main

# After all 4 iterations, commit and push changes to Git
cd /home/userland/pingdata_collection
git remote set-url origin git@github.com:rishabh20399/pingdata_collection.git

git checkout -b my-changes
git add /home/userland/pingdata_collection/airtel/data
git commit -m "Add files from data"
git push origin my-changes

# Link your local repository to the remote repository
# git remote add origin https://github.com/rishabh20399/pingdata_collection.git
# git push origin main -u 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


