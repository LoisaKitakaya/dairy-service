import click
from datetime import datetime
from main import db_connect, my_timezone


@click.group()
def cli():
    pass


@click.command()
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
                    animal VARCHAR(50) NOT NULL,
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

        click.echo("Tables created successfully.")

    except Exception as error:
        raise Exception(str(error))

    finally:
        if conn is not None:
            conn.close()

    return


@click.command()
def delete_tables():
    conn = None

    try:
        conn = db_connect()

        cur = conn.cursor()

        cur.execute(f"DROP TABLE milk_production;")

        conn.commit()

        cur.close()

        click.echo("Tables deleted successfully.")

    except Exception as error:
        raise Exception(str(error))

    finally:
        if conn is not None:
            conn.close()

    return


@click.command()
@click.option(
    "--animal",
    prompt="name of cow",
    help="This represents the name of the animal (cow).",
)
@click.option(
    "--morning-production",
    prompt="morning production",
    help="This represents the amount (e.g. in Litres) produced by the cow in the morning.",
)
@click.option(
    "--afternoon-production",
    prompt="afternoon production",
    help="This represents the amount (e.g. in Litres) produced by the cow in the afternoon.",
)
@click.option(
    "--evening-production",
    prompt="evening production",
    help="This represents the amount (e.g. in Litres) produced by the cow in the evening.",
)
@click.option(
    "--production-unit",
    default="Litres",
    help="This represents the unit of production, default: Litres.",
)
@click.option(
    "--production-date",
    prompt="date of production",
    help='This represents the date of production (of milk by each cow), e.g. "2023-10-231"',
)
def create_record(
    animal: str,
    morning_production: float,
    afternoon_production: float,
    evening_production: float,
    production_unit: str,
    production_date: str,
):
    conn = None

    date_obj = my_timezone.localize(datetime.strptime(production_date, "%Y-%m-%d"))

    try:
        conn = db_connect()

        cur = conn.cursor()

        cur.execute(
            f"INSERT INTO milk_production(animal, morning_production, afternoon_production, evening_production, production_unit, production_date) VALUES('{animal}', {morning_production}, { afternoon_production}, {evening_production}, '{production_unit}', '{date_obj.date()}')"
        )

        conn.commit()

        cur.close()

        click.echo("Record has been created successfully.")

    except Exception as error:
        raise Exception(str(error))

    finally:
        if conn is not None:
            conn.close()

    return


@click.command()
@click.option(
    "--table",
    default="milk_production",
    help="This represents the name of the database table to query.",
)
@click.option(
    "--id",
    help="This represents the id (a unique identifier) of a record in a table in the database to query.",
)
def delete_record(table: str, id: int):
    conn = None

    try:
        conn = db_connect()

        cur = conn.cursor()

        cur.execute(f"DELETE from {table} WHERE id = {id};")

        conn.commit()

        cur.close()

        click.echo("Record has been deleted successfully.")

    except Exception as error:
        raise Exception(str(error))

    finally:
        if conn is not None:
            conn.close()

    return


cli.add_command(create_tables)
cli.add_command(delete_tables)
cli.add_command(create_record)
cli.add_command(delete_record)


if __name__ == "__main__":
    cli()
