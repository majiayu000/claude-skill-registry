---
description: HuggingFace model deployment patterns, cost optimization, and API proxy tracking
---

# HuggingFace Deployment & AI Provider Management

Deploy HuggingFace models using serverless Inference API or dedicated endpoints with proper cost tracking, billing integration, and API proxy management.

## Overview

AINative Studio supports multiple AI providers through a factory pattern with automatic cost tracking and markup calculation:

- **OpenAI** - API proxy (GPT-4, Whisper, DALL-E, TTS)
- **Anthropic** - API proxy (Claude models)
- **MiniMax** - API proxy (TTS, Music Generation, Voice Cloning)
- **HuggingFace** - Serverless Inference API + Dedicated Endpoints
- **TogetherAI** - API proxy

All providers flow through `BillingService.calculate_cost_with_markup()` for consistent pricing with 100% markup (50% profit margin).

## HuggingFace Deployment Options

### Option A: Inference API (Serverless) - RECOMMENDED FOR AUDIO

**When to use:**
- Audio/TTS models with variable usage
- Models that don't need constant availability
- Cost-sensitive deployments (pay-per-request)
- Quick prototyping and testing

**URL Pattern:**
```
https://api-inference.huggingface.co/models/{model_id}
```

**Example Models:**
- `facebook/mms-tts-eng` - Multilingual TTS
- `suno/bark` - Audio generation
- `openai/whisper-large-v3` - Speech recognition

**Cost Structure:**
- Pay per request (typically $0.001-$0.02 per request)
- Zero cost when idle
- Shared infrastructure (may have cold starts)

**Implementation Pattern:**
```python
from app.providers.nouscoder_provider import NousCoderProvider

# Uses HF Inference API
provider = NousCoderProvider(
    api_key=os.getenv("HUGGINGFACE_API_KEY"),
    base_url="https://api-inference.huggingface.co"
)
```

### Option B: Dedicated Endpoints - FOR HIGH-TRAFFIC MODELS

**When to use:**
- Production models with consistent traffic
- Low-latency requirements (< 100ms)
- Custom inference configurations
- Models needing GPUs (T4, A10G, A100)

**URL Pattern:**
```
https://{endpoint-name}.endpoints.huggingface.cloud
```

**Cost Structure (per hour):**
- T4: $0.60/hr
- L4: $0.80/hr
- A10G: $1.00/hr
- A100: $4.00/hr

**Supports scale-to-zero:** Endpoint pauses after idle time, resumes on request

**Implementation Pattern:**
```python
from app.services.huggingface_endpoint_service import HuggingFaceEndpointService
from app.services.ai_providers.huggingface_endpoint_provider import HuggingFaceEndpointProvider

# Create dedicated endpoint
endpoint_service = HuggingFaceEndpointService(db)
endpoint = await endpoint_service.create_endpoint(
    endpoint_name="my-audio-model",
    model_repo="facebook/mms-tts-eng",
    hardware_type="nvidia-t4",
    auto_scale=True,
    min_replicas=0,  # Scale to zero
    max_replicas=1
)

# Use the endpoint
provider = HuggingFaceEndpointProvider(
    api_key=os.getenv("HUGGINGFACE_API_KEY"),
    endpoint_url=endpoint.endpoint_url,
    model_name=endpoint.model_repo,
    db=db
)
```

## Cost Tracking & Billing Flow

### 1. Provider Calculates Usage Cost

Each provider implementation calculates the base cost in USD:

```python
# Example: Audio TTS model
duration_seconds = 30
cost_per_second = Decimal("0.0001")  # HF Inference API rate
base_cost_usd = duration_seconds * cost_per_second  # $0.003
```

### 2. Convert to Credits

1 credit = $0.04 USD

```python
base_cost_credits = int(base_cost_usd / Decimal("0.04"))  # $0.003 / $0.04 = 0.075 → 1 credit
```

### 3. Apply Markup

100% markup = 2x cost = 50% profit margin

```python
from app.services.billing_service import BillingService

billing_service = BillingService(db)
final_cost = await billing_service.calculate_cost_with_markup(
    user_id=user.id,
    base_cost=base_cost_credits,  # 1 credit
    developer_markup=Decimal("100.0")  # 100% markup
)
# final_cost = 2 credits ($0.08)
```

### 4. Deduct from User Account

```python
# Create transaction record
transaction = await billing_service.create_transaction(
    user_id=user.id,
    amount=-final_cost,  # Negative = debit
    transaction_type="usage",
    description=f"TTS generation ({duration_seconds}s)",
    metadata={
        "model": "facebook/mms-tts-eng",
        "provider": "huggingface",
        "base_cost_usd": str(base_cost_usd),
        "credits_charged": final_cost
    }
)
```

### 5. Log Usage for Analytics

```python
from app.models.ai_usage_log import AIUsageLog

usage_log = AIUsageLog(
    user_id=user.id,
    model_name="facebook/mms-tts-eng",
    provider="huggingface",
    cost_credits=final_cost,
    cost_usd=base_cost_usd * 2,  # With markup
    metadata={"duration_seconds": duration_seconds}
)
db.add(usage_log)
await db.commit()
```

## Database Schema Patterns

### For Audio/TTS Models

Create these tables using Alembic migration:

```python
# app/models/audio_models.py
class AudioModel(Base):
    __tablename__ = "audio_models"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    model_id = Column(String(200), unique=True, nullable=False)  # HF repo ID
    model_name = Column(String(100), nullable=False)
    provider = Column(String(50), nullable=False)  # "huggingface" or "minimax"
    deployment_type = Column(String(50))  # "inference_api", "dedicated", "api_proxy"
    category = Column(String(50))  # "tts", "music", "voice_clone", "speech_to_text"

    # Cost tracking (per request or per second)
    base_cost_usd = Column(Numeric(10, 6))
    cost_unit = Column(String(20))  # "per_request", "per_second", "per_token"

    # HF-specific fields
    hf_endpoint_url = Column(Text)
    hardware_type = Column(String(50))

    # MiniMax API-specific fields
    api_endpoint = Column(Text)
    api_method = Column(String(10))  # "POST", "GET"

    status = Column(String(20), default="active")
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class AudioModelUsage(Base):
    __tablename__ = "audio_model_usage"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    audio_model_id = Column(UUID(as_uuid=True), ForeignKey("audio_models.id"))
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))

    duration_seconds = Column(Numeric(10, 2))
    requests_count = Column(Integer, default=1)

    base_cost_usd = Column(Numeric(10, 6))
    cost_credits = Column(Integer)  # After markup

    created_at = Column(DateTime(timezone=True), server_default=func.now())
```

### Provider Registry Pattern

Register all AI providers in the factory:

```python
# app/services/ai_providers/factory.py
from app.schemas.ai import AIProviderSchema
from app.services.ai_providers.openai_provider import OpenAIProvider
from app.services.ai_providers.anthropic_provider import AnthropicProvider
from app.providers.together_ai_provider import TogetherAIProvider
from app.providers.nouscoder_provider import NousCoderProvider
from app.providers.minimax_provider import MiniMaxProvider  # NEW

class AIProviderFactory:
    _providers: Dict[str, Type[BaseAIProvider]] = {
        AIProviderSchema.OPENAI: OpenAIProvider,
        AIProviderSchema.ANTHROPIC: AnthropicProvider,
        AIProviderSchema.TOGETHER_AI: TogetherAIProvider,
        AIProviderSchema.HUGGINGFACE: NousCoderProvider,  # HF Inference API
        AIProviderSchema.MINIMAX: MiniMaxProvider,  # NEW: MiniMax API
    }
```

## Environment Variables

### Required for HuggingFace

```bash
# HuggingFace Inference API (serverless)
HUGGINGFACE_API_KEY="hf_xxxxxxxxxxxxxxxxxxxxx"
HUGGINGFACE_BASE_URL="https://api-inference.huggingface.co"
HUGGINGFACE_TOKEN="hf_xxxxxxxxxxxxxxxxxxxxx"  # Same as API key
```

### Required for MiniMax

```bash
# MiniMax Audio API (TTS, Music, Voice Cloning)
MINIMAX_API_KEY="sk-api-xxxxxxxxxxxxxxxxxxxxx"
MINIMAX_API_BASE_URL="https://api.minimaxi.chat"
```

### Required for Other API Proxies

```bash
# OpenAI API (GPT, Whisper, TTS, DALL-E)
OPENAI_API_KEY="sk-xxxxxxxxxxxxxxxxxxxxx"

# Anthropic API (Claude)
ANTHROPIC_API_KEY="sk-ant-xxxxxxxxxxxxxxxxxxxxx"
```

## Implementation Checklist

When adding a new AI provider or model category:

### 1. Create Provider Class

```python
# app/providers/your_provider.py
from app.services.ai_providers.base import BaseAIProvider

class YourProvider(BaseAIProvider):
    def __init__(self, api_key: str, base_url: Optional[str] = None):
        super().__init__(api_key, base_url)
        self.base_url = base_url or "https://api.example.com"

    async def generate_audio(self, text: str, **kwargs):
        # Implementation
        pass
```

### 2. Register in Factory

```python
# app/services/ai_providers/factory.py
from app.providers.your_provider import YourProvider

AIProviderFactory._providers["your_provider"] = YourProvider
```

### 3. Create Database Models

```python
# Create Alembic migration
alembic revision --autogenerate -m "Add your_provider models"
alembic upgrade head
```

### 4. Update AIProviderSchema

```python
# app/schemas/ai.py
class AIProviderSchema:
    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    HUGGINGFACE = "huggingface"
    MINIMAX = "minimax"
    YOUR_PROVIDER = "your_provider"  # NEW
```

### 5. Create API Endpoint

```python
# app/api/api_v1/endpoints/audio.py (or your category)
@router.post("/generate")
async def generate_audio(
    request: AudioRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Get provider
    provider = AIProviderFactory.get_provider("your_provider")

    # Generate audio
    result = await provider.generate_audio(request.text)

    # Calculate cost
    billing_service = BillingService(db)
    cost = await billing_service.calculate_cost_with_markup(
        user_id=current_user.id,
        base_cost=calculate_base_cost(result),
        developer_markup=current_user.developer_markup
    )

    # Deduct credits and log usage
    await billing_service.create_transaction(...)

    return result
```

### 6. Update Frontend Model Catalog

```typescript
// AINative-website-nextjs/lib/model-aggregator.ts
async fetchYourCategoryModels(): Promise<UnifiedAIModel[]> {
  return [
    {
      id: 'model-id',
      slug: 'model-slug',
      name: 'Model Name',
      provider: 'Your Provider',
      category: 'YourCategory',
      endpoint: '/v1/your-category/generate',
      method: 'POST',
      pricing: {
        input: { amount: 0.01, unit: 'per request' },
        output: { amount: 0.02, unit: 'per second' }
      }
    }
  ];
}
```

## Cost Optimization Best Practices

### 1. Use Inference API for Audio Models

- Audio models have variable usage patterns
- Cold start latency (2-5s) is acceptable for TTS/music generation
- Zero cost when idle saves significant money
- Example: 90% cost savings vs dedicated endpoints

### 2. Monitor Usage Patterns

```sql
-- Find high-cost users
SELECT user_id, SUM(cost_credits) as total_credits
FROM audio_model_usage
WHERE created_at > NOW() - INTERVAL '30 days'
GROUP BY user_id
ORDER BY total_credits DESC
LIMIT 10;

-- Find high-cost models
SELECT audio_model_id, SUM(cost_credits) as total_credits
FROM audio_model_usage
WHERE created_at > NOW() - INTERVAL '30 days'
GROUP BY audio_model_id
ORDER BY total_credits DESC;
```

### 3. Cache Expensive Operations

```python
# Cache TTS results for common phrases
from functools import lru_cache

@lru_cache(maxsize=1000)
async def generate_tts_cached(text: str, voice: str):
    # Only generate if not in cache
    return await provider.generate_tts(text, voice)
```

### 4. Break-Even Analysis

For dedicated endpoints with scale-to-zero:

```
Inference API cost: $0.01 per request
Dedicated endpoint: $0.60/hr (T4)

Break-even = $0.60 / $0.01 = 60 requests/hour

If usage > 60 requests/hour → Use dedicated endpoint
If usage < 60 requests/hour → Use Inference API
```

## Monitoring & Debugging

### Check HF Credentials

```bash
# Verify credentials are set
railway variables | grep HUGGINGFACE

# Test Inference API
curl -X POST \
  https://api-inference.huggingface.co/models/facebook/mms-tts-eng \
  -H "Authorization: Bearer $HUGGINGFACE_API_KEY" \
  -d '{"inputs": "Hello world"}'
```

### Check Provider Registration

```python
from app.services.ai_providers.factory import AIProviderFactory

# List all registered providers
providers = AIProviderFactory.get_available_providers()
print(providers)
# ['openai', 'anthropic', 'together_ai', 'huggingface', 'minimax']
```

### Check Endpoint Status (Dedicated)

```python
from app.services.huggingface_endpoint_service import HuggingFaceEndpointService

service = HuggingFaceEndpointService(db)
endpoints = await service.list_endpoints()

for endpoint in endpoints:
    print(f"{endpoint.endpoint_name}: {endpoint.status}")
    print(f"  URL: {endpoint.endpoint_url}")
    print(f"  Cost: ${endpoint.hourly_cost_usd}/hr")
```

### Monitor Costs

```python
from app.services.billing_service import BillingService

billing = BillingService(db)

# Get user's total spend
total_spent = await billing.get_total_usage(user_id, days=30)

# Get breakdown by provider
breakdown = await billing.get_usage_by_provider(user_id, days=30)
```

## API Proxy Tracking

All API proxies (OpenAI, Anthropic, MiniMax) flow through the same cost tracking system:

1. **Provider calls external API** (OpenAI, Anthropic, MiniMax)
2. **Provider returns usage data** (tokens, duration, requests)
3. **BillingService converts to credits** (with 100% markup)
4. **Transaction created** (credit_transactions table)
5. **Usage logged** (ai_usage_log table for analytics)

This ensures consistent billing regardless of whether we're:
- Proxying API calls (OpenAI, Anthropic, MiniMax)
- Using serverless models (HF Inference API)
- Running dedicated endpoints (HF Dedicated)

## References

- HuggingFace Inference API Docs: https://huggingface.co/docs/api-inference/index
- HuggingFace Dedicated Endpoints: https://huggingface.co/docs/inference-endpoints/index
- MiniMax API Docs: https://platform.minimaxi.com/docs
- Existing Implementation: `src/backend/app/services/huggingface_endpoint_service.py`
- Provider Factory: `src/backend/app/services/ai_providers/factory.py`
- Billing Service: `src/backend/app/services/billing_service.py`

## Related Skills

- `/database-schema-sync` - Database migration patterns
- `/mandatory-tdd` - Testing requirements
- `/api-catalog` - API endpoint documentation
- `/code-quality` - Security and validation standards

Refs #1179
