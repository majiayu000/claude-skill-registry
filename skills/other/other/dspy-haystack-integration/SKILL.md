---
name: dspy-haystack-integration
version: "1.0.0"
dspy-compatibility: "3.1.2"
description: This skill should be used when the user asks to "integrate DSPy with Haystack", "optimize Haystack prompts using DSPy", "use DSPy to improve Haystack pipeline", mentions "Haystack pipeline optimization", "combining DSPy and Haystack", "extract DSPy prompt for Haystack", or wants to use DSPy's optimization capabilities to automatically improve prompts in existing Haystack pipelines.
allowed-tools:
  - Read
  - Write
  - Glob
  - Grep
---

# DSPy + Haystack Integration

## Goal

Use DSPy's optimization capabilities to automatically improve prompts in Haystack pipelines.

## When to Use

- You have existing Haystack pipelines
- Manual prompt tuning is tedious
- Need data-driven prompt optimization
- Want to combine Haystack components with DSPy optimization

## Inputs

| Input | Type | Description |
|-------|------|-------------|
| `haystack_pipeline` | `Pipeline` | Existing Haystack pipeline |
| `trainset` | `list[dspy.Example]` | Training examples |
| `metric` | `callable` | Evaluation function |

## Outputs

| Output | Type | Description |
|--------|------|-------------|
| `optimized_prompt` | `str` | DSPy-optimized prompt |
| `optimized_pipeline` | `Pipeline` | Updated Haystack pipeline |

## Workflow

### Phase 1: Build Initial Haystack Pipeline

```python
from haystack import Pipeline
from haystack.components.generators import OpenAIGenerator
from haystack.components.builders import PromptBuilder
from haystack.components.retrievers.in_memory import InMemoryBM25Retriever
from haystack.document_stores.in_memory import InMemoryDocumentStore

# Setup document store
doc_store = InMemoryDocumentStore()
doc_store.write_documents(documents)

# Initial generic prompt
initial_prompt = """
Context: {{context}}
Question: {{question}}
Answer:
"""

# Build pipeline
pipeline = Pipeline()
pipeline.add_component("retriever", InMemoryBM25Retriever(document_store=doc_store))
pipeline.add_component("prompt_builder", PromptBuilder(template=initial_prompt))
pipeline.add_component("generator", OpenAIGenerator(model="gpt-4o-mini"))

pipeline.connect("retriever", "prompt_builder.context")
pipeline.connect("prompt_builder", "generator")
```

### Phase 2: Create DSPy RAG Module

```python
import dspy

class HaystackRAG(dspy.Module):
    """DSPy module wrapping Haystack retriever."""
    
    def __init__(self, retriever, k=3):
        super().__init__()
        self.retriever = retriever
        self.k = k
        self.generate = dspy.ChainOfThought("context, question -> answer")
    
    def forward(self, question):
        # Use Haystack retriever
        results = self.retriever.run(query=question, top_k=self.k)
        context = [doc.content for doc in results['documents']]
        
        # Use DSPy for generation
        pred = self.generate(context=context, question=question)
        return dspy.Prediction(context=context, answer=pred.answer)
```

### Phase 3: Define Custom Metric

```python
from haystack.components.evaluators import SASEvaluator

# Haystack semantic evaluator
sas_evaluator = SASEvaluator(model="sentence-transformers/all-MiniLM-L6-v2")

def mixed_metric(example, pred, trace=None):
    """Combine semantic accuracy with conciseness."""
    
    # Semantic similarity (Haystack SAS)
    sas_result = sas_evaluator.run(
        ground_truth_answers=[example.answer],
        predicted_answers=[pred.answer]
    )
    semantic_score = sas_result['score']
    
    # Conciseness penalty
    word_count = len(pred.answer.split())
    conciseness = 1.0 if word_count <= 20 else max(0, 1 - (word_count - 20) / 50)
    
    return 0.7 * semantic_score + 0.3 * conciseness
```

### Phase 4: Optimize with DSPy

```python
from dspy.teleprompt import BootstrapFewShot

lm = dspy.LM("openai/gpt-4o-mini")
dspy.configure(lm=lm)

# Create DSPy module with Haystack retriever
rag_module = HaystackRAG(retriever=pipeline.get_component("retriever"))

# Optimize
optimizer = BootstrapFewShot(
    metric=mixed_metric,
    max_bootstrapped_demos=4,
    max_labeled_demos=4
)

compiled = optimizer.compile(rag_module, trainset=trainset)
```

### Phase 5: Extract and Apply Optimized Prompt

After optimization, extract the optimized prompt and apply it to your Haystack pipeline.

See [Prompt Extraction Guide](references/prompt-extraction.md) for detailed steps on:
- Extracting prompts from compiled DSPy modules
- Mapping DSPy demos to Haystack templates
- Building optimized Haystack pipelines

## Production Example

For a complete production-ready implementation, see [HaystackDSPyOptimizer](examples/haystack-dspy-optimizer.py).

This class provides:
- Wrapper for Haystack retrievers in DSPy modules
- Automatic optimization with BootstrapFewShot
- Prompt extraction and Haystack pipeline rebuilding
- Complete usage example with document store setup

## Best Practices

1. **Match retrievers** - Use same retriever in DSPy module as Haystack pipeline
2. **Custom metrics** - Combine Haystack evaluators with DSPy optimization
3. **Prompt extraction** - Carefully map DSPy demos to Haystack template format
4. **Test both** - Validate DSPy module AND final Haystack pipeline

## Limitations

- Prompt template conversion can be tricky
- Some Haystack features don't map directly to DSPy
- Requires maintaining two codebases initially
- Complex pipelines may need custom integration

## Official Documentation

- **DSPy Documentation**: https://dspy.ai/
- **DSPy GitHub**: https://github.com/stanfordnlp/dspy
- **Haystack Documentation**: https://docs.haystack.deepset.ai/
