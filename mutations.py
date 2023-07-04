import os
import jwt
import bcrypt
from pytz import timezone
from datetime import datetime
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()

salt = os.getenv("SECRET_KEY")


"""
Database configuration
"""

client = MongoClient(os.getenv("DATABASE_URI"))

db = client.dairy_db

production_collection = db.milk_production

payment_collection = db.milk_payment

customers_collection = db.milk_customers

users_collection = db.app_users


"""
timezone and datetime settings
"""

my_timezone = timezone("Africa/Nairobi")


def get_datetime():
    datetime_obj = my_timezone.localize(datetime.now())

    return datetime_obj.timestamp()


"""
mutation resolvers
"""


def resolve_create_user(*_, username: str, password: str):
    existing_user = users_collection.find_one({"username": username})

    if not existing_user:
        hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())

        new_user = {
            "username": username,
            "password": hashed_password,
            "status": "active",
            "date_joined": get_datetime(),
        }

        user = users_collection.insert_one(new_user)

        if user.acknowledged:
            return True

        else:
            raise Exception("Write operation failed.")

    else:
        raise Exception("User already exists.")


def resolve_authenticate_user(*_, username: str, password: str):
    existing_user = users_collection.find_one({"username": username})

    hashed_password = existing_user["password"]  # type: ignore
    user_id = existing_user["_id"]  # type: ignore

    if existing_user:
        if bcrypt.checkpw(password.encode(), hashed_password):
            token = jwt.encode({"username": username, "id": str(user_id)}, salt)

            return token

        else:
            raise Exception("Entered wrong password or username.")

    else:
        raise Exception("Entered wrong password or username.")
