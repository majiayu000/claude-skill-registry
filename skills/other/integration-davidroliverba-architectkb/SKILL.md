---
context: fork
---

# /integration

Create an Integration note documenting how two systems exchange data, including pattern, protocol, frequency, SLA, and error handling.

## Usage

```
/integration <source-system> <target-system>
/integration SAP DataPlatform
/integration DataPlatform Snowflake --pattern batch
/integration "System - SAP S/4HANA" "System - DataPlatform" --frequency hourly
```

## Instructions

Creates comprehensive Integration notes linking System notes and documenting connection characteristics.

### Phase 1: Parse Input & Validate Systems

1. Extract source and target system names
2. Search vault for both systems:
   ```
   node scripts/graph-query.js --type System --search "<source>"
   node scripts/graph-query.js --type System --search "<target>"
   ```
3. If systems not found:
   - "[[System - {{name}}]] not found. Create it first? (Y/n)"
   - Offer to create System notes before Integration
4. If system already integrates, show existing:
   - "Found: [[Integration - SAP to DataPlatform]]. Edit instead? (Y/n)"

### Phase 2: Essential Information

Gather required fields:

```
Creating Integration: {{source}} → {{target}}

1️⃣ Integration Pattern:
   - api-sync (REST/GraphQL synchronous)
   - event-streaming (Kafka/Pub-Sub asynchronous)
   - batch-etl (scheduled bulk data transfer)
   - message-queue (queued messages with processing)
   - file-transfer (SFTP/S3 file exchange)
   - database-replication (direct DB sync)
   Default: api-sync
   User input: [selection]

2️⃣ Protocol:
   (Based on pattern selection, suggest defaults)
   - For api-sync: rest, graphql, soap, odata
   - For event-streaming: kafka, rabbitmq, pubsub
   - For batch-etl: s3, sftp, sql
   Default: [depends on pattern]
   User input: [selection]

3️⃣ Frequency:
   - real-time (< 1 second latency)
   - near-real-time (< 5 minutes)
   - hourly
   - daily
   - weekly
   - on-demand
   Default: daily
   User input: [selection]

4️⃣ Direction:
   - one-way (source → target only)
   - bidirectional (source ↔ target)
   Default: one-way
   User input: [selection]

5️⃣ Criticality:
   - critical (business stops if fails)
   - high (significant impact)
   - medium (moderate impact)
   - low (minimal impact)
   Default: medium
   User input: [selection]
```

### Phase 3: SLA & Performance (Brief)

```
6️⃣ Availability SLA (%):
   Default: 99.5
   User input: [number 90-99.99]

7️⃣ Maximum acceptable latency:
   For real-time: < 100ms
   For batch: < 5 minutes
   For daily: no constraint
   Default: [based on frequency]
   User input: [optional override]

8️⃣ Data volume (records/second or volume/day):
   Default: null
   User input: [e.g., "500 rec/sec" or "2.5GB/day"]
```

### Phase 4: Middleware & Infrastructure

```
9️⃣ Does this use middleware?
   (Search for integration platforms)
   - [[System - Kong]] (API Gateway)
   - [[System - Cloud Platform Integration Suite]]
   - [[System - Apache Kafka]]
   - None (direct connection)
   Default: None
   User input: [selection]
```

### Phase 5: Error Handling (Optional)

Ask: "Add error handling details? (Y/n)"

If YES:
```
- Retry strategy: exponential-backoff | linear-backoff | none
- Max retries: 3
- Dead letter queue: enabled | disabled
- Idempotent: yes | no
```

### Phase 6: Generate Frontmatter

```yaml
type: Integration
title: "{{source}} → {{target}}"

integrationId: "INT-{{source|upper}}-{{target|upper}}-001"
status: active
version: "1.0.0"

sourceSystem: "[[System - {{source}}]]"
targetSystem: "[[System - {{target}}]]"

pattern: {{pattern}}
protocol: [{{protocol}}]
direction: {{direction}}
criticality: {{criticality}}
frequency: {{frequency}}
latency-sla: "{{latency}}"

middleware: {{middleware|null}}

retryPolicy: exponential-backoff
maxRetries: 3
deadLetterQueue: {{dlq|true}}
idempotency: {{idempotency|true}}

slo: "{{sla}}%"

confidence: medium
freshness: current
verified: false

created: 2026-01-14
modified: 2026-01-14
tags: [type/integration, pattern/{{pattern}}, {{source|lower}}-{{target|lower}}]
```

### Phase 7: Generate Body Content

1. **Overview**: What data flows and why
2. **Data Flow Sequence Diagram**: Mermaid sequence showing flow
3. **Integration Properties Table**: Quick reference
4. **Middleware Details**: If applicable
5. **Protocol & Connection Details**: Endpoints, auth, encryption
6. **Error Handling**: Retry logic, DLQ, monitoring
7. **Monitoring & SLA**: Health checks, alerts, dashboards
8. **Related Architecture**: Link to ADRs and Architectures

### Phase 8: Update Related Systems

Automatically update both System notes:
1. Add this Integration to source System's `connectsTo`
2. Add this Integration to target System's `connectedFrom`
3. Suggest: "Update {{source}} and {{target}} System notes? (Y/n)"

### Phase 9: Create File

**Filename**: `Integration - {{source}} to {{target}}.md`

**Location**: Vault root

**Output**:
```
✅ Created: Integration - {{source}} to {{target}}.md

Links updated:
- [[System - {{source}}]] → connectsTo added
- [[System - {{target}}]] → connectedFrom added

Next steps:
1. Add data sources: /datasource <name>
2. Generate diagram: /dataflow-diagram [[Project - <name>]]
3. Add to architecture: /architecture --relate-integration <name>
```

## Example Interaction

```
User: /integration SAP DataPlatform

Skill: Searching for systems...
Found: [[System - SAP S/4HANA]] and [[System - DataPlatform]]

Integration Pattern (default: api-sync):
1. api-sync (REST/GraphQL synchronous)
2. event-streaming (Kafka publish/subscribe)
3. batch-etl (scheduled bulk transfer)
4. message-queue (queued messages)
> 2

Protocol (default: kafka):
> kafka

Frequency (default: daily):
> real-time

Direction (default: one-way):
> one-way

Criticality (default: medium):
> high

Availability SLA (default: 99.5):
> 99.95

Latency (default: < 1 second for real-time):
> < 100ms

Data volume:
> 500 records/second

Middleware:
> None

✅ Created: Integration - SAP to DataPlatform.md

Updated:
- [[System - SAP S/4HANA]] added to connectsTo
- [[System - DataPlatform]] added to connectedFrom

Next: /datasource SAP Invoices
```
