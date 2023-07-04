import os
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()

"""
Database configuration
"""

client = MongoClient(os.getenv("DATABASE_URI"))

db = client.dairy_db

production_collection = db.milk_production

payment_collection = db.milk_payment

customers_collection = db.milk_customers

users_collection = db.app_users


def resolve_get_all_users(*_):
    all_users = None

    try:
        all_users = users_collection.find()

    except Exception as e:
        raise Exception(str(e))

    finally:
        return all_users
