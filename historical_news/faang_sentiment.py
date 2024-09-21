import schedule
import time
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, lower, split
import os

# Directory where the result will be saved (local file system)
output_path = "file:///home/student/project_files/faang_sentiments"  # Specify output path for local file system

# Initialize Spark session (create once and reuse)
spark = SparkSession.builder \
    .appName("GKG_FAANG_Sentiment_Analysis") \
    .config("spark.sql.shuffle.partitions", "10") \
    .config("spark.dynamicAllocation.enabled", "true") \
    .config("spark.dynamicAllocation.minExecutors", "2") \
    .config("spark.dynamicAllocation.maxExecutors", "10") \
    .getOrCreate()

# Function to perform FAANG sentiment analysis
def process_faang_sentiment():
    try:
        # Path to the unzipped GKG files in local file system
        gkg_path = "file:///home/student/project_files/extractedfiles/*.csv"  # Use "file:///" for local path

        # Load GKG data with Spark
        gkg_df = spark.read.option("delimiter", "\t").csv(gkg_path)

        # Select relevant columns from GKG (assuming they are in specific positions)
        gkg_df = gkg_df.select(
            col("_c0").alias("GKGRECORDID"),  # Record ID
            col("_c1").alias("DATE"),         # Date
            col("_c3").alias("ORGANIZATIONS"),  # Organizations mentioned in the article
            col("_c15").alias("TONE")          # Sentiment (Tone) information
        )

        # List of FAANG companies to filter (lowercase for case-insensitive comparison)
        faang_companies = ["facebook", "apple", "amazon", "netflix", "google"]

        # Filter for rows that mention any FAANG company in the organizations column (case-insensitive)
        faang_df = gkg_df.filter(
            lower(col("ORGANIZATIONS")).rlike("|".join(faang_companies))
        )

        # Split the TONE column and extract the overall tone score (the first value)
        faang_df = faang_df.withColumn("SENTIMENT_SCORE", split(col("TONE"), ",").getItem(0))

        # Extract date and sentiment score for each FAANG company
        faang_sentiment_df = faang_df.select("DATE", "ORGANIZATIONS", "SENTIMENT_SCORE")

        # Filter for only rows where a FAANG company is mentioned
        faang_sentiment_df = faang_sentiment_df.filter(
            col("ORGANIZATIONS").rlike("|".join(faang_companies))
        )

        # Ensure the output directory exists
        os.makedirs("/home/student/project_files/faang_sentiments", exist_ok=True)

        # Save the result to a CSV file in the local file system
        faang_sentiment_df.write.csv(output_path, mode="overwrite", header=True)

        print(f"Saved FAANG sentiment analysis to {output_path}")

    except Exception as e:
        print(f"Error processing FAANG sentiment: {str(e)}")

# Schedule the job to run every 5 minutes
schedule.every(5).minutes.do(process_faang_sentiment)

# Keep the script running to continue scheduling tasks
while True:
    schedule.run_pending()
    time.sleep(1)

