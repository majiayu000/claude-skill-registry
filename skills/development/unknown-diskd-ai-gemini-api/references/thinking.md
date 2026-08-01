# Thinking Features

Gemini 3 and 2.5 models use internal reasoning for improved multi-step planning, coding, math, and data analysis.

## Table of Contents

- [Thinking Levels (Gemini 3)](#thinking-levels-gemini-3)
- [Thinking Budgets (Gemini 2.5)](#thinking-budgets-gemini-25)
- [Thought Summaries](#thought-summaries)
- [Thought Signatures](#thought-signatures)
- [Token Usage](#token-usage)
- [Best Practices](#best-practices)

---

## Thinking Levels (Gemini 3)

| Level | Description |
|-------|-------------|
| `minimal` | Matches "no thinking" for most queries (Flash only) |
| `low` | Minimizes latency/cost for simple tasks |
| `medium` | Balanced thinking (Flash only) |
| `high` | Default - maximizes reasoning depth |

Cannot fully disable thinking on Gemini 3 Pro. `minimal` on Flash doesn't guarantee thinking is off.

### Python
```python
from google import genai
from google.genai import types

client = genai.Client()
response = client.models.generate_content(
    model="gemini-3-flash-preview",
    contents="Explain Occam's Razor with an example",
    config=types.GenerateContentConfig(
        thinking_config=types.ThinkingConfig(thinking_level="low")
    ),
)
print(response.text)
```

### JavaScript
```javascript
import { GoogleGenAI, ThinkingLevel } from "@google/genai";

const ai = new GoogleGenAI({});
const response = await ai.models.generateContent({
  model: "gemini-3-flash-preview",
  contents: "Explain Occam's Razor with an example",
  config: {
    thinkingConfig: { thinkingLevel: ThinkingLevel.LOW },
  },
});
console.log(response.text);
```

### REST
```bash
curl "https://generativelanguage.googleapis.com/v1beta/models/gemini-3-flash-preview:generateContent" \
  -H "x-goog-api-key: $GEMINI_API_KEY" \
  -H 'Content-Type: application/json' \
  -d '{
    "contents": [{"parts": [{"text": "Explain Occam'\''s Razor"}]}],
    "generationConfig": {"thinkingConfig": {"thinkingLevel": "low"}}
  }'
```

---

## Thinking Budgets (Gemini 2.5)

For Gemini 2.5 models, use `thinkingBudget` instead of `thinkingLevel`.

| Model | Range | Disable | Dynamic |
|-------|-------|---------|---------|
| 2.5 Pro | 128-32768 | N/A | `-1` (default) |
| 2.5 Flash | 0-24576 | `0` | `-1` (default) |
| 2.5 Flash Lite | 512-24576 | `0` | `-1` |

### Python
```python
response = client.models.generate_content(
    model="gemini-2.5-flash-preview-05-20",
    contents="Complex reasoning task...",
    config=types.GenerateContentConfig(
        thinking_config=types.ThinkingConfig(
            thinking_budget=1024  # Set specific budget
            # thinking_budget=0   # Turn off thinking
            # thinking_budget=-1  # Dynamic (default)
        )
    ),
)
```

### JavaScript
```javascript
const response = await ai.models.generateContent({
  model: "gemini-2.5-flash-preview-05-20",
  contents: "Complex reasoning task...",
  config: {
    thinkingConfig: {
      thinkingBudget: 1024,  // Set specific budget
      // thinkingBudget: 0   // Turn off thinking
      // thinkingBudget: -1  // Dynamic (default)
    },
  },
});
```

---

## Thought Summaries

Get insights into the model's reasoning by enabling `includeThoughts`.

### Python
```python
response = client.models.generate_content(
    model="gemini-3-flash-preview",
    contents="What is the sum of the first 50 prime numbers?",
    config=types.GenerateContentConfig(
        thinking_config=types.ThinkingConfig(include_thoughts=True)
    )
)

for part in response.candidates[0].content.parts:
    if not part.text:
        continue
    if part.thought:
        print("Thought summary:", part.text)
    else:
        print("Answer:", part.text)
```

### JavaScript
```javascript
const response = await ai.models.generateContent({
  model: "gemini-3-flash-preview",
  contents: "What is the sum of the first 50 prime numbers?",
  config: {
    thinkingConfig: { includeThoughts: true },
  },
});

for (const part of response.candidates[0].content.parts) {
  if (part.thought) {
    console.log("Thought summary:", part.text);
  } else {
    console.log("Answer:", part.text);
  }
}
```

### Streaming with Thoughts
```python
for chunk in client.models.generate_content_stream(
    model="gemini-3-flash-preview",
    contents="Solve this logic puzzle...",
    config=types.GenerateContentConfig(
        thinking_config=types.ThinkingConfig(include_thoughts=True)
    )
):
    for part in chunk.candidates[0].content.parts:
        if part.thought:
            print("Thinking:", part.text, end="")
        else:
            print("Answer:", part.text, end="")
```

---

## Thought Signatures

Encrypted representations of internal thinking for multi-turn context. Required for function calling with thinking models.

- **Gemini 2.5**: Returns signatures with function calling
- **Gemini 3**: May return signatures for all part types

Always pass signatures back as received. Required even with `minimal` for Gemini 3 Flash.

The SDK handles signatures automatically. Manual handling only needed when modifying history or using REST.

---

## Token Usage

```python
print("Thoughts tokens:", response.usage_metadata.thoughts_token_count)
print("Output tokens:", response.usage_metadata.candidates_token_count)
```

```javascript
console.log("Thoughts tokens:", response.usageMetadata.thoughtsTokenCount);
console.log("Output tokens:", response.usageMetadata.candidatesTokenCount);
```

---

## Best Practices

| Task Complexity | Recommendation | Examples |
|-----------------|----------------|----------|
| **Easy** | Thinking OFF | Fact retrieval, classification |
| **Medium** | Default | Analogies, comparisons |
| **Hard** | High budget | AIME problems, complex code |

**Tips:**
- Review thought summaries to debug unexpected responses
- Constrain thinking budget for lengthy outputs
- Use `high` for complex math/reasoning tasks
