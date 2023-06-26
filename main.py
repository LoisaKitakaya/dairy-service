import os
import psycopg2
from pytz import timezone
from datetime import datetime
from dotenv import load_dotenv
from flask import Flask, jsonify

load_dotenv()

my_timezone = timezone("Africa/Nairobi")


def make_timestamp(date_sr: str):
    date_obj = datetime.strptime(date_sr, "%Y-%m-%d")

    return date_obj.timestamp()


def db_connect():
    return psycopg2.connect(
        database=os.getenv("DATABASE_NAME"),
        user=os.getenv("DATABASE_USER"),
        host=os.getenv("DATABASE_HOST"),
        password=os.getenv("DATABASE_PASSWORD"),
        port=os.getenv("DATABASE_PORT"),
    )


def daily_update():
    conn = None

    records = None

    formatted_records = []

    date_obj = my_timezone.localize(datetime.today())

    try:
        conn = db_connect()

        cur = conn.cursor()

        cur.execute(
            f"SELECT * FROM milk_production WHERE production_date = '{date_obj.date()}';"
        )

        records = cur.fetchall()

        cur.close()

    except Exception as error:
        raise Exception(str(error))

    finally:
        if conn is not None:
            conn.close()

    if records:
        for record in records:
            new_record = {
                "name": record[1],
                "morning_production": record[2],
                "afternoon_production": record[3],
                "evening_production": record[4],
                "total_production": (record[2] + record[3] + record[4]),
            }

            formatted_records.append(new_record)

    else:
        pass


def create_app():
    app = Flask(__name__)

    @app.route("/check_connection/")
    def check_connection():
        conn = None

        db_version = None

        try:
            conn = db_connect()

            cur = conn.cursor()

            cur.execute("SELECT version()")

            db_version = cur.fetchone()

            cur.close()

        except Exception as error:
            raise Exception(str(error))

        finally:
            if conn is not None:
                conn.close()

        if db_version:
            return jsonify({"message": f"Connection successful: {db_version}"})
        else:
            return jsonify({"message": "Connection failed."})

    @app.route("/view_tables/")
    def view_tables():
        conn = None

        tables = None

        try:
            conn = db_connect()

            cur = conn.cursor()

            cur.execute(
                "SELECT table_name FROM information_schema.tables WHERE table_schema = 'public';"
            )

            tables = cur.fetchall()

            cur.close()

        except Exception as error:
            raise Exception(str(error))

        finally:
            if conn is not None:
                conn.close()

        if tables:
            return jsonify(
                {
                    "message": f"{len(tables)} tables found in the database.",
                    "tables": list(table[0] for table in tables),
                }
            )

        else:
            return jsonify({"message": f"0 tables found in the database."})

    @app.route("/view_all_records/")
    def view_all_records():
        conn = None

        records = None

        formatted_records = []

        try:
            conn = db_connect()

            cur = conn.cursor()

            cur.execute("SELECT * FROM milk_production;")

            records = cur.fetchall()

            cur.close()

        except Exception as error:
            raise Exception(str(error))

        finally:
            if conn is not None:
                conn.close()

        if records:
            for record in records:
                new_record = {
                    "id": record[0],
                    "name": record[1],
                    "morning_production": record[2],
                    "afternoon_production": record[3],
                    "evening_production": record[4],
                    "production_unit": record[5],
                    "production_date": make_timestamp(str(record[6])),
                }

                formatted_records.append(new_record)

            return jsonify(
                {
                    "message": f"{len(records)} records found in table 'milk_production'.",
                    "records": list(record for record in formatted_records),
                }
            )

        else:
            return jsonify({"message": "0 records in table 'milk_production'."})

    @app.route("/view_record/<name>/")
    def view_record(name):
        conn = None

        records = None

        formatted_records = []

        try:
            conn = db_connect()

            cur = conn.cursor()

            cur.execute(f"SELECT * FROM milk_production WHERE animal = '{name}';")

            records = cur.fetchall()

            cur.close()

        except Exception as error:
            raise Exception(str(error))

        finally:
            if conn is not None:
                conn.close()

        if records:
            for record in records:
                new_record = {
                    "id": record[0],
                    "name": record[1],
                    "morning_production": record[2],
                    "afternoon_production": record[3],
                    "evening_production": record[4],
                    "production_unit": record[5],
                    "production_date": make_timestamp(str(record[6])),
                }

                formatted_records.append(new_record)

            return jsonify(
                {
                    "message": f"{len(records)} records of '{name}' found in table 'milk_production'.",
                    "records": list(record for record in formatted_records),
                }
            )

        else:
            return jsonify(
                {"message": f"0 records of '{name}' found in table 'milk_production'."}
            )

    @app.route("/view_record_by_date/<date>/")
    def view_record_by_date(date):
        conn = None

        records = None

        formatted_records = []

        date_obj = my_timezone.localize(datetime.strptime(date, "%Y-%m-%d"))

        try:
            conn = db_connect()

            cur = conn.cursor()

            cur.execute(
                f"SELECT * FROM milk_production WHERE production_date = '{date_obj.date()}';"
            )

            records = cur.fetchall()

            cur.close()

        except Exception as error:
            raise Exception(str(error))

        finally:
            if conn is not None:
                conn.close()

        if records:
            for record in records:
                new_record = {
                    "id": record[0],
                    "name": record[1],
                    "morning_production": record[2],
                    "afternoon_production": record[3],
                    "evening_production": record[4],
                    "production_unit": record[5],
                    "production_date": make_timestamp(str(record[6])),
                }

                formatted_records.append(new_record)

            return jsonify(
                {
                    "message": f"{len(records)} records from date '{date}' found in table 'milk_production'.",
                    "records": list(record for record in formatted_records),
                }
            )

        else:
            return jsonify(
                {
                    "message": f"0 records from date '{date}' found in table 'milk_production'."
                }
            )

    return app


if __name__ == "__main__":
    app = create_app()

    app.run(
        debug=os.getenv("FLASK_DEBUG", default=False),  # type: ignore
        port=os.getenv("PORT", default=5000),  # type: ignore
    )
