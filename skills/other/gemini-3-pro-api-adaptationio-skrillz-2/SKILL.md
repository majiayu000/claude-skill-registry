---
name: gemini-3-pro-api
description: Gemini 3 Pro API/SDK integration for text generation, reasoning, and chat. Covers setup, authentication, thinking levels, streaming, and production deployment. Use when working with Gemini 3 Pro API, Python SDK, Node.js SDK, text generation, chat applications, or advanced reasoning tasks.
---

# Gemini 3 Pro API Integration

Comprehensive guide for integrating Google's Gemini 3 Pro API/SDK into your applications. Covers setup, authentication, text generation, advanced reasoning with dynamic thinking, chat applications, streaming responses, and production deployment patterns.

## Overview

**Gemini 3 Pro** (`gemini-3-pro-preview`) is Google's most intelligent model designed for complex tasks requiring advanced reasoning and broad world knowledge. This skill provides complete workflows for API integration using Python or Node.js SDKs.

### Key Capabilities

- **Massive Context:** 1M token input, 64k token output
- **Dynamic Thinking:** Adaptive reasoning with high/low modes
- **Streaming:** Real-time token delivery
- **Chat:** Multi-turn conversations with history
- **Production-Ready:** Error handling, retry logic, cost optimization

### When to Use This Skill

- Setting up Gemini 3 Pro API access
- Building text generation applications
- Implementing chat applications with reasoning
- Configuring advanced thinking modes
- Deploying production Gemini applications
- Optimizing API usage and costs

---

## Quick Start

### Prerequisites

- **API Key:** Get from [Google AI Studio](https://aistudio.google.com/)
- **Python 3.9+** or **Node.js 18+**

### Python Quick Start

```python
# Install SDK
pip install google-genai

# Basic usage
import google.generativeai as genai

genai.configure(api_key="YOUR_API_KEY")
model = genai.GenerativeModel("gemini-3-pro-preview")

response = model.generate_content("Explain quantum computing")
print(response.text)
```

### Node.js Quick Start

```typescript
// Install SDK
npm install @google/generative-ai

// Basic usage
import { GoogleGenerativeAI } from "@google/generative-ai";

const genAI = new GoogleGenerativeAI("YOUR_API_KEY");
const model = genAI.getGenerativeModel({ model: "gemini-3-pro-preview" });

const result = await model.generateContent("Explain quantum computing");
console.log(result.response.text());
```

---

## Core Workflows

### Workflow 1: Quick Start Setup

**Goal:** Get from zero to first successful API call in < 5 minutes.

**Steps:**

1. **Get API Key**
   - Visit [Google AI Studio](https://aistudio.google.com/)
   - Create or select project
   - Generate API key
   - Copy key securely

2. **Install SDK**
   ```bash
   # Python
   pip install google-genai

   # Node.js
   npm install @google/generative-ai
   ```

3. **Configure Authentication**
   ```python
   # Python - using environment variable (recommended)
   import os
   import google.generativeai as genai

   genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
   ```

   ```typescript
   // Node.js - using environment variable (recommended)
   const genAI = new GoogleGenerativeAI(process.env.GEMINI_API_KEY);
   ```

4. **Make First API Call**
   ```python
   # Python
   model = genai.GenerativeModel("gemini-3-pro-preview")
   response = model.generate_content("Write a haiku about coding")
   print(response.text)
   ```

5. **Verify Success**
   - Check response received
   - Verify text output
   - Note token usage
   - Confirm API key working

**Expected Outcome:** Working API integration in under 5 minutes.

---

### Workflow 2: Chat Application Development

**Goal:** Build a production-ready chat application with conversation history and streaming.

**Steps:**

1. **Initialize Chat Model**
   ```python
   # Python
   model = genai.GenerativeModel(
       "gemini-3-pro-preview",
       generation_config={
           "thinking_level": "high",  # Dynamic reasoning
           "temperature": 1.0,  # Keep at 1.0 for best results
           "max_output_tokens": 8192
       }
   )
   ```

2. **Start Chat Session**
   ```python
   chat = model.start_chat(history=[])
   ```

3. **Send Message with Streaming**
   ```python
   response = chat.send_message(
       "Explain how neural networks learn",
       stream=True
   )

   # Stream tokens in real-time
   for chunk in response:
       print(chunk.text, end="", flush=True)
   ```

4. **Manage Conversation History**
   ```python
   # History is automatically maintained
   # Access it anytime
   print(f"Conversation turns: {len(chat.history)}")

   # Continue conversation
   response = chat.send_message("Can you give an example?")
   ```

5. **Handle Thought Signatures**
   - SDKs handle automatically in standard chat flows
   - No manual intervention needed for basic use
   - See `references/thought-signatures.md` for advanced cases

6. **Implement Error Handling**
   ```python
   import time
   from google.api_core import retry, exceptions

   @retry.Retry(predicate=retry.if_exception_type(
       exceptions.ResourceExhausted,
       exceptions.ServiceUnavailable
   ))
   def send_with_retry(chat, message):
       return chat.send_message(message)

   try:
       response = send_with_retry(chat, user_input)
   except exceptions.GoogleAPIError as e:
       print(f"API error: {e}")
   ```

**Expected Outcome:** Production-ready chat application with streaming, history, and error handling.

---

### Workflow 3: Production Deployment

**Goal:** Deploy Gemini 3 Pro integration with monitoring, cost control, and reliability.

**Steps:**

1. **Setup Authentication (Production)**
   ```python
   # Use environment variables (never hardcode keys)
   import os
   from pathlib import Path

   # Option 1: Environment variable
   api_key = os.getenv("GEMINI_API_KEY")

   # Option 2: Secrets manager (recommended for production)
   # Use Google Secret Manager, AWS Secrets Manager, etc.
   ```

2. **Configure Production Settings**
   ```python
   model = genai.GenerativeModel(
       "gemini-3-pro-preview",
       generation_config={
           "thinking_level": "high",  # or "low" for simple tasks
           "temperature": 1.0,  # CRITICAL: Keep at 1.0
           "max_output_tokens": 4096,
           "top_p": 0.95,
           "top_k": 40
       },
       safety_settings={
           # Configure content filtering as needed
       }
   )
   ```

3. **Implement Comprehensive Error Handling**
   ```python
   from google.api_core import exceptions, retry
   import logging

   logging.basicConfig(level=logging.INFO)
   logger = logging.getLogger(__name__)

   def generate_with_fallback(prompt, max_retries=3):
       @retry.Retry(
           predicate=retry.if_exception_type(
               exceptions.ResourceExhausted,
               exceptions.ServiceUnavailable,
               exceptions.DeadlineExceeded
           ),
           initial=1.0,
           maximum=10.0,
           multiplier=2.0,
           deadline=60.0
       )
       def _generate():
           return model.generate_content(prompt)

       try:
           return _generate()
       except exceptions.InvalidArgument as e:
           logger.error(f"Invalid argument: {e}")
           raise
       except exceptions.PermissionDenied as e:
           logger.error(f"Permission denied: {e}")
           raise
       except Exception as e:
           logger.error(f"Unexpected error: {e}")
           # Fallback to simpler model or cached response
           return None
   ```

4. **Monitor Usage and Costs**
   ```python
   def log_usage(response):
       usage = response.usage_metadata
       logger.info(f"Tokens - Input: {usage.prompt_token_count}, "
                   f"Output: {usage.candidates_token_count}, "
                   f"Total: {usage.total_token_count}")

       # Estimate cost (for prompts ≤200k tokens)
       input_cost = (usage.prompt_token_count / 1_000_000) * 2.00
       output_cost = (usage.candidates_token_count / 1_000_000) * 12.00
       total_cost = input_cost + output_cost

       logger.info(f"Estimated cost: ${total_cost:.6f}")

   response = model.generate_content(prompt)
   log_usage(response)
   ```

5. **Implement Rate Limiting**
   ```python
   import time
   from collections import deque

   class RateLimiter:
       def __init__(self, max_requests_per_minute=60):
           self.max_rpm = max_requests_per_minute
           self.requests = deque()

       def wait_if_needed(self):
           now = time.time()
           # Remove requests older than 1 minute
           while self.requests and self.requests[0] < now - 60:
               self.requests.popleft()

           # Check if at limit
           if len(self.requests) >= self.max_rpm:
               sleep_time = 60 - (now - self.requests[0])
               if sleep_time > 0:
                   time.sleep(sleep_time)

           self.requests.append(now)

   limiter = RateLimiter(max_requests_per_minute=60)

   def generate_with_rate_limit(prompt):
       limiter.wait_if_needed()
       return model.generate_content(prompt)
   ```

6. **Setup Logging and Monitoring**
   ```python
   import logging
   from datetime import datetime

   # Configure logging
   logging.basicConfig(
       level=logging.INFO,
       format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
       handlers=[
           logging.FileHandler('gemini_api.log'),
           logging.StreamHandler()
       ]
   )

   logger = logging.getLogger(__name__)

   def monitored_generate(prompt):
       start_time = datetime.now()
       try:
           response = model.generate_content(prompt)
           duration = (datetime.now() - start_time).total_seconds()

           logger.info(f"Success - Duration: {duration}s, "
                       f"Tokens: {response.usage_metadata.total_token_count}")
           return response
       except Exception as e:
           duration = (datetime.now() - start_time).total_seconds()
           logger.error(f"Failed - Duration: {duration}s, Error: {e}")
           raise
   ```

**Expected Outcome:** Production-ready deployment with monitoring, cost control, error handling, and rate limiting.

---

## Thinking Levels

### Dynamic Thinking System

Gemini 3 Pro introduces `thinking_level` to control reasoning depth:

**`thinking_level: "high"` (default)**
- Maximum reasoning depth
- Best quality for complex tasks
- Slower first-token response
- Higher cost
- **Use for:** Complex reasoning, coding, analysis, research

**`thinking_level: "low"`**
- Minimal reasoning overhead
- Faster response
- Lower cost
- Simpler output
- **Use for:** Simple questions, factual answers, quick queries

### Configuration

```python
# Python
model = genai.GenerativeModel(
    "gemini-3-pro-preview",
    generation_config={
        "thinking_level": "high"  # or "low"
    }
)
```

```typescript
// Node.js
const model = genAI.getGenerativeModel({
  model: "gemini-3-pro-preview",
  generationConfig: {
    thinking_level: "high"  // or "low"
  }
});
```

### Critical Notes

⚠️ **Temperature MUST stay at 1.0** - Changing temperature can cause looping or degraded performance on complex reasoning tasks.

⚠️ **Cannot combine** `thinking_level` with legacy `thinking_budget` parameter.

See `references/thinking-levels.md` for detailed guide.

---

## Streaming Responses

### Python Streaming

```python
response = model.generate_content(
    "Write a long article about AI",
    stream=True
)

for chunk in response:
    print(chunk.text, end="", flush=True)
```

### Node.js Streaming

```typescript
const result = await model.generateContentStream("Write a long article about AI");

for await (const chunk of result.stream) {
    process.stdout.write(chunk.text());
}
```

### Benefits

- Lower perceived latency
- Real-time user feedback
- Better UX for long responses
- Can process tokens as they arrive

See `references/streaming.md` for advanced patterns.

---

## Cost Optimization

### Pricing (Gemini 3 Pro)

| Context Size | Input | Output |
|-------------|-------|--------|
| ≤ 200k tokens | $2/1M | $12/1M |
| > 200k tokens | $4/1M | $18/1M |

### Optimization Strategies

1. **Keep prompts under 200k tokens** (50% cheaper)
2. **Use `thinking_level: "low"` for simple tasks** (faster, lower cost)
3. **Implement context caching** for reusable contexts (see `gemini-3-advanced` skill)
4. **Monitor token usage** and set budgets
5. **Use Gemini 1.5 Flash** for simple tasks (20x cheaper)

See `references/best-practices.md` for comprehensive cost optimization.

---

## Model Selection

### Gemini 3 Pro vs Other Models

| Model | Context | Output | Input Price | Best For |
|-------|---------|--------|-------------|----------|
| **gemini-3-pro-preview** | 1M | 64k | $2-4/1M | Complex reasoning, coding |
| gemini-1.5-pro | 1M | 8k | $7-14/1M | General use, multimodal |
| gemini-1.5-flash | 1M | 8k | $0.35-0.70/1M | Simple tasks, cost-sensitive |

### When to Use Gemini 3 Pro

✅ Complex reasoning tasks
✅ Advanced coding problems
✅ Long-context analysis (up to 1M tokens)
✅ Large output requirements (up to 64k tokens)
✅ Tasks requiring dynamic thinking

### When to Use Alternatives

- **Gemini 1.5 Flash:** Simple tasks, cost-sensitive applications
- **Gemini 1.5 Pro:** Multimodal tasks, general use
- **Gemini 2.5 models:** Experimental features, specific capabilities

---

## Error Handling

### Common Errors

| Error | Cause | Solution |
|-------|-------|----------|
| `ResourceExhausted` | Rate limit exceeded | Implement retry with backoff |
| `InvalidArgument` | Invalid parameters | Validate input, check docs |
| `PermissionDenied` | Invalid API key | Check authentication |
| `DeadlineExceeded` | Request timeout | Reduce context, retry |

### Production Error Handling

```python
from google.api_core import exceptions, retry

@retry.Retry(
    predicate=retry.if_exception_type(
        exceptions.ResourceExhausted,
        exceptions.ServiceUnavailable
    ),
    initial=1.0,
    maximum=60.0,
    multiplier=2.0
)
def safe_generate(prompt):
    try:
        return model.generate_content(prompt)
    except exceptions.InvalidArgument as e:
        logger.error(f"Invalid argument: {e}")
        raise
    except exceptions.PermissionDenied as e:
        logger.error(f"Permission denied - check API key: {e}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        raise
```

See `references/error-handling.md` for comprehensive patterns.

---

## References

**Setup & Configuration**
- [Setup Guide](references/setup-guide.md) - Installation, authentication, configuration
- [Best Practices](references/best-practices.md) - Optimization, cost control, tips

**Features**
- [Text Generation](references/text-generation.md) - Detailed text generation patterns
- [Chat Patterns](references/chat-patterns.md) - Chat conversation management
- [Thinking Levels](references/thinking-levels.md) - Dynamic thinking system guide
- [Streaming](references/streaming.md) - Streaming response patterns

**Production**
- [Error Handling](references/error-handling.md) - Error handling and retry strategies

**Official Resources**
- [Gemini 3 Documentation](https://ai.google.dev/gemini-api/docs/gemini-3)
- [Python SDK Docs](https://googleapis.github.io/python-genai/)
- [Node.js SDK Docs](https://github.com/google/generative-ai-js)
- [API Reference](https://ai.google.dev/gemini-api/docs)
- [Pricing](https://ai.google.dev/pricing)

---

## Next Steps

### After Basic Setup

1. **Explore chat applications** - Build conversational interfaces
2. **Add multimodal capabilities** - Use `gemini-3-multimodal` skill
3. **Add image generation** - Use `gemini-3-image-generation` skill
4. **Add advanced features** - Use `gemini-3-advanced` skill (caching, tools, batch)

### Common Integration Patterns

- **Simple Chatbot:** This skill only
- **Multimodal Assistant:** This skill + `gemini-3-multimodal`
- **Creative Bot:** This skill + `gemini-3-image-generation`
- **Production App:** All 4 Gemini 3 skills

---

## Troubleshooting

### Issue: API key not working
**Solution:** Verify API key in Google AI Studio, check environment variable

### Issue: Rate limit errors
**Solution:** Implement rate limiting, upgrade to paid tier, reduce request frequency

### Issue: Slow responses
**Solution:** Use `thinking_level: "low"` for simple tasks, enable streaming, reduce context size

### Issue: High costs
**Solution:** Keep prompts under 200k tokens, use appropriate thinking level, consider Gemini 1.5 Flash for simple tasks

### Issue: Temperature warnings
**Solution:** Keep temperature at 1.0 (default) - do not modify for complex reasoning tasks

---

## Summary

This skill provides everything needed to integrate Gemini 3 Pro API into your applications:

✅ Quick setup (< 5 minutes)
✅ Production-ready chat applications
✅ Dynamic thinking configuration
✅ Streaming responses
✅ Error handling and retry logic
✅ Cost optimization strategies
✅ Monitoring and logging patterns

For multimodal, image generation, and advanced features, see the companion skills.

**Ready to build?** Start with **Workflow 1: Quick Start Setup** above!
