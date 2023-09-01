import pandas as pd
import matplotlib as plt
import sys
import shutil
from datetime import date

if len(sys.argv) < 3:
    raise Exception("Not enough args to start.")

# Get logs directory and output logs directories from system args
log_directory = sys.argv[1]
dated_logs_directory = sys.argv[2]


# Move the access and error logs to a separate folder
def moveFiles():
    date_string = str(date.today())
    print(
        "Moving " + log_directory + "/web_ui_access.log" + " -> " + dated_logs_directory + "/log_access_" + date_string + ".log")
    shutil.move(log_directory + "/web_ui_access.log", dated_logs_directory + "/log_access_" + date_string + ".log")
    print(
        "Moving " + log_directory + "/web_ui_error.log" + " -> " + dated_logs_directory + "/log_error_" + date_string + ".log")
    shutil.move(log_directory + "/web_ui_error.log", dated_logs_directory + "/log_error_" + date_string + ".log")


def createErrorDf():
    error_file = open(log_directory + "/web_ui_error.log", 'r')
    error_lines = error_file.readlines()
    error_file.close()

    # Split error lines into array of lines
    error_lines = [string.split(" ", 4) for string in error_lines]
    error_df = pd.DataFrame(error_lines)
    error_df.columns = ["date", "time", "log_level", "proccess_id", "message"]
    return error_df



