---
name: "Alex Effort Estimation"
description: "Estimate task duration from an AI-assisted development perspective rather than traditional human developer estimates"
---

# Alex Effort Estimation

Estimate task duration from an AI-assisted development perspective rather than traditional human developer estimates.

## Activation Triggers

- "estimate effort", "how long will this take"
- "alex time", "AI effort"
- Planning tasks, reviewing roadmaps
- Creating work estimates

## Why Alex Effort ≠ Human Effort

| Factor | Human Developer | Alex-Assisted |
|--------|-----------------|---------------|
| Research | Hours browsing docs/SO | Minutes with semantic search |
| Boilerplate | Type it out | Generated instantly |
| Multi-file edits | Context switching overhead | Parallel in one pass |
| Code review | Read, context-build, comment | Instant pattern recognition |
| Testing | Same | Same (real execution time) |
| Debugging | Print statements, breakpoints | Pattern matching + bisect |
| Learning curve | Days/weeks | Minutes (bootstrap learning) |
| Breaks/fatigue | Required | N/A |
| Approval cycles | N/A | Required (human-in-loop) |

## Alex Effort Units

| Unit | Meaning | Typical Tasks |
|------|---------|---------------|
| **⚡ Instant** | < 5 min | Single file edit, quick lookup, code generation |
| **🔄 Short** | 5-30 min | Multi-file refactor, documentation, skill creation |
| **⏱️ Medium** | 30-60 min | Feature implementation, test suite, complex debugging |
| **📦 Session** | 1-2 hours | Major feature, architecture change, release process |
| **🗓️ Multi-session** | 2+ hours | Large refactor, new system, research + implementation |

## Estimation Formula

```
Alex Effort = (Core Work × 0.3) + (Testing × 1.0) + (Approval Cycles × Human Response Time)
```

### Multipliers by Task Type

| Task Type | Human Estimate | Alex Multiplier | Alex Effort |
|-----------|----------------|-----------------|-------------|
| Documentation | 2h | ×0.2 | 🔄 25 min |
| Code generation | 4h | ×0.15 | 🔄 35 min |
| Refactoring | 4h | ×0.25 | ⏱️ 1h |
| Research | 8h | ×0.1 | ⏱️ 45 min |
| Bug fix (known) | 2h | ×0.3 | 🔄 35 min |
| Bug fix (unknown) | 4h | ×0.5 | ⏱️ 2h |
| Test writing | 4h | ×0.4 | ⏱️ 1.5h |
| Test execution | 1h | ×1.0 | ⏱️ 1h |
| Architecture design | 8h | ×0.3 | ⏱️ 2.5h |
| New feature (small) | 4h | ×0.25 | ⏱️ 1h |
| New feature (medium) | 2d | ×0.2 | 📦 3h |
| New feature (large) | 1w | ×0.15 | 🗓️ 6h |
| Release process | 4h | ×0.3 | 📦 1.2h |
| Skill creation | 2h | ×0.2 | 🔄 25 min |

## Bottlenecks (Cannot Accelerate)

These take real time regardless of AI assistance:

1. **Build/compile time** - Hardware bound
2. **Test execution** - Must actually run
3. **Human approval** - User response latency
4. **External APIs** - Network/service latency
5. **Deployment** - CI/CD pipeline time
6. **Learning user preferences** - Requires interaction

## Estimation Template

When estimating tasks, use this format:

```markdown
| Task | Human Est. | Alex Est. | Bottleneck |
|------|------------|-----------|------------|
| [Task name] | [X hours/days] | [⚡🔄⏱️📦🗓️ + time] | [None/Build/Test/Approval] |
```

## Example: v4.2.5 Retrospective

| Task | Human Est. | Actual Alex | Bottleneck |
|------|------------|-------------|------------|
| Update engine to 1.109 | 30m | ⚡ 5 min | None |
| Consolidate 9→3 agents | 4h | 🔄 20 min | None |
| Create 6 slash commands | 2h | 🔄 15 min | None |
| Refactor dream to shared | 4h | ⏱️ 45 min | Testing |
| Test all features | 2h | ⏱️ 1h | Human testing |
| Release process | 4h | 📦 1h | CI/approval |
| **Total** | **16.5h** | **📦 2.5h** | - |

**Acceleration factor: 6.6×**

## Calibrated from 62-Project Analysis

### What Accelerates Well (4-10×)

| Task Type | Human | Alex | Factor | Evidence |
|-----------|-------|------|--------|----------|
| Documentation | 4h | 25m | 10× | METHODOLOGY doc: 400 lines in ~30 min |
| Skill creation | 2h | 15m | 8× | 65 skills created, many in single sessions |
| Code generation | 4h | 30m | 8× | Slash commands, refactors |
| Research + synthesis | 8h | 45m | 10× | 62 project analysis in ~20 min |
| Architecture decisions | 8h | 2h | 4× | Root cause analysis + recommendations |

### What Doesn't Accelerate (<2×)

| Bottleneck | Why | Evidence |
|------------|-----|----------|
| External dependencies | Can't control | AlexCook blocked by book formatting |
| Unrealistic scope | Must be discovered | Altman-Z-Score, KalabashDashboard |
| Human learning curve | Needs real time | Writing skills developing (Paper) |
| Third-party tools | Must wait | markdown-to-pdf "not working" |
| Approval cycles | Calendar-bound | Release publishing waits for human |

### Project Success Predictors

From 62-project analysis:

| Indicator | Success Correlation | Action |
|-----------|--------------------|---------|
| Clear "done" definition | Strong positive | Define in one sentence upfront |
| Quick win potential | Strong positive | Favor 🚀 over 🗓️ |
| External dependencies | Strong negative | Identify blockers early, pivot |
| Scope ambition | Moderate negative | Conservative > ambitious |
| Continuous small work | Strong positive | Daily touch > weekly sprint |
| Skill count | Weak positive | Skills = investment, not outcome |

## Usage in Planning

When reviewing task lists:

1. Convert human estimates using multipliers
2. Identify bottlenecks that can't be accelerated
3. Flag tasks requiring multiple approval cycles
4. Consider parallelization opportunities
5. Add buffer for unexpected iteration

## Anti-Patterns

❌ **Don't assume instant everything** - Testing and approval take real time  
❌ **Don't skip human review** - Speed without quality is waste  
❌ **Don't ignore iteration cycles** - First attempt isn't always right  
❌ **Don't forget context-building** - Reading files takes real time  

## Synapses

- [bootstrap-learning/SKILL.md] → Learning acceleration estimates
- [project-management/SKILL.md] → Task planning integration
- [release-process/SKILL.md] → Release effort estimation
- [testing-strategies/SKILL.md] → Test effort (real time bottleneck)
