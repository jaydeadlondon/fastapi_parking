#!/usr/bin/env python3
"""
Быстрый тест API
"""

import requests
import json

BASE_URL = "http://localhost:8000"

def test_api():
    print("🚀 Тестирование API...")
    
    # 1. Проверка основной страницы
    print("\n1. Проверка основной страницы:")
    try:
        response = requests.get(f"{BASE_URL}/")
        print(f"✅ Статус: {response.status_code}")
        print(f"✅ Ответ: {response.json()}")
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        return
    
    # 2. Логин админа
    print("\n2. Логин админа:")
    try:
        login_data = {
            "username": "admin",
            "password": "admin123"
        }
        response = requests.post(f"{BASE_URL}/auth/login/", json=login_data)
        print(f"✅ Статус: {response.status_code}")
        
        if response.status_code == 200:
            token_data = response.json()
            access_token = token_data["access_token"]
            print(f"✅ Токен получен: {access_token[:20]}...")
            
            # Заголовок для авторизации
            headers = {"Authorization": f"Bearer {access_token}"}
            
            # 3. Проверка /auth/me
            print("\n3. Проверка профиля:")
            response = requests.get(f"{BASE_URL}/auth/me/", headers=headers)
            print(f"✅ Статус: {response.status_code}")
            if response.status_code == 200:
                print(f"✅ Профиль: {response.json()}")
            
            # 4. Создание парковки
            print("\n4. Создание парковки:")
            parking_data = {
                "address": "Тестовая улица, 1",
                "opened": True,
                "count_places": 10
            }
            response = requests.post(f"{BASE_URL}/parkings/create/", json=parking_data, headers=headers)
            print(f"✅ Статус: {response.status_code}")
            if response.status_code == 200:
                parking = response.json()
                print(f"✅ Парковка создана: {parking}")
                
                # 5. Получение списка парковок
                print("\n5. Список парковок:")
                response = requests.get(f"{BASE_URL}/parkings/", headers=headers)
                print(f"✅ Статус: {response.status_code}")
                if response.status_code == 200:
                    parkings = response.json()
                    print(f"✅ Найдено парковок: {len(parkings)}")
            
        else:
            print(f"❌ Ошибка логина: {response.json()}")
            
    except Exception as e:
        print(f"❌ Ошибка: {e}")

    print("\n🎉 Тестирование завершено!")

if __name__ == "__main__":
    test_api()
