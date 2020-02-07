import pytest
from .app import create_app, db


@pytest.fixture(scope="session")
def client():
    test_app = create_app(
        {"SQLALCHEMY_DATABASE_URL": "sqlite:///:memory:", "TESTING": True}
    )
    with test_app.app_context():
        db.create_all()

    with test_app.test_client() as client_:
        yield client_

    with test_app.app_context():
        db.session.close_all()
        db.drop_all()
