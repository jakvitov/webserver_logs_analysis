import itertools

import pandas as pd
import matplotlib as plt
from pandasql import sqldf
import sys
import shutil
from datetime import date
import json
import requests

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


def getBasicErrorsData():
    error_df = createErrorDf();
    errors_by_date = sqldf("SELECT date, count()  FROM error_df GROUP BY date")
    log_level_groupped = sqldf("SELECT log_level, count() FROM error_df GROUP BY log_level")
    open_file_errors = len(sqldf("SELECT * FROM error_df WHERE message like '%open()%'").index)
    ssl_handshake_errors = len(sqldf("SELECT * FROM error_df WHERE message like '%SSL_do_handshake() failed'").index)

def getAccessDataDf():
    data = []
    # Open the JSON file and read it line by line
    with open(log_directory + "/web_ui_access.log", 'r') as file:
        for line in file:
            # Parse each line as a JSON object and append it to the list
            json_data = json.loads(line)
            data.append(json_data)
    return pd.DataFrame(data)

def translateIps(ipList):
    result = [];
    # We split the ipList to groups of 99 -> the external service limit
    for i in range(0, len(ipList), 99):
        api_url = "http://ip-api.com/batch?fields=city,country,countryCode,query,asname,proxy"
        body = ipList[i : i + 99]
        response = requests.post(api_url, json=body)
        result += (response.json())
    return result


access_df = getAccessDataDf()
requests_total = len(access_df.index)

requests_code_count = sqldf("SELECT status, count() c FROM access_df GROUP BY status ORDER BY c DESC")
often_request_ip = sqldf("SELECT address, count() c FROM access_df GROUP BY address HAVING c >= 10 ORDER BY c DESC")

non_ok_req_avg_per_ip = sqldf("SELECT address, count() as count FROM access_df GROUP BY address HAVING status IS NOT 200")
max_non_ok_per_ip = non_ok_req_avg_per_ip["count"].max()
non_ok_per_ip_mean = non_ok_req_avg_per_ip["count"].mean()
var_coef_non_ok_per_ip = (non_ok_req_avg_per_ip["count"].std()/non_ok_per_ip_mean) * 100;

max_non_ok_ips = sqldf("SELECT address FROM non_ok_req_avg_per_ip WHERE count=" + str(1))

print(translateIps(list(max_non_ok_ips["address"])))
