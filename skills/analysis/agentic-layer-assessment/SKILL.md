---
name: agentic-layer-assessment
description: Assess agentic layer maturity using the 12-grade classification system (Class 1-3). Use when evaluating codebase readiness, identifying next upgrade steps, or tracking progress toward the Codebase Singularity.
allowed-tools: Read, Grep, Glob
---

# Agentic Layer Assessment

Assess agentic layer maturity using the complete 12-grade classification system from TAC Lesson 14.

## When to Use

- Evaluating current agentic layer maturity
- Identifying the next grade to achieve
- Tracking progress toward Codebase Singularity
- Onboarding new team members to agentic patterns
- Planning agentic infrastructure investments

## Prerequisites

- Access to the codebase's `.claude/` directory
- Understanding of @adw-framework.md classification system

## The Classification System

Three classes with 12 total grades:

### Class 1: Foundation (In-Loop Agentic Coding)

| Grade | Component | Indicator |
| --- | --- | --- |
| 1 | Memory Files | CLAUDE.md exists with guidance |
| 2 | Sub-Agents | Task agents used for parallelization |
| 3 | Skills/MCPs | Custom skills or MCP integrations |
| 4 | Closed-Loops | Self-validating prompts |
| 5 | Templates | Bug/feature/chore classification |
| 6 | Prompt Chains | Multi-step composite workflows |
| 7 | Agent Experts | Expertise files with self-improve |

### Class 2: External Integration (Out-Loop Agentic Coding)

| Grade | Component | Indicator |
| --- | --- | --- |
| 1 | Webhooks | External triggers (PITER framework) |
| 2 | ADWs | AI Developer Workflows running |

### Class 3: Production Orchestration (Orchestrated Agentic Coding)

| Grade | Component | Indicator |
| --- | --- | --- |
| 1 | Orchestrator | Meta-agent managing fleet |
| 2 | Orchestrator Workflows | Human-orchestrator interaction |
| 3 | ADWs + Orchestrator | Full autonomous execution |

## Assessment Process

### Step 1: Scan Codebase

Check for indicators of each grade:

```bash
# Grade 1: Memory files
ls .claude/ CLAUDE.md

# Grade 2: Sub-agents
ls .claude/agents/

# Grade 3: Skills
ls .claude/skills/ || ls -d */skills/ 2>/dev/null

# Grade 4: Closed-loop patterns
grep -r "validation" .claude/commands/
grep -r "retry" .claude/commands/

# Grade 5: Templates
ls .claude/commands/ | grep -E "(chore|bug|feature)"

# Grade 6: Prompt chains
grep -r "Step 1" .claude/commands/
grep -r "Then execute" .claude/commands/

# Grade 7: Agent experts
ls .claude/commands/experts/ 2>/dev/null
find . -name "expertise.yaml"

# Grade 8 (Class 2 G1): Webhooks
find . -name "*webhook*" -o -name "*trigger*"

# Grade 9 (Class 2 G2): ADWs
ls adws/ 2>/dev/null

# Grade 10-12 (Class 3): Orchestrator
find . -name "*orchestrator*"
```

### Step 2: Score Each Grade

For each grade, determine status:

| Status | Meaning |
| --- | --- |
| ✅ Complete | Fully implemented and used |
| 🔶 Partial | Some elements present |
| ❌ Missing | Not implemented |

### Step 3: Calculate Current Level

Your level = highest consecutive completed grade

Example:

- Grades 1-4: ✅
- Grade 5: 🔶
- Grades 6-7: ❌

**Result**: Class 1 Grade 4 (solid), targeting Grade 5

### Step 4: Identify Next Step

Recommend specific actions for next grade:

| Current | Next Step |
| --- | --- |
| Grade 1 | Add Task agents for parallelization |
| Grade 2 | Create custom skills or MCP |
| Grade 3 | Add validation loops to prompts |
| Grade 4 | Implement issue classification templates |
| Grade 5 | Chain prompts into workflows |
| Grade 6 | Build first agent expert |
| Grade 7 | Set up external triggers |
| C2G1 | Implement AI Developer Workflows |
| C2G2 | Build orchestrator agent |
| C3G1 | Add human-orchestrator workflows |
| C3G2 | Connect orchestrator to ADWs |

## Output Format

```markdown
## Agentic Layer Assessment Report

**Codebase:** [project name]
**Date:** [assessment date]
**Assessed by:** [model]

### Classification Summary

**Current Level:** Class [1/2/3] Grade [1-7/1-2/1-3]
**Maturity Score:** [X]/12 grades achieved

### Grade-by-Grade Assessment

| Grade | Component | Status | Evidence |
| --- | --- | --- | --- |
| C1G1 | Memory Files | ✅/🔶/❌ | [what was found] |
| C1G2 | Sub-Agents | ✅/🔶/❌ | [what was found] |
...

### Strengths

- [What's working well]

### Gaps

- [What's missing or weak]

### Recommended Next Steps

1. **Priority 1:** [Most impactful improvement]
2. **Priority 2:** [Second priority]
3. **Priority 3:** [Third priority]

### Path to Class 3

[Roadmap of remaining grades to achieve]
```

## Assessment Checklist

- [ ] Scanned `.claude/` directory structure
- [ ] Checked for memory files (CLAUDE.md)
- [ ] Searched for agent/skill definitions
- [ ] Analyzed prompt patterns (loops, chains)
- [ ] Looked for templates and classification
- [ ] Checked for expertise files
- [ ] Searched for external triggers
- [ ] Identified ADW presence
- [ ] Assessed orchestrator implementation
- [ ] Calculated maturity score
- [ ] Identified highest consecutive grade
- [ ] Recommended next steps

## Key Insight

> "Your agentic layer should be specialized to fit and wrap your codebase. Don't focus on reuse, focus on making these prompts great for that one codebase."

Each grade builds on the previous. Skip a grade and the foundation becomes unstable.

## Anti-Patterns

| Anti-Pattern | Problem | Solution |
| --- | --- | --- |
| Skipping grades | Missing foundation | Build progressively |
| Over-engineering early | Complexity before value | Start with Grade 1-2 |
| Generic layers | Don't fit codebase | Specialize for your project |
| Assessment without action | No improvement | Prioritize next step |

## Cross-References

- @adw-framework.md - Classification system details
- @agentic-layer-structure.md - Directory structure
- @zte-progression.md - Zero-touch engineering path
- @minimum-viable-agentic skill - Starting point

## Version History

- **v1.0.0** (2026-01-01): Initial release (Lesson 14)

---

## Last Updated

**Date:** 2026-01-01
**Model:** claude-opus-4-5-20251101
