---
name: recommendation-system
description: Deploy production recommendation systems with feature stores, caching, A/B testing. Use for personalization APIs, low latency serving, or encountering cache invalidation, experiment tracking, quality monitoring issues.
keywords: recommendation system, personalization, feature store, model serving, caching strategy, Redis, A/B testing, Thompson sampling, recommendation metrics, CTR, conversion rate, catalog coverage, diversity, Prometheus monitoring, recommendation API, real-time recommendations, collaborative filtering integration, production recommendations, experiment tracking
license: MIT
---

# Recommendation System

Production-ready architecture for scalable recommendation systems with feature stores, multi-tier caching, A/B testing, and comprehensive monitoring.

## When to Use This Skill

Load this skill when:
- **Building Recommendation APIs**: Serving personalized recommendations at scale
- **Implementing Caching**: Multi-tier caching for sub-millisecond latency
- **Running A/B Tests**: Experimenting with recommendation algorithms
- **Monitoring Quality**: Tracking CTR, conversion, diversity, coverage
- **Optimizing Performance**: Reducing latency, increasing throughput
- **Feature Engineering**: Managing user/item features with feature stores

## Quick Start: Recommendation API in 5 Steps

```bash
# 1. Install dependencies
pip install fastapi==0.109.0 redis==5.0.0 prometheus-client==0.19.0

# 2. Start Redis (for caching and feature store)
docker run -d -p 6379:6379 redis:alpine

# 3. Create recommendation service: app.py
cat > app.py << 'EOF'
from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
import redis
import json

app = FastAPI()
cache = redis.Redis(host='localhost', port=6379, decode_responses=True)

class RecommendationResponse(BaseModel):
    user_id: str
    items: List[str]
    cached: bool

@app.post("/recommendations", response_model=RecommendationResponse)
async def get_recommendations(user_id: str, n: int = 10):
    # Check cache
    cache_key = f"recs:{user_id}:{n}"
    cached = cache.get(cache_key)

    if cached:
        return RecommendationResponse(
            user_id=user_id,
            items=json.loads(cached),
            cached=True
        )

    # Generate recommendations (simplified)
    items = [f"item_{i}" for i in range(n)]

    # Cache for 5 minutes
    cache.setex(cache_key, 300, json.dumps(items))

    return RecommendationResponse(
        user_id=user_id,
        items=items,
        cached=False
    )

@app.get("/health")
async def health():
    return {"status": "healthy"}
EOF

# 4. Run API
uvicorn app:app --host 0.0.0.0 --port 8000

# 5. Test
curl -X POST "http://localhost:8000/recommendations?user_id=user_123&n=10"
```

**Result**: Working recommendation API with caching in under 5 minutes.

## System Architecture

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│ User Events │────▶│ Feature     │────▶│ Model       │
│ (clicks,    │     │ Store       │     │ Serving     │
│  purchases) │     │ (Redis)     │     │             │
└─────────────┘     └─────────────┘     └─────────────┘
                           │                    │
                           ▼                    ▼
                    ┌─────────────┐     ┌─────────────┐
                    │ Training    │     │ API         │
                    │ Pipeline    │     │ (FastAPI)   │
                    └─────────────┘     └─────────────┘
                                               │
                                               ▼
                                        ┌─────────────┐
                                        │ Monitoring  │
                                        │ (Prometheus)│
                                        └─────────────┘
```

## Core Components

### 1. Feature Store

Centralized storage for user and item features:

```python
import redis
import json

class FeatureStore:
    """Fast feature access with Redis caching."""

    def __init__(self, redis_client):
        self.redis = redis_client
        self.ttl = 3600  # 1 hour

    def get_user_features(self, user_id: str) -> dict:
        cache_key = f"user_features:{user_id}"
        cached = self.redis.get(cache_key)

        if cached:
            return json.loads(cached)

        # Fetch from database
        features = fetch_from_db(user_id)

        # Cache
        self.redis.setex(cache_key, self.ttl, json.dumps(features))
        return features
```

### 2. Model Serving

Serve multiple models for A/B testing:

```python
class ModelServing:
    """Serve multiple recommendation models."""

    def __init__(self):
        self.models = {}

    def register_model(self, name: str, model, is_default: bool = False):
        self.models[name] = model
        if is_default:
            self.default_model = name

    def predict(self, user_features: dict, item_features: list, model_name: str = None):
        model = self.models.get(model_name or self.default_model)
        return model.predict(user_features, item_features)
```

### 3. Caching Layer

Multi-tier caching for low latency:

```python
class TieredCache:
    """L1 (memory) -> L2 (Redis) -> L3 (database)."""

    def __init__(self, redis_client):
        self.l1_cache = {}  # In-memory
        self.redis = redis_client  # L2

    def get(self, key: str):
        # L1: In-memory (fastest)
        if key in self.l1_cache:
            return self.l1_cache[key]

        # L2: Redis
        cached = self.redis.get(key)
        if cached:
            value = json.loads(cached)
            self.l1_cache[key] = value  # Promote to L1
            return value

        # L3: Miss (fetch from database)
        return None
```

## Key Metrics

| Metric | Description | Target |
|--------|-------------|--------|
| **CTR** | Click-through rate | >5% |
| **Conversion Rate** | Purchases from recs | >2% |
| **P95 Latency** | 95th percentile response time | <200ms |
| **Cache Hit Rate** | % served from cache | >80% |
| **Coverage** | % of catalog recommended | >50% |
| **Diversity** | Variety in recommendations | >0.7 |

## Known Issues Prevention

### 1. Cold Start for New Users
**Problem**: No recommendations for users without history, poor initial experience.

**Solution**: Use popularity-based fallback:
```python
def get_recommendations(user_id: str, n: int = 10):
    user_features = feature_store.get_user_features(user_id)

    # Check if new user (no purchase history)
    if user_features.get('total_purchases', 0) == 0:
        # Fallback to popular items
        return get_popular_items(n)

    # Personalized recommendations
    return generate_personalized_recs(user_id, n)
```

### 2. Cache Invalidation on User Actions
**Problem**: User makes purchase, cache still shows purchased item in recommendations.

**Solution**: Invalidate cache on relevant actions:
```python
INVALIDATING_ACTIONS = {'purchase', 'rating', 'add_to_cart'}

def on_user_action(user_id: str, action: str):
    if action in INVALIDATING_ACTIONS:
        cache_key = f"recs:{user_id}:*"
        redis_client.delete(cache_key)
        logger.info(f"Invalidated cache for {user_id} due to {action}")
```

### 3. Thundering Herd on Cache Expiry
**Problem**: Many users' caches expire simultaneously, overload database/model.

**Solution**: Add random jitter to TTL:
```python
import random

def set_cache(key: str, value: dict, base_ttl: int = 300):
    # Add ±10% jitter
    jitter = random.uniform(-0.1, 0.1) * base_ttl
    ttl = int(base_ttl + jitter)
    redis_client.setex(key, ttl, json.dumps(value))
```

### 4. Poor Diversity = Filter Bubble
**Problem**: Recommendations too similar, users only see same category.

**Solution**: Implement diversity constraint:
```python
def rank_with_diversity(items: list, scores: list, n: int = 10):
    selected = []
    category_counts = {}

    for item, score in sorted(zip(items, scores), key=lambda x: -x[1]):
        category = item['category']

        # Limit 3 items per category
        if category_counts.get(category, 0) >= 3:
            continue

        selected.append(item)
        category_counts[category] = category_counts.get(category, 0) + 1

        if len(selected) >= n:
            break

    return selected
```

### 5. No Monitoring = Silent Degradation
**Problem**: Recommendation quality drops, nobody notices until users complain.

**Solution**: Continuous monitoring with alerts:
```python
from prometheus_client import Counter, Histogram

recommendation_clicks = Counter('recommendation_clicks_total')
recommendation_latency = Histogram('recommendation_latency_seconds')

@app.post("/recommendations")
async def get_recommendations(user_id: str):
    start = time.time()

    recs = generate_recs(user_id)

    latency = time.time() - start
    recommendation_latency.observe(latency)

    return recs

@app.post("/track/click")
async def track_click(user_id: str, item_id: str):
    recommendation_clicks.inc()
    # Alert if CTR drops below 3%
```

### 6. Stale Features = Outdated Recommendations
**Problem**: User preferences change but features don't update, recommendations irrelevant.

**Solution**: Set appropriate TTLs and update triggers:
```python
class FeatureStore:
    def __init__(self, redis_client):
        self.redis = redis_client
        # Shorter TTL for frequently changing features
        self.user_ttl = 300  # 5 minutes
        self.item_ttl = 3600  # 1 hour

    def update_on_event(self, user_id: str, event: str):
        # Invalidate on important events
        if event in ['purchase', 'rating']:
            self.redis.delete(f"user_features:{user_id}")
            logger.info(f"Refreshed features for {user_id}")
```

### 7. A/B Test Sample Size Too Small
**Problem**: Declare winner too early, results not statistically significant.

**Solution**: Calculate required sample size first:
```python
def calculate_sample_size(
    baseline_rate: float,
    min_detectable_effect: float,
    alpha: float = 0.05,
    power: float = 0.8
) -> int:
    """Calculate required sample size per variant."""
    from scipy import stats

    z_alpha = stats.norm.ppf(1 - alpha/2)
    z_beta = stats.norm.ppf(power)

    p1 = baseline_rate
    p2 = baseline_rate * (1 + min_detectable_effect)
    p_avg = (p1 + p2) / 2

    n = (
        (z_alpha + z_beta)**2 * 2 * p_avg * (1 - p_avg) /
        (p2 - p1)**2
    )

    return int(n)

# Example: detect 10% lift with baseline CTR=5%
n_required = calculate_sample_size(
    baseline_rate=0.05,
    min_detectable_effect=0.10
)
print(f"Required sample size: {n_required} per variant")
# Wait until both variants reach this size before concluding
```

## When to Load References

Load reference files for detailed production implementations:

- **Production Architecture**: Load `references/production-architecture.md` for complete FeatureStore, ModelServing, and RecommendationService implementations with batch fetching, caching integration, and FastAPI deployment patterns.

- **Caching Strategies**: Load `references/caching-strategies.md` when implementing multi-tier caching (L1/L2/L3), cache warming, invalidation strategies, probabilistic refresh, or thundering herd prevention.

- **A/B Testing Framework**: Load `references/ab-testing-framework.md` for deterministic variant assignment, Thompson sampling (multi-armed bandits), Bayesian and frequentist significance testing, and experiment tracking.

- **Monitoring & Alerting**: Load `references/monitoring-alerting.md` for Prometheus metrics integration, dashboard endpoints, alert rules, and quality monitoring (diversity, coverage).

## Best Practices

1. **Feature Precomputation**: Compute features offline, serve from cache
2. **Batch Fetching**: Use Redis MGET for multiple users/items
3. **Cache Aggressively**: 5-15 minute TTL for user recommendations
4. **Fail Gracefully**: Return popular items if personalization fails
5. **Monitor Everything**: Track CTR, latency, diversity, coverage
6. **A/B Test Continuously**: Always be experimenting with new algorithms
7. **Diversity Constraint**: Ensure varied recommendations
8. **Explain Recommendations**: Provide reasons ("Highly rated", "Popular")

## Common Patterns

### Recommendation Service
```python
class RecommendationService:
    def __init__(self, feature_store, model_serving, cache):
        self.feature_store = feature_store
        self.model_serving = model_serving
        self.cache = cache

    def get_recommendations(self, user_id: str, n: int = 10):
        # 1. Check cache
        cached = self.cache.get(f"recs:{user_id}:{n}")
        if cached:
            return cached

        # 2. Get features
        user_features = self.feature_store.get_user_features(user_id)
        candidates = self.get_candidates(user_id)

        # 3. Score candidates
        scores = self.model_serving.predict(user_features, candidates)

        # 4. Rank with diversity
        recommendations = self.rank_with_diversity(candidates, scores, n)

        # 5. Cache
        self.cache.set(f"recs:{user_id}:{n}", recommendations, ttl=300)

        return recommendations
```

### A/B Testing
```python
def assign_variant(user_id: str, experiment_id: str) -> str:
    """Deterministic assignment - same user always gets same variant."""
    import hashlib

    hash_input = f"{user_id}:{experiment_id}"
    hash_value = int(hashlib.md5(hash_input.encode()).hexdigest(), 16)

    # 50/50 split
    return 'control' if hash_value % 2 == 0 else 'treatment'

# Usage
variant = assign_variant('user_123', 'rec_algo_v2')
model_name = 'main' if variant == 'control' else 'experimental'
recs = get_recommendations(user_id, model_name=model_name)
```

### Monitoring
```python
from prometheus_client import Counter, Histogram

requests_total = Counter('recommendation_requests_total', ['status'])
latency_seconds = Histogram('recommendation_latency_seconds')

@app.post("/recommendations")
async def get_recommendations(user_id: str):
    with latency_seconds.time():
        try:
            recs = generate_recs(user_id)
            requests_total.labels(status='success').inc()
            return recs
        except Exception as e:
            requests_total.labels(status='error').inc()
            raise
```
