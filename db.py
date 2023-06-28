from datetime import datetime
from main import db_connect, my_timezone

date_obj = my_timezone.localize(datetime.strptime("2023-6-27", "%Y-%m-%d"))

SAMPLE_DATA = {
    "name": "Cow",
    "morning_production": 5.6,
    "afternoon_production": 4.7,
    "evening_production": 6.1,
    "production_unit": "Litres",
    "production_date": date_obj,
}


def create_tables():
    conn = None

    try:
        conn = db_connect()

        cur = conn.cursor()

        cur.execute(
            """
            CREATE TABLE
                milk_production (
                    id SERIAL PRIMARY KEY,
                    animal VARCHAR(50) UNIQUE NOT NULL,
                    morning_production FLOAT NOT NULL,
                    afternoon_production FLOAT NOT NULL,
                    evening_production FLOAT NOT NULL,
                    production_unit VARCHAR(50) NOT NULL,
                    production_date DATE NOT NULL
                );
            """
        )

        conn.commit()

        cur.close()

    except Exception as error:
        raise Exception(str(error))

    finally:
        if conn is not None:
            conn.close()

    return


def delete_tables():
    conn = None

    try:
        conn = db_connect()

        cur = conn.cursor()

        cur.execute(f"DROP TABLE milk_production;")

        conn.commit()

        cur.close()

    except Exception as error:
        raise Exception(str(error))

    finally:
        if conn is not None:
            conn.close()

    return


def create_record(
    animal: str = SAMPLE_DATA["name"],
    morning_production: float = SAMPLE_DATA["morning_production"],
    afternoon_production: float = SAMPLE_DATA["afternoon_production"],
    evening_production: float = SAMPLE_DATA["evening_production"],
    production_unit: str = SAMPLE_DATA["production_unit"],
    production_date: datetime = SAMPLE_DATA["production_date"],
):
    conn = None

    try:
        conn = db_connect()

        cur = conn.cursor()

        cur.execute(
            f"INSERT INTO milk_production(animal, morning_production, afternoon_production, evening_production, production_unit, production_date) VALUES('{animal}', {morning_production}, { afternoon_production}, {evening_production}, '{production_unit}', '{production_date.date()}')"
        )

        conn.commit()

        cur.close()

    except Exception as error:
        raise Exception(str(error))

    finally:
        if conn is not None:
            conn.close()

    return


def delete_record(table: str = "milk_production", id: int = 1):
    conn = None

    try:
        conn = db_connect()

        cur = conn.cursor()

        cur.execute(f"DELETE from {table} WHERE id = {id};")

        conn.commit()

        cur.close()

    except Exception as error:
        raise Exception(str(error))

    finally:
        if conn is not None:
            conn.close()

    return
