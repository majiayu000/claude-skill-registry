---
name: Audit Trails for Agents
description: Comprehensive guide to implementing audit trails and logging for AI agents including tracing, observability, compliance, and debugging
---

# Audit Trails for Agents

## What are Audit Trails?

**Audit Trail:** Complete record of all agent actions, decisions, and interactions for accountability, debugging, and compliance.

### Why Audit Trails Matter
```
Debugging: "Why did agent do X?"
Compliance: "What data did agent access?"
Security: "Did agent misuse tools?"
Improvement: "Where does agent fail?"
Trust: "Can we explain agent behavior?"
```

---

## What to Log

### Agent Inputs
```json
{
  "timestamp": "2024-01-16T12:00:00Z",
  "session_id": "sess_abc123",
  "user_id": "user_456",
  "input": {
    "type": "user_message",
    "content": "Book a flight to Paris",
    "metadata": {
      "source": "web_chat",
      "ip_address": "192.168.1.1"
    }
  }
}
```

### Agent Reasoning
```json
{
  "timestamp": "2024-01-16T12:00:01Z",
  "session_id": "sess_abc123",
  "reasoning": {
    "thought": "User wants to book a flight. I need to search for flights first.",
    "plan": [
      "Search for flights to Paris",
      "Present options to user",
      "Book selected flight"
    ],
    "confidence": 0.95
  }
}
```

### Tool Calls
```json
{
  "timestamp": "2024-01-16T12:00:02Z",
  "session_id": "sess_abc123",
  "tool_call": {
    "tool_name": "search_flights",
    "parameters": {
      "destination": "Paris",
      "departure_date": "2024-02-01",
      "return_date": "2024-02-08"
    },
    "result": {
      "status": "success",
      "flights": [...]
    },
    "duration_ms": 1250
  }
}
```

### Agent Outputs
```json
{
  "timestamp": "2024-01-16T12:00:03Z",
  "session_id": "sess_abc123",
  "output": {
    "type": "agent_response",
    "content": "I found 5 flights to Paris. Here are the best options...",
    "metadata": {
      "tokens_used": 150,
      "model": "gpt-4",
      "cost": 0.0045
    }
  }
}
```

### Errors and Exceptions
```json
{
  "timestamp": "2024-01-16T12:00:04Z",
  "session_id": "sess_abc123",
  "error": {
    "type": "ToolExecutionError",
    "tool_name": "book_flight",
    "message": "Payment API timeout",
    "stack_trace": "...",
    "recovery_action": "Retry with exponential backoff"
  }
}
```

---

## Logging Levels

### Trace (Most Detailed)
```python
# Every LLM call, every tool call, every decision
logger.trace("Agent thinking: Should I use search_flights or get_flight_status?")
```

### Debug
```python
# Important decisions and intermediate results
logger.debug(f"Selected tool: search_flights with params: {params}")
```

### Info
```python
# High-level actions
logger.info(f"Agent completed task: book_flight for user {user_id}")
```

### Warning
```python
# Potential issues
logger.warning(f"Tool call took {duration}ms (expected <1000ms)")
```

### Error
```python
# Failures
logger.error(f"Tool execution failed: {error}")
```

---

## Implementation

### Basic Logging
```python
import logging
import json
from datetime import datetime

class AgentLogger:
    def __init__(self, session_id):
        self.session_id = session_id
        self.logger = logging.getLogger(f"agent.{session_id}")
    
    def log_input(self, user_id, message):
        self.logger.info(json.dumps({
            "timestamp": datetime.utcnow().isoformat(),
            "session_id": self.session_id,
            "user_id": user_id,
            "type": "input",
            "message": message
        }))
    
    def log_tool_call(self, tool_name, params, result, duration_ms):
        self.logger.info(json.dumps({
            "timestamp": datetime.utcnow().isoformat(),
            "session_id": self.session_id,
            "type": "tool_call",
            "tool_name": tool_name,
            "parameters": params,
            "result": result,
            "duration_ms": duration_ms
        }))
    
    def log_output(self, response, tokens_used, cost):
        self.logger.info(json.dumps({
            "timestamp": datetime.utcnow().isoformat(),
            "session_id": self.session_id,
            "type": "output",
            "response": response,
            "tokens_used": tokens_used,
            "cost": cost
        }))

# Usage
logger = AgentLogger(session_id="sess_abc123")
logger.log_input(user_id="user_456", message="Book a flight")
logger.log_tool_call("search_flights", {...}, {...}, 1250)
logger.log_output("I found 5 flights...", 150, 0.0045)
```

### Structured Logging (JSON)
```python
import structlog

# Configure structlog
structlog.configure(
    processors=[
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.JSONRenderer()
    ]
)

logger = structlog.get_logger()

# Log with structured data
logger.info(
    "tool_call",
    session_id="sess_abc123",
    tool_name="search_flights",
    parameters={"destination": "Paris"},
    duration_ms=1250
)
```

---

## Tracing

### OpenTelemetry
```python
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter

# Setup tracer
trace.set_tracer_provider(TracerProvider())
tracer = trace.get_tracer(__name__)

# Export to observability platform
otlp_exporter = OTLPSpanExporter(endpoint="http://localhost:4317")
span_processor = BatchSpanProcessor(otlp_exporter)
trace.get_tracer_provider().add_span_processor(span_processor)

# Trace agent execution
with tracer.start_as_current_span("agent_execution") as span:
    span.set_attribute("session_id", session_id)
    span.set_attribute("user_id", user_id)
    
    # Trace tool call
    with tracer.start_as_current_span("tool_call") as tool_span:
        tool_span.set_attribute("tool_name", "search_flights")
        result = search_flights(destination="Paris")
        tool_span.set_attribute("result_count", len(result))
```

### LangSmith (LangChain)
```python
from langchain.callbacks import LangChainTracer

# Setup tracer
tracer = LangChainTracer(
    project_name="my-agent",
    client=langsmith_client
)

# Run agent with tracing
agent.run(
    "Book a flight to Paris",
    callbacks=[tracer]
)

# View traces in LangSmith UI
# https://smith.langchain.com
```

---

## Storage

### Database (PostgreSQL)
```sql
CREATE TABLE agent_logs (
    id BIGSERIAL PRIMARY KEY,
    timestamp TIMESTAMPTZ NOT NULL,
    session_id VARCHAR(100) NOT NULL,
    user_id VARCHAR(100),
    log_type VARCHAR(50) NOT NULL,
    data JSONB NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_session_id ON agent_logs(session_id);
CREATE INDEX idx_user_id ON agent_logs(user_id);
CREATE INDEX idx_timestamp ON agent_logs(timestamp);
CREATE INDEX idx_log_type ON agent_logs(log_type);
```

```python
import psycopg2
import json

def log_to_db(session_id, user_id, log_type, data):
    conn = psycopg2.connect("postgresql://...")
    cursor = conn.cursor()
    
    cursor.execute("""
        INSERT INTO agent_logs (timestamp, session_id, user_id, log_type, data)
        VALUES (NOW(), %s, %s, %s, %s)
    """, (session_id, user_id, log_type, json.dumps(data)))
    
    conn.commit()
    cursor.close()
    conn.close()
```

### Object Storage (S3)
```python
import boto3
import json
from datetime import datetime

s3 = boto3.client('s3')

def log_to_s3(session_id, log_data):
    # Partition by date for efficient querying
    date = datetime.utcnow().strftime("%Y/%m/%d")
    key = f"agent-logs/{date}/{session_id}.jsonl"
    
    # Append to JSONL file
    s3.put_object(
        Bucket='my-agent-logs',
        Key=key,
        Body=json.dumps(log_data) + '\n',
        ContentType='application/x-ndjson'
    )
```

### Elasticsearch
```python
from elasticsearch import Elasticsearch

es = Elasticsearch(['http://localhost:9200'])

def log_to_elasticsearch(session_id, log_data):
    es.index(
        index='agent-logs',
        document={
            **log_data,
            'session_id': session_id,
            'timestamp': datetime.utcnow().isoformat()
        }
    )

# Query logs
results = es.search(
    index='agent-logs',
    body={
        'query': {
            'match': {'session_id': 'sess_abc123'}
        },
        'sort': [{'timestamp': 'asc'}]
    }
)
```

---

## Compliance

### GDPR Compliance
```python
# Log with PII redaction
def redact_pii(text):
    # Redact email
    text = re.sub(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', '[EMAIL]', text)
    
    # Redact phone
    text = re.sub(r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b', '[PHONE]', text)
    
    # Redact credit card
    text = re.sub(r'\b\d{4}[-\s]?\d{4}[-\s]?\d{4}[-\s]?\d{4}\b', '[CARD]', text)
    
    return text

logger.log_input(
    user_id=user_id,
    message=redact_pii(user_message)
)

# Right to be forgotten
def delete_user_logs(user_id):
    db.execute("DELETE FROM agent_logs WHERE user_id = %s", (user_id,))
```

### SOC 2 Compliance
```python
# Immutable logs (append-only)
# Encrypted at rest
# Access controls (who can view logs)
# Retention policy (delete after X days)

# Audit log access
def log_access(viewer_id, session_id):
    audit_logger.info(f"User {viewer_id} accessed logs for session {session_id}")
```

---

## Querying and Analysis

### Query by Session
```python
def get_session_logs(session_id):
    return db.query("""
        SELECT * FROM agent_logs
        WHERE session_id = %s
        ORDER BY timestamp ASC
    """, (session_id,))
```

### Query by User
```python
def get_user_logs(user_id, start_date, end_date):
    return db.query("""
        SELECT * FROM agent_logs
        WHERE user_id = %s
          AND timestamp BETWEEN %s AND %s
        ORDER BY timestamp DESC
    """, (user_id, start_date, end_date))
```

### Aggregate Metrics
```python
# Tool usage stats
def get_tool_usage_stats():
    return db.query("""
        SELECT
            data->>'tool_name' as tool_name,
            COUNT(*) as call_count,
            AVG((data->>'duration_ms')::int) as avg_duration_ms
        FROM agent_logs
        WHERE log_type = 'tool_call'
        GROUP BY data->>'tool_name'
        ORDER BY call_count DESC
    """)

# Error rate
def get_error_rate():
    return db.query("""
        SELECT
            DATE(timestamp) as date,
            COUNT(*) FILTER (WHERE log_type = 'error') as error_count,
            COUNT(*) as total_count,
            (COUNT(*) FILTER (WHERE log_type = 'error')::float / COUNT(*)) as error_rate
        FROM agent_logs
        GROUP BY DATE(timestamp)
        ORDER BY date DESC
    """)
```

---

## Observability Platforms

### Datadog
```python
from datadog import initialize, statsd

initialize(api_key='...', app_key='...')

# Log metrics
statsd.increment('agent.tool_call', tags=[f'tool:{tool_name}'])
statsd.histogram('agent.tool_duration', duration_ms, tags=[f'tool:{tool_name}'])

# Log events
statsd.event(
    title='Agent Error',
    text=f'Tool {tool_name} failed: {error}',
    alert_type='error'
)
```

### New Relic
```python
import newrelic.agent

# Trace agent execution
@newrelic.agent.background_task()
def run_agent(user_input):
    # Agent logic
    pass

# Custom metrics
newrelic.agent.record_custom_metric('Agent/ToolCall/Duration', duration_ms)
newrelic.agent.record_custom_event('AgentError', {
    'tool_name': tool_name,
    'error': str(error)
})
```

### Langfuse
```python
from langfuse import Langfuse

langfuse = Langfuse(
    public_key="pk-...",
    secret_key="sk-..."
)

# Trace agent execution
trace = langfuse.trace(
    name="agent_execution",
    user_id=user_id,
    session_id=session_id
)

# Log generation
generation = trace.generation(
    name="llm_call",
    model="gpt-4",
    input=prompt,
    output=response,
    usage={
        "prompt_tokens": 100,
        "completion_tokens": 50,
        "total_tokens": 150
    }
)

# Log tool call
span = trace.span(
    name="tool_call",
    input={"tool": "search_flights", "params": {...}},
    output=result
)
```

---

## Best Practices

### 1. Log Everything (But Redact PII)
```python
# Good
logger.log_input(redact_pii(user_message))

# Bad
# Don't log at all (can't debug)
```

### 2. Use Structured Logging (JSON)
```python
# Good
logger.info(json.dumps({
    "event": "tool_call",
    "tool": "search_flights",
    "duration_ms": 1250
}))

# Bad
logger.info(f"Called search_flights, took 1250ms")
```

### 3. Include Context (Session ID, User ID)
```python
# Good
logger.info({
    "session_id": session_id,
    "user_id": user_id,
    "event": "tool_call"
})

# Bad
logger.info({"event": "tool_call"})  # No context
```

### 4. Set Retention Policy
```python
# Delete logs older than 90 days
db.execute("""
    DELETE FROM agent_logs
    WHERE timestamp < NOW() - INTERVAL '90 days'
""")
```

### 5. Monitor Log Volume
```python
# Alert if log volume spikes (potential issue)
daily_log_count = db.query("SELECT COUNT(*) FROM agent_logs WHERE timestamp > NOW() - INTERVAL '1 day'")

if daily_log_count > expected_max:
    send_alert(f"Log volume spike: {daily_log_count}")
```

---

## Summary

**Audit Trails:** Complete record of agent actions

**What to Log:**
- Inputs (user messages)
- Reasoning (thoughts, plans)
- Tool calls (parameters, results)
- Outputs (responses)
- Errors (exceptions, recovery)

**Logging Levels:**
- Trace, Debug, Info, Warning, Error

**Storage:**
- Database (PostgreSQL)
- Object storage (S3)
- Elasticsearch

**Compliance:**
- GDPR (PII redaction, right to be forgotten)
- SOC 2 (immutable, encrypted, access controls)

**Observability:**
- OpenTelemetry
- LangSmith
- Datadog, New Relic
- Langfuse

**Best Practices:**
- Log everything (redact PII)
- Use structured logging (JSON)
- Include context (session_id, user_id)
- Set retention policy
- Monitor log volume
