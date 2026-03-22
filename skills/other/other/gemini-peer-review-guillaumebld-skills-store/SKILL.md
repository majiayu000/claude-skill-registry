---
name: gemini-peer-review
description: "Get a second opinion from Gemini on code, architecture, debugging, or security. Uses gemini-coach CLI with AI-to-AI prompting for clear, actionable analysis. Trigger with 'ask gemini', 'gemini review', 'second opinion', 'peer review', or 'consult gemini'."
compatibility: claude-code-only
---

# Gemini Peer Review

Consult Gemini as a coding peer for a second opinion on code quality, architecture decisions, debugging, or security reviews.

## Prerequisites

- `gemini-coach` CLI installed (wraps Gemini CLI with AI-to-AI prompting)
- Gemini CLI authenticated (`gemini` to test)

## Modes

### Code Review

```bash
gemini-coach review src/auth.ts src/api.ts
```

Review specific files for bugs, logic errors, security vulnerabilities, performance issues, and best practice violations.

### Architecture Advice

```bash
gemini-coach architect "Should I use D1 or KV for session storage?" .
```

Get feedback on design decisions with trade-off analysis. Passing `.` includes project context.

### Debugging Help

```bash
gemini-coach debug src/problematic-file.ts
```

Analyse errors when stuck after 2+ failed fix attempts. Gemini sees the code fresh without your debugging context bias.

### Security Scan

```bash
gemini-coach security-scan ./src/api/
```

Scan code for security vulnerabilities (injection, auth bypass, data exposure).

### Quick Question

```bash
gemini-coach quick "Best way to handle WebSockets in Workers?"
```

Fast question without file context.

### Project Review

```bash
gemini-coach project-review "Analyse architecture and suggest improvements" /path/to/project
```

Full project analysis using Gemini's 1M token context.

## When to Use

**Good use cases**:
- Before committing major changes (final review)
- When stuck debugging after multiple attempts
- Architecture decisions with multiple valid options
- Security-sensitive code review
- "What am I missing?" moments

**Avoid using for**:
- Simple syntax checks (Claude handles these faster)
- Every single edit (too slow, unnecessary)
- Questions with obvious answers

## Model Selection

`gemini-coach` automatically selects the right model:

| Mode | Model | Typical Time |
|------|-------|-------------|
| review, debug, quick | gemini-2.5-flash | 5-15s |
| architect, security-scan | gemini-2.5-pro | 15-30s |

Override: `GEMINI_MODEL=gemini-2.5-pro gemini-coach review ...`

## Synthesizing Results

After receiving Gemini's analysis:
1. Present Gemini's findings to the user
2. Add your own perspective — agree/disagree with specific points
3. Let the user decide which recommendations to implement

## Reference Files

| When | Read |
|------|------|
| AI-to-AI prompt templates, model details | [references/prompt-templates.md](references/prompt-templates.md) |
