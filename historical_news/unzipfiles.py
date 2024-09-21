import os
import zipfile
import schedule
import time
from pyspark import SparkConf, SparkContext
from pyspark.sql import SparkSession

# Initialize Spark
conf = SparkConf() \
    .setAppName("UnzipFilesApp") \
    .set("spark.executor.memory", "2g") \
    .set("spark.executor.cores", "2") \
    .set("spark.dynamicAllocation.enabled", "true") \
    .set("spark.dynamicAllocation.minExecutors", "1") \
    .set("spark.dynamicAllocation.maxExecutors", "10") \
    .set("spark.sql.adaptive.enabled", "true")
    
sc = SparkContext.getOrCreate(conf=conf)
spark = SparkSession.builder.getOrCreate()

# Define the directory paths
zip_dir = "/home/student/project_files/zippedfiles"  # Directory where zip files are located
unzip_dir = "/home/student/project_files/extractedfiles"  # Directory where files will be extracted

# Create the extraction directory if it doesn't exist
os.makedirs(unzip_dir, exist_ok=True)

# Function to unzip a single file
def unzip_file(zip_filepath, unzip_dir):
    try:
        with zipfile.ZipFile(zip_filepath, 'r') as zip_ref:
            zip_ref.extractall(unzip_dir)
        print(f"Unzipped {zip_filepath} into {unzip_dir}")
    except Exception as e:
        print(f"Failed to unzip {zip_filepath}: {str(e)}")

# Function to unzip all files in the zip_dir using Spark
def unzip_files_spark(zip_dir, unzip_dir):
    # List all files in the zip_dir
    zip_files = [os.path.join(zip_dir, filename) for filename in os.listdir(zip_dir) if filename.endswith(".zip")]

    # Parallelize the list of zip files and process them using Spark
    rdd = sc.parallelize(zip_files)
    rdd.foreach(lambda zip_filepath: unzip_file(zip_filepath, unzip_dir))

    print(f"Unzipped all files in {zip_dir} to {unzip_dir}")

# Schedule the unzipping job to run every 5 minutes
schedule.every(5).minutes.do(unzip_files_spark, zip_dir, unzip_dir)

# Keep the script running to continue scheduling tasks
while True:
    schedule.run_pending()
    time.sleep(1)

