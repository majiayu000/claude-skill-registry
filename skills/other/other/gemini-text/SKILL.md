---
name: gemini-text
description: Generate text content using Google Gemini models via scripts/. Use for text generation, multimodal prompts with images, thinking mode for complex reasoning, JSON-formatted outputs, and Google Search grounding for real-time information. Triggers on "generate with gemini", "use gemini for text", "AI text generation", "multimodal prompt", "gemini thinking mode", "grounded response".
license: MIT
version: 1.0.0
keywords: text generation, multimodal, thinking mode, grounding, JSON output, search, reasoning, gemini-3, gemini-2.5
---

# Gemini Text Generation

Generate content using Google's Gemini API through executable scripts with advanced capabilities including system instructions, thinking mode, JSON output, and Google Search grounding.

## When to Use This Skill

Use this skill when you need to:
- Generate any type of text content (blogs, emails, code, stories)
- Process images with text descriptions or analysis
- Perform complex reasoning requiring step-by-step thinking
- Get structured JSON outputs for data processing
- Access real-time information via Google Search
- Apply specific personas or behavior patterns
- Combine text generation with other Gemini skills (images, TTS, embeddings)

## Available Scripts

### scripts/generate.py
**Purpose**: Full-featured text generation with all Gemini capabilities

**When to use**:
- Any text generation task
- Multimodal prompts (text + image)
- Complex reasoning requiring thinking mode
- Structured JSON output requirements
- Real-time information needs (grounding)
- Custom system instructions/personas

**Key parameters**:
| Parameter | Description | Example |
|-----------|-------------|---------|
| `prompt` | Text prompt (required) | `"Explain quantum computing"` |
| `--model`, `-m` | Model to use | `gemini-3-flash-preview` |
| `--system`, `-s` | System instruction | `"You are a helpful assistant"` |
| `--thinking`, `-t` | Enable thinking mode | Flag |
| `--json`, `-j` | Force JSON output | Flag |
| `--grounding`, `-g` | Enable Google Search | Flag |
| `--image`, `-i` | Image for multimodal | `photo.png` |
| `--temperature` | Sampling 0.0-2.0 | `0.7` for creative |
| `--max-tokens` | Output limit | `1000` |

**Output**: Generated text string, optionally with grounding sources

## Workflows

### Workflow 1: Basic Text Generation
```bash
python scripts/generate.py "Explain quantum computing in simple terms"
```
- Best for: Simple content creation, explanations, summaries
- Model: `gemini-3-flash-preview` (default, fast)

### Workflow 2: With System Instruction (Persona)
```bash
python scripts/generate.py "How do I read a file in Python?" --system "You are a helpful coding assistant"
```
- Best for: Domain-specific tasks, expert personas, consistent tone
- Use when: You need specific behavioral constraints

### Workflow 3: Complex Reasoning (Thinking Mode)
```bash
python scripts/generate.py "Analyze the ethical implications of AI in healthcare" --thinking
```
- Best for: Complex analysis, step-by-step reasoning, multi-step problems
- Use when: Task requires careful consideration and logical progression

### Workflow 4: Structured JSON Output
```bash
python scripts/generate.py "Generate a user profile object with name, email, and preferences" --json
```
- Best for: Data extraction, structured data generation, API responses
- Output: Valid JSON ready for parsing
- Note: Prompt must clearly request JSON structure

### Workflow 5: Real-Time Information (Grounding)
```bash
python scripts/generate.py "Who won the latest Super Bowl?" --grounding
```
- Best for: Current events, news, factual information after training cutoff
- Output: Response + grounding sources with citations
- Use when: Accuracy of current information is critical

### Workflow 6: Multimodal (Image Analysis)
```bash
python scripts/generate.py "Describe what's in this image in detail" --image photo.png
```
- Best for: Image captioning, visual analysis, image-based Q&A
- Requires: Image file in PNG or JPEG format
- Combines well with: gemini-files for file upload

### Workflow 7: Content Creation Pipeline (Batch + Text + TTS)
```bash
# 1. Create batch requests (gemini-batch skill)
# 2. Generate content
python scripts/generate.py "Create a 500-word blog post about sustainable energy"
# 3. Convert to audio (gemini-tts skill)
```
- Best for: High-volume content production, podcasts, audiobooks

## Parameters Reference

### Model Selection

| Model | Speed | Intelligence | Context | Best For |
|-------|-------|--------------|---------|----------|
| `gemini-3-flash-preview` | Fast | High | 1M | General use, agentic tasks (default) |
| `gemini-3-pro-preview` | Medium | Highest | 1M | Complex reasoning, research |
| `gemini-2.5-flash` | Fast | Medium | 1M | Stable, reliable generation |
| `gemini-2.5-pro` | Slow | High | 1M | Code, math, STEM tasks |

### Temperature Settings

| Value | Creativity | Best For |
|-------|-----------|----------|
| 0.0-0.3 | Low | Code, facts, formal writing |
| 0.4-0.7 | Medium | Balanced output |
| 0.8-1.0 | High | Creative writing, brainstorming |
| 1.0-2.0 | Very High | Highly creative, varied outputs |

### Thinking Budget

| Value | Description |
|-------|-------------|
| 0 | Disabled (default behavior) |
| 512-1024 | Standard reasoning |
| 2048+ | Deep analysis (slower, more tokens) |

## Output Interpretation

### Standard Text Output
- Plain text response ready for use
- Check for truncation if max-tokens was set
- May include markdown formatting

### JSON Output
- Valid JSON object (use `--json` flag)
- Parse with: `import json; data = json.loads(output)`
- Verify structure matches your requirements
- Handle potential parsing errors

### Grounded Response
When `--grounding` is used, the script prints:
1. Main response text
2. "--- Grounding Sources ---" section
3. List of sources with titles and URLs

### Thinking Mode Output
- May include reasoning steps before final answer
- Longer response times due to thinking process
- Better for tasks requiring careful analysis

## Common Issues

### "google-genai not installed"
```bash
pip install google-genai
```

### "API key not set"
Set environment variable:
```bash
export GOOGLE_API_KEY="your-key-here"
# or
export GEMINI_API_KEY="your-key-here"
```

### "Model not available"
- Check model name spelling
- Verify API access for selected model
- Try `gemini-3-flash-preview` (most available)

### JSON parse errors
- Ensure prompt explicitly requests JSON structure
- Check output for JSON formatting
- Consider using system instruction: "You always respond with valid JSON"

### Image file not found
- Verify image path is correct
- Use absolute paths if relative paths fail
- Supported formats: PNG, JPEG

### Response truncated
- Increase `--max-tokens` value
- Break task into smaller requests
- Use pro models with higher token limits

## Best Practices

### Performance Optimization
- Use flash models for speed, pro for quality
- Lower temperature (0.0-0.3) for deterministic outputs
- Set appropriate max-tokens to control costs
- Use thinking mode only for complex tasks

### Prompt Engineering
- Be specific and clear in your prompts
- Use system instructions for consistent behavior
- Include examples in prompts for better results
- For JSON: specify exact structure in prompt

### Error Handling
- Wrap script calls in try-except blocks
- Validate JSON output before parsing
- Handle network timeouts with retries
- Check API quota limits for batch operations

### Cost Management
- Use flash models when possible (lower cost)
- Limit max-tokens for simple queries
- Cache results for repeated queries
- Use batch API for high-volume tasks

## Related Skills

- **gemini-image**: Generate images from text
- **gemini-tts**: Convert text to speech
- **gemini-embeddings**: Create vector embeddings for semantic search
- **gemini-files**: Upload files for multimodal processing
- **gemini-batch**: Process multiple requests efficiently

## Quick Reference

```bash
# Basic
python scripts/generate.py "Your prompt"

# Persona
python scripts/generate.py "Prompt" --system "You are X"

# Thinking
python scripts/generate.py "Complex task" --thinking

# JSON
python scripts/generate.py "Generate JSON" --json

# Search
python scripts/generate.py "Current event" --grounding

# Multimodal
python scripts/generate.py "Describe this" --image photo.png
```

## Reference

- See `references/models.md` for detailed model information
- Get API key: https://aistudio.google.com/apikey
- Documentation: https://ai.google.dev/gemini-api
