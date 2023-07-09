import os
import bcrypt
import requests
from pytz import timezone
from datetime import datetime
from dotenv import load_dotenv
from pymongo import MongoClient
from bson.objectid import ObjectId

load_dotenv()

"""
Database configuration
"""

CLIENT = MongoClient(os.getenv("DATABASE_URI"))

db = CLIENT.dairy_db

users_collection = db.app_users


"""
timezone and datetime settings
"""

my_timezone = timezone("Africa/Nairobi")


class TelegramBot:
    def __init__(self, token: str) -> None:
        self.token = token
        self.url = f"https://api.telegram.org/bot{token}"

        self.valid_commands = [
            "new",
            "update",
            "view",
            "delete",
            "permissions",
            "commands",
            "start",
        ]

    @property
    def list_commands(self):
        return self.valid_commands

    def parse_message(self, message: dict):
        msg = message["message"]["text"]
        chat_id = message["message"]["chat"]["id"]

        return {"chat_id": chat_id, "msg": msg}

    def send_message(self, chat_id: str, message: str):
        payload = {"chat_id": chat_id, "text": message}

        requests.post(f"{self.url}/sendMessage", json=payload)

        return

    def new(self, chat_id: str, command: list):
        admin = users_collection.find_one({"username": "admin"})

        hashed_password = admin["password"]  # type: ignore

        if bcrypt.checkpw(command[4].encode(), hashed_password):
            existing_email = users_collection.find_one({"email": command[2]})
            existing_username = users_collection.find_one({"username": command[1]})

            if not existing_email and not existing_username:
                datetime_obj = my_timezone.localize(datetime.now())

                hashed_password = bcrypt.hashpw(command[3].encode(), bcrypt.gensalt())

                new_user = {
                    "username": command[1],
                    "email": command[2],
                    "password": hashed_password,
                    "status": "active",
                    "permission": "read",
                    "date_joined": datetime_obj.timestamp(),
                    "created_on": datetime_obj.timestamp(),
                    "updated_on": datetime_obj.timestamp(),
                }

                user = users_collection.insert_one(new_user)

                if user.acknowledged:
                    pass

                else:
                    raise Exception("Write operation failed.")

            else:
                raise Exception("User already exists.")

            new_user = users_collection.find_one({"_id": user.inserted_id})

            username = new_user["username"]  # type: ignore
            email = new_user["email"]  # type: ignore
            permission = new_user["permission"]  # type: ignore

            message = f"""
                Created new user.
                \nid: {str(user.inserted_id)}
                \nusername: {username}
                \nemail: {email}
                \npermission: {permission}
            """

            payload = {"chat_id": chat_id, "text": message}

            requests.post(f"{self.url}/sendMessage", json=payload)

        else:
            message = f"LOL! 😂😂😂😂😂"

            payload = {"chat_id": chat_id, "text": message}

            requests.post(f"{self.url}/sendMessage", json=payload)

        return

    def update(self, chat_id: str, command: list):
        admin = users_collection.find_one({"username": "admin"})

        hashed_password = admin["password"]  # type: ignore

        if bcrypt.checkpw(command[5].encode(), hashed_password):
            update = users_collection.update_one(
                {"_id": ObjectId(command[1])}, {"$set": {"username": command[2]}}
            )

            try:
                assert update.acknowledged == True

            except AssertionError:
                raise Exception("Write operation failed.")

            update = users_collection.update_one(
                {"_id": ObjectId(command[1])}, {"$set": {"email": command[3]}}
            )

            try:
                assert update.acknowledged == True

            except AssertionError:
                raise Exception("Write operation failed.")

            update = users_collection.update_one(
                {"_id": ObjectId(command[1])}, {"$set": {"password": command[4]}}
            )

            try:
                assert update.acknowledged == True

            except AssertionError:
                raise Exception("Write operation failed.")

            date_obj = my_timezone.localize(datetime.now())

            update = users_collection.update_one(
                {"_id": ObjectId(command[1])},
                {"$set": {"updated_on": date_obj.timestamp()}},
            )

            updated_user = users_collection.find_one({"_id": ObjectId(command[1])})

            username = updated_user["username"]  # type: ignore
            email = updated_user["email"]  # type: ignore
            permission = updated_user["permission"]  # type: ignore

            message = f"""
                Created new user.
                \nid: {ObjectId(command[1])}
                \nusername: {username}
                \nemail: {email}
                \npermission: {permission}
            """

            payload = {"chat_id": chat_id, "text": message}

            requests.post(f"{self.url}/sendMessage", json=payload)

        else:
            message = f"LOL! 😂😂😂😂😂"

            payload = {"chat_id": chat_id, "text": message}

            requests.post(f"{self.url}/sendMessage", json=payload)

        return

    def view(self, chat_id: str, command: str):
        admin = users_collection.find_one({"username": "admin"})

        hashed_password = admin["password"]  # type: ignore

        if bcrypt.checkpw(command[1].encode(), hashed_password):

            all_users = None

            try:
                all_users = users_collection.find()

            except Exception as e:
                raise Exception(str(e))

            all_users_list = "\n"

            for user in all_users:
                id = user["_id"]  # type: ignore
                username = user["username"]  # type: ignore
                email = user["email"]  # type: ignore
                permission = user["permission"]  # type: ignore

                all_users_list = (
                    all_users_list
                    + f"\n[id: {id}, username: {username}, email: {email}, permission: {permission}]\n"
                )

            message = f"""
                All users in the database:
                {all_users_list}
            """

            payload = {"chat_id": chat_id, "text": message}

            requests.post(f"{self.url}/sendMessage", json=payload)

        else:
            message = f"LOL! 😂😂😂😂😂"

            payload = {"chat_id": chat_id, "text": message}

            requests.post(f"{self.url}/sendMessage", json=payload)

        return

    def delete(self, chat_id: str, command: list):
        admin = users_collection.find_one({"username": "admin"})

        hashed_password = admin["password"]  # type: ignore

        if bcrypt.checkpw(command[2].encode(), hashed_password):

            delete = users_collection.delete_one({"_id": ObjectId(command[1])})

            if delete.deleted_count == 1:
                pass

            else:
                raise Exception("Write operation failed.")

            message = f"""
                Deleted user successfully:
                \ndeleted count: {delete.deleted_count}
            """

            payload = {"chat_id": chat_id, "text": message}

            requests.post(f"{self.url}/sendMessage", json=payload)

        else:
            message = f"LOL! 😂😂😂😂😂"

            payload = {"chat_id": chat_id, "text": message}

            requests.post(f"{self.url}/sendMessage", json=payload)

        return

    def permissions(self, chat_id: str, command: list):
        admin = users_collection.find_one({"username": "admin"})

        hashed_password = admin["password"]  # type: ignore

        if bcrypt.checkpw(command[3].encode(), hashed_password):
            update = users_collection.update_one(
                {"_id": ObjectId(command[1])}, {"$set": {"permission": command[2]}}
            )

            try:
                assert update.acknowledged == True

            except AssertionError:
                raise Exception("Write operation failed.")

            date_obj = my_timezone.localize(datetime.now())

            update = users_collection.update_one(
                {"_id": ObjectId(command[1])},
                {"$set": {"updated_on": date_obj.timestamp()}},
            )

            updated_user = users_collection.find_one({"_id": ObjectId(command[1])})

            username = updated_user["username"]  # type: ignore
            email = updated_user["email"]  # type: ignore
            permission = updated_user["permission"]  # type: ignore

            message = f"""
                Updated user permissions.
                \nid: {ObjectId(command[1])}
                \nusername: {username}
                \nemail: {email}
                \npermission: {permission}
            """

            payload = {"chat_id": chat_id, "text": message}

            requests.post(f"{self.url}/sendMessage", json=payload)

        else:
            message = f"LOL! 😂😂😂😂😂"

            payload = {"chat_id": chat_id, "text": message}

            requests.post(f"{self.url}/sendMessage", json=payload)

        return

    def commands(self, chat_id: str, command: list):
        message = """
            All available commands:
            \n-> /commands
            \n-> /new
            \n-> /update
            \n-> /view
            \n-> /delete
            \n-> /permissions
            \nUsage:
            \n-> /new
            \n/new [username] [email] [password] [salt]
            \n-> /update
            \n/update [id] [new username] [new email] [new password] [salt]
            \n-> /view
            \n/view [salt]
            \n-> /delete
            \n/delete [id] [salt]
            \n-> /permissions
            \n/permissions [id] [permission] [salt]
        """

        payload = {"chat_id": chat_id, "text": message}

        requests.post(f"{self.url}/sendMessage", json=payload)

        return

    def start(self, chat_id: str):
        message = """
            Hello there! I am Rislo Farm Bot, your virtual admin assistant.\nI can help with the following operations:
            -> Adding new users to the database.
            -> Updating user information (including user permissions).
            -> Viewing user information.
            -> deleting users from the database.
            -> changing user permissions.\nType /commands to see the list of commands at your disposal.
        """
        payload = {"chat_id": chat_id, "text": message}

        requests.post(f"{self.url}/sendMessage", json=payload)

        return
