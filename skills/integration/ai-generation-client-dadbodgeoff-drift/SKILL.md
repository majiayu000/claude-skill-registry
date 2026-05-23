---
name: ai-generation-client
description: External AI API integration with retry logic, rate limiting, content safety detection, and multi-turn conversation support for image generation.
license: MIT
compatibility: TypeScript/JavaScript, Python
metadata:
  category: integrations
  time: 6h
  source: drift-masterguide
---

# AI Generation Client

Robust AI API integration with retry logic and content safety.

## When to Use This Skill

- Integrating with AI generation APIs (Gemini, OpenAI, etc.)
- Need retry logic for flaky AI services
- Handling rate limits gracefully
- Detecting content policy violations
- Supporting multi-turn refinements

## Core Concepts

AI API integration requires:
1. **Exponential backoff** - Retry with increasing delays
2. **Rate limit handling** - Respect Retry-After headers
3. **Content safety** - Detect and handle policy violations
4. **Multi-turn context** - Enable cheaper refinements

## Implementation

### Python

```python
import asyncio
import base64
import time
import uuid
from dataclasses import dataclass
from typing import Optional, List
import aiohttp


@dataclass
class GenerationRequest:
    prompt: str
    width: int
    height: int
    model: str = "gemini-2.0-flash-exp"
    seed: Optional[int] = None
    input_image: Optional[bytes] = None
    conversation_history: Optional[List[dict]] = None


@dataclass
class GenerationResponse:
    image_data: bytes
    generation_id: str
    seed: int
    inference_time_ms: int
    thought_signature: Optional[bytes] = None


class RateLimitError(Exception):
    def __init__(self, retry_after: int = 60):
        self.retry_after = retry_after


class ContentPolicyError(Exception):
    def __init__(self, reason: str = "Content violates usage policies"):
        self.reason = reason


class GenerationError(Exception):
    def __init__(self, message: str, details: dict = None):
        self.message = message
        self.details = details or {}


class AIGenerationClient:
    """Async client for AI generation APIs with retry logic."""
    
    RETRY_DELAYS = [1, 2, 4]  # Exponential backoff
    BASE_URL = "https://generativelanguage.googleapis.com/v1beta"
    
    STRICT_CONSTRAINT = """STRICT RULES:
1. CREATE ORIGINAL ART - Do NOT use screenshots or existing images.
2. TEXT RENDERING - Render ALL text EXACTLY as written.
3. QUANTITIES - If prompt says "3 items" render EXACTLY 3.
4. NO ADDITIONS - Do NOT add elements not mentioned.
"""
    
    def __init__(self, api_key: str, timeout: int = 120, max_retries: int = 3):
        self.api_key = api_key
        self.timeout = timeout
        self.max_retries = min(max_retries, len(self.RETRY_DELAYS))
        self._session: Optional[aiohttp.ClientSession] = None
    
    async def _get_session(self) -> aiohttp.ClientSession:
        if self._session is None or self._session.closed:
            self._session = aiohttp.ClientSession(
                timeout=aiohttp.ClientTimeout(total=self.timeout)
            )
        return self._session
    
    async def close(self):
        if self._session and not self._session.closed:
            await self._session.close()
    
    async def generate(self, request: GenerationRequest) -> GenerationResponse:
        """Generate with exponential backoff retry."""
        last_exception = None
        
        for attempt in range(self.max_retries):
            try:
                return await self._execute_generation(request)
            
            except ContentPolicyError:
                raise  # Don't retry content policy violations
            
            except RateLimitError as e:
                last_exception = e
                delay = e.retry_after if e.retry_after else self.RETRY_DELAYS[attempt]
                if attempt < self.max_retries - 1:
                    await asyncio.sleep(delay)
                    continue
                raise
            
            except (GenerationError, asyncio.TimeoutError) as e:
                last_exception = e
                if attempt < self.max_retries - 1:
                    await asyncio.sleep(self.RETRY_DELAYS[attempt])
                    continue
                raise
        
        raise last_exception or GenerationError("Generation failed after all retries")
    
    async def _execute_generation(self, request: GenerationRequest) -> GenerationResponse:
        generation_id = str(uuid.uuid4())
        used_seed = request.seed or int(time.time() * 1000) % (2**31)
        start_time = time.time()
        
        # Build prompt with constraints
        constrained_prompt = f"{self.STRICT_CONSTRAINT}{request.prompt}\n\nGenerate as {request.width}x{request.height} pixels."
        
        parts = []
        if request.input_image:
            parts.append({
                "inlineData": {
                    "mimeType": "image/png",
                    "data": base64.b64encode(request.input_image).decode()
                }
            })
        parts.append({"text": constrained_prompt})
        
        # Handle multi-turn conversation
        if request.conversation_history:
            contents = self._build_multi_turn(request.conversation_history, request.prompt, request.width, request.height)
        else:
            contents = [{"parts": parts}]
        
        request_body = {
            "contents": contents,
            "generationConfig": {
                "responseModalities": ["IMAGE", "TEXT"],
            },
            "safetySettings": [
                {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
                {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
                {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
                {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
            ]
        }
        
        url = f"{self.BASE_URL}/models/{request.model}:generateContent"
        headers = {"Content-Type": "application/json", "x-goog-api-key": self.api_key}
        
        session = await self._get_session()
        async with session.post(url, json=request_body, headers=headers) as response:
            inference_time_ms = int((time.time() - start_time) * 1000)
            
            if response.status == 200:
                data = await response.json()
                image_data, thought_sig = self._extract_image(data)
                return GenerationResponse(
                    image_data=image_data,
                    generation_id=generation_id,
                    seed=used_seed,
                    inference_time_ms=inference_time_ms,
                    thought_signature=thought_sig,
                )
            
            elif response.status == 429:
                retry_after = int(response.headers.get("Retry-After", 60))
                raise RateLimitError(retry_after=retry_after)
            
            elif response.status == 400:
                error_data = await response.json()
                error_str = str(error_data).lower()
                if any(term in error_str for term in ["safety", "blocked", "policy"]):
                    raise ContentPolicyError(reason=str(error_data))
                raise GenerationError(f"Bad request: {error_data}")
            
            else:
                error_text = await response.text()
                raise GenerationError(f"API error {response.status}: {error_text}")
    
    def _build_multi_turn(self, history: List[dict], prompt: str, width: int, height: int) -> List[dict]:
        contents = []
        for turn in history:
            parts = []
            if turn.get("text"):
                parts.append({"text": turn["text"]})
            if turn.get("image_data"):
                image_b64 = base64.b64encode(turn["image_data"]).decode() if isinstance(turn["image_data"], bytes) else turn["image_data"]
                parts.append({"inlineData": {"mimeType": "image/png", "data": image_b64}})
            if parts:
                contents.append({"role": turn.get("role", "user"), "parts": parts})
        
        contents.append({
            "role": "user",
            "parts": [{"text": f"Refinement: {prompt}\n\nKeep at {width}x{height} pixels."}]
        })
        return contents
    
    def _extract_image(self, data: dict) -> tuple:
        candidates = data.get("candidates", [])
        if not candidates:
            raise GenerationError("No image generated")
        
        parts = candidates[0].get("content", {}).get("parts", [])
        for part in parts:
            if "inlineData" in part and "data" in part["inlineData"]:
                image_data = base64.b64decode(part["inlineData"]["data"])
                thought_sig = base64.b64decode(part["thoughtSignature"]) if "thoughtSignature" in part else None
                return image_data, thought_sig
        
        raise GenerationError("No image data in response")
```

### TypeScript

```typescript
interface GenerationRequest {
  prompt: string;
  width: number;
  height: number;
  model?: string;
  seed?: number;
  inputImage?: Buffer;
  conversationHistory?: Array<{ role: string; text?: string; imageData?: Buffer }>;
}

interface GenerationResponse {
  imageData: Buffer;
  generationId: string;
  seed: number;
  inferenceTimeMs: number;
  thoughtSignature?: Buffer;
}

class RateLimitError extends Error {
  constructor(public retryAfter: number = 60) {
    super(`Rate limit exceeded. Retry after ${retryAfter} seconds.`);
  }
}

class ContentPolicyError extends Error {
  constructor(public reason: string = "Content violates usage policies") {
    super(`Content policy violation: ${reason}`);
  }
}

class AIGenerationClient {
  private static RETRY_DELAYS = [1000, 2000, 4000];
  
  constructor(
    private apiKey: string,
    private timeout: number = 120000,
    private maxRetries: number = 3
  ) {}

  async generate(request: GenerationRequest): Promise<GenerationResponse> {
    let lastError: Error | null = null;

    for (let attempt = 0; attempt < this.maxRetries; attempt++) {
      try {
        return await this.executeGeneration(request);
      } catch (error) {
        if (error instanceof ContentPolicyError) throw error;
        
        lastError = error as Error;
        if (attempt < this.maxRetries - 1) {
          const delay = error instanceof RateLimitError
            ? error.retryAfter * 1000
            : AIGenerationClient.RETRY_DELAYS[attempt];
          await new Promise(resolve => setTimeout(resolve, delay));
        }
      }
    }

    throw lastError || new Error('Generation failed after all retries');
  }

  private async executeGeneration(request: GenerationRequest): Promise<GenerationResponse> {
    const generationId = crypto.randomUUID();
    const seed = request.seed ?? Math.floor(Date.now() % (2 ** 31));
    const startTime = Date.now();

    const response = await fetch(
      `https://generativelanguage.googleapis.com/v1beta/models/${request.model || 'gemini-2.0-flash-exp'}:generateContent`,
      {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'x-goog-api-key': this.apiKey,
        },
        body: JSON.stringify(this.buildRequestBody(request)),
        signal: AbortSignal.timeout(this.timeout),
      }
    );

    const inferenceTimeMs = Date.now() - startTime;

    if (response.status === 429) {
      const retryAfter = parseInt(response.headers.get('Retry-After') || '60');
      throw new RateLimitError(retryAfter);
    }

    if (response.status === 400) {
      const error = await response.json();
      if (JSON.stringify(error).toLowerCase().includes('safety')) {
        throw new ContentPolicyError(JSON.stringify(error));
      }
      throw new Error(`Bad request: ${JSON.stringify(error)}`);
    }

    if (!response.ok) {
      throw new Error(`API error ${response.status}`);
    }

    const data = await response.json();
    const imageData = this.extractImage(data);

    return { imageData, generationId, seed, inferenceTimeMs };
  }

  private buildRequestBody(request: GenerationRequest): object {
    const parts: any[] = [];
    
    if (request.inputImage) {
      parts.push({
        inlineData: {
          mimeType: 'image/png',
          data: request.inputImage.toString('base64'),
        },
      });
    }
    
    parts.push({ text: request.prompt });

    return {
      contents: [{ parts }],
      generationConfig: { responseModalities: ['IMAGE', 'TEXT'] },
    };
  }

  private extractImage(data: any): Buffer {
    const parts = data.candidates?.[0]?.content?.parts || [];
    for (const part of parts) {
      if (part.inlineData?.data) {
        return Buffer.from(part.inlineData.data, 'base64');
      }
    }
    throw new Error('No image data in response');
  }
}
```

## Usage Examples

### Basic Generation

```python
client = AIGenerationClient(api_key="your-key")

response = await client.generate(GenerationRequest(
    prompt="A cute cartoon banana mascot waving",
    width=512,
    height=512,
))
# response.image_data contains PNG bytes
```

### Multi-Turn Refinement

```python
# First generation
response1 = await client.generate(GenerationRequest(
    prompt="Gaming thumbnail with bold text 'EPIC WIN'",
    width=1280,
    height=720,
))

# Refinement (cheaper, uses context)
response2 = await client.generate(GenerationRequest(
    prompt="Make the text bigger and add more glow",
    width=1280,
    height=720,
    conversation_history=[
        {"role": "user", "text": "Gaming thumbnail with bold text 'EPIC WIN'"},
        {"role": "model", "image_data": response1.image_data},
    ],
))
```

## Best Practices

1. Always use retry logic - AI APIs can be flaky
2. Respect Retry-After headers for rate limits
3. Don't retry content policy errors
4. Use strict prompts to prevent hallucination
5. Track generation IDs for debugging
6. Set appropriate timeouts (30-120s)

## Common Mistakes

- No retry logic (fails on transient errors)
- Retrying content policy violations (wastes quota)
- Ignoring Retry-After headers (gets blocked)
- No timeout (hangs forever)
- Missing generation ID logging

## Related Patterns

- prompt-engine - Template-based prompt building
- rate-limiting - Protect your API quota
- circuit-breaker - Handle AI service outages
