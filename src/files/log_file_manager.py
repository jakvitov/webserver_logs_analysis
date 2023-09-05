from datetime import date
import shutil

# Manages logfile manipulation during and after the data analysis

# Move the access and error logs to a separate folder
def moveLogFiles(log_directory, dated_logs_directory):
    date_string = str(date.today())
    print(
        "Moving " + log_directory + "/web_ui_access.log" + " -> " + dated_logs_directory + "/log_access_" + date_string + ".log")
    shutil.move(log_directory + "/web_ui_access.log", dated_logs_directory + "/log_access_" + date_string + ".log")
    print(
        "Moving " + log_directory + "/web_ui_error.log" + " -> " + dated_logs_directory + "/log_error_" + date_string + ".log")
    shutil.move(log_directory + "/web_ui_error.log", dated_logs_directory + "/log_error_" + date_string + ".log")

