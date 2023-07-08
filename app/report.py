import os
from pytz import timezone
from datetime import datetime
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()

"""
Database configuration
"""

CLIENT = MongoClient(os.getenv("DATABASE_URI"))

db = CLIENT.dairy_db

production_collection = db.milk_production

payment_collection = db.milk_payment

customers_collection = db.milk_customers

expenses_collection = db.production_expenses


"""
timezone and datetime settings
"""

my_timezone = timezone("Africa/Nairobi")


class AutoReport:
    def __init__(self, start_date: datetime, end_date: datetime) -> None:
        self.start_date = start_date
        self.end_date = end_date


class GenerateReport:
    def __init__(self, start_date: datetime, end_date: datetime) -> None:
        self.start_date = start_date
        self.end_date = end_date
