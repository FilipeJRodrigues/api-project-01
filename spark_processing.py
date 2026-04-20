from dotenv import load_dotenv
import os

load_dotenv()

python_path = os.getenv("PYTHON_PATH")

os.environ["PYSPARK_PYTHON"] = python_path
os.environ["PYSPARK_DRIVER_PYTHON"] = python_path

from pyspark.sql import SparkSession


def create_spark_session():
    spark = (SparkSession.builder
             .appName("SpotifyData")
             .config("spark.hadoop.io.native.lib.available", "false")
             .config("spark.hadoop.fs.file.impl", "org.apache.hadoop.fs.LocalFileSystem")
             .config("spark.hadoop.fs.file.impl.disable.cache", "true")
             .getOrCreate()
    )
    return spark

def json_to_dataframe(spark,data):
    df= spark.createDataFrame(data["items"])
    return df