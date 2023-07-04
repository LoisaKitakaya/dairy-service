import os
import time
import schedule
import threading
from flask_cors import CORS
from dotenv import load_dotenv
from flask import Flask, jsonify, request
from ariadne.explorer import ExplorerGraphiQL
from ariadne import (
    QueryType,
    MutationType,
    graphql_sync,
    load_schema_from_path,
    make_executable_schema,
)

load_dotenv()

web_app = os.getenv("WEB_APP")


"""
Scheduled operations
"""

from tasks import daily_update

task_lock = threading.Lock()


def schedule_task():
    with task_lock:
        schedule.every().day.at("20:00", "Africa/Nairobi").do(daily_update)


schedule_task()


def run_scheduled_tasks():
    while True:
        schedule.run_pending()
        time.sleep(1)


schedule_thread = threading.Thread(target=run_scheduled_tasks, daemon=True)
schedule_thread.start()


"""
GraphQl setup
"""

from queries import *
from mutations import *

type_defs = load_schema_from_path("schema.graphql")

query = QueryType()
mutation = MutationType()

# app queries

query.set_field("get_all_production_records", resolve_get_all_production_records)
query.set_field("get_production_record", resolve_get_production_record)
query.set_field("get_all_payment_records", resolve_get_all_payment_records)
query.set_field("get_payment_record", resolve_get_payment_record)
query.set_field("get_all_customer_records", resolve_get_all_customer_records)
query.set_field("get_customer_record", resolve_get_customer_record)

# app mutations

mutation.set_field("create_user", resolve_create_user)
mutation.set_field("authenticate_user", resolve_authenticate_user)

mutation.set_field("create_production_record", resolve_create_production_record)
mutation.set_field("update_production_record", resolve_update_production_record)
mutation.set_field("delete_production_record", resolve_delete_production_record)
mutation.set_field("create_payment_record", resolve_create_payment_record)
mutation.set_field("update_payment_record", resolve_update_payment_record)
mutation.set_field("delete_payment_record", resolve_delete_payment_record)
mutation.set_field("create_customer_record", resolve_create_customer_record)
mutation.set_field("update_customer_record", resolve_update_customer_record)
mutation.set_field("delete_customer_record", resolve_delete_customer_record)

schema = make_executable_schema(type_defs, [query, mutation])


"""
Main Flask application
"""

app = Flask(__name__)


CORS(app, resources={r"/*": {"origins": web_app}})

explorer_html = ExplorerGraphiQL().html(None)


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


if __name__ == "__main__":
    app.run(
        debug=os.getenv("FLASK_DEBUG", default=False),  # type: ignore
        port=os.getenv("PORT", default=5000),  # type: ignore
    )
