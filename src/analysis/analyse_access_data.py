import pandas as pd
import matplotlib.pyplot as plt
from pandasql import sqldf
import json

from src.ip_services.ip_translator import translateIps

# Script for access data analysis. We open the access log, compute data from it and return data objects
# ready to be filled into email template

def getAccessDataDf(log_directory):
    data = []
    # Open the JSON file and read it line by line
    with open(log_directory + "/web_ui_access.log", 'r') as file:
        for line in file:
            # Parse each line as a JSON object and append it to the list
            json_data = json.loads(line)
            data.append(json_data)
    return pd.DataFrame(data)

def createAccessCountriesPlot(translated_ips):
    country_counts = translated_ips['country'].value_counts()
    # Create a bar plot
    country_counts.plot(kind='bar')
    plt.title('Visits per country')
    plt.xlabel('Country')
    plt.ylabel('Count of visits')
    plt.xticks(rotation=90)
    plt.tight_layout()
    return plt

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
    access_by_country_graph = createAccessCountriesPlot(ips_translated)

    error_info["requests_count"] = str(requests_total)
    error_info["errors_count"] = str(non_ok_requests)
    error_info["errors_per_req"] = str(non_ok_requests/requests_total)

    error_info["avg_failed"] = str(non_ok_per_ip_mean)
    error_info["failed_per_date"] = failed_by_date.to_html()
    error_info["max_failed_per_ip"] = max_no_ok_ips_translated.to_html()
    error_info["proxy_total"] = str(proxy_count)
    error_info["proxy_relative"] = str(proxy_count/requests_total)

