import os
from dotenv import load_dotenv
from bson.objectid import ObjectId
from app.decorators import is_authenticated
from pymongo import MongoClient, ASCENDING

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

users_collection = db.app_users

auto_report_collection = db.auto_gen_reports


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
        all_products_records = production_collection.find().sort("_id", ASCENDING)

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
        all_payment_records = payment_collection.find().sort("_id", ASCENDING)

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
        all_customer_records = customers_collection.find().sort("_id", ASCENDING)

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


@is_authenticated
def resolve_get_all_expense_records(_, info):
    all_expense_records = None

    try:
        all_expense_records = expenses_collection.find().sort("_id", ASCENDING)

    except Exception as e:
        raise Exception(str(e))

    finally:
        return all_expense_records


@is_authenticated
def resolve_get_expense_record(_, info, id: str):
    expense_record = None

    try:
        expense_record = expenses_collection.find_one({"_id": ObjectId(id)})

    except Exception as e:
        raise Exception(str(e))

    finally:
        return expense_record


@is_authenticated
def resolve_get_all_auto_reports_records(_, info):
    all_report_records = None
    record_list = []

    try:
        all_report_records = auto_report_collection.find().sort("_id", ASCENDING)

    except Exception as e:
        raise Exception(str(e))

    finally:
        if all_report_records:
            for report_record in all_report_records:
                report_record["_id"] = str(report_record["_id"])

                record_list.append(report_record)

        return record_list


@is_authenticated
def resolve_get_auto_reports_record(_, info, id: str):
    report_record = None

    try:
        report_record = auto_report_collection.find_one({"_id": ObjectId(id)})

    except Exception as e:
        raise Exception(str(e))

    finally:
        if report_record:
            report_record["_id"] = str(report_record["_id"])

        return report_record
