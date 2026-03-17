---
name: batch-processing
description: Message Batches API for Claude with 50% cost savings on bulk processing. Activate for batch jobs, JSONL processing, bulk analysis, and cost optimization.
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Task
triggers:
  - batch
  - batches
  - bulk
  - jsonl
  - batch processing
  - batch api
  - cost optimization
  - mass processing
dependencies:
  - llm-integration
related-skills:
  - prompt-caching
  - streaming
---

# Batch Processing Skill

Leverage Anthropic's Message Batches API for 50% cost savings on bulk processing workloads.

## When to Use This Skill

- Processing 10K+ documents
- Model evaluation and benchmarks
- ETL and data enrichment
- Training data generation
- Bulk content analysis
- Any non-time-sensitive workload

## Cost Savings

| Processing Type | Cost |
|----------------|------|
| Standard API | 100% |
| **Batch API** | **50%** |

**Example:** 1M tokens @ $3/1M = $3 (standard) vs $1.50 (batch)

## Batch Lifecycle

```
Created → Processing → Ended (completed/failed/expired/canceled)
```

- **Processing time:** Up to 24 hours
- **Results retention:** 29 days
- **Full feature support:** Tools, vision, system prompts

## Core Implementation

### Step 1: Create JSONL File

```python
import json

# Each line is a complete request
requests = [
    {
        "custom_id": "request-1",
        "params": {
            "model": "claude-sonnet-4-20250514",
            "max_tokens": 1024,
            "messages": [{"role": "user", "content": "Summarize: Document 1..."}]
        }
    },
    {
        "custom_id": "request-2",
        "params": {
            "model": "claude-sonnet-4-20250514",
            "max_tokens": 1024,
            "messages": [{"role": "user", "content": "Summarize: Document 2..."}]
        }
    }
]

# Write JSONL file
with open("batch_requests.jsonl", "w") as f:
    for request in requests:
        f.write(json.dumps(request) + "\n")
```

### Step 2: Submit Batch

```python
import anthropic

client = anthropic.Anthropic()

# Create batch from file
with open("batch_requests.jsonl", "rb") as f:
    batch = client.beta.messages.batches.create(
        requests=f
    )

print(f"Batch ID: {batch.id}")
print(f"Status: {batch.processing_status}")
```

### Step 3: Poll for Completion

```python
import time

def wait_for_batch(client, batch_id, poll_interval=60):
    """Poll until batch completes"""
    while True:
        batch = client.beta.messages.batches.retrieve(batch_id)

        if batch.processing_status == "ended":
            print(f"Batch completed!")
            print(f"  Succeeded: {batch.request_counts.succeeded}")
            print(f"  Errored: {batch.request_counts.errored}")
            print(f"  Expired: {batch.request_counts.expired}")
            return batch

        print(f"Status: {batch.processing_status} - waiting...")
        time.sleep(poll_interval)
```

### Step 4: Stream Results

```python
def process_results(client, batch_id):
    """Stream and process batch results"""
    results = {}

    for result in client.beta.messages.batches.results(batch_id):
        custom_id = result.custom_id

        if result.result.type == "succeeded":
            message = result.result.message
            results[custom_id] = {
                "status": "success",
                "content": message.content[0].text,
                "usage": message.usage
            }
        elif result.result.type == "errored":
            results[custom_id] = {
                "status": "error",
                "error": result.result.error
            }
        elif result.result.type == "expired":
            results[custom_id] = {
                "status": "expired"
            }

    return results
```

## Complete Workflow

```python
import anthropic
import json
import time

def run_batch_job(documents):
    """Complete batch processing workflow"""
    client = anthropic.Anthropic()

    # 1. Create requests
    requests = []
    for i, doc in enumerate(documents):
        requests.append({
            "custom_id": f"doc-{i}",
            "params": {
                "model": "claude-sonnet-4-20250514",
                "max_tokens": 1024,
                "messages": [{"role": "user", "content": f"Summarize: {doc}"}]
            }
        })

    # 2. Write JSONL
    with open("batch.jsonl", "w") as f:
        for req in requests:
            f.write(json.dumps(req) + "\n")

    # 3. Submit batch
    with open("batch.jsonl", "rb") as f:
        batch = client.beta.messages.batches.create(requests=f)

    print(f"Batch submitted: {batch.id}")

    # 4. Wait for completion
    while True:
        batch = client.beta.messages.batches.retrieve(batch.id)
        if batch.processing_status == "ended":
            break
        time.sleep(60)

    # 5. Collect results
    results = {}
    for result in client.beta.messages.batches.results(batch.id):
        if result.result.type == "succeeded":
            results[result.custom_id] = result.result.message.content[0].text

    return results
```

## Error Handling

### Retry Failed Requests

```python
def retry_failed(client, original_batch_id):
    """Retry failed and expired requests"""
    retry_requests = []

    for result in client.beta.messages.batches.results(original_batch_id):
        if result.result.type in ["errored", "expired"]:
            # Re-create the request (you'll need to store original params)
            retry_requests.append({
                "custom_id": result.custom_id,
                "params": get_original_params(result.custom_id)  # Your implementation
            })

    if retry_requests:
        # Write and submit retry batch
        with open("retry.jsonl", "w") as f:
            for req in retry_requests:
                f.write(json.dumps(req) + "\n")

        with open("retry.jsonl", "rb") as f:
            return client.beta.messages.batches.create(requests=f)

    return None
```

### Error Types

| Result Type | Action |
|-------------|--------|
| `succeeded` | Process normally |
| `errored` | Check error, may retry |
| `expired` | Request took >24h, retry |
| `canceled` | Batch was canceled |

## API Reference

### Endpoints

| Method | Endpoint | Purpose |
|--------|----------|---------|
| POST | `/v1/messages/batches` | Create batch |
| GET | `/v1/messages/batches/{id}` | Get batch status |
| GET | `/v1/messages/batches` | List batches |
| POST | `/v1/messages/batches/{id}/cancel` | Cancel batch |
| GET | `/v1/messages/batches/{id}/results` | Stream results |

### Request Format

```json
{
    "custom_id": "unique-identifier",
    "params": {
        "model": "claude-sonnet-4-20250514",
        "max_tokens": 1024,
        "system": "Optional system prompt",
        "messages": [{"role": "user", "content": "..."}],
        "tools": [],
        "temperature": 0.7
    }
}
```

## Best Practices

### DO:
- Use for workloads >100 requests
- Include unique custom_id for tracking
- Store original params for retry logic
- Monitor batch status via polling
- Process results as streaming JSONL

### DON'T:
- Use for time-sensitive requests
- Expect immediate results
- Forget to handle expired requests
- Ignore error results

## Cost Optimization Tips

1. **Batch similar requests** - Same model, similar prompts
2. **Combine with caching** - Cache static context before batch
3. **Use appropriate model** - Haiku for simple tasks, Sonnet for complex
4. **Optimize prompts** - Shorter prompts = lower cost

## Use Case: Document Processing

```python
# Process 10,000 documents at 50% cost
documents = load_documents("data/*.txt")  # 10K files

# Create batch with consistent format
requests = [{
    "custom_id": doc.id,
    "params": {
        "model": "claude-haiku-4-20250514",  # Cheapest for bulk
        "max_tokens": 512,
        "system": "Extract key information as JSON.",
        "messages": [{"role": "user", "content": doc.content}]
    }
} for doc in documents]

# Run batch job
results = run_batch_job(requests)
# Cost: ~50% of standard API!
```

## See Also

- llm-integration - API basics
- prompt-caching - Cache context
- streaming - Real-time output
