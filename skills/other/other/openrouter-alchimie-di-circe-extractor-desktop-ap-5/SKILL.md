---
name: openrouter
description: OpenRouter API - Unified access to 400+ AI models through one API
---

# OpenRouter Skill

Comprehensive assistance with OpenRouter API development, providing unified access to hundreds of AI models through a single endpoint with intelligent routing, automatic fallbacks, and standardized interfaces.

## When to Use This Skill

This skill should be triggered when:
- Making API calls to multiple AI model providers through a unified interface
- Implementing model fallback strategies or auto-routing
- Working with OpenAI-compatible SDKs but targeting multiple providers
- Configuring advanced sampling parameters (temperature, top_p, penalties)
- Setting up streaming responses or structured JSON outputs
- Comparing costs across different AI models
- Building applications that need automatic provider failover
- Implementing function/tool calling across different models
- Questions about OpenRouter-specific features (routing, fallbacks, zero completion insurance)

## Quick Reference

### Basic Chat Completion (Python)
```python
from openai import OpenAI

client = OpenAI(
  base_url="https://openrouter.ai/api/v1",
  api_key="<OPENROUTER_API_KEY>",
)

completion = client.chat.completions.create(
  model="openai/gpt-4o",
  messages=[{"role": "user", "content": "What is the meaning of life?"}]
)
print(completion.choices[0].message.content)
```

### Basic Chat Completion (JavaScript/TypeScript)
```typescript
import OpenAI from 'openai';

const openai = new OpenAI({
  baseURL: 'https://openrouter.ai/api/v1',
  apiKey: '<OPENROUTER_API_KEY>',
});

const completion = await openai.chat.completions.create({
  model: 'openai/gpt-4o',
  messages: [{"role": 'user', "content": 'What is the meaning of life?'}],
});
console.log(completion.choices[0].message);
```

### cURL Request
```bash
curl https://openrouter.ai/api/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $OPENROUTER_API_KEY" \
  -d '{
    "model": "openai/gpt-4o",
    "messages": [{"role": "user", "content": "What is the meaning of life?"}]
  }'
```

### Model Fallback Configuration (Python)
```python
completion = client.chat.completions.create(
    model="openai/gpt-4o",
    extra_body={
        "models": ["anthropic/claude-3.5-sonnet", "gryphe/mythomax-l2-13b"],
    },
    messages=[{"role": "user", "content": "Your prompt here"}]
)
```

### Model Fallback Configuration (TypeScript)
```typescript
const completion = await client.chat.completions.create({
    model: 'openai/gpt-4o',
    models: ['anthropic/claude-3.5-sonnet', 'gryphe/mythomax-l2-13b'],
    messages: [{ role: 'user', content: 'Your prompt here' }],
});
```

### Auto Router (Dynamic Model Selection)
```python
completion = client.chat.completions.create(
    model="openrouter/auto",  # Automatically selects best model for the prompt
    messages=[{"role": "user", "content": "Your prompt here"}]
)
```

### Advanced Parameters Example
```python
completion = client.chat.completions.create(
    model="openai/gpt-4o",
    messages=[{"role": "user", "content": "Write a creative story"}],
    temperature=0.8,           # Higher for creativity (0.0-2.0)
    max_tokens=500,            # Limit response length
    top_p=0.9,                 # Nucleus sampling (0.0-1.0)
    frequency_penalty=0.5,     # Reduce repetition (-2.0-2.0)
    presence_penalty=0.3       # Encourage topic diversity (-2.0-2.0)
)
```

### Streaming Response
```python
stream = client.chat.completions.create(
    model="openai/gpt-4o",
    messages=[{"role": "user", "content": "Tell me a story"}],
    stream=True
)

for chunk in stream:
    if chunk.choices[0].delta.content:
        print(chunk.choices[0].delta.content, end='')
```

### JSON Mode (Structured Output)
```python
completion = client.chat.completions.create(
    model="openai/gpt-4o",
    messages=[{
        "role": "user",
        "content": "Extract person's name, age, and city from: John is 30 and lives in NYC"
    }],
    response_format={"type": "json_object"}
)
```

### Deterministic Output with Seed
```python
completion = client.chat.completions.create(
    model="openai/gpt-4o",
    messages=[{"role": "user", "content": "Generate a random number"}],
    seed=42,            # Same seed = same output (when supported)
    temperature=0.0     # Deterministic sampling
)
```

## Key Concepts

### Model Routing
OpenRouter provides intelligent routing capabilities:
- **Auto Router** (`openrouter/auto`): Automatically selects the best model based on your prompt using NotDiamond
- **Fallback Models**: Specify multiple models that automatically retry if primary fails
- **Provider Routing**: Automatically routes across providers for reliability

### Authentication
- Uses Bearer token authentication with API keys
- API keys can be managed programmatically
- Compatible with OpenAI SDK authentication patterns

### Model Naming Convention
Models use the format `provider/model-name`:
- `openai/gpt-4o` - OpenAI's GPT-4 Optimized
- `anthropic/claude-3.5-sonnet` - Anthropic's Claude 3.5 Sonnet
- `google/gemini-2.0-flash-exp:free` - Google's free Gemini model
- `openrouter/auto` - Auto-routing system

### Sampling Parameters

**Temperature** (0.0-2.0, default: 1.0)
- Lower = more predictable, focused responses
- Higher = more creative, diverse responses
- Use low (0.0-0.3) for factual tasks, high (0.8-1.5) for creative work

**Top P** (0.0-1.0, default: 1.0)
- Limits choices to percentage of likely tokens
- Dynamic filtering of improbable options
- Balance between consistency and variety

**Frequency/Presence Penalties** (-2.0-2.0, default: 0.0)
- Frequency: Discourages repeating tokens proportional to use
- Presence: Simpler penalty not scaled by count
- Positive values reduce repetition, negative encourage reuse

**Max Tokens** (integer)
- Sets maximum response length
- Cannot exceed context length minus prompt length
- Use to control costs and enforce concise replies

### Response Formats
- **Standard JSON**: Default chat completion format
- **Streaming**: Server-Sent Events (SSE) with `stream: true`
- **JSON Mode**: Guaranteed valid JSON with `response_format: {"type": "json_object"}`
- **Structured Outputs**: Schema-validated JSON responses

### Advanced Features
- **Tool/Function Calling**: Connect models to external APIs
- **Multimodal Inputs**: Support for images, PDFs, audio
- **Prompt Caching**: Reduce costs for repeated prompts
- **Web Search Integration**: Enhanced responses with web data
- **Zero Completion Insurance**: Protection against failed responses
- **Logprobs**: Access token probabilities for confidence analysis

## Reference Files

This skill includes comprehensive documentation in `references/`:

- **llms-full.md** - Complete list of available models with metadata
- **llms-small.md** - Curated subset of popular models
- **llms.md** - Standard model listings

Use `view` to read specific reference files when detailed model information is needed.

## Working with This Skill

### For Beginners
1. Start with basic chat completion examples (Python/JavaScript/cURL above)
2. Use the standard OpenAI SDK for easy integration
3. Try simple model names like `openai/gpt-4o` or `anthropic/claude-3.5-sonnet`
4. Keep parameters simple initially (just model and messages)

### For Intermediate Users
1. Implement model fallback arrays for reliability
2. Experiment with sampling parameters (temperature, top_p)
3. Use streaming for better UX in conversational apps
4. Try `openrouter/auto` for automatic model selection
5. Implement JSON mode for structured data extraction

### For Advanced Users
1. Fine-tune multiple sampling parameters together
2. Implement custom routing logic with fallback chains
3. Use logprobs for confidence scoring
4. Leverage tool/function calling capabilities
5. Optimize costs by selecting appropriate models per task
6. Implement prompt caching strategies
7. Use seed parameter for reproducible testing

## Common Patterns

### Error Handling with Fallbacks
```python
try:
    completion = client.chat.completions.create(
        model="openai/gpt-4o",
        extra_body={
            "models": [
                "anthropic/claude-3.5-sonnet",
                "google/gemini-2.0-flash-exp:free"
            ]
        },
        messages=[{"role": "user", "content": "Your prompt"}]
    )
except Exception as e:
    print(f"All models failed: {e}")
```

### Cost-Optimized Routing
```python
# Use cheaper models for simple tasks
simple_completion = client.chat.completions.create(
    model="google/gemini-2.0-flash-exp:free",
    messages=[{"role": "user", "content": "Simple question"}]
)

# Use premium models for complex tasks
complex_completion = client.chat.completions.create(
    model="openai/o1",
    messages=[{"role": "user", "content": "Complex reasoning task"}]
)
```

### Context-Aware Temperature
```python
# Low temperature for factual responses
factual = client.chat.completions.create(
    model="openai/gpt-4o",
    temperature=0.2,
    messages=[{"role": "user", "content": "What is the capital of France?"}]
)

# High temperature for creative content
creative = client.chat.completions.create(
    model="openai/gpt-4o",
    temperature=1.2,
    messages=[{"role": "user", "content": "Write a unique story opening"}]
)
```

## Resources

### Official Documentation
- API Reference: https://openrouter.ai/docs/api-reference/overview
- Quickstart Guide: https://openrouter.ai/docs/quickstart
- Model List: https://openrouter.ai/docs/models
- Parameters Guide: https://openrouter.ai/docs/api-reference/parameters

### Key Endpoints
- Chat Completions: `POST https://openrouter.ai/api/v1/chat/completions`
- List Models: `GET https://openrouter.ai/api/v1/models`
- Generation Info: `GET https://openrouter.ai/api/v1/generation`

## Notes

- OpenRouter normalizes API schemas across all providers
- Uses OpenAI-compatible API format for easy migration
- Automatic provider fallback if models are rate-limited or down
- Pricing based on actual model used (important for fallbacks)
- Response includes metadata about which model processed the request
- All models support streaming via Server-Sent Events
- Compatible with popular frameworks (LangChain, Vercel AI SDK, etc.)

## Best Practices

1. **Always implement fallbacks** for production applications
2. **Use appropriate temperature** based on task type (low for factual, high for creative)
3. **Set max_tokens** to control costs and response length
4. **Enable streaming** for better user experience in chat applications
5. **Use JSON mode** when you need guaranteed structured output
6. **Test with seed parameter** for reproducible results during development
7. **Monitor costs** by selecting appropriate models per task
8. **Use auto-routing** when unsure which model performs best
9. **Implement proper error handling** for rate limits and failures
10. **Cache prompts** for repeated requests to reduce costs
