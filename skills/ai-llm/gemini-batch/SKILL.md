---
name: gemini-batch
version: 1.0
description: This skill should be used when the user asks to "use Gemini Batch API", "process documents at scale", "submit a batch job", "upload files to Gemini", or needs large-scale LLM processing. Includes production gotchas and best practices.
---

# Gemini Batch API Skill

Large-scale asynchronous document processing using Google's Gemini models.

## When to Use

- Process thousands of documents with the same prompt
- Cost-effective bulk extraction (50% cheaper than synchronous API)
- Jobs that can tolerate 24-hour completion windows

## IRON LAW: Use Examples First, Never Guess API

**READ EXAMPLES BEFORE WRITING ANY CODE. NO EXCEPTIONS.**

### The Rule

```
User asks for batch API work
    ↓
MANDATORY: Read examples/batch_processor.py or examples/icon_batch_vision.py
    ↓
Copy the pattern exactly
    ↓
DO NOT guess parameter names
DO NOT try wrapper types
DO NOT improvise API calls
```

### Why This Matters

The Batch API has non-obvious requirements that will fail silently:
1. **Metadata must be flat primitives** - Nested objects cause cryptic errors
2. **Parameter is `dest=` not `destination=`** - Wrong name → TypeError
3. **Config is plain dict** - Not a wrapper type
4. **Examples are authoritative** - Working code beats assumptions

**Rationale:** Previous agents wasted hours debugging API errors that the examples would have prevented. The patterns in `examples/` are battle-tested production code.

### Rationalization Table - STOP If You Catch Yourself Thinking:

| Excuse | Reality | Do Instead |
|--------|---------|------------|
| "I know how APIs work" | You're overconfident about non-obvious gotchas | Read examples first |
| "I can figure it out" | You'll waste 30+ minutes on trial-and-error | Copy working patterns |
| "The examples might be outdated" | They're maintained and tested | Trust the examples |
| "I need to customize anyway" | Your customization comes AFTER copying base pattern | Start with examples, then adapt |
| "Reading examples takes too long" | You'll save 30 minutes debugging with 2 minutes of reading | Read examples first |
| "My approach is simpler" | Your simpler approach already failed | Use proven patterns |

### Red Flags - STOP If You Catch Yourself Thinking:

- **"Let me try `destination=` instead of `dest=`"** → You're about to cause a TypeError. Read examples.
- **"I'll create a `CreateBatchJobConfig` object"** → You're instantiating a type instead of using a plain dict. Stop.
- **"I'll nest metadata like a normal API"** → You'll trigger BigQuery type errors. Flatten your data.
- **"This should work like other Google APIs"** → Your assumption is wrong; this API is different.
- **"I'll figure out the JSONL format"** → You'll waste time. Copy from examples instead.

### MANDATORY Checklist Before ANY Batch API Code

- [ ] Read `examples/batch_processor.py` OR `examples/icon_batch_vision.py`
- [ ] Identify which example matches the use case (Standard API vs Vertex AI)
- [ ] Copy the example's API call pattern **exactly**
- [ ] Copy the example's JSONL structure **exactly**
- [ ] Copy the example's metadata structure **exactly**
- [ ] Adapt for specific needs only after copying base pattern

**Enforcement:** Writing batch API code without reading examples first violates this IRON LAW and will result in preventable errors.

## Prerequisites

### Install gcloud SDK

```bash
# macOS: Install Google Cloud SDK via Homebrew
brew install google-cloud-sdk

# Linux: Install Google Cloud SDK from official sources
curl https://sdk.cloud.google.com | bash
```

### Authentication Setup

```bash
# Authenticate with Google Cloud Platform
gcloud auth login

# Set up Application Default Credentials for Python libraries
gcloud auth application-default login

# Enable Vertex AI API in your project
gcloud services enable aiplatform.googleapis.com
```

**Why both auth methods?**
- `gcloud auth login`: For gsutil and gcloud CLI commands
- `gcloud auth application-default login`: For google-generativeai Python library
- **CRITICAL:** Vertex AI requires ADC (step 2), not just API key

### Create GCS Bucket

```bash
# Create bucket in us-central1 (required region)
gsutil mb -l us-central1 gs://your-batch-bucket

# Verify bucket location is us-central1
gsutil ls -L -b gs://your-batch-bucket | grep "Location"
```

See `references/gcs-setup.md` for complete setup guide.

## Quick Start

### Standard Gemini API (API Key)

```python
from examples.batch_processor import GeminiBatchProcessor

processor = GeminiBatchProcessor(
    bucket_name="my-batch-bucket",  # Must be in us-central1
    model="gemini-2.0-flash-lite"
)

results = processor.run_pipeline(
    input_dir="./documents",
    prompt="Extract as JSON: {title, date, summary}",
    output_dir="./results"
)
```

### Vertex AI (Recommended)

```python
import google.generativeai as genai

# Use Vertex AI with ADC
client = genai.Client(
    vertexai=True,
    project="your-project-id",
    location="us-central1"
)

# Submit batch job
job = client.batches.create(
    model="gemini-2.5-flash-lite",
    src="gs://bucket/requests.jsonl",
    dest="gs://bucket/outputs/"
)
```

## Core Workflow

1. **Upload files** to GCS bucket (us-central1 region required)
2. **Create JSONL** request file with document URIs and prompts
3. **Submit batch job** via `genai.batches.create()`
4. **Poll for completion** (jobs expire after 24 hours)
5. **Download and parse** results from output URI
6. **Handle failures** gracefully (partial failures are common)

## IRON LAW: Metadata and API Call Structure

**YOU MUST USE FLAT PRIMITIVES FOR METADATA. YOU MUST USE SIMPLE STRINGS FOR API PARAMETERS.**

### Rule 1: Metadata Structure

```
CORRECT ✓
"metadata": {
    "request_id": "icon_123",        # String
    "file_name": "copy.svg",         # String
    "file_size": 1024                # Integer
}

WRONG ✗
"metadata": {
    "request_id": "icon_123",
    "file_info": {                   # ← NESTED OBJECT FAILS!
        "name": "copy.svg",
        "size": 1024
    }
}

WORKAROUND (if complex data needed)
"metadata": {
    "request_id": "icon_123",
    "file_info": json.dumps({"name": "copy.svg", "size": 1024})  # JSON string OK
}
```

**Why:** Vertex AI stores metadata in BigQuery-compatible format. BigQuery doesn't support nested types. Violation causes: `"metadata" in the specified input data is of unsupported type.`

### Rule 2: API Call Structure

```python
CORRECT ✓
job = client.batches.create(
    model="gemini-2.5-flash-lite",
    src="gs://bucket/input.jsonl",        # Just a string
    dest="gs://bucket/output/",           # Just a string
    config={"display_name": "my-job"}     # Just a dict
)

WRONG ✗
job = client.batches.create(
    model="gemini-2.5-flash-lite",
    src="gs://bucket/input.jsonl",
    destination="gs://bucket/output/",    # ← PARAMETER DOESN'T EXIST!
)

WRONG ✗
job = client.batches.create(
    model="gemini-2.5-flash-lite",
    src="gs://bucket/input.jsonl",
    config=types.CreateBatchJobConfig(    # ← DON'T INSTANTIATE TYPES!
        dest="gs://bucket/output/"
    )
)
```

**Why:** The SDK uses simple types. Parameter is `dest=` (not destination). Config is a plain dict (not a type instance). The SDK converts internally.

### Rationalization Table - STOP If You Catch Yourself Thinking:

| Excuse | Reality | Do Instead |
|--------|---------|------------|
| "Nested metadata is cleaner" | Your code will fail silently with cryptic errors | Flatten or use `json.dumps()` |
| "I'll try `destination=` parameter" | You'll get a TypeError; parameter doesn't exist | Use `dest=` |
| "I should use `CreateBatchJobConfig`" | You're confusing internal typing with API calls | Pass plain dict to `config=` |
| "Other APIs accept nested objects" | Your assumption breaks here; it's BigQuery-backed | Follow the examples |
| "I'll fix it if it breaks" | Your job fails 5 minutes after submission | Get it right the first time |

### Pre-Submission Validation

```python
# Add this check BEFORE submitting batch job
def validate_metadata(metadata: dict):
    """Ensure metadata contains only primitive types."""
    for key, value in metadata.items():
        if isinstance(value, (dict, list)):
            raise ValueError(
                f"Metadata '{key}' is {type(value).__name__}. "
                f"Only primitives (str, int, float, bool) allowed. "
                f"Use json.dumps() for complex data."
            )
        if not isinstance(value, (str, int, float, bool, type(None))):
            raise ValueError(f"Unsupported type for '{key}': {type(value)}")

# Validate all requests before submission:
for request in batch_requests:
    validate_metadata(request["metadata"])
```

**Enforcement:** Jobs will fail if metadata contains nested objects. There is no workaround for this requirement.

## Key Gotchas

| Issue | Solution |
|-------|----------|
| **Nested metadata fails** | **Use flat primitives or `json.dumps()` for complex data** |
| **TypeError: unexpected keyword** | **Use `dest=` not `destination=`, pass plain dict** |
| Auth errors with Vertex AI | Run `gcloud auth application-default login` |
| vertexai=True requires ADC | API key is ignored with vertexai=True |
| Missing aiplatform API | Run `gcloud services enable aiplatform.googleapis.com` |
| Region mismatch | Use `us-central1` bucket only |
| Wrong URI format | Use `gs://` not `https://` |
| Invalid JSONL | Use `scripts/validate_jsonl.py` |
| Image batch: inline data | Use `fileData.fileUri` for batch, not inline |
| Duplicate IDs | Hash file content + prompt for unique IDs |
| Large PDFs fail | Split at 50 pages / 50MB max |
| JSON parsing fails | Use robust extraction (see gotchas.md) |
| Output not found | Output URI is prefix, not file path |

**Top 2 mistakes** (bolded above):
1. Using nested objects in metadata instead of flat primitives
2. Guessing parameter names instead of using `dest=`

See `references/gotchas.md` for detailed solutions (now with Gotchas 10 & 11).

## Rate Limits

| Limit | Value |
|-------|-------|
| Max requests per JSONL | 10,000 |
| Max concurrent jobs | 10 |
| Max job size | 100MB |
| Job expiration | 24 hours |

## Recommended Models

| Model | Use Case | Cost |
|-------|----------|------|
| `gemini-2.0-flash-lite` | Most batch jobs | Lowest |
| `gemini-2.0-flash` | Complex extraction | Medium |
| `gemini-1.5-pro` | Highest accuracy | Highest |

## Additional Resources

### References
- `references/gcs-setup.md` - **NEW:** Complete GCS and Vertex AI setup guide
- `references/gotchas.md` - 9 critical production gotchas (updated auth section)
- `references/best-practices.md` - Idempotent IDs, state tracking, validation
- `references/troubleshooting.md` - Common errors and debugging
- `references/vertex-ai.md` - Enterprise alternative with comparison
- `references/cli-reference.md` - gsutil and gcloud commands

### Examples
- `examples/icon_batch_vision.py` - **NEW:** Batch vision analysis with Vertex AI
- `examples/batch_processor.py` - Complete GeminiBatchProcessor class
- `examples/pipeline_template.py` - Customizable pipeline template

### Scripts
- `scripts/validate_jsonl.py` - Validate JSONL before submission
- `scripts/test_single.py` - Test single request before batch

## External Documentation

- [Gemini Batch API Guide](https://ai.google.dev/gemini-api/docs/batch)
- [Google Cloud Storage](https://cloud.google.com/python/docs/reference/storage/latest)
- [Vertex AI Batch Prediction](https://cloud.google.com/vertex-ai/docs/predictions/batch-predictions)

## Date Awareness

**Pattern from oh-my-opencode:** Gemini API and documentation evolve rapidly.

Current date: Use `datetime.now()` for:
- API version checking
- Model availability ("gemini-2.5-flash-lite available as of Dec 2024")
- Documentation freshness validation

For API features or model names with uncertainty, verify against current date and check latest Gemini API documentation.
