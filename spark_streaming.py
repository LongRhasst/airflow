from pyspark.sql import SparkSession
from pyspark.sql.functions import *

spark = SparkSession.builder.appName("ClickstreamAnalytics").getOrCreate()

df = spark.readStream.format("kafka") \
    .option("kafka.bootstrap.servers", "localhost:9092") \
    .option("subscribe", "click_events") \
    .option("startingOffsets", "earliest") \
    .load()
    
clicks = df.select(
    from_json(col("value").cast("string"),
    "event_id STRING, user_id STRING, event_type STRING, timestamp TIMESTAMP, page_url STRING"
    ).alias("data")) \
    .select("data.*") \
    .groupBy("user_id")
    
query = clicks.writeStream \
    .outputMode("complete") \
    .format("paraquet") \
    .option("path", "/data/clicks_output") \
    .option("checkpointLocation", "/checkpoints") \
    .start()
    
query.awaitTermination()
