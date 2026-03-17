---
name: gemini-batch
description: Process large volumes of requests using Gemini Batch API via scripts/. Use for batch processing, bulk text generation, processing JSONL files, async job execution, and cost-efficient high-volume AI tasks. Triggers on "batch processing", "bulk requests", "JSONL", "async job", "batch job".
license: MIT
version: 1.0.0
keywords: batch processing, bulk generation, JSONL, async jobs, cost-efficient, high volume, scalable, parallel processing
---

# Gemini Batch Processing

Process large volumes of requests efficiently using Gemini Batch API through executable scripts for cost savings and high throughput.

## When to Use This Skill

Use this skill when you need to:
- Process hundreds/thousands of requests
- Generate content in bulk (blogs, emails, descriptions)
- Reduce costs for high-volume tasks
- Run async jobs without blocking
- Process large datasets with AI
- Generate multiple documents at once
- Create scalable content pipelines
- Process requests that don't need real-time responses

## Available Scripts

### scripts/create_batch.py
**Purpose**: Create a batch job from a JSONL file

**When to use**:
- Starting any batch processing task
- Uploading multiple requests for processing
- Creating async jobs for large workloads

**Key parameters**:
| Parameter | Description | Example |
|-----------|-------------|---------|
| `input_file` | JSONL file path (required) | `requests.jsonl` |
| `--model`, `-m` | Model to use | `gemini-3-flash-preview` |
| `--name`, `-n` | Display name for job | `"my-batch-job"` |

**Output**: Job name/ID to track with check_status.py

### scripts/check_status.py
**Purpose**: Monitor batch job progress and completion

**When to use**:
- Checking if a batch job is complete
- Polling job status until finished
- Monitoring async job execution

**Key parameters**:
| Parameter | Description | Example |
|-----------|-------------|---------|
| `job_name` | Batch job name/ID (required) | `batches/abc123` |
| `--wait`, `-w` | Poll until completion | Flag |

**Output**: Job status and final state

### scripts/get_results.py
**Purpose**: Retrieve completed batch job results

**When to use**:
- Downloading completed batch results
- Parsing batch job output
- Extracting generated content

**Key parameters**:
| Parameter | Description | Example |
|-----------|-------------|---------|
| `job_name` | Batch job name/ID (required) | `batches/abc123` |
| `--output`, `-o` | Output file path | `results.jsonl` |

**Output**: Results content or file

## Workflows

### Workflow 1: Basic Batch Processing
```bash
# 1. Create JSONL file
echo '{"key": "req1", "request": {"contents": [{"parts": [{"text": "Explain photosynthesis"}]}]}}' > requests.jsonl
echo '{"key": "req2", "request": {"contents": [{"parts": [{"text": "What is gravity?"}]}}]}' >> requests.jsonl

# 2. Create batch job
python scripts/create_batch.py requests.jsonl --name "science-questions"

# 3. Check status
python scripts/check_status.py <job-name> --wait

# 4. Get results
python scripts/get_results.py <job-name> --output results.jsonl
```
- Best for: Basic bulk processing, cost efficiency
- Typical time: Minutes to hours depending on job size

### Workflow 2: Bulk Content Generation
```bash
# 1. Generate JSONL with content requests
python3 << 'EOF'
import json

topics = ["sustainable energy", "AI in healthcare", "space exploration"]
with open("content-requests.jsonl", "w") as f:
    for i, topic in enumerate(topics):
        req = {
            "key": f"blog-{i}",
            "request": {
                "contents": [{
                    "parts": [{
                        "text": f"Write a 500-word blog post about {topic}"
                    }]
                }]
            }
        }
        f.write(json.dumps(req) + "\n")
EOF

# 2. Process batch
python scripts/create_batch.py content-requests.jsonl --name "blog-posts" --model gemini-3-flash-preview
python scripts/check_status.py <job-name> --wait
python scripts/get_results.py <job-name> --output blog-posts.jsonl
```
- Best for: Blog generation, article creation, bulk writing
- Combines with: gemini-text for content needs

### Workflow 3: Dataset Processing
```bash
# 1. Load dataset and create batch requests
python3 << 'EOF'
import json

# Your dataset
data = [
    {"product": "laptop", "features": ["fast", "lightweight"]},
    {"product": "headphones", "features": ["wireless", "noise-cancelling"]},
]

with open("product-descriptions.jsonl", "w") as f:
    for item in data:
        features = ", ".join(item["features"])
        prompt = f"Write a product description for {item['product']} with these features: {features}"
        req = {
            "key": item["product"],
            "request": {
                "contents": [{"parts": [{"text": prompt}]}]
            }
        }
        f.write(json.dumps(req) + "\n")
EOF

# 2. Process
python scripts/create_batch.py product-descriptions.jsonl
python scripts/check_status.py <job-name> --wait
python scripts/get_results.py <job-name> --output results.jsonl
```
- Best for: Product descriptions, dataset enrichment, bulk analysis

### Workflow 4: Email Campaign Generation
```bash
# 1. Create personalized email requests
python3 << 'EOF'
import json

customers = [
    {"name": "Alice", "product": "premium plan"},
    {"name": "Bob", "product": "basic plan"},
]

with open("emails.jsonl", "w") as f:
    for cust in customers:
        prompt = f"Write a personalized email to {cust['name']} about upgrading to our {cust['product']}"
        req = {
            "key": f"email-{cust['name'].lower()}",
            "request": {
                "contents": [{"parts": [{"text": prompt}]}]
            }
        }
        f.write(json.dumps(req) + "\n")
EOF

# 2. Process batch
python scripts/create_batch.py emails.jsonl --name "email-campaign"
python scripts/check_status.py <job-name> --wait
python scripts/get_results.py <job-name> --output email-results.jsonl
```
- Best for: Marketing campaigns, personalized outreach
- Combines with: gemini-text for email content

### Workflow 5: Async Job Monitoring
```bash
# 1. Create job
python scripts/create_batch.py large-batch.jsonl --name "big-job"

# 2. Check status periodically (non-blocking)
while true; do
    python scripts/check_status.py <job-name>
    sleep 60  # Check every minute
done

# 3. Get results when done
python scripts/get_results.py <job-name> --output final-results.jsonl
```
- Best for: Long-running jobs, background processing
- Use when: You don't need immediate results

### Workflow 6: Cost-Optimized Bulk Processing
```bash
# 1. Use flash model for cost efficiency
python scripts/create_batch.py requests.jsonl --model gemini-3-flash-preview --name "cost-optimized"

# 2. Monitor and retrieve
python scripts/check_status.py <job-name> --wait
python scripts/get_results.py <job-name>
```
- Best for: High-volume, cost-sensitive applications
- Savings: Batch API typically 50%+ cheaper than real-time

### Workflow 7: Multi-Stage Pipeline
```bash
# Stage 1: Generate content
python scripts/create_batch.py content-requests.jsonl --name "stage1-content"
python scripts/check_status.py <job1> --wait

# Stage 2: Summarize content
python scripts/create_batch.py summaries.jsonl --name "stage2-summaries"
python scripts/check_status.py <job2> --wait

# Stage 3: Convert to audio (gemini-tts)
# Process results from stage 2
```
- Best for: Complex workflows, multi-step processing
- Combines with: Other Gemini skills for complete pipelines

## Parameters Reference

### JSONL Format

Each line is a separate JSON object:

```json
{
  "key": "unique-identifier",
  "request": {
    "contents": [
      {
        "parts": [
          {
            "text": "Your prompt here"
          }
        ]
      }
    ]
  }
}
```

### Model Selection

| Model | Best For | Cost | Speed |
|-------|----------|------|-------|
| `gemini-3-flash-preview` | General bulk processing | Lowest | Fast |
| `gemini-3-pro-preview` | Complex reasoning tasks | Medium | Medium |
| `gemini-2.5-flash` | Stable, reliable | Low | Fast |
| `gemini-2.5-pro` | Code/math/STEM | Medium | Slow |

### Job States

| State | Description |
|-------|-------------|
| `JOB_STATE_PENDING` | Job queued, waiting to start |
| `JOB_STATE_RUNNING` | Job actively processing |
| `JOB_STATE_SUCCEEDED` | Job completed successfully |
| `JOB_STATE_FAILED` | Job failed (check error message) |
| `JOB_STATE_CANCELLED` | Job was cancelled |
| `JOB_STATE_EXPIRED` | Job timed out |

### Size Limits

| Method | Max Size | Best For |
|--------|-----------|----------|
| File upload | Unlimited | Large batches (recommended) |
| Inline requests | <20MB | Small batches |

## Output Interpretation

### Results JSONL
Each line contains:
```json
{
  "key": "your-identifier",
  "response": {
    "text": "Generated content here..."
  }
}
```

### Error Handling
- Failed requests appear in results with error information
- Check for `error` field in response
- Partial failures don't stop entire job

### Result Access
- Use `--output` to save to file
- Script prints preview of results
- Parse JSONL line by line for processing

## Common Issues

### "google-genai not installed"
```bash
pip install google-genai
```

### "JSONL file not found"
- Verify file path is correct
- Check file extension is `.jsonl` (not `.json`)
- Use absolute paths if relative paths fail

### "Invalid JSONL format"
- Each line must be valid JSON
- No trailing commas between objects
- Check for syntax errors in JSON
- Use JSON validator if unsure

### "Job failed"
- Check error message in status
- Verify request format is correct
- Check model availability
- Review API quota limits

### "No results found"
- Ensure job state is `JOB_STATE_SUCCEEDED`
- Wait for job completion before retrieving
- Check job status first with check_status.py

### "Processing stuck in RUNNING state"
- Large jobs can take hours
- Use `--wait` flag for automated polling
- Check job size and model choice
- Contact support if stuck >24 hours

## Best Practices

### JSONL Creation
- Use unique keys for each request
- Validate JSON before uploading
- Test with small batch first (5-10 requests)
- Include error handling in your scripts

### Job Management
- Use descriptive display names (`--name`)
- Save job names for tracking
- Monitor status before retrieving results
- Keep backup of original JSONL file

### Performance Optimization
- Use flash models for cost efficiency
- Batch as many requests as possible
- File upload preferred over inline
- Process during off-peak hours if timing sensitive

### Error Handling
- Check for failed requests in results
- Retry failed requests individually
- Log job names for audit trails
- Validate output format before use

### Cost Management
- Batch API is 50%+ cheaper than real-time
- Use flash models when possible
- Monitor token usage
- Process in chunks if quota limited

## Related Skills

- **gemini-text**: Generate individual text requests
- **gemini-image**: Batch image generation
- **gemini-tts**: Batch audio generation
- **gemini-embeddings**: Batch embedding creation

## Quick Reference

```bash
# Basic workflow
python scripts/create_batch.py requests.jsonl
python scripts/check_status.py <job-name> --wait
python scripts/get_results.py <job-name> --output results.jsonl

# With model and name
python scripts/create_batch.py requests.jsonl --model gemini-3-flash-preview --name "my-job"

# Create JSONL programmatically
echo '{"key":"1","request":{"contents":[{"parts":[{"text":"Prompt"}]}]}}' > batch.jsonl
```

## Reference

- Get API key: https://aistudio.google.com/apikey
- Documentation: https://ai.google.dev/gemini-api/docs/batch-processing
- JSONL: https://jsonlines.org/
- Cost savings: Batch API typically 50-90% cheaper than real-time API
