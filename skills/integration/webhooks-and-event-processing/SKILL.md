---
name: webhooks-and-event-processing
description: Design webhook/event pipelines for Solana activity with idempotency, dedupe, retries, and ordering. Use when consuming RPC/webhook feeds.
---

# Webhooks and Event Processing

Role framing: You are an event pipeline engineer. Your goal is to process Solana webhooks/log streams reliably.

## Initial Assessment
- Event source (Helius, Dialect, custom listener)?
- Volume and burst expectations?
- Ordering requirements and acceptable lag?
- Downstream actions (alerts, DB writes, bots)?

## Core Principles
- Idempotency is mandatory; every event must be safe to replay.
- Separate ingestion from processing with a queue.
- Persist offsets/checkpoints; handle reorgs by slot/signature.
- Apply backpressure; avoid unbounded retries.

## Workflow
1) Intake
   - Receive webhook -> verify signature/auth -> enqueue message (include slot, sig, index).
2) Dedupe/idempotency
   - Use composite key (slot+sig+index); store processed marker.
3) Ordering
   - Process by slot then index; allow slight reordering but reconcile with checkpoints.
4) Retries
   - Exponential backoff with DLQ for poison messages; alert on DLQ growth.
5) Backfill + catchup
   - On startup, backfill missing slots; reconcile with queue state.
6) Monitoring
   - Metrics: queue depth, processing latency, failure rate; alerts.

## Templates / Playbooks
- Message schema: {slot, signature, index, type, payload, received_at}.
- Dedup key example: slot:signature:index in Redis/DB.
- DLQ policy: max retries 5 -> send to DLQ with reason.

## Common Failure Modes + Debugging
- Duplicate webhooks: dedupe with keys.
- Out-of-order slots causing state mismatch: enforce ordering or replay after lag window.
- Burst overload: autoscale workers; drop non-critical events or sample.
- Missing auth verification -> spoofed events; validate signatures.

## Quality Bar / Validation
- Idempotency proven by replay test.
- Queue size stable under expected load; DLQ monitored.
- Checkpointing recovers correctly after restart.

## Output Format
Provide pipeline design (sources, queue, workers), idempotency/dedupe method, retry/DLQ policy, and monitoring plan.

## Examples
- Simple: Low-volume alerts -> webhook to Cloudflare Worker -> queue -> Slack; dedupe by signature.
- Complex: High-volume log stream -> webhook to ingestion service -> Kafka/SQS -> processors updating DB and sending alerts; checkpoints by slot; replay script validated.