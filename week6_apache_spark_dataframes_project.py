# -*- coding: utf-8 -*-
"""Week6_Apache_Spark_DataFrames_Project.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1mxsxtAyEUm4yQy1g4TIsJLiArwijk-pv

# Apache Spark DataFrames Project

# **Instructions**


As a Data professional, you need to perform an analysis by answering questions about some stock market data on Safaricom from the years 2012-2017.


You will need to perform the following:

**Data Importation and Exploration**

● Start a spark session and load the stock file while inferring the data types.

● Determine the column names

● Make observations about the schema.

● Show the first 5 rows

● Use the describe method to learn about the data frame

**Data Preparation**

● Format all the data to 2 decimal places i.e. format_number()

● Create a new data frame with a column called HV Ratio that is the ratio of the High Price versus volume of stock traded for a day

**Data Analysis**

● What day had the Peak High in Price?

● What is the mean of the Close column?

● What is the max and min of the Volume column?

● How many days was the Close lower than 60 dollars?

● What percentage of the time was the High greater than 80 dollars?

● What is the Pearson correlation between High and Volume?

● What is the max High per year?

● What is the average Close for each Calendar Month?
"""

# Installing pyspark

!pip install pyspark
import pandas as pd

# Run a local spark session
# ---
from pyspark import SparkFiles
from pyspark.sql import SparkSession
spark = SparkSession.builder.master("local[*]").getOrCreate()
sc = spark.sparkContext

"""## Load data from the dataset"""

!wget -O saf_stock.csv https://bit.ly/3pmchka
f = open('saf_stock.csv')

for i in range(0,5):
    print(f.readline())

"""## Determine the column names"""

df = pd.read_csv('saf_stock.csv')
df.columns

"""## Read json data from csv file and print its schema"""

#Reading in Data
from pyspark.sql import SQLContext

# Pass in the SparkContext object `sc`
sqlCtx = SQLContext(sc)

# Read JSON data into a DataFrame object `df`
df = sqlCtx.read.csv("saf_stock.csv")

df.registerTempTable('saf_stock')
tables = sqlCtx.tableNames()
print(tables)
# Print the type
print(type(df))

#Schema
#Call the printSchema() method on the Spark DataFrame df to display the schema that Spark inferred.
df = sqlCtx.read.csv("saf_stock.csv", header=True, inferSchema=True)
df.printSchema()

"""## Showing the first 5 rows"""

df.show(5)

"""## Use the describe method to learn about the data frame"""

query = 'select * from saf_stock'
sqlCtx.sql(query).describe().show(5)

"""## Create a new data frame with a column called HV Ratio that is the ratio of the High Price versus volume of stock traded for a day"""

from pyspark.sql.functions import lit,when,col,expr,round
df_prep= (
 df.withColumn('HV',expr("High/Volume")))

df_prep.show(5)

"""## Data Analysis"""

from pyspark.sql import SQLContext
sqlCtx = SQLContext(sc)


#Register a table in SQL
table = df_prep.registerTempTable("saf_stock1")

table = sqlCtx.tableNames()
print(table)

"""## What day had the Peak High in Price?"""

query = "SELECT \
         Date,max(High) AS Peak_Price \
     FROM saf_stock1 GROUP BY Date \
    ORDER BY Peak_Price DESC LIMIT 1 "
sqlCtx.sql(query).show()

"""## What is the mean of the Close column?"""

query = "\
SELECT\
    MEAN(Close) AS MEAN\
        FROM saf_stock1"

sqlCtx.sql(query).show()

"""## What is the max and min of the Volume column?"""

query = "SELECT\
     MIN(Volume) Min_Volume, MAX(Volume) Max_Volume\
         FROM saf_stock1 "

sqlCtx.sql(query).show()

"""## How many days was the Close lower than 60 dollars?"""

query = "SELECT  COUNT(Date) FROM saf_stock1 WHERE Close <= 60 "
sqlCtx.sql(query).show()

"""## What percentage of the time was the High greater than 80 dollars?"""

query = "SELECT ROUND((COUNT(High)/1258*100),2) higher_than_80  FROM saf_stock1  WHERE High >= 80"

sqlCtx.sql(query).show()

"""## What is the Pearson correlation between High and Volume?"""

query = "SELECT ROUND(corr(High,Volume),2) Pearson_Correlation\
          FROM saf_stock1"

sqlCtx.sql(query).show()

"""## What is the max High per year?"""

query = "SELECT  EXTRACT(YEAR FROM Date) Year, MAX(High) Max_High FROM saf_stock1\
     GROUP BY Year ORDER BY Max_High DESC"
sqlCtx.sql(query).show()

"""## What is the average Close for each Calendar Month?"""

query = "SELECT EXTRACT(MONTH FROM Date) Month,ROUND(AVG(Close),2) Avg_Close FROM saf_stock1\
    GROUP BY Month ORDER BY Month ASC"

sqlCtx.sql(query).show()