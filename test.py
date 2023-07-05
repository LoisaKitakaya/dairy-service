import pytest
from main import app as flask_app


class TestAppMutations:
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


class TestAppQueries:
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
