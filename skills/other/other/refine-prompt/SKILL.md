---
allowed-tools: Bash(mkdir:*), Read, Write, Glob
argument-hint: '[prompt-request]'
disable-model-invocation: true
model: opus
name: refine-prompt
user-invocable: true
description: This skill should be used when the user asks to "refine a prompt", "optimize a prompt", "improve my prompt", "rewrite prompt for LLM", "craft a better prompt", or mentions prompt engineering, prompt optimization, or appending to PROMPT.md.
---

## Context

- Working directory: !`pwd`
- Request: $ARGUMENTS

## Task

You are an expert prompt engineer. Create an optimized prompt based on `$ARGUMENTS`.

### 1. Craft the Prompt

Apply relevant techniques:

- Few-shot examples (when helpful)
- Chain-of-thought reasoning
- Role/perspective setting
- Output format specification
- Constraints and boundaries
- Self-consistency checks

Structure with:

- Clear role definition (if applicable)
- Explicit task description
- Expected output format
- Constraints and guidelines

### 2. Display the Result

Show the complete prompt in a code block, ready to copy:

```
[Complete prompt text]
```

Briefly note which techniques you applied and why.

### 3. Save to .ai/PROMPT.md

First ensure the directory exists: `mkdir -p .ai`

**If `.ai/PROMPT.md` exists:**

Read current contents and append:

```
---

## [Brief title from $ARGUMENTS]

[The optimized prompt]
```

**If `.ai/PROMPT.md` does not exist:**

Create with:

```
# Optimized Prompts

## [Brief title from $ARGUMENTS]

[The optimized prompt]
```

Confirm: "Saved to .ai/PROMPT.md"
