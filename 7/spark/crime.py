from pyspark.sql import SparkSession
from pyspark.sql.functions import count
from pyspark import AccumulatorParam
import csv
import pandas as pd


def remove_header(itr_index, itr):
    return iter(list(itr)[1:]) if itr_index == 0 else itr


def rdd_to_csv(rdd, filename):
    lines = rdd.map(lambda line: ','.join(str(d) for d in line))
    lines.saveAsTextFile(filename)


def list_to_csv(cols, data, filename):
    with open(filename, 'w') as myfile:
        wr = csv.writer(myfile)
        wr.writerow(cols)
        wr.writerows(data)


def dict_to_csv(cols, data, filename):
    with open(filename, 'w') as myfile:
        wr = csv.writer(myfile)
        wr.writerow(cols)
        wr.writerows(list(data.items()))


spark = SparkSession \
    .builder \
    .appName("crimedesc") \
    .getOrCreate()

cols = ["crimedesc", "frequency"]

df_pd = pd.read_csv('data.csv')
df_spark = spark.createDataFrame(df_pd)

rdd = df_spark.rdd

rdd = rdd.mapPartitionsWithIndex(remove_header)
base_rdd = rdd.map(lambda c: (
    c[5], 1)).cache()

# RDD method
crime_desc_freq_list = base_rdd.reduceByKey(lambda x, y: x + y).collect()
list_to_csv(cols, crime_desc_freq_list, "crimedesc_freq.rdd.csv")

# Accumulator method
class DictAccumulator(AccumulatorParam):

    def zero(self, init_value=dict()):
        return init_value

    def add(self, d, key, value):
        d.update({key: (d[key] + value) if key in d else value})

    def addInPlace(self, v1: dict, v2: dict):
        for key, value in v2.items():
            self.add(v1, key, value)
        return v1


def acc_count(item, acc):
    key = item[0]
    val = item[1]
    acc += {key: val}


acc = spark.sparkContext.accumulator(dict(), DictAccumulator())
base_rdd.foreach(lambda item: acc_count(item, acc))
dict_to_csv(cols, acc.value, "crimedesc_freq.accumulator.csv")


# Dataframe method
freq_df = df_spark.groupBy("crimedescr").agg(count("*").alias("frequency"))
freq_df.toPandas().to_csv('crimedesc_freq.df.csv', index=False)

# Dataframe SQL method
# Create Temporary table in PySpark
df_spark.createOrReplaceTempView("crime")
sql_str = "select crimedescr, count(*) as frequency from crime group by crimedescr"
sql_freq_df = spark.sql(sql_str)
sql_freq_df.toPandas().to_csv('crimedesc_freq.df_sql.csv', index=False)
