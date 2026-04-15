import requests 
from dotenv import load_dotenv
import os
import base64


load_dotenv()
def get_token():
    client_id = os.getenv("id")
    client_secret = os.getenv("client_secret")

    auth_str = f"{client_id}:{client_secret}"
    auth_bytes = auth_str.encode("utf-8")
    auth_base64 = base64.b64encode(auth_bytes).decode("utf-8")

    url = "https://accounts.spotify.com/api/token"

    headers = {
        "Authorization": f"Basic {auth_base64}",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {
        "grant_type": "client_credentials"
    }

    response = requests.post(url,headers=headers,data=data)
    if response.status_code != 200:
        raise Exception(f"Erro na autenticação: {response.text}")
    
    token = response.json()["access_token"]
    return token