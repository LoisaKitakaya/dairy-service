import os
import jwt
import bcrypt
from pytz import timezone
from datetime import datetime
from dotenv import load_dotenv
from pymongo import MongoClient
from auth import is_authenticated
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

    if existing_user:
        if bcrypt.checkpw(password.encode(), hashed_password):
            return jwt.encode({"username": username}, salt)

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


@is_authenticated
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
    production_obj = production_collection.find_one({"_id": ObjectId(id)})

    if (
        name
        or morning_production
        or afternoon_production
        or evening_production
        or production_date
    ):
        if name:
            update = production_collection.update_one(
                {"name": production_obj["name"]}, {"$set": {"name": name}}  # type: ignore
            )

            try:
                assert update.acknowledged == True

            except AssertionError:
                raise Exception("Write operation failed.")

        if morning_production:
            update = production_collection.update_one(
                {"morning_production": production_obj["morning_production"]},  # type: ignore
                {"$set": {"morning_production": float(morning_production)}},
            )

            try:
                assert update.acknowledged == True

            except AssertionError:
                raise Exception("Write operation failed.")

        if afternoon_production:
            update = production_collection.update_one(
                {"afternoon_production": production_obj["afternoon_production"]},  # type: ignore
                {"$set": {"afternoon_production": float(afternoon_production)}},
            )

            try:
                assert update.acknowledged == True

            except AssertionError:
                raise Exception("Write operation failed.")

        if evening_production:
            update = production_collection.update_one(
                {"evening_production": production_obj["evening_production"]},  # type: ignore
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
                {"production_date": production_obj["production_date"]},  # type: ignore
                {"$set": {"production_date": date_obj.timestamp()}},
            )

            try:
                assert update.acknowledged == True

            except AssertionError:
                raise Exception("Write operation failed.")

        date_obj = my_timezone.localize(datetime.now())

        update = production_collection.update_one(
            {"updated_on": production_obj["updated_on"]},  # type: ignore
            {"$set": {"updated_on": date_obj.timestamp()}},
        )

        return True

    else:
        raise Exception("Empty request. Nothing to update.")


@is_authenticated
def resolve_delete_production_record(_, info, id):
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
):
    date_obj = my_timezone.localize(datetime.strptime(payment_date, "%Y-%m-%dT%H:%M"))

    datetime_obj = my_timezone.localize(datetime.now())

    payment_obj = {
        "name": name,
        "amount": float(amount),
        "payment_method": payment_method,
        "quantity": float(quantity),
        "payment_date": date_obj,
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
    id,
    name: str,
    amount: str,
    payment_method: str,
    quantity: str,
    payment_date: str,
):
    payment_obj = payment_collection.find_one({"_id": ObjectId(id)})

    if name or amount or payment_method or quantity or payment_date:
        if name:
            update = payment_collection.update_one(
                {"name": payment_obj["name"]}, {"$set": {"name": name}}  # type: ignore
            )

            try:
                assert update.acknowledged == True

            except AssertionError:
                raise Exception("Write operation failed.")

        if amount:
            update = payment_collection.update_one(
                {"amount": payment_obj["amount"]}, {"$set": {"amount": float(amount)}}  # type: ignore
            )

            try:
                assert update.acknowledged == True

            except AssertionError:
                raise Exception("Write operation failed.")

        if payment_method:
            update = payment_collection.update_one(
                {"payment_method": payment_obj["payment_method"]},  # type: ignore
                {"$set": {"payment_method": payment_method}},
            )

            try:
                assert update.acknowledged == True

            except AssertionError:
                raise Exception("Write operation failed.")

        if quantity:
            update = payment_collection.update_one(
                {"quantity": payment_obj["quantity"]},  # type: ignore
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
                {"payment_date": payment_obj["payment_date"]},  # type: ignore
                {"$set": {"payment_date": date_obj.timestamp()}},
            )

            try:
                assert update.acknowledged == True

            except AssertionError:
                raise Exception("Write operation failed.")

        date_obj = my_timezone.localize(datetime.now())

        update = production_collection.update_one(
            {"updated_on": production_obj["updated_on"]},  # type: ignore
            {"$set": {"updated_on": date_obj.timestamp()}},
        )

        return True

    else:
        raise Exception("Empty request. Nothing to update.")


@is_authenticated
def resolve_delete_payment_record(_, info, id):
    delete = payment_collection.delete_one({"_id": ObjectId(id)})

    if delete.deleted_count == 1:
        return True

    else:
        raise Exception("Write operation failed.")


@is_authenticated
def resolve_create_customer_record(
    _, info, name: str, priority: str, contact: str, trip: str, package: str
):
    datetime_obj = my_timezone.localize(datetime.now())

    customer_obj = {
        "name": name,
        "priority": priority,
        "contact": contact,
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
    _, info, id, name: str, priority: str, contact: str, trip: str, package: str
):
    customer_obj = customers_collection.find_one({"_id": ObjectId(id)})

    if name or priority or contact or trip or package:
        if name:
            update = customers_collection.update_one(
                {"name": customer_obj["name"]}, {"$set": {"name": name}}  # type: ignore
            )

            try:
                assert update.acknowledged == True

            except AssertionError:
                raise Exception("Write operation failed.")

        if priority:
            update = customers_collection.update_one(
                {"priority": customer_obj["priority"]}, {"$set": {"priority": priority}}  # type: ignore
            )

            try:
                assert update.acknowledged == True

            except AssertionError:
                raise Exception("Write operation failed.")

        if contact:
            update = customers_collection.update_one(
                {"contact": customer_obj["contact"]}, {"$set": {"contact": contact}}  # type: ignore
            )

            try:
                assert update.acknowledged == True

            except AssertionError:
                raise Exception("Write operation failed.")

        if trip:
            update = customers_collection.update_one(
                {"trip": customer_obj["trip"]}, {"$set": {"trip": trip}}  # type: ignore
            )

            try:
                assert update.acknowledged == True

            except AssertionError:
                raise Exception("Write operation failed.")

        if package:
            update = customers_collection.update_one(
                {"package": customer_obj["package"]},  # type: ignore
                {"$set": {"package": float(package)}},
            )

            try:
                assert update.acknowledged == True

            except AssertionError:
                raise Exception("Write operation failed.")

        date_obj = my_timezone.localize(datetime.now())

        update = production_collection.update_one(
            {"updated_on": production_obj["updated_on"]},  # type: ignore
            {"$set": {"updated_on": date_obj.timestamp()}},
        )

        return True

    else:
        raise Exception("Empty request. Nothing to update.")


@is_authenticated
def resolve_delete_customer_record(_, info, id):
    delete = customers_collection.delete_one({"_id": ObjectId(id)})

    if delete.deleted_count == 1:
        return True

    else:
        raise Exception("Write operation failed.")
