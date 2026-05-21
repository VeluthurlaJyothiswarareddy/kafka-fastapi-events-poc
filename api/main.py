from fastapi import FastAPI
from kafka import KafkaProducer
import json

app = FastAPI()

producer = KafkaProducer(
    bootstrap_servers = 'localhost:9092',
    value_serializer = lambda v: json.dumps(v).encode('utf-8')
)

@app.post("/users")
async def public_user_event(user: dict):
    producer.send('user_events', user)
    producer.flush()
    return {"status": "User event published", "data": user}  