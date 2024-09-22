# **FAANG Stock Sentiment Analysis and Prediction**

## **Project Overview**

This project aims to predict whether the stock prices of FAANG companies (Facebook, Amazon, Apple, Netflix, and Google) will go up or down using historical news sentiment data. The data pipeline incorporates news ingestion from GDELT, sentiment analysis, processing via Apache Spark, and machine learning models (Random Forest, XGBoost, and LSTM) to forecast stock price movements.

### **Key Components:**

1. **Data Collection**: News data ingestion from GDELT via Apache Flume.
2. **Data Preprocessing**: Unzipping, filtering, and extracting relevant FAANG news data.
3. **Sentiment Analysis**: Quantifying the sentiment of FAANG-related news articles.
4. **Data Processing with Spark**: Performing transformations and insight generation using Apache Spark.
5. **Data Storage and Visualization**: Storing processed data in MongoDB for visualization.
6. **Stock Prediction Models**: Using machine learning models to predict whether FAANG stock prices will rise or fall based on sentiment.

---

## **Table of Contents**

- [Project Overview](#project-overview)
- [Pipeline Workflow](#pipeline-workflow)
  - [Data Ingestion](#data-ingestion)
  - [Data Preprocessing](#data-preprocessing)
  - [Sentiment Analysis](#sentiment-analysis)
  - [Data Processing with Spark](#data-processing-with-spark)
  - [Data Storage and Visualization](#data-storage-and-visualization)
  - [Modeling and Prediction](#modeling-and-prediction)
- [Technologies Used](#technologies-used)
- [Installation and Setup](#installation-and-setup)
- [Running the Pipeline](#running-the-pipeline)
- [Future Enhancements](#future-enhancements)

---

## **Pipeline Workflow**

### **1. Data Ingestion**

The project starts by ingesting historical news data from GDELT (Global Database of Events, Language, and Tone). We use **Apache Flume** to collect news data streams and store them into HDFS.

- **Configuration File**: The Flume agent is configured in [GDELT.conf](./GDELT.conf) to fetch news data continuously.
![data_saved_hdfs](https://github.com/user-attachments/assets/79d24065-3527-4715-bb47-21c747271362)

### **2. Data Preprocessing**

Once the data is ingested into HDFS, the news files, which are in a compressed format, need to be **unzipped**. After unzipping, the dataset is filtered to focus on FAANG-related news articles.

- **Unzipping Files**: The script [unzipfiles.py](./unzipfiles.py) is used to extract the zipped news files.
  ![unzipping_the_data](https://github.com/user-attachments/assets/000c89b7-f76c-4ffb-ac3f-0848578a0bb4)

- **Extracting Relevant Data**: After extracting the URLs, only FAANG-related news articles are retained using the [get_from_flume.py](./get_from_flume.py) script.
![sentiment_score_faang](https://github.com/user-attachments/assets/2907d2db-7000-4399-8cff-574e4bc64784)

### **3. Sentiment Analysis**

For each FAANG-related news article, we compute a **sentiment score** that indicates the tone of the news (positive, negative, or neutral). This score will be used to analyze how news sentiment influences stock movements.

- **Sentiment Score Extraction**: Sentiment analysis is performed using the [faang_sentiment.py](./faang_sentiment.py) script to assign sentiment values for FAANG companies.
![filtering_the_data](https://github.com/user-attachments/assets/00306e60-0854-4c92-ab19-c322c7ff7562)

### **4. Data Processing with Spark**

Next, the sentiment data is loaded into **Apache Spark** for further processing and insight generation. Spark is used to transform and analyze the data at scale, preparing it for model training and visualization.

- **Spark Processing**: We use the [spark_to_mongo.py](./spark_to_mongo.py) script to load the sentiment data into Spark, transform it, and send the processed data to MongoDB for visualization.

### **5. Data Storage and Visualization**

The processed data is then moved to **MongoDB** for storage. MongoDB allows us to visualize the trends and insights from the sentiment data through interactive dashboards.
![stock_price_and_sentiment](https://github.com/user-attachments/assets/a030303a-5f95-478d-880d-5884c5860529)

### **6. Modeling and Prediction**

To predict future stock movements (up or down), we applied several machine learning models:
  
  - **Random Forest (RF)**
  - ![calculating_accuracy_rf](https://github.com/user-attachments/assets/1437ad44-8902-47bb-8a39-63376d69c9d0)
  - **XGBoost**
  - ![calculating_accuracy_XGBoost](https://github.com/user-attachments/assets/a40d2c48-3849-4189-adfd-190704918966)
  - **LSTM (Long Short-Term Memory)**
  - ![calculating_accuracy_LSTM](https://github.com/user-attachments/assets/3c4d16f0-8a84-4f93-8195-221b3eda3c98)

These models were trained using the sentiment data to predict whether the stock price will increase or decrease for each FAANG company.

- **Model Training and Evaluation**: All models are trained in the [modeling_insights.ipynb](./modeling_insights.ipynb) notebook, where predictions and evaluations are performed.

---

## **Technologies Used**

### **Data Processing & Ingestion:**
- **Apache Flume** – For collecting GDELT data.
- **Apache HDFS** – For distributed storage of raw data.
- **Apache Spark** – For distributed processing and transformation of data.

### **Database & Visualization:**
- **MongoDB** – For storing processed data and enabling visualization.

### **Programming Languages & Libraries:**
- **Python** – For writing data processing, sentiment analysis, and machine learning scripts.
- **Pandas, NumPy** – For data manipulation and analysis.
- **pandas-ta** – For technical indicator calculations.
- **scikit-learn, XGBoost, TensorFlow/Keras** – For building machine learning models.

---

## **Installation and Setup**

### **Prerequisites**
- **Apache Flume**
- **Apache HDFS**
- **Apache Spark**
- **MongoDB**
- **Python (3.7 or higher)**

### **Python Dependencies**

You can install the required Python libraries by running:

```bash
pip install -r requirements.txt
```

---

## **Running the Pipeline**

### 1. **Data Ingestion**:

To start ingesting data from GDELT, configure and run the Flume agent:

```bash
flume-ng agent -n agent -c conf -f GDELT.conf
```

### 2. **Unzip and Filter Data**:

Once the data is ingested and saved to HDFS, unzip and filter the FAANG-related news:

```bash
python unzipfiles.py
python get_from_flume.py
```

### 3. **Run Sentiment Analysis**:

Generate sentiment scores for FAANG news articles:

```bash
python faang_sentiment.py
```

### 4. **Process Data with Spark**:

Use Spark to load data from HDFS, process it, and send it to MongoDB:

```bash
spark-submit spark_to_mongo.py
```

### 5. **Train and Evaluate Models**:

To train the machine learning models and evaluate their performance, run the notebook:

```bash
jupyter notebook modeling_insights.ipynb
```

---


