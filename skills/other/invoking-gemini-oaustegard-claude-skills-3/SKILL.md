---
name: invoking-gemini
description: Invokes Google Gemini models for structured outputs, multi-modal tasks, and Google-specific features. Use when users request Gemini, structured JSON output, Google API integration, or cost-effective parallel processing.
metadata:
  version: 0.4.0
---

# Invoking Gemini

Delegate tasks to Google's Gemini models when they offer advantages over Claude.

## When to Use Gemini

**Structured outputs:**
- JSON Schema validation with property ordering guarantees
- Pydantic model compliance
- Strict schema adherence (enum values, required fields)

**Cost optimization:**
- Parallel batch processing (Gemini 3 Flash is lightweight)
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

All Gemini 3 models are currently in preview. Use only these — no Gemini 2.x.

### Text / Reasoning Models

**gemini-3-flash-preview** (Default / Recommended):
- Gemini 3 Flash: Pro-level intelligence at Flash speed and pricing
- 1M token context window, 64k output
- Knowledge cutoff: Jan 2025
- $0.50 input / $3.00 output per 1M tokens
- Alias: `flash`

**gemini-3.1-pro-preview**:
- Gemini 3.1 Pro: Best for complex tasks requiring broad world knowledge and advanced reasoning across modalities
- 1M token context window, 64k output
- Knowledge cutoff: Jan 2025
- $2.00 / $12.00 per 1M tokens (<200k tokens); $4.00 / $18.00 (>200k tokens)
- Alias: `pro`

**gemini-3.1-flash-lite-preview**:
- Gemini 3.1 Flash-Lite: Workhorse model for cost-efficiency and high-volume tasks
- 1M token context window, 64k output
- Knowledge cutoff: Jan 2025
- $0.25 (text, image, video), $0.50 (audio) input / $1.50 output per 1M tokens
- Alias: `lite`

### Image Generation Models

**nano-banana-2** (Default image model):
- Gemini 3.1 Flash Image — high-volume, high-efficiency image generation
- API model: `gemini-3.1-flash-image-preview`
- 128k input context, 32k output
- $0.25 per 1M text input tokens / $0.067 per image output
- Alias: `image`

**nano-banana-pro**:
- Gemini 3 Pro Image — highest quality image generation with text rendering and multi-turn editing
- API model: `gemini-3-pro-image-preview`
- 65k input context, 32k output
- $2.00 per 1M text input tokens / $0.134 per image output
- Alias: `image-pro`

See [references/models.md](references/models.md) for full model details and pricing.

## Setup

**Prerequisites:**

```bash
uv pip install requests pydantic
# google-generativeai only needed for direct API fallback:
# uv pip install google-generativeai
```

**Credentials — Option A (recommended): Cloudflare AI Gateway**

Requests are routed through [Cloudflare AI Gateway](https://developers.cloudflare.com/ai-gateway/),
bypassing IP blocks and gaining caching, analytics, and rate limiting.

Create `/mnt/project/proxy.env`:
```
CF_ACCOUNT_ID=<your-cloudflare-account-id>
CF_GATEWAY_ID=<your-gateway-name>
CF_API_TOKEN=<your-cf-api-token>
# GOOGLE_API_KEY only needed if not using Cloudflare BYOK:
# GOOGLE_API_KEY=AIzaSy...
```

- Get your Cloudflare Account ID: Cloudflare dashboard → right sidebar
- Create a gateway: Cloudflare dashboard → AI Gateway → Create gateway
- Generate an API token: https://dash.cloudflare.com/profile/api-tokens
- Store your Gemini key in the gateway (BYOK): AI Gateway → your gateway → API Keys

**Credentials — Option B: Direct Google API (fallback)**

If no `proxy.env` is found, the client falls back to direct Google API access:

- Create document: `GOOGLE_API_KEY.txt` (content: `AIzaSy...`)
- Or create `API_CREDENTIALS.json`: `{"google_api_key": "AIzaSy..."}`

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
    model="gemini-3-flash-preview"
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
    model="gemini-3-flash-preview"
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
    model="gemini-3-flash-preview"
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
    model="gemini-3-flash-preview",
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

## Image Generation

Generate images using Gemini's native image models:

```python
from gemini_client import generate_image

# Basic generation
result = generate_image("A watercolor painting of a mountain lake at sunset")
print(result["path"])     # /mnt/user-data/outputs/gemini_image_1740000000.png
print(result["caption"])  # Optional text the model returns alongside the image
```

### Model Selection

```python
# Fast generation (default) — nano-banana-2 → gemini-3.1-flash-image-preview
result = generate_image("A red bicycle", model="nano-banana-2")

# High-fidelity — nano-banana-pro → gemini-3-pro-image-preview
result = generate_image("A red bicycle", model="image-pro")
```

### Custom Output Path

```python
result = generate_image(
    "A logo for a coffee shop called 'Bean There'",
    output_path="/mnt/user-data/outputs/coffee_logo.png"
)
```

### Effective Prompt Patterns

- **Be specific about style:** "A watercolor painting of..." vs "A picture of..."
- **Include composition details:** "centered, wide angle, high contrast"
- **Specify text rendering:** "A poster with the text 'SALE' in bold red letters"
- **Multi-turn editing:** Generate once, then refine with follow-up prompts

### Return Value

```python
{
    "path": "/mnt/user-data/outputs/gemini_image_1740000000.png",
    "caption": "Optional descriptive text from the model"  # or None
}
```

Returns `None` on failure (credentials missing, API error, no image in response).

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

Gemini 3 Flash is cost-effective for sub-tasks:

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
- gemini-3-flash-preview: ~1M input, 64k output
- gemini-3.1-pro-preview: ~1M input, 64k output (2x pricing above 200k)
- gemini-3.1-flash-lite-preview: ~1M input, 64k output

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

**"No credentials configured":**
- Create `/mnt/project/proxy.env` with `CF_ACCOUNT_ID`, `CF_GATEWAY_ID`, `CF_API_TOKEN`
- Or add `GOOGLE_API_KEY.txt` for direct API access
- See Setup section above for details

**CF Gateway 401/403:**
- Verify your `CF_API_TOKEN` has AI Gateway permissions
- Check that gateway authentication is enabled in the Cloudflare dashboard
- If not using BYOK, add `GOOGLE_API_KEY` to `proxy.env`

**CF Gateway 429 (rate limited):**
- The client automatically retries with exponential backoff
- Check your gateway's rate limit settings in Cloudflare dashboard

**Import errors:**
```bash
uv pip install requests pydantic
# For direct API fallback only:
uv pip install google-generativeai
```

**Schema validation failures:**
- Check Pydantic model definitions
- Ensure prompt is clear about expected structure
- Add examples to prompt if needed

## Cost Comparison

All Gemini 3 models (preview, Jan 2025 cutoff):

| Model | Input / 1M tokens | Output / 1M tokens |
|---|---|---|
| Gemini 3 Flash (`gemini-3-flash-preview`) | $0.50 | $3.00 |
| Gemini 3.1 Pro (`gemini-3.1-pro-preview`) | $2.00 (<200k) / $4.00 (>200k) | $12.00 / $18.00 |
| Gemini 3.1 Flash-Lite (`gemini-3.1-flash-lite-preview`) | $0.25 text/image/video, $0.50 audio | $1.50 |
| Nano Banana 2 / 3.1 Flash Image (`gemini-3.1-flash-image-preview`) | $0.25 text | $0.067 per image |
| Nano Banana Pro / 3 Pro Image (`gemini-3-pro-image-preview`) | $2.00 text | $0.134 per image |

**Strategy:** Use Flash-Lite for high-volume simple tasks, 3 Flash for balanced performance, 3.1 Pro for complex reasoning.
