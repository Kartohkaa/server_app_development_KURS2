import httpx

BASE_URL = "http://127.0.0.1:8008"
LOGIN = "user123"
PASS = "password123"

def test_auth():
    with httpx.Client() as client:
        print("[1] Вход в систему...")
        response = client.post(
            f"{BASE_URL}/login",
            json={"username": LOGIN, "password": PASS}
        )
        print(f"Логин: {response.status_code}")
        print(f"Ответ: {response.text}")
        
        if response.status_code != 200:
            return
        
        print("\n[2] Сохранённые куки:")
        for key, value in client.cookies.items():
            print(f"{key}: {value}")
        
        print("\n[3] Запрос к /profile...")
        profile = client.get(f"{BASE_URL}/profile")
        print(f"Profile: {profile.status_code}")
        print(f"Ответ: {profile.text}")
        
        print("\n[4] Выход из системы...")
        logout = client.post(f"{BASE_URL}/logout")
        print(f"Logout: {logout.status_code}")
        print(f"Ответ: {logout.text}")
        
        print("\n[5] Запрос к /profile после выхода...")
        after = client.get(f"{BASE_URL}/profile")
        print(f"Profile after logout: {after.status_code}")

if __name__ == "__main__":
    test_auth()