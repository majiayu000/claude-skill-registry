---
name: cove
description: Apply Chain-of-Verification (CoVe) prompting to improve response accuracy through self-verification. Use for complex questions requiring fact-checking, technical accuracy, or multi-step reasoning.
---

# Chain-of-Verification (CoVe)

CoVe is a verification technique that improves response accuracy by making the model fact-check its own answers. Instead of accepting an initial response at face value, CoVe instructs the model to generate verification questions, answer them independently, and revise the original answer based on findings.

## When to Use This Skill

CoVe adds the most value in these scenarios:

**Precision-required questions:**
- Questions containing precision language ("exactly", "precisely", "specific")
- Complex factual questions (dates, statistics, specifications)

**Complex reasoning:**
- Multi-step reasoning chains (3+ logical dependencies)
- Technical claims about APIs, libraries, or version-specific behavior

**Fact-checking scenarios:**
- Historical facts, statistics, or quantitative data
- Technical specifications and API behavior

**High-stakes accuracy:**
- Security-critical code paths or analysis
- Code generation requiring accuracy verification
- Any response where correctness is critical

**Self-correction triggers:**
- When initial response contains hedging language ("I think", "probably", "might be")

> **Note:** These heuristics can be copied to your project's CLAUDE.md if you want Claude to auto-invoke CoVe for matching scenarios. By default, CoVe requires manual invocation to give you control over when to invest additional tokens/time for verification.

## Verification Modes

CoVe offers two verification modes to balance accuracy vs. cost:

### Standard Mode (`/cove`)

Uses prompt-based isolation within a single conversation turn.

- **Token cost:** ~3-5x base tokens
- **Isolation:** Best-effort (mental reset instructions)
- **Speed:** Faster, single context
- **Best for:** Quick fact-checking, cost-sensitive scenarios

See [cove-process.md](./cove-process.md) for the standard workflow.

### Isolated Mode (`/cove-isolated`)

Uses Claude Code's Task tool to spawn isolated sub-agents for true factored verification.

- **Token cost:** ~8-15x base tokens
- **Isolation:** True (sub-agents have zero context about initial answer)
- **Speed:** Parallel execution minimizes latency
- **Best for:** High-stakes accuracy, codebase verification

**Sub-agent customization flags:**
| Flag | Effect |
|------|--------|
| `--explore` | Use Explore agent for codebase verification |
| `--haiku` | Use haiku model for faster/cheaper verification |
| `--agent=<name>` | Use custom agent type |

See [cove-isolated.md](./cove-isolated.md) for the isolated workflow.

### Mode Selection Guide

| Use Case | Recommended Mode |
|----------|------------------|
| Quick fact-checking | `/cove` |
| High-stakes accuracy | `/cove-isolated` |
| Codebase verification | `/cove-isolated --explore` |
| Cost-sensitive verification | `/cove` or `/cove-isolated --haiku` |

## Process Overview

The CoVe workflow follows 4 steps:

1. **Initial Response** - Generate baseline answer
2. **Verification Questions** - Create 3-5 targeted questions to expose errors
3. **Independent Verification** - Answer questions without referencing the original
4. **Reconciliation** - Revise answer based on verification findings

See [cove-process.md](./cove-process.md) for the standard workflow, or [cove-isolated.md](./cove-isolated.md) for the isolated sub-agent workflow.

## Invocation

Use the `/cove` command followed by your question:

```
/cove What is the time complexity of Python's sorted() function?
```

Or invoke `/cove` after receiving a response to verify it.

For isolated verification with sub-agents:

```
/cove-isolated What is the time complexity of Python's sorted() function?
```

With flags:

```
/cove-isolated --explore How does the auth system work?
/cove-isolated --haiku What year was TCP standardized?
```

## Natural Language Invocation

Claude should recognize these phrases as requests to invoke the CoVe skill:

- "verify this using chain of verification"
- "use CoVe to answer"
- "fact-check your response"
- "double-check this with verification"
- "use self-verification for this"
- "apply chain of verification"
- "verify this answer"

For isolated mode:

- "use isolated verification"
- "verify with sub-agents"
- "use factored verification with isolation"

> **Important:** This is guidance for manual recognition only. Auto-trigger is NOT implemented by default per design goals. Users who want automatic CoVe invocation for certain scenarios can add the heuristics from "When to Use This Skill" to their project's CLAUDE.md.
