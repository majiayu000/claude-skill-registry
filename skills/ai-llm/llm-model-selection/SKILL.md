---
name: "LLM Model Selection Skill"
description: "Choosing the right model for the task — power vs. cost vs. speed."
applyTo: "**/*model*,**/*llm*,**/*copilot*,**/*claude*,**/*gpt*"
---

# LLM Model Selection Skill

> Choosing the right model for the task — power vs. cost vs. speed.

## ⚠️ Staleness Warning

This skill depends on rapidly evolving technology. Model capabilities, pricing, and availability change frequently.

**Refresh triggers:**

- New model announcements (Claude, GPT, Gemini, etc.)
- Significant pricing changes
- Context window expansions
- New capability tiers

**Last validated:** February 2026 (Claude 4.6 generation)

**Check current state:** [Anthropic Models](https://platform.claude.com/docs/en/docs/about-claude/models), [OpenAI Models](https://platform.openai.com/docs/models)

---

## The Core Question

> Is Claude Opus 4.6 overkill?

**Sometimes yes, sometimes no.** Match the model to the task.

## Claude 4 Model Family (Current)

| Model | API ID | Best For | Input/Output (MTok) | Context | Max Output |
| ----- | ------ | -------- | ------------------- | ------- | ---------- |
| **Opus 4.6** | `claude-opus-4-6` | Building agents, most intelligent | $5 / $25 | 200K (1M beta) | 128K |
| **Sonnet 4.6** | `claude-sonnet-4-6` | Best speed + intelligence balance | $3 / $15 | 200K (1M beta) | 64K |
| **Haiku 4.5** | `claude-haiku-4-5-20251001` | Near-frontier intelligence, fastest | $1 / $5 | 200K | 64K |

**All Claude 4 models support:**
- Extended thinking
- Vision (images)
- Tool use
- Priority Tier access

**Opus 4.6 and Sonnet 4.6 additionally support:**
- Adaptive thinking (dynamic reasoning depth)
- 1M token context window (beta, via `context-1m-2025-08-07` header — long context pricing applies beyond 200K)

**AWS Bedrock IDs:** `anthropic.claude-opus-4-6-v1`, `anthropic.claude-sonnet-4-6`
**GCP Vertex AI IDs:** `claude-opus-4-6`, `claude-sonnet-4-6`

## Model Tiers

| Tier | Models | Best For | Relative Cost |
| ---- | ------ | -------- | ------------- |
| **Frontier** | Claude Opus 4.6, GPT-5, Gemini 2.5 Ultra | Complex reasoning, architecture, novel problems | $$$$$ |
| **Capable** | Claude Sonnet 4.6, GPT-4.1, Gemini 2.5 Pro | Most coding tasks, refactoring, debugging | $$$ |
| **Fast** | Claude Haiku 4.5, GPT-4.1-mini, Gemini 2.5 Flash | Simple edits, formatting, boilerplate | $ |

## When Opus 4.6 IS Worth It

- ✅ **Architecture decisions** — Multi-file refactoring, system design
- ✅ **Novel problem-solving** — No clear pattern to follow
- ✅ **Complex reasoning chains** — Many dependencies, edge cases
- ✅ **Long context understanding** — Large codebases, documentation
- ✅ **Nuanced judgment** — Taste, style, UX decisions
- ✅ **Learning sessions** — Bootstrap learning, skill development
- ✅ **Meditation/self-actualization** — Meta-cognitive operations
- ✅ **Extended thinking tasks** — Deep analysis requiring internal reasoning

## When Opus 4.6 IS Overkill

- ❌ **Simple file edits** — Renaming, adding imports
- ❌ **Boilerplate generation** — CRUD, scaffolding
- ❌ **Format conversion** — JSON ↔ YAML, etc.
- ❌ **Syntax fixes** — Lint errors, typos
- ❌ **Documentation updates** — README badges, version bumps

## How LLM Choice Affects Alex

| Capability | Frontier (Opus 4.6) | Capable (Sonnet 4.6) | Fast (Haiku 4.5) |
| ---------- | ------------------- | -------------------- | ---------------- |
| Complex refactoring | Excellent | Excellent | Good |
| Context retention | 200K / 1M (beta) | 200K / 1M (beta) | 200K tokens |
| Extended thinking | Full depth | Supported | Supported |
| Adaptive thinking | Yes | Yes | No |
| Max output tokens | 128K | 64K | 64K |
| Nuanced judgment | Excellent | Good | Basic |
| Speed | Moderate | Fast | Fastest |
| Cost per session | $2-5 | $0.50-2 | $0.05-0.30 |
| Multi-step planning | Excellent | Excellent | Good |
| Error recovery | Self-corrects | Self-corrects | Needs guidance |

## Alex's Cognitive Power by Model

```text
Opus 4.6:     [████████████████████] Full cognitive architecture + deep thinking
Sonnet 4.6:   [██████████████████░░] Most capabilities, excellent for coding
Haiku 4.5:    [██████████████░░░░░░] Solid baseline, fast responses
```

**With Opus 4.6**, Alex can:

- Maintain 7±2 working memory rules across long sessions
- Execute complex meditation protocols with extended thinking
- Perform genuine meta-cognitive reflection
- Handle multi-file architecture changes
- Learn new skills through bootstrap learning

**With Sonnet 4.6**, Alex gets:

- Excellent coding capabilities (recommended for most development)
- 1M context window (beta) for large codebases
- 64K max output tokens + adaptive thinking
- Good cost-to-capability ratio
- Extended thinking support

**With Haiku 4.5**, Alex has:

- Near-frontier intelligence at lowest cost
- Fastest response times
- Good for routine operations

## Cost Optimization Strategy

| Session Type | Recommended Model | Rationale |
| ------------ | ----------------- | --------- |
| Architecture/design | Opus 4.6 | Worth the cost for complex decisions |
| Feature development | Sonnet 4.6 | Best balance of capability and cost |
| Bug fixes | Sonnet 4.6 or Haiku 4.5 | Depends on complexity |
| Documentation | Haiku 4.5 | Simple edits, fast turnaround |
| Large codebase analysis | Sonnet 4.6 (1M beta) | Extended context window up to 1M tokens |

## Knowledge Cutoffs

| Model | Reliable Knowledge | Training Data |
| ----- | ------------------ | ------------- |
| Opus 4.6 | May 2025 | Aug 2025 |
| Sonnet 4.6 | Aug 2025 | Jan 2026 |
| Haiku 4.5 | Feb 2025 | Jul 2025 |

## Auto Model Selection ⚠️

When using **Auto** in VS Code Copilot, the model switches dynamically based on task complexity. Alex cannot detect which model is currently running.

### Tasks That REQUIRE Opus 4.5 (Warn User)

| Task | Why Opus Required |
| ---- | ----------------- |
| Meditation/consolidation | Meta-cognitive protocols need full reasoning depth |
| Self-actualization | Comprehensive architecture assessment |
| Complex architecture refactoring | Multi-file changes, deep context |
| Bootstrap learning (new skills) | Skill acquisition needs maximum capability |
| Synapse validation/dream | Neural maintenance requires full architecture |
| Adaptive thinking tasks | Opus 4.6 uses dynamic reasoning depth for optimal results |

### Warning Protocol

When user requests an Opus-level task while potentially on Auto/lesser model:

> ⚠️ **Model Check**: This task works best with Claude Opus 4.6. If you're using Auto model selection, please manually select Opus from the model picker for optimal results. Continue anyway?

### Safe for Any Model

- Simple file edits, formatting
- Documentation updates
- Quick Q&A
- Code review (Sonnet+ recommended)
- Bug fixes (depends on complexity)

## Practical Guidance

### When to Upgrade Model Mid-Session

If you notice:

- Repeated mistakes on the same issue
- Losing context from earlier in conversation
- Superficial answers to complex questions
- Failure to see cross-file dependencies

→ Consider switching to a more capable model

### When to Downgrade

If you're doing:

- Repetitive mechanical edits
- Simple Q&A
- Format conversions
- Quick lookups

→ Save cost with a faster model

## The Alex Recommendation

For **Master Alex** (source of truth, architecture evolution):
→ **Always use Opus 4.6** — The cognitive architecture demands full capability

For **Heirs** (production deployment, user-facing):
→ **Default to Sonnet 4.6** — Best balance of capability and cost
→ **Allow Opus for complex tasks** — User can request escalation

## Token Economics

| Operation | Approximate Tokens | Opus 4.6 Cost | Sonnet 4.6 Cost |
| --------- | ------------------ | ------------- | --------------- |
| Read large file | 2,000-5,000 | $0.03-0.08 | $0.006-0.015 |
| Complex refactor | 10,000-20,000 | $0.15-0.30 | $0.03-0.06 |
| Full session | 50,000-150,000 | $0.75-2.25 | $0.15-0.45 |
| Meditation | 30,000-80,000 | $0.45-1.20 | $0.09-0.24 |

## Synapses

See [synapses.json](synapses.json) for connections.
