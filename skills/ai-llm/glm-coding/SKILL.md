---
name: glm-coding
description: This skill provides specialized knowledge for integrating and using GLM-4.7 Coding Plan API (智谱编程套餐). Use this skill when working with GLM-4.7 for prompt optimization, code generation, or technical documentation tasks. GLM-4.7 uses a unique response format with reasoning_content field and requires special endpoint handling.
---

# GLM-4.7 Coding Plan Integration

This skill provides specialized knowledge for integrating and using GLM-4.7 Coding Plan API (智谱编程套餐) from Zhipu AI (智谱AI).

## Purpose

GLM-4.7 Coding Plan is a specialized OpenAI-compatible API designed for programming and code-related tasks. This skill covers:
- API integration with correct endpoint format
- Response format handling (`reasoning_content` vs `content`)
- Performance characteristics and optimization strategies
- Best practices for prompt optimization

## When to Use This Skill

Use this skill when:
- Integrating GLM-4.7 Coding Plan API into applications
- Troubleshooting GLM API connection or response issues
- Optimizing prompts for video generation or other tasks
- Comparing GLM with other AI providers (DeepSeek, etc.)

## API Integration

### Endpoint Format (⚠️ Critical Difference)

GLM-4.7 Coding Plan uses a **non-standard endpoint format**:

```
Base URL: https://open.bigmodel.cn/api/coding/paas/v4
Full Endpoint: https://open.bigmodel.cn/api/coding/paas/v4/chat/completions
```

**Key Difference**: No `/v1` prefix, directly `/chat/completions`

**Example** (openaiClient.js):
```javascript
// ❌ Wrong: Standard OpenAI format
const baseURL = 'https://api.openai.com/v1';
const endpoint = '/chat/completions';

// ✅ Correct: GLM Coding Plan format
const baseURL = 'https://open.bigmodel.cn/api/coding/paas/v4';
const endpoint = '/chat/completions';  // No /v1 prefix
const url = `${baseURL}${endpoint}`;  // Final: https://open.bigmodel.cn/api/coding/paas/v4/chat/completions
```

### Response Format Handling (⚠️ Critical)

GLM-4.7 returns content in `reasoning_content` field, **NOT** the standard OpenAI `content` field:

```javascript
// Response structure from GLM-4.7
{
  "choices": [{
    "message": {
      "content": "",           // ⚠️ Empty
      "reasoning_content": "Actual content here",  // ✅ Real content
      "role": "assistant"
    }
  }]
}

// ❌ Wrong: Only reads content field
const result = response.data.choices[0].message.content;
// Result: "" (empty string)

// ✅ Correct: Compatible with both formats
const message = response.data.choices[0].message;
const result = message.content || message.reasoning_content || '';
```

**Implementation Example** (openaiClient.js - Lines 111, 170):
```javascript
// In optimizePrompt method (Line 111)
const message = response.data.choices[0].message;
const result = message.content || message.reasoning_content || '';

// In testConnection method (Line 170)
const message = response.data.choices[0].message;
const result = message.content || message.reasoning_content || '';
```

### API Key Format

GLM API keys use a special format: `{id}.{key}`

**Example**: `xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`

**Storage** (per-service in localStorage):
```javascript
// Store API keys per service
const apiKeys = JSON.parse(localStorage.getItem('winjin-openai-keys') || '{}');
apiKeys['glm_coding'] = userApiKey;
localStorage.setItem('winjin-openai-keys', JSON.stringify(apiKeys));

// Retrieve
const apiKeys = JSON.parse(localStorage.getItem('winjin-openai-keys') || '{}');
const apiKey = apiKeys['glm_coding'] || '';
```

## Performance Characteristics

Based on production testing (10 optimization requests):

| Metric | Value | Notes |
|--------|-------|-------|
| **Response Time** | ~60 seconds | Significantly slower than other providers |
| **Token Usage** | ~2,339 tokens/request | Higher consumption for optimization tasks |
| **Success Rate** | 100% (10/10) | Reliable when format is handled correctly |
| **Model** | GLM-4.7 (only option) | Coding Plan has only one model |

**Timeout Configuration**:
```javascript
// Set longer timeout for GLM requests (120 seconds)
const response = await axios.post(url, body, {
  timeout: 120000,  // 2 minutes
  headers: {
    'Authorization': `Bearer ${apiKey}`,
    'Content-Type': 'application/json'
  }
});
```

## Use Cases

### 1. Prompt Optimization (picture-book style)

**Tested and working** - GLM-4.7 successfully optimizes prompts for video generation:

**Request Example**:
```json
{
  "base_url": "https://open.bigmodel.cn/api/coding/paas/v4",
  "api_key": "your_api_key_here",
  "model": "GLM-4.7",
  "prompt": "@b2e75200f.pennypuf 在海边玩耍",
  "style": "picture-book",
  "context": {
    "target_duration": 10,
    "characters": []
  }
}
```

**Response Example**:
```json
{
  "success": true,
  "data": {
    "optimized_prompt": "卡通绘本风格的视频，一只拟人化的海鹦鹉正站在海边湿润的岩石上...",
    "meta": {
      "model_used": "GLM-4.7",
      "style": "picture-book",
      "tokens_used": 2311
    }
  }
}
```

### 2. Code Generation and Optimization

GLM-4.7 is designed for programming tasks:
- Code review and refactoring
- Bug fixing and optimization
- Technical documentation generation

### 3. Technical Documentation

Auto-generating documentation from code:
- API documentation
- Code comments and explanations
- Architecture descriptions

## Known Limitations

⚠️ **Performance Issues**:
- **Slow response time** (~60 seconds per request)
- **Not suitable for real-time interactions**
- **Better suited for batch processing**

⚠️ **Quality Concerns**:
- **Optimization quality is average** (user feedback: "GLM效果不好")
- Consider alternatives like DeepSeek for better quality
- Use GLM when cost is a priority over quality

⚠️ **Token Consumption**:
- Higher token usage compared to alternatives
- May not be cost-effective for large-scale applications

## Best Practices

### 1. Use for Batch Processing

GLM-4.7 is best suited for non-interactive, background tasks:

```javascript
// ✅ Good: Background batch processing
async function batchOptimizePrompts(prompts) {
  const results = [];
  for (const prompt of prompts) {
    const result = await glmClient.optimize(prompt);
    results.push(result);
  }
  return results;
}

// ❌ Bad: Real-time user interaction
async function handleUserChat(message) {
  // User waits 60+ seconds - poor UX
  const response = await glmClient.chat(message);
  return response;
}
```

### 2. Implement Retry Logic

Due to slower response times, implement retry logic:

```javascript
async function callGLMWithRetry(request, maxRetries = 3) {
  for (let i = 0; i < maxRetries; i++) {
    try {
      const response = await axios.post(url, request, {
        timeout: 120000  // 2 minutes
      });
      return response.data;
    } catch (error) {
      if (i === maxRetries - 1) throw error;
      await new Promise(r => setTimeout(r, 5000 * (i + 1)));  // Exponential backoff
    }
  }
}
```

### 3. Fallback Strategy

Consider implementing fallback to alternative providers:

```javascript
const PROVIDERS = {
  deepseek: { priority: 1, quality: 'high', speed: 'fast' },
  glm_coding: { priority: 2, quality: 'medium', speed: 'slow' }
};

async function optimizeWithFallback(prompt) {
  // Try DeepSeek first (faster, better quality)
  try {
    return await callDeepSeek(prompt);
  } catch (error) {
    console.warn('DeepSeek failed, falling back to GLM');
    return await callGLM(prompt);
  }
}
```

## Comparison with Alternatives

| Feature | GLM-4.7 Coding | DeepSeek | [ge2.5] |
|---------|---------------|----------|----------|
| **Speed** | Slow (~60s) | Fast (~10s) | Fast (~15s) |
| **Quality** | Average | Good | Good |
| **Cost** | Lower | Higher | - |
| **Use Case** | Batch tasks | Real-time | Real-time |
| **Response Format** | `reasoning_content` | `content` | `content` |

## Troubleshooting

### Problem: Empty response from GLM

**Symptom**: API returns success but `result` is empty string

**Root Cause**: Reading `message.content` instead of `message.reasoning_content`

**Solution**:
```javascript
// ❌ Wrong
const result = response.data.choices[0].message.content;

// ✅ Correct
const message = response.data.choices[0].message;
const result = message.content || message.reasoning_content || '';
```

### Problem: Timeout errors

**Symptom**: Request timeout after 30 seconds

**Root Cause**: GLM-4.7 needs more time to process (reasoning step)

**Solution**: Increase timeout to 120 seconds
```javascript
await axios.post(url, body, { timeout: 120000 });
```

### Problem: 404 Not Found

**Symptom**: API returns 404 error

**Root Cause**: Using wrong endpoint format

**Solution**: Verify endpoint is `/chat/completions` without `/v1` prefix
```javascript
// ✅ Correct
const url = 'https://open.bigmodel.cn/api/coding/paas/v4/chat/completions';

// ❌ Wrong
const url = 'https://open.bigmodel.cn/api/coding/paas/v4/v1/chat/completions';
```

## References

See `references/glm_integration.md` for:
- Complete API specification
- Error handling patterns
- Example implementations

## Scripts

See `scripts/` for:
- `test_glm_connection.py` - Test GLM API connectivity
- `benchmark_prompts.py` - Benchmark prompt optimization
