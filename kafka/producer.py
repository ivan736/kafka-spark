import sys

from kafka import KafkaProducer


def send(server_ip, demo_msg):
    producer = KafkaProducer(bootstrap_servers=f'{server_ip}:9092')
    producer.send('demo-topic', demo_msg.encode('utf8'))
    producer.flush()


if __name__ == "__main__":
    server_ip = sys.argv[1]
    demo_msg = sys.argv[2]
    send(server_ip, demo_msg)
