#!/bin/bash

# Path to your Python script
script1_path="/data/data/com.termux/files/home/pingdata_collection/airtel/DataCollection2.py"
script2_path="/data/data/com.termux/files/home/pingdata_collection/airtel/tracerouteData.py"


data_dir="/data/data/com.termux/files/home/pingdata_collection/airtel/data"

# Check if the data directory exists, and if not, create it
if [ ! -d "$data_dir" ]; then
  mkdir -p "$data_dir"
fi

# Path to your Git repository
repository_path="/data/data/com.termux/files/home/pingdata_collection"

# Specify the starting time as "1645" for 16:45
start_time="1315"  # Use your desired start time in HHMM format

# Get the current date in 'YYYY-MM-DD' format
current_date=$(date +'%Y-%m-%d')

# Loop for 4 iterations
for ((iteration=0; iteration<4; iteration++)); do
    execution_time="$current_date $start_time"

    echo "Iteration $((iteration + 1)) running..."

    # Schedule the script to run in the background
    python3 "$script1_path" &

    # Wait for the current iteration to complete
    wait


    # Print a message for each iteration
    echo "Iteration $((iteration + 1)) completed"

done

# After running script1 four times, execute script2
echo "Executing traceroute data collection..."
python3 "$script2_path"

# Configure your Git identity
git config --global user.email "rishabh20399@iiitd.ac.in"
git config --global user.name "rishabh20399"
# git config --global init.defaultBranch main

# After all 4 iterations, commit and push changes to Git
cd /data/data/com.termux/files/home/pingdata_collection
git remote set-url origin git@github.com:rishabh20399/pingdata_collection.git

git checkout -b my-changes
git add /data/data/com.termux/files/home/pingdata_collection/airtel/data
git commit -m "Add files from data"
git push origin my-changes

# Link your local repository to the remote repository
# git remote add origin https://github.com/rishabh20399/pingdata_collection.git
# git push origin main -u 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


