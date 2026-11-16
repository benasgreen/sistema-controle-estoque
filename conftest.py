import pytest
from app import create_app
from app.extensions import db
from app.models import User

@pytest.fixture()
def app():
    app = create_app({"TESTING": True, "SECRET_KEY": "test-secret", "SQLALCHEMY_DATABASE_URI": "sqlite://"})
    with app.app_context():
        db.drop_all()
        db.create_all()
        user = User(username="admin")
        user.set_password("admin123")
        db.session.add(user)
        db.session.commit()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture()
def client(app):
    return app.test_client()

@pytest.fixture()
def logged_client(client):
    client.post("/login", data={"username": "admin", "password": "admin123"})
    return client
