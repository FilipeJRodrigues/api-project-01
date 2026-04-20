import urllib.parse
from dotenv import load_dotenv
import os
from flask import Flask, request
import auth
import extract
import spark_processing
from pyspark.sql.functions import current_date

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

        spark = spark_processing.create_spark_session()
        df = spark_processing.json_to_dataframe(spark,dados)
        spark.conf.set("spark.hadoop.io.native.lib.available", "false")
        df = df.withColumn("ingest_date", current_date())

        (df.write 
            .mode("append") 
            .partitionBy("ingest_date") 
            .parquet("C:\\data_lake\\raw\\api_spotify\\tb_raw_spotify_top_artists")
        )
        df2 = spark.read.parquet("C:\\data_lake\\raw\\api_spotify\\tb_raw_spotify_top_artists")
        df2.show()

        return "Dados carregados no spark com sucesso!"

    except Exception as e:
        return str(e)


if __name__ == "__main__":
    print("Acesse essa URL no navegador:")
    print(auth_url)
    app.run(port=3000)