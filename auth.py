import os
import jwt
import functools
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()

salt = os.getenv("SECRET_KEY")

"""
Database configuration
"""

client = MongoClient(os.getenv("DATABASE_URI"))

db = client.dairy_db

users_collection = db.app_users


def is_authenticated(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        info = args[1]

        request = info.context["request"]

        auth_header = request.headers.get("Authorization")

        if auth_header:
            auth_header_list = auth_header.split(" ")

            try:
                assert auth_header_list[0] == "Bearer"

            except AssertionError:
                raise Exception("Your authorization header must begin with 'Bearer'.")

            token = auth_header_list[1]

            decode = jwt.decode(token, salt, algorithms=["HS256"])

            try:
                user = users_collection.find_one({"username": decode["username"]})

                assert user is not None and user["username"] == decode["username"]

            except:
                raise Exception("Invalid authentication token.")

            else:
                return func(*args, **kwargs)

        else:
            raise Exception("Access denied. Could not authenticate.")

    return wrapper
