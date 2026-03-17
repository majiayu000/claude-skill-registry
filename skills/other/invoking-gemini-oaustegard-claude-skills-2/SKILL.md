---
name: invoking-gemini
description: Invokes Google Gemini models for structured outputs, multi-modal tasks, and Google-specific features. Use when users request Gemini, structured JSON output, Google API integration, or cost-effective parallel processing.
metadata:
  version: 0.0.3
---

# Invoking Gemini

Delegate tasks to Google's Gemini models when they offer advantages over Claude.

## When to Use Gemini

**Structured outputs:**
- JSON Schema validation with property ordering guarantees
- Pydantic model compliance
- Strict schema adherence (enum values, required fields)

**Cost optimization:**
- Parallel batch processing (Gemini Flash is lightweight)
- High-volume simple tasks
- Budget-constrained operations

**Google ecosystem:**
- Integration with Google services
- Vertex AI workflows
- Google-specific APIs

**Multi-modal tasks:**
- Image analysis with JSON output
- Video processing
- Audio transcription with structure

## Available Models

**gemini-2.0-flash-exp** (Recommended):
- Fast, cost-effective
- Native JSON Schema support
- Good for structured outputs

**gemini-1.5-pro**:
- More capable reasoning
- Better for complex tasks
- Higher cost

**gemini-1.5-flash**:
- Balanced speed/quality
- Good for most tasks

See [references/models.md](references/models.md) for full model details.

## Setup

**Prerequisites:**

1. Install google-generativeai:
   ```bash
   uv pip install google-generativeai pydantic
   ```

2. Configure API key via project knowledge file:

   **Option 1 (recommended): Individual file**
   - Create document: `GOOGLE_API_KEY.txt`
   - Content: Your API key (e.g., `AIzaSy...`)

   **Option 2: Combined file**
   - Create document: `API_CREDENTIALS.json`
   - Content:
     ```json
     {
       "google_api_key": "AIzaSy..."
     }
     ```

   Get your API key: https://console.cloud.google.com/apis/credentials

## Basic Usage

Import the client:

```python
import sys
sys.path.append('/mnt/skills/invoking-gemini/scripts')
from gemini_client import invoke_gemini

# Simple prompt
response = invoke_gemini(
    prompt="Explain quantum computing in 3 bullet points",
    model="gemini-2.0-flash-exp"
)
print(response)
```

## Structured Output

Use Pydantic models for guaranteed JSON Schema compliance:

```python
from pydantic import BaseModel, Field
from gemini_client import invoke_with_structured_output

class BookAnalysis(BaseModel):
    title: str
    genre: str = Field(description="Primary genre")
    key_themes: list[str] = Field(max_length=5)
    rating: int = Field(ge=1, le=5)

result = invoke_with_structured_output(
    prompt="Analyze the book '1984' by George Orwell",
    pydantic_model=BookAnalysis
)

# result is a BookAnalysis instance
print(result.title)  # "1984"
print(result.genre)  # "Dystopian Fiction"
```

**Advantages over Claude:**
- Guaranteed property ordering in JSON
- Strict enum enforcement
- Native schema validation (no prompt engineering)
- Lower cost for simple extractions

## Parallel Invocation

Process multiple prompts concurrently:

```python
from gemini_client import invoke_parallel

prompts = [
    "Summarize the plot of Hamlet",
    "Summarize the plot of Macbeth",
    "Summarize the plot of Othello"
]

results = invoke_parallel(
    prompts=prompts,
    model="gemini-2.0-flash-exp"
)

for prompt, result in zip(prompts, results):
    print(f"Q: {prompt[:30]}...")
    print(f"A: {result[:100]}...\n")
```

**Use cases:**
- Batch classification tasks
- Data labeling
- Multiple independent analyses
- A/B testing prompts

## Error Handling

The client handles common errors:

```python
from gemini_client import invoke_gemini

response = invoke_gemini(
    prompt="Your prompt here",
    model="gemini-2.0-flash-exp"
)

if response is None:
    print("Error: API call failed")
    # Check project knowledge file for valid google_api_key
```

**Common issues:**
- Missing API key → Add GOOGLE_API_KEY.txt to project knowledge (see Setup above)
- Invalid model → Raises ValueError
- Rate limit → Automatically retries with backoff
- Network error → Returns None after retries

## Advanced Features

### Custom Generation Config

```python
response = invoke_gemini(
    prompt="Write a haiku",
    model="gemini-2.0-flash-exp",
    temperature=0.9,
    max_output_tokens=100,
    top_p=0.95
)
```

### Multi-modal Input

```python
# Image analysis with structured output
from pydantic import BaseModel

class ImageDescription(BaseModel):
    objects: list[str]
    scene: str
    colors: list[str]

result = invoke_with_structured_output(
    prompt="Describe this image",
    pydantic_model=ImageDescription,
    image_path="/mnt/user-data/uploads/photo.jpg"
)
```

See [references/advanced.md](references/advanced.md) for more patterns.

## Comparison: Gemini vs Claude

**Use Gemini when:**
- Structured output is primary goal
- Cost is a constraint
- Property ordering matters
- Batch processing many simple tasks

**Use Claude when:**
- Complex reasoning required
- Long context needed (200K tokens)
- Code generation quality matters
- Nuanced instruction following

**Use both:**
- Claude for planning/reasoning
- Gemini for structured extraction
- Parallel workflows with different strengths

## Token Efficiency Pattern

Gemini Flash is cost-effective for sub-tasks:

```python
# Claude (you) plans the approach
# Gemini executes structured extractions

data_points = []
for file in uploaded_files:
    # Gemini extracts structured data
    result = invoke_with_structured_output(
        prompt=f"Extract contact info from {file}",
        pydantic_model=ContactInfo
    )
    data_points.append(result)

# Claude synthesizes results
# ... your analysis here ...
```

## Limitations

**Not suitable for:**
- Tasks requiring deep reasoning
- Long context (>1M tokens)
- Complex code generation
- Subjective creative writing

**Token limits:**
- gemini-2.0-flash-exp: ~1M input tokens
- gemini-1.5-pro: ~2M input tokens

**Rate limits:**
- Vary by API tier
- Client handles automatic retry

## Examples

See [references/examples.md](references/examples.md) for:
- Data extraction from documents
- Batch classification
- Multi-modal analysis
- Hybrid Claude+Gemini workflows

## Troubleshooting

**"API key not configured":**
- Add project knowledge file `GOOGLE_API_KEY.txt` with your API key
- Or add to `API_CREDENTIALS.json`: `{"google_api_key": "AIzaSy..."}`
- See Setup section above for details

**Import errors:**
```bash
uv pip install google-generativeai pydantic
```

**Schema validation failures:**
- Check Pydantic model definitions
- Ensure prompt is clear about expected structure
- Add examples to prompt if needed

## Cost Comparison

Approximate pricing (as of 2024):

**Gemini 2.0 Flash:**
- Input: $0.15 / 1M tokens
- Output: $0.60 / 1M tokens

**Claude Sonnet:**
- Input: $3.00 / 1M tokens
- Output: $15.00 / 1M tokens

For 1000 simple extraction tasks (100 tokens each):
- Gemini Flash: ~$0.10
- Claude Sonnet: ~$2.00

**Strategy:** Use Claude for complex reasoning, Gemini for high-volume simple tasks.
