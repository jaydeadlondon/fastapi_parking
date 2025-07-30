import pytest

from factories import ClientFactory, ParkingFactory


@pytest.mark.parametrize("url", ["/clients", "/clients/1"])
def test_get_methods(client, url):
    response = client.get(url)
    assert response.status_code == 200


def test_create_client(client):
    data = {
        "name": "Иван",
        "surname": "Иванов",
        "credit_card": "1234-5678-9012-3456",
        "car_number": "A123BC77",
    }
    response = client.post("/clients", json=data)
    assert response.status_code == 201
    assert "id" in response.get_json()


def test_create_parking(client):
    data = {"address": "ул. Пушкина, д. 1", "opened": True, "count_places": 10}
    response = client.post("/parkings", json=data)
    assert response.status_code == 201
    assert "id" in response.get_json()


@pytest.mark.parking
def test_enter_parking(client, db):
    client_data = {
        "name": "Петр",
        "surname": "Петров",
        "credit_card": "5555-6666-7777-8888",
        "car_number": "B123BC77",
    }
    client_resp = client.post("/clients", json=client_data)
    client_id = client_resp.get_json()["id"]

    parking_data = {"address": "ул. Ленина, д. 2", "opened": True, "count_places": 2}
    parking_resp = client.post("/parkings", json=parking_data)
    parking_id = parking_resp.get_json()["id"]

    response = client.post(
        "/client_parkings", json={"client_id": client_id, "parking_id": parking_id}
    )
    assert response.status_code == 200
    assert "entry_id" in response.get_json()

    from app.models import Parking

    parking = Parking.query.get(parking_id)
    assert parking.count_available_places == 1


@pytest.mark.parking
def test_exit_parking(client, db):
    client_data = {
        "name": "Сидор",
        "surname": "Сидоров",
        "credit_card": "9999-8888-7777-6666",
        "car_number": "C123BC77",
    }
    client_resp = client.post("/clients", json=client_data)
    client_id = client_resp.get_json()["id"]

    parking_data = {"address": "ул. Гагарина, д. 3", "opened": True, "count_places": 1}
    parking_resp = client.post("/parkings", json=parking_data)
    parking_id = parking_resp.get_json()["id"]

    client.post(
        "/client_parkings", json={"client_id": client_id, "parking_id": parking_id}
    )

    response = client.delete(
        "/client_parkings", json={"client_id": client_id, "parking_id": parking_id}
    )
    assert response.status_code == 200
    data = response.get_json()
    assert "time_out" in data

    from app.models import Parking

    parking = Parking.query.get(parking_id)
    assert parking.count_available_places == 1

    from app.models import ClientParking

    log = ClientParking.query.filter_by(
        client_id=client_id, parking_id=parking_id
    ).first()
    assert log.time_out >= log.time_in


def test_enter_parking_no_places(client, db):
    client_data = {
        "name": "НетМест",
        "surname": "НетМестов",
        "credit_card": "0000-0000-0000-0000",
        "car_number": "Z000ZZ00",
    }
    client_resp = client.post("/clients", json=client_data)
    client_id = client_resp.get_json()["id"]

    parking_data = {"address": "ул. НетМест, д. 0", "opened": True, "count_places": 0}
    parking_resp = client.post("/parkings", json=parking_data)
    parking_id = parking_resp.get_json()["id"]

    response = client.post(
        "/client_parkings", json={"client_id": client_id, "parking_id": parking_id}
    )
    assert response.status_code == 400
    assert "Нет свободных мест" in response.get_json()["error"]


def test_exit_parking_no_card(client, db):
    client_data = {"name": "БезКарты", "surname": "БезКартов", "car_number": "X000XX00"}
    client_resp = client.post("/clients", json=client_data)
    client_id = client_resp.get_json()["id"]

    parking_data = {"address": "ул. БезКарты, д. 1", "opened": True, "count_places": 1}
    parking_resp = client.post("/parkings", json=parking_data)
    parking_id = parking_resp.get_json()["id"]

    client.post(
        "/client_parkings", json={"client_id": client_id, "parking_id": parking_id}
    )

    response = client.delete(
        "/client_parkings", json={"client_id": client_id, "parking_id": parking_id}
    )
    assert response.status_code == 400
    assert "нет привязанной карты" in response.get_json()["error"].lower()


def test_create_client_factory(client, db):
    client_obj = ClientFactory()
    data = {
        "name": client_obj.name,
        "surname": client_obj.surname,
        "credit_card": client_obj.credit_card,
        "car_number": client_obj.car_number,
    }
    response = client.post("/clients", json=data)
    assert response.status_code == 201
    assert "id" in response.get_json()

    from app.models import Client

    assert (
        db.session.query(Client)
        .filter_by(name=client_obj.name, surname=client_obj.surname)
        .count()
        == 1
    )


def test_create_parking_factory(client, db):
    parking_obj = ParkingFactory()
    data = {
        "address": parking_obj.address,
        "opened": parking_obj.opened,
        "count_places": parking_obj.count_places,
    }
    response = client.post("/parkings", json=data)
    assert response.status_code == 201
    assert "id" in response.get_json()

    from app.models import Parking

    assert db.session.query(Parking).filter_by(address=parking_obj.address).count() == 1
