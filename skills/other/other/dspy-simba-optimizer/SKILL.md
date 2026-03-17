---
name: dspy-simba-optimizer
version: "1.0.0"
dspy-compatibility: "3.1.2"
description: This skill should be used when the user asks to "optimize with SIMBA", "use Bayesian optimization", "optimize agents with custom feedback", mentions "SIMBA optimizer", "mini-batch optimization", "statistical optimization", "lightweight optimizer", or needs an alternative to MIPROv2/GEPA for programs with rich feedback signals.
allowed-tools:
  - Read
  - Write
  - Glob
  - Grep
---

# DSPy SIMBA Optimizer

## Goal

Optimize DSPy programs using mini-batch Bayesian optimization with statistical analysis of feedback signals.

## When to Use

- Need lighter-weight alternative to GEPA
- Have custom feedback metrics (not just accuracy)
- Agentic tasks with rich failure signals
- Budget-conscious optimization (fewer eval calls)
- Programs where few-shot examples aren't critical

## Related Skills

- Alternative optimizers: [dspy-miprov2-optimizer](../dspy-miprov2-optimizer/SKILL.md), [dspy-gepa-reflective](../dspy-gepa-reflective/SKILL.md)
- Agent optimization: [dspy-react-agent-builder](../dspy-react-agent-builder/SKILL.md)
- Evaluation: [dspy-evaluation-suite](../dspy-evaluation-suite/SKILL.md)

## Inputs

| Input | Type | Description |
|-------|------|-------------|
| `program` | `dspy.Module` | Program to optimize |
| `trainset` | `list[dspy.Example]` | Training examples |
| `metric` | `callable` | Returns float or `dspy.Prediction(score=..., feedback=...)` |
| `max_steps` | `int` | Number of optimization steps |
| `bsize` | `int` | Mini-batch size |

## Outputs

| Output | Type | Description |
|--------|------|-------------|
| `optimized_program` | `dspy.Module` | SIMBA-optimized program |

## Workflow

### Phase 1: Understand SIMBA

**SIMBA** (Stochastic Introspective Mini-Batch Ascent):
- Iterative prompt optimization with mini-batch sampling
- Identifies challenging examples with high output variability
- Generates self-reflective rules or adds successful demonstrations
- Lighter than GEPA (no reflection LM)
- More flexible than Bootstrap (uses feedback)

**Comparison:**
- **MIPROv2**: Best accuracy, lots of data
- **GEPA**: Agentic systems, expensive
- **SIMBA**: Custom feedback, budget-friendly
- **Bootstrap**: Simplest, demo-based

### Phase 2: Basic SIMBA Optimization

```python
import dspy

dspy.configure(lm=dspy.LM("openai/gpt-4o-mini"))

# Program to optimize
class QAPipeline(dspy.Module):
    def __init__(self):
        self.generate = dspy.ChainOfThought("question -> answer")

    def forward(self, question):
        return self.generate(question=question)

# Metric (can return just score or (score, feedback))
def qa_metric(example, pred, trace=None):
    correct = example.answer.lower() in pred.answer.lower()
    return 1.0 if correct else 0.0

# SIMBA optimizer
optimizer = dspy.SIMBA(
    metric=qa_metric,
    max_steps=10,  # Optimization iterations
    bsize=5  # Mini-batch size
)

program = QAPipeline()
compiled = optimizer.compile(program, trainset=trainset)
compiled.save("qa_simba.json")
```

### Phase 3: SIMBA with Feedback Signals

SIMBA works best with rich feedback:

```python
import dspy

def detailed_metric(example, pred, trace=None):
    """Metric with feedback signal."""
    expected = example.answer.lower()
    actual = pred.answer.lower()

    if expected == actual:
        return dspy.Prediction(score=1.0, feedback="Perfect match")
    elif expected in actual:
        return dspy.Prediction(score=0.7, feedback=f"Contains answer but verbose: '{actual}'")
    else:
        overlap = len(set(expected.split()) & set(actual.split()))
        if overlap > 0:
            return dspy.Prediction(score=0.3, feedback=f"Partial overlap: {overlap} words")
        return dspy.Prediction(score=0.0, feedback=f"No match. Expected '{expected}'")

optimizer = dspy.SIMBA(
    metric=detailed_metric,
    max_steps=20,  # Optimization iterations
    bsize=8  # Mini-batch size
)

compiled = optimizer.compile(program, trainset=trainset)
```

### Phase 4: Production Agent Optimization

```python
import dspy
from dspy.evaluate import Evaluate
import logging

logger = logging.getLogger(__name__)

# Define tools as functions
def search(query: str) -> str:
    """Search knowledge base for relevant information."""
    retriever = dspy.ColBERTv2(url='http://20.102.90.50:2017/wiki17_abstracts')
    results = retriever(query, k=3)
    return "\n".join([r['text'] for r in results])

def calculate(expr: str) -> str:
    """Evaluate Python expressions safely."""
    try:
        with dspy.PythonInterpreter() as interp:
            return str(interp.execute(expr))
    except Exception as e:
        return f"Error: {e}"

class ResearchAgent(dspy.Module):
    def __init__(self):
        self.agent = dspy.ReAct(
            "question -> answer",
            tools=[search, calculate]
        )

    def forward(self, question):
        return self.agent(question=question)

def agent_metric(example, pred, trace=None):
    """Rich metric for agent optimization."""
    expected = example.answer.lower().strip()
    actual = pred.answer.lower().strip() if pred.answer else ""

    # Exact match
    if expected == actual:
        return dspy.Prediction(score=1.0, feedback="Correct answer")

    # Partial match
    if expected in actual:
        return dspy.Prediction(score=0.7, feedback="Answer contains expected result")

    # Check key terms
    expected_terms = set(expected.split())
    actual_terms = set(actual.split())
    overlap = len(expected_terms & actual_terms)

    if overlap >= len(expected_terms) * 0.5:
        return dspy.Prediction(score=0.5, feedback=f"50%+ term overlap")

    return dspy.Prediction(score=0.0, feedback=f"Incorrect: expected '{example.answer}'")

def optimize_agent(trainset, devset):
    """Full SIMBA optimization pipeline."""
    dspy.configure(lm=dspy.LM("openai/gpt-4o-mini"))

    agent = ResearchAgent()

    # Baseline evaluation
    eval_metric = lambda ex, pred, trace: agent_metric(ex, pred, trace).score
    evaluator = dspy.Evaluate(devset=devset, metric=eval_metric, num_threads=4)
    baseline = evaluator(agent)
    logger.info(f"Baseline: {baseline:.2%}")

    # SIMBA optimization
    optimizer = dspy.SIMBA(
        metric=agent_metric,
        max_steps=25,  # Optimization iterations
        bsize=6  # Mini-batch size
    )

    compiled = optimizer.compile(agent, trainset=trainset)

    # Evaluate optimized
    optimized = evaluator(compiled)
    logger.info(f"SIMBA optimized: {optimized:.2%}")

    compiled.save("research_agent_simba.json")
    return compiled
```

## Configuration

```python
optimizer = dspy.SIMBA(
    metric=metric_fn,
    max_steps=20,                          # Optimization iterations
    bsize=32,                              # Mini-batch size (default: 32)
    num_candidates=6,                      # Candidates per iteration (default: 6)
    max_demos=4,                           # Max demos per predictor (default: 4)
    temperature_for_sampling=0.2,          # Sampling temperature (default: 0.2)
    temperature_for_candidates=0.2         # Candidate selection temperature (default: 0.2)
)
```

## Best Practices

1. **Use feedback signals** - SIMBA benefits from `dspy.Prediction(score=..., feedback=...)` objects
2. **Balance parameters** - Adjust `bsize` (default 32) and `max_steps` (default 8) based on dataset size
3. **Patience** - SIMBA is slower than Bootstrap, faster than GEPA
4. **Custom metrics** - Best for scenarios with nuanced scoring (not binary)
5. **Tune temperatures** - Lower temperatures (0.1-0.3) for exploitation, higher (0.5-1.0) for exploration

## Limitations

- Newer optimizer, less battle-tested than MIPROv2
- Requires thoughtful metric design (garbage in, garbage out)
- Not as thorough as GEPA for agent optimization
- Mini-batch sampling adds variance to results
- No automatic prompt reflection like GEPA

## Official Documentation

- **DSPy Documentation**: https://dspy.ai/
- **DSPy GitHub**: https://github.com/stanfordnlp/dspy
- **SIMBA Optimizer**: https://dspy.ai/api/optimizers/SIMBA/
- **Optimizers Guide**: https://dspy.ai/learn/optimization/optimizers/
