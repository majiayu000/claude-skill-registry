---
name: cost-aware-llm-pipeline
description: "Use when building an LLM-powered app that needs cost control via model routing, budget tracking, retry, and prompt caching."
license: MIT
metadata:
  author: shimo4228
  version: "1.0"
  extracted: "2026-02-08"
---

# Cost-Aware LLM Pipeline
# コスト最適化LLMパイプライン

**Extracted / 抽出日:** 2026-02-08
**Context / コンテキスト:** LLMを使うアプリで、コスト制御しながら品質を維持するパターン

---

## Problem / 課題

LLM APIは高コスト。全リクエストに最高性能モデルを使うと予算超過する。
リトライやキャッシュの仕組みがないと無駄なコストが発生する。

- 単純なタスクにも高価なモデルを使ってしまう
- 一時的なエラーでリトライせず失敗する
- 同じシステムプロンプトを毎回送信しトークンを浪費する
- 予算超過に気づかない

---

## Solution / 解決策

4つの要素を組み合わせる：

### 1. Model Routing（モデル自動選択）

タスクの複雑度に基づいてモデルを自動選択する。

```python
MODEL_SONNET = "claude-sonnet-4-5-20250929"
MODEL_HAIKU = "claude-haiku-4-5-20251001"

_SONNET_TEXT_THRESHOLD = 10_000  # chars
_SONNET_CARD_THRESHOLD = 30     # items

def select_model(
    text_length: int,
    item_count: int,
    force_model: str | None = None,
) -> str:
    """Automatically select model based on task complexity."""
    if force_model is not None:
        return force_model
    if text_length >= _SONNET_TEXT_THRESHOLD or item_count >= _SONNET_CARD_THRESHOLD:
        return MODEL_SONNET  # Complex task
    return MODEL_HAIKU  # Simple task (3-4x cheaper)
```

### 2. Immutable Cost Tracking（不変コスト追跡）

```python
from dataclasses import dataclass

@dataclass(frozen=True, slots=True)
class CostRecord:
    model: str
    input_tokens: int
    output_tokens: int
    cost_usd: float

@dataclass(frozen=True, slots=True)
class CostTracker:
    budget_limit: float = 1.00
    records: tuple[CostRecord, ...] = ()

    def add(self, record: CostRecord) -> "CostTracker":
        """Return new tracker with added record (never mutates self)."""
        return CostTracker(
            budget_limit=self.budget_limit,
            records=(*self.records, record),
        )

    @property
    def total_cost(self) -> float:
        return sum(r.cost_usd for r in self.records)

    @property
    def over_budget(self) -> bool:
        return self.total_cost > self.budget_limit
```

### 3. Narrow Retry Logic（限定的リトライ）

```python
from anthropic import (
    APIConnectionError,
    InternalServerError,
    RateLimitError,
)

_RETRYABLE_ERRORS = (APIConnectionError, RateLimitError, InternalServerError)
_MAX_RETRIES = 3

def _call_with_retry(func, *, max_retries: int = _MAX_RETRIES):
    """Retry only on transient errors, fail fast on others."""
    for attempt in range(max_retries):
        try:
            return func()
        except _RETRYABLE_ERRORS:
            if attempt == max_retries - 1:
                raise
            time.sleep(2 ** attempt)  # Exponential backoff
    # AuthenticationError, BadRequestError etc. → raise immediately
```

### 4. Prompt Caching（プロンプトキャッシュ）

```python
messages = [
    {
        "role": "user",
        "content": [
            {
                "type": "text",
                "text": system_prompt,
                "cache_control": {"type": "ephemeral"},  # Cache this
            },
            {
                "type": "text",
                "text": user_input,  # Variable part
            },
        ],
    }
]
```

---

## Composition / 組み合わせ方

```python
def process(text: str, config: Config, tracker: CostTracker) -> tuple[Result, CostTracker]:
    # 1. Route model
    model = select_model(len(text), estimated_items, config.force_model)

    # 2. Check budget
    if tracker.over_budget:
        raise BudgetExceededError(tracker.total_cost, tracker.budget_limit)

    # 3. Call with retry + caching
    response = _call_with_retry(lambda: client.messages.create(
        model=model,
        messages=build_cached_messages(system_prompt, text),
    ))

    # 4. Track cost (immutable)
    record = CostRecord(model=model, input_tokens=..., output_tokens=..., cost_usd=...)
    tracker = tracker.add(record)

    return parse_result(response), tracker
```

---

## Pricing Reference (2025-2026) / 価格参考

| Model | Input ($/1M tokens) | Output ($/1M tokens) |
|-------|---------------------|----------------------|
| Haiku 4.5 | $0.80 | $4.00 |
| Sonnet 4.5 | $3.00 | $15.00 |
| Opus 4.5 | $15.00 | $75.00 |

---

## When to Use / 使用すべき場面

- Claude/OpenAI APIを使うアプリケーション全般
- バッチ処理でコスト管理が必要な場合
- 複数モデルを使い分けたい場合
- 長いシステムプロンプトを繰り返し送信する場合

---

## Related Patterns / 関連パターン

- `python-immutable-accumulator.md` — CostTrackerの不変蓄積パターン
- `immutable-model-updates.md` — Swift版の不変更新パターン
