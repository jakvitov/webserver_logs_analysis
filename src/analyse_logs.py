import sys
import datetime

from create_email_service import createAndSendEmail

# Entrypoint to this whole app to be periodically launched

if len(sys.argv) < 3:
    raise Exception("Not enough args to start.")

def runEmailTask():
    # Get logs directory and output logs directories from system args
    log_directory = sys.argv[1]
    dated_logs_directory = sys.argv[2]

    print("Started creating report at: " + datetime.datetime.now().ctime())
    createAndSendEmail(log_directory, dated_logs_directory)

#We run the email task once to test, that it runs ok
runEmailTask()
