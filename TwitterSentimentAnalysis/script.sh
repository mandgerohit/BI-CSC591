initdir(){
    cd '/home/rohit/BI-CSC591/02.Apache.Spark.Streaming.Project-2.SentimentAnalysis.FINAL/kafka_2.10-0.9.0.0'
}
initdir
gnome-terminal --tab -e 'bash -c "bin/zookeeper-server-start.sh config/zookeeper.properties"'
sleep 2
gnome-terminal --tab -e 'bash -c "bin/kafka-server-start.sh config/server.properties"'
sleep 3
gnome-terminal --tab -e 'bash -c "bin/kafka-console-consumer.sh --zookeeper localhost:2181 --topic twitterstream --from-beginning"'
changedir(){
    cd ..
}
changedir
sleep 1
gnome-terminal --tab -e 'bash -c "python twitter_to_kafka.py"'
sleep 2
gnome-terminal --tab -e 'bash -c "$SPARK_HOME/bin/spark-submit --packages org.apache.spark:spark-streaming-kafka_2.10:1.5.1 twitterStream.py"'







