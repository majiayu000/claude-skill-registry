---
name: discover-protocols
description: Automatically discover protocol skills when working with HTTP, TCP, UDP, QUIC, and network protocols
---

# Protocols Skills Discovery

Provides automatic access to comprehensive network protocol skills.

## When This Skill Activates

This skill auto-activates when you're working with:
- HTTP, HTTP/2, HTTP/3
- TCP, UDP, QUIC
- network protocols
- protocol debugging
- protocol selection
- network communication
- web protocols
- transport layer
- application layer protocols

## Available Skills

### Quick Reference

The Protocols category contains 8 skills:

1. **grpc-implementation** - gRPC services with Protocol Buffers, streaming RPCs
2. **http2-multiplexing** - HTTP/2 binary protocol, multiplexing, server push, HPACK
3. **kafka-streams** - Apache Kafka stream processing and event streaming
4. **mqtt-messaging** - MQTT pub-sub messaging for IoT and real-time applications
5. **amqp-rabbitmq** - RabbitMQ and AMQP message broker implementation
6. **protobuf-schemas** - Protocol Buffers schema design, evolution, code generation
7. **tcp-optimization** - TCP performance optimization and tuning
8. **websocket-protocols** - WebSocket protocol implementation, scaling, production

### Load Full Category Details

For complete descriptions and workflows:

```bash
cat ~/.claude/skills/protocols/INDEX.md
```

This loads the full Protocols category index with:
- Detailed skill descriptions
- Usage triggers for each skill
- Common workflow combinations
- Cross-references to related skills

### Load Specific Skills

Load individual skills as needed:

```bash
cat ~/.claude/skills/protocols/grpc-implementation.md
cat ~/.claude/skills/protocols/http2-multiplexing.md
cat ~/.claude/skills/protocols/kafka-streams.md
cat ~/.claude/skills/protocols/mqtt-messaging.md
cat ~/.claude/skills/protocols/amqp-rabbitmq.md
cat ~/.claude/skills/protocols/protobuf-schemas.md
cat ~/.claude/skills/protocols/tcp-optimization.md
cat ~/.claude/skills/protocols/websocket-protocols.md
```

## Common Workflows

### gRPC Microservices
```bash
# Schema design → gRPC implementation → Optimization
cat ~/.claude/skills/protocols/protobuf-schemas.md
cat ~/.claude/skills/protocols/grpc-implementation.md
cat ~/.claude/skills/protocols/http2-multiplexing.md
cat ~/.claude/skills/protocols/tcp-optimization.md
```

### Event Streaming Pipeline
```bash
# Kafka setup → Stream processing → Schema evolution
cat ~/.claude/skills/protocols/kafka-streams.md
cat ~/.claude/skills/protocols/protobuf-schemas.md
```

### Real-time IoT Platform
```bash
# MQTT for devices → RabbitMQ for backend → WebSockets for web
cat ~/.claude/skills/protocols/mqtt-messaging.md
cat ~/.claude/skills/protocols/amqp-rabbitmq.md
cat ~/.claude/skills/protocols/websocket-protocols.md
```

### High-Performance Web Application
```bash
# HTTP/2 optimization → WebSocket for real-time → TCP tuning
cat ~/.claude/skills/protocols/http2-multiplexing.md
cat ~/.claude/skills/protocols/websocket-protocols.md
cat ~/.claude/skills/protocols/tcp-optimization.md
```

## Progressive Loading

This gateway skill enables progressive loading:
- **Level 1**: Gateway loads automatically (you're here now)
- **Level 2**: Load category INDEX.md for full overview
- **Level 3**: Load specific skills as needed

## Usage Instructions

1. **Auto-activation**: This skill loads automatically when Claude Code detects protocol work
2. **Browse skills**: Run `cat ~/.claude/skills/protocols/INDEX.md` for full category overview
3. **Load specific skills**: Use bash commands above to load individual skills

---

**Next Steps**: Run `cat ~/.claude/skills/protocols/INDEX.md` to see full category details.
