import httpx

BASE_URL = "http://127.0.0.1:8007"
LOGIN = "user123"
PASS = "password123"

def proverka_auth():
    with httpx.Client() as client:
        
        print("\n[1] Пытаемся войти в систему...")
        
        dlya_vhoda = {
            "username": LOGIN,
            "password": PASS
        }
        
        otvet = client.post(
            f"{BASE_URL}/login",
            json=dlya_vhoda
        )
        
        print(f"Код ответа: {otvet.status_code}")
        print(f"Сообщение сервера: {otvet.text}")
        
        if otvet.status_code != 200:
            print("\n Не удалось войти. Проверьте данные.")
            return
        
        print("\n[2] Сохранённые куки:")
        for key, value in client.cookies.items():
            print(f"  {key} = {value}")
        
        print("\n[3] Запрашиваем защищённую страницу...")
        user_data = client.get(f"{BASE_URL}/user")
        
        print(f"Код ответа: {user_data.status_code}")
        print(f"Данные пользователя: {user_data.text}")
        
        if user_data.status_code == 200:
            print("\n Успех! Аутентификация работает корректно.")
        else:
            print("\n Ошибка доступа к защищённому ресурсу.")
        
        print("\n[4] Проверяем выход из системы...")
        logout = client.post(f"{BASE_URL}/logout")
        print(f"Код ответа: {logout.status_code}")
        print(f"Сообщение: {logout.text}")
        
        print("\n[5] Пробуем зайти после выхода...")
        posle_vihoda = client.get(f"{BASE_URL}/user")
        print(f"Код ответа: {posle_vihoda.status_code}")
        
        if posle_vihoda.status_code == 401:
            print("Сессия завершена, доступ закрыт.")

if __name__ == "__main__":
    proverka_auth()