---
name: leindex-code
description: Token-efficient code analysis via 5-layer stack (AST, Call Graph, CFG, DFG, PDG). 82% savings (balanced mode) with semantic completeness.
allowed-tools: [Bash]
keywords: [debug, refactor, understand, complexity, "call graph", "data flow", "what calls", "how complex", search, explore, analyze, dead code, architecture, imports]
---

# LeIndex-Code: Complete Reference

Token-efficient code analysis with **82% token savings** (balanced mode) while preserving semantic completeness for LLM usage.

## Quick Reference

| Task | Command |
|------|---------|
| Context extraction | `from maestro.leindex import ContextExtractor` |
| Semantic search | `from maestro.leindex import semantic_search` |
| AST analysis | `from maestro.leindex import ASTAnalyzer` |
| Call graph | `from maestro.leindex import CallGraphAnalyzer` |

---

## Modes

### Balanced Mode (Default) - 82% savings, LLM Actionable

**Use for:** Code generation, refactoring, implementation

```python
from maestro.leindex import ContextExtractor

extractor = ContextExtractor(mode='balanced')  # Default
result = extractor.extract_for_file('src/api.py')

print(f"Savings: {result.savings_percent:.1f}%")
print(result.context.to_llm_string())

# Output includes:
# L119: analyze_file(file_path: str, include_call...) -> ContextExtractionResult
# L136: semantic_search(query: str, project_path..., limit: int)
```

### Ultra Mode - 98% savings, Exploration Only

**Use for:** Code exploration, search, impact analysis

```python
extractor = ContextExtractor(mode='ultra')
result = extractor.extract_for_file('src/api.py')

# Output:
# fn:analyze_file build_semantic_index get_token_savings
# (No signatures, NOT actionable for code generation)
```

---

## Token Efficiency Comparison

| Mode | Savings | Semantic Quality | LLM Actionable | Use Case |
|------|---------|------------------|----------------|----------|
| Raw | 0% | Complete | ✓ Yes | Full file |
| **Balanced** | **82%** | **High** | **✓ Yes** | **Code generation** |
| Ultra | 98% | Low | ❌ No | Exploration only |

**Key Insight:** Balanced mode at 82% savings is the OPTIMAL balance for LLM-assisted coding. Ultra mode sacrifices too much semantic information (no signatures, no line numbers, no types) for LLM to accurately use the code.

---

## Python API

```python
from maestro.leindex import (
    # 5-layer analyzers
    ASTAnalyzer,
    CallGraphAnalyzer,
    CFGAnalyzer,
    DFGAnalyzer,
    SlicingAnalyzer,

    # Context extraction
    ContextExtractor,
    get_relevant_context,
    get_context_for_prompt,

    # Semantic search
    SemanticIndex,
    semantic_search,
    build_semantic_index,

    # Memory integration
    LeIndexMemoryBridge,
    get_leindex_memory_bridge,
)

# Example: Get token-efficient context (balanced mode)
extractor = ContextExtractor(mode='balanced')
result = extractor.extract_for_file('maestro/leindex/__init__.py')

print(f"Savings: {result.savings_percent:.1f}%")
print(f"Quality: {result.get_quality_report()}")

# Example: Semantic search
results = semantic_search("authentication functions", "/path/to/project")
for entity, score in results:
    print(f"{entity.name} in {entity.file} (score: {score:.2f})")
```
