# kafka-fastapi-events-poc

A lightweight Kafka proof-of-concept that includes:
- a FastAPI producer endpoint at `POST /users`
- a Kafka topic named `user_events`
- a standalone Kafka consumer script that reads events and appends them to `events.log`
- Docker Compose configuration to start Zookeeper and Kafka locally

## Contents

- `api/main.py` - FastAPI application that publishes user events to Kafka
- `consumer.py` - Kafka consumer that listens on `user_events` and logs incoming messages
- `docker-compose.yml` - local Kafka + Zookeeper stack for development
- `requirements.txt` - Python dependencies

## Prerequisites

- Python 3.9+ installed
- Docker and Docker Compose installed and available on your machine
- `jq` is optional for formatted JSON output when testing with `curl`

## Setup

1. Create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

2. Install Python dependencies:

```bash
pip install -r requirements.txt
```

3. Start Kafka and Zookeeper:

```bash
docker compose up -d
```

4. Confirm Kafka is running by checking Docker containers:

```bash
docker compose ps
```

## Run the API

Start the FastAPI app:

```bash
uvicorn api.main:app --reload --host 0.0.0.0 --port 8000
```

The API listens on `http://localhost:8000`.

## Publish a test event

Use `curl` to send a user event to the producer endpoint:

```bash
curl -s -X POST http://localhost:8000/users \
  -H "Content-Type: application/json" \
  -d '{"product_id":"P123","quantity":3,"user_id":"U777"}' | jq
```

Expected response:

```json
{
  "status": "User event published",
  "data": {
    "product_id": "P123",
    "quantity": 3,
    "user_id": "U777"
  }
}
```

## Run the consumer

In a separate terminal, activate the same virtual environment and run:

```bash
python consumer.py
```

The consumer will print events as they arrive and append them to `events.log`.

## Notes

- The Kafka producer uses `localhost:9092` and publishes to the topic `user_events`.
- The consumer also reads from `localhost:9092` and uses `auto_offset_reset='earliest'`.
- If you restart the consumer, it will re-read messages from the beginning of the topic.

## Cleanup

Stop the local stack when finished:

```bash
docker compose down
```

## Troubleshooting

- If Kafka cannot connect, verify the Docker Compose stack is running.
- If the API cannot produce messages, ensure Kafka is accessible at `localhost:9092`.
- If `events.log` is not created, confirm the consumer process is running and receiving messages.
