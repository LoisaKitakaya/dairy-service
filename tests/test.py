import pytest
from .schema import *
from main import app as flask_app
from .config import delete_database, check_database_exists

if check_database_exists("dairy_db"):
    delete_database("dairy_db")

ids = {}
credentials = {}


def set_id(key, val):
    ids.update({key: val})


def get_id(key):
    return ids[key]


def set_token(val):
    credentials.update({"token": val})


def get_token():
    return credentials["token"]


class TestMainApp:
    @pytest.fixture()
    def app(self):
        flask_app.config.update(
            {
                "TESTING": True,
            }
        )

        # setup

        yield flask_app

        # cleanup / reset

    @pytest.fixture()
    def client(self, app):
        return app.test_client()

    def test_create_user(self, client):
        res = client.post(
            "/graphql/",
            json={
                "query": create_user,
                "variables": {
                    "username": "testuser",
                    "email": "testuser@example.com",
                    "password": "testpassword",
                },
            },
        )

        assert res.status_code == 200

        assert res.json["data"]["create_user"] == True

    def test_authenticate_user(self, client):
        res = client.post(
            "/graphql/",
            json={
                "query": authenticate_user,
                "variables": {
                    "username": "testuser",
                    "password": "testpassword",
                },
            },
        )

        assert res.status_code == 200

        assert res.json["data"]["authenticate_user"]["token"] is not None
        assert res.json["data"]["authenticate_user"]["authenticated"] == True

        set_token(res.json["data"]["authenticate_user"]["token"])

    def test_request_reset(self, client):
        res = client.post(
            "/graphql/",
            json={
                "query": request_reset,
                "variables": {
                    "email": "testuser@example.com",
                    "testing": True,
                },
            },
        )

        assert res.status_code == 200

        assert res.json["data"]["request_reset"]["status"] == "success"
        assert res.json["data"]["request_reset"]["credentials"] is not None

    def test_password_reset(self, client):
        res = client.post(
            "/graphql/",
            json={
                "query": password_reset,
                "variables": {
                    "email": "testuser@example.com",
                    "new_password": "newtestpassword",
                },
            },
        )

        assert res.status_code == 200

        assert res.json["data"]["password_reset"]["status"] == "success"
        assert (
            res.json["data"]["password_reset"]["message"]
            == "Your password has been updated successfully."
        )

    def test_create_production_record(self, client):
        token = get_token()

        res = client.post(
            "/graphql/",
            headers={"Authorization": f"Bearer {token}"},
            json={
                "query": create_production_record,
                "variables": {
                    "name": "animal_one",
                    "morning_production": "20",
                    "afternoon_production": "30",
                    "evening_production": "30",
                    "production_date": "2023-07-17T20:00",
                },
            },
        )

        assert res.status_code == 200

        assert res.json["data"]["create_production_record"] == True

    def test_get_all_production_records(self, client):
        token = get_token()

        res = client.post(
            "/graphql/",
            headers={"Authorization": f"Bearer {token}"},
            json={"query": all_production_records},
        )

        assert res.status_code == 200

        assert res.json["data"]["get_all_production_records"][0]["_id"] is not None
        assert res.json["data"]["get_all_production_records"][0]["name"] == "animal_one"
        assert (
            res.json["data"]["get_all_production_records"][0]["morning_production"]
            == 20.0
        )
        assert (
            res.json["data"]["get_all_production_records"][0]["afternoon_production"]
            == 30.0
        )
        assert (
            res.json["data"]["get_all_production_records"][0]["evening_production"]
            == 30.0
        )
        assert (
            res.json["data"]["get_all_production_records"][0]["production_date"]
            is not None
        )

        set_id(
            "production_record",
            res.json["data"]["get_all_production_records"][0]["_id"],
        )

    def test_update_production_record(self, client):
        token = get_token()

        id = get_id("production_record")

        res = client.post(
            "/graphql/",
            headers={"Authorization": f"Bearer {token}"},
            json={
                "query": update_production_record,
                "variables": {
                    "id": id,
                    "name": "animal_one",
                    "morning_production": "30",
                    "afternoon_production": "40",
                    "evening_production": "40",
                    "production_date": "2023-07-17T20:00",
                },
            },
        )

        assert res.status_code == 200

        assert res.json["data"]["update_production_record"] == True

    def test_delete_production_record(self, client):
        token = get_token()

        id = get_id("production_record")

        res = client.post(
            "/graphql/",
            headers={"Authorization": f"Bearer {token}"},
            json={
                "query": delete_production_record,
                "variables": {"id": id},
            },
        )

        assert res.status_code == 200

        assert res.json["data"]["delete_production_record"] == True

    def test_create_payment_record(self, client):
        token = get_token()

        res = client.post(
            "/graphql/",
            headers={"Authorization": f"Bearer {token}"},
            json={
                "query": create_payment_record,
                "variables": {
                    "name": "customer_one",
                    "amount": "500",
                    "payment_method": "Mpesa",
                    "quantity": "30",
                    "payment_date": "2023-07-17T20:00",
                },
            },
        )

        assert res.status_code == 200

        assert res.json["data"]["create_payment_record"] == True

    def test_get_all_payment_records(self, client):
        token = get_token()

        res = client.post(
            "/graphql/",
            headers={"Authorization": f"Bearer {token}"},
            json={"query": all_payment_records},
        )

        assert res.status_code == 200

        assert res.json["data"]["get_all_payment_records"][0]["_id"] is not None
        assert res.json["data"]["get_all_payment_records"][0]["name"] == "customer_one"
        assert res.json["data"]["get_all_payment_records"][0]["amount"] == 500.0
        assert (
            res.json["data"]["get_all_payment_records"][0]["payment_method"] == "Mpesa"
        )
        assert res.json["data"]["get_all_payment_records"][0]["quantity"] == 30.0
        assert (
            res.json["data"]["get_all_payment_records"][0]["payment_date"] is not None
        )

        set_id(
            "payment_record",
            res.json["data"]["get_all_payment_records"][0]["_id"],
        )

    def test_update_payment_record(self, client):
        token = get_token()

        id = get_id("payment_record")

        res = client.post(
            "/graphql/",
            headers={"Authorization": f"Bearer {token}"},
            json={
                "query": update_payment_record,
                "variables": {
                    "id": id,
                    "name": "animal_one",
                    "amount": "1000",
                    "payment_method": "Cash",
                    "quantity": "40",
                    "payment_date": "2023-07-17T20:00",
                },
            },
        )

        assert res.status_code == 200

        assert res.json["data"]["update_payment_record"] == True

    def test_delete_payment_record(self, client):
        token = get_token()

        id = get_id("payment_record")

        res = client.post(
            "/graphql/",
            headers={"Authorization": f"Bearer {token}"},
            json={
                "query": delete_payment_record,
                "variables": {"id": id},
            },
        )

        assert res.status_code == 200

        assert res.json["data"]["delete_payment_record"] == True

    def test_create_customer_record(self, client):
        token = get_token()

        res = client.post(
            "/graphql/",
            headers={"Authorization": f"Bearer {token}"},
            json={
                "query": create_customer_record,
                "variables": {
                    "name": "customer_one",
                    "priority": "High",
                    "phone": "0712345678",
                    "trip": "Morning",
                    "package": "30",
                },
            },
        )

        assert res.status_code == 200

        assert res.json["data"]["create_customer_record"] == True

    def test_get_all_customer_records(self, client):
        token = get_token()

        res = client.post(
            "/graphql/",
            headers={"Authorization": f"Bearer {token}"},
            json={"query": all_customer_records},
        )

        assert res.status_code == 200

        assert res.json["data"]["get_all_customer_records"][0]["_id"] is not None
        assert res.json["data"]["get_all_customer_records"][0]["name"] == "customer_one"
        assert res.json["data"]["get_all_customer_records"][0]["priority"] == "High"
        assert res.json["data"]["get_all_customer_records"][0]["phone"] == "0712345678"
        assert res.json["data"]["get_all_customer_records"][0]["trip"] == "Morning"
        assert res.json["data"]["get_all_customer_records"][0]["package"] == 30.0

        set_id(
            "customer_record",
            res.json["data"]["get_all_customer_records"][0]["_id"],
        )

    def test_update_customer_record(self, client):
        token = get_token()

        id = get_id("customer_record")

        res = client.post(
            "/graphql/",
            headers={"Authorization": f"Bearer {token}"},
            json={
                "query": update_customer_record,
                "variables": {
                    "id": id,
                    "name": "customer_one",
                    "priority": "Mid",
                    "phone": "+254712345678",
                    "trip": "Evening",
                    "package": "35",
                },
            },
        )

        assert res.status_code == 200

        assert res.json["data"]["update_customer_record"] == True

    def test_delete_customer_record(self, client):
        token = get_token()

        id = get_id("customer_record")

        res = client.post(
            "/graphql/",
            headers={"Authorization": f"Bearer {token}"},
            json={
                "query": delete_customer_record,
                "variables": {"id": id},
            },
        )

        assert res.status_code == 200

        assert res.json["data"]["delete_customer_record"] == True

    def test_create_expense_record(self, client):
        token = get_token()

        res = client.post(
            "/graphql/",
            headers={"Authorization": f"Bearer {token}"},
            json={
                "query": create_expense_record,
                "variables": {
                    "item": "animal_feed",
                    "category": "Utility Expense",
                    "amount": "1500",
                    "date_of_action": "2023-07-17T20:00",
                },
            },
        )

        assert res.status_code == 200

        assert res.json["data"]["create_expense_record"] == True

    def test_get_all_expense_records(self, client):
        token = get_token()

        res = client.post(
            "/graphql/",
            headers={"Authorization": f"Bearer {token}"},
            json={"query": all_expense_records},
        )

        assert res.status_code == 200

        assert res.json["data"]["get_all_expense_records"][0]["_id"] is not None
        assert res.json["data"]["get_all_expense_records"][0]["item"] == "animal_feed"
        assert (
            res.json["data"]["get_all_expense_records"][0]["category"]
            == "Utility Expense"
        )
        assert res.json["data"]["get_all_expense_records"][0]["amount"] == 1500.0
        assert (
            res.json["data"]["get_all_expense_records"][0]["date_of_action"] is not None
        )

        set_id(
            "expense_record",
            res.json["data"]["get_all_expense_records"][0]["_id"],
        )

    def test_update_expense_record(self, client):
        token = get_token()

        id = get_id("expense_record")

        res = client.post(
            "/graphql/",
            headers={"Authorization": f"Bearer {token}"},
            json={
                "query": update_expense_record,
                "variables": {
                    "id": id,
                    "item": "animal_feed",
                    "category": "Utility Expense",
                    "amount": "2000",
                    "date_of_action": "2023-07-17T20:00",
                },
            },
        )

        assert res.status_code == 200

        assert res.json["data"]["update_expense_record"] == True

    def test_delete_expense_record(self, client):
        token = get_token()

        id = get_id("expense_record")

        res = client.post(
            "/graphql/",
            headers={"Authorization": f"Bearer {token}"},
            json={
                "query": delete_expense_record,
                "variables": {"id": id},
            },
        )

        assert res.status_code == 200

        assert res.json["data"]["delete_expense_record"] == True


class TestMisc:
    @pytest.fixture()
    def app(self):
        flask_app.config.update(
            {
                "TESTING": True,
            }
        )

        # setup

        yield flask_app

        # cleanup / reset

    @pytest.fixture()
    def client(self, app):
        return app.test_client()
