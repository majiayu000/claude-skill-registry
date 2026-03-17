---
name: ai-era-architecture-principles
description: "Framework adoption decision matrix: custom vs large frameworks in the Claude Code era. Use when evaluating whether to adopt a large framework or build custom with AI."
license: MIT
metadata:
  author: shimo4228
  version: "1.0"
  extracted: "2026-02-09"
---

# AI Era Architecture Principles

**Extracted:** 2026-02-09
**Context:** When deciding whether to use large frameworks (LangChain, LiteLLM, etc.) vs custom implementation in the Claude Code era

## Problem

Traditional software development wisdom says "Don't Reinvent the Wheel" — use existing libraries and frameworks to save development time. But in the AI-driven development era with Claude Code, is this still the best approach?

**Key Questions:**
- Should I use LangChain for LLM applications?
- Should I use a large framework with 50+ dependencies?
- When is custom implementation better than a comprehensive library?

## Solution: The Three Principles

### 1. Micro-Dependencies Principle

**Avoid large frameworks when Claude Code can implement needed features in hours.**

```
Traditional Development:
  Custom implementation: weeks → months ⏰
  Use existing framework: days → weeks ✅

Claude Code Era:
  Custom implementation: hours → 1 day ✅
  Use existing framework: still brings 50+ dependencies ❌
```

**Example (pdf2anki project):**
- ❌ **With LangChain:** 50+ dependencies, black-box abstractions, breaking changes
- ✅ **Custom:** 6 dependencies (anthropic, pymupdf, pydantic, pyyaml, typer, rich)
- ✅ **Result:** 3,348 lines, full control, 96% test coverage, transparent

**Benefits:**
- Minimal dependencies → Easier maintenance
- No black-box abstractions → Full transparency
- No framework lock-in → Complete flexibility
- Faster startup/install → Better user experience

---

### 2. Perfect Fit Principle

**Generic abstractions → Domain-specific design**

Large frameworks provide generic solutions that work for many use cases. But your project has specific requirements. With Claude Code, you can implement exactly what you need.

**Example (pdf2anki project):**
```python
# Project-specific requirements:
@dataclass(frozen=True)  # ← Immutability requirement
class Section:
    # Structure-aware chunking for long documents
    heading_stack: tuple[str, ...]
    # Per-section model routing (Haiku vs Sonnet)
    char_count: int

# Batch API with 50% discount (Claude-specific)
client.messages.batches.create(requests=[...])

# Prompt caching control (Claude-specific)
system=[{
    "type": "text",
    "text": SYSTEM_PROMPT,
    "cache_control": {"type": "ephemeral"}  # ← Direct control
}]
```

These features are perfectly tailored to the project's needs. A generic framework would either:
- Not support these features, or
- Support them through complex configuration/plugins

**Benefits:**
- Code matches domain model exactly
- No unused features → Simpler codebase
- Direct control over critical features

---

### 3. Full Control Principle

**Complete control over API calls, cost tracking, error handling**

With direct SDK usage, you understand every line of code. With frameworks, behavior is hidden behind abstractions.

**Example:**
```python
# ✅ Direct SDK: Crystal clear what happens
client = anthropic.Anthropic()
response = client.messages.create(
    model=model,
    max_tokens=max_tokens,
    system=[...],  # Explicit prompt caching
    messages=[...]
)
cost = (response.usage.input_tokens / 1_000_000) * PRICE_PER_1M

# ❌ Framework: What's happening internally?
llm = ChatAnthropic(model=model)
chain = prompt | llm | parser
result = chain.invoke({"text": text})  # Caching enabled? Cost?
```

**Benefits:**
- Debugging is easy → No abstraction layers to dig through
- Testing is simple → Mock at SDK level
- Performance optimization → Profile exact bottlenecks
- Cost control → Track every token

---

## The New Mantra

### Traditional Era
> **"Don't Reinvent the Wheel"**

### AI Era (with Claude Code)
> **"Don't Import the Warehouse for a Single Wheel"**

**Why?**
- Claude Code can build the exact wheel you need in hours
- Importing the warehouse (large framework) brings:
  - 50+ dependencies you don't need
  - Features you'll never use
  - Complexity you don't want
  - Breaking changes you must handle

---

## When to Use Large Frameworks

Large frameworks ARE valuable when:

1. **You need 80%+ of the framework's features**
   - Example: Django for full-stack web apps (ORM, auth, admin, forms, templates)

2. **The framework provides critical infrastructure you can't easily replicate**
   - Example: React for complex UI state management

3. **You're prototyping and speed > control**
   - Example: Using LangChain to quickly test different LLM providers

4. **The framework has strong network effects**
   - Example: TensorFlow/PyTorch for ML (ecosystem, community, tools)

---

## When to Avoid Large Frameworks

Avoid large frameworks when:

1. **You need < 20% of the framework's features**
   - Example: Using LangChain just for API calls to Claude/OpenAI

2. **Your requirements are highly specific**
   - Example: Custom cost tracking, specific batching logic, domain-specific optimizations

3. **You value simplicity and control**
   - Example: CLI tools, libraries, utilities

4. **The framework is rapidly changing**
   - Example: Early-stage AI frameworks with frequent breaking changes

---

## Decision Framework

```
┌─────────────────────────────────────────────┐
│ Do I need > 50% of the framework features?  │
└─────────────┬───────────────────────────────┘
              │
         No ──┴── Yes
         │        │
         │        └─→ Use Framework
         │
         ▼
┌─────────────────────────────────────────────┐
│ Are my requirements highly specific?        │
└─────────────┬───────────────────────────────┘
              │
         No ──┴── Yes
         │        │
         │        └─→ Custom Implementation
         │
         ▼
┌─────────────────────────────────────────────┐
│ Can Claude Code implement it in < 1 day?    │
└─────────────┬───────────────────────────────┘
              │
         No ──┴── Yes
         │        │
         │        └─→ Custom Implementation
         │
         └─→ Consider Framework
```

---

## Real-World Example: pdf2anki

**Decision:** Add OpenAI API support alongside Claude API

**Option 1: Use LangChain**
- Dependencies: +10 packages (langchain, langchain-core, langchain-anthropic, langchain-openai, etc.)
- Code: ~200 lines (shorter)
- Control: Limited (cost tracking, batch API, caching = opaque)
- Maintenance: Must track LangChain updates

**Option 2: Custom Provider Abstraction**
- Dependencies: +1 package (openai SDK)
- Code: ~500 lines (longer, but all visible)
- Control: Complete (cost tracking, batch API, caching = explicit)
- Maintenance: Only SDK updates (Anthropic, OpenAI)

**Chosen:** Option 2 with **conditional dependencies** (even better!)

```toml
[project.optional-dependencies]
claude = ["anthropic>=0.40.0"]
openai = ["openai>=1.0.0"]
all = ["anthropic>=0.40.0", "openai>=1.0.0"]
```

Users install only what they need:
```bash
pip install pdf2anki[claude]   # Only Anthropic SDK
pip install pdf2anki[openai]   # Only OpenAI SDK
pip install pdf2anki[all]      # Both (for comparison)
```

**Result:**
- Micro-Dependencies ✅ (users choose)
- Perfect Fit ✅ (domain-specific features preserved)
- Full Control ✅ (transparent cost tracking, batch API)

---

## When to Use This Skill

**Trigger:** When you or the user are considering adding a large framework (especially for LLM applications).

**Questions to Ask:**
1. What percentage of the framework's features will we actually use?
2. Can Claude Code implement the needed features in < 1 day?
3. Are there project-specific requirements that need fine-grained control?
4. How important is dependency minimization for this project?

**Remember:** In the AI era, the cost of custom implementation has dropped dramatically. Factor this into your architecture decisions.

---

## Related Patterns

- `python-optional-dependencies.md` - Implementation pattern for multi-provider support
- `cost-aware-llm-pipeline.md` - Custom cost tracking implementation
- `long-document-llm-pipeline.md` - Domain-specific document processing
