from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import HTTPBearer
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from .schemas import ClientCreate, ClientResponse, ParkingCreate, ParkingResponse, ClientParkingCreate, ClientParkingResponse, Token, UserLogin, UserResponse, UserCreate
from .models import Client, Parking, ClientParking, User
from .config import Settings
from typing import List
from datetime import datetime
import math
from .auth import hash_password, create_token, verify_password, verify_token, username_exists


app = FastAPI(title="Parking API", version="2.0.0")

engine = create_engine(Settings.SQLALCHEMY_DATABASE_URI)
security = HTTPBearer()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_current_user(token: str = Depends(security), db: Session = Depends(get_db)):
    username = verify_token(token.credentials)
    if not username:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    
    return user


@app.get("/")
def read_root():
    return {"message": "Parking API v2.0 is running!"}


@app.post("/clients/create/", response_model=ClientResponse)
def create_client(client: ClientCreate, db: Session = (Depends(get_db))):
    db_client = Client(name=client.name, surname=client.surname, credit_card=client.credit_card, car_number=client.car_number)
    db.add(db_client)
    db.commit()
    db.refresh(db_client)
    return db_client


@app.post("/parkings/create/", response_model=ParkingResponse)
def create_parking(parking: ParkingCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    db_parking = Parking(address=parking.address, opened=parking.opened, count_places=parking.count_places, count_available_places=parking.count_places)
    db.add(db_parking)
    db.commit()
    db.refresh(db_parking)
    return db_parking


@app.get("/clients/", response_model=List[ClientResponse])
def get_clients(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    db_clients = db.query(Client).all()
    return db_clients


@app.get("/parkings/", response_model=List[ParkingResponse])
def get_parkings(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    db_parkings = db.query(Parking).all()
    return db_parkings


@app.post("/parkings/{id}/enter/", response_model=ClientParkingResponse)
def enter_parking(data: ClientParkingCreate, db: Session = Depends(get_db)):
    db_client_parking = ClientParking(client_id = data.client_id, parking_id = data.parking_id, time_in = datetime.now())
    parking = db.query(Parking).filter(Parking.id == data.parking_id).first()
    if parking.count_available_places > 0:
        parking.count_available_places -= 1
    else:
        raise HTTPException(status_code=400, detail="Parking is full")
    db.add(db_client_parking)
    db.commit()
    db.refresh(db_client_parking)
    return db_client_parking


@app.delete("/parkings/{id}/exit/", response_model=ClientParkingResponse)
def exit_parking(data: ClientParkingCreate, db: Session = Depends(get_db)):
    active = db.query(ClientParking).filter(
        ClientParking.client_id == data.client_id,
        ClientParking.parking_id == data.parking_id, 
        ClientParking.time_out == None
).first()
    
    active.time_out = datetime.now()
    parking = db.query(Parking).filter(Parking.id == data.parking_id).first()
    
    duration = (active.time_out - active.time_in).total_seconds() / 3600
    hours_rounded = math.ceil(duration) 
    active.total_cost = hours_rounded * parking.price_per_hour
    
    parking.count_available_places += 1
    db.add(parking)
    db.commit()
    db.refresh(parking)
    return active


@app.post("/auth/login/", response_model=Token)
def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.username == user.username).first()
    if not db_user:
        raise HTTPException(status_code=401, detail="Invalid username or password")
    
    if not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid username or password")
    
    return Token(access_token=create_token(db_user.username))
    
    
@app.post("/auth/register/", response_model=UserResponse)
def register(user: UserCreate, db: Session = Depends(get_db)):
    if username_exists(user.username, db):
        raise HTTPException(status_code=400, detail="Username already exists")
    
    db_user = User(username=user.username, hashed_password=hash_password(user.password), email=user.email)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


@app.get("/auth/me/", response_model=UserResponse)
def me(current_user: User = Depends(get_current_user)):
    return current_user