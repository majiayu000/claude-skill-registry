---
name: kafka
description: "Manage Apache Kafka — topics, consumer groups, and produce/consume messages via the Confluent REST Proxy."
metadata: {"thinkfleetbot":{"emoji":"📨","requires":{"bins":["curl","jq"],"env":[]}}}
---

# Apache Kafka

Manage topics, consumer groups, and messages via the Confluent REST Proxy.

## List topics

```bash
curl -s "http://localhost:8082/topics" | jq '.[]'
```

## Get topic details

```bash
curl -s "http://localhost:8082/topics/TOPIC_NAME" | jq '{name, partitions: (.partitions | length), configs}'
```

## Produce message

```bash
curl -s -X POST -H "Content-Type: application/vnd.kafka.json.v2+json" \
  "http://localhost:8082/topics/TOPIC_NAME" \
  -d '{"records":[{"key":"key1","value":{"message":"hello"}}]}' | jq '.offsets[]'
```

## Create consumer

```bash
curl -s -X POST -H "Content-Type: application/vnd.kafka.v2+json" \
  "http://localhost:8082/consumers/my-group" \
  -d '{"name":"my-consumer","format":"json","auto.offset.reset":"earliest"}' | jq '{instance_id, base_uri}'
```

## Consume messages

```bash
curl -s -H "Accept: application/vnd.kafka.json.v2+json" \
  "http://localhost:8082/consumers/my-group/instances/my-consumer/records" | jq '.[] | {topic, key, value, offset}'
```

## Notes

- Requires Confluent REST Proxy running (default port 8082).
- Always confirm before producing messages.
