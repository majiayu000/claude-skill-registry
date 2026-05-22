---
name: genai-text
description: Generate text using Google GenAI Gemini models via CLI. Use when the user asks to generate text, get AI responses, create content, write with AI, or use Gemini for text completion.
---

# GenAI Text Generation Skill

Generate text using the `genai-cli text` command with Gemini models.

## Quick Start

```bash
# Basic text generation
uv run genai-cli text "What is the capital of France?"

# With custom model
uv run genai-cli text "Explain quantum computing" --model gemini-3-pro-preview

# Creative writing with temperature
uv run genai-cli text "Write a poem about the ocean" --temperature 0.9

# With system instruction
uv run genai-cli text "Explain this code" --system "You are a senior software engineer"

# Streaming output
uv run genai-cli text "Tell me a long story" --stream

# Save to file
uv run genai-cli text "Generate documentation" --output ./docs.md
```

## CLI Reference

```
uv run genai-cli text [OPTIONS] PROMPT

Options:
  --model, -m        Model: gemini-2.5-flash (default), gemini-2.5-flash-lite,
                     gemini-3-pro-preview, gemini-2.0-flash
  --temperature, -t  Randomness (0.0-2.0, default: 0.7)
  --max-tokens, -M   Maximum output tokens
  --system, -s       System instruction/persona
  --top-p            Nucleus sampling threshold (0.0-1.0)
  --top-k            Top-k token sampling (1-100)
  --stop             Stop sequences (can be specified multiple times)
  --seed             Random seed for reproducibility
  --stream           Stream output in real-time
  --output, -o       Save response to file
  --json             Output as JSON
```

## Available Models

| Model | Use Case | Notes |
|-------|----------|-------|
| `gemini-2.5-flash` | General text/multimodal | **Default** - balanced speed/quality |
| `gemini-2.5-flash-lite` | Low latency, high volume | Faster, cheaper |
| `gemini-3-pro-preview` | Complex reasoning/coding | Most capable |
| `gemini-2.0-flash` | Alternative general use | Stable |

## Parameters

### Temperature

Controls randomness. Lower = more deterministic, higher = more creative.

```bash
# Factual, deterministic response
uv run genai-cli text "What is 2+2?" --temperature 0.0

# Creative writing
uv run genai-cli text "Write a creative story" --temperature 1.5
```

### System Instruction

Set a persona or context for the model:

```bash
# Technical expert
uv run genai-cli text "Review this code" --system "You are a senior security engineer"

# Creative writer
uv run genai-cli text "Write about sunset" --system "You are a poet who loves nature"

# Specific format
uv run genai-cli text "Explain REST APIs" --system "Explain like I'm 5 years old"
```

### Token Control

Limit or control output length:

```bash
# Short response
uv run genai-cli text "Summarize this topic" --max-tokens 100

# Long form content
uv run genai-cli text "Write an essay" --max-tokens 2000
```

### Sampling Parameters

Fine-tune generation with advanced sampling:

```bash
# Nucleus sampling (top-p)
uv run genai-cli text "Generate ideas" --top-p 0.9

# Top-k sampling
uv run genai-cli text "Complete this sentence" --top-k 40

# Combined for fine control
uv run genai-cli text "Creative brainstorm" --temperature 0.8 --top-p 0.95 --top-k 50
```

### Stop Sequences

Stop generation at specific text:

```bash
# Stop at markers
uv run genai-cli text "Write a story" --stop "THE END" --stop "---"
```

### Reproducibility

Use seed for consistent outputs:

```bash
# Same seed = same output
uv run genai-cli text "Generate a name" --seed 42
uv run genai-cli text "Generate a name" --seed 42  # Same result
```

## Output Modes

### Standard Output

```bash
uv run genai-cli text "Hello"
# Output: Hello! How can I assist you today?
```

### Streaming

Real-time output as tokens are generated:

```bash
uv run genai-cli text "Tell me a story" --stream
# Output appears word by word
```

### JSON Output

Structured output for automation:

```bash
uv run genai-cli text "Hello" --json
```

```json
{
  "success": true,
  "command": "text",
  "data": {
    "response": "Hello! How can I assist you today?",
    "model": "gemini-2.5-flash"
  },
  "metadata": {
    "temperature": null,
    "max_tokens": null,
    "stream": false,
    "output_file": null
  }
}
```

### File Output

Save directly to file:

```bash
uv run genai-cli text "Generate documentation" --output ./docs.md

# With streaming
uv run genai-cli text "Write a report" --stream --output ./report.txt
```

## Use Cases

### Code Generation

```bash
uv run genai-cli text "Write a Python function to calculate fibonacci" \
  --model gemini-3-pro-preview \
  --system "You are an expert Python developer"
```

### Documentation

```bash
uv run genai-cli text "Document this API endpoint" \
  --system "You are a technical writer" \
  --output ./api-docs.md
```

### Creative Writing

```bash
uv run genai-cli text "Write a short story about space exploration" \
  --temperature 1.2 \
  --max-tokens 1000 \
  --stream
```

### Data Analysis

```bash
uv run genai-cli text "Analyze this dataset and provide insights" \
  --model gemini-3-pro-preview \
  --system "You are a data scientist"
```

### Translation

```bash
uv run genai-cli text "Translate to Spanish: Hello, how are you?" \
  --temperature 0.3
```

## Prerequisites

API key must be configured:

```bash
uv run genai-cli auth set-key
```
