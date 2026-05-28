---
name: system2-attention
description: System 2 attention mechanisms for deliberate, slow reasoning in transformer
version: 1.0.0
---


# System 2 Attention Skill: Deliberate Reasoning Validation

**Status**: ✅ Production Ready
**Trit**: -1 (MINUS - validator/constraint)
**Color**: #2626D8 (Blue)
**Principle**: Filter noise via deliberate re-attention
**Frame**: Two-stage attention with explicit reasoning

---

## Overview

**System 2 Attention** (S2A) validates and filters transformer attention by regenerating context deliberately. Standard attention (System 1) is fast but susceptible to sycophancy and irrelevant context. S2A re-attends after explicit reasoning.

1. **Context regeneration**: LLM rewrites context removing irrelevant info
2. **Two-pass attention**: Fast then deliberate
3. **Sycophancy reduction**: Filter opinion-seeking noise
4. **Factual grounding**: Anchor to verified facts

## Core Pattern

```
S2A(x, context):
  # System 1: fast pattern matching
  context_filtered = LLM("Extract only relevant facts from: {context}")
  
  # System 2: deliberate reasoning on clean context
  return LLM(x, context=context_filtered)
```

```python
def system2_attention(query: str, context: str, model) -> str:
    # Stage 1: Regenerate context (remove sycophantic/irrelevant)
    filter_prompt = f"""Given the context below, extract only the 
    objective facts relevant to answering questions. Remove opinions,
    leading questions, and irrelevant details.
    
    Context: {context}
    
    Relevant facts only:"""
    
    clean_context = model.generate(filter_prompt)
    
    # Stage 2: Answer with filtered context
    return model.generate(query, context=clean_context)
```

## Key Concepts

### 1. Context Filtering

```python
class S2AFilter:
    def __init__(self, model):
        self.model = model
    
    def filter_sycophancy(self, context: str) -> str:
        """Remove opinion-seeking and leading content."""
        return self.model.generate(
            f"Rewrite removing any opinions or leading questions:\n{context}"
        )
    
    def filter_irrelevant(self, context: str, query: str) -> str:
        """Keep only query-relevant facts."""
        return self.model.generate(
            f"Extract facts from context relevant to: {query}\n\n{context}"
        )
```

### 2. Two-Pass Architecture

```python
class System2AttentionLayer:
    def __init__(self, base_attention, filter_model):
        self.attn = base_attention
        self.filter = filter_model
    
    def forward(self, q, k, v, context_mask=None):
        # Pass 1: Standard attention (System 1)
        attn_weights = self.attn(q, k, v)
        
        # Identify high-entropy (uncertain) positions
        entropy = -torch.sum(attn_weights * torch.log(attn_weights + 1e-9), dim=-1)
        uncertain = entropy > self.threshold
        
        # Pass 2: Deliberate re-attention on uncertain positions
        if uncertain.any():
            filtered_kv = self.filter(k, v, uncertain)
            attn_weights[uncertain] = self.attn(q[uncertain], filtered_kv)
        
        return attn_weights
```

### 3. Factual Grounding Validator

```python
def validate_factual_grounding(response: str, facts: list[str]) -> float:
    """Score response grounding in verified facts."""
    claims = extract_claims(response)
    grounded = sum(1 for c in claims if any(entails(f, c) for f in facts))
    return grounded / len(claims) if claims else 1.0
```

## Commands

```bash
# Apply S2A filtering
just s2a-filter context.txt query.txt

# Measure sycophancy reduction
just s2a-sycophancy-test model responses/

# Validate factual grounding
just s2a-grounding response.txt facts.txt
```

## Integration with GF(3) Triads

```
system2-attention (-1) ⊗ causal-inference (0) ⊗ gflownet (+1) = 0 ✓  [Deliberate Search]
system2-attention (-1) ⊗ cognitive-superposition (0) ⊗ forward-forward-learning (+1) = 0 ✓  [Local Validation]
```

## Related Skills

- **causal-inference** (0): Coordinate causal reasoning
- **forward-forward-learning** (+1): Generate local learning signals
- **proofgeneral-narya** (-1): Formal verification baseline

---

**Skill Name**: system2-attention
**Type**: Deliberate Reasoning Validator
**Trit**: -1 (MINUS)
**Color**: #2626D8 (Blue)



## Scientific Skill Interleaving

This skill connects to the K-Dense-AI/claude-scientific-skills ecosystem:

### Graph Theory
- **networkx** [○] via bicomodule
  - Universal graph hub

### Bibliography References

- `general`: 734 citations in bib.duckdb

## Cat# Integration

This skill maps to **Cat# = Comod(P)** as a bicomodule in the equipment structure:

```
Trit: 0 (ERGODIC)
Home: Prof
Poly Op: ⊗
Kan Role: Adj
Color: #26D826
```

### GF(3) Naturality

The skill participates in triads satisfying:
```
(-1) + (0) + (+1) ≡ 0 (mod 3)
```

This ensures compositional coherence in the Cat# equipment structure.