---
name: handoff-gemini
description: Delegate tasks to Gemini CLI to save Claude context
user-invocable: true
---

# Handoff to Gemini CLI

Delegate tasks to Google Gemini CLI to save Claude context.

---

## When to Use Gemini

| Use Gemini For | Keep in Claude |
|----------------|----------------|
| Long document analysis | Complex coding |
| Multimodal tasks | Architecture decisions |
| Research and summarization | Multi-step workflows |
| Large file comprehension | Problem analysis |

---

## Prerequisites

```bash
npm install -g @anthropic/gemini-cli
```

---

## Handoff Process

### 1. Prepare Context
```markdown
## Task for Gemini
**Goal**: [What needs to be done]
**Files**: [Which files to analyze]
**Output**: [What format to return]
```

### 2. Generate Command
```bash
# Analyze large file
gemini "Summarize components in codebase" -f src/**/*.ts

# Research task
gemini "Research best practices for [topic]"

# Document analysis
gemini "Extract key points" -f docs/spec.md
```

### 3. Provide Instructions
- Why Gemini is suitable
- Expected output
- How to continue workflow

---

## Example

```markdown
## Task: Research API Best Practices

**Command:**
gemini "Research REST API versioning strategies. Summarize pros/cons."

**After:**
- Review research
- Share relevant findings
- Implement chosen strategy
```

---

## Benefits

- **Token Savings**: Research tasks don't consume Claude context
- **Long Context**: Handles very large documents
- **Specialization**: Use each AI's strengths
