#!/bin/bash

# Check if the script is running with sudo privileges
if [[ $EUID -ne 0 ]]; then
    echo "This script must be run with sudo privileges."
    exit 1
fi

# Get the current username
current_username=$(whoami)

# Prompt for the username
read -p "Enter username or leave blank to use the current user ($current_username): " username

# If the username is left blank, use the current user
if [[ -z "$username" ]]; then
    username=$current_username
fi

# Prepare a temporary file
temp_file=$(mktemp)

# Write all the commands into the temporary file for the specified username
cat <<EOL > "$temp_file"
$username ALL=(ALL:ALL) NOPASSWD:/usr/sbin/adduser
$username ALL=(ALL:ALL) NOPASSWD:/usr/sbin/userdel
$username ALL=(ALL:ALL) NOPASSWD:/usr/bin/sed
$username ALL=(ALL:ALL) NOPASSWD:/usr/bin/kill
$username ALL=(ALL:ALL) NOPASSWD:/usr/bin/killall
$username ALL=(ALL:ALL) NOPASSWD:/usr/bin/lsof
$username ALL=(ALL:ALL) NOPASSWD:/usr/sbin/lsof
$username ALL=(ALL:ALL) NOPASSWD:/usr/bin/rm
$username ALL=(ALL:ALL) NOPASSWD:/usr/bin/chpasswd
$username ALL=(ALL:ALL) NOPASSWD:/usr/sbin/service
EOL

# Use visudo to append the contents of the temporary file to the sudoers file
sudo visudo -c -f "$temp_file" && sudo cat "$temp_file" >> /etc/sudoers

# Clean up the temporary file
rm "$temp_file"
