---
name: codex-architect
description: Codex architecture consulting (third brain). Get Codex architecture advice during design phase, forming dual perspective with Claude.
allowed-tools: Read, Grep, Glob, mcp__codex__codex, mcp__codex__codex-reply
---

# Codex Architect Skill (Third Brain)

## Trigger

- Keywords: architecture design, solution evaluation, tech selection, third brain, Codex advice, design consulting, ask Codex, second opinion

## When NOT to Use

- Code implementation (use /codex-implement)
- Code review (use /codex-review)
- Deep discussion/exhaustive exploration (use /codex-brainstorm)

## Usage

```bash
/codex-architect "<question>"
/codex-architect "Evaluate this design" --context src/xxx.ts --mode review
/codex-architect "Redis vs MongoDB?" --mode compare
```

## Modes

| Mode    | Purpose                 | When                       |
| ------- | ----------------------- | -------------------------- |
| design  | Provide design advice   | Starting from scratch (default) |
| review  | Evaluate existing design | Validate solution, find issues |
| compare | Compare multiple options | Tech selection             |

## Core Principle

```
User -> Claude -> Codex -> Integrate
          |         |         |
    Initial thinking  Third perspective  Combined advice
```

## Codex Prompt Template

When using `mcp__codex__codex`, must include the following:

```typescript
mcp__codex__codex({
  prompt: `You are a senior architect. Please provide architecture advice for the following question.

## Question
${QUESTION}

## Mode
${MODE} (design/review/compare)

## IMPORTANT: You must independently research the project

Before providing architecture advice, you **must** perform the following research:

### Research Steps
1. Understand project structure: \`ls src/\`, \`ls src/service/\`, \`ls src/provider/\`
2. Search related modules: \`grep -r "keyword" src/ --include="*.ts" -l | head -10\`
3. Read existing implementations: \`cat <relevant files> | head -150\`
4. Understand existing architecture patterns and conventions

### Verification Focus
- What does the existing architecture look like?
- What are the existing code style and patterns?
- What similar features can be referenced?

## Output Requirements

1. First describe which files you researched
2. Provide advice based on current project state
3. Consider consistency with existing architecture

...(other review dimensions)`,
  sandbox: 'read-only',
  'approval-policy': 'never',
});
```

## Workflow Integration

```
/codex-architect -> /tech-spec -> /review-spec -> /codex-implement -> /codex-review-fast
    Design           Plan          Review          Implement          Code Review
```

## Verification

- Report includes Codex advice + Claude perspective
- Consensus and divergence points clearly marked
- Final recommendation integrates both perspectives

## References

- `references/project-knowledge.md` - Project architecture knowledge + report template

## Examples

```
Input: /codex-architect "How to design a high-concurrency cache?"
Action: Codex analysis -> Claude supplement -> Integrated output
```

```
Input: /codex-architect "Any issues with this API design?" --mode review
Action: Codex evaluation -> Claude verification -> Output issues + recommendations
```
