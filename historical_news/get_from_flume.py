from pyspark import SparkConf, SparkContext
from pyspark.sql import SparkSession, Row
import os
import re
import schedule
import time
from pyspark.sql.functions import udf, col
from pyspark.sql.types import StringType

# Function to get the size of the data in HDFS
def get_data_size(hdfs_path):
    fs = sc._jvm.org.apache.hadoop.fs.FileSystem.get(sc._jsc.hadoopConfiguration())
    path = sc._jvm.org.apache.hadoop.fs.Path(hdfs_path)
    return fs.getContentSummary(path).getLength()

# Function to dynamically adjust partition size based on the dataset size
def get_optimal_partitions(data_size):
    if data_size < 500 * 1024 * 1024:  # Less than 500MB
        return 10
    elif data_size < 1 * 1024 * 1024 * 1024:  # Less than 1GB
        return 50
    else:
        return 100

# HDFS path where the data is located
hdfs_path = "hdfs://localhost:9000/user/khalid/flume/gdelt_flume/"

# Initialize or get the existing Spark Session and Spark Context
conf = SparkConf() \
    .setAppName("GDELT Processing") \
    .set("spark.executor.memory", "4g") \
    .set("spark.dynamicAllocation.enabled", "true") \
    .set("spark.dynamicAllocation.minExecutors", "2") \
    .set("spark.dynamicAllocation.maxExecutors", "50") \
    .set("spark.executor.cores", "2") \
    .set("spark.sql.adaptive.enabled", "true") \
    .set("spark.sql.adaptive.advisoryPartitionSizeInBytes", "64MB") \
    .set("spark.executor.heartbeatInterval", "60s") \
    .set("spark.sql.shuffle.partitions", "200") \
    .set("spark.rpc.message.maxSize", "1024")  # Increase max size for Spark RPC communication
 
# Create the SparkContext and SparkSession
sc = SparkContext.getOrCreate(conf=conf)
spark = SparkSession.builder \
    .config("spark.executor.memoryOverhead", "512m") \
    .getOrCreate()

# Get an estimate of the size of data in HDFS
data_size = get_data_size(hdfs_path)
optimal_partitions = get_optimal_partitions(data_size)

# Adjust the number of shuffle partitions based on data size
spark.conf.set("spark.sql.shuffle.partitions", str(optimal_partitions))

# Define a function for processing GKG files and saving URLs
def process_and_save_gkg_files():
    try:
        # Get list of all GKG files from HDFS with appropriate partitioning
        gkg_files_rdd = sc.textFile(hdfs_path + "*", minPartitions=optimal_partitions)

        # Filter for GKG files (those ending in .gkg.csv.zip)
        gkg_files = gkg_files_rdd.filter(lambda x: ".gkg.csv.zip" in x).collect()

        # Convert the data into a list of Rows
        rows = [Row(line=line) for line in gkg_files]

        # Create DataFrame
        df = spark.createDataFrame(rows)

        # Define a UDF to extract URLs from text
        def extract_url(text):
            url = re.search(r'http[s]?://\S+', text)
            return url.group(0) if url else None

        # Register the UDF
        extract_url_udf = udf(extract_url, StringType())

        # Apply the UDF to extract URLs and create a new column
        df_with_urls = df.withColumn("url", extract_url_udf(col("line")))

        # Filter out rows where URL is None
        df_filtered = df_with_urls.filter(col("url").isNotNull())
        df_filtered = df_filtered.repartition(200)

        # Print filtered DataFrame to check contents
        print("Filtered DataFrame with URLs:")
        df_filtered.show(truncate=False)
        df_filtered.select("url").show(10, truncate=False)

        # Define the output path
        output_path = "file:///home/student/project_files/urls_output"
        
        # Ensure the output path exists
        #os.makedirs(os.path.dirname(output_path), exist_ok=True)

        # Write the filtered URLs to multiple part files (overwrite if it exists)
        df_filtered.select("url").write.mode("overwrite").text(output_path)

        print(f"Processed and saved URLs at {time.strftime('%Y-%m-%d %H:%M:%S')}")
    
    except Exception as e:
        print(f"An error occurred during processing: {e}")

# Schedule the job to run every 5 minutes
schedule.every(5).minutes.do(process_and_save_gkg_files)

# Keep the script running to continue scheduling tasks
while True:
    schedule.run_pending()
    time.sleep(1)

