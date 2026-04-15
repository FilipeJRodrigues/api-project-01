import urllib.parse
from dotenv import load_dotenv
import os
from flask import Flask, request
import auth
import extract

load_dotenv()

client_id = os.getenv("id")
redirect_uri = "http://127.0.0.1:3000/callback"

# 🔹 URL de login
params = {
    "client_id": client_id,
    "response_type": "code",
    "redirect_uri": redirect_uri,
    "scope": "user-top-read",
}

auth_url = "https://accounts.spotify.com/authorize?" + urllib.parse.urlencode(params)

app = Flask(__name__)

@app.route("/callback")
def callback():
    code = request.args.get("code")

    if not code:
        return "Erro: code não recebido"

    try:
        token = auth.get_access_token_from_code(code)

        dados = extract.get_top_artists(token)

        return dados

    except Exception as e:
        return str(e)


if __name__ == "__main__":
    print("Acesse essa URL no navegador:")
    print(auth_url)
    app.run(port=3000)