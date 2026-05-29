---
name: rabbitmq
description: RabbitMQ message broker operations including export/import and message publishing.
---

# RabbitMQ

```bash
rabbitmqadmin -u admin -p ? export broker

rabbitmqadmin -u admin -p ? import broker

rabbitmqadmin -u admin -p admin publish \
    exchange=ex \
    routing_key=key \
    payload='{"a": "","b":{"c": ""}}' \
    properties='{"headers": {"id": "6D933FBEEA6D42E2AD0E1FA479A5DABA"}}'
```