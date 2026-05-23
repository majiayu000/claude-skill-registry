---
name: deepeval
description: Use when discussing or working with DeepEval (the python AI evaluation framework)
---

# DeepEval

## Overview

DeepEval is a pytest-based framework for testing LLM applications. It provides 50+ evaluation metrics covering RAG pipelines, conversational AI, agents, safety, and custom criteria. DeepEval integrates into development workflows through pytest, supports multiple LLM providers, and includes component-level tracing with the `@observe` decorator.

**Repository:** https://github.com/confident-ai/deepeval
**Documentation:** https://deepeval.com

## Installation

```bash
pip install -U deepeval
```

Requires Python 3.9+.

## Quick Start

### Basic pytest test

```python
import pytest
from deepeval import assert_test
from deepeval.test_case import LLMTestCase
from deepeval.metrics import AnswerRelevancyMetric

def test_chatbot():
    metric = AnswerRelevancyMetric(threshold=0.7, model="athropic-claude-sonnet-4-5")
    test_case = LLMTestCase(
        input="What if these shoes don't fit?",
        actual_output="You have 30 days for full refund"
    )
    assert_test(test_case, [metric])
```

Run with: `deepeval test run test_chatbot.py`

### Environment setup

DeepEval automatically loads `.env.local` then `.env`:

```bash
# .env
OPENAI_API_KEY="sk-..."
```

## Core Workflows

### RAG Evaluation

Evaluate both retrieval and generation phases:

```python
from deepeval.metrics import (
    ContextualPrecisionMetric,
    ContextualRecallMetric,
    ContextualRelevancyMetric,
    AnswerRelevancyMetric,
    FaithfulnessMetric
)

# Retrieval metrics
contextual_precision = ContextualPrecisionMetric(threshold=0.7)
contextual_recall = ContextualRecallMetric(threshold=0.7)
contextual_relevancy = ContextualRelevancyMetric(threshold=0.7)

# Generation metrics
answer_relevancy = AnswerRelevancyMetric(threshold=0.7)
faithfulness = FaithfulnessMetric(threshold=0.8)

test_case = LLMTestCase(
    input="What are the side effects of aspirin?",
    actual_output="Common side effects include stomach upset and nausea.",
    expected_output="Aspirin side effects include gastrointestinal issues.",
    retrieval_context=[
        "Aspirin common side effects: stomach upset, nausea, vomiting.",
        "Serious aspirin side effects: gastrointestinal bleeding.",
    ]
)

evaluate(test_cases=[test_case], metrics=[
    contextual_precision, contextual_recall, contextual_relevancy,
    answer_relevancy, faithfulness
])
```

**Component-level tracing:**

```python
from deepeval.tracing import observe, update_current_span

@observe(metrics=[contextual_relevancy])
def retriever(query: str):
    chunks = your_vector_db.search(query)
    update_current_span(
        test_case=LLMTestCase(input=query, retrieval_context=chunks)
    )
    return chunks

@observe(metrics=[answer_relevancy, faithfulness])
def generator(query: str, chunks: list):
    response = your_llm.generate(query, chunks)
    update_current_span(
        test_case=LLMTestCase(
            input=query,
            actual_output=response,
            retrieval_context=chunks
        )
    )
    return response

@observe
def rag_pipeline(query: str):
    chunks = retriever(query)
    return generator(query, chunks)
```

### Conversational AI Evaluation

Test multi-turn dialogues:

```python
from deepeval.test_case import Turn, ConversationalTestCase
from deepeval.metrics import (
    RoleAdherenceMetric,
    KnowledgeRetentionMetric,
    ConversationCompletenessMetric,
    TurnRelevancyMetric
)

convo_test_case = ConversationalTestCase(
    chatbot_role="professional, empathetic medical assistant",
    turns=[
        Turn(role="user", content="I have a persistent cough"),
        Turn(role="assistant", content="How long have you had this cough?"),
        Turn(role="user", content="About a week now"),
        Turn(role="assistant", content="A week-long cough should be evaluated.")
    ]
)

metrics = [
    RoleAdherenceMetric(threshold=0.7),
    KnowledgeRetentionMetric(threshold=0.7),
    ConversationCompletenessMetric(threshold=0.6),
    TurnRelevancyMetric(threshold=0.7)
]

evaluate(test_cases=[convo_test_case], metrics=metrics)
```

### Agent Evaluation

Test tool usage and task completion:

```python
from deepeval.test_case import ToolCall
from deepeval.metrics import (
    TaskCompletionMetric,
    ToolUseMetric,
    ArgumentCorrectnessMetric
)

agent_test_case = ConversationalTestCase(
    turns=[
        Turn(role="user", content="When did Trump first raise tariffs?"),
        Turn(
            role="assistant",
            content="Let me search for that information.",
            tools_called=[
                ToolCall(
                    name="WebSearch",
                    arguments={"query": "Trump first raised tariffs year"}
                )
            ]
        ),
        Turn(role="assistant", content="Trump first raised tariffs in 2018.")
    ]
)

evaluate(
    test_cases=[agent_test_case],
    metrics=[
        TaskCompletionMetric(threshold=0.7),
        ToolUseMetric(threshold=0.7),
        ArgumentCorrectnessMetric(threshold=0.7)
    ]
)
```

### Safety Evaluation

Check for harmful content:

```python
from deepeval.metrics import (
    ToxicityMetric,
    BiasMetric,
    PIILeakageMetric,
    HallucinationMetric
)

def safety_gate(output: str, input: str) -> tuple[bool, list]:
    """Returns (passed, reasons) tuple"""
    test_case = LLMTestCase(input=input, actual_output=output)

    safety_metrics = [
        ToxicityMetric(threshold=0.5),
        BiasMetric(threshold=0.5),
        PIILeakageMetric(threshold=0.5)
    ]

    failures = []
    for metric in safety_metrics:
        metric.measure(test_case)
        if not metric.is_successful():
            failures.append(f"{metric.name}: {metric.reason}")

    return len(failures) == 0, failures
```

## Metric Selection Guide

### RAG Metrics

**Retrieval Phase:**
- `ContextualPrecisionMetric` - Relevant chunks ranked higher than irrelevant ones
- `ContextualRecallMetric` - All necessary information retrieved
- `ContextualRelevancyMetric` - Retrieved chunks relevant to input

**Generation Phase:**
- `AnswerRelevancyMetric` - Output addresses the input query
- `FaithfulnessMetric` - Output grounded in retrieval context

### Conversational Metrics

- `TurnRelevancyMetric` - Each turn relevant to conversation
- `KnowledgeRetentionMetric` - Information retained across turns
- `ConversationCompletenessMetric` - All aspects addressed
- `RoleAdherenceMetric` - Chatbot maintains assigned role
- `TopicAdherenceMetric` - Conversation stays on topic

### Agent Metrics

- `TaskCompletionMetric` - Task successfully completed
- `ToolUseMetric` - Correct tools selected
- `ArgumentCorrectnessMetric` - Tool arguments correct
- `MCPUseMetric` - MCP correctly used

### Safety Metrics

- `ToxicityMetric` - Harmful content detection
- `BiasMetric` - Biased outputs identification
- `HallucinationMetric` - Fabricated information
- `PIILeakageMetric` - Personal information leakage

### Custom Metrics

**G-Eval (LLM-based):**

```python
from deepeval.metrics import GEval
from deepeval.test_case import LLMTestCaseParams

custom_metric = GEval(
    name="Professional Tone",
    criteria="Determine if response maintains professional, empathetic tone",
    evaluation_params=[LLMTestCaseParams.ACTUAL_OUTPUT],
    threshold=0.7,
    model="anthropic-claude-sonnet-4-5"
)
```

**BaseMetric subclass:**

See `references/custom_metrics.md` for complete guide on creating custom metrics with BaseMetric subclassing and deterministic scorers (ROUGE, BLEU, BERTScore).

## Configuration

### LLM Provider Setup

DeepEval supports OpenAI, Anthropic Claude, Google Gemini, AWS Bedrock, and 100+ providers via LiteLLM.
Anthropic models are preferred.

**CLI configuration (global):**

```bash
deepeval set-azure-openai --openai-endpoint=... --openai-api-key=... --deployment-name=...
deepeval set-ollama deepseek-r1:1.5b
```

**Python configuration (per-metric):**

```python
from deepeval.models import AnthropicModel, OllamaModel

anthropic_model = AnthropicModel(
    model_id=settings.anthropic_model_id,
    client_args={"api_key": settings.anthropic_api_key},
    temperature=settings.agent_temperature
)

metric = AnswerRelevancyMetric(model=anthropic_model)
```

See `references/model_providers.md` for complete provider configuration guide.

### Performance Optimisation

Async mode is enabled by default. Configure with `AsyncConfig` and `CacheConfig`:

```python
from deepeval import evaluate, AsyncConfig, CacheConfig

evaluate(
    test_cases=[...],
    metrics=[...],
    async_config=AsyncConfig(
        run_async=True,
        max_concurrent=20,    # Reduce if rate limited
        throttle_value=0      # Delay between test cases (seconds)
    ),
    cache_config=CacheConfig(
        use_cache=True,       # Read from cache
        write_cache=True      # Write to cache
    )
)
```

**CLI parallelisation:**

```bash
deepeval test run -n 4 -c -i  # 4 processes, cached, ignore errors
```

**Best practices:**
- Limit to 5 metrics maximum (2-3 generic + 1-2 custom)
- Use the latest available Anthropic Claude Sonnet or Haiku models
- Reduce `max_concurrent` to 5 if hitting rate limits
- Use `evaluate()` function over individual `measure()` calls

See `references/async_performance.md` for detailed performance optimisation guide.

## Dataset Management

### Loading datasets

```python
from deepeval.dataset import EvaluationDataset, Golden

dataset = EvaluationDataset()

# From CSV
dataset.add_goldens_from_csv_file(
    file_path="./test_data.csv",
    input_col_name="question",
    expected_output_col_name="answer",
    context_col_name="context",
    context_col_delimiter="|"
)

# From JSON
dataset.add_goldens_from_json_file(
    file_path="./test_data.json",
    input_key_name="query",
    expected_output_key_name="response"
)
```

### Synthetic generation

```python
from deepeval.synthesizer import Synthesizer

synthesizer = Synthesizer()

# From documents
goldens = synthesizer.generate_goldens_from_docs(
    document_paths=["./docs/knowledge_base.pdf"],
    max_goldens_per_document=10,
    evolution_types=["REASONING", "MULTICONTEXT", "COMPARATIVE"]
)

# From scratch
goldens = synthesizer.generate_goldens_from_scratch(
    subject="customer support for SaaS product",
    task="answer user questions about billing",
    max_goldens=20
)
```

**Evolution types:** REASONING, MULTICONTEXT, CONCRETISING, CONSTRAINED, COMPARATIVE, HYPOTHETICAL, IN_BREADTH

See `references/dataset_management.md` for complete dataset guide including versioning and cloud integration.

## Test Case Types

### Single-turn (LLMTestCase)

```python
from deepeval.test_case import LLMTestCase

test_case = LLMTestCase(
    input="What if these shoes don't fit?",
    actual_output="You have 30 days for full refund",
    expected_output="We offer 30-day full refund",
    retrieval_context=["All customers eligible for 30 day refund"],
    tools_called=[ToolCall(name="...", arguments={"...": "..."})]
)
```

### Multi-turn (ConversationalTestCase)

```python
from deepeval.test_case import Turn, ConversationalTestCase

convo_test_case = ConversationalTestCase(
    chatbot_role="helpful customer service agent",
    turns=[
        Turn(role="user", content="I need help with my order"),
        Turn(role="assistant", content="I'd be happy to help"),
        Turn(role="user", content="It hasn't arrived yet")
    ]
)
```

### Multimodal (MLLMTestCase)

```python
from deepeval.test_case import MLLMTestCase, MLLMImage

m_test_case = MLLMTestCase(
    input=["Describe this image", MLLMImage(url="./photo.png", local=True)],
    actual_output=["A red bicycle leaning against a wall"]
)
```

## CI/CD Integration

```yaml
# .github/workflows/test.yml
name: LLM Tests
on: [push, pull_request]

jobs:
  evaluate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v5
      - name: Install dependencies
        run: pip install deepeval
      - name: Run evaluations
        env:
          OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}
        run: deepeval test run tests/
```

## References

Detailed implementation guides:

- **references/model_providers.md** - Complete guide for configuring OpenAI, Anthropic, Gemini, Bedrock, and local models. Includes provider-specific considerations, cost analysis, and troubleshooting.

- **references/custom_metrics.md** - Complete guide for creating custom metrics by subclassing BaseMetric. Includes deterministic scorers (ROUGE, BLEU, BERTScore) and LLM-based evaluation patterns.

- **references/async_performance.md** - Complete guide for optimising evaluation performance with async mode, caching, concurrency tuning, and rate limit handling.

- **references/dataset_management.md** - Complete guide for dataset loading, saving, synthetic generation, versioning, and cloud integration with Confident AI.

## Best Practices

### Metric Selection
- Match metrics to use case (RAG systems need retrieval + generation metrics)
- Start with 2-3 essential metrics, expand as needed
- Use appropriate thresholds (0.7-0.8 for production, 0.5-0.6 for development)
- Combine complementary metrics (answer relevancy + faithfulness)

### Test Case Design
- Create representative examples covering common queries and edge cases
- Include context when needed (`retrieval_context` for RAG, `expected_output` for G-Eval)
- Use datasets for scale testing
- Version test cases over time

### Evaluation Workflow
- Component-level first - Use `@observe` for individual parts
- End-to-end validation before deployment
- Automate in CI/CD with `deepeval test run`
- Track results over time with Confident AI cloud

### Testing Anti-Patterns

**Avoid:**
- Testing only happy paths
- Using unrealistic inputs
- Ignoring metric reasons
- Setting thresholds too high initially
- Running full test suite on every change

**Do:**
- Test edge cases and failure modes
- Use real user queries as test inputs
- Read and analyse metric reasons
- Adjust thresholds based on empirical results
- Use component-level tests during development
- Separate config and eval content from code
