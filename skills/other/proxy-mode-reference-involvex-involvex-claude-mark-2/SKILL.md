---
name: proxy-mode-reference
version: 1.0.0
description: Reference guide for using PROXY_MODE with external AI models. Use when running multi-model reviews, understanding which agents support PROXY_MODE, or debugging external model integration issues.
---

# PROXY_MODE Reference Guide

## What is PROXY_MODE?

PROXY_MODE is a directive that tells an agent to delegate its task to an external AI model via Claudish.

## How It Works

1. **Orchestrator** launches Task with PROXY_MODE-enabled agent
2. **Agent** detects `PROXY_MODE: {model}` at start of prompt
3. **Agent** extracts model ID and actual task
4. **Agent** runs `claudish --model {model}` with the task
5. **Agent** returns external model's response

## The PROXY_MODE Directive

Format:
```
PROXY_MODE: {model_id}

{actual task}
```

Example:
```
PROXY_MODE: x-ai/grok-code-fast-1

Review the architecture plan at ai-docs/plan.md
```

## Supported Agents

**Total: 18 PROXY_MODE-enabled agents across 3 plugins**

### agentdev plugin (3 agents)

| Agent | subagent_type | Best For |
|-------|---------------|----------|
| reviewer | `agentdev:reviewer` | Implementation quality reviews |
| architect | `agentdev:architect` | Design plan reviews |
| developer | `agentdev:developer` | Implementation with external models |

### frontend plugin (8 agents)

| Agent | subagent_type | Best For |
|-------|---------------|----------|
| plan-reviewer | `frontend:plan-reviewer` | Architecture plan validation |
| reviewer | `frontend:reviewer` | Code reviews |
| architect | `frontend:architect` | Architecture design |
| designer | `frontend:designer` | Design reviews |
| developer | `frontend:developer` | Full-stack implementation |
| ui-developer | `frontend:ui-developer` | UI implementation reviews |
| css-developer | `frontend:css-developer` | CSS architecture & styling |
| test-architect | `frontend:test-architect` | Testing strategy & implementation |

### seo plugin (5 agents)

| Agent | subagent_type | Best For |
|-------|---------------|----------|
| editor | `seo:editor` | SEO content reviews |
| writer | `seo:writer` | Content generation |
| analyst | `seo:analyst` | Analysis tasks |
| researcher | `seo:researcher` | Research & data gathering |
| data-analyst | `seo:data-analyst` | Data analysis & insights |

## Common Mistakes

### Mistake 1: Using general-purpose

```typescript
// ❌ WRONG
Task({
  subagent_type: "general-purpose",
  prompt: "PROXY_MODE: grok..."
})
```

`general-purpose` doesn't have `<proxy_mode_support>` so it won't recognize the directive.

### Mistake 2: Instructing agent to run claudish

```typescript
// ❌ WRONG
Task({
  subagent_type: "general-purpose",
  prompt: "Run claudish with model X to review..."
})
```

The agent doesn't know the claudish pattern. Use PROXY_MODE instead.

### Mistake 3: Wrong prompt format

```typescript
// ❌ WRONG - PROXY_MODE must be first line
Task({
  subagent_type: "agentdev:reviewer",
  prompt: "Please review this plan.
PROXY_MODE: grok..."
})
```

The directive must be at the START of the prompt.

## Correct Usage Pattern

```typescript
// ✅ CORRECT
Task({
  subagent_type: "agentdev:reviewer",
  description: "Grok review",
  run_in_background: true,
  prompt: `PROXY_MODE: x-ai/grok-code-fast-1

Review the implementation at path/to/file.ts

Focus on:
1. Code quality
2. Error handling
3. Performance
4. Security`
})
```

## Checking Agent Support

To verify if an agent supports PROXY_MODE:

```bash
# Find agents with PROXY_MODE support
grep -l "proxy_mode_support" plugins/*/agents/*.md

# Check specific agent
grep "proxy_mode_support" plugins/agentdev/agents/reviewer.md
```

## Troubleshooting

### "Agent didn't use external model"

**Cause:** Agent doesn't support PROXY_MODE
**Fix:** Use a PROXY_MODE-enabled agent (see table above)

### "Got Claude response instead of Grok response"

**Cause:** `general-purpose` or other non-PROXY_MODE agent was used
**Fix:** Switch to `agentdev:reviewer` or similar

### "PROXY_MODE directive in output"

**Cause:** Agent treated directive as content, not instruction
**Fix:** Use correct agent; ensure directive is first line
