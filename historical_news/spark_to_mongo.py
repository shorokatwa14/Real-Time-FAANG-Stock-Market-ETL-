import time
from pymongo import MongoClient

# Assuming pandas_df is your existing Pandas DataFrame
pdf = pandas_df

if not pdf.empty:
    try:
        # Connect to MongoDB
        client = MongoClient("mongodb+srv://khalid:2422@cluster0.mdxcz.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")

        # Access the database and collection
        db = client["news_hist"]
        collection = db["news_historical"]

        # Convert the DataFrame to a list of dictionaries
        records = pdf.to_dict(orient='records')

        # Loop through each record and insert it every 5 seconds
        for record in records:
            collection.insert_one(record)  # Insert one record
            print(f"Inserted record: {record}")
            time.sleep(5)  # Wait for 5 seconds before inserting the next record

        print("All records inserted successfully.")

    except Exception as e:
        print(f"Error: {e}")
else:
    print("The DataFrame is empty. No data to insert.")
