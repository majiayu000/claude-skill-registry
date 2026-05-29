---
name: mock-prediction
description: Mock prediction skill for 4-layer thinking test. Calls Task subagent.
allowed-tools: Read, Write, Task
model: claude-opus-4-5
permissionMode: dontAsk
context: fork
---

# Mock Prediction (Layer 2)

**Goal**: Test thinking token capture when forked skill calls Task subagent.

**Thinking**: Use `ultrathink` for this analysis.

## Task

1. Think about what we're testing: Layer 2 (forked skill) calling Layer 3 (Task subagent)
2. Write your reasoning to: `earnings-analysis/test-outputs/mock-prediction-reasoning.txt`
3. Call a Task subagent using the Task tool with subagent_type="Explore":
   - Ask it to find all SKILL.md files in .claude/skills/
   - Use model: opus for the subagent
4. After subagent returns, write summary to: `earnings-analysis/test-outputs/mock-prediction-summary.txt`

Include in your files:
- Note that this is "mock-prediction (Layer 2)"
- The subagent result
