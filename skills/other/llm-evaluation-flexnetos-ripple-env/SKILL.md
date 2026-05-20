---
name: llm-evaluation
description: LLM testing and evaluation tools including promptfoo, trulens, and evals frameworks
icon: 🧪
category: ai
tools:
  - promptfoo
  - trulens
  - openai-evals
---

# LLM Evaluation Skills

## Overview

This skill provides expertise in testing, evaluating, and monitoring LLM-based systems for robotics agents and AI assistants.

## promptfoo - LLM Testing Framework

promptfoo is a CLI tool for testing and evaluating LLM prompts systematically.

### Installation

```bash
# Via npm
npm install -g promptfoo

# Or via npx (no install)
npx promptfoo@latest

# Via Nix
nix profile install nixpkgs#promptfoo
```

### Basic Configuration

```yaml
# promptfooconfig.yaml
description: "Robot command parser evaluation"

providers:
  - openai:gpt-4
  - anthropic:claude-3-sonnet-20240229
  - ollama:llama2

prompts:
  - file://prompts/robot_command.txt
  - |
    Parse the following user command into a structured robot action:
    Command: {{command}}

    Output JSON with: action, target, parameters

tests:
  - vars:
      command: "Move forward 2 meters"
    assert:
      - type: contains-json
      - type: javascript
        value: output.action === 'move'

  - vars:
      command: "Pick up the red box"
    assert:
      - type: contains-json
      - type: javascript
        value: output.action === 'pick' && output.target === 'red box'

  - vars:
      command: "Navigate to the charging station"
    assert:
      - type: llm-rubric
        value: "The output should identify navigation as the action and charging station as the destination"
```

### Test Assertions

```yaml
tests:
  # Exact match
  - vars: { input: "hello" }
    assert:
      - type: equals
        value: "Hello! How can I help?"

  # Contains substring
  - assert:
      - type: contains
        value: "error"

  # JSON validation
  - assert:
      - type: is-json
      - type: contains-json
        value:
          action: "move"

  # JavaScript evaluation
  - assert:
      - type: javascript
        value: |
          const parsed = JSON.parse(output);
          return parsed.confidence > 0.8;

  # LLM-as-judge
  - assert:
      - type: llm-rubric
        value: "Response should be helpful and accurate"

  # Latency check
  - assert:
      - type: latency
        threshold: 2000  # ms

  # Cost check
  - assert:
      - type: cost
        threshold: 0.01  # dollars

  # Similarity
  - assert:
      - type: similar
        value: "expected response"
        threshold: 0.8
```

### Running Tests

```bash
# Run evaluation
promptfoo eval

# With specific config
promptfoo eval -c promptfooconfig.yaml

# View results in browser
promptfoo view

# Output formats
promptfoo eval --output results.json
promptfoo eval --output results.csv

# Compare providers
promptfoo eval --table
```

### CI/CD Integration

```yaml
# .github/workflows/llm-tests.yml
name: LLM Evaluation

on:
  push:
    paths:
      - 'prompts/**'
      - 'promptfooconfig.yaml'

jobs:
  evaluate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20'

      - name: Install promptfoo
        run: npm install -g promptfoo

      - name: Run evaluation
        env:
          OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}
          ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
        run: |
          promptfoo eval --output results.json

      - name: Check for failures
        run: |
          if jq -e '.results.stats.failures > 0' results.json; then
            echo "LLM tests failed!"
            exit 1
          fi

      - name: Upload results
        uses: actions/upload-artifact@v4
        with:
          name: llm-eval-results
          path: results.json
```

### Robot Command Parser Example

```yaml
# promptfooconfig.yaml
description: "Robot NLU evaluation suite"

providers:
  - id: openai:gpt-4
    config:
      temperature: 0
  - id: anthropic:claude-3-sonnet-20240229
    config:
      temperature: 0

prompts:
  - |
    You are a robot command parser. Convert natural language commands to JSON.

    Output format:
    {
      "action": "move|pick|place|navigate|stop|rotate",
      "parameters": {...},
      "confidence": 0.0-1.0
    }

    Command: {{command}}

tests:
  # Movement commands
  - vars:
      command: "Go forward 3 meters"
    assert:
      - type: javascript
        value: |
          const r = JSON.parse(output);
          return r.action === 'move' && r.parameters.distance === 3;

  - vars:
      command: "Turn left 90 degrees"
    assert:
      - type: javascript
        value: |
          const r = JSON.parse(output);
          return r.action === 'rotate' && r.parameters.angle === 90;

  # Manipulation commands
  - vars:
      command: "Pick up the blue cube from the table"
    assert:
      - type: javascript
        value: |
          const r = JSON.parse(output);
          return r.action === 'pick' &&
                 r.parameters.object.includes('blue') &&
                 r.parameters.location === 'table';

  # Navigation commands
  - vars:
      command: "Go to the kitchen"
    assert:
      - type: javascript
        value: |
          const r = JSON.parse(output);
          return r.action === 'navigate' &&
                 r.parameters.destination === 'kitchen';

  # Edge cases
  - vars:
      command: "Do a backflip"
    assert:
      - type: javascript
        value: |
          const r = JSON.parse(output);
          return r.confidence < 0.5 || r.action === 'unknown';
```

## TruLens - LLM App Evaluation

TruLens provides feedback functions and tracing for LLM applications.

### Installation

```bash
pixi add trulens-eval
```

### Basic Usage

```python
from trulens_eval import Tru, TruChain, Feedback
from trulens_eval.feedback import Groundedness, GroundTruthAgreement
from trulens_eval.feedback.provider import OpenAI

# Initialize
tru = Tru()

# Create feedback functions
provider = OpenAI()

f_relevance = Feedback(provider.relevance).on_input_output()
f_coherence = Feedback(provider.coherence).on_output()
f_groundedness = Feedback(
    Groundedness(groundedness_provider=provider).groundedness_measure_with_cot_reasons
).on(
    TruChain.select_context(),
    output=True
)

# Wrap your LLM app
from langchain.chains import LLMChain

tru_chain = TruChain(
    chain,
    app_id="robot_assistant",
    feedbacks=[f_relevance, f_coherence, f_groundedness]
)

# Run with evaluation
with tru_chain as recording:
    response = tru_chain("Navigate to the warehouse")

# View results
tru.run_dashboard()
```

### Custom Feedback Functions

```python
from trulens_eval import Feedback, Select
from trulens_eval.feedback.provider import OpenAI

provider = OpenAI()

# Custom: Check if response is a valid robot command
def is_valid_robot_command(response: str) -> float:
    """Check if the response is a valid robot command JSON."""
    try:
        import json
        data = json.loads(response)
        required = ['action', 'parameters', 'confidence']
        if all(k in data for k in required):
            return 1.0
        return 0.5
    except:
        return 0.0

f_valid_command = Feedback(is_valid_robot_command).on_output()

# Custom: Safety check
def safety_check(response: str) -> float:
    """Check if command is safe to execute."""
    unsafe_keywords = ['maximum speed', 'override safety', 'ignore obstacle']
    response_lower = response.lower()
    for keyword in unsafe_keywords:
        if keyword in response_lower:
            return 0.0
    return 1.0

f_safety = Feedback(safety_check).on_output()
```

### RAG Evaluation

```python
from trulens_eval import TruChain
from trulens_eval.feedback import Groundedness

# For RAG systems
groundedness = Groundedness(groundedness_provider=OpenAI())

f_groundedness = (
    Feedback(groundedness.groundedness_measure_with_cot_reasons)
    .on(Select.RecordCalls.retrieve.rets.collect())  # Context
    .on_output()  # Response
    .aggregate(groundedness.grounded_statements_aggregator)
)

f_context_relevance = (
    Feedback(provider.qs_relevance)
    .on_input()
    .on(Select.RecordCalls.retrieve.rets[:])
    .aggregate(np.mean)
)
```

## Evaluation Metrics

### Standard Metrics

| Metric | Description | Use Case |
|--------|-------------|----------|
| Accuracy | Exact match rate | Classification |
| F1 Score | Precision/recall balance | Entity extraction |
| BLEU | N-gram overlap | Translation |
| ROUGE | Recall-based overlap | Summarization |
| BERTScore | Semantic similarity | General text |

### LLM-Specific Metrics

| Metric | Description | Use Case |
|--------|-------------|----------|
| Relevance | Response addresses query | All |
| Coherence | Logical flow | Long-form |
| Groundedness | Factual accuracy | RAG |
| Helpfulness | Utility to user | Assistants |
| Harmlessness | Safety check | All |

### Robotics-Specific Metrics

| Metric | Description | Use Case |
|--------|-------------|----------|
| Command Validity | Parseable to robot action | NLU |
| Safety Score | No dangerous commands | All |
| Confidence Calibration | Uncertainty estimation | Decision-making |
| Latency | Response time | Real-time |

## Best Practices

### Test Organization

```
prompts/
├── robot_commands/
│   ├── movement.yaml
│   ├── manipulation.yaml
│   └── navigation.yaml
├── safety/
│   ├── boundary_checks.yaml
│   └── adversarial.yaml
└── performance/
    └── latency_tests.yaml
```

### Evaluation Pipeline

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   Develop   │────>│   Evaluate  │────>│   Deploy    │
│   Prompts   │     │   (CI/CD)   │     │   (Gated)   │
└─────────────┘     └─────────────┘     └─────────────┘
       │                   │                   │
       v                   v                   v
  Local testing      Automated tests     Production
  (promptfoo)        (promptfoo +        monitoring
                      TruLens)           (TruLens)
```

### Guidelines

1. **Version prompts** - Track prompt changes in git
2. **Test edge cases** - Include adversarial and boundary tests
3. **Monitor in production** - Use TruLens for ongoing evaluation
4. **Set quality gates** - Block deployment on test failures
5. **Use multiple models** - Compare performance across providers

## Related Skills

- [AI Assistants](../ai-assistants/SKILL.md) - AI tool usage
- [DevOps](../devops/SKILL.md) - CI/CD integration
- [ROS2 Development](../ros2-development/SKILL.md) - Robot integration
