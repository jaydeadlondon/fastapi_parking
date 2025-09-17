#!/usr/bin/env python3
"""
Скрипт для создания тестового админа
"""

from app.models import User, Base
from app.routes import engine, SessionLocal
from app.auth import hash_password

def create_admin():
    # Создаём таблицы если их нет
    Base.metadata.create_all(engine)
    
    # Создаём сессию
    db = SessionLocal()
    
    try:
        # Проверяем существует ли админ
        existing_admin = db.query(User).filter(User.username == "admin").first()
        if existing_admin:
            print("❌ Админ 'admin' уже существует!")
            return
        
        # Создаём админа
        admin = User(
            username="admin",
            hashed_password=hash_password("admin123"),
            email="admin@parking.com",
            is_active=True
        )
        
        db.add(admin)
        db.commit()
        
        print("✅ Тестовый админ создан!")
        print("👤 Username: admin")
        print("🔑 Password: admin123")
        print("📧 Email: admin@parking.com")
        
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    create_admin()
