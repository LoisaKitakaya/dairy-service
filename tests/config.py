import os
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()

"""
Database configuration
"""

CLIENT = MongoClient(os.getenv("DATABASE_URI"))


def check_database_exists(database_name):
    database_list = CLIENT.list_database_names()
    
    return database_name in database_list


def delete_database(database_name):
    CLIENT.drop_database(database_name)
