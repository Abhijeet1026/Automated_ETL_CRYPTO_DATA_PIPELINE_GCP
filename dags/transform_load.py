import pyspark
from pyspark.sql import SparkSession
from pyspark.conf import SparkConf
from pyspark.context import SparkContext
import warnings
from pyspark.sql.functions import col, to_timestamp, current_timestamp
from google.cloud import bigquery

# Ignore all warnings
warnings.filterwarnings("ignore")

# Set your credentials location
credentials_location = '/home/abhi/gcp_keys/keys/my-terra-creds.json'

# Spark configuration
conf = SparkConf() \
    .setMaster('local[*]') \
    .setAppName('test') \
    .set("spark.jars", "/home/abhi/notebooks/lib/gcs-connector-hadoop3-2.2.5.jar, /home/abhi/notebooks/lib/spark-3.2-bigquery-0.29.0-preview.jar") \
    .set("spark.hadoop.google.cloud.auth.service.account.enable", "true") \
    .set("spark.hadoop.google.cloud.auth.service.account.json.keyfile", credentials_location) \
    .set("temporaryGcsBucket", "dataengineering1-433721_crypto_data_raw")

sc = SparkContext(conf=conf)

hadoop_conf = sc._jsc.hadoopConfiguration()

# Set up GCS configurations
hadoop_conf.set("fs.AbstractFileSystem.gs.impl", "com.google.cloud.hadoop.fs.gcs.GoogleHadoopFS")
hadoop_conf.set("fs.gs.impl", "com.google.cloud.hadoop.fs.gcs.GoogleHadoopFileSystem")
hadoop_conf.set("fs.gs.auth.service.account.json.keyfile", credentials_location)
hadoop_conf.set("fs.gs.auth.service.account.enable", "true")

# Initialize Spark session
spark = SparkSession.builder \
    .config(conf=sc.getConf()) \
    .getOrCreate()

# Define GCS file path
json_file_path = "gs://dataengineering1-433721_crypto_data_raw/crypto_raw"

# Read the JSON data
df = spark.read.json(f"{json_file_path}/*")

# Apply transformations and add ingestion timestamp
selected_columns_df = df.select(
    col("id").cast("string"),
    col("symbol").cast("string"),
    col("name").cast("string"),
    col("current_price").cast("float"),
    col("market_cap").cast("float"),
    col("market_cap_rank").cast("integer"),
    col("total_volume").cast("float"),
    col("high_24h").cast("float"),
    col("low_24h").cast("float"),
    col("total_supply").cast("float"),
    col("price_change_percentage_24h").cast("float"),
    col("circulating_supply").cast("float"),
    col("max_supply").cast("float"),
    to_timestamp("last_updated", "yyyy-MM-dd'T'HH:mm:ss.SSS'Z'").alias("last_updated"),
).withColumn("ingestion_timestamp", current_timestamp())

# Deduplicate data based on 'id' and 'last_updated'
deduplicated_df = selected_columns_df.dropDuplicates(["id", "last_updated"])

# Define BigQuery parameters
project_id = "dataengineering1-433721"
schema_name = "crypto_de"
table_name = "crypto_data"
table_id = f"{project_id}.{schema_name}.{table_name}"

# Write deduplicated data to BigQuery
deduplicated_df.write \
    .format("bigquery") \
    .mode("append") \
    .option("table", table_id) \
    .save()

# Stop Spark session
spark.stop()
