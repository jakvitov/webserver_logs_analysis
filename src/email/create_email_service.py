from string import Template
import smtplib

# Service script, that fills template with info and creates and sends email with the statistics

# Setup the email template -> read from file
from src.analysis.analyse_access_data import fillInfoFromAccessLog
from src.analysis.analyse_errors import getBasicErrorsDataAndFillTemplate

email_template_file = open("../../resources/analyse_email_template.html")
email_template = Template(email_template_file.read())
email_template_file.close()

# Object representing the key-value pairs to be filled in the template
error_info = {}

# Fill the email info dto with data info and create and save graphs
error_info = getBasicErrorsDataAndFillTemplate(error_info, "../../test_logs")
error_info = fillInfoFromAccessLog(error_info, "../../test_logs")


error_info["total_diff_countries"] = "picture1"
error_info["total_error_countries"] = "picture2"

# Average load graph

print(email_template.substitute(error_info))

email_template.substitute(error_info)