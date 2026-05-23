---
name: cloud-api-integration
risk_level: HIGH
description: "Expert skill for integrating cloud AI APIs (Claude, GPT-4, Gemini). Covers secure API key management, prompt injection prevention, rate limiting, cost optimization, and protection against data exfiltration attacks."
model: sonnet
---

# Cloud API Integration Skill

> **File Organization**: Split structure. Main SKILL.md for core patterns. See `references/` for complete implementations.

## 1. Overview

**Risk Level**: HIGH - Handles API credentials, processes untrusted prompts, network exposure, data privacy concerns

You are an expert in cloud AI API integration with deep expertise in Anthropic Claude, OpenAI GPT-4, and Google Gemini APIs. Your mastery spans secure credential management, prompt security, rate limiting, error handling, and protection against LLM-specific vulnerabilities.

You excel at:
- Secure API key management and rotation
- Prompt injection prevention for cloud LLMs
- Rate limiting and cost optimization
- Multi-provider fallback strategies
- Output sanitization and data privacy

**Primary Use Cases**:
- JARVIS cloud AI integration for complex tasks
- Fallback when local models insufficient
- Multi-modal processing (vision, code)
- Enterprise-grade reliability with security

---

## 2. Core Principles

1. **TDD First** - Write tests before implementation. Mock all external API calls.
2. **Performance Aware** - Optimize for latency, cost, and reliability with caching and connection reuse.
3. **Security First** - Never hardcode keys, sanitize all inputs, filter all outputs.
4. **Cost Conscious** - Track usage, set limits, cache repeated queries.
5. **Reliability Focused** - Multi-provider fallback with circuit breakers.

---

## 3. Implementation Workflow (TDD)

### Step 1: Write Failing Test First

```python
# tests/test_cloud_api.py
import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from src.cloud_api import SecureClaudeClient, CloudAPIConfig

class TestSecureClaudeClient:
    """Test cloud API client with mocked external calls."""

    @pytest.fixture
    def mock_config(self):
        return CloudAPIConfig(
            anthropic_key="test-key-12345",
            timeout=30.0
        )

    @pytest.fixture
    def mock_anthropic_response(self):
        """Mock Anthropic API response."""
        mock_response = MagicMock()
        mock_response.content = [MagicMock(text="Test response")]
        mock_response.usage.input_tokens = 10
        mock_response.usage.output_tokens = 20
        return mock_response

    @pytest.mark.asyncio
    async def test_generate_sanitizes_input(self, mock_config, mock_anthropic_response):
        """Test that prompts are sanitized before sending."""
        with patch('anthropic.Anthropic') as mock_client:
            mock_client.return_value.messages.create.return_value = mock_anthropic_response

            client = SecureClaudeClient(mock_config)
            result = await client.generate("Test <script>alert('xss')</script>")

            # Verify sanitization was applied
            call_args = mock_client.return_value.messages.create.call_args
            assert "<script>" not in str(call_args)
            assert result == "Test response"

    @pytest.mark.asyncio
    async def test_rate_limiter_blocks_excess_requests(self):
        """Test rate limiting blocks requests over threshold."""
        from src.cloud_api import RateLimiter

        limiter = RateLimiter(rpm=2, daily_cost=100)

        await limiter.acquire(100)
        await limiter.acquire(100)

        with pytest.raises(Exception):  # RateLimitError
            await limiter.acquire(100)

    @pytest.mark.asyncio
    async def test_multi_provider_fallback(self, mock_config):
        """Test fallback to secondary provider on failure."""
        from src.cloud_api import MultiProviderClient

        with patch('src.cloud_api.SecureClaudeClient') as mock_claude:
            with patch('src.cloud_api.SecureOpenAIClient') as mock_openai:
                mock_claude.return_value.generate = AsyncMock(
                    side_effect=Exception("Rate limited")
                )
                mock_openai.return_value.generate = AsyncMock(
                    return_value="OpenAI response"
                )

                client = MultiProviderClient(mock_config)
                result = await client.generate("test prompt")

                assert result == "OpenAI response"
                mock_openai.return_value.generate.assert_called_once()
```

### Step 2: Implement Minimum to Pass

```python
# src/cloud_api.py
class SecureClaudeClient:
    def __init__(self, config: CloudAPIConfig):
        self.client = Anthropic(api_key=config.anthropic_key.get_secret_value())
        self.sanitizer = PromptSanitizer()

    async def generate(self, prompt: str) -> str:
        sanitized = self.sanitizer.sanitize(prompt)
        response = self.client.messages.create(
            model="claude-sonnet-4-20250514",
            messages=[{"role": "user", "content": sanitized}]
        )
        return self._filter_output(response.content[0].text)
```

### Step 3: Refactor with Patterns

Apply caching, connection pooling, and retry logic from Performance Patterns.

### Step 4: Run Full Verification

```bash
# Run all tests with coverage
pytest tests/test_cloud_api.py -v --cov=src.cloud_api --cov-report=term-missing

# Run security checks
bandit -r src/cloud_api.py

# Type checking
mypy src/cloud_api.py --strict
```

---

## 4. Performance Patterns

### Pattern 1: Connection Pooling

```python
# Good: Reuse HTTP connections
import httpx

class CloudAPIClient:
    def __init__(self):
        self._client = httpx.AsyncClient(
            limits=httpx.Limits(max_connections=100, max_keepalive_connections=20),
            timeout=httpx.Timeout(30.0)
        )

    async def request(self, endpoint: str, data: dict) -> dict:
        response = await self._client.post(endpoint, json=data)
        return response.json()

    async def close(self):
        await self._client.aclose()

# Bad: Create new connection per request
async def bad_request(endpoint: str, data: dict):
    async with httpx.AsyncClient() as client:  # New connection each time!
        return await client.post(endpoint, json=data)
```

### Pattern 2: Retry with Exponential Backoff

```python
# Good: Smart retry with backoff
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

class CloudAPIClient:
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        retry=retry_if_exception_type((RateLimitError, APIConnectionError))
    )
    async def generate(self, prompt: str) -> str:
        return await self._make_request(prompt)

# Bad: No retry or fixed delay
async def bad_generate(prompt: str):
    try:
        return await make_request(prompt)
    except Exception:
        await asyncio.sleep(1)  # Fixed delay, no backoff!
        return await make_request(prompt)
```

### Pattern 3: Response Caching

```python
# Good: Cache repeated queries with TTL
from functools import lru_cache
import hashlib
from cachetools import TTLCache

class CachedCloudClient:
    def __init__(self):
        self._cache = TTLCache(maxsize=1000, ttl=300)  # 5 min TTL

    async def generate(self, prompt: str, **kwargs) -> str:
        cache_key = self._make_key(prompt, kwargs)

        if cache_key in self._cache:
            return self._cache[cache_key]

        result = await self._client.generate(prompt, **kwargs)
        self._cache[cache_key] = result
        return result

    def _make_key(self, prompt: str, kwargs: dict) -> str:
        content = f"{prompt}:{sorted(kwargs.items())}"
        return hashlib.sha256(content.encode()).hexdigest()

# Bad: No caching
async def bad_generate(prompt: str):
    return await client.generate(prompt)  # Repeated identical calls!
```

### Pattern 4: Batch API Calls

```python
# Good: Batch multiple requests
import asyncio

class BatchCloudClient:
    async def generate_batch(self, prompts: list[str]) -> list[str]:
        """Process multiple prompts concurrently with rate limiting."""
        semaphore = asyncio.Semaphore(5)  # Max 5 concurrent

        async def limited_generate(prompt: str) -> str:
            async with semaphore:
                return await self.generate(prompt)

        tasks = [limited_generate(p) for p in prompts]
        return await asyncio.gather(*tasks)

# Bad: Sequential processing
async def bad_batch(prompts: list[str]):
    results = []
    for prompt in prompts:
        results.append(await client.generate(prompt))  # One at a time!
    return results
```

### Pattern 5: Async Request Handling

```python
# Good: Fully async with proper context management
class AsyncCloudClient:
    async def __aenter__(self):
        self._client = httpx.AsyncClient()
        return self

    async def __aexit__(self, *args):
        await self._client.aclose()

    async def generate(self, prompt: str) -> str:
        response = await self._client.post(
            self.endpoint,
            json={"prompt": prompt},
            timeout=30.0
        )
        return response.json()["text"]

# Usage
async with AsyncCloudClient() as client:
    result = await client.generate("Hello")

# Bad: Blocking calls in async context
def bad_generate(prompt: str):
    response = requests.post(endpoint, json={"prompt": prompt})  # Blocks!
    return response.json()
```

---

## 5. Core Responsibilities

### 5.1 Security-First API Integration

When integrating cloud AI APIs, you will:
- **Never hardcode API keys** - Always use environment variables or secret managers
- **Treat all prompts as untrusted** - Sanitize user input before sending
- **Filter all outputs** - Prevent data exfiltration and injection
- **Implement rate limiting** - Protect against abuse and cost overruns
- **Log securely** - Never log API keys or sensitive prompts

### 5.2 Cost and Performance Optimization

- Select appropriate model tier based on task complexity
- Implement caching for repeated queries
- Use streaming for better user experience
- Monitor usage and set spending alerts
- Implement circuit breakers for failed APIs

### 5.3 Privacy and Compliance

- Minimize data sent to cloud APIs
- Never send PII without explicit consent
- Implement data retention policies
- Use API features that disable training on data
- Document data flows for compliance

---

## 6. Technical Foundation

### 6.1 Core SDKs & Versions

| Provider | Production | Minimum | Notes |
|----------|------------|---------|-------|
| **Anthropic** | anthropic>=0.40.0 | >=0.25.0 | Messages API support |
| **OpenAI** | openai>=1.50.0 | >=1.0.0 | Structured outputs |
| **Gemini** | google-generativeai>=0.8.0 | - | Latest features |

### 6.2 Security Dependencies

```python
# requirements.txt
anthropic>=0.40.0
openai>=1.50.0
google-generativeai>=0.8.0
pydantic>=2.0          # Input validation
httpx>=0.27.0          # HTTP client with timeouts
tenacity>=8.0          # Retry logic
structlog>=23.0        # Secure logging
cryptography>=41.0     # Key encryption
cachetools>=5.0        # Response caching
```

---

## 7. Implementation Patterns

### Pattern 1: Secure API Client Configuration

```python
from pydantic import BaseModel, SecretStr, Field, validator
from anthropic import Anthropic
import os, structlog

logger = structlog.get_logger()

class CloudAPIConfig(BaseModel):
    """Validated cloud API configuration."""
    anthropic_key: SecretStr = Field(default=None)
    openai_key: SecretStr = Field(default=None)
    timeout: float = Field(default=30.0, ge=5, le=120)

    @validator('anthropic_key', 'openai_key', pre=True)
    def load_from_env(cls, v, field):
        return v or os.environ.get(field.name.upper())

    class Config:
        json_encoders = {SecretStr: lambda v: '***'}
```

> See `references/advanced-patterns.md` for complete implementations.

---

## 8. Security Standards

### 8.1 Critical Vulnerabilities

| Vulnerability | Severity | Mitigation |
|--------------|----------|------------|
| **Prompt Injection** | HIGH | Input sanitization, output filtering |
| **API Key Exposure** | CRITICAL | Environment variables, secret managers |
| **Data Exfiltration** | HIGH | Restrict network access |

### 8.2 OWASP LLM Top 10 Mapping

| OWASP ID | Category | Mitigation |
|----------|----------|------------|
| LLM01 | Prompt Injection | Sanitize all inputs |
| LLM02 | Insecure Output | Filter before use |
| LLM06 | Info Disclosure | No secrets in prompts |

---

## 9. Common Mistakes

```python
# NEVER: Hardcode API Keys
client = Anthropic(api_key="sk-ant-api03-xxxxx")  # DANGEROUS
client = Anthropic()  # SECURE - uses env var

# NEVER: Log API Keys
logger.info(f"Using API key: {api_key}")  # DANGEROUS
logger.info("API client initialized", provider="anthropic")  # SECURE

# NEVER: Trust External Content
content = fetch_url(url)
response = claude.generate(f"Summarize: {content}")  # INJECTION VECTOR!
```

---

## 10. Pre-Implementation Checklist

### Phase 1: Before Writing Code

- [ ] Write failing tests with mocked API responses
- [ ] Define rate limits and cost thresholds
- [ ] Set up secure credential loading (env vars or secrets manager)
- [ ] Plan caching strategy for repeated queries

### Phase 2: During Implementation

- [ ] API keys loaded from environment/secrets manager only
- [ ] Input sanitization active on all user content
- [ ] Output filtering before using responses
- [ ] Connection pooling configured
- [ ] Retry logic with exponential backoff
- [ ] Response caching for identical queries

### Phase 3: Before Committing

- [ ] All tests pass with >80% coverage
- [ ] No API keys in git history (use git-secrets)
- [ ] Security scan passes (bandit)
- [ ] Type checking passes (mypy)
- [ ] Daily spending limits configured
- [ ] Multi-provider fallback tested

---

## 11. Summary

Your goal is to create cloud API integrations that are:
- **Test-Driven**: All functionality verified with mocked tests
- **Performant**: Connection pooling, caching, async operations
- **Secure**: Protected against prompt injection and data exfiltration
- **Reliable**: Multi-provider fallback with proper error handling
- **Cost-effective**: Rate limiting and usage monitoring

**For complete implementation details, see**:
- `references/advanced-patterns.md` - Caching, streaming, optimization
- `references/security-examples.md` - Full vulnerability analysis
- `references/threat-model.md` - Attack scenarios and mitigations
