import os 

class Settings:
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite:///instance/parking.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    PROJECT_NAME = "Parking API"
    VERSION = "2.0.0"
    SECRET_KEY = os.getenv("SECRET_KEY", "fastapi-parking-secret-key")
