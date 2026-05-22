---
name: gemini-llm
description: Invoke Google Gemini 3 Pro for text generation, reasoning, and code tasks using the Python google-genai SDK. Supports gemini-3-pro-preview (best multimodal), gemini-2.5-pro (reasoning), and gemini-2.5-flash (fast).
---

# Gemini LLM Skill

Invoke Google Gemini models for text generation, reasoning, code analysis, and complex tasks using the Python `google-genai` SDK.

## Available Models

| Model ID | Description | Best For |
|----------|-------------|----------|
| `gemini-3-pro-preview` | Best multimodal understanding | Complex reasoning, analysis |
| `gemini-2.5-pro` | Advanced thinking model | Deep reasoning, planning |
| `gemini-2.5-flash` | Fast and capable | Quick tasks, high throughput |
| `gemini-2.5-flash-lite` | Fastest, cost-efficient | Simple tasks, bulk processing |

## Configuration

**API Key Location**: `C:\Users\USERNAME\env` (GEMINI_API_KEY)

**Default API Key**: `${GEMINI_API_KEY}`

## Usage

### Basic Text Generation

```bash
python -c "
from google import genai
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))
response = client.models.generate_content(
    model='gemini-3-pro-preview',
    contents='YOUR_PROMPT_HERE'
)
print(response.text)
"
```

### With System Instructions

```bash
python -c "
from google import genai
from google.genai import types

client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))
response = client.models.generate_content(
    model='gemini-3-pro-preview',
    contents='YOUR_PROMPT_HERE',
    config=types.GenerateContentConfig(
        system_instruction='You are a helpful coding assistant.',
        temperature=0.7,
        max_output_tokens=8192
    )
)
print(response.text)
"
```

### Streaming Response

```bash
python -c "
from google import genai
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))
for chunk in client.models.generate_content_stream(
    model='gemini-3-pro-preview',
    contents='YOUR_PROMPT_HERE'
):
    print(chunk.text, end='', flush=True)
print()
"
```

## Workflow

When this skill is invoked:

1. **Parse the user request** to determine:
   - The prompt/task to send to Gemini
   - Which model to use (default: `gemini-3-pro-preview`)
   - Any configuration options (temperature, max tokens, system instruction)

2. **Select the appropriate model**:
   - Complex reasoning/analysis → `gemini-3-pro-preview`
   - Deep planning/thinking → `gemini-2.5-pro`
   - Quick responses → `gemini-2.5-flash`
   - Bulk/simple tasks → `gemini-2.5-flash-lite`

3. **Execute the Python command** using Bash tool:
   ```bash
   python -c "
   from google import genai
   client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))
   response = client.models.generate_content(
       model='MODEL_ID',
       contents='''PROMPT'''
   )
   print(response.text)
   "
   ```

4. **Return the response** to the user

## Example Invocations

### Code Review
```bash
python -c "
from google import genai
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))
response = client.models.generate_content(
    model='gemini-3-pro-preview',
    contents='''Review this Python code for bugs and improvements:

def calculate_total(items):
    total = 0
    for item in items:
        total += item.price * item.quantity
    return total
'''
)
print(response.text)
"
```

### Explain Concept
```bash
python -c "
from google import genai
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))
response = client.models.generate_content(
    model='gemini-2.5-flash',
    contents='Explain async/await in Python in simple terms'
)
print(response.text)
"
```

### Generate Code
```bash
python -c "
from google import genai
from google.genai import types

client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))
response = client.models.generate_content(
    model='gemini-3-pro-preview',
    contents='Write a Python function to merge two sorted lists',
    config=types.GenerateContentConfig(
        system_instruction='You are an expert Python developer. Write clean, efficient, well-documented code.',
        temperature=0.3
    )
)
print(response.text)
"
```

## Multi-turn Conversations

For conversations with history:

```bash
python -c "
from google import genai
from google.genai import types

client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

history = [
    types.Content(role='user', parts=[types.Part(text='What is Python?')]),
    types.Content(role='model', parts=[types.Part(text='Python is a high-level programming language...')]),
    types.Content(role='user', parts=[types.Part(text='How do I install it?')])
]

response = client.models.generate_content(
    model='gemini-3-pro-preview',
    contents=history
)
print(response.text)
"
```

## Error Handling

The skill handles common errors:
- **404 Not Found**: Model not available - fall back to gemini-2.5-pro
- **Rate Limiting**: Wait and retry with exponential backoff
- **Token Limits**: Truncate input or use streaming for large outputs

## Notes

- Gemini 3 Pro is NOT available via the Gemini CLI (v0.17.1) - must use Python SDK
- The `thought_signature` warning can be ignored - it's internal model metadata
- For long prompts, use triple quotes and escape special characters
- Maximum context: varies by model (check documentation)

## Tools to Use

- **Bash**: Execute Python commands
- **Read**: Load files to include in prompts
- **Write**: Save Gemini responses to files
