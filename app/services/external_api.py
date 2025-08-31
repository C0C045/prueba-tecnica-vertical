import requests

BASE_URL = "https://jsonplaceholder.typicode.com"

def get_posts():
    try:
        response = requests.get(f"{BASE_URL}/posts", timeout=5)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}
