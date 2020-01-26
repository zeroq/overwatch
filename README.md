# About/Final Goal:

Overwatch is a small Python-based Linux Agent to check Systems for security issues. It can be used to deploy rootkit hunter (rkhunter) on all registered hosts, run it on a regular basis, and store the results centrally to visualize security issues.

It also will allow to perform YARA searches across all registered hosts to find malicious software in the near future.

# Current Status:

Only basic functionality provided so far. Missing most of the graphical interface and the YARA scanning part. Work in progress ...

# Installation:

- Install Python requirements from requirements.txt file
- Download rkhunter version 1.4.6 and copy it to the ow_downloads folder for automated deployment
- Or have rkhunter version 1.4.6 pre-installed on the client systems you want to watch
- Add "rkhunter" as a profilename to the profiles database table
