---
name: llm-testing
description: Testing patterns for LLM-based applications. Use when testing AI/ML integrations, mocking LLM responses, testing async timeouts, or validating structured outputs from LLMs.
context: fork
agent: test-generator
version: 2.0.0
tags: [testing, llm, ai, deepeval, ragas, 2026]
author: SkillForge
user-invocable: false
---

# LLM Testing Patterns

Test AI applications with deterministic patterns using DeepEval and RAGAS.

## Quick Reference

### Mock LLM Responses

```python
from unittest.mock import AsyncMock, patch

@pytest.fixture
def mock_llm():
    mock = AsyncMock()
    mock.return_value = {"content": "Mocked response", "confidence": 0.85}
    return mock

@pytest.mark.asyncio
async def test_with_mocked_llm(mock_llm):
    with patch("app.core.model_factory.get_model", return_value=mock_llm):
        result = await synthesize_findings(sample_findings)
    assert result["summary"] is not None
```

### DeepEval Quality Testing

```python
from deepeval import assert_test
from deepeval.test_case import LLMTestCase
from deepeval.metrics import AnswerRelevancyMetric, FaithfulnessMetric

test_case = LLMTestCase(
    input="What is the capital of France?",
    actual_output="The capital of France is Paris.",
    retrieval_context=["Paris is the capital of France."],
)

metrics = [
    AnswerRelevancyMetric(threshold=0.7),
    FaithfulnessMetric(threshold=0.8),
]

assert_test(test_case, metrics)
```

### Timeout Testing

```python
import asyncio
import pytest

@pytest.mark.asyncio
async def test_respects_timeout():
    with pytest.raises(asyncio.TimeoutError):
        async with asyncio.timeout(0.1):
            await slow_llm_call()
```

## Quality Metrics (2026)

| Metric | Threshold | Purpose |
|--------|-----------|---------|
| Answer Relevancy | ≥ 0.7 | Response addresses question |
| Faithfulness | ≥ 0.8 | Output matches context |
| Hallucination | ≤ 0.3 | No fabricated facts |
| Context Precision | ≥ 0.7 | Retrieved contexts relevant |

## Anti-Patterns (FORBIDDEN)

```python
# ❌ NEVER test against live LLM APIs in CI
response = await openai.chat.completions.create(...)

# ❌ NEVER use random seeds (non-deterministic)
model.generate(seed=random.randint(0, 100))

# ❌ NEVER skip timeout handling
await llm_call()  # No timeout!

# ✅ ALWAYS mock LLM in unit tests
with patch("app.llm", mock_llm):
    result = await function_under_test()

# ✅ ALWAYS use VCR.py for integration tests
@pytest.mark.vcr()
async def test_llm_integration():
    ...
```

## Key Decisions

| Decision | Recommendation |
|----------|----------------|
| Mock vs VCR | VCR for integration, mock for unit |
| Timeout | Always test with < 1s timeout |
| Schema validation | Test both valid and invalid |
| Edge cases | Test all null/empty paths |
| Quality metrics | Use multiple dimensions (3-5) |

## Detailed Documentation

| Resource | Description |
|----------|-------------|
| [references/deepeval-ragas-api.md](references/deepeval-ragas-api.md) | DeepEval & RAGAS API reference |
| [examples/test-patterns.md](examples/test-patterns.md) | Complete test examples |
| [checklists/llm-test-checklist.md](checklists/llm-test-checklist.md) | Setup and review checklists |
| [templates/llm-test-template.py](templates/llm-test-template.py) | Starter test template |

## Related Skills

- `vcr-http-recording` - Record LLM responses
- `llm-evaluation` - Quality assessment
- `unit-testing` - Test fundamentals

## Capability Details

### llm-response-mocking
**Keywords:** mock LLM, fake response, stub LLM, mock AI
**Solves:**
- Mock LLM responses in tests
- Create deterministic AI test fixtures
- Avoid live API calls in CI

### async-timeout-testing
**Keywords:** timeout, async test, wait for, polling
**Solves:**
- Test async LLM operations
- Handle timeout scenarios
- Implement polling assertions

### structured-output-validation
**Keywords:** structured output, JSON validation, schema validation, output format
**Solves:**
- Validate structured LLM output
- Test JSON schema compliance
- Assert output structure

### deepeval-assertions
**Keywords:** DeepEval, assert_test, LLMTestCase, metric assertion
**Solves:**
- Use DeepEval for LLM assertions
- Implement metric-based tests
- Configure quality thresholds

### golden-dataset-testing
**Keywords:** golden dataset, golden test, reference output, expected output
**Solves:**
- Test against golden datasets
- Compare with reference outputs
- Implement regression testing

### vcr-recording
**Keywords:** VCR, cassette, record, replay, HTTP recording
**Solves:**
- Record LLM API responses
- Replay recordings in tests
- Create deterministic test suites
