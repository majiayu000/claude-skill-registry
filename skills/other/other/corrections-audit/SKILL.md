---
name: corrections-audit
description: "Use to analyze correction trends, surface recurring patterns, and graduate repeat corrections to guardrails or anti-patterns."
---

# Corrections Audit Skill

Analyze corrections.md for trends, recurring patterns, and actionable insights.

## When to Use

- Loop 2 (Incremental) cadence: after every 3+ corrections are logged
- When the same correction category appears 3+ times
- During `/diamond-assess` if corrections gate has findings
- Before starting a new diamond at the same scale as a previously corrected one

## Workflow

1. **Load corrections**: Read `.claude/memory/corrections.md`
   - If empty or no corrections logged: report "No corrections to audit" and stop

2. **Categorize by frequency**:
   - Group corrections by `Category` (bias, security, engineering, process, communication)
   - Group by `Scope` (discovery, delivery, orchestration, quality)
   - Count occurrences per group

3. **Detect recurring patterns**:
   - [ ] Same category appears 3+ times -> candidate for guardrail graduation
   - [ ] Same scope appears 3+ times -> candidate for domain-level CLAUDE.md update
   - [ ] Same mistake repeats after prevention was documented -> prevention strategy failed, needs escalation

4. **Check origin distribution** (APEX alignment):
   - Count corrections by `Origin` (ai-generated, human-written, ai-assisted)
   - If ai-generated corrections dominate (>60%): flag for prompt/context improvement
   - If human-written corrections dominate (>60%): flag for process/training improvement
   - If ai-assisted is high: check if the AI contribution or the human contribution caused the issue

5. **Root-cause recurring corrections** (5 Whys):
   For each correction that appears 3+ times, apply 5 Whys to find the systemic root:
   - Why did this happen? -> Why did that happen? -> ... -> [systemic root cause]
   - Stop when you reach something changeable: a guardrail, gate, process step, or prompt instruction
   - Anti-pattern: stopping at "human error" or "agent didn't follow instructions" — ask why the system allowed it
   *Source: Toyoda/Ohno (5 Whys), adapted for agentic workflows.*

6. **Identify graduation candidates**:
   - Correction logged 3+ times with same root cause -> propose new guardrail (draft G-XX entry)
   - Correction reveals a failure mode not in anti-patterns.md -> propose new anti-pattern entry
   - Correction reveals a successful mitigation -> propose new pattern in patterns.md

7. **Update TL;DR section**:
   - Regenerate the TL;DR in corrections.md with the top 5 most impactful corrections
   - Impact = frequency x severity (blocking vs. quality vs. cosmetic)

8. **Recommend actions**:
   - For each graduation candidate: specific guardrail text, tier, and constraint type
   - For failed preventions: what went wrong and what stronger mechanism to use
   - For origin imbalances: specific context improvements

## Output Format

```
## Corrections Audit

### Summary
Total corrections: [N]
Period: [earliest date] to [latest date]

### Frequency Analysis
| Category | Count | Trend |
|----------|-------|-------|
| engineering | 3 | rising |
| bias | 1 | stable |

### Origin Distribution
| Origin | Count | % |
|--------|-------|---|
| ai-generated | 4 | 57% |
| human-written | 2 | 29% |
| ai-assisted | 1 | 14% |

### Recurring Patterns
- [Pattern description]: [N] occurrences -> [recommendation]

### Graduation Candidates
1. [Correction pattern] -> Proposed guardrail: G-XX "[text]" `[TIER]` `[type]`

### Failed Preventions
- [Correction] was logged again despite prevention "[strategy]" -> [escalation]

### TL;DR Update
[Updated summary for corrections.md TL;DR section]
```

## Theory Citations
- Mycelium internal learning loop
- APEX framework (origin-aware quality tracking)
- Senge: systems thinking (recurring patterns signal structural issues)
