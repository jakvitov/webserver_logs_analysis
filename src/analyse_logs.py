import sys
import pandas as pd
import matplotlib.pyplot as plt
from pandasql import sqldf
import json


# Entrypoint to this whole app to be periodically launched
from src.analysis.analyse_access_data import getAccessDataDf, createAccessCountriesPlot
from src.ip_services.ip_translator import translateIps

if len(sys.argv) < 3:
    raise Exception("Not enough args to start.")

# Get logs directory and output logs directories from system args
log_directory = sys.argv[1]
dated_logs_directory = sys.argv[2]




access_df = getAccessDataDf(log_directory)
all_ips = sqldf("SELECT address FROM access_df GROUP BY address")
ips_translated = translateIps(list(all_ips["address"]))

requests_total = len(access_df.index)
non_ok_requests = len((sqldf("SELECT * FROM access_df WHERE status IS NOT 200")).index)
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


proxy_count = len(sqldf("SELECT * FROM ips_translated where proxy IS True").index)
error_ips_countries = ips_translated[ips_translated["query"].isin(list(non_ok_req_avg_per_ip["address"]))]

#access_by_country_graph = createAccessCountriesPlot(ips_translated, "Request to website server per country")
errors_by_country_graph = createAccessCountriesPlot(error_ips_countries, "Error requests to website server per country")

errors_by_country_graph.savefig("errors_by_country.png")

print(error_ips_countries['country'].value_counts())



