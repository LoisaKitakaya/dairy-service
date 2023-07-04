import os
import jwt
import bcrypt
from pytz import timezone
from datetime import datetime
from dotenv import load_dotenv
from pymongo import MongoClient
from bson.objectid import ObjectId

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


"""
mutation resolvers
"""


def resolve_create_user(*_, username: str, password: str):
    existing_user = users_collection.find_one({"username": username})

    datetime_obj = my_timezone.localize(datetime.now())

    if not existing_user:
        hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())

        new_user = {
            "username": username,
            "password": hashed_password,
            "status": "active",
            "permission": "read/write",
            "date_joined": datetime_obj.timestamp(),
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
            return jwt.encode({"username": username, "id": str(user_id)}, salt)

        else:
            raise Exception("Entered wrong password or username.")

    else:
        raise Exception("Entered wrong password or username.")


def resolve_create_production_record(
    _,
    info,
    name: str,
    morning_production: str,
    afternoon_production: str,
    evening_production: str,
    production_date: str,
):
    date_obj = my_timezone.localize(
        datetime.strptime(production_date, "%Y-%m-%dT%H:%M")
    )

    datetime_obj = my_timezone.localize(datetime.now())

    production_obj = {
        "name": name,
        "morning_production": float(morning_production),
        "afternoon_production": float(afternoon_production),
        "evening_production": float(evening_production),
        "production_date": date_obj.timestamp(),
        "created_on": datetime_obj.timestamp(),
        "updated_on": datetime_obj.timestamp(),
    }

    production = production_collection.insert_one(production_obj)

    if production.acknowledged:
        return True

    else:
        raise Exception("Write operation failed.")


def resolve_update_production_record(
    _,
    info,
    id,
    name: str,
    morning_production: str,
    afternoon_production: str,
    evening_production: str,
    production_date: str,
):
    production_obj_original = production_collection.find_one({"_id": ObjectId(id)})

    if (
        name
        or morning_production
        or afternoon_production
        or evening_production
        or production_date
    ):
        if name:
            update = production_collection.update_one(
                {"name": production_obj_original["name"]}, {"$set": {"name": name}}  # type: ignore
            )

            try:
                assert update.acknowledged == True

            except:
                raise Exception("Write operation failed.")

        if morning_production:
            update = production_collection.update_one(
                {"morning_production": production_obj_original["morning_production"]},  # type: ignore
                {"$set": {"morning_production": float(morning_production)}},
            )

            try:
                assert update.acknowledged == True

            except:
                raise Exception("Write operation failed.")

        if afternoon_production:
            update = production_collection.update_one(
                {"afternoon_production": production_obj_original["afternoon_production"]},  # type: ignore
                {"$set": {"afternoon_production": float(afternoon_production)}},
            )

            try:
                assert update.acknowledged == True

            except:
                raise Exception("Write operation failed.")

        if evening_production:
            update = production_collection.update_one(
                {"evening_production": production_obj_original["evening_production"]},  # type: ignore
                {"$set": {"evening_production": float(evening_production)}},
            )

            try:
                assert update.acknowledged == True

            except:
                raise Exception("Write operation failed.")

        if production_date:
            date_obj = my_timezone.localize(
                datetime.strptime(production_date, "%Y-%m-%dT%H:%M")
            )

            update = production_collection.update_one(
                {"production_date": production_obj_original["production_date"]},  # type: ignore
                {"$set": {"production_date": date_obj.timestamp()}},
            )

            try:
                assert update.acknowledged == True

            except:
                raise Exception("Write operation failed.")

        return True

    else:
        raise Exception("Empty request. Nothing to update.")


def resolve_delete_production_record(_, info, id):
    delete = production_collection.delete_one({"_id": ObjectId(id)})

    if delete.deleted_count == 1:
        return True

    else:
        raise Exception("Write operation failed.")


def resolve_create_payment_record(_, info):
    pass


def resolve_update_payment_record(_, info):
    pass


def resolve_delete_payment_record(_, info):
    pass


def resolve_create_customer_record(_, info):
    pass


def resolve_update_customer_record(_, info):
    pass


def resolve_delete_customer_record(_, info):
    pass
