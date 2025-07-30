from datetime import datetime

from flask import Flask, jsonify, request

from .config import Config
from .models import Client, ClientParking, Parking, db


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)

    @app.route("/")
    def index():
        return "Parking API is running!"

    @app.route("/clients", methods=["GET"])
    def get_clients():
        clients = Client.query.all()
        return jsonify(
            [
                {
                    "id": c.id,
                    "name": c.name,
                    "surname": c.surname,
                    "credit_card": c.credit_card,
                    "car_number": c.car_number,
                }
                for c in clients
            ]
        )

    @app.route("/clients/<int:client_id>", methods=["GET"])
    def get_client(client_id):
        client = Client.query.get_or_404(client_id)
        return jsonify(
            {
                "id": client.id,
                "name": client.name,
                "surname": client.surname,
                "credit_card": client.credit_card,
                "car_number": client.car_number,
            }
        )

    @app.route("/clients", methods=["POST"])
    def create_client():
        data = request.json
        client = Client(
            name=data["name"],
            surname=data["surname"],
            credit_card=data.get("credit_card"),
            car_number=data.get("car_number"),
        )
        db.session.add(client)
        db.session.commit()
        return jsonify({"id": client.id}), 201

    @app.route("/parkings", methods=["POST"])
    def create_parking():
        data = request.json
        parking = Parking(
            address=data["address"],
            opened=data.get("opened", True),
            count_places=data["count_places"],
            count_available_places=data["count_places"],
        )
        db.session.add(parking)
        db.session.commit()
        return jsonify({"id": parking.id}), 201

    @app.route("/client_parkings", methods=["POST"])
    def enter_parking():
        data = request.json
        client_id = data["client_id"]
        parking_id = data["parking_id"]

        parking = Parking.query.get_or_404(parking_id)

        if not parking.opened:
            return jsonify({"error": "Парковка закрыта"}), 400
        if parking.count_available_places < 1:
            return jsonify({"error": "Нет свободных мест"}), 400

        existing = ClientParking.query.filter_by(
            client_id=client_id, parking_id=parking_id, time_out=None
        ).first()
        if existing:
            return jsonify({"error": "Клиент уже на парковке"}), 400

        parking.count_available_places -= 1
        entry = ClientParking(
            client_id=client_id, parking_id=parking_id, time_in=datetime.utcnow()
        )
        db.session.add(entry)
        db.session.commit()
        return jsonify({"message": "Въезд разрешён", "entry_id": entry.id})

    @app.route("/client_parkings", methods=["DELETE"])
    def exit_parking():
        data = request.json
        client_id = data["client_id"]
        parking_id = data["parking_id"]

        client = Client.query.get_or_404(client_id)
        parking = Parking.query.get_or_404(parking_id)

        if not client.credit_card:
            return jsonify({"error": "У клиента нет привязанной карты"}), 400

        entry = ClientParking.query.filter_by(
            client_id=client_id, parking_id=parking_id, time_out=None
        ).first()
        if not entry:
            return jsonify({"error": "Нет активной парковки для этого клиента"}), 400

        entry.time_out = datetime.utcnow()
        parking.count_available_places += 1

        db.session.commit()
        return jsonify(
            {"message": "Выезд разрешён", "time_out": entry.time_out.isoformat()}
        )

    return app
