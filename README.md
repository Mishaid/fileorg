# FileOrg

A program that runs as a service to sort files in specified directories.  
It uses python watchdog module to monitor new files in directories, and does not require a restart after adding new directories to the configuration.

![](.\demo.gif)

## Installation and Configuration

### Linux

Download and extract latest release archive and run `setup.sh`.  
Scrpit will install program files to FileOrg directory in your home and create systemd user unit.  
It will also ask for a directory that the program should monitor.  

You can control service with the following commands:
```bash
systemctl --user status fileorg.service
systemctl --user stop fileorg.service
systemctl --user disable fileorg.service
```

To add a new directory for the program to monitor, just specify full path in `~/FileOrg/dirs.txt` (one path one each line).  
You can review logs in `~/FileOrg/fileorg.log` file.

### Windows

Download and extract latest release archive and run `setup.bat`. 
Scrpit will install program files to FileOrg folder in your home and create link in `shell:startup` for running program on logon.  
It will also ask for a directory that the program should monitor. 

> [!WARNING]
> I Recomend adding `.exe` and `.bat` files to antivirus exceptions before installation.

You can control running program with the Task Manager.

To add a new directory for the program to monitor, just specify full path in `%USERPROFILE%\FileOrg\dirs.txt` (one path one each line).
You can review logs in `%USERPROFILE%\FileOrg\dirs.txt` file.