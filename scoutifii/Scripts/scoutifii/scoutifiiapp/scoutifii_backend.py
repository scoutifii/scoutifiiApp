import json
import time

from kafka import KafkaProducer, producer

SCOUTIFII_KAFKA_TOPIC ="player_details"
POST_LIMIT = 15

producer = KafkaProducer(
	bootstrap_servers="localhost:29092",
	api_version=(2,0,2)
)

print("will generate one unique detail every 10 seconds")

for i in range(1, POST_LIMIT):
	data = {
		"post_id": i,
		"user_id": f"user_{i}",
		"total_cost": i*2,
		"items": "player, agent, manager"
	}

	producer.send(
		SCOUTIFII_KAFKA_TOPIC,
		json.dumps(data).encode("utf-8")
	)
	
	print(f"Done sending...{i}")
	time.sleep(10)