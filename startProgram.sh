#!/bin/bash

# Check if the student account is provided as a command-line argument
if [ $# -eq 0 ]; then
    echo "Usage: $0 <student_account>"
    exit 1
fi

# Extract the student account from the command-line argument
student_account=$1

# Step 1: Establish SSH tunnel to Dolphin
echo "Enter your SSH password when prompted."
ssh -N -L 3306:dolphin.csci.viu.ca:3306 $student_account@otter.csci.viu.ca &
ssh_pid=$!

# Check if SSH tunnel was successfully established
wait $ssh_pid
if [ $? -ne 0 ]; then
    echo "Failed to establish SSH tunnel. Exiting."
    exit 1
fi

# Wait for a moment to ensure the SSH tunnel is established
sleep 2

# Step 2: Connect to the database using your Python script
python src/python/databaseConnector.py
