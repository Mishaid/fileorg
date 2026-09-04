#!/bin/bash

USER_HOME=$(echo ~)

echo "Creating application directory: ~/FileOrg"

mkdir -p ~/FileOrg

echo "Copying application..."

install -m 600 dirs.txt ~/FileOrg/dirs.txt
install -m 700 fileorg ~/FileOrg/fileorg

if [ $? -eq 1 ]
    then
        echo "ERROR: Failed to copy application."
        exit 1
    fi

echo "Application copied successfully."

echo "Creating systemd user service..."

cat > ~/.config/systemd/user/fileorg.service << EOF
[Unit]
Description=FileOrg service
After=network.target

[Service]
ExecStart=$USER_HOME/FileOrg/fileorg
Restart=on-failure

[Install]
WantedBy=default.target
EOF

if [ $? -eq 1 ]
    then
        echo "ERROR: Failed to set application startup."
        exit 1
    fi

echo "Systemd user service created successfully."

echo "Specify one directory path to start: "
read dir
echo $dir > ~/FileOrg/dirs.txt

echo "Adding service to startup..."

systemctl --user daemon-reload
systemctl --user enable --now fileorg.service

echo "Service added to startup successfully"