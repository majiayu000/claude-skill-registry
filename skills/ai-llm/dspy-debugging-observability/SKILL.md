---
name: dspy-debugging-observability
version: "1.0.0"
dspy-compatibility: "3.1.2"
description: This skill should be used when the user asks to "debug DSPy programs", "trace LLM calls", "monitor production DSPy", "use MLflow with DSPy", mentions "inspect_history", "custom callbacks", "observability", "production monitoring", "cost tracking", or needs to debug, trace, and monitor DSPy applications in development and production.
allowed-tools:
  - Read
  - Write
  - Glob
  - Grep
---

# DSPy Debugging & Observability

## Goal

Debug, trace, and monitor DSPy programs using built-in inspection, MLflow tracing, and custom callbacks for production observability.

## When to Use

- Debugging unexpected outputs
- Understanding multi-step program flow
- Production monitoring (cost, latency, errors)
- Analyzing optimizer behavior
- Tracking LLM API usage

## Related Skills

- Optimize programs: [dspy-miprov2-optimizer](../dspy-miprov2-optimizer/SKILL.md)
- Evaluate quality: [dspy-evaluation-suite](../dspy-evaluation-suite/SKILL.md)
- Build agents: [dspy-react-agent-builder](../dspy-react-agent-builder/SKILL.md)

## Inputs

| Input | Type | Description |
|-------|------|-------------|
| `program` | `dspy.Module` | Program to debug/monitor |
| `callback` | `BaseCallback` | Optional custom callback (subclass of `dspy.utils.callback.BaseCallback`) |

## Outputs

| Output | Type | Description |
|--------|------|-------------|
| `GLOBAL_HISTORY` | `list[dict]` | Raw execution trace from `dspy.clients.base_lm` |
| `metrics` | `dict` | Cost, latency, token counts from callbacks |

## Workflow

### Phase 1: Basic Inspection with inspect_history()

The simplest debugging approach:

```python
import dspy

dspy.configure(lm=dspy.LM("openai/gpt-4o-mini"))

# Run program
qa = dspy.ChainOfThought("question -> answer")
result = qa(question="What is the capital of France?")

# Inspect last execution (prints to console)
dspy.inspect_history(n=1)

# To access raw history programmatically:
from dspy.clients.base_lm import GLOBAL_HISTORY
for entry in GLOBAL_HISTORY[-1:]:
    print(f"Model: {entry['model']}")
    print(f"Usage: {entry.get('usage', {})}")
    print(f"Cost: {entry.get('cost', 0)}")
```

### Phase 2: MLflow Tracing

MLflow integration requires explicit setup:

```python
import dspy
import mlflow

# Setup MLflow (4 steps required)
# 1. Set tracking URI and experiment
mlflow.set_tracking_uri("http://localhost:5000")
mlflow.set_experiment("DSPy")

# 2. Enable DSPy autologging
mlflow.dspy.autolog(
    log_traces=True,              # Log traces during inference
    log_traces_from_compile=True, # Log traces when compiling/optimizing
    log_traces_from_eval=True,    # Log traces during evaluation
    log_compiles=True,            # Log optimization process info
    log_evals=True                # Log evaluation call info
)

dspy.configure(lm=dspy.LM("openai/gpt-4o-mini"))

# Configure retriever (required before using dspy.Retrieve)
rm = dspy.ColBERTv2(url="http://20.102.90.50:2017/wiki17_abstracts")
dspy.configure(rm=rm)

class RAGPipeline(dspy.Module):
    def __init__(self):
        self.retrieve = dspy.Retrieve(k=3)
        self.generate = dspy.ChainOfThought("context, question -> answer")

    def forward(self, question):
        context = self.retrieve(question).passages
        return self.generate(context=context, question=question)

pipeline = RAGPipeline()
result = pipeline(question="What is machine learning?")

# View traces in MLflow UI (run in terminal): mlflow ui --port 5000
```

MLflow captures LLM calls, token usage, costs, and execution times when autolog is enabled.

### Phase 3: Custom Callbacks for Production

Build custom callbacks for specialized monitoring:

```python
import dspy
from dspy.utils.callback import BaseCallback
import logging
import time
from typing import Any

logger = logging.getLogger(__name__)

class ProductionMonitoringCallback(BaseCallback):
    """Track cost, latency, and errors in production."""

    def __init__(self):
        super().__init__()
        self.total_cost = 0.0
        self.total_tokens = 0
        self.call_count = 0
        self.errors = []
        self.start_times = {}

    def on_lm_start(self, call_id: str, instance: Any, inputs: dict[str, Any]):
        """Called when LM is invoked."""
        self.start_times[call_id] = time.time()

    def on_lm_end(self, call_id: str, outputs: dict[str, Any] | None, exception: Exception | None = None):
        """Called after LM finishes."""
        if exception:
            self.errors.append(str(exception))
            logger.error(f"LLM error: {exception}")
            return

        # Calculate latency
        start = self.start_times.pop(call_id, time.time())
        latency = time.time() - start

        # Extract usage from outputs
        usage = outputs.get('usage', {}) if isinstance(outputs, dict) else {}
        tokens = usage.get('total_tokens', 0)
        model = outputs.get('model', 'unknown') if isinstance(outputs, dict) else 'unknown'
        cost = self._estimate_cost(model, usage)

        self.total_tokens += tokens
        self.total_cost += cost
        self.call_count += 1

        logger.info(f"LLM call: {latency:.2f}s, {tokens} tokens, ${cost:.4f}")

    def _estimate_cost(self, model: str, usage: dict[str, int]) -> float:
        """Estimate cost based on model pricing (update rates for 2026)."""
        pricing = {
            'gpt-4o-mini': {'input': 0.00015 / 1000, 'output': 0.0006 / 1000},
            'gpt-4o': {'input': 0.0025 / 1000, 'output': 0.01 / 1000},
        }
        model_key = next((k for k in pricing if k in model), 'gpt-4o-mini')
        input_cost = usage.get('prompt_tokens', 0) * pricing[model_key]['input']
        output_cost = usage.get('completion_tokens', 0) * pricing[model_key]['output']
        return input_cost + output_cost

    def get_metrics(self) -> dict[str, Any]:
        """Return aggregated metrics."""
        return {
            'total_cost': self.total_cost,
            'total_tokens': self.total_tokens,
            'call_count': self.call_count,
            'avg_cost_per_call': self.total_cost / max(self.call_count, 1),
            'error_count': len(self.errors)
        }

# Usage
monitor = ProductionMonitoringCallback()
dspy.configure(lm=dspy.LM("openai/gpt-4o-mini"), callbacks=[monitor])

# Run your program
qa = dspy.ChainOfThought("question -> answer")
for question in questions:
    result = qa(question=question)

# Get metrics
metrics = monitor.get_metrics()
print(f"Total cost: ${metrics['total_cost']:.2f}")
print(f"Total calls: {metrics['call_count']}")
print(f"Errors: {metrics['error_count']}")
```

### Phase 4: Sampling for High-Volume Production

For high-traffic applications, sample traces to reduce overhead:

```python
import random
from dspy.utils.callback import BaseCallback
from typing import Any

class SamplingCallback(BaseCallback):
    """Sample 10% of traces."""

    def __init__(self, sample_rate: float = 0.1):
        super().__init__()
        self.sample_rate = sample_rate
        self.sampled_calls = []

    def on_lm_end(self, call_id: str, outputs: dict[str, Any] | None, exception: Exception | None = None):
        """Sample a subset of LM calls."""
        if random.random() < self.sample_rate:
            self.sampled_calls.append({
                'call_id': call_id,
                'outputs': outputs,
                'exception': exception
            })

# Use with high-volume apps
callback = SamplingCallback(sample_rate=0.1)
dspy.configure(lm=dspy.LM("openai/gpt-4o-mini"), callbacks=[callback])
```

## Best Practices

1. **Use inspect_history() for debugging** - Quick inspection during development
2. **MLflow for comprehensive tracing** - Automatic instrumentation in production
3. **Sample high-volume traces** - Reduce overhead with 1-10% sampling
4. **Privacy-aware logging** - Redact PII before logging
5. **Async callbacks** - Non-blocking callbacks for production

## Limitations

- Callbacks are synchronous by default (can block LLM calls)
- MLflow tracing adds ~5-10ms overhead per call
- inspect_history() only stores recent calls (last 100 by default)
- Custom callbacks don't capture internal optimizer steps
- Cost estimation requires manual pricing table updates

## Official Documentation

- **DSPy Documentation**: https://dspy.ai/
- **DSPy GitHub**: https://github.com/stanfordnlp/dspy
- **Observability Guide**: https://dspy.ai/tutorials/observability/
