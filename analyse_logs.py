import pandas as pd
import matplotlib as plt
import os
import shutil
from datetime import date


log_directory = "./test_logs"
dated_logs_directory = "./dated_logs"

# Move the access and error logs to a separate folder
shutil.move(log_directory + "/web_ui_access.log", dated_logs_directory + "/log_access_" + str(date.today()) + ".log")
shutil.move(log_directory + "/web_ui_error.log", dated_logs_directory + "/log_error_" + str(date.today()) + ".log")





#%%
