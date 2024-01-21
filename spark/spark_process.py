import logging
from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col
from pyspark.sql.types import StructType, StructField, StringType

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s:%(funcName)s:%(levelname)s:%(message)s')
logger = logging.getLogger("spark_structured_streaming")

def create_spark_session():
    """
    Creates a Spark session.
    """
    spark = SparkSession.builder \
        .appName("Kafka to Redshift Stream") \
        .getOrCreate()
    logger.info("Spark Session created")

    return spark

def create_initial_dataframe(spark_session):
    """
    Reads the streaming data from Kafka.
    """
    kafka_df = spark_session.readStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", "your_kafka_broker_servers") \
        .option("subscribe", "your_kafka_topic") \
        .load() \
        .selectExpr("CAST(value AS STRING) as json")
    logger.info("Initial dataframe created")

    return kafka_df

def create_final_dataframe(stream_df): 
    """
    Modifies the initial dataframe, and creates the final dataframe.
    """
    schema = StructType([
        StructField("id", StringType()),
        StructField("publishedAt", StringType()),
        StructField("salary", StringType()),
        StructField("title", StringType()),
        StructField("jobUrl", StringType()),
        StructField("companyName", StringType()),
        StructField("companyUrl", StringType()),
        StructField("location", StringType()),
        StructField("postedTime", StringType()),
        StructField("applicationsCount", StringType()),
        StructField("description", StringType()),
        StructField("contractType", StringType()),
        StructField("experienceLevel", StringType()),
        StructField("workType", StringType()),
        StructField("sector", StringType()),
        StructField("companyId", StringType()),
        StructField("posterProfileUrl", StringType()),
        StructField("posterFullName", StringType()),
    ])

    stream_df = stream_df.select(from_json(col("json"), schema).alias("data")).select("data.*")
    logger.info("Final dataframe created")

    return stream_df

def start_streaming(parsed_df):
    """
    Writes the final dataframe to Redshift.
    """
    query = parsed_df.writeStream \
        .format("com.databricks.spark.redshift") \
        .option("url", "jdbc:redshift://your_redshift_cluster_url:5439/your_database?user=your_user&password=your_password") \
        .option("dbtable", "your_redshift_table") \
        .option("checkpointLocation", "/path/to/checkpoint/dir") \
        .start()
    logger.info("Streaming started")

    return query.awaitTermination()

def streaming_data():
    """
    Orchestrates the streaming process.
    """
    spark = create_spark_session()
    df = create_initial_dataframe(spark)
    df_final = create_final_dataframe(df)
    start_streaming(df_final)


if __name__ == '__main__':
    streaming_data()