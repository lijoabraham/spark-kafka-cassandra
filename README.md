# spark-kafka-cassandra

## 🛠 Setup

Clone project
```git clone https://github.com/lijoabraham/spark-kafka-cassandra.git```

### Build spark-python Docker
```
$ cd spark-kafka-cassandra
$ docker build --tag python-docker .
```
Change the image name in the below place of docker-compose.yaml file, if you have a different image name
```
python-worker:
    build: .
    image: python-docker:latest
```

### Launch containers
```
$ cd spark-kafka-cassandra/
$ docker-compose -f docker-compose.yml up -d
```



### Check accesses
- Spark Master: http://localhost:8081
- Apache superset - http://localhost:8088 (admin/admin)

### For importing dump in MySQL
- Login to cassandra docker container and run the  SQL file from ```app/db``` folder 

### For running the commands manually
- Login to ```spark-kafka-cassandra:latest``` container and run the following jobs
  #### Producer job 
  ```
  python app/producer.py
  ```
  #### Consumer Spark job 
  ```
  spark-submit --master spark://spark:7077 --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.2.0,com.datastax.spark:spark-cassandra-connector_2.12:3.2.0 --conf spark.cassandra.connection.host=cassandra --conf spark.cassandra.auth.username=cassandra --conf spark.cassandra.auth.password=cassandra app/consumer.py
  ```
 
