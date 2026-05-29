---
name: cc-askuserquestion
description: Use when designing AskUserQuestion tool calls - covers schema constraints, effectiveness patterns, and known issues.
---

# AskUserQuestion Tool

Structured user input for clarifying requirements and gathering decisions.

## Schema

```typescript
{
  questions: Array<{
    // 1-4 questions per call
    question: string; // Full question text, ends with "?"
    header: string; // Max 12 chars, displayed as chip/tag
    multiSelect: boolean; // true = multiple selections allowed
    options: Array<{
      // 2-4 options per question
      label: string; // 1-5 words, concise and scannable
      description: string; // Explains implications and trade-offs
    }>;
  }>;
}
```

**Constraints:**

- Questions: 1-4 per call
- Options: 2-4 per question (min 2, max 4)
- Header: max 12 characters
- Label: 1-5 words
- Timeout: 60 seconds for user response
- "Other": Always available for custom text input (automatic)

## Effectiveness Patterns

### Label + Description Separation

Labels should be **scannable**, descriptions should provide **context**.

```typescript
// GOOD - concise label, detailed description
{
  label: "Immediate failure",
  description: "Fail fast and expose errors to caller immediately. Best for debugging."
}

// BAD - everything crammed into label
{
  label: "Fail fast and expose errors immediately to the caller",
  description: "Good for debugging"
}
```

### Mark Recommended Option

Place recommended option **first** with "(Recommended)" suffix:

```typescript
options: [
  { label: "JWT tokens (Recommended)", description: "Stateless, scalable..." },
  { label: "Session cookies", description: "Simpler but requires state..." },
  { label: "OAuth only", description: "Delegates auth entirely..." },
];
```

### Use multiSelect for Non-Exclusive Choices

```typescript
// multiSelect: true - user can pick multiple
{
  question: "Which OAuth providers should we support?",
  header: "Providers",
  multiSelect: true,
  options: [
    { label: "Google", description: "Widest adoption" },
    { label: "GitHub", description: "Developer-focused" },
    { label: "Microsoft", description: "Enterprise integration" }
  ]
}
```

### Interview-Then-Execute Workflow

**Phase 1 - Interview:** Use AskUserQuestion to gather requirements
**Phase 2 - Specification:** Produce written spec from answers
**Phase 3 - Execution:** Implement with ambiguity eliminated

This reduces rework by 50-80% compared to assumption-driven development.

## Known Issues

### PreToolUse Hooks Break AskUserQuestion

When PreToolUse hooks are active, AskUserQuestion may return **empty responses** without showing UI.

**Workaround:** Use `PermissionRequest` hook instead of `PreToolUse`. Both hooks fire for AskUserQuestion, but `PermissionRequest` is semantically correct for user-input scenarios and avoids the stdin/stdout conflict.

See `cc-writing-hooks` skill for implementation example.

### Cannot Use From Subagents

AskUserQuestion only works in main conversation thread, not from Task tool subagents.

### Permission Mode Conflicts

Issues reported when bypass permissions enabled. Test in your environment.

## Context Source

Guidance for using AskUserQuestion works **similarly regardless of source**:

- System prompts / CLAUDE.md
- Rules (.claude/rules/)
- Skills
- Hook additionalContext

All end up in Claude's context. No documented performance difference.

## References

### Official Documentation

- [Handle approvals and user input - Claude Docs](https://platform.claude.com/docs/en/agent-sdk/user-input)
- [Internal tool implementation (schema source)](https://gist.github.com/bgauryy/0cdb9aa337d01ae5bd0c803943aa36bd)
- [claude-code-system-prompts - tool description](https://github.com/Piebald-AI/claude-code-system-prompts/blob/main/system-prompts/tool-description-askuserquestion.md)

### Effectiveness Claims

- [SmartScope guide](https://smartscope.blog/en/generative-ai/claude/claude-code-askuserquestion-tool-guide/) - 50-80% rework reduction, interview-then-execute workflow
- [atcyrus guide](https://www.atcyrus.com/stories/claude-code-ask-user-question-tool-guide) - Label/description patterns
- [egghead.io course](https://egghead.io/create-interactive-ai-tools-with-claude-codes-ask-user-question~b47wn) - Interactive patterns

### GitHub Issues

- [#15872](https://github.com/anthropics/claude-code/issues/15872) - Feature request: hook support for AskUserQuestion
