---
name: queue-management
description: Standards for DLQs (Dead Letter Queues), Idempotency, and Retry policies.
role: eng-backend, ops-sre
triggers:
  - queue
  - kafka
  - rabbitmq
  - sqs
  - dlq
  - dead letter
  - idempotency
  - retry
---

# queue-management Skill

Async messaging is powerful but dangerous. Messages must never be lost.

## 1. Dead Letter Queues (DLQ)
- **Rule**: Every consumer MUST have a configured DLQ.
- **Behavior**: If a message fails processing N times (Poison Pill), move it to DLQ. Alert `ops-sre`.
- **Replay**: Must have a mechanism to replay messages from DLQ after bug fix.

## 2. Idempotency
- **Rule**: All consumers `handle(msg)` must be idempotent.
- **Pattern**:
  1. Check `processed_messages` table for `msg.id`.
  2. If found, ack and ignore.
  3. If not, process transactionally.
  4. Save `msg.id` to `processed_messages`.

## 3. At-Least-Once Delivery
- Assume you will receive duplicates. Network acks fail. Design for it.

## 4. Ordering
- **Kafka**: Ordering is only guaranteed *within a partition*.
- **SQS FIFO**: Guaranteed but lower throughput.
- **Best Practice**: Don't rely on global ordering if possible. Use state machines that accept events in any order (e.g., "OrderShipped" before "OrderPaid" -> Store in "Pending" state).

## 5. Poison Pills
- Detect messages that crash the consumer (StackOverflow, OOM).
- Reject them immediately to DLQ to prevent blocking the partition.
