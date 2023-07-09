import os
import time
import schedule
import threading
from flask import Response
from flask_cors import CORS
from dotenv import load_dotenv
from app.bot import TelegramBot
from flask import Flask, jsonify, request
from ariadne.explorer import ExplorerGraphiQL
from ariadne import (
    QueryType,
    ScalarType,
    MutationType,
    graphql_sync,
    load_schema_from_path,
    make_executable_schema,
)

load_dotenv()

WEB_APP = os.getenv("WEB_APP")
BOT = os.getenv("TELEGRAM_TOKEN")


"""
Scheduled operations
"""

from app.tasks import weekly_update

task_lock = threading.Lock()


def schedule_task():
    with task_lock:
        schedule.every().monday.at("06:00", "Africa/Nairobi").do(weekly_update)


schedule_task()


def run_scheduled_tasks():
    while True:
        schedule.run_pending()
        time.sleep(1)


schedule_thread = threading.Thread(target=run_scheduled_tasks, daemon=True)
schedule_thread.start()


"""
GraphQl api setup
"""

from app.queries import *
from app.mutations import *

type_defs = load_schema_from_path("schema.graphql")

query = QueryType()
mutation = MutationType()

# custom scalar type

otp_scalar = ScalarType("OTP")
token_scalar = ScalarType("Token")
password_scalar = ScalarType("Password")


@otp_scalar.serializer
def serialize_otp(value):
    return value


@token_scalar.serializer
def serialize_token(value):
    return value


@password_scalar.serializer
def serialize_password(value):
    return value


# app queries

query.set_field("get_all_users", resolve_get_all_users)

query.set_field("get_all_production_records", resolve_get_all_production_records)
query.set_field("get_production_record", resolve_get_production_record)
query.set_field("get_all_payment_records", resolve_get_all_payment_records)
query.set_field("get_payment_record", resolve_get_payment_record)
query.set_field("get_all_customer_records", resolve_get_all_customer_records)
query.set_field("get_customer_record", resolve_get_customer_record)
query.set_field("get_all_expense_records", resolve_get_all_expense_records)
query.set_field("get_expense_record", resolve_get_expense_record)

# app mutations

mutation.set_field("create_user", resolve_create_user)
mutation.set_field("authenticate_user", resolve_authenticate_user)
mutation.set_field("request_reset", resolve_request_reset)
mutation.set_field("password_reset", resolve_password_reset)

mutation.set_field("create_production_record", resolve_create_production_record)
mutation.set_field("update_production_record", resolve_update_production_record)
mutation.set_field("delete_production_record", resolve_delete_production_record)
mutation.set_field("create_payment_record", resolve_create_payment_record)
mutation.set_field("update_payment_record", resolve_update_payment_record)
mutation.set_field("delete_payment_record", resolve_delete_payment_record)
mutation.set_field("create_customer_record", resolve_create_customer_record)
mutation.set_field("update_customer_record", resolve_update_customer_record)
mutation.set_field("delete_customer_record", resolve_delete_customer_record)
mutation.set_field("create_expense_record", resolve_create_expense_record)
mutation.set_field("update_expense_record", resolve_update_expense_record)
mutation.set_field("delete_expense_record", resolve_delete_expense_record)

schema = make_executable_schema(
    type_defs,
    [query, mutation, otp_scalar, token_scalar, password_scalar],
)


"""
Main Flask application
"""

app = Flask(__name__)


CORS(app, resources={r"/*": {"origins": WEB_APP}})

explorer_html = ExplorerGraphiQL().html(None)


"""
GraphQL api endpoint
"""


@app.route("/graphql/", methods=["GET"])
def graphql_explorer():
    return explorer_html, 200


@app.route("/graphql/", methods=["POST"])
def graphql_server():
    data = request.get_json()

    success, result = graphql_sync(
        schema, data, context_value={"request": request}, debug=app.debug
    )

    status_code = 200 if success else 400
    return jsonify(result), status_code


"""
Telegram webhook
"""


@app.route("/telegram/", methods=["POST"])
def telegram_server():
    bot = TelegramBot(BOT)  # type: ignore

    bot_commands = bot.list_commands

    parsed_data = bot.parse_message(request.get_json())

    chat_id = parsed_data["chat_id"]
    command = parsed_data["msg"].strip("/")

    command = command.split()

    try:
        if command[0] not in bot_commands:
            reply = """
                Entered invalid command.
                \nType /commands to get a list of all the valid commands commands.
            
            """

            bot.send_message(chat_id, reply)

        else:
            if command[0] == "new":
                bot.new(chat_id, command)

            elif command[0] == "update":
                bot.update(chat_id, command)

            elif command[0] == "view":
                bot.view(chat_id, command)

            elif command[0] == "delete":
                bot.delete(chat_id, command)

            elif command[0] == "permissions":
                bot.permissions(chat_id, command)

            elif command[0] == "commands":
                bot.commands(chat_id)

            elif command[0] == "start":
                bot.start(chat_id)

    except Exception as e:
        if os.getenv("FLASK_DEBUG"):
            print(e)
        else:
            pass

    finally:
        return Response("ok", 200)


if __name__ == "__main__":
    app.run(
        debug=os.getenv("FLASK_DEBUG", default=False),  # type: ignore
        port=os.getenv("PORT", default=5000),  # type: ignore
    )
