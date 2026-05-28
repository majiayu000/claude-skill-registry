---
name: mock-orchestrator
description: Mock orchestrator for 4-layer thinking test. Calls prediction and attribution skills.
allowed-tools: Read, Write, Skill
model: claude-opus-4-5
permissionMode: dontAsk
context: fork
---

# Mock Orchestrator (Layer 1)

**Goal**: Test thinking token capture across 4 layers: Main → Orchestrator → Prediction/Attribution → Task Subagents

**Thinking**: Use `ultrathink` for this analysis.

## Task

1. Think about the 4-layer architecture we're testing
2. Write your reasoning to: `earnings-analysis/test-outputs/mock-orchestrator-reasoning.txt`
3. Call `/mock-prediction` skill (Layer 2 → Layer 3)
4. Call `/mock-attribution` skill (Layer 2 → Layer 3)
5. After both complete, write final summary to: `earnings-analysis/test-outputs/mock-orchestrator-final.txt`

Include in your files:
- Note that this is "mock-orchestrator (Layer 1)"
- Summary of what each child skill returned
- The complete layer structure being tested
