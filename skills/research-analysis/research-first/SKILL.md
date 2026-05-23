---
name: research-first
description: This skill should be used when the user asks about frameworks (React, Next.js, FastAPI, PydanticAI, Supabase, LiveKit, LlamaIndex, Tailwind, Zustand, etc.), when implementing new features, when expressing uncertainty ("how do I", "what's the best way", "should I", "is this right"), when designing solutions or architecture, or before committing to any implementation approach. Spawns a research sub-agent to query context7 (framework docs) and Perplexity (solution validation) in a separate context window, returning concise findings to keep the main context clean.
version: 1.0.0
title: "Research First"
status: active
---

# Research-First Skill

Spawn a research sub-agent before implementation to ensure current best practices and validated approaches.

## Why This Skill Exists

LLM knowledge has a cutoff date. Frameworks evolve rapidly. What was best practice 6 months ago may be deprecated today. This skill ensures:

1. **Current documentation** via context7 (real-time framework docs)
2. **Validated approaches** via Perplexity (cross-referenced solutions)
3. **Clean main context** by running research in a separate context window

## When to Use

### Automatic Triggers

Invoke this skill when encountering:

| Trigger Type | Examples |
|--------------|----------|
| Framework mentions | React, Next.js, FastAPI, PydanticAI, Supabase, LiveKit, LlamaIndex, Tailwind, Zustand, Playwright, etc. |
| Uncertainty phrases | "how do I", "what's the best way", "should I", "is this the right approach" |
| Implementation start | "implement", "build", "create", "add feature" + any technology |
| Solution design | Architecture decisions, choosing between approaches |
| API usage | Using any library API not used in current session |
| Version concerns | Deprecation warnings, version mismatches, "latest" patterns |

### Proactive Use

Even without explicit triggers, invoke before:

- Writing more than 20 lines of framework-specific code
- Making architectural decisions
- Fixing bugs with unclear root causes
- Implementing patterns for the first time

## How to Use

### Step 1: Identify the Research Query

Formulate what needs to be researched:

- **Framework question**: "What's the current pattern for X in [framework]?"
- **Solution validation**: "Is [approach] the right way to solve [problem]?"
- **Best practices**: "What are current best practices for [domain]?"

### Step 2: Spawn Research Sub-Agent

Use the Task tool to spawn a Haiku sub-agent (fast and cheap):

```python
Task(
    subagent_type="general-purpose",
    model="haiku",
    description="Research [topic] for implementation",
    prompt="""
    Research Query: [specific question]

    Context: [brief context about what we're building]

    Instructions:
    1. Use mcp__context7__resolve-library-id to find the framework
    2. Use mcp__context7__query-docs to get current documentation
    3. Use mcp__perplexity__perplexity_ask to validate the approach
    4. If comparing approaches/frameworks, use mcp__perplexity__perplexity_reason
       to analyze tradeoffs with structured reasoning

    Return Format:
    ## Current Best Practice
    [What the docs say]

    ## Code Example
    ```[language]
    [working example from docs]
    ```

    ## Gotchas
    [Common mistakes, deprecations, version notes]

    ## Validation
    [What Perplexity confirms or contradicts]
    """
)
```

### Step 3: Apply Findings

After receiving the research summary:

1. Review the current best practice
2. Check for gotchas that apply to our situation
3. Use the validated code patterns
4. Proceed with implementation

## Research Patterns

### Pattern 1: Framework Documentation Lookup

For questions about how to use a framework feature:

```python
Task(
    subagent_type="general-purpose",
    model="haiku",
    description="Research [framework] [feature]",
    prompt="""
    Query: How to [specific feature] in [framework]?

    Steps:
    1. context7: resolve-library-id for "[framework]"
    2. context7: query-docs with "[feature] [specific question]"

    Return: Current pattern, code example, version notes
    """
)
```

### Pattern 2: Solution Design Validation

For validating an approach before committing:

```python
Task(
    subagent_type="general-purpose",
    model="haiku",
    description="Validate [solution] approach",
    prompt="""
    I'm considering this approach: [description]

    Context: [what we're solving]

    Use Perplexity to answer:
    1. Is this approach sound for [use case]?
    2. What alternatives should I consider?
    3. What are the trade-offs?
    4. Any gotchas or edge cases?

    Return: Recommendation with reasoning
    """
)
```

### Pattern 3: Solution Design Validation with Reasoning

For validating approaches that involve comparing multiple frameworks or architectures:

```python
Task(
    subagent_type="general-purpose",
    model="haiku",
    description="Validate and compare [approaches]",
    prompt="""
    I'm choosing between: [approach A] vs [approach B]

    Context: [what we're solving]

    Steps:
    1. Use mcp__perplexity__perplexity_ask for quick validation of each approach
    2. Use mcp__perplexity__perplexity_reason to analyze tradeoffs:
       "Given these approaches: [A] vs [B], analyze the tradeoffs
       considering performance, maintainability, and current ecosystem support"

    Return: Recommended approach with structured reasoning
    """
)
```

### Pattern 4: Deep Research

For comprehensive investigations (new domain, major architecture decisions):

```python
Task(
    subagent_type="general-purpose",
    model="haiku",
    description="Deep research on [topic]",
    prompt="""
    Goal: Comprehensive investigation of [topic]

    Use mcp__perplexity__perplexity_research for an exhaustive multi-step
    investigation. This tool takes 1-5 minutes but returns thorough results.

    Query: "[detailed research question about the topic]"

    After receiving results, summarize:
    - Key findings and recommendations
    - Risks and considerations
    - Recommended next steps
    """
)
```

### Pattern 5: Combined Research

For new implementations needing both docs and validation:

```python
Task(
    subagent_type="general-purpose",
    model="haiku",
    description="Research [feature] implementation",
    prompt="""
    Goal: Implement [feature] using [framework]

    Research Steps:
    1. context7: Get current [framework] docs for [feature]
    2. Perplexity: Validate the approach for [our specific context]

    Return:
    - Current recommended pattern (from docs)
    - Working code example
    - Our-context-specific considerations
    - Potential issues to watch for
    """
)
```

## Context Efficiency

This skill saves context by:

| Without Skill | With Skill |
|---------------|------------|
| Research pollutes main context | Research runs in separate context |
| Full docs loaded into main window | Only summary returned |
| Multiple back-and-forth queries | Single sub-agent handles all |
| ~10-20k tokens for research | ~500-1000 tokens for summary |

## Integration with Reflective Solution Design

This skill implements the research phase of the Reflective Solution Design pattern from CLAUDE.md:

```
1. RECALL    → "What do I know about this problem?"
2. REFLECT   → "What approach might work?"
3. RESEARCH  → [THIS SKILL] Query context7 + Perplexity
4. IMPLEMENT → Execute the validated approach
5. RETAIN    → Store the outcome for future synthesis
```

## Common Frameworks Reference

See `references/frameworks.md` for the full list of frameworks that should trigger this skill.

Quick reference of most common:

| Category | Frameworks |
|----------|------------|
| Frontend | React, Next.js, Tailwind, Zustand, @assistant-ui |
| Backend | FastAPI, PydanticAI, LlamaIndex, pydantic-graph |
| Database | Supabase, PostgreSQL, Redis, FAISS |
| Voice/RT | LiveKit, WebRTC, Twilio |
| Testing | Pytest, Jest, Playwright |
| Infra | Docker, Vercel, Railway |

## Examples

See `examples/` for complete research query examples:

- `examples/react-hook-research.md` - Researching React patterns
- `examples/fastapi-validation.md` - Validating API design
- `examples/architecture-decision.md` - Making architecture choices

## Best Practices

### Do

- Research BEFORE writing code, not after hitting errors
- Include context about what you're building in the query
- Ask specific questions, not vague ones
- Use Haiku for cost efficiency (research doesn't need Opus)

### Don't

- Skip research for "simple" things (they often aren't)
- Copy code without understanding the gotchas
- Ignore version-specific notes
- Research the same thing multiple times (store findings in Hindsight)

## After Research: Store Learnings

After successful implementation, retain the pattern in Hindsight:

```python
mcp__hindsight__retain(
    content="Pattern for [X] in [framework]: [summary]. Gotcha: [important note]",
    context="patterns"
)
```

This prevents re-researching the same patterns and builds project-specific knowledge.
