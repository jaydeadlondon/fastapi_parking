from datetime import datetime

import pytest
from module_30_ci_linters.homework.hw1.fastapi_parking.app import create_app
from module_30_ci_linters.homework.hw1.fastapi_parking.app.models import (
    Client, ClientParking, Parking)
from module_30_ci_linters.homework.hw1.fastapi_parking.app.models import \
    db as _db


@pytest.fixture
def app():
    app = create_app()
    app.config.update(
        {
            "TESTING": True,
            "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
            "SQLALCHEMY_TRACK_MODIFICATIONS": False,
        }
    )
    with app.app_context():
        _db.create_all()
        client = Client(
            name="Test",
            surname="User",
            credit_card="1111-2222-3333-4444",
            car_number="A000AA00",
        )
        _db.session.add(client)
        parking = Parking(
            address="Test St, 1", opened=True, count_places=5, count_available_places=5
        )
        _db.session.add(parking)
        _db.session.commit()
        log = ClientParking(
            client_id=client.id,
            parking_id=parking.id,
            time_in=datetime.utcnow(),
            time_out=datetime.utcnow(),
        )
        _db.session.add(log)
        _db.session.commit()
    yield app


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def db(app):
    return _db
