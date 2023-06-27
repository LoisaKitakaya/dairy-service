import pytest
from db.db import *
from db.actions import (
    create_tables as ct,
    delete_tables as dt,
    create_record as _ct,
    delete_record as _dt,
)
from click.testing import CliRunner
from main import app as flask_app, daily_update


class TestMainApp:
    @pytest.fixture()
    def app(self):
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
    def client(self, app):
        return app.test_client()

    def test_check_connection(self, client):
        res = client.get("/check_connection/")

        assert res.status_code == 200

        assert res.json["data"]["message"] == "Connection successful."

    def test_view_all_records(self, client):
        res = client.get("/view_all_records/")

        assert res.status_code == 200

        assert (
            res.json["data"]["message"]
            == "1 record(s) found in table 'milk_production'."
        )

        for record in res.json["data"]["records"]:
            assert record["id"] == 1
            assert record["name"] == "Cow"
            assert record["morning_production"] == 5.6
            assert record["afternoon_production"] == 4.7
            assert record["evening_production"] == 6.1
            assert record["production_unit"] == "Litres"
            assert record["production_date"] == 1687813200.0

    def test_view_record(self, client):
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

    def test_view_record_by_date(self, client):
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

    def test_daily_update(self):
        create_tables()

        res = daily_update(testing=True)

        assert res == True

        delete_tables()


runner = CliRunner()


class TestAppActionsTables:
    def test_create_tables(self):
        res = runner.invoke(ct)

        assert res.exit_code == 0
        assert res.output == "Tables created successfully.\n"

    def test_delete_tables(self):
        res = runner.invoke(dt)

        assert res.exit_code == 0
        assert res.output == "Tables deleted successfully.\n"


class TestAppActionsRecords:
    def test_create_record(self):
        create_tables()

        input_params = [
            "--animal",
            "Cow 1",
            "--morning-production",
            10.5,
            "--afternoon-production",
            12.3,
            "--evening-production",
            9.2,
            "--production-unit",
            "Litres",
            "--production-date",
            "2023-06-25",
        ]

        res = runner.invoke(_ct, input_params)

        assert res.exit_code == 0
        assert res.output == "Record has been created successfully.\n"

        delete_tables()

    def test_delete_record(self):
        create_tables()

        input_params = ["--id", 1]

        res = runner.invoke(_dt, input_params)

        assert res.exit_code == 0
        assert res.output == "Record has been deleted successfully.\n"

        delete_tables()
