[【入門】Apache kafka とは？docker で起動から使い方までを解説](https://hogetech.info/2020/11/07/kafka-%e5%85%a5%e9%96%80-%e3%82%b9%e3%83%88%e3%83%aa%e3%83%bc%e3%83%a0%e5%87%a6%e7%90%86-%e5%88%86%e6%95%a3%e3%82%b9%e3%83%88%e3%83%aa%e3%83%bc%e3%83%9f%e3%83%b3%e3%82%b0%e3%83%97%e3%83%a9%e3%83%83/)
[Kafka in Docker のチュートリアル](https://qiita.com/psyashes/items/e50bdfe35a2e7778986d)

### コンテナ起動
```
docker-compose up -d
# Scale up
docker-compose scale kafka=3
```

### Apache Kafka を CLI で操作

クライアント用コンテナ(Producer)の操作

```
# コンテナ起動
export DOCKER_HOST_IP=$(ipconfig getifaddr en0) && export ZK_HOST=${DOCKER_HOST_IP} && export ZK_PORT=2181 && \
./start-kafka-shell.sh $DOCKER_HOST_IP $ZK_HOST:$ZK_PORT

# トピック作成: パーティション:3, レプリカ:2(リーダーレプリカ:1, フォロワーレプリカ:1)
# ここでいうtopicCLIはトピック名なので自由に変えてOK
# topicはzookeeperに保存されるっぽい -> クライアント用コンテナを削除してもtopicCLIは残っていた
$KAFKA_HOME/bin/kafka-topics.sh --create --topic topicCLI --zookeeper $ZK --partitions 3 --replication-factor 2

# Topicの一覧表示
$KAFKA_HOME/bin/kafka-topics.sh --list --zookeeper $ZK
# 出力
topicCLI

# topicCLIの詳細
$KAFKA_HOME/bin/kafka-topics.sh --describe --zookeeper $ZK --topic topicCLI
# 出力
Topic: topicCLI	PartitionCount: 3	ReplicationFactor: 2	Configs:
	Topic: topicCLI	Partition: 0	Leader: 1001	Replicas: 1001,1002	Isr: 1001,1002
	Topic: topicCLI	Partition: 1	Leader: 1002	Replicas: 1002,1003	Isr: 1002,1003
	Topic: topicCLI	Partition: 2	Leader: 1003	Replicas: 1003,1001	Isr: 1003,1001

# ちなみに$ZKの中身
echo $ZK
# 出力
192.168.10.113:2181

# prducer, consumerそれぞれの操作用スクリプトが用意されている
ls $KAFKA_HOME/bin/kafka-console*
/opt/kafka/bin/kafka-console-consumer.sh  /opt/kafka/bin/kafka-console-producer.sh

# producerとしてメッセージ送信
$KAFKA_HOME/bin/kafka-console-producer.sh --topic=topicCLI --broker-list=`broker-list.sh`
>test1
>test2
>test3
>test4
```

クライアント用コンテナ(Consumer)の操作

```
# コンテナ起動
export DOCKER_HOST_IP=$(ipconfig getifaddr en0) && export ZK_HOST=${DOCKER_HOST_IP} && export ZK_PORT=2181 && \
./start-kafka-shell.sh $DOCKER_HOST_IP $ZK_HOST:$ZK_PORT

# consumerとしてメッセージを受信
$KAFKA_HOME/bin/kafka-console-consumer.sh --topic=topicCLI --bootstrap-server=`broker-list.sh` --from-beginning
```

### Apache Kafka を Python で操作

scripts 配下の Python スクリプトを Mac から実行  
1つのKafka Brokerのホストのポート番号が49795の場合  

```
# producer起動
python3 producer.py -p 49795

# 別タブを開いてconsumer起動
python consumer.py -p 49795
```
