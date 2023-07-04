import os
import time
import schedule
import threading
from pytz import timezone
from flask_cors import CORS
from datetime import datetime
from dotenv import load_dotenv
from flask import Flask, jsonify

load_dotenv()

my_timezone = timezone("Africa/Nairobi")

web_app = os.getenv("WEB_APP")


def db_connect():
    pass


def make_timestamp(date_sr: str):
    date_obj = my_timezone.localize(datetime.strptime(date_sr, "%Y-%m-%d"))

    return date_obj.timestamp()


def daily_update(testing: bool = False):
    pass


task_lock = threading.Lock()


def schedule_task():
    with task_lock:
        schedule.every().day.at("20:00", "Africa/Nairobi").do(daily_update)


schedule_task()


def run_scheduled_tasks():
    while True:
        schedule.run_pending()
        time.sleep(1)


schedule_thread = threading.Thread(target=run_scheduled_tasks, daemon=True)
schedule_thread.start()


app = Flask(__name__)


CORS(app, resources={r"/*": {"origins": web_app}})


if __name__ == "__main__":
    app.run(
        debug=os.getenv("FLASK_DEBUG", default=False),  # type: ignore
        port=os.getenv("PORT", default=5000),  # type: ignore
    )
