---
name: llm-safety-patterns
description: Security patterns for LLM integrations including prompt injection defense and hallucination prevention. Use when implementing context separation, validating LLM outputs, or protecting against prompt injection attacks.
context: fork
agent: security-auditor
version: 1.0.0
author: SkillForge
user-invocable: false
---

# LLM Safety Patterns

## Overview

Defensive patterns to protect LLM integrations against prompt injection, hallucination, and data leakage through layered validation and output filtering.

## When to Use

- Securing LLM-powered features in production
- Implementing context separation for multi-tenant AI
- Validating and filtering LLM outputs
- Protecting against prompt injection attacks

## The Core Principle

> **Identifiers flow AROUND the LLM, not THROUGH it.**
> **The LLM sees only content. Attribution happens deterministically.**

## Why This Matters

When identifiers appear in prompts, bad things happen:

1. **Hallucination:** LLM invents IDs that don't exist
2. **Confusion:** LLM mixes up which ID belongs where
3. **Injection:** Attacker manipulates IDs via prompt injection
4. **Leakage:** IDs appear in logs, caches, traces
5. **Cross-tenant:** LLM could reference other users' data

## The Architecture

```
┌─────────────────────────────────────────────────────────────────────────┐
│                                                                         │
│   SYSTEM CONTEXT (flows around LLM)                                     │
│   ┌─────────────────────────────────────────────────────────────────┐   │
│   │ user_id │ tenant_id │ analysis_id │ trace_id │ permissions     │   │
│   └─────────────────────────────────────────────────────────────────┘   │
│        │                                                       │        │
│        │                                                       │        │
│        ▼                                                       ▼        │
│   ┌─────────┐                                           ┌─────────┐    │
│   │ PRE-LLM │       ┌─────────────────────┐            │POST-LLM │    │
│   │ FILTER  │──────▶│        LLM          │───────────▶│ATTRIBUTE│    │
│   │         │       │                     │            │         │    │
│   │ Returns │       │ Sees ONLY:          │            │ Adds:   │    │
│   │ CONTENT │       │ - content text      │            │ - IDs   │    │
│   │ (no IDs)│       │ - context text      │            │ - refs  │    │
│   └─────────┘       │ (NO IDs!)           │            └─────────┘    │
│                     └─────────────────────┘                            │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

## What NEVER Goes in Prompts

### SkillForge Forbidden Parameters

| Parameter | Type | Why Forbidden |
|-----------|------|---------------|
| `user_id` | UUID | Can be hallucinated, enables cross-user access |
| `tenant_id` | UUID | Critical for multi-tenant isolation |
| `analysis_id` | UUID | Job tracking, not for LLM |
| `document_id` | UUID | Source tracking, not for LLM |
| `artifact_id` | UUID | Output tracking, not for LLM |
| `chunk_id` | UUID | RAG reference, not for LLM |
| `session_id` | str | Auth context, not for LLM |
| `trace_id` | str | Observability, not for LLM |
| Any UUID | UUID | Pattern: `[0-9a-f]{8}-...` |

### Detection Pattern

```python
import re

FORBIDDEN_PATTERNS = [
    r'user[_-]?id',
    r'tenant[_-]?id',
    r'analysis[_-]?id',
    r'document[_-]?id',
    r'artifact[_-]?id',
    r'chunk[_-]?id',
    r'session[_-]?id',
    r'trace[_-]?id',
    r'[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}',
]

def audit_prompt(prompt: str) -> list[str]:
    """Check for forbidden patterns in prompt"""
    violations = []
    for pattern in FORBIDDEN_PATTERNS:
        if re.search(pattern, prompt, re.IGNORECASE):
            violations.append(pattern)
    return violations
```

## The Three-Phase Pattern

### Phase 1: Pre-LLM (Filter & Extract)

```python
async def prepare_for_llm(
    query: str,
    ctx: RequestContext,
) -> tuple[str, list[str], SourceRefs]:
    """
    Filter data and extract content for LLM.
    Returns: (content, context_texts, source_references)
    """
    # 1. Retrieve with tenant filter
    documents = await semantic_search(
        query_embedding=embed(query),
        ctx=ctx,  # Filters by tenant_id, user_id
    )

    # 2. Save references for attribution
    source_refs = SourceRefs(
        document_ids=[d.id for d in documents],
        chunk_ids=[c.id for c in chunks],
    )

    # 3. Extract content only (no IDs)
    content_texts = [d.content for d in documents]

    return query, content_texts, source_refs
```

### Phase 2: LLM Call (Content Only)

```python
def build_prompt(content: str, context_texts: list[str]) -> str:
    """
    Build prompt with ONLY content, no identifiers.
    """
    prompt = f"""
    Analyze the following content and provide insights.

    CONTENT:
    {content}

    RELEVANT CONTEXT:
    {chr(10).join(f"- {text}" for text in context_texts)}

    Provide analysis covering:
    1. Key concepts
    2. Prerequisites
    3. Learning objectives
    """

    # AUDIT: Verify no IDs leaked
    violations = audit_prompt(prompt)
    if violations:
        raise SecurityError(f"IDs leaked to prompt: {violations}")

    return prompt

async def call_llm(prompt: str) -> dict:
    """LLM only sees content, never IDs"""
    response = await llm.generate(prompt)
    return parse_response(response)
```

### Phase 3: Post-LLM (Attribute)

```python
async def save_with_attribution(
    llm_output: dict,
    ctx: RequestContext,
    source_refs: SourceRefs,
) -> Analysis:
    """
    Attach context and references to LLM output.
    Attribution is deterministic, not LLM-generated.
    """
    return await Analysis.create(
        # Generated
        id=uuid4(),

        # From RequestContext (system-provided)
        user_id=ctx.user_id,
        tenant_id=ctx.tenant_id,
        analysis_id=ctx.resource_id,
        trace_id=ctx.trace_id,

        # From Pre-LLM refs (deterministic)
        source_document_ids=source_refs.document_ids,
        source_chunk_ids=source_refs.chunk_ids,

        # From LLM (content only)
        content=llm_output["analysis"],
        key_concepts=llm_output["key_concepts"],
        difficulty=llm_output["difficulty"],

        # Metadata
        created_at=datetime.now(timezone.utc),
        model_used=MODEL_NAME,
    )
```

## Output Validation

After LLM returns, validate:

1. **Schema:** Response matches expected structure
2. **Guardrails:** No toxic/harmful content
3. **Grounding:** Claims are supported by provided context
4. **No IDs:** LLM didn't hallucinate any IDs

```python
async def validate_output(
    llm_output: dict,
    context_texts: list[str],
) -> ValidationResult:
    """Validate LLM output before use"""

    # 1. Schema validation
    try:
        parsed = AnalysisOutput.model_validate(llm_output)
    except ValidationError as e:
        return ValidationResult(valid=False, reason=f"Schema error: {e}")

    # 2. Guardrails
    if await contains_toxic_content(parsed.content):
        return ValidationResult(valid=False, reason="Toxic content detected")

    # 3. Grounding check
    if not is_grounded(parsed.content, context_texts):
        return ValidationResult(valid=False, reason="Ungrounded claims")

    # 4. No hallucinated IDs
    if contains_uuid_pattern(parsed.content):
        return ValidationResult(valid=False, reason="Hallucinated IDs")

    return ValidationResult(valid=True)
```

## Integration Points in SkillForge

### Content Analysis Workflow

```
backend/app/workflows/
├── agents/
│   ├── execution.py        # Add context separation
│   └── prompts/            # Audit all prompts
├── tasks/
│   └── generate_artifact.py  # Add attribution
```

### Services

```
backend/app/services/
├── embeddings/            # Pre-LLM filtering
└── analysis/              # Post-LLM attribution
```

## Checklist Before Any LLM Call

- [ ] RequestContext available
- [ ] Data filtered by tenant_id and user_id
- [ ] Content extracted without IDs
- [ ] Source references saved
- [ ] Prompt passes audit (no forbidden patterns)
- [ ] Output validated before use
- [ ] Attribution uses context, not LLM output

---

## Related Skills

- `input-validation` - Input sanitization patterns that complement LLM safety
- `rag-retrieval` - RAG pipeline patterns requiring tenant-scoped retrieval
- `llm-evaluation` - Output quality assessment including hallucination detection
- `security-scanning` - Automated security scanning for LLM integrations

## Key Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| ID handling | Flow around LLM, never through | Prevents hallucination, injection, and cross-tenant leakage |
| Output validation | Schema + guardrails + grounding | Defense-in-depth for LLM outputs |
| Attribution approach | Deterministic post-LLM | System context provides IDs, not LLM |
| Prompt auditing | Regex pattern matching | Fast detection of forbidden identifiers |

**Version:** 1.0.0 (December 2025)
## Capability Details

### context-separation
**Keywords:** context separation, prompt context, id in prompt, parameterized
**Solves:**
- How do I prevent IDs from leaking into prompts?
- How do I separate system context from prompt content?
- What should never appear in LLM prompts?

### pre-llm-filtering
**Keywords:** pre-llm, rag filter, data filter, tenant filter
**Solves:**
- How do I filter data before sending to LLM?
- How do I ensure tenant isolation in RAG?
- How do I scope retrieval to current user?

### post-llm-attribution
**Keywords:** attribution, source tracking, provenance, citation
**Solves:**
- How do I track which sources the LLM used?
- How do I attribute results correctly?
- How do I avoid LLM-generated IDs?

### output-guardrails
**Keywords:** guardrail, output validation, hallucination, toxicity
**Solves:**
- How do I validate LLM output?
- How do I detect hallucinations?
- How do I prevent toxic content generation?

### prompt-audit
**Keywords:** prompt audit, prompt security, prompt injection
**Solves:**
- How do I verify no IDs leaked to prompts?
- How do I audit prompts for security?
- How do I prevent prompt injection?