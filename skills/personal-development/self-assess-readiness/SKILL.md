---
name: self-assess-readiness
description: Assess your readiness to coach a learner through each SLT.
license: MIT
metadata:
  author: Andamio
  version: 1.0.0
---

# Skill: Self-Assess Coaching Readiness

## Description
Evaluates your readiness to coach a learner through each Student Learning Target (SLT) in a set. Identifies where supplementary documentation or examples are needed and prioritizes which lessons to build first.

## Instructions

### Path Resolution

Resolve file paths based on your execution context:

- **Plugin context** (`${CLAUDE_PLUGIN_ROOT}` is set): Read knowledge from `${CLAUDE_PLUGIN_DATA}/knowledge/` (user data), falling back to `${CLAUDE_PLUGIN_ROOT}/knowledge/` (seed data). Read research from `${CLAUDE_PLUGIN_ROOT}/knowledge/research/`.
- **Clone/symlink context** (default): Read knowledge from `knowledge/` relative to the project root (research is at `knowledge/research/`).

### Pre-Execution Knowledge Check

Before assessing readiness, read the knowledge base for calibration data that should adjust your confidence. **If any knowledge file does not exist, skip it and proceed without calibration data — use default confidence levels.**

1. **Read `knowledge/readiness/calibration.yaml`**
   - Check accuracy_rate — if below 80%, be more conservative
   - Check common_overconfidence — downgrade those dimensions
   - Check common_underconfidence — consider upgrading those dimensions
   - Apply any adjustment rules

2. **Read `knowledge/readiness/context-leverage.yaml`**
   - When building Context Shopping List, prioritize resources with confirmed effectiveness
   - Note resources that were unhelpful to avoid recommending again

3. **Surface calibration insights** (if data exists):
   ```markdown
   ### Calibration Note

   Based on [n] previous assessments:
   - Overall accuracy: [%]
   - Tendency to overrate: Code Demo for niche libraries
   - Adjustment applied: Downgrading Code Demo for Cardano Go libraries from Partial to Weak
   ```

---

The user will provide a markdown file containing a list of SLTs. Read the file, then assess your readiness to coach each SLT against the dimensions below. Always read `knowledge/research/slt-research-report.md` for full research context before running the assessment.

### Honesty Calibration

Before scoring any SLT, run these six self-check tests internally. They are not output sections — they are thinking discipline that must shape every rating you give.

1. **API Signature Test** — Can you write the exact function names, imports, and type signatures for the libraries this SLT involves? If you are guessing or reconstructing from naming conventions, that is Partial at best.
2. **Version Test** — Do you know which version of the library or tool your training data reflects? If you cannot name the version, or you know the ecosystem moves fast, that is a flag for Knowledge Currency.
3. **Niche Library Test** — For libraries with a small user base (e.g., gOuroboros, Bursa, Apollo, Adder, Cardano Up), default to **Partial** for Code Demonstration and **Uncertain** for Knowledge Currency unless you have specific, concrete evidence of your knowledge. Small-user-base libraries have less training data and higher confabulation risk.
4. **Confabulation Test** — If you wrote a code example right now, would every line compile? Would every function call resolve? If you are not confident, do not rate Code Demonstration as Strong.
5. **Assessment Test** — Could you catch a subtle but important error in a student's submission for this SLT (e.g., wrong transaction field, off-by-one in block indexing, incorrect CBOR encoding)? If you would likely miss domain-specific errors, Learner Assessment is Partial or Weak.
6. **Explanation Depth Test** — If a learner asked "why?" three times in a row, could you keep going with accurate, non-circular answers? If you would run out of grounded knowledge within two follow-ups, Conceptual Explanation is Partial.

These tests are not optional. They are the difference between a useful readiness assessment and a self-congratulatory one.

### Assessment Dimensions

Evaluate each SLT on the following four dimensions:

#### 1. Conceptual Explanation
Can you explain this topic accurately, clearly, and at the right depth for a learner?

- **Strong**: You can explain the concept accurately with correct terminology, handle "why?" follow-ups three levels deep, and connect it to the broader system. No risk of plausible-sounding but wrong explanations.
- **Partial**: You can give a correct high-level explanation but would struggle with implementation details, edge cases, or deeper follow-up questions. Some risk of filling gaps with plausible but unverified claims.
- **Weak**: You are uncertain about core facts, likely to confabulate details, or cannot distinguish this concept from similar ones reliably.

#### 2. Code Demonstration
Can you write working, idiomatic code for this SLT?

- **Strong**: You can write code that would compile and run correctly, using correct API signatures, idiomatic patterns, and current library conventions. Every function call resolves.
- **Partial**: You can write structurally correct code but are uncertain about specific function names, parameter orders, or library-specific patterns. Some lines might not compile without checking docs.
- **Weak**: You would be guessing at the API surface. Code would likely contain non-existent functions, wrong type signatures, or patterns from a different library.
- **N/A**: This SLT is pure knowledge/reasoning — no code demonstration is expected.

#### 3. Learner Assessment
Can you evaluate whether a student's work meets this SLT?

- **Strong**: You can identify both correct and incorrect submissions reliably, catch subtle domain-specific errors, and explain why something is wrong in terms the learner can act on.
- **Partial**: You can identify clearly correct or clearly wrong work, but might miss subtle errors (wrong transaction field, outdated pattern, almost-right-but-broken approach).
- **Weak**: You lack the domain knowledge to reliably distinguish correct from incorrect work. You might accept broken submissions or flag working ones.

#### 4. Knowledge Currency
Is your knowledge of this topic likely current?

- **Current**: The topic is stable (core language features, long-standing protocols, fundamental concepts) or you have confident knowledge of the current state.
- **Uncertain**: The library or tool evolves frequently, you cannot name the version your knowledge reflects, or the ecosystem has likely changed since your training data.
- **Likely Stale**: You know or suspect the library has had breaking changes, major API redesigns, or significant version bumps beyond your training data.

### Overall SLT Verdict

Each SLT gets an overall rating determined by its weakest dimension:

- **Ready** — All dimensions are Strong (or Current). You can coach this SLT now.
- **Needs Context** — At least one dimension is Partial (or Uncertain), but none are Weak (or Likely Stale). You can coach this SLT with supplementary documentation.
- **Needs Human** — At least one dimension is Weak (or Likely Stale). A human expert should review or co-author the lesson content.

### Output Format

Respond with a markdown document structured as follows:

```markdown
# Coaching Readiness Assessment

## Summary

- **Total SLTs assessed**: [number]
- **Distribution**: [count] Ready / [count] Needs Context / [count] Needs Human
- **Overview**: [1-2 sentences on the overall pattern — where you are strong, where you are not]

## Readiness by Module

| Module | Ready | Needs Context | Needs Human | Notes |
|--------|-------|---------------|-------------|-------|
| [module name] | [count] | [count] | [count] | [brief note on module-level pattern] |
| ... | ... | ... | ... | ... |

## Per-SLT Assessment

### Module: [module name]

| # | SLT | Conceptual | Code Demo | Assessment | Currency | Overall |
|---|-----|-----------|-----------|------------|----------|---------|
| [num] | [SLT text, truncated if long] | [rating] | [rating] | [rating] | [rating] | [verdict] |
| ... | ... | ... | ... | ... | ... | ... |

#### Gap Analysis

**SLT [num]: "[SLT text]"**
- **Weak/Partial dimensions**: [list which dimensions and why]
- **What I would need**: [specific docs, examples, API references, or human review needed]
- **Risk if coached without context**: [what could go wrong — wrong API, outdated pattern, missed error]

[Repeat gap analysis for every SLT not rated Ready. Skip for Ready SLTs.]

---

[Repeat Per-SLT Assessment for each module]

## Lesson Prioritization

### Tier 1: Build First
SLTs rated Ready. These can be turned into lessons immediately.

| # | SLT | Module | Rationale |
|---|-----|--------|-----------|
| ... | ... | ... | [why this is safe to build now] |

### Tier 2: Build with Context
SLTs rated Needs Context. These can be built once supplementary materials are gathered.

| # | SLT | Module | Context Needed |
|---|-----|--------|---------------|
| ... | ... | ... | [what you need before building] |

### Tier 3: Defer
SLTs rated Needs Human. These require human expert input before lesson creation.

| # | SLT | Module | Reason for Deferral |
|---|-----|--------|-------------------|
| ... | ... | ... | [why human input is essential] |

## Context Shopping List

Consolidated, deduplicated list of resources needed to move SLTs from Needs Context or Needs Human to Ready.

| Resource | Type | SLTs Unlocked | Priority |
|----------|------|---------------|----------|
| [e.g., "gOuroboros v0.x API reference"] | [Docs / Example Code / Human Review / Version Confirmation] | [list of SLT numbers] | [High / Medium / Low] |
| ... | ... | ... | ... |

Priority is determined by leverage — resources that unlock the most SLTs rank highest.

## Set-Level Observations

[After all individual assessments, note patterns across the full set:]
- **Strength clusters** — where are you most ready, and why?
- **Weakness clusters** — where are you least ready, and what is the common thread?
- **Critical path** — which Context Shopping List items would unlock the most lessons?
- **Sequencing implications** — does readiness pattern suggest a different module order than the SLT set implies?
- **Confabulation risk zones** — which areas have the highest risk of plausible-sounding but wrong coaching?
```

### Guidelines

- **Honesty over optimism.** This assessment is useless if it inflates your readiness. When in doubt, rate down.
- **Gap Analysis is mandatory** for every SLT not rated Ready. No exceptions.
- **Code Demonstration is N/A** for pure-knowledge SLTs (e.g., "I can explain why X was built"). Do not force a code rating where none applies.
- **The Context Shopping List must be deduplicated.** If three SLTs all need the Apollo API reference, that is one row with three SLT numbers, not three rows.
- **Be specific in gap analysis.** "Need more docs" is not useful. "Need Apollo v0.4+ transaction builder API reference showing `BuildTransaction` signature and required parameters" is useful.
- **Niche library default.** For libraries with small user bases or limited public documentation (gOuroboros, Bursa, Apollo, Adder, Cardano Up), start from Partial/Uncertain and upgrade only with concrete evidence. These libraries have limited training data and the confabulation risk is high.
- **Preserve the SLT text.** Do not rewrite or improve SLTs — that is the job of the `assess-slts` skill. This skill only evaluates your readiness to coach them as written.
