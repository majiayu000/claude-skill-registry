---
name: anthropic-evaluations
description: This skill should be used when the user asks to "create evals", "evaluate an agent", "build evaluation suite", or mentions agent testing, graders, or benchmarks. Also suggest when building coding agents, conversational agents, or research agents that need quality assurance.
---

# Anthropic Evaluations

Build rigorous evaluations for AI agents using Anthropic's proven patterns.

## Quick Reference

You MUST read the reference files for detailed guidance:

- [Grader Types](./references/grader-types.md) - Code-based, model-based, human graders
- [Agent Type Patterns](./references/agent-type-patterns.md) - Coding, conversational, research, computer use
- [Roadmap](./references/roadmap.md) - Steps 0-8 for building evals from scratch
- [Frameworks](./references/frameworks.md) - Harbor, Promptfoo, Braintrust, etc.

**YAML Templates:**
- [coding-agent-eval.yaml](./references/coding-agent-eval.yaml) - Coding agent template
- [conversational-agent-eval.yaml](./references/conversational-agent-eval.yaml) - Support agent template

**Annotated Examples:**
- [Example: Coding Agent](./references/example-coding-agent.md) - Auth bypass fix walkthrough
- [Example: Conversational](./references/example-conversational.md) - Refund handling walkthrough

## Core Definitions

| Term | Definition |
|------|------------|
| **Task** | Single test with defined inputs and success criteria |
| **Trial** | One attempt at a task (run multiple for consistency) |
| **Grader** | Logic that scores agent performance; tasks can have multiple |
| **Transcript** | Complete record of a trial (outputs, tool calls, reasoning) |
| **Outcome** | Final state in environment (not just what agent said) |
| **Evaluation harness** | Infrastructure that runs evals end-to-end |
| **Agent harness** | System enabling model to act as agent (scaffold) |
| **Evaluation suite** | Collection of tasks measuring specific capabilities |

## Grader Types (Quick Reference)

| Type | Methods | Best For |
|------|---------|----------|
| **Code-based** | String match, unit tests, static analysis, state checks | Fast, cheap, objective verification |
| **Model-based** | Rubric scoring, assertions, pairwise comparison | Nuanced, open-ended tasks |
| **Human** | SME review, A/B testing, spot-check sampling | Gold standard calibration |

See [Grader Types](./references/grader-types.md) for detailed comparison.

## Capability vs Regression Evals

| Type | Question | Target Pass Rate |
|------|----------|------------------|
| **Capability** | "What can this agent do well?" | Start low, hill-climb |
| **Regression** | "Does it still handle what it used to?" | Near 100% |

Capability evals with high pass rates "graduate" to regression suites.

## Non-Determinism Metrics

| Metric | Measures | Use When |
|--------|----------|----------|
| **pass@k** | At least 1 success in k attempts | One success matters (coding) |
| **pass^k** | All k attempts succeed | Consistency essential (customer-facing) |

Example: 75% per-trial success rate
- pass@3 ≈ 98% (likely to get at least one)
- pass^3 ≈ 42% (0.75³ all succeed)

## Tracked Metrics

```yaml
tracked_metrics:
  - type: transcript
    metrics: [n_turns, n_toolcalls, n_total_tokens]
  - type: latency
    metrics: [time_to_first_token, output_tokens_per_sec, time_to_last_token]
```

## Attribution

Based on [Demystifying evals for AI agents](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents) by Anthropic (January 2026).
