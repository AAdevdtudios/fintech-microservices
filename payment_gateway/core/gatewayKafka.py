import json
from kafka import KafkaConsumer, KafkaProducer
import random

PRODUCERTOPIC="Gateway"

# producer = KafkaProducer(bootstrap_servers='localhost:29092')
consumer = KafkaConsumer(PRODUCERTOPIC, bootstrap_servers='localhost:9092',value_deserializer=lambda v: json.loads(v.decode("utf-8")))
print("Ready to listen to server")
while True:
    for message in consumer:
        print(message.value)
        # Consume the information to create a customer in the gateway
        # request(url, headers)
        # producer.send("AuthUser", value={}, )