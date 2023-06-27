import pytest
from db.db import *
from main import app as flask_app, daily_update


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

    assert res.json["data"]["message"] == "Connection successful."


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


def test_view_record(client):
    query = "Cow"

    res = client.get(f"/view_record/{query}/")

    assert res.status_code == 200

    assert (
        res.json["data"]["message"]
        == f"1 record(s) of '{query}' found in table 'milk_production'."
    )

    for record in res.json["data"]["records"]:
        assert record["id"] == 1
        assert record["name"] == "Cow"
        assert record["morning_production"] == 5.6
        assert record["afternoon_production"] == 4.7
        assert record["evening_production"] == 6.1
        assert record["production_unit"] == "Litres"
        assert record["production_date"] == 1687813200.0


def test_view_record_by_date(client):
    query = "2023-06-27"

    res = client.get(f"/view_record_by_date/{query}/")

    assert res.status_code == 200

    assert (
        res.json["data"]["message"]
        == f"1 record(s) from date '{query}' found in table 'milk_production'."
    )

    for record in res.json["data"]["records"]:
        assert record["id"] == 1
        assert record["name"] == "Cow"
        assert record["morning_production"] == 5.6
        assert record["afternoon_production"] == 4.7
        assert record["evening_production"] == 6.1
        assert record["production_unit"] == "Litres"
        assert record["production_date"] == 1687813200.0


def test_daily_update():
    create_tables()

    res = daily_update(testing=True)

    assert res == True

    delete_tables()
