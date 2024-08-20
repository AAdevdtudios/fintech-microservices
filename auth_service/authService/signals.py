from django.db.models.signals import post_save
from django.dispatch import receiver
import json
from authService.schemas import KafkaMessageModel
from .models import Account
# from extras.authKafka import producer 
from kafka import KafkaProducer

producer = KafkaProducer(bootstrap_servers='localhost:9092',value_serializer=lambda v: json.dumps(v).encode('utf-8'))
@receiver(post_save, sender=Account)
def send_kafka_message_on_create(sender, instance, created, **kwargs):
    if created:
        try:
            print("I ran o ")
            user = KafkaMessageModel(
                actions="Creating-Account",
                data={
                    "email": instance.email,
                    "firstname": instance.first_name,
                    "lastname": instance.last_name,
                    "phone_number": instance.phone_number,
                }
            )
            producer.send("Gateway",value=user.model_dump_json())
        except Exception as e:
            print(f"{e}")