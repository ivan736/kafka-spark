# to create a spark image with kafka.jars installed
FROM mesosphere/spark

# download and unzip kafka required jars to jar_files
# https://jar-download.com/?search_box=spark-streaming-kafka-0-8
# spark-streaming-kafka-0-8-assembly_2.11 from group org.apache.spark (version 2.4.1)
COPY jar_files /opt/spark/dist/jars