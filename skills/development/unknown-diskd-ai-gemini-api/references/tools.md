# Built-in Tools

Gemini 3 models support built-in tools: Google Search, File Search, Code Execution, URL Context, and Function Calling.

**Note**: Function calling cannot be combined with other built-in tools.

## Table of Contents

- [Google Search](#google-search)
- [URL Context](#url-context)
- [Code Execution](#code-execution)
- [Function Calling](#function-calling)
- [File Search](#file-search)

---

## Google Search

Ground responses with real-time web search results.

### Python
```python
from google import genai

client = genai.Client()
response = client.models.generate_content(
    model="gemini-3-pro-preview",
    contents="What are the latest developments in AI?",
    config={"tools": [{"google_search": {}}]},
)
print(response.text)
```

### JavaScript
```javascript
import { GoogleGenAI } from "@google/genai";

const ai = new GoogleGenAI({});
const response = await ai.models.generateContent({
  model: "gemini-3-pro-preview",
  contents: "What are the latest developments in AI?",
  config: { tools: [{ googleSearch: {} }] },
});
console.log(response.text);
```

### REST
```bash
curl "https://generativelanguage.googleapis.com/v1beta/models/gemini-3-pro-preview:generateContent" \
  -H "x-goog-api-key: $GEMINI_API_KEY" \
  -H 'Content-Type: application/json' \
  -d '{
    "contents": [{"parts": [{"text": "What are the latest developments in AI?"}]}],
    "tools": [{"google_search": {}}]
  }'
```

---

## URL Context

Fetch and analyze content from specified URLs.

### Python
```python
response = client.models.generate_content(
    model="gemini-3-pro-preview",
    contents="Summarize the main points from https://example.com/article",
    config={"tools": [{"url_context": {}}]},
)
```

### JavaScript
```javascript
const response = await ai.models.generateContent({
  model: "gemini-3-pro-preview",
  contents: "Summarize the main points from https://example.com/article",
  config: { tools: [{ urlContext: {} }] },
});
```

### Combining Search and URL Context
```python
response = client.models.generate_content(
    model="gemini-3-pro-preview",
    contents="Find and summarize the latest research on quantum computing",
    config={"tools": [{"google_search": {}}, {"url_context": {}}]},
)
```

---

## Code Execution

Execute Python code in a sandboxed environment.

### Python
```python
response = client.models.generate_content(
    model="gemini-3-pro-preview",
    contents="Calculate the factorial of 20 and verify it",
    config={"tools": [{"code_execution": {}}]},
)
print(response.text)
```

### JavaScript
```javascript
const response = await ai.models.generateContent({
  model: "gemini-3-pro-preview",
  contents: "Calculate the factorial of 20 and verify it",
  config: { tools: [{ codeExecution: {} }] },
});
```

---

## Function Calling

Define custom functions the model can call. **Cannot be combined with other built-in tools.**

### Python
```python
from google.genai import types

# Define the function schema
get_weather = types.FunctionDeclaration(
    name="get_weather",
    description="Get current weather for a location",
    parameters={
        "type": "object",
        "properties": {
            "location": {"type": "string", "description": "City name"},
            "unit": {"type": "string", "enum": ["celsius", "fahrenheit"]},
        },
        "required": ["location"],
    },
)

response = client.models.generate_content(
    model="gemini-3-flash-preview",
    contents="What's the weather in Tokyo?",
    config=types.GenerateContentConfig(
        tools=[types.Tool(function_declarations=[get_weather])]
    ),
)

# Check for function call
if response.function_calls:
    fc = response.function_calls[0]
    print(f"Function: {fc.name}, Args: {fc.args}")
```

### JavaScript
```javascript
const getWeather = {
  name: "get_weather",
  description: "Get current weather for a location",
  parameters: {
    type: "object",
    properties: {
      location: { type: "string", description: "City name" },
      unit: { type: "string", enum: ["celsius", "fahrenheit"] },
    },
    required: ["location"],
  },
};

const response = await ai.models.generateContent({
  model: "gemini-3-flash-preview",
  contents: "What's the weather in Tokyo?",
  config: {
    tools: [{ functionDeclarations: [getWeather] }],
  },
});

if (response.functionCalls) {
  const { name, args } = response.functionCalls[0];
  console.log(`Function: ${name}, Args: ${JSON.stringify(args)}`);
}
```

For comprehensive function calling documentation including automatic execution, compositional calling, multimodal responses, MCP integration, and best practices, see [function-calling.md](function-calling.md)

---

## File Search

Search through uploaded files.

### Python
```python
# Upload a file first
file = client.files.upload(path="/path/to/document.pdf")

response = client.models.generate_content(
    model="gemini-3-pro-preview",
    contents=[
        "What are the key findings in this document?",
        file,
    ],
    config={"tools": [{"file_search": {}}]},
)
```

---

## Resources

- [Google Search](https://ai.google.dev/gemini-api/docs/google-search)
- [URL Context](https://ai.google.dev/gemini-api/docs/url-context)
- [Code Execution](https://ai.google.dev/gemini-api/docs/code-execution)
- [Function Calling](https://ai.google.dev/gemini-api/docs/function-calling)
- [File Search](https://ai.google.dev/gemini-api/docs/file-search)
