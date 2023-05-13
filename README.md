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


## 👣 Additional steps
### Create a test user for Airflow
```
$ docker-compose run airflow-webserver airflow users create --role Admin --username admin \
  --email admin --firstname admin --lastname admin --password admin
```


### Check accesses
- Spark Master: http://localhost:8081
- Apache superset - http://localhost:8088 (admin/admin)

### For importing dump in MySQL
- Login to mysql docker container and import the ```dump-superset-latest``` SQL file from ```src/app/sqls``` folder 

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
 
