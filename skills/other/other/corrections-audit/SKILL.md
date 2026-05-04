---
name: corrections-audit
description: "Use to analyze correction trends, surface recurring patterns, and graduate repeat corrections to guardrails or anti-patterns."
instruction_budget: 40
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
   - If ai-generated corrections dominate (>60%): flag for prompt/context improvement, BUT see `detection_origin` cross-check below before acting on this interpretation
   - If human-written corrections dominate (>60%): flag for process/training improvement
   - If ai-assisted is high: check if the AI contribution or the human contribution caused the issue

4b. **Cross-check with detection_origin** (when field is present — see memory/README.md):
   - Count corrections by `Detection_origin` if present (user / agent_self / hook / evaluator / eval_runner / external_review)
   - **Critical disambiguation**: if Origin is heavily ai-generated AND detection_origin is heavily `user`, the apparent AI-quality signal is actually a HARNESS-DETECTION GAP. The AI is generating failures and the user is the only entity catching them. The right intervention is more harness checks (hooks, evaluators), NOT more AI context.
   - If detection_origin is dominantly `user` (>70%): flag for harness-detection gap. Suggest where new hooks or evaluators could catch the failure modes earlier.
   - If detection_origin is well-distributed across mechanisms: harness coverage is healthy; trust the Origin signal at face value.
   - Surfaced 2026-05-03 (mycelium-roadmap dogfood): without this cross-check, the audit's "100% ai-generated → improve prompt context" framing would have driven the wrong intervention. Real signal was "AI generates, user catches" — fixed by shipping the framework-guard hook (harness-detection layer), not by improving prompts.

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

7. **Consolidate memory files** (automated hygiene):
   - **Deduplication**: Identify corrections that describe the same root cause in different words. Merge into a single entry, preserving all dates and evidence.
   - **Contradiction detection**: Flag corrections that contradict each other (e.g., "always use X" vs "never use X"). Present conflicts to the user for resolution.
   - **Staleness removal**: Corrections older than 6 months whose prevention has been verified effective (no recurrence) can be archived to `memory/corrections-archive.md`.
   - **Size cap**: If corrections.md exceeds 50 entries, consolidate the oldest resolved entries into a summary paragraph in the archive.
   - Apply the same consolidation to `memory/patterns.md`.
   *Inspired by: greyhaven-ai/autocontext curator agent — periodic dedup, cap, and contradiction removal.*

8. **Update TL;DR section**:
   - Regenerate the TL;DR in corrections.md with the top 5 most impactful corrections
   - Impact = frequency x severity (blocking vs. quality vs. cosmetic)

9. **Recommend actions**:
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
