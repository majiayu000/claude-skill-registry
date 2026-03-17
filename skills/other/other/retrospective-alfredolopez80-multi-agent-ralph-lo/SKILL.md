---
# VERSION: 2.88.0
name: retrospective
description: Analyze completed tasks to improve the Ralph system
---

# Skill: Retrospective & Self-Improvement

**ultrathink** - Take a deep breath. We're not here to write code. We're here to make a dent in the universe.

## v2.88 Key Changes (MODEL-AGNOSTIC)

- **Model-agnostic**: Uses model configured in `~/.claude/settings.json` or CLI/env vars
- **No flags required**: Works with the configured default model
- **Flexible**: Works with GLM-5, Claude, Minimax, or any configured model
- **Settings-driven**: Model selection via `ANTHROPIC_DEFAULT_*_MODEL` env vars

## The Vision
Every retrospective should make the system inevitable and better.

## Your Work, Step by Step
1. **Summarize outcomes**: Task, complexity, iterations, models.
2. **Analyze effectiveness**: Routing, clarification, and agents.
3. **Identify gaps**: Missed checks or friction.
4. **Propose improvements**: Concrete, minimal changes.

## Ultrathink Principles in Practice
- **Think Different**: Question the status quo.
- **Obsess Over Details**: Use evidence, not guesses.
- **Plan Like Da Vinci**: Structure feedback before writing.
- **Craft, Don't Code**: Keep recommendations actionable.
- **Iterate Relentlessly**: Apply learnings immediately.
- **Simplify Ruthlessly**: Focus on the few changes that matter.

## Purpose
Analyze completed tasks to improve the Ralph Wiggum system.

## When to Use
MANDATORY after every task completion, before declaring VERIFIED_DONE.

## Analysis Categories

### 1. Routing Effectiveness
- Was the complexity classification accurate?
- Did the chosen model perform well?
- Should routing thresholds change?

## Agent Teams Integration (v2.88)

**Optimal Scenario**: Pure Agent Teams (Native)

This skill uses Pure Agent Teams with native coordination - no custom subagent specialization needed.

### Why Scenario A for This Skill
- Retrospective is primarily analytical and sequential
- Read/Grep tools available to all native agents
- Analysis doesn't require specialized tool restrictions
- Native agent types sufficient for metric gathering
- Lower complexity, faster execution

### Configuration
1. **TeamCreate**: Optional, for simple retrospective tasks
2. **Task**: Use native agent types (no ralph-* needed)
3. **Hooks**: TeammateIdle + TaskCompleted available if needed
4. **Simple**: Minimal setup overhead

### Workflow Pattern
```
TeamCreate (optional)
  → Task(analyze completed work)
  → Native agent gathers metrics
  → Complete with improvement proposals
```

### When This Is Sufficient
- Single-task retrospective analysis
- Simple metric gathering workflows
- No specialized analysis needed
- Quick post-task reviews preferred

### 2. Clarification Quality
- Were the right questions asked?
- Did any missed clarifications cause rework?
- Should question templates be updated?

### 3. Agent Performance
- Which subagents were most useful?
- Any agents that didn't add value?
- New agent patterns needed?

### 4. Quality Gate Effectiveness
- Did gates catch real issues?
- Any false positives/negatives?
- Missing validations?

### 5. Iteration Efficiency
- How many iterations were used?
- Could it have been done faster?
- Any wasted iterations?

## Output Format

```markdown
## 📊 Task Retrospective

### Summary
- Task: [description]
- Complexity: [classified] → [actual]
- Iterations: [used] / [limit]
- Models: [list used]

### What Went Well
- [positive 1]
- [positive 2]

### Improvement Opportunities
1. **[Category]**: [description]
   - Current: [what happens now]
   - Proposed: [improvement]
   - Impact: [low/medium/high]
   - Risk: [low/medium/high]

### Proposed Changes
```json
{
  "type": "routing_adjustment|clarification_enhancement|agent_behavior|new_command|delegation_update|quality_gate",
  "file": "[path to modify]",
  "change": "[description]",
  "justification": "[why]"
}
```
```

## Improvement Types

| Type | Example |
|------|---------|
| routing_adjustment | Change complexity thresholds |
| clarification_enhancement | Add new question templates |
| agent_behavior | Modify agent instructions |
| new_command | Create new slash command |
| delegation_update | Change model assignments |
| quality_gate | Add/modify validations |
