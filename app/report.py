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

expenses_collection = db.production_expenses

auto_report_collection = db.auto_gen_reports


"""
timezone and datetime settings
"""

my_timezone = timezone("Africa/Nairobi")


class AutoReport:
    def __init__(self, start_date, end_date) -> None:
        self.start_date = start_date
        self.end_date = end_date

        self.avg_market_price = 70

    @property
    def market(self):
        return self.avg_market_price

    @market.setter
    def market(self, val):
        self.avg_market_price = val

    def fetch_data(self):
        production_query = {
            "production_date": {
                "$gte": self.end_date.timestamp(),
                "$lte": self.start_date.timestamp(),
            }
        }

        payment_query = {
            "payment_date": {
                "$gte": self.end_date.timestamp(),
                "$lte": self.start_date.timestamp(),
            }
        }

        expenses_query = {
            "date_of_action": {
                "$gte": self.end_date.timestamp(),
                "$lte": self.start_date.timestamp(),
            }
        }

        production = production_collection.find(production_query)
        payment = payment_collection.find(payment_query)
        expenses = expenses_collection.find(expenses_query)

        data = {"production": production, "payment": payment, "expenses": expenses}

        return data

    def get_report_data(self, production: list, payment: list, expenses: list) -> dict:
        production_len = 0

        total_milk_production = 0
        total_expected_earnings = 0

        total_earnings = 0

        total_expenses = 0

        mpesa_count = 0
        cash_count = 0

        rent_expenses = 0
        utilities_expenses = 0
        salaries_wages = 0
        raw_materials_expenses = 0
        direct_labor_expenses = 0
        manufacturing_overhead_expenses = 0
        packaging_expenses = 0
        shipping_expenses = 0

        if production:
            for milk in production:
                total = (
                    milk["morning_production"]
                    + milk["afternoon_production"]
                    + milk["evening_production"]
                )

                earnings = total * self.avg_market_price

                total_milk_production += total
                total_expected_earnings += earnings

                production_len += 1

        if payment:
            for earnings in payment:
                total_earnings += earnings["amount"]

                if earnings["payment_method"] == "Mpesa":
                    mpesa_count += 1

                elif earnings["payment_method"] == "Cash":
                    cash_count += 1

        if expenses:
            for expense in expenses:
                total_expenses += expense["amount"]

                if expense["category"] == "Rent Expenses":
                    rent_expenses += 1
                if expense["category"] == "Utilities Expenses":
                    utilities_expenses += 1
                if expense["category"] == "Salaries and Wages":
                    salaries_wages += 1
                if expense["category"] == "Raw Materials Expenses":
                    raw_materials_expenses += 1
                if expense["category"] == "Direct Labor Expenses":
                    direct_labor_expenses += 1
                if expense["category"] == "Manufacturing Overhead Expenses":
                    manufacturing_overhead_expenses += 1
                if expense["category"] == "Packaging Expenses":
                    packaging_expenses += 1
                if expense["category"] == "Shipping Expenses":
                    shipping_expenses += 1

        return {
            "production": {
                "total_milk_production": total_milk_production,
                "average_milk_production": total_milk_production / production_len,
            },
            "payment": {
                "gross_earnings": total_earnings,
                "expected_gross_earnings": total_expected_earnings,
                "net_earnings": total_earnings - total_expenses,
                "payment_methods_stats": {
                    "mpesa_count": mpesa_count,
                    "cash_count": cash_count,
                },
            },
            "expenses": {
                "total_expenses": total_expenses,
                "expense_category_stats": {
                    "rent_expenses": rent_expenses,
                    "utilities_expenses": utilities_expenses,
                    "salaries_wages": salaries_wages,
                    "raw_materials_expenses": raw_materials_expenses,
                    "direct_labor_expenses": direct_labor_expenses,
                    "manufacturing_overhead_expenses": manufacturing_overhead_expenses,
                    "packaging_expenses": packaging_expenses,
                    "shipping_expenses": shipping_expenses,
                },
            },
        }

    def save_report(self, report_data: dict, start: datetime, end: datetime):
        datetime_obj = my_timezone.localize(datetime.now())

        new_data = {
            "created_on": datetime_obj.timestamp(),
            "updated_on": datetime_obj.timestamp(),
            "title": f"Weekly report - {str(end.date())} to {str(start.date())}",
        }

        report_data.update(new_data)

        report = auto_report_collection.insert_one(report_data)

        if report.acknowledged:
            return report

        else:
            raise Exception("Write operation failed.")
