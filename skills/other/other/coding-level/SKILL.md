---
name: coding-level
version: 1.0.0
description: '[Utilities] Set coding experience level for tailored explanations'
activation: user-invoked
---

> **[IMPORTANT]** Use `TaskCreate` to break ALL work into small tasks BEFORE starting — including tasks for each file read. This prevents context loss from long files. For simple tasks, AI may ask user whether to skip.

## Quick Summary

**Goal:** Set the user's coding experience level to tailor explanation depth and detail.

**Workflow:**
1. **Ask** -- Query user for their experience level (beginner/intermediate/expert)
2. **Configure** -- Adjust response verbosity and explanation depth accordingly

**Key Rules:**
- Expert: minimal explanation, focus on code and architecture
- Intermediate: moderate explanation with key concepts
- Beginner: detailed explanation with examples and context

Set your coding experience level for tailored explanations and output format.

## Usage

`/coding-level [0-5]`

## Levels

| Level | Name      | Description                                                 |
| ----- | --------- | ----------------------------------------------------------- |
| 0     | ELI5      | Zero coding experience - analogies, no jargon, step-by-step |
| 1     | Junior    | 0-2 years - concepts explained, WHY not just HOW            |
| 2     | Mid-Level | 3-5 years - design patterns, system thinking                |
| 3     | Senior    | 5-8 years - trade-offs, business context, architecture      |
| 4     | Tech Lead | 8-10 years - risk assessment, business impact, strategy     |
| 5     | God Mode  | Expert - default behavior, maximum efficiency (default)     |

## How It Works

1. Set `codingLevel` in `.claude/.ck.json`
2. Guidelines are **automatically injected** on every session start
3. No manual activation needed - it just works!

## Example

Set level 1 in `.claude/.ck.json`:

```json
{
  "codingLevel": 1,
  ...
}
```

Next session, Claude will automatically:

- Explain concepts and techniques clearly
- Always explain WHY, not just HOW
- Point out common mistakes
- Add "Key Takeaways" after implementations

## Optional: Manual Output Styles

For finer control, you can also use `/output-style` with these styles:

- `coding-level-0-eli5`
- `coding-level-1-junior`
- `coding-level-2-mid`
- `coding-level-3-senior`
- `coding-level-4-lead`
- `coding-level-5-god`

---

**IMPORTANT Task Planning Notes (MUST FOLLOW)**

- Always plan and break work into many small todo tasks
- Always add a final review todo task to verify work quality and identify fixes/enhancements
