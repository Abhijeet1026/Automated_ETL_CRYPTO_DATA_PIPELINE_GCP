import pyspark
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, to_timestamp, current_timestamp
from google.cloud import storage

# Initialize Spark session
spark = SparkSession.builder \
    .appName("Dataproc job") \
    .getOrCreate()

# Set BigQuery connector version to avoid conflict

#spark.conf.set("spark.sql.catalog.spark_bigquery", "com.google.cloud.spark.bigquery.v2.Spark32BigQueryTableProvider")
# Set the temporary GCS bucket for Dataproc jobs
# spark.conf.set("spark.hadoop.fs.gs.system.bucket", "dataengineering1-433721_spark_files_uscentral1")

# Define GCS file paths
json_file_path = "gs://dataengineering1-433721_crypto_data_raw/crypto_raw_test"
staging_file_path = "gs://dataengineering1-433721_crypto_data_raw/crypto_raw_staging_test"
processed_file_path = "gs://dataengineering1-433721_crypto_data_raw/processed_files_test"

# Move new files from raw to staging
def move_files_to_staging(source_bucket, source_prefix, staging_prefix):
    client = storage.Client()
    bucket = client.get_bucket(source_bucket)
    
    # List files in the raw directory
    blobs = bucket.list_blobs(prefix=source_prefix)
    
    for blob in blobs:
        # Generate new file name in the staging location
        new_blob_name = staging_prefix + blob.name.split('/')[-1]
        
        # Copy file to the staging location
        bucket.copy_blob(blob, bucket, new_blob_name)
        
        # Delete the original file from the raw folder
        blob.delete()

# Move files to the staging folder
move_files_to_staging('dataengineering1-433721_crypto_data_raw', 'crypto_raw_test/', 'crypto_raw_staging_test/')

# Read the JSON data from the staging folder
df = spark.read.json(f"{staging_file_path}/*")

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
deduplicated_df.printSchema()
deduplicated_df.show(5)

# Define BigQuery parameters
project_id = "dataengineering1-433721"
schema_name = "crypto_de"
table_name = "crypto_data"
table_id = f"{project_id}.{schema_name}.{table_name}"

spark.conf.set("spark.hadoop.fs.gs.system.bucket", "dataengineering1-433721_spark_files_uscentral1")
# Write deduplicated data to BigQuery
deduplicated_df.write \
    .format("bigquery") \
    .option("temporaryGcsBucket","dataengineering1-433721_spark_files_uscentral1") \
    .mode("append") \
    .option("table", table_id) \
    .save()

# Mark processed files by moving them from staging to processed
def mark_files_as_processed(source_bucket, staging_prefix, processed_prefix):
    client = storage.Client()
    bucket = client.get_bucket(source_bucket)
    
    # List files in the staging directory
    blobs = bucket.list_blobs(prefix=staging_prefix)
    
    for blob in blobs:
        # Generate new file name in the processed location
        new_blob_name = processed_prefix + blob.name.split('/')[-1]
        
        # Copy file to the processed location
        bucket.copy_blob(blob, bucket, new_blob_name)
        
        # Delete the original file from the staging folder
        blob.delete()

# Mark files as processed by moving them to the processed folder
mark_files_as_processed('dataengineering1-433721_crypto_data_raw', 'crypto_raw_staging_test/', 'processed_files_test/')

# Stop Spark session
spark.stop()
