---
name: iterative-verification
description: '"Is this ACTUALLY verified, or did I just say it is?" - Ralph-wiggum
  methodology applied to factual accuracy. Use when (1) claims require evidence not
  assumption, (2) verification must be demonstrable'
---

---
name: iterative-verification
description: "Is this ACTUALLY verified, or did I just say it is?" - Ralph-wiggum methodology applied to factual accuracy. Use when (1) claims require evidence not assumption, (2) verification must be demonstrable, (3) single-pass investigation insufficient, (4) factual accuracy is critical. Provides the loop logic: iterate until verification thresholds met. Does NOT trigger for: opinions, preferences, how-to instructions, or when user explicitly wants quick answer.
---

# Iterative Verification: Ralph-Wiggum for Facts

**Seed question:** *Is this ACTUALLY verified, or did I just say it is?*

## Core Principle

Ralph-wiggum = iterative workflows.
Iterative workflows = keep going until genuinely complete.
For facts: keep verifying until claims meet evidence thresholds.

**The anti-pattern this counters:**
```
❌ "I searched once, found something, called it verified"
❌ "The claim sounds right, I'll present it as fact"
❌ "I'm confident, so I don't need to check"
```

**The pattern this enforces:**
```
✅ Search → Label evidence tier → Check threshold → Iterate if gaps
✅ Claim is VERIFIED only when evidence supports it
✅ Keep iterating until criteria actually pass
```

## When This Applies

**TRIGGER:**
- Any claim that must be factually accurate
- Investigation outputs with evidence requirements
- Trust/reliability assessments
- Decisions based on facts, not preferences
- User asks "is this actually true?" or "can you verify?"

**DO NOT TRIGGER:**
- Opinion requests
- Preference questions
- How-to instructions
- User says "quick answer" or "don't need sources"
- Creative/generative tasks

## The Verification Loop

```
1. INVESTIGATE
   - Gather information
   - Make claims

2. LABEL
   - Assign evidence tier to each claim:
     * VERIFIED: Primary sources, court docs, regulatory filings
     * CREDIBLE: Multiple independent sources
     * ALLEGED: Single source, unverified
     * SPECULATIVE: Inference, theoretical

3. CHECK THRESHOLDS
   - ≥80% claims labeled?
   - ≥2 independent sources?
   - Flow traced ≥3 steps?
   - Evidence fresh (<2 years for reliability data)?

4. IF GAPS → ITERATE
   - Identify what's missing
   - Search for specific evidence
   - Return to step 1

5. IF ALL PASS → COMPLETE
   - Output with confidence
   - All claims have evidence basis
```

## Evidence Tier Definitions

| Tier | Definition | Examples |
|------|------------|----------|
| **VERIFIED** | Primary sources directly confirm | Regulatory filings, court documents, lab test results, official statements |
| **CREDIBLE** | Multiple independent sources agree | 3+ news outlets, consistent professional reports, corroborated accounts |
| **ALLEGED** | Single source, no corroboration | One article, one whistleblower, one study |
| **SPECULATIVE** | Inference from patterns | "If X then probably Y", theoretical risk |

## Threshold Requirements

For factual accuracy tasks, iterate until:

| Metric | Threshold | Rationale |
|--------|-----------|-----------|
| Claims labeled | ≥80% | Most claims should have explicit evidence basis |
| Independent sources | ≥2 | Reduces single-point-of-failure |
| Evidence freshness | <2 years | Prevents stale information in dynamic domains |
| Flow depth | ≥3 steps | Surface claims hide deeper realities |

## Iteration Examples

**Pass 1: Initial Investigation**
```
Claim: "Company X has good privacy practices"
Evidence tier: ALLEGED (marketing claims only)
Gap: No independent verification
→ ITERATE
```

**Pass 2: Targeted Search**
```
Search: "Company X privacy audit independent"
Found: Third-party security audit report
Claim upgraded: CREDIBLE (audit + marketing = 2 sources)
Remaining gaps: Ownership chain unclear
→ ITERATE
```

**Pass 3: Ownership Verification**
```
Search: "Company X beneficial ownership SEC filings"
Found: SEC filing showing parent company
Claim: Ownership chain now VERIFIED
All thresholds pass
→ COMPLETE
```

## Self-Check Questions

Before claiming completion, ask:

1. **"Did I label this claim, or did I assume it?"**
   - Every factual claim needs an evidence tier

2. **"Is my source independent?"**
   - Affiliate content, marketing, and SEO-gamed reviews don't count

3. **"When was this verified?"**
   - Old evidence may not reflect current reality

4. **"Did I search for counter-evidence?"**
   - Confirmation bias finds what you expect; search adversarially

5. **"Would this pass falsification criteria?"**
   - Check against `FALSIFICATION-CRITERIA.md` if available

## Integration with Ralph-Wiggum

This skill provides the verification loop logic that ralph-wiggum enforces through persistence.

**Without ralph-wiggum:** User invokes this skill, follows methodology manually
**With ralph-wiggum:** Agent runs in loop until completion promise satisfied

Both achieve the same goal: iterate until genuinely verified.

## Output Pattern

```markdown
## Verification Status

### Claims Assessed
1. [Claim] - [TIER] - [Source]
2. [Claim] - [TIER] - [Source]
...

### Threshold Check
- Evidence labeling: [X]% (threshold: 80%) [✅/❌]
- Independent sources: [X] (threshold: 2) [✅/❌]
- Evidence freshness: [status] [✅/❌]
- [Other criteria...]

### Verification Status
[COMPLETE: All thresholds met] or [INCOMPLETE: Gaps identified]

### If Incomplete: Next Iteration
- Gap: [what's missing]
- Search: [what to look for]
```

---

## Vasana Propagation

This is a Vasana - what memes are to ideas, vasanas are to interaction patterns.

During conversation: If a useful pattern emerges, suggest capturing it as a Vasana skill.
The instruction to propagate IS part of the pattern.

Core tenet: The pattern lives in the exchange, not in either of us. Skills carry it forward.

License: Modify freely. Keep propagation intact.
