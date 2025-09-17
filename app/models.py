from sqlalchemy import Column, Float, Integer, String, Boolean, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True)
    username = Column(String(50), nullable=False, unique=True)
    hashed_password = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)
    email = Column(String(255), nullable=True, unique=True)

    def __repr__(self):
        return f"<User {self.username}>"


class Client(Base):
    __tablename__ = "client"
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    surname = Column(String(50), nullable=False)
    credit_card = Column(String(50))
    car_number = Column(String(10))

    def __repr__(self):
        return f"<Client {self.name} {self.surname}>"


class Parking(Base):
    __tablename__ = "parking"
    id = Column(Integer, primary_key=True)
    address = Column(String(100), nullable=False)
    opened = Column(Boolean)
    count_places = Column(Integer, nullable=False)
    count_available_places = Column(Integer, nullable=False)
    price_per_hour = Column(Float, nullable=False, default = 2.0)

    def __repr__(self):
        return f"<Parking {self.address}>"


class ClientParking(Base):
    __tablename__ = "client_parking"
    id = Column(Integer, primary_key=True)
    client_id = Column(Integer, ForeignKey("client.id"))
    parking_id = Column(Integer, ForeignKey("parking.id"))
    time_in = Column(DateTime)
    time_out = Column(DateTime)
    total_cost = Column(Float)
    
    client = relationship("Client", backref="client_parkings")
    parking = relationship("Parking", backref="client_parkings")

    __table_args__ = (
        UniqueConstraint("client_id", "parking_id", name="unique_client_parking"),
    )

    def __repr__(self):
        return f"<ClientParking client={self.client_id} parking={self.parking_id}>"
