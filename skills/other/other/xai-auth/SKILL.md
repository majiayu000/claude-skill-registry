---
name: xai-auth
description: xAI Grok API authentication and setup. Use when configuring xAI API access, setting up API keys, or troubleshooting authentication issues.
version: 1.0.0
---

# xAI Grok API Authentication

Complete guide for setting up and managing xAI API authentication for Grok models with Twitter/X integration.

## Quick Start

### 1. Get API Key
1. Go to [console.x.ai](https://console.x.ai)
2. Sign in with your X (Twitter) account
3. Navigate to "API Keys" section
4. Click "Create API Key"
5. Copy and save the key (starts with `xai-`)

### 2. Set Environment Variable
```bash
# Add to .bashrc, .zshrc, or .env
export XAI_API_KEY="xai-your-key-here"
```

### 3. Test Connection
```bash
curl https://api.x.ai/v1/models \
  -H "Authorization: Bearer $XAI_API_KEY"
```

## Authentication Methods

### Method 1: Environment Variable (Recommended)
```python
import os
from openai import OpenAI

client = OpenAI(
    api_key=os.getenv("XAI_API_KEY"),
    base_url="https://api.x.ai/v1"
)
```

### Method 2: Direct Key
```python
from openai import OpenAI

client = OpenAI(
    api_key="xai-your-key-here",
    base_url="https://api.x.ai/v1"
)
```

### Method 3: Using xai-sdk
```python
from xai_sdk import Client

client = Client(api_key=os.getenv("XAI_API_KEY"))
```

## API Compatibility

xAI API is **fully compatible with OpenAI SDK**:

```python
# Just change base_url - everything else works the same
from openai import OpenAI

client = OpenAI(
    api_key=os.getenv("XAI_API_KEY"),
    base_url="https://api.x.ai/v1"  # Only difference
)

response = client.chat.completions.create(
    model="grok-3-fast",  # Use Grok models
    messages=[{"role": "user", "content": "Hello!"}]
)
```

## Free Credits

### $150/Month Free Credits
1. Go to [console.x.ai](https://console.x.ai)
2. Navigate to Settings → Data Sharing
3. Enable data sharing opt-in
4. Receive $150/month in API credits

### Credit Usage
| Action | Cost |
|--------|------|
| Grok 4.1 Fast (input) | $0.20/1M tokens |
| Grok 4.1 Fast (output) | $0.50/1M tokens |
| X Search / Web Search | $5/1,000 calls |
| Code Execution | $5/1,000 calls |

## Configuration File

Create `.env.xai`:
```bash
# xAI API Configuration
XAI_API_KEY=xai-your-key-here
XAI_BASE_URL=https://api.x.ai/v1
XAI_DEFAULT_MODEL=grok-3-fast
```

## Error Handling

### Common Errors

| Error | Cause | Solution |
|-------|-------|----------|
| `no credits` | No credits on account | Add credits or enable free tier |
| `invalid_api_key` | Wrong or expired key | Generate new key at console.x.ai |
| `rate_limit_exceeded` | Too many requests | Implement backoff, reduce frequency |
| `model_not_found` | Invalid model name | Check available models |

### Python Error Handling
```python
from openai import OpenAI, APIError, RateLimitError

client = OpenAI(
    api_key=os.getenv("XAI_API_KEY"),
    base_url="https://api.x.ai/v1"
)

try:
    response = client.chat.completions.create(
        model="grok-3-fast",
        messages=[{"role": "user", "content": "Hello"}]
    )
except RateLimitError:
    print("Rate limit hit, waiting...")
    time.sleep(60)
except APIError as e:
    print(f"API error: {e}")
```

## Security Best Practices

1. **Never commit API keys** to git
2. **Use environment variables** instead of hardcoding
3. **Rotate keys regularly** via console.x.ai
4. **Use separate keys** for dev/prod environments
5. **Add to .gitignore**:
   ```
   .env
   .env.*
   **/secrets.*
   ```

## Rate Limits

| Model | Requests/Min | Tokens/Min |
|-------|--------------|------------|
| Grok 4.1 Fast | 60 | 100,000 |
| Grok 4 | 30 | 50,000 |
| Grok 3 Mini | 100 | 200,000 |

## Endpoints

| Endpoint | Description |
|----------|-------------|
| `https://api.x.ai/v1/chat/completions` | Chat completions |
| `https://api.x.ai/v1/models` | List available models |
| `https://api.x.ai/v1/responses` | Agent Tools API |

## Related Skills
- `xai-models` - Model selection guide
- `xai-x-search` - Twitter/X search
- `xai-sentiment` - Sentiment analysis

## References
- [xAI Console](https://console.x.ai)
- [xAI Documentation](https://docs.x.ai)
- [API Overview](https://docs.x.ai/docs/overview)
