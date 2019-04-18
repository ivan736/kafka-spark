import os
import sys

from kafka import KafkaConsumer

KAFKA_HOST = os.environ.get('KAFKA_HOST')


def subscribe_topic(topic):
    consumer = KafkaConsumer(topic, bootstrap_servers=KAFKA_HOST)
    for msg in consumer:
        print(msg)
        sys.stdout.flush()


if __name__ == "__main__":
    kafka_topic = sys.argv[1]
    subscribe_topic(kafka_topic)
