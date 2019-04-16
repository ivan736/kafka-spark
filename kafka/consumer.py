import sys

from kafka import KafkaConsumer


def read_msg(server_ip):
    consumer = KafkaConsumer(
        'demo-topic', bootstrap_servers=f'{server_ip}:9092')
    for msg in consumer:
        print(msg)
        sys.stdout.flush()


if __name__ == "__main__":
    server_ip = sys.argv[1]
    read_msg(server_ip)
