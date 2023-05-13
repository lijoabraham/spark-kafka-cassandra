from queue_dao import QueueDAO
from pyspark.sql.types import StructType,StructField,LongType,IntegerType,FloatType,StringType
from pyspark.sql.functions import split,from_json,col


class Consumer:

    def run(self):
        stockSchema = StructType([
                StructField("s_index",StringType(),False),
                StructField("s_date",StringType(),False),
                StructField("open",FloatType(),False),
                StructField("high",FloatType(),False),
                StructField("low",FloatType(),False),
                StructField("close",FloatType(),False),
                StructField("adj_close",FloatType(),False),
                StructField("volume",FloatType(),False),
                StructField("close_usd",FloatType(),False)
            ])

        dao = QueueDAO('kafka')
        df = dao.recieve_stream('topic_test')
        df.printSchema() 

        df1 = df.selectExpr("CAST(value AS STRING)").select(from_json(col("value"),stockSchema).alias("data")).select("data.*")
        df1.printSchema()

        # query = df1.writeStream \
        #     .outputMode("append") \
        #     .format("console") \
        #     .option("truncate", False) \
        #     .start() \
        #     .awaitTermination()
        # print(df1)

        def writeToCassandra(writeDF, _):
            writeDF.write \
                .format("org.apache.spark.sql.cassandra")\
                .mode('update')\
                .options(table="data", keyspace="stock_market")\
                .save()

        df1.writeStream \
            .option("spark.cassandra.connection.host","172.18.0.5")\
            .option("spark.cassandra.auth.username","cassandra")\
            .option("spark.cassandra.auth.password","cassandra")\
            .foreachBatch(writeToCassandra) \
            .outputMode("update") \
            .start()\
            .awaitTermination()


    def run1(self):
        dao = QueueDAO('kafka')
        consumer = dao.recieve_message('topic_test')
        for message in consumer:
            message = message.value
            print('{} retrieved'.format(message))
       
       

if __name__ == '__main__':
    p = Consumer()
    p.run()

# spark-submit --master spark://spark:7077 --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.2.0,com.datastax.spark:spark-cassandra-connector_2.12:3.2.0 --conf spark.cassandra.connection.host=cassandra --conf spark.cassandra.auth.username=cassandra --conf spark.cassandra.auth.password=cassandra app/consumer.py
# spark-submit --jars /usr/local/spark/app/dependencies/spark-sql-kafka-0-10_2.12-3.2.1.jar,/usr/local/spark/app/dependencies/commons-pool2-2.8.0.jar,/usr/local/spark/app/dependencies/kafka-clients-2.1.1.jar,/usr/local/spark/app/dependencies/spark-streaming-kafka-0-10-assembly_2.12-3.2.1.jar,/usr/local/spark/app/dependencies/spark-token-provider-kafka-0-10_2.12-3.1.2.jar --packages org.apache.spark:spark-sql-kafka-0-10_2.13:3.2.1 consumer.py