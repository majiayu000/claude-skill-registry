---
name: cost-estimation
description: Guidelines for estimating token usage and costs per task and phase. Reference this skill when planning to provide accurate budget estimates.
---

// Project Autopilot - Cost Estimation Guidelines
// Copyright (c) 2026 Jeremy McSpadden <jeremy@fluxlabs.net>

# Cost Estimation Skill

Reference this skill when creating phases to provide accurate token/cost estimates.

---

## Task Cost Estimates

### By Task Type

| Task Type | Input Tokens | Output Tokens | Est. Cost (Sonnet) |
|-----------|--------------|---------------|-------------------|
| Read/analyze file | 500-2,000 | 200-500 | $0.002-0.01 |
| Create new file | 1,000-3,000 | 1,500-5,000 | $0.01-0.03 |
| Modify existing file | 1,500-4,000 | 1,000-3,000 | $0.01-0.025 |
| Write unit tests | 2,000-5,000 | 2,000-6,000 | $0.015-0.045 |
| Write integration tests | 3,000-8,000 | 3,000-8,000 | $0.025-0.06 |
| Code review | 2,000-6,000 | 1,000-3,000 | $0.01-0.03 |
| Documentation | 1,000-3,000 | 1,500-4,000 | $0.01-0.025 |
| Debug/fix | 3,000-10,000 | 2,000-5,000 | $0.02-0.05 |
| Schema design | 1,500-4,000 | 2,000-5,000 | $0.015-0.035 |
| API endpoint | 2,000-5,000 | 2,500-6,000 | $0.02-0.045 |
| React component | 2,000-6,000 | 3,000-8,000 | $0.025-0.055 |
| Configuration | 500-1,500 | 500-1,500 | $0.003-0.01 |

### By Complexity

| Complexity | Multiplier | Example |
|------------|------------|---------|
| Simple | 1.0x | Add config value, simple function |
| Medium | 1.5x | New endpoint with validation |
| Complex | 2.5x | Auth system, complex logic |
| Very Complex | 4.0x | Multi-service integration |

---

## Phase Cost Estimates

### Typical Phase Costs (Sonnet)

| Phase | Tasks | Est. Tokens | Est. Cost |
|-------|-------|-------------|-----------|
| 001 Setup | 3-5 | 15K-30K | $0.08-0.20 |
| 002 Database | 4-6 | 25K-50K | $0.15-0.35 |
| 003 Infrastructure | 4-6 | 20K-40K | $0.12-0.28 |
| 004 Auth | 5-8 | 40K-80K | $0.25-0.55 |
| 005 API | 6-12 | 50K-120K | $0.35-0.85 |
| 006 Business Logic | 6-15 | 60K-150K | $0.40-1.00 |
| 007 Frontend | 8-15 | 80K-180K | $0.55-1.25 |
| 008 Features | 10-25 | 100K-300K | $0.70-2.00 |
| 009 Testing | 6-12 | 50K-120K | $0.35-0.85 |
| 010 Security | 4-8 | 30K-70K | $0.20-0.50 |
| 011 Documentation | 4-8 | 30K-60K | $0.20-0.40 |
| 012 DevOps | 5-10 | 40K-90K | $0.28-0.60 |
| 013 Polish | 3-8 | 25K-60K | $0.15-0.40 |

**Total Typical Project:** 400K-1.5M tokens, $2.50-$10.00

---

## Estimation Formula

### Per Task

```
Base Cost = (input_tokens × input_rate) + (output_tokens × output_rate)

Haiku:  input_rate = $1/1M,  output_rate = $5/1M
Sonnet: input_rate = $3/1M,  output_rate = $15/1M
Opus:   input_rate = $5/1M,  output_rate = $25/1M

Adjusted Cost = Base Cost × Complexity Multiplier × Buffer (1.2)
```

### Per Phase

```
Phase Estimate = Σ(Task Estimates) × Phase Buffer (1.15)
```

### Buffer Factors

| Factor | Buffer | Reason |
|--------|--------|--------|
| Task | 1.2x | Retries, validation |
| Phase | 1.15x | Integration, fixes |
| Project | 1.25x | Unknowns, scope creep |

---

## Confidence Levels

| Level | Variance | When to Use |
|-------|----------|-------------|
| High | ±15% | Well-defined, done before |
| Medium | ±30% | Clear scope, some unknowns |
| Low | ±50% | Vague requirements, new tech |

---

## Estimation Checklist

Before finalizing phase estimates:

- [ ] Each task has complexity rating
- [ ] Model specified (Opus vs Sonnet)
- [ ] Buffer applied (1.2x task, 1.15x phase)
- [ ] Confidence level stated
- [ ] Range provided (min-max)
- [ ] Total phase estimate calculated
- [ ] Fits within project budget
