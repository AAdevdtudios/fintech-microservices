from kafka import KafkaConsumer, KafkaProducer

PRODUCERTOPIC="AuthUser"

producer = KafkaProducer(bootstrap_servers='localhost:29092')
consumer = KafkaConsumer(PRODUCERTOPIC, bootstrap_servers='localhost:29092')

while True:
    for message in consumer:
        ## Do something
        pass

