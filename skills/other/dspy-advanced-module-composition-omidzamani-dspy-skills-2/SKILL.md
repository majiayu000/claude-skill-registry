---
name: dspy-advanced-module-composition
version: "1.0.0"
dspy-compatibility: "3.1.2"
description: This skill should be used when the user asks to "compose DSPy modules", "use Ensemble optimizer", "combine multiple programs", "use dspy.MultiChainComparison", mentions "ensemble voting", "module composition", "sequential pipelines", or needs to build complex multi-module DSPy programs with ensemble patterns or multi-chain comparison.
allowed-tools:
  - Read
  - Write
  - Glob
  - Grep
---

# DSPy Advanced Module Composition

## Goal

Compose complex DSPy programs using the Ensemble optimizer, MultiChainComparison for reasoning synthesis, and sequential module patterns.

## When to Use

- Need consensus from multiple approaches
- Comparing different reasoning strategies
- Building robust pipelines with fallbacks
- Complex multi-step workflows with branching
- Ensemble methods for improved accuracy

## Related Skills

- Design modules: [dspy-custom-module-design](../dspy-custom-module-design/SKILL.md)
- Define signatures: [dspy-signature-designer](../dspy-signature-designer/SKILL.md)
- Evaluate performance: [dspy-evaluation-suite](../dspy-evaluation-suite/SKILL.md)

## Inputs

| Input | Type | Description |
|-------|------|-------------|
| `modules` | `list[dspy.Module]` | Modules to compose |
| `composition_type` | `str` | "ensemble", "sequential", "comparison" |

## Outputs

| Output | Type | Description |
|--------|------|-------------|
| `composed_program` | `dspy.Module` | Composed multi-module program |

## Workflow

### Phase 1: Ensemble Voting

Combine multiple programs using the Ensemble optimizer:

```python
import dspy
from dspy.teleprompt import Ensemble

dspy.configure(lm=dspy.LM("openai/gpt-4o-mini"))

# Define a signature for the task
class BasicQA(dspy.Signature):
    """Answer questions with short factoid answers."""
    question = dspy.InputField()
    answer = dspy.OutputField()

# Create multiple program instances (should be optimized/compiled programs)
# For simple demonstration, we'll use different predictors
program1 = dspy.Predict(BasicQA)
program2 = dspy.ChainOfThought(BasicQA)
program3 = dspy.Predict(BasicQA)

# Ensemble is an optimizer that compiles programs together
ensemble = Ensemble(reduce_fn=dspy.majority)
ensembled_program = ensemble.compile([program1, program2, program3])

# Use the ensembled program
result = ensembled_program(question="What is 2 + 2?")
print(result.answer)  # Voted answer
```

### Phase 2: MultiChainComparison

Compare multiple reasoning attempts:

```python
import dspy

class BasicQA(dspy.Signature):
    """Answer questions with short factoid answers."""
    question = dspy.InputField()
    answer = dspy.OutputField(desc="often between 1 and 5 words")

class ComparisonPipeline(dspy.Module):
    def __init__(self):
        # Generate multiple reasoning attempts
        self.cot = dspy.ChainOfThought(BasicQA)

        # Compare M attempts and select best
        # Must pass a Signature class, not a string
        self.compare = dspy.MultiChainComparison(
            BasicQA,
            M=3,  # Number of attempts to compare
            temperature=0.7
        )

    def forward(self, question):
        # Generate multiple completions to compare
        # Each completion must have rationale/reasoning field
        completions = [
            self.cot(question=question)
            for _ in range(3)
        ]

        # MultiChainComparison synthesizes them into best answer
        # Pass completions as positional arg, not keyword arg
        return self.compare(completions, question=question)

# Usage
dspy.configure(lm=dspy.LM("openai/gpt-4o-mini"))
pipeline = ComparisonPipeline()
result = pipeline(question="Explain quantum computing")
print(f"Best answer: {result.answer}")
print(f"Rationale: {result.rationale}")
```

### Phase 3: Sequential Composition

Chain modules for multi-step workflows:

```python
import dspy

# Define signatures for each step
class QueryRewrite(dspy.Signature):
    """Rewrite a question for better retrieval."""
    question = dspy.InputField()
    refined_query: str = dspy.OutputField()

class GenerateAnswer(dspy.Signature):
    """Generate answer from context and question."""
    context = dspy.InputField()
    question = dspy.InputField()
    answer = dspy.OutputField()

class ValidateAnswer(dspy.Signature):
    """Validate answer quality."""
    answer = dspy.InputField()
    question = dspy.InputField()
    is_valid: bool = dspy.OutputField()
    confidence: float = dspy.OutputField()

class SequentialRAG(dspy.Module):
    """Multi-step RAG pipeline."""

    def __init__(self):
        # Step 1: Query rewriting
        self.rewrite = dspy.Predict(QueryRewrite)

        # Step 2: Retrieval
        self.retrieve = dspy.Retrieve(k=5)

        # Step 3: Answer generation
        self.generate = dspy.ChainOfThought(GenerateAnswer)

        # Step 4: Validation
        self.validate = dspy.Predict(ValidateAnswer)

    def forward(self, question):
        # Sequential execution
        refined = self.rewrite(question=question)
        passages = self.retrieve(refined.refined_query).passages

        answer_pred = self.generate(
            context=passages,
            question=question
        )

        validation = self.validate(
            answer=answer_pred.answer,
            question=question
        )

        return dspy.Prediction(
            answer=answer_pred.answer,
            is_valid=validation.is_valid,
            confidence=validation.confidence
        )

# Usage
dspy.configure(lm=dspy.LM("openai/gpt-4o-mini"))
rag = SequentialRAG()
result = rag(question="What causes lightning?")
print(f"Answer: {result.answer} (valid: {result.is_valid})")
```

### Phase 4: Fallback Strategies

Handle failures with fallback modules:

```python
import dspy
import logging

logger = logging.getLogger(__name__)

class BasicQA(dspy.Signature):
    """Answer questions with short factoid answers."""
    question = dspy.InputField()
    answer = dspy.OutputField()

class RobustQA(dspy.Module):
    """Fallback strategy for errors."""

    def __init__(self):
        self.primary = dspy.ChainOfThought(BasicQA)
        self.fallback = dspy.Predict(BasicQA)

    def forward(self, question):
        try:
            result = self.primary(question=question)
            if result.answer and len(result.answer) > 10:
                return result
        except Exception as e:
            logger.error(f"Primary failed: {e}")

        return self.fallback(question=question)
```

## Production Example

```python
import dspy
from dspy.teleprompt import BootstrapFewShot, Ensemble

class GenerateAnswer(dspy.Signature):
    """Generate answer from context and question."""
    context = dspy.InputField()
    question = dspy.InputField()
    answer = dspy.OutputField()

class MultiStrategyQA(dspy.Module):
    """Production QA with retrieval."""

    def __init__(self):
        self.retrieve = dspy.Retrieve(k=3)
        self.generate = dspy.ChainOfThought(GenerateAnswer)

    def forward(self, question: str):
        context = self.retrieve(question).passages
        return self.generate(context=context, question=question)

# Usage with optimization
dspy.configure(lm=dspy.LM("openai/gpt-4o-mini"))
qa = MultiStrategyQA()

# First, optimize the base program
optimizer = BootstrapFewShot(
    metric=lambda ex, pred, trace: ex.answer in pred.answer,
    max_bootstrapped_demos=3
)

compiled_qa = optimizer.compile(qa, trainset=trainset)

# Then create ensemble from multiple optimized programs
# (train with different seeds or optimizers to get diversity)
program1 = optimizer.compile(qa, trainset=trainset)
program2 = optimizer.compile(qa, trainset=trainset)
program3 = optimizer.compile(qa, trainset=trainset)

ensemble = Ensemble(reduce_fn=dspy.majority)
final_program = ensemble.compile([program1, program2, program3])
```

## Best Practices

1. **Test modules independently** - Validate each module before composition
2. **Handle failures gracefully** - Use try/except in parallel composition
3. **Balance cost vs accuracy** - Ensembles are expensive (N × cost)
4. **Optimize composed programs** - Use BootstrapFewShot or MIPROv2 on final composition
5. **Module reusability** - Design modules to work in multiple compositions

## Limitations

- Ensemble increases cost linearly with module count
- Voting strategies may not work for all output types
- Sequential composition amplifies latency
- Error propagation in chains can be hard to debug
- Parallel composition requires careful state management

## Official Documentation

- **DSPy Documentation**: https://dspy.ai/
- **DSPy GitHub**: https://github.com/stanfordnlp/dspy
- **Modules Guide**: https://dspy.ai/learn/programming/modules/
