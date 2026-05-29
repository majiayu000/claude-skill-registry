---
name: analyze-skills
description: Analyze ~/.claude session files to find unused agent skills and reduce context token waste. Scans subagent JSONL files for injected skills and cross-references with agent responses.
user-invocable: true
argument-hint: "[project-filter]"
---

# Analyze Agent Skill Usage

You are analyzing Claude Code session files to determine which agent skills are actually used vs wasted context tokens.

## What This Does

Scans `~/.claude/projects/` for subagent JSONL files, detects which skills were injected into each agent, and checks whether the agent actually referenced that skill's content. Produces a report with recommendations to optimize agent configurations.

## Step 1: Find Subagent Files

Find all subagent JSONL files for the target project:

```bash
# If project argument provided, filter by it. Otherwise use current project.
# Subagent files live at: ~/.claude/projects/<encoded-path>/<session-id>/subagents/agent-*.jsonl
find ~/.claude/projects/ -path "*/subagents/agent-*.jsonl" -type f 2>/dev/null
```

If `$ARGUMENTS.project` is provided, filter paths containing that project name.
If not provided, use the current working directory to determine the project.

## Step 2: Read Agent Definitions

Read all agent files from `.claude/agents/*.md` in the current project. Extract:
- Agent name (from frontmatter `name:`)
- Skills list (from frontmatter `skills:`)

## Step 3: Analyze Each Subagent File

For each subagent JSONL file:

### 3a. Identify the agent type
Look at the first user message — it usually contains the task description from the `Task` tool prompt. Cross-reference with the parent session if needed.

### 3b. Extract injected skills
Search the first 20 lines for `<command-name>SKILL_NAME</command-name>` markers. This tells you which skills were loaded into the agent's context.

### 3c. Check skill usage
For each injected skill, search the agent's **assistant** messages for distinctive keywords:

| Skill | Keywords to search for |
|---|---|
| `uiux` | gray-950, terracotta, design system, bg-gray, border-gray |
| `tanstack-start` | createServerFn, server function, TanStack Start, SSR |
| `typescript-rules` | strict typing, Zod, z.object, z.infer, unknown, type guard |
| `react-rules` | useQuery, useSuspenseQuery, queryOptions, named export, TanStack Query |
| `testing` | vitest, describe, it, expect, vi.mock, happy-dom, testing-library |
| `playwright-cli` | playwright, browser, e2e, spec.ts, page.goto |
| `sdlc` | pipeline, SDLC, acceptance criteria |

A skill is "used" if ANY of its keywords appear in the agent's assistant responses.

## Step 4: Build Usage Matrix

Aggregate results into a table:

```
Agent Type | Skill | Injected | Used | Usage % | Recommendation
-----------|-------|----------|------|---------|---------------
architect  | tanstack-start | 15 | 8 | 53% | KEEP
...
```

## Step 5: Generate Report

Output a structured report with:

### 5a. Per-Agent Summary
For each agent type, show:
- Current skills (from `.claude/agents/<name>.md`)
- Usage rates from session data
- Recommended changes (KEEP / REMOVE / ADD)

### 5b. Token Savings Estimate
For each removed skill, estimate context tokens saved:
- Read the skill's SKILL.md file
- Count approximate tokens (chars / 4)
- Multiply by number of agent invocations

### 5c. Actionable Changes
List the exact frontmatter changes needed for each agent file. Example:

```yaml
# .claude/agents/implementer.md — BEFORE
skills:
  - tanstack-start
  - typescript-rules
  - react-rules
  - uiux              # REMOVE (3% usage, ~1.5K tokens wasted per invocation)

# .claude/agents/implementer.md — AFTER
skills:
  - tanstack-start
  - typescript-rules
  - react-rules
```

### 5d. Skills Not Assigned to Any Agent
List skills in `.claude/skills/` that are NOT in any agent's frontmatter. These are either:
- Main-context-only skills (like `/feature`, `/review`) — expected
- Potentially useful skills missing from agents — flag for review

## Step 6: Ask User

After presenting the report, use AskUserQuestion to ask:
"Would you like me to apply the recommended changes to the agent configuration files?"

If yes, update the `.claude/agents/*.md` files with the optimized skill lists.

## Important Rules

- **Read-only for ~/.claude** — never modify files in `~/.claude/`
- Agent config files (`.claude/agents/*.md`) are in the project — those CAN be modified
- Base recommendations on data, not assumptions
- A skill with < 15% usage rate across 5+ invocations is a REMOVE candidate
- A skill with 0% usage across ANY number of invocations is a definite REMOVE
- Always show the data before recommending changes
- Consider that some skills may be critical for rare but important tasks — flag these as REVIEW rather than REMOVE
