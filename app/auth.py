from passlib.context import CryptContext
import datetime
from .config import Settings
from jose import jwt, JWTError
from .models import User
from sqlalchemy.orm import Session

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def username_exists(username: str, db: Session) -> bool:
    return db.query(User).filter(User.username == username).first() is not None

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(password: str, hashed_password: str) -> bool:
    return pwd_context.verify(password, hashed_password)

def create_token(username: str) -> str:
    return jwt.encode(
        {
            "sub": username,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
        },
        Settings.SECRET_KEY,
        algorithm="HS256"
    )
    
def verify_token(token: str) -> str:
    try: 
        payload = jwt.decode(token, Settings.SECRET_KEY, algorithms=["HS256"])
        return payload["sub"]
    except JWTError:
        return None