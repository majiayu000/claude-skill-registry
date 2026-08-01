# Gemini 3 Model Family

Gemini 3 is Google's most intelligent model family, built on state-of-the-art reasoning. Designed for agentic workflows, autonomous coding, and complex multimodal tasks.

## Models

| Model ID | Context (In/Out) | Knowledge Cutoff | Pricing (Input/Output per 1M tokens) |
|----------|------------------|------------------|--------------------------------------|
| `gemini-3-pro-preview` | 1M / 64k | Jan 2025 | $2/$12 (<200k), $4/$18 (>200k) |
| `gemini-3-flash-preview` | 1M / 64k | Jan 2025 | $0.50 / $3 |
| `gemini-3-pro-image-preview` | 65k / 32k | Jan 2025 | $2 (text) / $0.134 (image) |

**Free Tier**: Flash only (`gemini-3-flash-preview`). No free tier for Pro in API (free in AI Studio).

---

## Thinking Level

Controls maximum reasoning depth. Default: `high`.

### Supported Levels

| Model | Levels |
|-------|--------|
| **Pro & Flash** | `low`, `high` |
| **Flash only** | `minimal`, `medium` |

- `minimal`: No thinking for most queries. Required thought signatures still apply.
- `low`: Minimizes latency/cost. Simple tasks, chat, high-throughput.
- `medium`: Balanced (Flash only).
- `high` (default): Maximum reasoning depth. Higher latency, better results.

### Python

```python
from google import genai
from google.genai import types

client = genai.Client()

response = client.models.generate_content(
    model="gemini-3-pro-preview",
    contents="How does AI work?",
    config=types.GenerateContentConfig(
        thinking_config=types.ThinkingConfig(thinking_level="low")
    ),
)
```

### JavaScript

```javascript
import { GoogleGenAI } from "@google/genai";

const ai = new GoogleGenAI({});

const response = await ai.models.generateContent({
    model: "gemini-3-pro-preview",
    contents: "How does AI work?",
    config: {
      thinkingConfig: {
        thinkingLevel: "low",
      }
    },
  });
```

### REST

```bash
curl "https://generativelanguage.googleapis.com/v1beta/models/gemini-3-pro-preview:generateContent" \
  -H "x-goog-api-key: $GEMINI_API_KEY" \
  -H 'Content-Type: application/json' \
  -d '{
    "contents": [{"parts": [{"text": "How does AI work?"}]}],
    "generationConfig": {
      "thinkingConfig": {"thinkingLevel": "low"}
    }
  }'
```

**Note**: Cannot combine `thinking_level` with legacy `thinking_budget`. Returns 400 error.

---

## Media Resolution

Controls multimodal vision processing fidelity. Available in `v1alpha` API.

### Levels

| Level | Max Tokens | Use Case |
|-------|------------|----------|
| `media_resolution_low` | 280 (image), 70 (video/frame) | Fast processing |
| `media_resolution_medium` | 560 (image), 70 (video/frame) | PDFs, balanced |
| `media_resolution_high` | 1120 (image), 280 (video/frame) | Most images |
| `media_resolution_ultra_high` | - | Per-part only |

### Recommendations

| Media Type | Setting | Notes |
|------------|---------|-------|
| **Images** | `high` | Maximum quality for most tasks |
| **PDFs** | `medium` | Quality saturates at medium |
| **Video (general)** | `low`/`medium` | Both = 70 tokens/frame |
| **Video (text-heavy)** | `high` | OCR, small details |

### Python

```python
from google import genai
from google.genai import types
import base64

# v1alpha required for media_resolution
client = genai.Client(http_options={'api_version': 'v1alpha'})

response = client.models.generate_content(
    model="gemini-3-pro-preview",
    contents=[
        types.Content(
            parts=[
                types.Part(text="What is in this image?"),
                types.Part(
                    inline_data=types.Blob(
                        mime_type="image/jpeg",
                        data=base64.b64decode("..."),
                    ),
                    media_resolution={"level": "media_resolution_high"}
                )
            ]
        )
    ]
)
```

### JavaScript

```javascript
import { GoogleGenAI } from "@google/genai";

// v1alpha required for media_resolution
const ai = new GoogleGenAI({ apiVersion: "v1alpha" });

const response = await ai.models.generateContent({
  model: "gemini-3-pro-preview",
  contents: [
    {
      parts: [
        { text: "What is in this image?" },
        {
          inlineData: {
            mimeType: "image/jpeg",
            data: "...",
          },
          mediaResolution: {
            level: "media_resolution_high"
          }
        }
      ]
    }
  ]
});
```

---

## Temperature

**Keep at default 1.0 for Gemini 3.** Changing temperature (especially <1.0) may cause looping or degraded performance on complex tasks.

---

## Thought Signatures

Encrypted representations of internal reasoning. **Required** for maintaining context across API calls.

### Validation Rules

| Use Case | Validation | Behavior |
|----------|------------|----------|
| **Function Calling** | Strict | 400 error if missing |
| **Image Generation/Editing** | Strict | 400 error if missing |
| **Text/Chat** | Not enforced | Degrades quality if omitted |

**SDKs handle signatures automatically** when using standard chat history.

### Function Calling (Sequential Multi-Step)

When model chains tool calls within one turn, accumulate all signatures:

```javascript
// Step 1: Model calls check_flight, returns <Sig_A>
// Step 2: Send flight result with <Sig_A>
// Step 3: Model calls book_taxi, returns <Sig_B>
// Step 4: Send taxi result with BOTH <Sig_A> AND <Sig_B>

[
  { "role": "user", "parts": [{ "text": "Check flight AA100..." }] },
  {
    "role": "model",
    "parts": [{
      "functionCall": { "name": "check_flight", "args": {...} },
      "thoughtSignature": "<Sig_A>"  // REQUIRED
    }]
  },
  { "role": "user", "parts": [{ "functionResponse": {...} }] },
  {
    "role": "model",
    "parts": [{
      "functionCall": { "name": "book_taxi", "args": {...} },
      "thoughtSignature": "<Sig_B>"  // REQUIRED
    }]
  },
  { "role": "user", "parts": [{ "functionResponse": {...} }] }
]
```

### Parallel Function Calling

Only first function call has signature:

```javascript
[
  { "role": "user", "parts": [{ "text": "Check weather in Paris and London." }] },
  {
    "role": "model",
    "parts": [
      {
        "functionCall": { "name": "check_weather", "args": { "city": "Paris" } },
        "thoughtSignature": "<Signature_A>"  // Only first has signature
      },
      {
        "functionCall": { "name": "check_weather", "args": { "city": "London" } }
        // No signature on subsequent parallel calls
      }
    ]
  },
  {
    "role": "user",
    "parts": [
      { "functionResponse": { "name": "check_weather", "response": { "temp": "15C" } } },
      { "functionResponse": { "name": "check_weather", "response": { "temp": "12C" } } }
    ]
  }
]
```

### Image Generation/Editing

Signatures appear on first part (text or image) and ALL subsequent image parts:

```javascript
// Model response
{
  "role": "model",
  "parts": [
    { "text": "I will generate...", "thoughtSignature": "<Sig_D>" },
    { "inlineData": {...}, "thoughtSignature": "<Sig_E>" }
  ]
}

// Next turn - return ALL signatures
{
  "contents": [
    { "role": "user", "parts": [{ "text": "Generate a cyberpunk city" }] },
    {
      "role": "model",
      "parts": [
        { "text": "...", "thoughtSignature": "<Sig_D>" },
        { "inlineData": "...", "thoughtSignature": "<Sig_E>" }
      ]
    },
    { "role": "user", "parts": [{ "text": "Make it daytime." }] }
  ]
}
```

### Migration Bypass

When migrating from other models or injecting custom function calls without valid signatures:

```json
"thoughtSignature": "context_engineering_is_the_way_to_go"
```

---

## Structured Outputs with Built-in Tools

Combine JSON schemas with Google Search, URL Context, or Code Execution.

### Python

```python
from google import genai
from pydantic import BaseModel, Field
from typing import List

class MatchResult(BaseModel):
    winner: str = Field(description="The name of the winner.")
    final_match_score: str = Field(description="The final match score.")
    scorers: List[str] = Field(description="The name of the scorer.")

client = genai.Client()

response = client.models.generate_content(
    model="gemini-3-pro-preview",
    contents="Search for all details for the latest Euro.",
    config={
        "tools": [{"google_search": {}}, {"url_context": {}}],
        "response_mime_type": "application/json",
        "response_json_schema": MatchResult.model_json_schema(),
    },
)

result = MatchResult.model_validate_json(response.text)
```

### JavaScript

```javascript
import { GoogleGenAI } from "@google/genai";
import { z } from "zod";
import { zodToJsonSchema } from "zod-to-json-schema";

const ai = new GoogleGenAI({});

const matchSchema = z.object({
  winner: z.string().describe("The name of the winner."),
  final_match_score: z.string().describe("The final score."),
  scorers: z.array(z.string()).describe("The name of the scorer.")
});

const response = await ai.models.generateContent({
  model: "gemini-3-pro-preview",
  contents: "Search for all details for the latest Euro.",
  config: {
    tools: [{ googleSearch: {} }, { urlContext: {} }],
    responseMimeType: "application/json",
    responseJsonSchema: zodToJsonSchema(matchSchema),
  },
});
```

---

## Nano Banana Pro (Image Generation)

`gemini-3-pro-image-preview` - Highest quality image generation with 4K output, grounded generation, and conversational editing.

### Capabilities

- **4K & text rendering**: Sharp, legible text and diagrams
- **Grounded generation**: Use `google_search` for real-world data
- **Conversational editing**: Multi-turn edits via thought signatures

### Python

```python
from google import genai
from google.genai import types

client = genai.Client()

response = client.models.generate_content(
    model="gemini-3-pro-image-preview",
    contents="Generate an infographic of the current weather in Tokyo.",
    config=types.GenerateContentConfig(
        tools=[{"google_search": {}}],
        image_config=types.ImageConfig(
            aspect_ratio="16:9",
            image_size="4K"
        )
    )
)

for part in response.parts:
    if part.inline_data is not None:
        part.as_image().save('weather_tokyo.png')
```

### JavaScript

```javascript
import { GoogleGenAI } from "@google/genai";
import * as fs from "node:fs";

const ai = new GoogleGenAI({});

const response = await ai.models.generateContent({
  model: "gemini-3-pro-image-preview",
  contents: "Generate a visualization of the current weather in Tokyo.",
  config: {
    tools: [{ googleSearch: {} }],
    imageConfig: {
      aspectRatio: "16:9",
      imageSize: "4K"
    }
  }
});

for (const part of response.candidates[0].content.parts) {
  if (part.inlineData) {
    const buffer = Buffer.from(part.inlineData.data, "base64");
    fs.writeFileSync("weather_tokyo.png", buffer);
  }
}
```

---

## Multimodal Function Responses

Return images/media in function responses for richer tool interactions.

### Python

```python
from google import genai
from google.genai import types
import requests

client = genai.Client()

# Define tool
get_image_declaration = types.FunctionDeclaration(
    name="get_image",
    description="Retrieves the image file reference for a specific order item.",
    parameters={
        "type": "object",
        "properties": {
            "item_name": {
                "type": "string",
                "description": "The name of the item ordered."
            }
        },
        "required": ["item_name"],
    },
)

# After receiving functionCall, send multimodal response
image_bytes = requests.get("https://example.com/image.jpg").content

function_response_multimodal = types.FunctionResponsePart(
    inline_data=types.FunctionResponseBlob(
        mime_type="image/jpeg",
        display_name="instrument.jpg",
        data=image_bytes,
    )
)

# Include in history
history = [
    types.Content(role="user", parts=[types.Part(text="Show me the instrument I ordered")]),
    response_1.candidates[0].content,
    types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name="get_image",
                response={"image_ref": {"$ref": "instrument.jpg"}},
                parts=[function_response_multimodal]
            )
        ],
    )
]
```

---

## Migration from Gemini 2.5

| Aspect | Change |
|--------|--------|
| **Thinking** | Use `thinking_level: "high"` with simpler prompts |
| **Temperature** | Remove explicit settings, use default 1.0 |
| **PDF resolution** | Test `media_resolution_high` for dense documents |
| **Token usage** | May increase for PDFs, decrease for video |
| **Image segmentation** | Not supported - use Gemini 2.5 Flash |
| **Maps/Computer Use** | Not yet supported |

---

## OpenAI Compatibility

`reasoning_effort` (OpenAI) maps to `thinking_level` (Gemini).

Note: `reasoning_effort: medium` maps to `thinking_level: high` on Gemini 3 Flash.

---

## Prompting Best Practices

1. **Be concise**: Direct, clear instructions. Avoid verbose prompt engineering.
2. **Request verbosity explicitly**: Default is direct answers. Ask for conversational style if needed.
3. **Context placement**: Put instructions/questions at END of prompt, after data. Start with "Based on the information above..."

---

## Supported Tools

- Google Search
- File Search
- Code Execution
- URL Context
- Function Calling (not with built-in tools)

**Not supported**: Google Maps grounding, Computer Use

---

## FAQ

| Question | Answer |
|----------|--------|
| Knowledge cutoff? | January 2025 |
| Context limits? | 1M input, 64k output |
| Free tier? | Flash only in API, both in AI Studio |
| `thinking_budget` supported? | Yes, but migrate to `thinking_level` |
| Batch API? | Yes |
| Context Caching? | Yes |
