import argparse
from kafka import KafkaConsumer
from json import loads
from time import sleep


def main():
    parser = argparse.ArgumentParser(description='Kafka consumer client')
    parser.add_argument('-p', '--port', help='port for one of kafka brokers', required=True)
    args = parser.parse_args()
    port = args.port

    # consumer の設定
    consumer = KafkaConsumer(
        'topicPython',  # トピック名
        bootstrap_servers=['localhost:{}'.format(port)],  # Kafka Broker ホスト
        auto_offset_reset='earliest',  # オフセットを一番最初から
        value_deserializer=lambda x: loads(x.decode('utf-8'))  # デシリアライズ
    )

    # 消費したメッセージを画面に表示
    for event in consumer:
        event_message = event.value
        print(event_message)
        sleep(0.5)


if __name__ == '__main__':
    main()
