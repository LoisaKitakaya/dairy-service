import os
import smtplib, ssl
from pytz import timezone
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from app.report import AutoReport
from email.mime.text import MIMEText
from datetime import datetime, timedelta
from email.mime.multipart import MIMEMultipart

load_dotenv()

WEB_APP = os.getenv("WEB_APP")


"""
timezone and datetime settings
"""

my_timezone = timezone("Africa/Nairobi")


"""
report generation function
"""


def generate_report(start_date: datetime, end_date: datetime):
    report_obj = AutoReport(start_date, end_date)

    last_week_data = report_obj.fetch_data()

    production = last_week_data["production"]
    payment = last_week_data["payment"]
    expenses = last_week_data["expenses"]

    report_data = report_obj.get_report_data(production, payment, expenses)  # type: ignore

    return report_obj.save_report(report_data, start_date, end_date)


"""
email settings
"""

SENDER_EMAIL = os.getenv("SENDER_EMAIL")
SENDER_EMAIL_PASSWORD = os.getenv("SENDER_EMAIL_PASSWORD")
RECIPIENTS = ("risloisa@gmail.com", "kitloisa@gmail.com", "loisadevmode@gmail.com")


"""
Weekly schedule function
"""


def weekly_update():
    datetime_obj = my_timezone.localize(datetime.now())

    start = datetime_obj - timedelta(days=1)

    end = datetime_obj - timedelta(days=7)

    report = generate_report(start, end)

    message = MIMEMultipart()

    message["From"] = SENDER_EMAIL
    message["To"] = ", ".join(RECIPIENTS)

    context = ssl.create_default_context()

    if report:
        with open("templates/email.html", "r") as file:
            template = file.read()

        soup = BeautifulSoup(template, "html.parser")

        tag = soup.find("a")

        tag["href"] = f"{WEB_APP}/app/reports/{report.inserted_id}"  # type: ignore

        soup.smooth()

        template = soup.prettify()

        email_template = MIMEText(template, "html")

        message["Subject"] = "Weekly Report [update]"

        message.attach(email_template)

        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(SENDER_EMAIL, SENDER_EMAIL_PASSWORD)  # type: ignore

            server.sendmail(SENDER_EMAIL, RECIPIENTS, message.as_string())  # type: ignore

        return

    else:
        with open("templates/error.html", "r") as file:
            template = file.read()

        soup = BeautifulSoup(template, "html.parser")

        template = soup.prettify()

        email_template = MIMEText(template, "html")

        message["Subject"] = "Weekly Report [not generated - missing records]"

        message.attach(email_template)

        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(SENDER_EMAIL, SENDER_EMAIL_PASSWORD)  # type: ignore

            server.sendmail(SENDER_EMAIL, RECIPIENTS, message.as_string())  # type: ignore

    return
