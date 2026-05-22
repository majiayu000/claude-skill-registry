---
name: model-selection
description: Automatically applies when choosing LLM models and providers. Ensures proper model comparison, provider selection, cost optimization, fallback patterns, and multi-model strategies.
category: ai-llm
---

# Model Selection and Provider Management

When selecting LLM models and managing providers, follow these patterns for optimal cost, performance, and reliability.

**Trigger Keywords**: model selection, provider, model comparison, fallback, OpenAI, Anthropic, model routing, cost optimization, model capabilities, provider failover

**Agent Integration**: Used by `ml-system-architect`, `performance-and-cost-engineer-llm`, `llm-app-engineer`

## ✅ Correct Pattern: Model Registry

```python
from typing import Optional, Dict, List
from pydantic import BaseModel, Field
from enum import Enum


class ModelProvider(str, Enum):
    """Supported LLM providers."""
    ANTHROPIC = "anthropic"
    OPENAI = "openai"
    GOOGLE = "google"
    LOCAL = "local"


class ModelCapabilities(BaseModel):
    """Model capabilities and constraints."""

    max_context_tokens: int
    max_output_tokens: int
    supports_streaming: bool = True
    supports_function_calling: bool = False
    supports_vision: bool = False
    supports_json_mode: bool = False


class ModelPricing(BaseModel):
    """Model pricing information."""

    input_price_per_mtok: float  # USD per million tokens
    output_price_per_mtok: float
    cache_write_price_per_mtok: Optional[float] = None
    cache_read_price_per_mtok: Optional[float] = None


class ModelConfig(BaseModel):
    """Complete model configuration."""

    id: str
    name: str
    provider: ModelProvider
    capabilities: ModelCapabilities
    pricing: ModelPricing
    recommended_use_cases: List[str] = Field(default_factory=list)
    quality_tier: str  # "flagship", "balanced", "fast"


class ModelRegistry:
    """Registry of available models with metadata."""

    def __init__(self):
        self.models: Dict[str, ModelConfig] = {}
        self._register_default_models()

    def _register_default_models(self):
        """Register commonly used models."""

        # Claude models
        self.register(ModelConfig(
            id="claude-sonnet-4-20250514",
            name="Claude Sonnet 4",
            provider=ModelProvider.ANTHROPIC,
            capabilities=ModelCapabilities(
                max_context_tokens=200_000,
                max_output_tokens=8_192,
                supports_streaming=True,
                supports_vision=True,
                supports_json_mode=True
            ),
            pricing=ModelPricing(
                input_price_per_mtok=3.00,
                output_price_per_mtok=15.00,
                cache_write_price_per_mtok=3.75,
                cache_read_price_per_mtok=0.30
            ),
            recommended_use_cases=[
                "complex reasoning",
                "long context",
                "code generation"
            ],
            quality_tier="flagship"
        ))

        self.register(ModelConfig(
            id="claude-haiku-3-5-20250514",
            name="Claude Haiku 3.5",
            provider=ModelProvider.ANTHROPIC,
            capabilities=ModelCapabilities(
                max_context_tokens=200_000,
                max_output_tokens=8_192,
                supports_streaming=True,
                supports_vision=True
            ),
            pricing=ModelPricing(
                input_price_per_mtok=0.80,
                output_price_per_mtok=4.00
            ),
            recommended_use_cases=[
                "high throughput",
                "cost-sensitive",
                "simple tasks"
            ],
            quality_tier="fast"
        ))

        # OpenAI models
        self.register(ModelConfig(
            id="gpt-4-turbo",
            name="GPT-4 Turbo",
            provider=ModelProvider.OPENAI,
            capabilities=ModelCapabilities(
                max_context_tokens=128_000,
                max_output_tokens=4_096,
                supports_streaming=True,
                supports_function_calling=True,
                supports_vision=True,
                supports_json_mode=True
            ),
            pricing=ModelPricing(
                input_price_per_mtok=10.00,
                output_price_per_mtok=30.00
            ),
            recommended_use_cases=[
                "function calling",
                "complex reasoning",
                "structured output"
            ],
            quality_tier="flagship"
        ))

    def register(self, model: ModelConfig):
        """Register a model."""
        self.models[model.id] = model

    def get(self, model_id: str) -> Optional[ModelConfig]:
        """Get model by ID."""
        return self.models.get(model_id)

    def find_by_criteria(
        self,
        max_cost_per_mtok: Optional[float] = None,
        min_context_tokens: Optional[int] = None,
        requires_streaming: bool = False,
        requires_vision: bool = False,
        quality_tier: Optional[str] = None,
        provider: Optional[ModelProvider] = None
    ) -> List[ModelConfig]:
        """
        Find models matching criteria.

        Args:
            max_cost_per_mtok: Maximum input cost
            min_context_tokens: Minimum context window
            requires_streaming: Must support streaming
            requires_vision: Must support vision
            quality_tier: Quality tier filter
            provider: Provider filter

        Returns:
            List of matching models
        """
        matches = []

        for model in self.models.values():
            # Check cost
            if max_cost_per_mtok is not None:
                if model.pricing.input_price_per_mtok > max_cost_per_mtok:
                    continue

            # Check context
            if min_context_tokens is not None:
                if model.capabilities.max_context_tokens < min_context_tokens:
                    continue

            # Check capabilities
            if requires_streaming and not model.capabilities.supports_streaming:
                continue
            if requires_vision and not model.capabilities.supports_vision:
                continue

            # Check tier
            if quality_tier and model.quality_tier != quality_tier:
                continue

            # Check provider
            if provider and model.provider != provider:
                continue

            matches.append(model)

        # Sort by cost (cheapest first)
        matches.sort(key=lambda m: m.pricing.input_price_per_mtok)

        return matches


# Usage
registry = ModelRegistry()

# Find cost-effective models with vision
models = registry.find_by_criteria(
    max_cost_per_mtok=5.00,
    requires_vision=True
)

for model in models:
    print(f"{model.name}: ${model.pricing.input_price_per_mtok}/MTok")
```

## Model Router

```python
import asyncio
from typing import Callable, Optional


class ModelRouter:
    """Route requests to appropriate models based on task."""

    def __init__(self, registry: ModelRegistry):
        self.registry = registry
        self.routing_rules = []

    def add_rule(
        self,
        name: str,
        condition: Callable[[str], bool],
        model_id: str,
        priority: int = 0
    ):
        """
        Add routing rule.

        Args:
            name: Rule name
            condition: Function that checks if rule applies
            model_id: Model to route to
            priority: Higher priority rules checked first
        """
        self.routing_rules.append({
            "name": name,
            "condition": condition,
            "model_id": model_id,
            "priority": priority
        })

        # Sort by priority
        self.routing_rules.sort(key=lambda r: r["priority"], reverse=True)

    def route(self, prompt: str) -> str:
        """
        Determine which model to use for prompt.

        Args:
            prompt: Input prompt

        Returns:
            Model ID to use
        """
        for rule in self.routing_rules:
            if rule["condition"](prompt):
                return rule["model_id"]

        # Default fallback
        return "claude-sonnet-4-20250514"


# Example routing rules
router = ModelRouter(registry)

# Route simple tasks to fast model
router.add_rule(
    name="simple_tasks",
    condition=lambda p: len(p) < 100 and "?" in p,
    model_id="claude-haiku-3-5-20250514",
    priority=1
)

# Route code to Sonnet
router.add_rule(
    name="code_tasks",
    condition=lambda p: any(kw in p.lower() for kw in ["code", "function", "class"]),
    model_id="claude-sonnet-4-20250514",
    priority=2
)

# Route long context to Claude
router.add_rule(
    name="long_context",
    condition=lambda p: len(p) > 50_000,
    model_id="claude-sonnet-4-20250514",
    priority=3
)

# Use router
prompt = "Write a Python function to sort a list"
model_id = router.route(prompt)
print(f"Using model: {model_id}")
```

## Fallback Chain

```python
from typing import List, Optional
import logging

logger = logging.getLogger(__name__)


class FallbackChain:
    """Implement fallback chain for reliability."""

    def __init__(
        self,
        primary_model: str,
        fallback_models: List[str],
        registry: ModelRegistry
    ):
        self.primary_model = primary_model
        self.fallback_models = fallback_models
        self.registry = registry

    async def complete_with_fallback(
        self,
        prompt: str,
        clients: Dict[str, any],
        **kwargs
    ) -> Dict[str, any]:
        """
        Try primary model, fallback on failure.

        Args:
            prompt: Input prompt
            clients: Dict mapping provider to client
            **kwargs: Additional model parameters

        Returns:
            Dict with response and metadata
        """
        models_to_try = [self.primary_model] + self.fallback_models

        last_error = None

        for model_id in models_to_try:
            model_config = self.registry.get(model_id)
            if not model_config:
                logger.warning(f"Model {model_id} not in registry")
                continue

            try:
                logger.info(f"Attempting request with {model_id}")

                # Get client for provider
                client = clients.get(model_config.provider.value)
                if not client:
                    logger.warning(f"No client for {model_config.provider}")
                    continue

                # Make request
                response = await client.complete(
                    prompt,
                    model=model_id,
                    **kwargs
                )

                return {
                    "response": response,
                    "model_used": model_id,
                    "fallback_occurred": model_id != self.primary_model
                }

            except Exception as e:
                logger.error(f"Request failed for {model_id}: {e}")
                last_error = e
                continue

        # All models failed
        raise Exception(f"All models failed. Last error: {last_error}")


# Usage
fallback_chain = FallbackChain(
    primary_model="claude-sonnet-4-20250514",
    fallback_models=[
        "gpt-4-turbo",
        "claude-haiku-3-5-20250514"
    ],
    registry=registry
)

result = await fallback_chain.complete_with_fallback(
    prompt="What is Python?",
    clients={
        "anthropic": anthropic_client,
        "openai": openai_client
    }
)

print(f"Response from: {result['model_used']}")
```

## Cost Optimization

```python
class CostOptimizer:
    """Optimize costs by selecting appropriate models."""

    def __init__(self, registry: ModelRegistry):
        self.registry = registry

    def estimate_cost(
        self,
        model_id: str,
        input_tokens: int,
        output_tokens: int
    ) -> float:
        """
        Estimate cost for request.

        Args:
            model_id: Model identifier
            input_tokens: Input token count
            output_tokens: Expected output tokens

        Returns:
            Estimated cost in USD
        """
        model = self.registry.get(model_id)
        if not model:
            raise ValueError(f"Unknown model: {model_id}")

        input_cost = (
            input_tokens / 1_000_000
        ) * model.pricing.input_price_per_mtok

        output_cost = (
            output_tokens / 1_000_000
        ) * model.pricing.output_price_per_mtok

        return input_cost + output_cost

    def find_cheapest_model(
        self,
        input_tokens: int,
        output_tokens: int,
        quality_tier: Optional[str] = None,
        **criteria
    ) -> tuple[str, float]:
        """
        Find cheapest model meeting criteria.

        Args:
            input_tokens: Input token count
            output_tokens: Expected output tokens
            quality_tier: Optional quality requirement
            **criteria: Additional model criteria

        Returns:
            Tuple of (model_id, estimated_cost)
        """
        # Find matching models
        candidates = self.registry.find_by_criteria(
            quality_tier=quality_tier,
            **criteria
        )

        if not candidates:
            raise ValueError("No models match criteria")

        # Calculate costs
        costs = [
            (
                model.id,
                self.estimate_cost(model.id, input_tokens, output_tokens)
            )
            for model in candidates
        ]

        # Return cheapest
        return min(costs, key=lambda x: x[1])

    def batch_cost_analysis(
        self,
        requests: List[Dict[str, int]],
        model_ids: List[str]
    ) -> Dict[str, Dict[str, float]]:
        """
        Analyze costs for batch of requests across models.

        Args:
            requests: List of dicts with input_tokens, output_tokens
            model_ids: Models to compare

        Returns:
            Cost breakdown per model
        """
        analysis = {}

        for model_id in model_ids:
            total_cost = 0.0
            total_tokens = 0

            for req in requests:
                cost = self.estimate_cost(
                    model_id,
                    req["input_tokens"],
                    req["output_tokens"]
                )
                total_cost += cost
                total_tokens += req["input_tokens"] + req["output_tokens"]

            analysis[model_id] = {
                "total_cost_usd": total_cost,
                "avg_cost_per_request": total_cost / len(requests),
                "total_tokens": total_tokens,
                "cost_per_1k_tokens": (total_cost / total_tokens) * 1000
            }

        return analysis


# Usage
optimizer = CostOptimizer(registry)

# Find cheapest model for task
model_id, cost = optimizer.find_cheapest_model(
    input_tokens=1000,
    output_tokens=500,
    quality_tier="balanced"
)

print(f"Cheapest model: {model_id} (${cost:.4f})")

# Compare costs across models
requests = [
    {"input_tokens": 1000, "output_tokens": 500},
    {"input_tokens": 2000, "output_tokens": 1000},
]

cost_analysis = optimizer.batch_cost_analysis(
    requests,
    model_ids=[
        "claude-sonnet-4-20250514",
        "claude-haiku-3-5-20250514",
        "gpt-4-turbo"
    ]
)

for model_id, stats in cost_analysis.items():
    print(f"{model_id}: ${stats['total_cost_usd']:.4f}")
```

## Multi-Model Ensemble

```python
class ModelEnsemble:
    """Ensemble multiple models for improved results."""

    def __init__(
        self,
        models: List[str],
        voting_strategy: str = "majority"
    ):
        self.models = models
        self.voting_strategy = voting_strategy

    async def complete_ensemble(
        self,
        prompt: str,
        clients: Dict[str, any],
        registry: ModelRegistry
    ) -> str:
        """
        Get predictions from multiple models and combine.

        Args:
            prompt: Input prompt
            clients: Provider clients
            registry: Model registry

        Returns:
            Combined prediction
        """
        # Get predictions from all models
        tasks = []
        for model_id in self.models:
            model_config = registry.get(model_id)
            client = clients.get(model_config.provider.value)

            task = client.complete(prompt, model=model_id)
            tasks.append(task)

        predictions = await asyncio.gather(*tasks)

        # Combine predictions
        if self.voting_strategy == "majority":
            return self._majority_vote(predictions)
        elif self.voting_strategy == "longest":
            return max(predictions, key=len)
        elif self.voting_strategy == "first":
            return predictions[0]
        else:
            raise ValueError(f"Unknown strategy: {self.voting_strategy}")

    def _majority_vote(self, predictions: List[str]) -> str:
        """Select most common prediction."""
        from collections import Counter
        counter = Counter(predictions)
        return counter.most_common(1)[0][0]


# Usage
ensemble = ModelEnsemble(
    models=[
        "claude-sonnet-4-20250514",
        "gpt-4-turbo",
        "claude-opus-4-20250514"
    ],
    voting_strategy="majority"
)

result = await ensemble.complete_ensemble(
    prompt="Is Python case-sensitive? Answer yes or no.",
    clients=clients,
    registry=registry
)
```

## ❌ Anti-Patterns

```python
# ❌ Hardcoded model ID everywhere
response = client.complete("prompt", model="claude-sonnet-4-20250514")

# ✅ Better: Use model registry and routing
model_id = router.route(prompt)
response = client.complete(prompt, model=model_id)


# ❌ No fallback on failure
try:
    response = await primary_client.complete(prompt)
except:
    raise  # App crashes!

# ✅ Better: Implement fallback chain
result = await fallback_chain.complete_with_fallback(prompt, clients)


# ❌ Always using most expensive model
model = "claude-opus-4-20250514"  # Always flagship!

# ✅ Better: Route based on task complexity
model_id = router.route(prompt)  # Uses appropriate model


# ❌ No cost tracking
response = await client.complete(prompt)  # No idea of cost!

# ✅ Better: Track and optimize costs
cost = optimizer.estimate_cost(model_id, input_tokens, output_tokens)
logger.info(f"Request cost: ${cost:.4f}")
```

## Best Practices Checklist

- ✅ Use model registry to centralize model metadata
- ✅ Implement routing to select appropriate models
- ✅ Set up fallback chains for reliability
- ✅ Track and optimize costs per model
- ✅ Consider quality tier for each use case
- ✅ Monitor model performance metrics
- ✅ Use cheaper models for simple tasks
- ✅ Cache model responses when appropriate
- ✅ Test fallback chains regularly
- ✅ Document model selection rationale
- ✅ Review costs regularly and optimize
- ✅ Keep model metadata up to date

## Auto-Apply

When selecting models:
1. Register models in ModelRegistry with capabilities and pricing
2. Implement ModelRouter for task-based routing
3. Set up FallbackChain for reliability
4. Use CostOptimizer to find cost-effective options
5. Track costs per model and request
6. Document routing logic and fallback strategy
7. Monitor model performance and costs

## Related Skills

- `llm-app-architecture` - For LLM integration
- `evaluation-metrics` - For model comparison
- `monitoring-alerting` - For tracking performance
- `performance-profiling` - For optimization
- `prompting-patterns` - For model-specific prompts
