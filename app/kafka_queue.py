from json import dumps, loads

from dependencies import spark as spk

class KafkaQueue:

    __queueInstance = None

    def __init__(self):
        if KafkaQueue.__queueInstance != None:
            raise Exception("Object Already exists!")
        else:
            from kafka import KafkaProducer
            from kafka import KafkaConsumer
            self.__producer = KafkaProducer(api_version=(0, 10, 0),bootstrap_servers=['localhost:9092'],
                                value_serializer=lambda x: 
                                dumps(x).encode('utf-8'))
            # self.__consumer =  KafkaConsumer(
            #         bootstrap_servers=['localhost:9092'],
            #         auto_offset_reset='earliest',
            #         enable_auto_commit=True,
            #         group_id='lijo-group-1',
            #         value_deserializer=lambda x: loads(x.decode('utf-8'))
            #     )
            KafkaQueue.__queueInstance = self
            
    @staticmethod
    def get_queue_connection():
        if KafkaQueue.__queueInstance == None:
            KafkaQueue()
        return KafkaQueue.__queueInstance
    
    def send(self, topic, data):
        KafkaQueue.__queueInstance.__producer.send(topic, data)
    
    def recieve(self, topic):
        KafkaQueue.__queueInstance.__consumer.subscribe([topic])
        print(topic)
        return KafkaQueue.__queueInstance.__consumer
    
    def recieve_stream(self, topic):
        params = {'app_name': 'KafkaToCassandra', 'files': [],'jars':[], 'packages' : ['org.apache.spark:spark-sql-kafka-0-10_2.12:3.2.0','com.datastax.spark:spark-cassandra-connector_2.12:3.2.0']}
        # spark, log, config = spk.SparkConnection(params)
        spark_details = spk.SparkConnection(params=params)
        # exit("here")
        # log = spark_details.log
        spark_details.spark.sparkContext.setLogLevel("DEBUG")
        df = spark_details.spark\
                .readStream \
                .format("kafka") \
                .option("kafka.bootstrap.servers", "kafka:9092") \
                .option("subscribe", topic) \
                .option("delimeter",",") \
                .option("startingOffsets", "earliest") \
                .load()
        return df