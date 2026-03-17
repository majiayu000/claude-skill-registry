---
name: distributed-systems
description: Distributed systems tools including NATS messaging, libp2p networking, and Temporal workflows
icon: 🌐
category: infrastructure
tools:
  - nats
  - nats-server
  - nats-cli
  - temporal
  - temporalite
---

# Distributed Systems Skills

## Overview

This skill provides expertise in distributed systems infrastructure for multi-robot coordination, microservices communication, and workflow orchestration.

## NATS - Cloud Native Messaging

NATS is a high-performance messaging system ideal for ROS2 multi-robot coordination.

### Installation (Nix)

```nix
# In flake.nix devshells or packages
{ pkgs, ... }:
{
  packages = with pkgs; [
    nats-server    # NATS server
    natscli        # CLI tools
  ];
}
```

### Installation (Pixi)

```bash
pixi add nats-py       # Python client
pixi add nats-server   # Server (if available)
```

### Quick Start

```bash
# Start NATS server
nats-server

# With JetStream (persistence)
nats-server --jetstream

# With config file
nats-server -c /path/to/nats.conf
```

### Configuration

```hcl
# nats.conf
port: 4222
http_port: 8222

jetstream {
  store_dir: "/var/lib/nats/jetstream"
  max_memory_store: 1G
  max_file_store: 10G
}

# Cluster configuration
cluster {
  name: "ros2-cluster"
  port: 6222
  routes: [
    "nats://robot1:6222"
    "nats://robot2:6222"
  ]
}
```

### Python Client

```python
import asyncio
import nats

async def main():
    # Connect to NATS
    nc = await nats.connect("nats://localhost:4222")

    # Publish message
    await nc.publish("robot.status", b"online")

    # Subscribe to topic
    async def message_handler(msg):
        print(f"Received: {msg.data.decode()}")

    sub = await nc.subscribe("robot.*", cb=message_handler)

    # Request-reply pattern
    response = await nc.request("robot.ping", b"hello", timeout=1.0)
    print(f"Response: {response.data.decode()}")

    await nc.close()

asyncio.run(main())
```

### ROS2 Integration Pattern

```python
import rclpy
from rclpy.node import Node
import nats
import asyncio
import json

class NATSBridgeNode(Node):
    """Bridge ROS2 topics to NATS subjects."""

    def __init__(self):
        super().__init__('nats_bridge')
        self.nc = None

    async def connect_nats(self):
        self.nc = await nats.connect("nats://localhost:4222")

    async def publish_to_nats(self, subject: str, data: dict):
        if self.nc:
            await self.nc.publish(subject, json.dumps(data).encode())

    async def subscribe_from_nats(self, subject: str, callback):
        if self.nc:
            await self.nc.subscribe(subject, cb=callback)
```

### JetStream (Persistence)

```python
import nats
from nats.js import JetStreamContext

async def setup_jetstream():
    nc = await nats.connect()
    js = nc.jetstream()

    # Create stream
    await js.add_stream(name="ROBOTS", subjects=["robot.*"])

    # Publish with acknowledgment
    ack = await js.publish("robot.telemetry", b"data")
    print(f"Published: seq={ack.seq}")

    # Consumer
    sub = await js.pull_subscribe("robot.*", "telemetry-consumer")
    msgs = await sub.fetch(10)
    for msg in msgs:
        await msg.ack()
```

### CLI Commands

```bash
# Server info
nats server info

# Publish message
nats pub robot.command "move forward"

# Subscribe
nats sub "robot.>"

# Request-reply
nats request robot.ping "hello"

# Stream management
nats stream add ROBOTS --subjects "robot.*"
nats stream info ROBOTS
nats consumer add ROBOTS telemetry
```

## Temporal - Workflow Orchestration

Temporal provides durable workflow execution for complex robotics tasks.

### Installation

```nix
{ pkgs, ... }:
{
  packages = with pkgs; [
    temporal-cli   # CLI tools
    # temporalite  # Local development server
  ];
}
```

### Quick Start

```bash
# Start local server
temporalite start --namespace default

# Or with Docker
docker run -d --name temporal \
  -p 7233:7233 -p 8233:8233 \
  temporalio/auto-setup:latest
```

### Python Workflow

```python
from temporalio import activity, workflow
from temporalio.client import Client
from temporalio.worker import Worker
from datetime import timedelta

@activity.defn
async def navigate_to_waypoint(waypoint: dict) -> bool:
    """Activity: Navigate robot to waypoint."""
    # ROS2 navigation logic here
    return True

@activity.defn
async def pick_object(object_id: str) -> bool:
    """Activity: Pick up an object."""
    return True

@workflow.defn
class DeliveryWorkflow:
    """Durable workflow for robot delivery task."""

    @workflow.run
    async def run(self, delivery_request: dict) -> str:
        # Navigate to pickup
        await workflow.execute_activity(
            navigate_to_waypoint,
            delivery_request["pickup_location"],
            start_to_close_timeout=timedelta(minutes=5)
        )

        # Pick up item
        await workflow.execute_activity(
            pick_object,
            delivery_request["object_id"],
            start_to_close_timeout=timedelta(minutes=2)
        )

        # Navigate to delivery
        await workflow.execute_activity(
            navigate_to_waypoint,
            delivery_request["delivery_location"],
            start_to_close_timeout=timedelta(minutes=5)
        )

        return "delivered"

async def main():
    client = await Client.connect("localhost:7233")

    # Start workflow
    handle = await client.start_workflow(
        DeliveryWorkflow.run,
        {"pickup_location": {...}, "delivery_location": {...}},
        id="delivery-001",
        task_queue="robot-tasks"
    )

    result = await handle.result()
    print(f"Delivery result: {result}")
```

## Architecture Patterns

### Multi-Robot Coordination

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   Robot 1   │     │   Robot 2   │     │   Robot 3   │
│   (ROS2)    │     │   (ROS2)    │     │   (ROS2)    │
└──────┬──────┘     └──────┬──────┘     └──────┬──────┘
       │                   │                   │
       └───────────────────┼───────────────────┘
                           │
                    ┌──────┴──────┐
                    │ NATS Cluster│
                    │  (JetStream)│
                    └──────┬──────┘
                           │
              ┌────────────┼────────────┐
              │            │            │
       ┌──────┴──────┐  ┌──┴───┐  ┌────┴─────┐
       │ Coordinator │  │ Fleet │  │ Telemetry│
       │   Service   │  │ Mgmt  │  │ Collector│
       └─────────────┘  └──────┘  └──────────┘
```

### Event-Driven Microservices

```
┌─────────────────────────────────────────────────────┐
│                   NATS Subjects                      │
├───────────────┬─────────────────┬───────────────────┤
│ robot.status  │ robot.telemetry │ robot.command     │
│ task.created  │ task.completed  │ task.failed       │
│ alert.warning │ alert.critical  │ alert.resolved    │
└───────────────┴─────────────────┴───────────────────┘
```

## Best Practices

1. **Use JetStream** for messages that need persistence or replay
2. **Subject naming**: Use dot-separated hierarchical names (`robot.{id}.{type}`)
3. **Cluster for HA**: Run 3+ NATS servers in production
4. **Workflows for durability**: Use Temporal for long-running, recoverable tasks
5. **Monitor with Prometheus**: Both NATS and Temporal export metrics

## Related Skills

- [ROS2 Development](../ros2-development/SKILL.md) - ROS2 integration
- [DevOps](../devops/SKILL.md) - Deployment and CI/CD
- [Observability](../observability/SKILL.md) - Monitoring and metrics
