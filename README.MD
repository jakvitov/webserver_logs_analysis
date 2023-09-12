# Webserver logs analysis
This repository contains Python script, that is used to periodically analyse access and error logs made by Nginx server.

## Features
- The script is run once a week using *cron* and *docker compose*
- The logs are parsed and analysed using scripts ini analysis package
- Then we fill the result data into an email template using the scripts in the email package and send them
- Afterwards are the logfiles removed from the Nginx log folder and renamed with appropriate analysis date and placed into already-analysed folder
- At the end we delete already analysed logfiles older than constant time ago

## Deployment
Thanks to larger number of used libraries and difficult installation we run the application in Docker

- We define two volumes for the application
- Volume with the directory including Nginx logfiles 
- Volume with the output directory
- We can also add volume with the resource files, so it is simple for us to edit file with email recievers and html template for analysis
- We launch *docker compose up*  with *cron* once every week  

## Resources 
Resources is a directory including static resources - template for email and file with email analysis targerts

- Email template is a HTML template to be filled with the analysis using Python default Template engine
- Email target file contains lines with emails, that get the analysis (we could use a database instead, but since I have usually 1 or 2 target emails, i prefer simpler approach with a file)


