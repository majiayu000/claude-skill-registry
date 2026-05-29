---
name: test-orchestrator-thinking
description: Layer 1 test - orchestrator forked skill that calls child skill to test thinking token capture
allowed-tools: Read, Write, Skill
model: claude-opus-4-5
permissionMode: dontAsk
context: fork
---

# Test Orchestrator Thinking (Layer 1)

**Goal**: Verify if thinking tokens are captured at multiple layers of forked skills.

**Thinking**: Use `ultrathink` for this analysis.

## Task

1. Think deeply about what we're testing: tracing thinking tokens through fork layers
2. Write your reasoning to: `earnings-analysis/test-outputs/orchestrator-reasoning.txt`
3. Then invoke the child skill: `/test-child-thinking`
4. After child completes, write summary to: `earnings-analysis/test-outputs/orchestrator-summary.txt`

Include in orchestrator-reasoning.txt:
- Your understanding of the test
- Your reasoning about what should happen
- A note that this is from "test-orchestrator-thinking skill (Layer 1)"
