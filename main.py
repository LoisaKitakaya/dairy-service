import os
import time
import psycopg2
import schedule
import threading
from pytz import timezone
from flask_cors import CORS
from datetime import datetime
from twilio.rest import Client
from dotenv import load_dotenv
from flask import Flask, jsonify

load_dotenv()

my_timezone = timezone("Africa/Nairobi")

account_sid = os.getenv("TWILIO_ACCOUNT_SID")
auth_token = os.getenv("TWILIO_AUTH_TOKEN")
sender = os.getenv("TWILIO_SENDER")
receiver_one = os.getenv("TWILIO_RECEIVER_ONE")

web_app = os.getenv("WEB_APP")


def db_connect():
    return psycopg2.connect(
        database=os.getenv("DATABASE_NAME"),
        user=os.getenv("DATABASE_USER"),
        host=os.getenv("DATABASE_HOST"),
        password=os.getenv("DATABASE_PASSWORD"),
        port=os.getenv("DATABASE_PORT"),
    )


def daily_update(testing: bool = False):
    conn = None

    records = None

    recipients = [receiver_one]

    date_obj = my_timezone.localize(datetime.today())

    try:
        conn = db_connect()

        cur = conn.cursor()

        cur.execute(
            f"SELECT * FROM milk_production WHERE production_date = '{date_obj.date()}';"
        )

        records = cur.fetchall()

        cur.close()

    except Exception as error:
        raise Exception(str(error))

    finally:
        if conn is not None:
            conn.close()

    if not testing:
        client = Client(account_sid, auth_token)

        if records:
            for recipient in recipients:
                client.messages.create(
                    from_=sender,
                    body=f"Check webapp for updates on records for date '{date_obj.date()}'. \nLink: {web_app}/date/{date_obj.date()}",
                    to=recipient,  # type: ignore
                )

        else:
            for recipient in recipients:
                client.messages.create(
                    from_=sender,
                    body=f"No records were found for date '{date_obj.date()}'.",
                    to=recipient,  # type: ignore
                )

        return recipients

    else:
        return True


def make_timestamp(date_sr: str):
    date_obj = my_timezone.localize(datetime.strptime(date_sr, "%Y-%m-%d"))

    return date_obj.timestamp()


app = Flask(__name__)


CORS(app, resources={r"/*": {"origins": f"{web_app}"}})


@app.route("/check_connection/")
def check_connection():
    conn = None

    db_version = None

    try:
        conn = db_connect()

        cur = conn.cursor()

        cur.execute("SELECT version()")

        db_version = cur.fetchone()

        cur.close()

    except Exception as error:
        raise Exception(str(error))

    finally:
        if conn is not None:
            conn.close()

    if db_version:
        return jsonify({"data": {"message": f"Connection successful."}})
    else:
        return jsonify({"data": {"message": "Connection failed."}})


@app.route("/view_all_records/")
def view_all_records():
    conn = None

    records = None

    formatted_records = []

    try:
        conn = db_connect()

        cur = conn.cursor()

        cur.execute("SELECT * FROM milk_production;")

        records = cur.fetchall()

        cur.close()

    except Exception as error:
        raise Exception(str(error))

    finally:
        if conn is not None:
            conn.close()

    if records:
        for record in records:
            new_record = {
                "id": record[0],
                "name": record[1],
                "morning_production": record[2],
                "afternoon_production": record[3],
                "evening_production": record[4],
                "production_unit": record[5],
                "production_date": make_timestamp(str(record[6])),
            }

            formatted_records.append(new_record)

        return jsonify(
            {
                "data": {
                    "message": f"{len(records)} record(s) found in table 'milk_production'.",
                    "records": list(record for record in formatted_records),
                }
            }
        )

    else:
        return jsonify(
            {
                "data": {
                    "message": "0 records in table 'milk_production'.",
                    "records": [],
                }
            }
        )


@app.route("/view_record/<name>/")
def view_record(name):
    conn = None

    records = None

    formatted_records = []

    try:
        conn = db_connect()

        cur = conn.cursor()

        cur.execute(f"SELECT * FROM milk_production WHERE animal = '{name}';")

        records = cur.fetchall()

        cur.close()

    except Exception as error:
        raise Exception(str(error))

    finally:
        if conn is not None:
            conn.close()

    if records:
        for record in records:
            new_record = {
                "id": record[0],
                "name": record[1],
                "morning_production": record[2],
                "afternoon_production": record[3],
                "evening_production": record[4],
                "production_unit": record[5],
                "production_date": make_timestamp(str(record[6])),
            }

            formatted_records.append(new_record)

        return jsonify(
            {
                "data": {
                    "message": f"{len(records)} record(s) of '{name}' found in table 'milk_production'.",
                    "records": list(record for record in formatted_records),
                }
            }
        )

    else:
        return jsonify(
            {
                "data": {
                    "message": f"0 records of '{name}' found in table 'milk_production'.",
                    "records": [],
                }
            }
        )


@app.route("/view_record_by_date/<date>/")
def view_record_by_date(date):
    conn = None

    records = None

    formatted_records = []

    date_obj = my_timezone.localize(datetime.strptime(date, "%Y-%m-%d"))

    try:
        conn = db_connect()

        cur = conn.cursor()

        cur.execute(
            f"SELECT * FROM milk_production WHERE production_date = '{date_obj.date()}';"
        )

        records = cur.fetchall()

        cur.close()

    except Exception as error:
        raise Exception(str(error))

    finally:
        if conn is not None:
            conn.close()

    if records:
        for record in records:
            new_record = {
                "id": record[0],
                "name": record[1],
                "morning_production": record[2],
                "afternoon_production": record[3],
                "evening_production": record[4],
                "production_unit": record[5],
                "production_date": make_timestamp(str(record[6])),
            }

            formatted_records.append(new_record)

        return jsonify(
            {
                "data": {
                    "message": f"{len(records)} record(s) from date '{date}' found in table 'milk_production'.",
                    "records": list(record for record in formatted_records),
                }
            }
        )

    else:
        return jsonify(
            {
                "data": {
                    "message": f"0 records from date '{date}' found in table 'milk_production'.",
                    "records": [],
                }
            }
        )


task_lock = threading.Lock()


def schedule_task():
    with task_lock:
        schedule.every().day.at("19:00", "Africa/Nairobi").do(daily_update)


schedule_task()


def run_scheduled_tasks():
    while True:
        schedule.run_pending()
        time.sleep(1)


schedule_thread = threading.Thread(target=run_scheduled_tasks, daemon=True)
schedule_thread.start()


if __name__ == "__main__":
    app.run(
        debug=os.getenv("FLASK_DEBUG", default=False),  # type: ignore
        port=os.getenv("PORT", default=5000),  # type: ignore
    )
