FAANG Stock Sentiment Analysis and Prediction
Project Overview
This project aims to predict whether the stock prices of FAANG companies (Facebook, Amazon, Apple, Netflix, and Google) will go up or down using historical news sentiment data. The data pipeline incorporates news ingestion from GDELT, sentiment analysis, processing via Apache Spark, and machine learning models (Random Forest, XGBoost, and LSTM) to forecast stock price movements.

Key Components:
Data Collection: News data ingestion from GDELT via Apache Flume.
Data Preprocessing: Unzipping, filtering, and extracting relevant FAANG news data.
Sentiment Analysis: Quantifying the sentiment of FAANG-related news articles.
Data Processing with Spark: Performing transformations and insight generation using Apache Spark.
Data Storage and Visualization: Storing processed data in MongoDB for visualization.
Stock Prediction Models: Using machine learning models to predict whether FAANG stock prices will rise or fall based on sentiment.
Table of Contents
Project Overview
Pipeline Workflow
Data Ingestion
Data Preprocessing
Sentiment Analysis
Data Processing with Spark
Data Storage and Visualization
Modeling and Prediction
Technologies Used
Installation and Setup
Running the Pipeline
Future Enhancements
Pipeline Workflow
1. Data Ingestion
The project starts by ingesting historical news data from GDELT (Global Database of Events, Language, and Tone). We use Apache Flume to collect news data streams and store them into HDFS.

Configuration File: The Flume agent is configured in GDELT.conf to fetch news data continuously.
2. Data Preprocessing
Once the data is ingested into HDFS, the news files, which are in a compressed format, need to be unzipped. After unzipping, the dataset is filtered to focus on FAANG-related news articles.

Unzipping Files: The script unzipfiles.py is used to extract the zipped news files.

Extracting Relevant Data: After extracting the URLs, only FAANG-related news articles are retained using the get_from_flume.py script.

3. Sentiment Analysis
For each FAANG-related news article, we compute a sentiment score that indicates the tone of the news (positive, negative, or neutral). This score will be used to analyze how news sentiment influences stock movements.

Sentiment Score Extraction: Sentiment analysis is performed using the faang_sentiment.py script to assign sentiment values for FAANG companies.
4. Data Processing with Spark
Next, the sentiment data is loaded into Apache Spark for further processing and insight generation. Spark is used to transform and analyze the data at scale, preparing it for model training and visualization.

Spark Processing: We use the spark_to_mongo.py script to load the sentiment data into Spark, transform it, and send the processed data to MongoDB for visualization.
5. Data Storage and Visualization
The processed data is then moved to MongoDB for storage. MongoDB allows us to visualize the trends and insights from the sentiment data through interactive dashboards.

6. Modeling and Prediction
To predict future stock movements (up or down), we applied several machine learning models:

Random Forest (RF)
XGBoost
LSTM (Long Short-Term Memory)
These models were trained using the sentiment data to predict whether the stock price will increase or decrease for each FAANG company.

Model Training and Evaluation: All models are trained in the modeling_insights.ipynb notebook, where predictions and evaluations are performed.
Technologies Used
Data Processing & Ingestion:
Apache Flume – For collecting GDELT data.
Apache HDFS – For distributed storage of raw data.
Apache Spark – For distributed processing and transformation of data.
Database & Visualization:
MongoDB – For storing processed data and enabling visualization.
Programming Languages & Libraries:
Python – For writing data processing, sentiment analysis, and machine learning scripts.
Pandas, NumPy – For data manipulation and analysis.
pandas-ta – For technical indicator calculations.
scikit-learn, XGBoost, TensorFlow/Keras – For building machine learning models.
Installation and Setup
Prerequisites
Apache Flume
Apache HDFS
Apache Spark
MongoDB
Python (3.7 or higher)
Python Dependencies
You can install the required Python libraries by running:

bash
Copy code
pip install -r requirements.txt
Running the Pipeline
1. Data Ingestion:
To start ingesting data from GDELT, configure and run the Flume agent:

bash
Copy code
flume-ng agent -n agent -c conf -f GDELT.conf
2. Unzip and Filter Data:
Once the data is ingested and saved to HDFS, unzip and filter the FAANG-related news:

bash
Copy code
python unzipfiles.py
python get_from_flume.py
3. Run Sentiment Analysis:
Generate sentiment scores for FAANG news articles:

bash
Copy code
python faang_sentiment.py
4. Process Data with Spark:
Use Spark to load data from HDFS, process it, and send it to MongoDB:

bash
Copy code
spark-submit spark_to_mongo.py
5. Train and Evaluate Models:
To train the machine learning models and evaluate their performance, run the notebook:

bash
Copy code
jupyter notebook modeling_insights.ipynb
