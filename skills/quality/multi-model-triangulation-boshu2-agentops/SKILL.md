---
name: multi-model-triangulation
user-invocable: false
skill_api_version: 1
hexagonal_role: supporting
metadata:
  tier: execution
description: >-
  Cross-validate decisions using multiple AI models (Codex, Gemini, Grok).
  Use when "get a second opinion", evaluating approaches, or high-stakes decisions.
practices:
- pragmatic-programmer
---
<!-- TOC: Core | Workflow | Quick Prompts | Synthesis | Model Strengths | Anti-Patterns | References -->

# Multi-Model Triangulation

> **Core Insight:** Different models have different blind spots. Consensus = confidence.

## How It Works

You can't directly call other models. Instead:
1. **I generate** copy-paste prompts for you
2. **You paste** into Codex/Gemini/Grok/etc
3. **You return** their responses to me
4. **I synthesize** into unified recommendation

```
Claude → generates prompt → You → paste to Model B → You → paste response back → Claude synthesizes
```

---

## Quick Start

Tell me what you want triangulated:

```
Triangulate: [topic]
Context: [relevant details]
Models to use: [Codex, Gemini, Grok, or "all available"]
```

I'll generate the prompt(s). You copy-paste and return results.

---

## Ready-to-Copy Prompts

### Idea Evaluation

```
# COPY TO [Model Name]:

Evaluate these ideas. Score 1-10 on Quality/Utility/Feasibility/Risk:

1. [IDEA 1]
2. [IDEA 2]
3. [IDEA 3]

For each: scores, one-sentence rationale, final ranking.
Be critical—don't just agree.
```

### Code Review

```
# COPY TO [Model Name]:

Review for bugs/security/improvements:

```[lang]
[CODE]
```

Categorize: Critical (must fix), Important (should fix), Suggestions.
Overall score: X/10. Be thorough.
```

### Architecture Decision

```
# COPY TO [Model Name]:

Choosing between:
A: [Option A]
B: [Option B]
C: [Option C]

Evaluate: complexity, maintainability, performance, scalability.
Recommend ONE with reasoning. Be opinionated.
```

More prompts: [PROMPTS.md](references/PROMPTS.md)

---

## Synthesis Template

After I receive responses from multiple models:

```markdown
## Triangulation: [Topic]

### Consensus (High Confidence)
- [Points ALL models agree on]

### Divergence (Investigate)
| Topic | Claude | Model B | Model C |
|-------|--------|---------|---------|
| [X]   | [view] | [view]  | [view]  |

### Unique Insights
- **Claude:** [unique point]
- **Model B:** [unique point]

### Recommendation
[Synthesized recommendation]

### Confidence: [High/Medium/Low]
```

---

## Model Strengths

| Model | Strengths | Best For |
|-------|-----------|----------|
| Claude | Nuance, safety, writing | Complex reasoning, docs |
| GPT/Codex | Code generation, breadth | Implementation details |
| Gemini | Multimodal, current data | Visual, recent events |
| Grok | Unconventional takes | Creative alternatives |

**Tip:** For security reviews, use ALL models. For routine code review, 2 is enough.

---

## When to Triangulate

| Decision Type | Triangulate? | Why |
|---------------|--------------|-----|
| High-stakes architecture | Yes | Hard to reverse |
| Security review | Yes | Blind spots are dangerous |
| Code review (routine) | Maybe | 1-2 models sufficient |
| Quick question | No | Overhead not worth it |
| Creative brainstorming | Yes | Different perspectives |

**Rule:** If hard to reverse or high-impact, triangulate.

---

## Anti-Patterns

| Don't | Do |
|-------|-----|
| Ask vague questions | Specific, structured prompts |
| Accept first answer | Get 2-3 perspectives |
| Ignore disagreements | Investigate WHY models differ |
| Weight all equally | Consider model strengths |
| Skip synthesis | Always produce unified view |

---

## Integration

### Script Helper

```bash
# Generate formatted prompt for ideas
./scripts/format-prompt.py idea "Idea 1" "Idea 2" "Idea 3"

# For code (reads from stdin)
cat code.py | ./scripts/format-prompt.py code

# For architecture
./scripts/format-prompt.py arch "Use Redis" "Use PostgreSQL"
```

### With Other Skills

| Combine with... | For... |
|-----------------|--------|
| ux-audit | Get multiple UX perspectives |
| multi-pass-bug-hunting | Cross-validate bug findings |
| idea-wizard | Score generated ideas |

---

## References

| Topic | File |
|-------|------|
| Full prompt library | [PROMPTS.md](references/PROMPTS.md) |
| Real examples | [EXAMPLES.md](references/EXAMPLES.md) |

## Scripts

| Script | Purpose |
|--------|---------|
| `scripts/format-prompt.py` | Generate copy-paste ready prompts |
