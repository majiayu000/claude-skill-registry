---
name: openai-llm
description: Invoke OpenAI models for text generation, reasoning, and code tasks using the Python openai SDK. Supports gpt-4o (multimodal), o1 (reasoning), o3-mini (fast reasoning), and gpt-4o-mini (fast).
---

# OpenAI LLM Skill

Invoke OpenAI models for text generation, reasoning, code analysis, and complex tasks using the Python `openai` SDK.

## Available Models

| Model ID | Description | Best For |
|----------|-------------|----------|
| `gpt-4o` | Flagship multimodal model | General tasks, vision, analysis |
| `gpt-4o-mini` | Fast and cost-efficient | Quick tasks, high throughput |
| `o1` | Advanced reasoning model | Complex reasoning, math, code |
| `o1-mini` | Fast reasoning | Moderate reasoning tasks |
| `o3-mini` | Newest reasoning model | Deep reasoning, planning |

## Configuration

**API Key Location**: `C:\Users\USERNAME\env` (OPENAI_API_KEY)

**Default API Key**: Use environment variable `OPENAI_API_KEY`

## Usage

### Basic Text Generation

```bash
python -c "
from openai import OpenAI
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
response = client.chat.completions.create(
    model='gpt-4o',
    messages=[{'role': 'user', 'content': 'YOUR_PROMPT_HERE'}]
)
print(response.choices[0].message.content)
"
```

### With System Instructions

```bash
python -c "
from openai import OpenAI
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
response = client.chat.completions.create(
    model='gpt-4o',
    messages=[
        {'role': 'system', 'content': 'You are a helpful coding assistant.'},
        {'role': 'user', 'content': 'YOUR_PROMPT_HERE'}
    ],
    temperature=0.7,
    max_tokens=4096
)
print(response.choices[0].message.content)
"
```

### Streaming Response

```bash
python -c "
from openai import OpenAI
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
stream = client.chat.completions.create(
    model='gpt-4o',
    messages=[{'role': 'user', 'content': 'YOUR_PROMPT_HERE'}],
    stream=True
)
for chunk in stream:
    if chunk.choices[0].delta.content:
        print(chunk.choices[0].delta.content, end='', flush=True)
print()
"
```

### Using Reasoning Models (o1, o3-mini)

```bash
python -c "
from openai import OpenAI
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
response = client.chat.completions.create(
    model='o1',
    messages=[{'role': 'user', 'content': 'YOUR_COMPLEX_REASONING_PROMPT'}]
)
print(response.choices[0].message.content)
"
```

## Workflow

When this skill is invoked:

1. **Parse the user request** to determine:
   - The prompt/task to send to OpenAI
   - Which model to use (default: `gpt-4o`)
   - Any configuration options (temperature, max tokens, system message)

2. **Select the appropriate model**:
   - General tasks/analysis → `gpt-4o`
   - Quick responses → `gpt-4o-mini`
   - Complex reasoning/math → `o1` or `o3-mini`
   - Moderate reasoning → `o1-mini`

3. **Execute the Python command** using Bash tool:
   ```bash
   python -c "
   from openai import OpenAI
   client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
   response = client.chat.completions.create(
       model='MODEL_ID',
       messages=[{'role': 'user', 'content': '''PROMPT'''}]
   )
   print(response.choices[0].message.content)
   "
   ```

4. **Return the response** to the user

## Example Invocations

### Code Review
```bash
python -c "
from openai import OpenAI
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
response = client.chat.completions.create(
    model='gpt-4o',
    messages=[{'role': 'user', 'content': '''Review this Python code for bugs and improvements:

def calculate_total(items):
    total = 0
    for item in items:
        total += item.price * item.quantity
    return total
'''}]
)
print(response.choices[0].message.content)
"
```

### Complex Reasoning (with o1)
```bash
python -c "
from openai import OpenAI
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
response = client.chat.completions.create(
    model='o1',
    messages=[{'role': 'user', 'content': 'Solve this step by step: A farmer has 17 sheep. All but 9 die. How many are left?'}]
)
print(response.choices[0].message.content)
"
```

### Generate Code
```bash
python -c "
from openai import OpenAI
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
response = client.chat.completions.create(
    model='gpt-4o',
    messages=[
        {'role': 'system', 'content': 'You are an expert Python developer. Write clean, efficient, well-documented code.'},
        {'role': 'user', 'content': 'Write a Python function to merge two sorted lists'}
    ],
    temperature=0.3
)
print(response.choices[0].message.content)
"
```

## Multi-turn Conversations

For conversations with history:

```bash
python -c "
from openai import OpenAI
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
response = client.chat.completions.create(
    model='gpt-4o',
    messages=[
        {'role': 'user', 'content': 'What is Python?'},
        {'role': 'assistant', 'content': 'Python is a high-level programming language...'},
        {'role': 'user', 'content': 'How do I install it?'}
    ]
)
print(response.choices[0].message.content)
"
```

## Model Notes

### Reasoning Models (o1, o3-mini)
- Do NOT support system messages - use user messages only
- Do NOT support temperature parameter
- May take longer to respond (they "think" internally)
- Best for math, logic, complex code problems

### GPT-4o Models
- Support system messages and all parameters
- Fast responses
- Good for general tasks, vision, multimodal

## Error Handling

The skill handles common errors:
- **Rate Limiting**: Wait and retry with exponential backoff
- **Token Limits**: Truncate input or use streaming for large outputs
- **Invalid Model**: Fall back to gpt-4o

## Tools to Use

- **Bash**: Execute Python commands
- **Read**: Load files to include in prompts
- **Write**: Save OpenAI responses to files
