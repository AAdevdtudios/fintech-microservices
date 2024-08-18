import json
from kafka import KafkaConsumer, KafkaProducer
import random

PRODUCERTOPIC="gateway"

producer = KafkaProducer(bootstrap_servers='localhost:29092')
consumer = KafkaConsumer(PRODUCERTOPIC, bootstrap_servers='localhost:29092')

while True:
    for message in consumer:
        print(message)
        # Consume the information to create a customer in the gateway
        # request(url, headers)
        rd = random.randint(10000000000,99999999999) # This would simulate customers number and save in the user table
        producer.send("AuthUser", value={}, )