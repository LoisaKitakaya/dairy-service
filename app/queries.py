import os
from dotenv import load_dotenv
from pymongo import MongoClient
from bson.objectid import ObjectId
from app.decorators import is_authenticated

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


@is_authenticated
def resolve_get_all_users(_, info):
    all_users = None

    try:
        all_users = users_collection.find()

    except Exception as e:
        raise Exception(str(e))

    finally:
        return all_users


@is_authenticated
def resolve_get_all_production_records(_, info):
    all_products_records = None

    try:
        all_products_records = production_collection.find()

    except Exception as e:
        raise Exception(str(e))

    finally:
        return all_products_records


@is_authenticated
def resolve_get_production_record(_, info, id: str):
    production_record = None

    try:
        production_record = production_collection.find_one({"_id": ObjectId(id)})

    except Exception as e:
        raise Exception(str(e))

    finally:
        return production_record


@is_authenticated
def resolve_get_all_payment_records(_, info):
    all_payment_records = None

    try:
        all_payment_records = payment_collection.find()

    except Exception as e:
        raise Exception(str(e))

    finally:
        return all_payment_records


@is_authenticated
def resolve_get_payment_record(_, info, id: str):
    payment_record = None

    try:
        payment_record = payment_collection.find_one({"_id": ObjectId(id)})

    except Exception as e:
        raise Exception(str(e))

    finally:
        return payment_record


@is_authenticated
def resolve_get_all_customer_records(_, info):
    all_customer_records = None

    try:
        all_customer_records = customers_collection.find()

    except Exception as e:
        raise Exception(str(e))

    finally:
        return all_customer_records


@is_authenticated
def resolve_get_customer_record(_, info, id: str):
    customer_record = None

    try:
        customer_record = customers_collection.find_one({"_id": ObjectId(id)})

    except Exception as e:
        raise Exception(str(e))

    finally:
        return customer_record
