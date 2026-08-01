# Structured Outputs

Generate JSON responses that adhere to a schema using Pydantic (Python) or Zod (JavaScript).

## Table of Contents

- [Basic Usage](#basic-usage)
- [Streaming](#streaming)
- [With Tools (Gemini 3)](#with-tools-gemini-3)
- [JSON Schema Reference](#json-schema-reference)
- [Structured Outputs vs Function Calling](#structured-outputs-vs-function-calling)
- [Best Practices](#best-practices)

---

## Basic Usage

### Python (Pydantic)
```python
from google import genai
from pydantic import BaseModel, Field
from typing import List, Optional

class Ingredient(BaseModel):
    name: str = Field(description="Name of the ingredient.")
    quantity: str = Field(description="Quantity with units.")

class Recipe(BaseModel):
    recipe_name: str
    prep_time_minutes: Optional[int] = None
    ingredients: List[Ingredient]
    instructions: List[str]

client = genai.Client()
response = client.models.generate_content(
    model="gemini-3-flash-preview",
    contents="Extract the recipe: chocolate chip cookies need 2 cups flour...",
    config={
        "response_mime_type": "application/json",
        "response_json_schema": Recipe.model_json_schema(),
    },
)

recipe = Recipe.model_validate_json(response.text)
print(recipe)
```

### JavaScript (Zod)
```javascript
import { GoogleGenAI } from "@google/genai";
import { z } from "zod";
import { zodToJsonSchema } from "zod-to-json-schema";

const recipeSchema = z.object({
  recipe_name: z.string(),
  prep_time_minutes: z.number().optional(),
  ingredients: z.array(z.object({
    name: z.string(),
    quantity: z.string(),
  })),
  instructions: z.array(z.string()),
});

const ai = new GoogleGenAI({});
const response = await ai.models.generateContent({
  model: "gemini-3-flash-preview",
  contents: "Extract the recipe: chocolate chip cookies need 2 cups flour...",
  config: {
    responseMimeType: "application/json",
    responseJsonSchema: zodToJsonSchema(recipeSchema),
  },
});

const recipe = recipeSchema.parse(JSON.parse(response.text));
```

### REST
```bash
curl "https://generativelanguage.googleapis.com/v1beta/models/gemini-3-flash-preview:generateContent" \
  -H "x-goog-api-key: $GEMINI_API_KEY" \
  -H 'Content-Type: application/json' \
  -d '{
    "contents": [{"parts": [{"text": "Extract the recipe..."}]}],
    "generationConfig": {
      "responseMimeType": "application/json",
      "responseJsonSchema": {
        "type": "object",
        "properties": {
          "recipe_name": {"type": "string"},
          "ingredients": {
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "name": {"type": "string"},
                "quantity": {"type": "string"}
              },
              "required": ["name", "quantity"]
            }
          },
          "instructions": {"type": "array", "items": {"type": "string"}}
        },
        "required": ["recipe_name", "ingredients", "instructions"]
      }
    }
  }'
```

---

## Streaming

Stream partial JSON chunks for better perceived performance.

```python
from pydantic import BaseModel
from typing import Literal

class Feedback(BaseModel):
    sentiment: Literal["positive", "neutral", "negative"]
    summary: str

response_stream = client.models.generate_content_stream(
    model="gemini-3-flash-preview",
    contents="Analyze: The new UI is great!",
    config={
        "response_mime_type": "application/json",
        "response_json_schema": Feedback.model_json_schema(),
    },
)

for chunk in response_stream:
    print(chunk.candidates[0].content.parts[0].text, end="")
```

---

## With Tools (Gemini 3)

Combine structured outputs with Google Search, URL Context, Code Execution.

### Python
```python
from pydantic import BaseModel, Field
from typing import List

class MatchResult(BaseModel):
    winner: str
    final_match_score: str
    scorers: List[str]

response = client.models.generate_content(
    model="gemini-3-pro-preview",
    contents="Search for details of the latest Euro final.",
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
const response = await ai.models.generateContent({
  model: "gemini-3-pro-preview",
  contents: "Search for details of the latest Euro final.",
  config: {
    tools: [{ googleSearch: {} }, { urlContext: {} }],
    responseMimeType: "application/json",
    responseJsonSchema: zodToJsonSchema(matchSchema),
  },
});
```

---

## JSON Schema Reference

### Supported Types

| Type | Description |
|------|-------------|
| `string` | Text values |
| `number` | Floating-point |
| `integer` | Whole numbers |
| `boolean` | true/false |
| `object` | Key-value pairs |
| `array` | Lists |
| `null` | Use `{"type": ["string", "null"]}` for nullable |

### Type-Specific Properties

**Object:** `properties`, `required`, `additionalProperties`

**String:** `enum`, `format` (date-time, date, time)

**Number/Integer:** `enum`, `minimum`, `maximum`

**Array:** `items`, `prefixItems`, `minItems`, `maxItems`

**Descriptive:** `title`, `description` (guides model output)

---

## Structured Outputs vs Function Calling

| Feature | Use Case |
|---------|----------|
| **Structured Outputs** | Format the final response (data extraction, classification) |
| **Function Calling** | Take action during conversation (call APIs, get data) |

---

## Best Practices

- Use `description` fields to guide the model
- Use specific types (`enum`, `integer`) when possible
- State clearly in prompts what to extract
- Validate output in application code (schema compliance does not guarantee semantic correctness)
- Simplify schemas if API rejects them (shorten names, reduce nesting)

**Note**: Gemini 2.0 requires explicit `propertyOrdering` in JSON schema.
