import pandas as pd
from pandasql import sqldf

# Script for error data analysis. We open the error log, compute data from it and return data objects
# ready to be filled into email template

def createErrorDf(log_directory):
    error_file = open(log_directory + "/web_ui_error.log", 'r')
    error_lines = error_file.readlines()
    error_file.close()

    # Split error lines into array of lines
    error_lines = [string.split(" ", 4) for string in error_lines]
    error_df = pd.DataFrame(error_lines)
    error_df.columns = ["date", "time", "log_level", "proccess_id", "message"]
    return error_df

# Fill in the basic info about errors log file into template email
def getBasicErrorsDataAndFillTemplate(error_info, log_directory):
    error_df = createErrorDf(log_directory)
    errors_by_date = sqldf("SELECT date, count()  FROM error_df GROUP BY date")
    log_level_groupped = sqldf("SELECT log_level, count() FROM error_df GROUP BY log_level")
    open_file_errors = len(sqldf("SELECT * FROM error_df WHERE message like '%open()%'").index)
    ssl_handshake_errors = len(sqldf("SELECT * FROM error_df WHERE message like '%SSL_do_handshake() failed'").index)
    error_info["error_log_errors"] = str(len(error_df.index))
    error_info["open_file_erros"] = str(open_file_errors)
    error_info["handshake_errors"] = str(ssl_handshake_errors)
    return error_info
