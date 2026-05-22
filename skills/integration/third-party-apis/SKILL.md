---
name: third-party-apis
description: |
  Best practices for integrating third-party APIs and services in career_ios_backend.
  Automatically invoked when working with external APIs like ElevenLabs, OpenAI, Gemini, etc.
  Trigger keywords: "third-party", "API integration", "ElevenLabs", "OpenAI", "Gemini",
  "Vertex AI", "external API", "第三方 API", "API 整合"

  Enforces documentation-first approach and TDD for external integrations.
allowed-tools: [Read, WebFetch, Bash, Grep]
---

# Third-Party API Integration Skill

## Purpose
Guide proper integration of third-party APIs with a documentation-first approach, preventing common mistakes and ensuring reliable integrations.

## Automatic Activation

This skill is AUTOMATICALLY activated when user mentions:
- ✅ "ElevenLabs" / "OpenAI" / "Gemini" / "Vertex AI"
- ✅ "third-party API" / "第三方 API"
- ✅ "external API" / "外部 API"
- ✅ "API integration" / "API 整合"
- ✅ "documentation" (in API context)

---

## Critical Rule: Documentation First

### ✅ MANDATORY: Read Official Docs FIRST

**Before writing ANY integration code**:

```
❌ WRONG Approach:
1. Search Google for "how to use X API"
2. Find random blog posts or Stack Overflow
3. Make assumptions based on similar APIs
4. Write code
5. Encounter errors
6. Read documentation (too late!)

✅ CORRECT Approach:
1. 需求確定 → 立即查官方文檔
2. Find correct API endpoint and parameter format
3. Review official example code
4. Write integration tests based on docs
5. Implement code
6. Test and verify
```

**Why Documentation First**:
- Official docs are **always** authoritative
- Prevents wasted commits from wrong assumptions
- Saves debugging time
- Ensures using latest API version
- Catches breaking changes early

---

## Lesson Learned: Real Example

### Case Study: ElevenLabs Language Code Issue

**What Happened** (2025-12-25):

```python
# ❌ WRONG: Assumed language code based on web search
{
    "language": "cmn"  # or "zho"
    # Assumption: Chinese = "cmn" (Mandarin) or "zho" (Chinese)
    # Source: Generic ISO 639-3 lists from Google
}

# ✅ CORRECT: Checked Realtime v2 docs
{
    "language": "zh"  # ISO 639-1 code
    # Source: https://elevenlabs.io/docs/api-reference/speech-to-text/v-1-speech-to-text-realtime
    # Realtime v2 uses ISO 639-1, not ISO 639-3!
}
```

**Impact**:
- ❌ 2 commits wasted
- ❌ Deployment delays
- ❌ Testing time lost
- ✅ Could have been avoided by reading docs first

**Rule**: **"When in doubt, RTFM (Read The F***ing Manual)"**

---

## Supported Third-Party Services

### Key Services & Official Documentation

**1. ElevenLabs (Voice AI)**

- **Text-to-Speech**:
  - Docs: https://elevenlabs.io/docs/api-reference/text-to-speech
  - Language codes: Various formats

- **Realtime v2 Speech-to-Text** ⚠️ **Special attention**:
  - Docs: https://elevenlabs.io/docs/api-reference/speech-to-text/v-1-speech-to-text-realtime
  - **Language codes**: ISO 639-1 (e.g., `zh` for Chinese)
  - ⚠️ **Different from TTS language codes!**
  - Always check version-specific docs

**2. OpenAI**

- **Official Docs**: https://platform.openai.com/docs/api-reference
- **Key Points**:
  - Always check model-specific parameters
  - Rate limits vary by tier
  - Different models have different capabilities
  - Check deprecation notices

**3. Google Gemini / Vertex AI**

- **Official Docs**: https://cloud.google.com/vertex-ai/docs
- **Key Points**:
  - Check regional availability
  - Authentication uses service accounts
  - Different pricing by region
  - Model versions and updates

**4. Other Services**

When integrating any third-party service:
1. Find official API documentation
2. Check API version (v1, v2, etc.)
3. Review authentication methods
4. Check rate limits and quotas
5. Read example code in official docs

---

## Development Process (Documentation-First)

### Step-by-Step Integration

```
1. 需求確定 → 立即查官方文檔
   - What feature do we need?
   - Which API endpoint provides it?
   - What's the current API version?
   ↓

2. 找到正確的 API endpoint 和參數格式
   - Read endpoint documentation
   - Check required vs. optional parameters
   - Understand request/response formats
   - Note authentication requirements
   ↓

3. 查看官方範例代碼
   - Copy official examples
   - Understand the pattern
   - Check error handling
   - Review best practices
   ↓

4. 實作並測試 (TDD)
   - Write test FIRST (based on docs)
   - Implement integration
   - Verify with official examples
   - Handle errors properly
   ↓

5. ✅ Integration complete
   ❌ NOT: Write code first, read docs later!
```

---

## Integration with TDD

### Test Third-Party APIs Properly

**Write tests based on official documentation**:

```python
# Example: ElevenLabs Realtime v2 STT integration test

@pytest.mark.asyncio
async def test_elevenlabs_realtime_stt():
    """
    Test ElevenLabs Realtime v2 Speech-to-Text

    Official docs:
    https://elevenlabs.io/docs/api-reference/speech-to-text/v-1-speech-to-text-realtime

    Key parameters (from official docs):
    - language: ISO 639-1 code (e.g., 'zh' for Chinese)
    - model: realtime-v2
    """
    config = {
        "language": "zh",  # ISO 639-1 (from official docs)
        "model": "realtime-v2"
    }

    # Test based on official API contract
    result = await stt_service.transcribe(audio_data, config)

    assert result["text"] is not None
    assert result["language"] == "zh"
```

**Best Practices**:

1. **Include documentation link in test comments**
   ```python
   """
   Test X API endpoint

   Official docs: https://example.com/docs/api/endpoint
   Parameters based on v2.0 specification
   """
   ```

2. **Use official examples as test cases**
   - Copy request/response from docs
   - Verify your code matches official behavior
   - Helps catch API version mismatches

3. **Validate API contract**
   - Test required fields
   - Verify response structure
   - Check error codes match docs

4. **Keep docs link updated**
   - When API version changes
   - When docs URL changes
   - When parameters update

---

## Common Mistakes to Avoid

### ❌ Anti-Pattern 1: Google-First Approach

```python
# ❌ WRONG
# Googles "python elevenlabs language code"
# Finds Stack Overflow from 2023
# Uses outdated information
# API has changed since then
# Code breaks

# ✅ CORRECT
# Goes directly to official docs
# Finds current API specification
# Uses correct parameters
# Code works
```

### ❌ Anti-Pattern 2: Assumption-Based Development

```python
# ❌ WRONG
# "OpenAI uses X format, so Gemini probably does too"
# Makes assumptions without checking
# Code breaks because APIs are different

# ✅ CORRECT
# Reads Gemini-specific documentation
# Understands Gemini's specific requirements
# Implements correctly from the start
```

### ❌ Anti-Pattern 3: Skipping Error Handling

```python
# ❌ WRONG
response = api.call(params)
return response.data  # No error checking

# ✅ CORRECT (based on official docs)
try:
    response = api.call(params)
    if response.status_code == 200:
        return response.data
    else:
        # Handle errors as documented in API docs
        raise APIError(f"API returned {response.status_code}")
except Exception as e:
    # Error handling based on official documentation
    logger.error(f"API call failed: {e}")
    raise
```

### ❌ Anti-Pattern 4: Hardcoding API Versions

```python
# ❌ WRONG
url = "https://api.example.com/v1/endpoint"  # Hardcoded v1

# ✅ CORRECT
# Use config/environment variables
API_VERSION = os.getenv("API_VERSION", "v2")
url = f"https://api.example.com/{API_VERSION}/endpoint"
```

---

## Documentation Checklist

### Before Writing Integration Code

- [ ] Found official API documentation
- [ ] Verified API version (v1, v2, beta, etc.)
- [ ] Read endpoint-specific documentation
- [ ] Reviewed official example code
- [ ] Checked authentication requirements
- [ ] Noted rate limits and quotas
- [ ] Checked for version deprecations

### During Implementation

- [ ] Using parameters exactly as documented
- [ ] Following official authentication pattern
- [ ] Handling errors as documented
- [ ] Testing with official example data
- [ ] Including docs link in comments

### After Implementation

- [ ] Test passes with real API calls
- [ ] Error handling covers documented errors
- [ ] Rate limiting implemented (if needed)
- [ ] Documentation link in test comments
- [ ] API version noted in code

---

## Service-Specific Guidelines

### ElevenLabs Realtime v2

```python
# ✅ CORRECT configuration (from official docs)
config = {
    "language": "zh",           # ISO 639-1
    "model": "realtime-v2",     # Realtime v2 model
    "encoding": "pcm_16000"     # Audio format
}

# ⚠️ IMPORTANT
# - Language code differs between TTS and STT
# - Realtime v2 uses ISO 639-1 ('zh')
# - TTS might use different codes
# - Always check version-specific docs
```

**Docs**: https://elevenlabs.io/docs/api-reference/speech-to-text/v-1-speech-to-text-realtime

### OpenAI GPT

```python
# ✅ CORRECT (based on official docs)
response = openai.ChatCompletion.create(
    model="gpt-4",              # Check model availability
    messages=[...],
    temperature=0.7,            # As documented
    max_tokens=1000             # Check model limits
)

# ⚠️ IMPORTANT
# - Different models have different limits
# - Check rate limits for your tier
# - Handle API errors properly
# - Monitor token usage
```

**Docs**: https://platform.openai.com/docs/api-reference

### Google Gemini / Vertex AI

```python
# ✅ CORRECT (based on official docs)
from google.cloud import aiplatform

aiplatform.init(
    project="your-project-id",
    location="us-central1"      # Check regional availability
)

# ⚠️ IMPORTANT
# - Requires service account authentication
# - Check model availability by region
# - Different pricing by region
# - Use official Python SDK
```

**Docs**: https://cloud.google.com/vertex-ai/docs

---

## Testing Third-Party Integrations

### Integration Test Pattern

```python
import pytest
from unittest.mock import Mock, patch

@pytest.mark.asyncio
async def test_third_party_api_integration():
    """
    Test integration with ThirdParty API

    Official docs: https://example.com/docs/api
    API version: v2.0
    Parameters based on official specification
    """

    # 1. Test with real API (integration test)
    # Use test API keys (not production)
    result = await service.call_api({
        "param1": "value1",  # From official docs
        "param2": "value2"   # From official docs
    })

    # Verify based on official API contract
    assert result.status == "success"
    assert "expected_field" in result.data

@pytest.mark.asyncio
async def test_third_party_api_error_handling():
    """
    Test error handling based on official docs

    Expected errors (from API docs):
    - 400: Bad Request
    - 401: Unauthorized
    - 429: Rate Limit Exceeded
    - 500: Server Error
    """

    # Test each documented error case
    with pytest.raises(APIError) as exc_info:
        await service.call_api(invalid_params)

    assert exc_info.value.code == 400
```

### Mocking External APIs

```python
@patch('app.services.third_party.ThirdPartyClient')
async def test_api_with_mock(mock_client):
    """
    Mock external API for unit testing

    Use official example response from docs
    """

    # Use official example response from documentation
    mock_client.return_value.call.return_value = {
        "status": "success",
        "data": {...}  # Copied from official docs
    }

    result = await service.process_with_api()
    assert result is not None
```

---

## Rate Limiting & Error Handling

### Implement Rate Limiting

```python
from tenacity import retry, stop_after_attempt, wait_exponential

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=2, max=10)
)
async def call_third_party_api(params):
    """
    Call third-party API with automatic retry

    Retry strategy based on API documentation:
    - Max 3 attempts
    - Exponential backoff (2s, 4s, 8s)
    - As recommended in official docs
    """
    try:
        response = await client.call(params)
        return response
    except RateLimitError:
        # Handle as documented
        logger.warning("Rate limit hit, retrying...")
        raise  # Retry will handle
    except Exception as e:
        logger.error(f"API call failed: {e}")
        raise
```

### Handle API Errors Properly

```python
async def safe_api_call(params):
    """
    Safe API call with proper error handling

    Error codes based on official documentation
    """
    try:
        response = await api_client.call(params)

        # Success codes from docs
        if response.status_code == 200:
            return response.data

        # Error codes from official docs
        elif response.status_code == 400:
            raise BadRequestError("Invalid parameters")
        elif response.status_code == 401:
            raise AuthenticationError("Invalid API key")
        elif response.status_code == 429:
            raise RateLimitError("Rate limit exceeded")
        else:
            raise APIError(f"Unexpected error: {response.status_code}")

    except Exception as e:
        logger.error(f"API integration error: {e}")
        # Fallback behavior based on requirements
        return None
```

---

## Environment Configuration

### API Keys and Secrets

```python
# ✅ CORRECT: Use environment variables
import os

ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GEMINI_PROJECT_ID = os.getenv("GEMINI_PROJECT_ID")

# ❌ NEVER hardcode API keys
# API_KEY = "sk-abc123..."  # NEVER DO THIS
```

### Configuration File

```python
# config/third_party.py

class ThirdPartyConfig:
    """
    Third-party API configuration

    All values from environment variables
    Never commit API keys to git
    """

    # ElevenLabs
    ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")
    ELEVENLABS_API_VERSION = os.getenv("ELEVENLABS_API_VERSION", "v2")

    # OpenAI
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    OPENAI_ORG_ID = os.getenv("OPENAI_ORG_ID")

    # Google
    GOOGLE_PROJECT_ID = os.getenv("GOOGLE_PROJECT_ID")
    GOOGLE_LOCATION = os.getenv("GOOGLE_LOCATION", "us-central1")
```

---

## Related Skills

- **tdd-workflow** - Test-first development for API integrations
- **api-development** - General API development patterns
- **quality-standards** - Code quality and testing standards

---

## Quick Reference: Official Docs

### Always Check These First

| Service | Official Docs URL |
|---------|------------------|
| ElevenLabs Realtime v2 STT | https://elevenlabs.io/docs/api-reference/speech-to-text/v-1-speech-to-text-realtime |
| ElevenLabs TTS | https://elevenlabs.io/docs/api-reference/text-to-speech |
| OpenAI API | https://platform.openai.com/docs/api-reference |
| Google Gemini / Vertex AI | https://cloud.google.com/vertex-ai/docs |
| FastAPI (our framework) | https://fastapi.tiangolo.com/ |

### When Docs Change

- Update test comments with new URL
- Verify parameters still match
- Check for breaking changes
- Update configuration if needed

---

**Remember**: "When in doubt, RTFM (Read The F***ing Manual)"

**Skill Version**: v1.0
**Last Updated**: 2025-12-25
**Project**: career_ios_backend (Prototype Phase)
