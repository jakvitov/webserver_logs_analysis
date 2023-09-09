#!/bin/bash

# We set paths to each individual package here - since we do not declare python packages
export PYTHONPATH=$PYTHONPATH:/home/jakub/Development/webserver-logs-analysis/webserver_logs_analysis/src/email

python3 ./src/analyse_logs.py $1 $2