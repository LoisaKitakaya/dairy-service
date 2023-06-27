import click
from main import db_connect
from datetime import datetime


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


cli.add_command(create_tables)
cli.add_command(delete_tables)


if __name__ == "__main__":
    cli()
