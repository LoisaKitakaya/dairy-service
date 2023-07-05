import os
import jwt
import pyotp
import bcrypt
from pytz import timezone
from datetime import datetime
from dotenv import load_dotenv
from pymongo import MongoClient
from app.decorators import is_authenticated
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


def resolve_create_user(*_, username: str, password: str) -> bool:
    existing_user = users_collection.find_one({"username": username})

    if not existing_user:
        datetime_obj = my_timezone.localize(datetime.now())

        hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())

        new_user = {
            "username": username,
            "password": hashed_password,
            "status": "active",
            "permission": "read",
            "otp_secret": str(pyotp.random_hex()),
            "date_joined": datetime_obj.timestamp(),
            "created_on": datetime_obj.timestamp(),
            "updated_on": datetime_obj.timestamp(),
        }

        user = users_collection.insert_one(new_user)

        if user.acknowledged:
            return True

        else:
            raise Exception("Write operation failed.")

    else:
        raise Exception("User already exists.")


def resolve_authenticate_user(*_, username: str, password: str) -> dict:
    existing_user = users_collection.find_one({"username": username})

    hashed_password = existing_user["password"]  # type: ignore
    user_id = existing_user["_id"]  # type: ignore

    if existing_user:
        if bcrypt.checkpw(password.encode(), hashed_password):
            return {
                "authenticated": True,
                "token": jwt.encode({"username": username, "id": str(user_id)}, salt),
            }

        else:
            raise Exception("Entered wrong password or username.")

    else:
        raise Exception("Entered wrong password or username.")


@is_authenticated
def resolve_create_production_record(
    _,
    info,
    name: str,
    morning_production: str,
    afternoon_production: str,
    evening_production: str,
    production_date: str,
) -> bool:
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


@is_authenticated
def resolve_update_production_record(
    _,
    info,
    id: str,
    name: str,
    morning_production: str,
    afternoon_production: str,
    evening_production: str,
    production_date: str,
) -> bool:
    if (
        name
        or morning_production
        or afternoon_production
        or evening_production
        or production_date
    ):
        if name:
            update = production_collection.update_one(
                {"_id": ObjectId(id)},
                {"$set": {"name": name}},
            )

            try:
                assert update.acknowledged == True

            except AssertionError:
                raise Exception("Write operation failed.")

        if morning_production:
            update = production_collection.update_one(
                {"_id": ObjectId(id)},
                {"$set": {"morning_production": float(morning_production)}},
            )

            try:
                assert update.acknowledged == True

            except AssertionError:
                raise Exception("Write operation failed.")

        if afternoon_production:
            update = production_collection.update_one(
                {"_id": ObjectId(id)},
                {"$set": {"afternoon_production": float(afternoon_production)}},
            )

            try:
                assert update.acknowledged == True

            except AssertionError:
                raise Exception("Write operation failed.")

        if evening_production:
            update = production_collection.update_one(
                {"_id": ObjectId(id)},
                {"$set": {"evening_production": float(evening_production)}},
            )

            try:
                assert update.acknowledged == True

            except AssertionError:
                raise Exception("Write operation failed.")

        if production_date:
            date_obj = my_timezone.localize(
                datetime.strptime(production_date, "%Y-%m-%dT%H:%M")
            )

            update = production_collection.update_one(
                {"_id": ObjectId(id)},
                {"$set": {"production_date": date_obj.timestamp()}},
            )

            try:
                assert update.acknowledged == True

            except AssertionError:
                raise Exception("Write operation failed.")

        date_obj = my_timezone.localize(datetime.now())

        update = production_collection.update_one(
            {"_id": ObjectId(id)},
            {"$set": {"updated_on": date_obj.timestamp()}},
        )

        return True

    else:
        raise Exception("Empty request. Nothing to update.")


@is_authenticated
def resolve_delete_production_record(_, info, id: str) -> bool:
    delete = production_collection.delete_one({"_id": ObjectId(id)})

    if delete.deleted_count == 1:
        return True

    else:
        raise Exception("Write operation failed.")


@is_authenticated
def resolve_create_payment_record(
    _,
    info,
    name: str,
    amount: str,
    payment_method: str,
    quantity: str,
    payment_date: str,
) -> bool:
    date_obj = my_timezone.localize(datetime.strptime(payment_date, "%Y-%m-%dT%H:%M"))

    datetime_obj = my_timezone.localize(datetime.now())

    payment_obj = {
        "name": name,
        "amount": float(amount),
        "payment_method": payment_method,
        "quantity": float(quantity),
        "payment_date": date_obj.timestamp(),
        "created_on": datetime_obj.timestamp(),
        "updated_on": datetime_obj.timestamp(),
    }

    payment = payment_collection.insert_one(payment_obj)

    if payment.acknowledged:
        return True

    else:
        raise Exception("Write operation failed.")


@is_authenticated
def resolve_update_payment_record(
    _,
    info,
    id: str,
    name: str,
    amount: str,
    payment_method: str,
    quantity: str,
    payment_date: str,
) -> bool:
    if name or amount or payment_method or quantity or payment_date:
        if name:
            update = payment_collection.update_one(
                {"_id": ObjectId(id)},
                {"$set": {"name": name}},
            )

            try:
                assert update.acknowledged == True

            except AssertionError:
                raise Exception("Write operation failed.")

        if amount:
            update = payment_collection.update_one(
                {"_id": ObjectId(id)},
                {"$set": {"amount": float(amount)}},
            )

            try:
                assert update.acknowledged == True

            except AssertionError:
                raise Exception("Write operation failed.")

        if payment_method:
            update = payment_collection.update_one(
                {"_id": ObjectId(id)},
                {"$set": {"payment_method": payment_method}},
            )

            try:
                assert update.acknowledged == True

            except AssertionError:
                raise Exception("Write operation failed.")

        if quantity:
            update = payment_collection.update_one(
                {"_id": ObjectId(id)},
                {"$set": {"quantity": float(quantity)}},
            )

            try:
                assert update.acknowledged == True

            except AssertionError:
                raise Exception("Write operation failed.")

        if payment_date:
            date_obj = my_timezone.localize(
                datetime.strptime(payment_date, "%Y-%m-%dT%H:%M")
            )

            update = payment_collection.update_one(
                {"_id": ObjectId(id)},
                {"$set": {"payment_date": date_obj.timestamp()}},
            )

            try:
                assert update.acknowledged == True

            except AssertionError:
                raise Exception("Write operation failed.")

        date_obj = my_timezone.localize(datetime.now())

        update = production_collection.update_one(
            {"_id": ObjectId(id)},
            {"$set": {"updated_on": date_obj.timestamp()}},
        )

        return True

    else:
        raise Exception("Empty request. Nothing to update.")


@is_authenticated
def resolve_delete_payment_record(_, info, id: str) -> bool:
    delete = payment_collection.delete_one({"_id": ObjectId(id)})

    if delete.deleted_count == 1:
        return True

    else:
        raise Exception("Write operation failed.")


@is_authenticated
def resolve_create_customer_record(
    _,
    info,
    name: str,
    priority: str,
    phone: str,
    trip: str,
    package: str,
) -> bool:
    datetime_obj = my_timezone.localize(datetime.now())

    customer_obj = {
        "name": name,
        "priority": priority,
        "phone": phone,
        "trip": trip,
        "package": float(package),
        "created_on": datetime_obj.timestamp(),
        "updated_on": datetime_obj.timestamp(),
    }

    customer = customers_collection.insert_one(customer_obj)

    if customer.acknowledged:
        return True

    else:
        raise Exception("Write operation failed.")


@is_authenticated
def resolve_update_customer_record(
    _,
    info,
    id: str,
    name: str,
    priority: str,
    phone: str,
    trip: str,
    package: str,
) -> bool:
    if name or priority or phone or trip or package:
        if name:
            update = customers_collection.update_one(
                {"_id": ObjectId(id)},
                {"$set": {"name": name}},
            )

            try:
                assert update.acknowledged == True

            except AssertionError:
                raise Exception("Write operation failed.")

        if priority:
            update = customers_collection.update_one(
                {"_id": ObjectId(id)},
                {"$set": {"priority": priority}},
            )

            try:
                assert update.acknowledged == True

            except AssertionError:
                raise Exception("Write operation failed.")

        if phone:
            update = customers_collection.update_one(
                {"_id": ObjectId(id)},
                {"$set": {"phone": phone}},
            )

            try:
                assert update.acknowledged == True

            except AssertionError:
                raise Exception("Write operation failed.")

        if trip:
            update = customers_collection.update_one(
                {"_id": ObjectId(id)},
                {"$set": {"trip": trip}},
            )

            try:
                assert update.acknowledged == True

            except AssertionError:
                raise Exception("Write operation failed.")

        if package:
            update = customers_collection.update_one(
                {"_id": ObjectId(id)},
                {"$set": {"package": float(package)}},
            )

            try:
                assert update.acknowledged == True

            except AssertionError:
                raise Exception("Write operation failed.")

        date_obj = my_timezone.localize(datetime.now())

        update = production_collection.update_one(
            {"_id": ObjectId(id)},
            {"$set": {"updated_on": date_obj.timestamp()}},
        )

        return True

    else:
        raise Exception("Empty request. Nothing to update.")


@is_authenticated
def resolve_delete_customer_record(_, info, id: str) -> bool:
    delete = customers_collection.delete_one({"_id": ObjectId(id)})

    if delete.deleted_count == 1:
        return True

    else:
        raise Exception("Write operation failed.")
