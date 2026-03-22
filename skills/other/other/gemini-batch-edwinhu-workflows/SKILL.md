---
name: gemini-batch
version: 1.0
description: This skill should be used when the user asks to "use Gemini Batch API", "process documents at scale", "submit a batch job", "upload files to Gemini", or needs large-scale LLM processing. Includes production gotchas and best practices.
user-invocable: false
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
# macOS: Install via nix-darwin (add to ~/nix/ configuration)
# Or if already available: gcloud --version

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

Uses the Gemini File API for input. Results returned via `batch_job.dest.file_name`.

```python
from google import genai

client = genai.Client()  # Uses GOOGLE_API_KEY env var

# Upload JSONL to File API
uploaded = client.files.upload(
    file="requests.jsonl",
    config={"mime_type": "application/jsonl"}
)

# Submit batch job
job = client.batches.create(
    model="gemini-2.5-flash-lite",
    src=uploaded.name,  # "files/..." URI
    config={"display_name": "my-batch-job"}
)

# Results available at job.dest.file_name after completion
```

### Vertex AI (Recommended for GCS workflows)

Uses GCS URIs directly. Supports `dest=` parameter for output location.

```python
from google import genai

# Use Vertex AI with ADC (not API key)
client = genai.Client(
    vertexai=True,
    project="your-project-id",
    location="us-central1"
)

# Submit batch job with GCS paths
job = client.batches.create(
    model="gemini-2.5-flash-lite",
    src="gs://bucket/requests.jsonl",   # GCS input
    dest="gs://bucket/outputs/"          # GCS output (Vertex AI only!)
)
```

**Key difference:** Standard API uses File API (`files/...`), Vertex AI uses GCS (`gs://...`) with explicit `dest=` parameter.

## Core Workflow

**Standard API:**
1. **Create JSONL** request file with prompts
2. **Upload JSONL** to File API via `client.files.upload()`
3. **Submit batch job** via `client.batches.create(src=uploaded.name)`
4. **Poll for completion** (jobs expire after 24 hours)
5. **Download results** from `job.dest.file_name`

**Vertex AI:**
1. **Upload files** to GCS bucket (us-central1 region required)
2. **Create JSONL** request file with document URIs and prompts
3. **Submit batch job** via `client.batches.create(src=..., dest=...)`
4. **Poll for completion** (jobs expire after 24 hours)
5. **Download and parse** results from GCS output URI
6. **Handle failures** gracefully (partial failures are common)

## Key Gotchas (API Structure)

**Metadata must be flat primitives** (no nested objects — BigQuery-backed storage). **Parameter is `dest=` not `destination=`** (Vertex AI only). **Config is a plain dict** (not a wrapper type).

See the Rationalization Table in the first Iron Law section above — the same gotchas apply here. The Key Gotchas table below summarizes all critical issues.

## Key Gotchas

| Issue | Solution |
|-------|----------|
| **Nested metadata fails** | **Use flat primitives or `json.dumps()` for complex data** |
| **TypeError: unexpected keyword** | **Use `dest=` not `destination=` (Vertex AI only)** |
| **Mixing API patterns** | **Standard API: File API + no dest. Vertex AI: GCS + dest** |
| Auth errors with Vertex AI | Run `gcloud auth application-default login` |
| vertexai=True requires ADC | API key is ignored with vertexai=True |
| Missing aiplatform API | Run `gcloud services enable aiplatform.googleapis.com` |
| Region mismatch (Vertex) | Use `us-central1` bucket only |
| Wrong URI format (Vertex) | Use `gs://` not `https://` |
| Invalid JSONL | Use `scripts/validate_jsonl.py` |
| Image batch: inline data | Use `fileData.fileUri` for batch, not inline |
| Duplicate IDs | Hash file content + prompt for unique IDs |
| Large PDFs fail | Split at 50 pages / 50MB max |
| JSON parsing fails | Use robust extraction (see gotchas.md) |
| Output not found (Vertex) | Output URI is prefix, not file path |

**Top 3 mistakes** (bolded above):
1. Using nested objects in metadata instead of flat primitives
2. Mixing Standard API and Vertex AI patterns
3. Using `destination=` instead of `dest=` (Vertex AI)

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
| `gemini-2.5-flash-lite` | Most batch jobs | Lowest |
| `gemini-2.5-flash` | Complex extraction | Medium |
| `gemini-2.5-pro` | Highest accuracy | Highest |

## Additional Resources

### References
- `references/gcs-setup.md` - **NEW:** Complete GCS and Vertex AI setup guide
- `references/gotchas.md` - 9 critical production gotchas (updated auth section)
- `references/best-practices.md` - Idempotent IDs, state tracking, validation
- `references/scale-up-testing.md` - Incremental scale-up testing (LangExtract prototyping, LLM-as-judge, Vertex AI batch)
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

Gemini API evolves rapidly. For API features or model names with uncertainty, verify against current documentation.
