from kafka import KafkaConsumer
import json

PRODUCERTOPIC="AuthUser"

consumer = KafkaConsumer(PRODUCERTOPIC, bootstrap_servers='localhost:29092')

while True:
    for message in consumer:
        ## Do something
        pass

