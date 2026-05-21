from kafka import KafkaConsumer
import json

consumer = KafkaConsumer(
    "user_events",
    bootstrap_servers="localhost:9092",
    auto_offset_reset="earliest",
    value_deserializer=lambda v: json.loads(v.decode("utf-8"))
)

print("Listening for events...")

for msg in consumer:
    data = msg.value
    print("📥 Received:", data)

    with open("events.log", "a") as f:
        f.write(json.dumps(data) + "\n")
