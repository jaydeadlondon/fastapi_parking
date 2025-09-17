from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class UserLogin(BaseModel):
    username: str
    password: str
    
class Token(BaseModel):
    access_token: str
    token_type: str = 'bearer'
    
class UserResponse(BaseModel):
    id: int
    username: str
    email: Optional[str] = None
    is_active: bool
    
class UserCreate(BaseModel):
    username: str
    password: str
    email: Optional[str] = None

class ClientCreate(BaseModel):
    name: str
    surname: str
    credit_card: Optional[str] = None
    car_number: Optional[str] = None
    
class ClientResponse(BaseModel):
    id: int
    name: str
    surname: str
    credit_card: Optional[str] = None
    car_number: Optional[str] = None
    
class ParkingCreate(BaseModel):
    address: str
    opened: bool = True
    count_places: int
    
class ParkingResponse(BaseModel):
    id: int
    address: str
    opened: bool
    count_places: int
    count_available_places: int
    price_per_hour: float

class ClientParkingCreate(BaseModel):
    client_id: int
    parking_id: int
    
class ClientParkingResponse(BaseModel):
    id: int
    client_id: int
    parking_id: int
    time_in: datetime
    time_out: Optional[datetime] = None
    total_cost: Optional[float] = None
