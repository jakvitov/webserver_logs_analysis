import itertools

import pandas as pd
import matplotlib.pyplot as plt
from string import Template
from pandasql import sqldf
import sys
import shutil
from datetime import date
import json
import requests
from datetime import datetime

if len(sys.argv) < 3:
    raise Exception("Not enough args to start.")

# Get logs directory and output logs directories from system args
log_directory = sys.argv[1]
dated_logs_directory = sys.argv[2]

#Setup the email template -> read from file
email_template_file = open("analyse_email_template.html")
email_template = Template(email_template_file.read())
email_template_file.close()
#Object representing the key-value pairs to be filled in the template
error_info = {}

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

# Fill in the basic info about errors log file into template email
def getBasicErrorsDataAndFillTemplate(error_info):
    error_df = createErrorDf()
    errors_by_date = sqldf("SELECT date, count()  FROM error_df GROUP BY date")
    log_level_groupped = sqldf("SELECT log_level, count() FROM error_df GROUP BY log_level")
    open_file_errors = len(sqldf("SELECT * FROM error_df WHERE message like '%open()%'").index)
    ssl_handshake_errors = len(sqldf("SELECT * FROM error_df WHERE message like '%SSL_do_handshake() failed'").index)
    error_info["error_log_errors"] = str(len(error_df.index))
    error_info["open_file_erros"] = str(open_file_errors)
    error_info["handshake_errors"] = str(ssl_handshake_errors)
    return error_info


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
    return pd.DataFrame(result)

def createPlotFromTranslatedIps(translated_ips):
    country_counts = translated_ips['country'].value_counts()

    # Create a bar plot
    plt.figure(figsize=(10, 6))
    country_counts.plot(kind='bar')
    plt.title('Country Counts')
    plt.xlabel('Country')
    plt.ylabel('Count')
    plt.xticks(rotation=45)
    plt.tight_layout()

def fillInfoFromAccessLog(error_info):
    access_df = getAccessDataDf()

    requests_total = len(access_df.index)
    non_ok_requests = len((sqldf("SELECT * FROM access_df GROUP BY WHERE status IS NOT 200")).index)
    non_ok_req_avg_per_ip = sqldf(
        "SELECT address, count() as count FROM access_df GROUP BY address HAVING status IS NOT 200")
    non_ok_per_ip_mean = non_ok_req_avg_per_ip["count"].mean()

    # Convert the timestamps to date column
    access_df["time_h"] = pd.to_datetime(access_df["time"], unit='s')
    access_df["date"] = access_df["time_h"].dt.date

    failed_by_date = sqldf("SELECT date, count() FROM access_df GROUP BY date HAVING STATUS IS NOT 200")

    max_non_ok_per_ip = non_ok_req_avg_per_ip["count"].max()
    max_non_ok_ips = sqldf("SELECT address FROM non_ok_req_avg_per_ip WHERE count=" + str(max_non_ok_per_ip))
    max_no_ok_ips_translated = translateIps(list(max_non_ok_ips["address"]))
    max_no_ok_ips_translated = sqldf("SELECT country, city, proxy FROM max_no_ok_ips_translated")
    max_no_ok_ips_translated["Requests"] = max_non_ok_per_ip;

    all_ips = sqldf("SELECT address FROM access_df GROUP BY address")
    ips_translated = translateIps(list(all_ips["address"]))
    proxy_count = len(sqldf("SELECT * FROM ips_translated where proxy IS True").index)

    error_info["requests_count"] = str(requests_total)
    error_info["errors_count"] = str(non_ok_requests)
    error_info["errors_per_req"] = str(non_ok_requests/requests_total)

    error_info["avg_failed"] = str(non_ok_per_ip_mean)
    error_info["failed_per_date"] = failed_by_date.to_html()
    error_info["max_failed_per_ip"] = max_no_ok_ips_translated.to_html()
    error_info["proxy_total"] = str(proxy_count)
    error_info["proxy_relative"] = str(proxy_count/requests_total)


access_df = getAccessDataDf()

all_ips = sqldf("SELECT address FROM access_df GROUP BY address")
ips_translated = translateIps(list(all_ips["address"]))

country_counts = ips_translated['country'].value_counts()

# Create a bar plot
country_counts.plot(kind='bar')
plt.title('Visits per country')
plt.xlabel('Country')
plt.ylabel('Count')
plt.xticks(rotation=90)
plt.yscale("log")
plt.tight_layout()

plt.show()

