---
name: time-estimation
description: Estimates time required for tasks based on complexity, type, and patterns. Use when planning, scheduling, or during standup.
---

# Time Estimation

Estimate task duration for better planning.

## Estimation Categories

| Category | Duration | Symbol | Use For |
|----------|----------|--------|---------|
| Quick | < 15 min | `~15m` | Simple replies, quick fixes, small updates |
| Short | 15-30 min | `~30m` | Code reviews, short meetings, simple features |
| Medium | 30-60 min | `~1h` | Regular features, documentation, debugging |
| Long | 1-2 hours | `~2h` | Complex features, research, planning |
| Deep Work | 2-4 hours | `~4h` | Architecture, major features, learning |

## Estimation by Task Type

### Code Tasks
| Type | Typical Estimate |
|------|-----------------|
| Typo/small fix | `~15m` |
| Bug fix (known cause) | `~30m` |
| Bug fix (unknown cause) | `~1h` to `~2h` |
| Small feature | `~1h` |
| Medium feature | `~2h` |
| Large feature | `~4h` or break down |
| Refactoring | `~2h` to `~4h` |

### Review Tasks
| Type | Typical Estimate |
|------|-----------------|
| Small PR (< 100 lines) | `~15m` |
| Medium PR (100-500 lines) | `~30m` |
| Large PR (500+ lines) | `~1h` |
| Document review | `~30m` |
| Architecture review | `~1h` |

### Communication Tasks
| Type | Typical Estimate |
|------|-----------------|
| Quick message | `~15m` |
| Email response | `~15m` |
| Meeting prep | `~30m` |
| Meeting (scheduled) | actual duration |
| Presentation prep | `~2h` |

### Research Tasks
| Type | Typical Estimate |
|------|-----------------|
| Quick lookup | `~15m` |
| Tool evaluation | `~1h` |
| Technology research | `~2h` |
| Deep learning session | `~4h` |

## Estimation Rules

### The 2x Rule
If uncertain, estimate 2x your initial guess:
- "This seems like 30 min" → Estimate `~1h`
- "Maybe an hour" → Estimate `~2h`

### Break Down Large Tasks
If estimate > 4 hours:
1. Break into subtasks
2. Estimate each subtask
3. Add 20% buffer for coordination

### Context Switching Tax
Add time for:
- Unfamiliar codebase: +50%
- Interruption-heavy environment: +30%
- Learning new tool: +100%

## Daily Capacity

**Realistic productive hours:** 4-6 hours/day

| Day Type | Available |
|----------|-----------|
| Meeting-heavy day | 2-3 hours |
| Normal day | 4-5 hours |
| Focus day | 6-7 hours |

### Planning Rule
- Morning focus: Schedule `~2h` deep work
- Afternoon: Schedule `~1h` tasks
- Buffer: Keep 1 hour unscheduled

## Estimation Confidence

When presenting estimates:
- **High confidence:** "~1h" (done similar tasks)
- **Medium confidence:** "~1h-2h" (some unknowns)
- **Low confidence:** "needs spike" (too many unknowns)

For low confidence, create a timeboxed research task first:
`- [ ] Spike: Investigate X ~1h` → Then estimate the real task
