# Set up kafka enviroments

* required `docker-compose`: `yum install docker-compose`
* start containers via `docker-compose`
* [kafka-compose.yml](kafka-compose.yml) contains `zookeeper`, `kafka` and `python-client` to run a minimal demo

## start containers

* execute following commands in this directory
* start required containers by `docker-compose -f kafka-compose.yml up -d`
* create a topic `demo-topic` in kafka:

    ```bash
    docker exec kafka-server /opt/bitnami/kafka/bin/kafka-topics.sh \
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
        /opt/bitnami/kafka/bin/kafka-console-consumer.sh \
        --bootstrap-server localhost:9092 --topic demo-topic --from-beginning
    ```

* export service ip

    ```bash
    export ZOOKEEPER_HOST=$(docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' zookeeper-server)
    export KAFKA_HOST=$(docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' kafka-server)
    ```

* copy files and install packages on `python-client`

    ```bash
    docker cp producer.py python-client:/app/producer.py
    docker cp ../Pipfile python-client:/app/Pipfile
    docker exec python-client pipenv install --skip-lock
    ```

* send a message vi producer.py on `python-client`

    ```bash
    docker exec python-client pipenv run python producer.py $KAFKA_HOST demo-msg
    ```

* test `consumer.py`

    ```bash
    docker exec python-client pipenv run python consumer.py $KAFKA_HOST
    ```