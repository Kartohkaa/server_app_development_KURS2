import httpx
import time

BASE_URL = "http://127.0.0.1:8009"
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
        
        print("\n[2] Запрос к /profile сразу...")
        profile = client.get(f"{BASE_URL}/profile")
        print(f"Profile: {profile.status_code}")
        
        print("\n[3] Ждем 2 минуты...")
        time.sleep(120)
        
        print("\n[4] Запрос к /profile через 2 минуты...")
        profile = client.get(f"{BASE_URL}/profile")
        print(f"Profile: {profile.status_code}")
        
        print("\n[5] Ждем еще 2 минуты...")
        time.sleep(120)
        
        print("\n[6] Запрос к /profile через 4 минуты...")
        profile = client.get(f"{BASE_URL}/profile")
        print(f"Profile: {profile.status_code}")
        
        print("\n[7] Ждем еще 3 минуты...")
        time.sleep(180)
        
        print("\n[8] Запрос к /profile через 7 минут...")
        profile = client.get(f"{BASE_URL}/profile")
        print(f"Profile: {profile.status_code}")

if __name__ == "__main__":
    test_auth()