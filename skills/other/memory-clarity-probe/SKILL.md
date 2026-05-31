---
name: memory-clarity-probe
description: >
  Probe memory/summary clarity via dual anchor questions: task progress,
  info gaps. Use when verifying session state or summary before handoff
  or compression.
alwaysApply: false
category: quality-assessment
tags:
  - memory-quality
  - anchor-questions
  - session-management
  - context-clarity
dependencies:
  - memory-palace:session-palace-builder
scripts: []
usage_patterns:
  - pre-handoff-verification
  - session-checkpoint
  - summary-quality-gate
  - best-of-n-selection
complexity: simple
model_hint: standard
estimated_tokens: 600
---

## Table of Contents

- [What It Is](#what-it-is)
- [The Dual-Probe Pattern](#the-dual-probe-pattern)
- [What This Is NOT](#what-this-is-not)
- [When to Use](#when-to-use)
- [Core Workflow](#core-workflow)
- [Best-of-N Mode](#best-of-n-mode)
- [Output Format](#output-format)
- [Integration Points](#integration-points)
- [Exit Criteria](#exit-criteria)


# Memory Clarity Probe

Assess whether a memory, summary, or session state retains enough
task information to guide future reasoning.

## What It Is

A quality gate for any memory or summary, based on the dual-probe
pattern from MMPO (arXiv:2605.30159, Liu et al. 2026). The probe
asks two anchor questions against the current memory and evaluates
whether the answers are confident and complete:

1. **Progress probe**: "Based on current memory, what is the
   current task progress?"
2. **Gap probe**: "Based on current memory, what information is
   still needed?"

A clear memory answers the progress probe with specific, verifiable
state (not vague placeholders) and enumerates bounded, concrete
unknowns on the gap probe. An ambiguous memory produces hedging on
the progress probe and open-ended uncertainty on the gap probe.

## The Dual-Probe Pattern

The two probes target different failure modes:

- **Confident-wrong**: the model has a wrong but confident belief
  about task state. The gap probe alone misses this. The model
  claims it has enough. The progress probe catches it: if the
  stated progress contradicts known facts, the memory has drifted.
- **Uncertain-incomplete**: the model is uncertain about where the
  task stands. Both probes surface this: the progress answer hedges
  and the gap answer lists open-ended unknowns.

The MMPO paper's ablation (Table 4) shows `progress+gap` outperforms
`gap-only` across all context lengths. Use both probes.

## What This Is NOT

This skill implements a **qualitative** clarity assessment. It does
not compute the token-level predictive entropy (Belief Entropy,
Eq. 5 in MMPO) that the paper uses for RL training. Night-market
has no access to the model's internal log-probabilities.

The paper's Table 6 shows that qualitative probing (labeled
"direct-answer entropy", r=0.54) is weaker than true entropy
(r=0.68), and can encourage premature confidence. Use this probe
as a necessary quality check, not a sufficient one.

## When to Use

- Before `conserve:clear-context` hands off to a continuation agent
- At session checkpoints in `memory-palace:session-palace-builder`
- Before committing a summary to a knowledge palace via
  `memory-palace:knowledge-intake`
- Before `imbue:proof-of-work` declares work complete
- When evaluating multiple candidate summaries (Best-of-N mode)

## When NOT to Use

- As a substitute for actually reading the task requirements
- To validate factual correctness (the probe tests clarity, not truth)
- When the memory is trivially short (under 100 tokens: read it)

## Core Workflow

### Step 1: Receive the memory

Accept the memory or summary as input. Sources:
- The current session-state.md (from clear-context)
- A palace room's content (from session-palace-builder)
- A knowledge digest (from knowledge-intake)
- Inline text provided by the caller

### Step 2: Ask the progress probe

Evaluate the memory against:

```
Based on the memory below, what is the current task progress?
Describe specifically what has been completed and what state
the task is in right now.

<memory>
{memory_content}
</memory>
```

Score the answer:
- **Clear**: specific completed steps, concrete current state,
  no hedging ("I think", "probably", "it seems")
- **Ambiguous**: some specifics but with hedging or gaps
- **Unclear**: vague ("some work was done"), generic, or empty

### Step 3: Ask the gap probe

Evaluate the memory against:

```
Based on the memory below, what information is still needed
to complete the task? List specific open questions or missing
facts, not generic categories.

<memory>
{memory_content}
</memory>
```

Score the answer:
- **Bounded**: finite list of specific missing items
- **Expanding**: generic categories or open-ended unknowns
  (signals the memory does not constrain what's missing)
- **Overconfident**: claims nothing is needed, but the task is
  incomplete (premature confidence, the failure mode the
  progress probe guards against)

### Step 4: Compute composite score

| Progress | Gap | Composite | Action |
|----------|-----|-----------|--------|
| Clear | Bounded | **Clear** | Proceed |
| Clear | Expanding | **Ambiguous** | Consider expanding memory |
| Clear | Overconfident | **Suspect** | Re-read task requirements |
| Ambiguous | Bounded | **Ambiguous** | Expand memory or ask user |
| Ambiguous | Expanding | **Unclear** | Regenerate or expand memory |
| Unclear | Any | **Unclear** | Memory must be regenerated |

### Step 5: Report

Produce the output in the format below and take the recommended
action if invoked as an autonomous gate.

## Best-of-N Mode

When evaluating N candidate summaries (e.g., from multiple
summarization attempts):

1. Apply the dual probe to each candidate.
2. Rank by: (a) composite score, (b) specificity of gap
   enumeration, (c) absence of hedging in progress answer.
3. Recommend the top-ranked candidate.
4. Report all scores so the caller can verify.

To generate N candidates, invoke a summarization skill N times with
varied prompts or temperatures, then pass all results to this probe.
Typical N=3 gives a useful signal; N=5 matches the paper's Best-of-5
finding (Figure 3c).

## Output Format

```
## Clarity Assessment

**Progress probe**: [Clear | Ambiguous | Unclear]
> {exact answer the model produced}

**Gap probe**: [Bounded | Expanding | Overconfident]
> {exact answer the model produced}

**Composite**: [Clear | Ambiguous | Suspect | Unclear]

**Recommendation**: [Proceed | Expand memory | Regenerate]

**Specific issues** (if composite is not Clear):
- {issue 1}
- {issue 2}
```

## Integration Points

**As a pre-handoff gate** (conserve:clear-context):
```
Before saving session-state.md, invoke memory-clarity-probe
on the draft state. If composite is Unclear, expand the state
with explicit answers to both probes before saving.
```

**As a session checkpoint** (memory-palace:session-palace-builder):
```
At major task transitions (design complete, implementation
started, tests passing), invoke memory-clarity-probe on the
current palace state. Log the composite score.
```

**As a completion check** (imbue:proof-of-work):
```
Before declaring work complete, invoke memory-clarity-probe.
The progress probe should return Clear with all deliverables
named. The gap probe should return Bounded with zero open items.
```

## Exit Criteria

- [ ] Skill invoked on a clear, specific summary returns
  composite "Clear" with both probes scoring positively
- [ ] Skill invoked on a vague one-sentence summary returns
  composite "Unclear" and recommends regeneration
- [ ] Skill invoked in Best-of-N mode on 3 candidates ranks
  them and names the recommended one
- [ ] Output matches the defined format with progress probe
  and gap probe scores both present
- [ ] Documentation of qualitative limitation vs logprob
  entropy is present and accurate (What This Is NOT section)
- [ ] Skill registered in plugin metadata
