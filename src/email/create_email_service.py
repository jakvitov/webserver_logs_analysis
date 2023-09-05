from string import Template

# Service script, that fills template with info and creates and sends email with the statistics

#Setup the email template -> read from file
email_template_file = open("../resources/analyse_email_template.html")
email_template = Template(email_template_file.read())
email_template_file.close()
#Object representing the key-value pairs to be filled in the template
error_info = {}