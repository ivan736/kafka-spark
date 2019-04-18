import os
import sys

from kafka import KafkaProducer

KAFKA_HOST = os.environ.get('KAFKA_HOST')


def send(topic, msg):
    producer = KafkaProducer(bootstrap_servers=KAFKA_HOST)
    producer.send(topic, msg.encode('utf8'))
    producer.flush()


if __name__ == "__main__":
    kafka_topic = sys.argv[1]
    kafka_msg = sys.argv[2]

    send(kafka_topic, kafka_msg)
