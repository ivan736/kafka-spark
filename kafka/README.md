# Set up kafka enviroments

* required `docker-compose`: `yum install docker-compose`
* start containers via `docker-compose`
* [kafka-compose.yml](kafka-compose.yml) contains `zookeeper`, `kafka`, `python-client` and `spark-client` to run a minimal demo

## start containers

* execute following commands in this directory
* start required containers by `docker-compose -f kafka-compose.yml up -d`

* copy files and install packages on `python-client`

    ```bash
    docker cp python-tools/. python-client:/app
    docker cp ../Pipfile python-client:/app
    docker exec python-client pipenv install --skip-lock
    ```

* create a topic `demo-topic` in kafka:

    ```bash
    docker exec kafka-server kafka-topics.sh \
        --create --bootstrap-server localhost:9092 \
        --replication-factor 1 --partitions 1 --topic demo-topic
    ```

* read topic list in kafka:

    ```bash
    docker run -it --rm --network kafka-pack \
        -e KAFKA_ZOOKEEPER_CONNECT=zookeeper-server:2181 \
        bitnami/kafka:latest \
        kafka-topics.sh --list  --zookeeper zookeeper-server:2181
    ```

* subscribe topic: the output will be show after `send a message` step is done

    ```bash
    docker exec kafka-server \
        kafka-console-consumer.sh \
        --bootstrap-server localhost:9092 --topic demo-topic --from-beginning
    ```

* subscribe demo-topic in spark
    * exec spark-client

        ```bash
        docker exec -ti spark-client bash
        ```

    * start pyspark shell
        ```bash
        bin/pyspark
        ```
    * subscribe kafka demo-topic

        ```python
        import os
        from pyspark import SparkContext
        from pyspark.streaming import StreamingContext
        from pyspark.streaming.kafka import KafkaUtils

        ZOOKEEPER_HOST = os.environ.get('ZOOKEEPER_HOST')

        sc.setLogLevel("ERROR")
        ssc = StreamingContext(sc,20)
        kafkaStream = KafkaUtils.createStream(ssc, ZOOKEEPER_HOST, 'spark-streaming', {'demo-topic':1})
        lines = kafkaStream.map(lambda x: x[1])
        lines.pprint()
        ssc.start()
        ssc.awaitTermination()
        ```

* test `consumer.py`: the output will be show after `send a message` step is done

    ```bash
    docker exec python-client pipenv run python consumer.py demo-topic
    ```

* send a message via producer.py on `python-client`

    ```bash
    docker exec python-client pipenv run python producer.py demo-topic demo-msg
    ```

* send messages via kafka

    ```bash
    docker exec -ti kafka-server \
    kafka-console-producer.sh --broker-list localhost:9092 --topic demo-topic
    ```

# notes  for quick access:
* export service ip

    ```bash
    export ZOOKEEPER_HOST=$(docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' zookeeper-server)
    export KAFKA_HOST=$(docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' kafka-server)
    ```