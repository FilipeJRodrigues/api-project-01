import requests

def get_top_artists(token):
    url = "https://api.spotify.com/v1/me/top/artists"

    headers = {
        "Authorization": f"Bearer {token}"
    }

    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        raise Exception(f"Erro ao buscar dados: {response.text}")

    return response.json()