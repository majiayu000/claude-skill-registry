---
name: prompt-writing
description: Creates effective prompts for AI coding agents and subagent delegation. Use PROACTIVELY when writing prompts for Task tool delegation, creating agent instructions, or designing multi-step workflows. MUST BE USED when delegating complex tasks to subagents or writing system prompts.
allowed-tools: ["Read", "Write", "Edit", "Grep", "Glob"]
---

# Prompt Writing Skill

## Overview

**Core Principle:** Context completeness over brevity. Agents cannot infer what you don't provide.

**Target Users:**
- Claude Code delegating to subagents via Task tool
- UI agents that need to generate prompts
- Engineers writing system prompts or agent instructions

---

## The CLEAR Framework

Use this mnemonic for every prompt you write:

| Letter | Component | Purpose | Key Question |
|--------|-----------|---------|--------------|
| **C** | Context | Background information | What does the agent need to know? |
| **L** | Limitations | Constraints, prohibitions | What should NOT be done? |
| **E** | Expectations | Output format, success criteria | What exactly should be returned? |
| **A** | Actions | Step-by-step instructions | What steps to follow? |
| **R** | Resources | Files, tools, references | What materials are available? |

### C - Context
Complete background: project state, environment, history. Include file paths, versions, prior decisions.

### L - Limitations
Explicit boundaries: DO NOT modify X, use only Y, forbidden patterns, compliance requirements.

### E - Expectations
Exact output format: markdown structure, JSON schema, where to save, success criteria checklist.

### A - Actions
Numbered steps, validation checkpoints, decision points, error handling guidance.

### R - Resources
Required reading (file paths), available tools, reference implementations, examples.

**Full guide with examples:** [reference/prompt-anatomy.md](reference/prompt-anatomy.md)

---

## Context Patterns

### Critical Insight
**Subagents have NO conversation history.** Each invocation is completely fresh. They cannot infer context.

### Three Strategies

| Strategy | When to Use | How |
|----------|-------------|-----|
| **File-Based** | Multi-step workflows | Save to file, pass path to next agent |
| **Embedded** | Small contexts | Include all info directly in prompt |
| **Layered** | Large contexts | Summary + references for deep-dive |

### State Transfer Pattern
```
Agent 1 → Save results to `.claude/state/results/agent-{timestamp}.md`
Agent 2 → Read from that file path
```

**Full patterns:** [reference/context-patterns.md](reference/context-patterns.md)

---

## Output Format Quick Reference

| Pattern | Use Case | Key Feature |
|---------|----------|-------------|
| **Structured Markdown** | Comprehensive results | Tables, sections, test output |
| **Binary Verdict** | Review/validation | PASS/FAIL first, then details |
| **Checklist** | Multi-requirement | Progress tracking with status |
| **Condensed** | Subagent responses | Max 3 findings, no verbose output |

### Delivery Patterns
- **State directory**: `.claude/state/results/[agent]-[timestamp].md`
- **Project output**: `output/[task-id]/[artifact].md`
- **Inline**: Return directly (use for summaries only)

**Full templates:** [reference/output-specifications.md](reference/output-specifications.md)

---

## Quality Checklist

**Before sending any prompt, verify:**

### Context (C)
- [ ] All background information included?
- [ ] File paths explicit and complete?
- [ ] No assumptions about prior knowledge?

### Limitations (L)
- [ ] Constraints clearly stated?
- [ ] Prohibited actions explicit?
- [ ] Scope boundaries defined?

### Expectations (E)
- [ ] Output format specified exactly?
- [ ] Success criteria measurable?
- [ ] Delivery location defined?

### Actions (A)
- [ ] Steps numbered and sequential?
- [ ] Validation checkpoints included?
- [ ] Error handling guidance provided?

### Resources (R)
- [ ] Required files listed with paths?
- [ ] Available tools mentioned?
- [ ] Examples provided where helpful?

### Subagent-Specific
- [ ] No implicit context assumptions?
- [ ] State transfer mechanism defined?
- [ ] Output format prevents overload?

---

## Anti-Patterns Quick Reference

| Anti-Pattern | Problem | Solution |
|--------------|---------|----------|
| **Context Amnesia** | Assumes agent remembers | Embed all context explicitly |
| **Vague Expectations** | "Give me a good result" | Specify exact format |
| **Implicit Constraints** | "Follow best practices" | List specific requirements |
| **Unbounded Scope** | "Improve the code" | Define precise boundaries |
| **Missing Resources** | "Check the docs" | Provide file paths |
| **Output Overload** | No format limits | Request condensed response |

**Full examples with solutions:** [reference/anti-patterns.md](reference/anti-patterns.md)

---

## Templates

Ready-to-use templates for common scenarios:

| Template | Purpose |
|----------|---------|
| [templates/subagent-delegation.md](templates/subagent-delegation.md) | Task tool delegation |
| [templates/code-task.md](templates/code-task.md) | Implementation tasks |
| [templates/research-task.md](templates/research-task.md) | Research/exploration |
| [templates/review-task.md](templates/review-task.md) | Code review/validation |

---

## Quick Start

1. **Choose template** from `templates/` matching your task type
2. **Fill CLEAR sections** systematically
3. **Run checklist** to verify completeness
4. **Execute** the prompt
5. **Iterate** if results don't match expectations

**Remember:** More context is almost always better. When in doubt, include it.

---

## Troubleshooting

| Problem | Likely Cause | Solution |
|---------|--------------|----------|
| Irrelevant results | Insufficient context | Add explicit file references, examples |
| Wrong format | Vague specification | Provide template with placeholders |
| Unwanted changes | Missing constraints | Add explicit DO NOT statements |
| Incomplete task | Unclear success criteria | Add specific acceptance criteria |
| Agent asks questions | Ambiguous requirements | Make all decisions upfront |

---

## Reference Documentation

- [reference/prompt-anatomy.md](reference/prompt-anatomy.md) - Full CLEAR examples by language
- [reference/context-patterns.md](reference/context-patterns.md) - State transfer strategies
- [reference/output-specifications.md](reference/output-specifications.md) - Output format templates
- [reference/anti-patterns.md](reference/anti-patterns.md) - Common mistakes and fixes
