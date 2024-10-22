import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from argparse import ArgumentParser

SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT= '587'
EMAIL_USER = 'mohitya125@gmail.com'
EMAIL_PASSWORD = 'twip iblb zbck uwpn'
EMAIL_TO = 'mohit.shah@uni-ulm.de'

parser = ArgumentParser()
parser.add_argument('-d', '--diff_file', metavar='', required=True, help="sv diff dump")
args = parser.parse_args()
python_version = args.python_version
diff_file = args.diff_file

with open(diff_file) as diff:
    dep_diff = ''.join(diff.readlines())

smtp_server = SMTP_SERVER
smtp_port = SMTP_PORT
email_user = EMAIL_USER
email_password = EMAIL_PASSWORD
email_to = EMAIL_TO

sv_changed = True if dep_diff else False

if sv_changed:

    # Email content
    subject = "❗ GitHub Actions: Test Job Failure Alert"
    body = f"""
    Hello,

    This is an automated message to notify you that the GitHub Actions test job has failed .

    The tests failed and the following status variables changed 

    {dep_diff}

    Best regards,
    Your GitHub Actions Bot
    """

    message = MIMEMultipart()
    message["From"] = email_user
    message["To"] = email_to
    message["Subject"] = subject
    message.attach(MIMEText(body, "plain"))

    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()  
        server.login(email_user, email_password)
        server.sendmail(email_user, email_to, message.as_string())
        print(f"Email sent to {email_to}")
        server.quit()

    except Exception as e:
        print(f"Failed to send email: {e}")

