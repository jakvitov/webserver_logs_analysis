import sys

# Entrypoint to this whole app to be periodically launched

if len(sys.argv) < 3:
    raise Exception("Not enough args to start.")

# Get logs directory and output logs directories from system args
log_directory = sys.argv[1]
dated_logs_directory = sys.argv[2]








