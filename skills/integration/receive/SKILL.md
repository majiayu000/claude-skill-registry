---
name: receive
description: Ingest and parse incoming messages, events, or signals into structured form. Use when processing external inputs, handling API responses, parsing webhook payloads, or ingesting sensor data.
argument-hint: "[input_source] [expected_format json|xml|text|binary] [validation_schema]"
disable-model-invocation: false
user-invocable: true
allowed-tools: Read, Grep
context: fork
agent: explore
---

## Intent

Execute **receive** to ingest incoming data from external sources and parse it into a structured, validated form for downstream processing.

**Success criteria:**
- Input data is successfully ingested from the source
- Data is parsed according to expected format
- Validation against schema (if provided) passes or errors are captured
- Structured output is ready for downstream capabilities
- Malformed or unexpected data is handled gracefully

**Compatible schemas:**
- `schemas/output_schema.yaml`
- `reference/event_schema.yaml`

## Inputs

| Parameter | Required | Type | Description |
|-----------|----------|------|-------------|
| `input_source` | Yes | string\|object | Source of incoming data: file path, URL, inline data, or stream identifier |
| `expected_format` | No | enum | Expected data format: `json`, `xml`, `yaml`, `text`, `csv`, `binary`. Default: auto-detect |
| `validation_schema` | No | string | Schema to validate parsed data against |
| `encoding` | No | string | Character encoding. Default: `utf-8` |
| `max_size` | No | string | Maximum input size to accept (e.g., "10MB"). Default: "100MB" |

## Procedure

1) **Identify input source**: Determine where data is coming from
   - File path: Read from local filesystem
   - URL: Fetch from network endpoint
   - Inline: Extract from request payload
   - Stream: Connect to data stream

2) **Validate source accessibility**: Verify source can be read
   - Check file exists and is readable
   - Verify URL is reachable
   - Confirm stream is connected
   - Check size does not exceed max_size

3) **Detect format**: Identify data format if not specified
   - Check content-type headers or file extension
   - Inspect data prefix for format signatures
   - Fall back to text if ambiguous

4) **Parse input**: Transform raw data into structured form
   - JSON: Parse to object/array using safe parser
   - XML: Parse to DOM or object representation
   - YAML: Parse to object using safe loader
   - CSV: Parse to array of records
   - Text: Split into lines/tokens as appropriate
   - Binary: Extract structured fields per schema

5) **Validate structure**: Check parsed data against schema
   - If validation_schema provided: validate and collect errors
   - If no schema: perform basic sanity checks
   - Flag missing required fields
   - Flag type mismatches

6) **Extract events/messages**: Identify discrete units in the data
   - Single message: wrap as single-element array
   - Batch: extract individual events
   - Stream chunk: identify complete messages

7) **Ground evidence**: Record provenance for ingested data
   - Source URI or path
   - Timestamp of receipt
   - Size and checksum if applicable

8) **Format output**: Structure results according to output contract

## Output Contract

Return a structured object:

```yaml
received:
  source: string  # Where data came from
  source_type: file | url | inline | stream
  timestamp: string  # ISO timestamp of receipt
  format_detected: json | xml | yaml | csv | text | binary
  size_bytes: integer  # Size of received data
  encoding: string  # Character encoding used
messages:
  - id: string  # Unique message identifier
    type: string | null  # Event/message type if identifiable
    payload: object  # Parsed message content
    timestamp: string | null  # Message timestamp if present
    metadata: object | null  # Additional message metadata
parsed_count: integer  # Number of messages/events parsed
validation:
  schema_ref: string | null  # Schema used for validation
  valid: boolean  # Whether all messages passed validation
  errors:
    - message_id: string
      field: string
      error: string
      severity: error | warning
conflicts:
  - type: string  # Type of conflict/anomaly
    description: string
    affected_messages: array[string]
confidence: number  # 0.0-1.0 based on parse success and validation
evidence_anchors: array[string]  # Source references
assumptions: array[string]  # Explicit assumptions
```

### Field Definitions

| Field | Type | Description |
|-------|------|-------------|
| `received.source` | string | Origin of the data |
| `messages` | array[object] | Parsed messages/events |
| `validation.valid` | boolean | Whether validation passed |
| `validation.errors` | array | Validation error details |
| `conflicts` | array | Anomalies or conflicts in data |
| `confidence` | number | Lower if parse errors or validation failures |

## Examples

### Example 1: Receiving JSON API Response

**Input:**
```yaml
input_source: "https://api.example.com/events"
expected_format: json
validation_schema: "schemas/event_v2.yaml"
```

**Output:**
```yaml
received:
  source: "https://api.example.com/events"
  source_type: url
  timestamp: "2024-01-16T12:00:00Z"
  format_detected: json
  size_bytes: 4256
  encoding: "utf-8"
messages:
  - id: "evt_001"
    type: "order.created"
    payload:
      order_id: "ORD-12345"
      customer_id: "CUST-789"
      total: 129.99
      currency: "USD"
    timestamp: "2024-01-16T11:58:30Z"
    metadata:
      source_system: "ecommerce"
      version: "2.1"
  - id: "evt_002"
    type: "order.paid"
    payload:
      order_id: "ORD-12345"
      payment_method: "credit_card"
      transaction_id: "TXN-ABC123"
    timestamp: "2024-01-16T11:59:00Z"
    metadata:
      source_system: "payments"
      version: "1.0"
parsed_count: 2
validation:
  schema_ref: "schemas/event_v2.yaml"
  valid: true
  errors: []
conflicts: []
confidence: 1.0
evidence_anchors:
  - "url:https://api.example.com/events"
  - "schema:schemas/event_v2.yaml"
assumptions:
  - "API response is authoritative source of truth"
  - "Timestamps are in UTC"
```

**Evidence pattern:** Source URL recorded; schema validation confirmed; each message given unique ID.

---

### Example 2: Receiving Malformed Data

**Input:**
```yaml
input_source: "/var/log/sensor_data.json"
expected_format: json
validation_schema: "schemas/sensor_reading.yaml"
```

**Output:**
```yaml
received:
  source: "/var/log/sensor_data.json"
  source_type: file
  timestamp: "2024-01-16T14:30:00Z"
  format_detected: json
  size_bytes: 1024
  encoding: "utf-8"
messages:
  - id: "msg_001"
    type: "sensor_reading"
    payload:
      sensor_id: "SENS-001"
      temperature: 23.5
      humidity: null
      timestamp: "2024-01-16T14:29:00Z"
    timestamp: "2024-01-16T14:29:00Z"
    metadata: null
  - id: "msg_002"
    type: "sensor_reading"
    payload:
      sensor_id: "SENS-002"
      temperature: "ERROR"
      humidity: 65.2
      timestamp: null
    timestamp: null
    metadata: null
parsed_count: 2
validation:
  schema_ref: "schemas/sensor_reading.yaml"
  valid: false
  errors:
    - message_id: "msg_001"
      field: "humidity"
      error: "Required field is null"
      severity: warning
    - message_id: "msg_002"
      field: "temperature"
      error: "Expected number, got string 'ERROR'"
      severity: error
    - message_id: "msg_002"
      field: "timestamp"
      error: "Required field is null"
      severity: error
conflicts:
  - type: "data_quality"
    description: "Sensor SENS-002 reporting error state instead of reading"
    affected_messages: ["msg_002"]
confidence: 0.5
evidence_anchors:
  - "file:/var/log/sensor_data.json"
  - "schema:schemas/sensor_reading.yaml"
assumptions:
  - "File contains most recent sensor batch"
  - "'ERROR' string indicates sensor malfunction"
next_actions:
  - "Investigate sensor SENS-002 for malfunction"
  - "Check why SENS-001 humidity is null"
```

---

### Example 3: Receiving Webhook Payload

**Input:**
```yaml
input_source:
  inline: |
    <?xml version="1.0"?>
    <notification type="alert">
      <severity>high</severity>
      <message>CPU usage exceeded threshold</message>
      <host>server-01</host>
    </notification>
expected_format: xml
```

**Output:**
```yaml
received:
  source: "inline"
  source_type: inline
  timestamp: "2024-01-16T15:00:00Z"
  format_detected: xml
  size_bytes: 198
  encoding: "utf-8"
messages:
  - id: "msg_001"
    type: "notification.alert"
    payload:
      severity: "high"
      message: "CPU usage exceeded threshold"
      host: "server-01"
    timestamp: null
    metadata:
      xml_root: "notification"
      xml_attributes:
        type: "alert"
parsed_count: 1
validation:
  schema_ref: null
  valid: true
  errors: []
conflicts: []
confidence: 0.95
evidence_anchors:
  - "inline:xml:notification"
assumptions:
  - "XML is well-formed and complete"
  - "No schema validation requested"
```

## Verification

- [ ] Source is accessible and data retrieved successfully
- [ ] Format detection matches actual data format
- [ ] All messages parsed without critical errors
- [ ] Validation errors logged with actionable detail
- [ ] confidence reflects parse success rate

**Verification tools:** Read (to access file sources), Grep (to search for patterns in text data)

## Safety Constraints

- `mutation`: false
- `requires_checkpoint`: false
- `requires_approval`: false
- `risk`: low

**Capability-specific rules:**
- Do not execute or run arbitrary code from received data
- Use safe parsing methods (JSON.parse, safe YAML loader)
- Validate max_size before loading large files into memory
- Sanitize file paths to prevent directory traversal
- Do not store credentials or secrets found in payloads
- Log but do not propagate malformed/suspicious data without flagging

## Composition Patterns

**Commonly follows:**
- External triggers (webhooks, API calls, file drops)
- `schedule` - Scheduled data ingestion

**Commonly precedes:**
- `transform` - Normalize received data for processing
- `validate` - Deeper validation beyond schema
- `integrate` - Merge received data with existing state
- `synchronize` - Combine with other data sources
- `recall` - Check received data against prior context

**Anti-patterns:**
- Never process received data without validation
- Never trust received data for authentication decisions without verification
- Avoid processing unbounded streams without size limits

**Workflow references:**
- See `reference/composition_patterns.md#digital-twin-sync-loop` for receive as entry point
- First step in most data ingestion pipelines
