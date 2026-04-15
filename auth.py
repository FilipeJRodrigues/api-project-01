import requests
import os
import base64
from dotenv import load_dotenv

load_dotenv()

client_id = os.getenv("id")
client_secret = os.getenv("client_secret")
redirect_uri = "http://127.0.0.1:3000/callback"

def get_access_token_from_code(code):
    auth_str = f"{client_id}:{client_secret}"
    auth_base64 = base64.b64encode(auth_str.encode()).decode()

    url = "https://accounts.spotify.com/api/token"

    headers = {
        "Authorization": f"Basic {auth_base64}",
        "Content-Type": "application/x-www-form-urlencoded"
    }

    data = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": redirect_uri
    }

    response = requests.post(url, headers=headers, data=data)

    if response.status_code != 200:
        raise Exception(f"Erro ao gerar token: {response.text}")

    return response.json()["access_token"]