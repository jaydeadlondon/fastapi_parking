# 🚗 Parking API

FastAPI система управления парковкой с JWT аутентификацией и автоматической тарификацией.

## 🚀 Возможности

- JWT аутентификация админов
- Управление парковками и клиентами  
- Автоматический расчёт стоимости парковки
- Swagger документация

## 🛠 Быстрый старт

### 1. Установка
```bash
pip install -r requirements.txt
```

### 2. Создание админа
```bash
python create_admin.py
```

### 3. Запуск
```bash
uvicorn main:app --reload
```

### 4. Документация
- API: `http://localhost:8000/docs`
- Тест: `python test_api_quick.py`

## 🔐 Тестовый админ

- **Username**: `admin`
- **Password**: `admin123`

## 📋 Основные endpoints

- `POST /auth/login/` - Логин и получение JWT
- `POST /parkings/create/` - Создание парковки (защищено)
- `POST /parkings/{id}/enter/` - Въезд на парковку
- `DELETE /parkings/{id}/exit/` - Выезд + расчёт оплаты

## 🎯 Особенности

- Автоматический учёт свободных мест
- Тарификация $2/час, округление до полных часов
- bcrypt хэширование паролей
- Валидация данных через Pydantic

## 🔧 Технологии

FastAPI • SQLAlchemy • JWT • bcrypt • Pydantic
