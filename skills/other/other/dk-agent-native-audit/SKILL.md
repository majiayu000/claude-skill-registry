---
name: dk-agent-native-audit
description: "Run comprehensive agent-native architecture review with scored principles. Audits a codebase against 8 agent-native architecture principles (Action Parity, Tools as Primitives, Context Injection, Shared Workspace, CRUD Completeness, UI Integration, Capability Discovery, Prompt-Native Features) by launching parallel sub-agents and producing a scored report. Use when the user wants to evaluate how agent-friendly their architecture is, or audit specific principles. Triggers on: 'agent native audit', 'architecture review', 'how agent-friendly is this', or /dk-agent-native-audit."
argument-hint: "[optional: specific principle to audit, e.g. 'action parity' or '1']"
allowed-tools: Bash, Read, Grep, Glob, Task
disable-model-invocation: true
---

# /dk-agent-native-audit — Agent-Native Architecture Review

Conducts a comprehensive review of the codebase against agent-native architecture principles, launching parallel sub-agents for each principle and producing a scored report.

## Context

<audit_context> $ARGUMENTS </audit_context>

## Core Principles

| # | Principle | One-liner |
|---|-----------|-----------|
| 1 | Action Parity | Whatever the user can do, the agent can do |
| 2 | Tools as Primitives | Tools provide capability, not behavior |
| 3 | Context Injection | System prompt includes dynamic context about app state |
| 4 | Shared Workspace | Agent and user work in the same data space |
| 5 | CRUD Completeness | Every entity has full Create, Read, Update, Delete |
| 6 | UI Integration | Agent actions immediately reflected in UI |
| 7 | Capability Discovery | Users can discover what the agent can do |
| 8 | Prompt-Native Features | Features are prompts defining outcomes, not code |

## Workflow

### Step 1: Load reference material

Read `references/agent-prompts.md` in this skill's directory to get the detailed prompt for each sub-agent. That file contains the exact instructions, search strategies, and output format for all 8 principle audits.

### Step 2: Check for single-principle audit

If `$ARGUMENTS` specifies a single principle, only run that one sub-agent. Valid argument forms:

| Argument | Principle |
|----------|-----------|
| `action parity` or `1` | Action Parity |
| `tools` or `primitives` or `2` | Tools as Primitives |
| `context` or `injection` or `3` | Context Injection |
| `shared` or `workspace` or `4` | Shared Workspace |
| `crud` or `5` | CRUD Completeness |
| `ui` or `integration` or `6` | UI Integration |
| `discovery` or `7` | Capability Discovery |
| `prompt` or `features` or `8` | Prompt-Native Features |

For single-principle audits, run one Explore sub-agent and present its findings directly — no summary table needed.

### Step 3: Launch parallel sub-agents

Launch 8 parallel sub-agents using the Task tool with `subagent_type: Explore`, one per principle. Each agent should:

1. Enumerate all relevant instances in the codebase (user actions, tools, contexts, data stores, etc.)
2. Check compliance against the principle
3. Provide a specific score in `X out of Y (percentage%)` format
4. List specific gaps and recommendations

Read `references/agent-prompts.md` for the exact prompt to give each agent. Pass the full agent prompt from that file — don't summarize it.

### Step 4: Compile summary report

After all agents complete, compile the summary using this template:

```markdown
## Agent-Native Architecture Review: [Project Name]

### Overall Score Summary

| Core Principle | Score | Percentage | Status |
|----------------|-------|------------|--------|
| Action Parity | X/Y | Z% | STATUS |
| Tools as Primitives | X/Y | Z% | STATUS |
| Context Injection | X/Y | Z% | STATUS |
| Shared Workspace | X/Y | Z% | STATUS |
| CRUD Completeness | X/Y | Z% | STATUS |
| UI Integration | X/Y | Z% | STATUS |
| Capability Discovery | X/Y | Z% | STATUS |
| Prompt-Native Features | X/Y | Z% | STATUS |

**Overall Agent-Native Score: X%**

### Status Legend
- Excellent (80%+)
- Partial (50-79%)
- Needs Work (<50%)

### Top 10 Recommendations by Impact

| Priority | Action | Principle | Effort |
|----------|--------|-----------|--------|

### What's Working Well

[List top 5 strengths]
```

## Success criteria

- All 8 sub-agents complete their audits (or the single requested one)
- Each principle has a specific numeric score (X/Y format)
- Summary table shows all scores and status indicators
- Top 10 recommendations are prioritized by impact
- Report identifies both strengths and gaps
