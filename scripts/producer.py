import argparse
from time import sleep
from json import dumps
from kafka import KafkaProducer


def main():
    parser = argparse.ArgumentParser(description='Kafka producer client')
    parser.add_argument('-p', '--port', help='port for one of kafka brokers', required=True)
    args = parser.parse_args()
    port = args.port

    # producer の設定
    producer = KafkaProducer(
        bootstrap_servers=['localhost:{}'.format(port)],  # Kafka Broker ホスト
        value_serializer=lambda x: dumps(x).encode('utf-8'),  # シリアライズ
        acks=1 # リーダーパーティションへの書き込みを待って送信官僚とする
    )

    # トピックにメッセージを送信
    for j in range(1000):
        message = {'testProduceData': j}
        # Python ではライブラリがトピックを自動生成する(第一引数がトピック名)
        producer.send('topicPython', value=message)  # トピック名と送信メッセージを指定

        # 以下のようにkeyを指定して配置先のパーティションをコントロールすることが可能
        # producer.send('topicPython', key='hostname', value=message)

        print(message)
        sleep(0.5)


if __name__ == '__main__':
    main()
