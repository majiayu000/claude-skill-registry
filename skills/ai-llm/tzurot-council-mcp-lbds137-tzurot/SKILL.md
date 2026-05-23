---
name: tzurot-council-mcp
description: Best practices for using the Council MCP server in Tzurot v3 development - When to consult external AI, how to structure prompts, model selection, and multi-turn conversations. Use when planning major changes or needing a second opinion.
lastUpdated: '2026-01-21'
---

# Tzurot v3 Council MCP Collaboration

**Use this skill when:** Planning major refactors, debugging complex issues, getting code reviews, brainstorming solutions, validating architectural decisions, or needing a second opinion.

## Overview

The Council MCP (v4.0.0) provides access to multiple AI models via OpenRouter. Default model is `google/gemini-3-pro-preview`.

## Available Tools

### Core Tools

| Tool                                    | Purpose                       |
| --------------------------------------- | ----------------------------- |
| `mcp__council__ask`                     | Ask general questions         |
| `mcp__council__brainstorm`              | Brainstorm ideas/solutions    |
| `mcp__council__code_review`             | Code review feedback          |
| `mcp__council__test_cases`              | Test case suggestions         |
| `mcp__council__explain`                 | Explain complex code/concepts |
| `mcp__council__synthesize_perspectives` | Combine multiple viewpoints   |

### New in v4.0.0

| Tool                            | Purpose                                                        |
| ------------------------------- | -------------------------------------------------------------- |
| `mcp__council__debug`           | Structured debugging with hypotheses, tracks previous attempts |
| `mcp__council__refactor`        | Step-by-step refactoring plans with before/after examples      |
| `mcp__council__recommend_model` | Get best model for a task type                                 |
| `mcp__council__list_models`     | Browse available models with filtering                         |
| `mcp__council__set_model`       | Change active model for session                                |

### Multi-Turn Conversations

| Tool                                     | Purpose                           |
| ---------------------------------------- | --------------------------------- |
| `mcp__council__start_conversation`       | Start session with specific model |
| `mcp__council__continue_conversation`    | Send follow-up message            |
| `mcp__council__list_conversations`       | List active sessions              |
| `mcp__council__get_conversation_history` | Get full message history          |
| `mcp__council__end_conversation`         | End session, optionally summarize |

## When to Consult Council

### Always Use For

**Major Refactorings (>500 lines)**

```typescript
mcp__council__brainstorm({
  topic: 'Risks in refactoring PersonalityService',
  constraints: 'Must maintain exact functionality',
});
```

**Structured Debugging**

```typescript
mcp__council__debug({
  error_message: 'Memory leak in BullMQ workers',
  code_context: 'Workers OOM after 2 hours',
  previous_attempts: ['Checked event listeners', 'Reviewed Redis connections'],
});
```

**Safe Refactoring Plans**

```typescript
mcp__council__refactor({
  code: myCode,
  goal: 'reduce_complexity', // or: extract_method, simplify_logic, improve_naming, etc.
  language: 'typescript',
});
```

**Before Completing Major PRs**

```typescript
mcp__council__code_review({
  code: changes,
  focus: 'behavior preservation, edge cases',
  language: 'typescript',
});
```

**When Thinking "This seems unnecessary"**
STOP! Consult Council before removing code.

### Don't Use For

- Questions answered by existing docs/skills
- Obvious code issues (typos, syntax errors)
- Small style preferences

## Model Selection

### Quick Guide

| Task Type        | Recommended Models                      |
| ---------------- | --------------------------------------- |
| Coding/Review    | Claude Sonnet 4, Claude 3.5 Sonnet      |
| Reasoning/Math   | DeepSeek R1, Gemini 3 Pro               |
| Vision/Images    | Gemini 2.5 Flash, Gemini 2.5 Pro        |
| Web Development  | Gemini 2.5 Pro                          |
| Long Documents   | Gemini (1M tokens), Llama 4 Scout (10M) |
| General/Creative | Claude 3.5 Sonnet, GPT-4o               |

### Model Classes

- **FLASH**: Fast & cheap (Haiku, GPT-4o-mini, Gemini Flash)
- **PRO**: Balanced quality/cost (Sonnet, GPT-4o, Gemini Pro)
- **DEEP**: Maximum quality (Opus, o1, DeepSeek R1)

### Free Tier Options

- `meta-llama/llama-3.3-70b-instruct:free`
- `deepseek/deepseek-chat:free`
- `qwen/qwen-2.5-72b-instruct:free`

### Using Model Selection

```typescript
// Get recommendation for task
mcp__council__recommend_model({ task: 'code_review' });

// Change model for session
mcp__council__set_model({ model: 'anthropic/claude-3.5-sonnet' });

// Or specify per-call
mcp__council__code_review({
  code: myCode,
  model: 'anthropic/claude-3.5-sonnet',
});
```

## Multi-Turn Conversations

For complex discussions that need context across multiple exchanges:

```typescript
// Start a session
const { session_id } = await mcp__council__start_conversation({
  model: 'deepseek/deepseek-r1',
  system_prompt: 'You are a TypeScript architecture expert',
  initial_message: 'Review this service design...',
});

// Continue the conversation
await mcp__council__continue_conversation({
  session_id,
  message: 'What about the error handling?',
});

// End and get summary
await mcp__council__end_conversation({
  session_id,
  summarize: true,
});
```

## Prompt Structuring

```typescript
// BAD - No context
mcp__council__ask({ question: 'How do I fix this?' });

// GOOD - Full context
mcp__council__ask({
  question: 'How do I fix race condition in webhook reply tracking?',
  context: 'Using Redis to map message IDs. Bot-client and api-gateway both access Redis.',
});

// BAD - Generic review
mcp__council__code_review({ code: myCode });

// GOOD - Focused review
mcp__council__code_review({
  code: myCode,
  focus: 'resource leaks, error handling, Redis connection management',
  language: 'typescript',
});
```

## The Safety Stack

**Thinking -> MCP -> Action**

1. Use thinking keywords to analyze ("Ultrathink about...")
2. Consult Council for second opinion
3. Follow project guidelines

## Council Limitations

**Council doesn't have access to:**

- Your local filesystem
- Project-specific documentation (unless provided)
- Git history

**Always validate against:**

- Project guidelines (CLAUDE.md, skills)
- Existing codebase patterns
- Architecture decisions

## When Council and Claude Disagree

**Resolution hierarchy:**

1. Project guidelines (CLAUDE.md, skills)
2. Existing codebase patterns
3. Technical correctness
4. User preference

## Related Skills

- **tzurot-architecture** - Major design decisions
- **tzurot-docs** - Document recommendations
- **tzurot-security** - Security pattern validation
- **tzurot-testing** - Test case suggestions

## References

- MCP tools: `mcp__council__*` functions
- Thinking keywords: `~/.claude/CLAUDE.md#mandatory-thinking-requirements`
- Project guidelines: `CLAUDE.md`
