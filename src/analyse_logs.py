import sys
import datetime
from scheduler import Scheduler
from scheduler.trigger import Monday, Tuesday

# Entrypoint to this whole app to be periodically launched
from src.analysis.analyse_access_data import getAccessDataDf, createAccessCountriesPlot
from src.email.create_email_service import createAndSendEmail
from src.ip_services.ip_translator import translateIps

if len(sys.argv) < 3:
    raise Exception("Not enough args to start.")



def runEmailTask():
    # Get logs directory and output logs directories from system args
    log_directory = sys.argv[1]
    dated_logs_directory = sys.argv[2]

    print("Started creating report at: " + datetime.now.time())
    createAndSendEmail(log_directory, dated_logs_directory)

schedule = Scheduler()
schedule.weekly(Sunday(datetime.time(hour=16), runEmailTask))

#We run the email task once to test, that it runs ok
runEmailTask()
print(schedule)
