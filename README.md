# spark-kafka-cassandra

# mutual_fund_recommendation_etl


## 🛠 Setup

Clone project
```git clone https://github.com/lijoabraham/mutual_fund_recommendation_etl.git```

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

### For initializing superset
After starting the Superset server, initialize the database with an admin user and Superset tables using the superset-init helper script:
```
docker run --detach --name superset [options] amancevice/superset
docker exec -it superset superset-init
```


### Check accesses
- Spark Master: http://localhost:8081
- Apache superset - http://localhost:8088 (admin/admin)

### For creating catalog in presto
```
PRESTO_CTR=$(docker container ls | grep 'presto_1' | awk '{print $1}')
docker cp cassandra.properties $PRESTO_CTR:/opt/presto-server/etc/catalog/cassandra.properties
docker exec -it $PRESTO_CTR sh -c "ls /opt/presto-server/etc/catalog"
```

### For checking the catalog is created correctly
```
docker exec -it $PRESTO_CTR presto-cli
show catalogs ;
```
- If you do not see cassandra, then we need to restart the container

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
 
