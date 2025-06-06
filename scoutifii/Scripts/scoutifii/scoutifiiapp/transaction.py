import json

from kafka import KafkaConsumer
from kafka import KafkaProducer

SCOUTIFII_KAFKA_TOPIC = "player_details"
SCOUTIFII_CONFIRMED_KAFKA_TOPIC = "player_confirmed"

consumer = KafkaConsumer(
	SCOUTIFII_KAFKA_TOPIC,
	bootstrap_servers = "localhost:29092",
	api_version = (2,0,2)
)
producer = KafkaProducer(
	bootstrap_servers="localhost:29092",
	api_version=(2,0,2)
)

print("Gonna start listening...")
while True:
	for message in consumer:
		print("Ongoing transaction...")
		consumed_message = json.loads(message.value.decode())
		print(consumed_message)
