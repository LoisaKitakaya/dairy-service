import pytest
from main import app as flask_app
from actions import *


@pytest.fixture()
def app():
    flask_app.config.update(
        {
            "TESTING": True,
        }
    )

    # setup

    create_tables()

    create_record()

    yield flask_app

    # cleanup / reset

    delete_record()

    delete_tables()


@pytest.fixture()
def client(app):
    return app.test_client()


def test_check_connection(client):
    res = client.get("/check_connection/")

    assert res.status_code == 200

    assert (
        res.json["data"]["message"]
        == "Connection successful: ('PostgreSQL 14.7 (Ubuntu 14.7-0ubuntu0.22.04.1) on x86_64-pc-linux-gnu, compiled by gcc (Ubuntu 11.3.0-1ubuntu1~22.04) 11.3.0, 64-bit',)"
    )


def test_view_all_records(client):
    res = client.get("/view_all_records/")

    assert res.status_code == 200

    assert (
        res.json["data"]["message"] == "1 record(s) found in table 'milk_production'."
    )

    for record in res.json["data"]["records"]:
        assert record["id"] == 1
        assert record["name"] == "Cow"
        assert record["morning_production"] == 5.6
        assert record["afternoon_production"] == 4.7
        assert record["evening_production"] == 6.1
        assert record["production_unit"] == "Litres"
        assert record["production_date"] == 1687813200.0

def test_
