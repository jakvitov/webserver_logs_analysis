import os
import smtplib
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from string import Template

# Setup the email template -> read from file
from src.analysis.analyse_access_data import fillInfoFromAccessLog
from src.analysis.analyse_errors import getBasicErrorsDataAndFillTemplate


# Service script, that fills template with info and creates and sends email with the statistics


def addImage(header_cid, msg, image_path):
    with open(image_path, 'rb') as image_file:
        image = MIMEImage(image_file.read())
        image.add_header('Content-ID', header_cid)
        msg.attach(image)
    return msg

smtp_server = "smtp.seznam.cz"
port = 465
sender_email = os.environ["EMAIL_NAME"]
password = os.environ["MAIL_BOT_PASSWORD"]
receiver_emails = open("../../resources/target_emails").readlines()

email_template_file = open("../../resources/analyse_email_template.html")
email_template = Template(email_template_file.read())
email_template_file.close()

# Object representing the key-value pairs to be filled in the template
error_info = {}

# Fill the email info dto with data info and create and save graphs
error_info = getBasicErrorsDataAndFillTemplate(error_info, "../../test_logs")
error_info = fillInfoFromAccessLog(error_info, "../../test_logs")

# Average load graph

msg = MIMEMultipart()
msg["From"] = sender_email
msg["To"] = ', '.join(receiver_emails)
msg["Subject"] = "Jakvitov web access statistics"

email_body = email_template.substitute(error_info)
msg.attach(MIMEText(email_body, 'html'))

access_by_country_graph_path = "./access_by_country.png"
errors_by_country_graph_path = "./errors_by_country.png"
request_distribution_graph_part = "./requests_distribution.png"
addImage("<countries_access_hist>", msg, access_by_country_graph_path)
addImage("<error_access_hist>", msg, errors_by_country_graph_path)
addImage("<requests_distribution>", msg, request_distribution_graph_part)

try:
    server = smtplib.SMTP_SSL(smtp_server, port)
    server.login(sender_email, password)

    server.sendmail(sender_email, receiver_emails, msg.as_string())
    print("Analysis sent OK")
except Exception as e:
    print(f"Error: {e}")
finally:
    server.quit()

# The files are automatically generated each time we run this script, so we clean them up afterwards
os.remove(access_by_country_graph_path)
os.remove(errors_by_country_graph_path)
os.remove(request_distribution_graph_part)