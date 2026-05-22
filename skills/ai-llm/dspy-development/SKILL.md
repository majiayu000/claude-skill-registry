---
name: dspy-development
description: >-
  This skill should be used when the user asks to "build with DSPy", "create a DSPy module",
  "optimize prompts", "build a RAG system", "create an AI agent with DSPy", "use declarative LM programming",
  "build an LM pipeline", "optimize few-shot examples", "use teleprompters", "compile a DSPy program",
  "fine-tune prompts", "create a DSPy signature", or mentions any of: DSPy, dspy, import dspy,
  dspy.LM, dspy.configure, dspy.Predict, dspy.ChainOfThought, dspy.ReAct, dspy.Module, dspy.Signature,
  dspy.InputField, dspy.OutputField, dspy.Retrieve, dspy.TypedPredictor, dspy.ProgramOfThought,
  dspy.Refine, dspy.BestofN, dspy.asyncify, dspy.streamify, dspy.MIPROv2, BootstrapFewShot,
  BootstrapFinetune, MIPRO, COPRO, dspy.Evaluate, dspy.Example, dspy.Prediction,
  dspy.RLM, dspy.RLM(, recursive language model, RLM module, long context processing,
  programmatic context exploration, REPL-based reasoning, llm_query, context decomposition,
  dspy.CodeAct, dspy.GEPA, dspy.SIMBA, ArborGRPO, dspy.Reasoning, dspy.Image, dspy.Audio,
  ChatAdapter, JSONAdapter, XMLAdapter, BAMLAdapter, Module.batch, dspy.adapter,
  dspy.teleprompt, dspy.evaluate, prompt optimization, few-shot learning, language model pipeline,
  LM programming framework, Stanford NLP DSPy, declarative prompting, or
  automated prompt engineering. Also trigger when code contains `import dspy` or `from dspy`.
version: 3.0.0
title: "Dspy Development"
status: active
---

# DSPy: Declarative Language Model Programming

Framework for programming — not prompting — language models. Build modular AI systems with automatic prompt optimization, RL training, and reflective prompt evolution.

**GitHub**: 22,000+ stars | **By**: Stanford NLP | **Current**: DSPy 3.1+ (Feb 2026)

## Installation

```bash
pip install dspy                    # Stable release (3.1.3)
pip install dspy[all]               # All LM providers
pip install git+https://github.com/stanfordnlp/dspy.git  # Latest dev
```

**For RLM/ProgramOfThought/CodeAct** (sandboxed code execution):
```bash
# Install Deno runtime (required for WASM sandbox)
curl -fsSL https://deno.land/install.sh | sh
```

**Python**: 3.10+ required (3.9 dropped in 3.0)

## Quick Start

```python
import dspy

# Configure LM (unified API — works with any provider)
lm = dspy.LM("anthropic/claude-sonnet-4-5-20250929", max_tokens=1000)
dspy.configure(lm=lm)

# Define a signature (input -> output contract)
class QA(dspy.Signature):
    """Answer questions with short factual answers."""
    question = dspy.InputField()
    answer = dspy.OutputField(desc="often between 1 and 5 words")

# Create and use a module
qa = dspy.Predict(QA)
result = qa(question="What is the capital of France?")
print(result.answer)  # "Paris"
```

### Chain of Thought

```python
cot = dspy.ChainOfThought("question -> answer")
result = cot(question="If John has 5 apples and gives 2 to Mary, how many remain?")
print(result.rationale)  # Step-by-step reasoning
print(result.answer)     # "3"
```

### RLM — Recursive Language Model (3.1+)

Process documents far beyond context window limits via programmatic exploration:

```python
rlm = dspy.RLM("context, query -> answer", max_iterations=20)
result = rlm(
    context="...massive document (100k+ tokens)...",
    query="What was Q3 revenue?"
)
# LM writes Python code to peek/grep/partition the context
# Recursive sub-calls via llm_query() aggregate results
```

## Core Concepts

### 1. LM Configuration

```python
import dspy

# Unified constructor for ALL providers
lm = dspy.LM("openai/gpt-4o-mini", temperature=0.7, cache=True)
dspy.configure(lm=lm)

# Anthropic Claude
lm = dspy.LM("anthropic/claude-sonnet-4-5-20250929", max_tokens=2000)

# Local models (Ollama)
lm = dspy.LM("ollama_chat/llama3.1", api_base="http://localhost:11434")

# Multiple models with context manager (thread-safe in 3.x)
cheap = dspy.LM("openai/gpt-4o-mini")
strong = dspy.LM("anthropic/claude-sonnet-4-5-20250929")

dspy.configure(lm=cheap)  # Default (only first thread can call this)
with dspy.context(lm=strong):
    result = expensive_module(question=q)  # Uses strong model

# Adapters (3.0+) — control output formatting
dspy.configure(lm=lm, adapter=dspy.ChatAdapter())      # Default
dspy.configure(lm=lm, adapter=dspy.JSONAdapter())       # JSON output
dspy.configure(lm=lm, adapter=dspy.XMLAdapter())        # XML output

# Track token usage
dspy.configure(lm=lm, track_usage=True)
result = qa(question="...")
print(result.get_lm_usage())  # Token counts per provider
```

### 2. Signatures

Define task structure as input-output contracts:

```python
# Inline (quick prototyping)
qa = dspy.Predict("question -> answer")
summarizer = dspy.ChainOfThought("text -> summary")

# Class-based (production — type hints, descriptions)
class ExtractEntities(dspy.Signature):
    """Extract named entities from text."""
    text = dspy.InputField(desc="raw text to analyze")
    entities = dspy.OutputField(desc="comma-separated list of entities")

# Multi-modal signatures (3.0+)
class DescribeImage(dspy.Signature):
    """Describe an image."""
    image: dspy.Image = dspy.InputField()
    description = dspy.OutputField()
```

### 3. Modules

Composable building blocks (like PyTorch nn.Module):

| Module | Purpose | When to Use |
|--------|---------|-------------|
| `dspy.Predict` | Direct prediction | Simple tasks, speed critical |
| `dspy.ChainOfThought` | Step-by-step reasoning | Complex reasoning, math |
| `dspy.ProgramOfThought` | Code-based reasoning | Calculations, data transforms |
| `dspy.ReAct` | Tool-using agent | Multi-step research, API calls |
| `dspy.RLM` | Recursive context exploration | Long documents beyond context window (3.1+) |
| `dspy.CodeAct` | Code generation + tool execution | Dynamic tool use, self-learning (3.0+) |
| `dspy.TypedPredictor` | Pydantic structured output | Extraction, typed responses |
| `dspy.Refine` | Iterative self-refinement | Quality-critical outputs |
| `dspy.BestofN` | N-sample selection | High-stakes decisions |
| `dspy.MultiChainComparison` | Compare multiple chains | Ambiguous questions |

See `references/modules.md` for complete API and usage patterns for each module.

### 4. Optimizers

Automatically improve prompts using training data:

| Optimizer | Best For | Speed | Data Needed |
|-----------|----------|-------|-------------|
| `BootstrapFewShot` | General purpose first try | Fast | 10-50 examples |
| `dspy.MIPROv2` | Reliable joint optimization | Medium | 50-200 examples |
| `dspy.GEPA` | Reflective prompt evolution (3.0+) | Medium | 20-100 examples |
| `dspy.SIMBA` | Self-reflection with feedback (3.0+) | Medium | 20-100 examples |
| `ArborGRPO` | RL-based weight training (3.0+) | Slow | 100+ examples |
| `BootstrapFinetune` | Model fine-tuning | Slow | 100+ examples |
| `COPRO` | Prompt search | Medium | 20-100 examples |

```python
# MIPROv2 with auto mode (recommended starting point)
tp = dspy.MIPROv2(metric=my_metric, auto="medium", num_threads=8)
optimized = tp.compile(my_module, trainset=trainset)

# GEPA with reflective evolution (3.0+)
optimizer = dspy.GEPA(
    metric=metric_with_feedback, auto="light", num_threads=32,
    reflection_lm=dspy.LM("openai/gpt-4o", temperature=1.0, max_tokens=32000)
)
optimized = optimizer.compile(program, trainset=trainset, valset=valset)
```

See `references/optimizers.md` for complete optimizer guide with metrics and evaluation patterns.

### 5. Building Custom Modules

```python
class RAG(dspy.Module):
    def __init__(self, num_passages=3):
        super().__init__()
        self.retrieve = dspy.Retrieve(k=num_passages)
        self.generate = dspy.ChainOfThought("context, question -> answer")

    def forward(self, question):
        passages = self.retrieve(question).passages
        context = "\n".join(passages)
        return self.generate(context=context, question=question)
```

## Key Patterns

### Structured Output with Pydantic

```python
from pydantic import BaseModel, Field

class PersonInfo(BaseModel):
    name: str = Field(description="Full name")
    age: int = Field(description="Age in years")

class ExtractPerson(dspy.Signature):
    """Extract person information from text."""
    text = dspy.InputField()
    person: PersonInfo = dspy.OutputField()

extractor = dspy.TypedPredictor(ExtractPerson)
result = extractor(text="John Doe, 35, is a software engineer.")
print(result.person.name)  # "John Doe"
```

### Async and Streaming

```python
# Async wrapping
async_cot = dspy.asyncify(dspy.ChainOfThought("question -> answer"))
result = await async_cot(question="What is DSPy?")

# Streaming outputs
stream_predict = dspy.streamify(my_module)
for chunk in stream_predict(question="Explain quantum computing"):
    print(chunk, end="")
```

### Thread-Safe Batch Processing (3.0+)

```python
results = my_module.batch(
    inputs_list,
    num_threads=8,
    return_failed_examples=True,
    max_errors=5
)
```

### Save and Load (Stable in 3.0+)

```python
# Save program with full metadata (guaranteed 3.x compatibility)
optimized.save("models/qa_v2", save_program=True)

# Load
loaded = dspy.ChainOfThought("question -> answer")
loaded.load("models/qa_v2.json")
```

## Evaluation

```python
from dspy.evaluate import Evaluate

def exact_match(example, pred, trace=None):
    return example.answer.lower() == pred.answer.lower()

evaluator = Evaluate(devset=testset, metric=exact_match, num_threads=4)
score = evaluator(optimized_module)
print(f"Accuracy: {score}")
```

## Best Practices

1. **Start simple** — `dspy.Predict` first, add `ChainOfThought` only if accuracy matters
2. **Use descriptive signatures** — docstrings and field descriptions guide the LM
3. **Optimize with representative data** — cover edge cases in training examples
4. **Evaluate on held-out test set** — avoid overfitting to training data
5. **Use `dspy.MIPROv2(auto="light")`** as first optimizer — fast and effective
6. **Try GEPA for agentic tasks** — reflective evolution with custom feedback (3.0+)
7. **Track usage** — `dspy.configure(track_usage=True)` to monitor costs
8. **Cache during development** — enabled by default, saves API calls
9. **Use Module.batch** for throughput — thread-safe concurrent processing (3.0+)

## Additional Resources

### Reference Files

Detailed documentation for each area:
- **`references/modules.md`** — Complete module API: Predict, ChainOfThought, ReAct, RLM, CodeAct, Refine, BestofN, adapters, types, and composition patterns
- **`references/optimizers.md`** — All optimizers: MIPROv2, GEPA, SIMBA, ArborGRPO, BootstrapFewShot, Ensemble, metrics, evaluation, and optimization workflows
- **`references/examples.md`** — Production examples: RAG, agents, classifiers, RLM long-context, multi-modal, pipelines, async patterns, teacher-student distillation
- **`references/migration.md`** — Breaking changes from DSPy 1.x/2.0 to 2.6, and from 2.6 to 3.x
- **`README.md`** — High-level DSPy overview for quick familiarization

### External Resources

- **Docs**: https://dspy.ai
- **Learn Path**: https://dspy.ai/learn/ (3-stage: Programming, Evaluation, Optimization)
- **GitHub**: https://github.com/stanfordnlp/dspy
- **Discord**: https://discord.gg/XCGy2WDCQB
- **Papers**: "DSPy: Compiling Declarative Language Model Calls into Self-Improving Pipelines", "Recursive Language Models" (arXiv:2512.24601)
