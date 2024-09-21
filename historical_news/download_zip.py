from pyspark.sql import SparkSession
import os
import requests
from pyspark.sql.functions import col

# Initialize Spark Session for Structured Streaming
spark = SparkSession.builder \
    .appName("GDELT Zip Downloader Streaming") \
    .config("spark.executor.memory", "4g") \
    .config("spark.sql.shuffle.partitions", "10") \
    .getOrCreate()

# Directory to save downloaded files
download_dir = "/home/student/project_files/zippedfiles"
os.makedirs(download_dir, exist_ok=True)

# Function to download a zip file given a URL
def download_zip(url, save_path):
    try:
        response = requests.get(url, stream=True)
        with open(save_path, 'wb') as file:
            file.write(response.content)
        print(f"Downloaded: {url}")
    except Exception as e:
        print(f"Error downloading {url}: {e}")

# Function to download the file (used in the foreachBatch)
def download_files_from_df(df, epoch_id):
    urls = df.select("url").collect()  # Collect all URLs in the current batch
    for row in urls:
        url = row['url']
        zip_file_name = os.path.join(download_dir, os.path.basename(url))
        download_zip(url, zip_file_name)

# Define the streaming source (assuming streaming data comes from the directory)
urls_output_path = "/home/student/project_files/urls_output"

# Read the streaming text data from the directory
df_stream = spark.readStream \
    .format("text") \
    .option("path", urls_output_path) \
    .option("maxFilesPerTrigger", 1) \
    .load()

# Rename the column to "url" for easier access
df_stream = df_stream.withColumnRenamed("value", "url")

# Process the streaming data and download the files as they come in
query = df_stream.writeStream \
    .foreachBatch(download_files_from_df) \
    .outputMode("append") \
    .start()

# Wait for the termination of the stream (keeps it running)
query.awaitTermination()

