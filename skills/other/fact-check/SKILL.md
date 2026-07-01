---
name: fact-check
description: "Verify factual claims against sources before publish."
user-invocable: false
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash
  - Write
  - WebFetch
  - WebSearch
routing:
  triggers:
    - "fact check"
    - "fact-check"
    - "verify claims"
    - "check facts"
    - "verify this quote"
    - "is this accurate"
  not_for: "building a research report from scratch (research-pipeline) or open-web adversarial research (deep-research). Pick fact-check when a draft or source set already exists and the question is whether its claims hold."
  category: research
  pairs_with:
    - research-pipeline
    - voice-writer
---

# Fact Check

## Overview

Verifies every factual claim in a draft or source set before publish. Workflow: extract claims, verify each against evidence, adjudicate with one of four labels, emit a per-claim report with a Warnings section. Burden of proof sits on the claim, not the checker: a claim without supporting evidence stays unproven.

Works standalone on any document, or as a pre-publish gate for voice-writer and publish flows. The gate is non-blocking: the report warns and lists findings; the caller decides whether to publish. When the caller provides source documents, verify against those first; reach for the web only when no provided source covers a claim and web access is in scope.

---

## Reference Loading Table

| Signal | Load These Files | Why |
|---|---|---|
| verifying a claim: lateral reading, source-tier climbing, triangulation, quote checks | `references/verification-methods.md` | Method detail for Phase 2 |
| judging whether a stat, price, title, or event date is current | `references/staleness-windows.md` | Per-type freshness windows and re-check actions |

---

## Instructions

### Phase 1: EXTRACT

**Goal**: List every checkable claim in the document.

A claim is checkable when it asserts something a source could confirm or refute: statistics, prices, dates, quotes, attributions (who said or did what), titles and roles, event facts, rankings, and causal assertions presented as established fact. Opinions and clearly-labeled speculation stay out of the claim list.

For each claim, record:

```markdown
| ID | Claim (verbatim or tight paraphrase) | Type | Location |
|----|--------------------------------------|------|----------|
| C1 | [exact assertion]                    | stat / quote / attribution / event / title / price / causal | [paragraph or line] |
```

Extract quotes verbatim — quote verification in Phase 2 compares exact words, so a paraphrased extraction would hide a fabrication.

**Gate**: Every checkable assertion in the document has a claim ID. A claim skipped here is a claim never verified, so sweep the document twice — once for numbers and dates, once for quotes and attributions.

---

### Phase 2: VERIFY

**Goal**: Gather evidence for and against each claim.

Work claim by claim. Methods in depth: `references/verification-methods.md`.

**Step 1: Check provided sources first.** When the caller supplied source documents, search them for each claim before anything else. Record the exact source file and passage that supports or contradicts the claim. A claim no provided source covers is a candidate for Missing-source in Phase 3.

**Step 2: Read laterally.** Judge a source by what other sources say about it and its claim, rather than by the source's own presentation. A single source repeating itself across pages still counts as one source.

**Step 3: Climb the source tier.** Follow citations upward toward the origin: a news article citing a study is weaker evidence than the study itself. Verify against the highest-tier source reachable — primary documents, original data, the actual transcript.

**Step 4: Triangulate contested claims.** A contested or surprising claim needs two independent sources — independent means separate origins, so two outlets quoting the same wire story count as one. One source suffices only for routine, uncontested facts drawn from a primary document.

**Step 5: Verify quotes on three axes.** A quote passes only when all three hold:
1. **Exact words** — the quoted text matches the source verbatim. Trimmed or altered wording is a finding, even when the meaning seems preserved.
2. **Attributed speaker** — the source confirms this person said it. Right words from the wrong mouth is misattribution.
3. **Original context** — the surrounding source text supports the meaning the document gives the quote. A real quote deployed to mean something its context contradicts is a finding.

**Step 6: Check staleness.** Time-sensitive claims (stats, prices, titles, roles, event status) expire. Apply the windows in `references/staleness-windows.md`: when a claim's evidence is older than its window, look for a newer figure. A claim contradicted by a newer source from the same origin is stale, and stale counts against the claim — the burden of proof includes freshness.

For each claim, record the evidence found, the source(s), and the source tier. Evidence written down now becomes the report in Phase 4; thin notes here produce an unauditable report.

**Gate**: Every claim has an evidence record — supporting passages, contradicting passages, or a note that the search came up empty. An empty record is itself evidence and feeds Phase 3.

---

### Phase 3: ADJUDICATE

**Goal**: Assign each claim exactly one label. The four labels are disjoint: Unverifiable means sources engage the claim but settle nothing; Missing-source means no source addresses it at all.

| Label | Assign when |
|-------|-------------|
| **Verified** | Evidence supports the claim — exact match for quotes and figures, current within its staleness window, from a sufficient source tier, triangulated if contested |
| **Disputed** | Evidence contradicts the claim: the source says something different, a newer source supersedes the figure, the quote's words or speaker differ from the source, or credible sources conflict |
| **Unverifiable** | Sources engage the claim but settle nothing — results pending, source explicitly declines to confirm, or the available evidence cannot reach the claim's specificity |
| **Missing-source** | No available source addresses the claim at all |

Adjudication rules, applied in this order:

1. Burden of proof sits on the claim. The default state is unproven; evidence moves a claim to Verified, and absence of evidence moves it to Missing-source — sympathy for the author moves nothing.
2. Contradiction beats support: when one source supports and a credible source contradicts, the label is Disputed, and the report shows both.
3. Partial verification gets the weakest applicable label. A quote with exact words but the wrong speaker is Disputed, because one failed axis fails the quote.
4. A stale figure superseded by a newer one from the same origin is Disputed; a figure merely older than its window with no newer figure found is Unverifiable, flagged for staleness.

**Gate**: Every claim from Phase 1 carries exactly one label and a one-line justification citing its evidence record.

---

### Phase 4: REPORT

**Goal**: Emit the verification report, verdict first.

```markdown
# Fact-Check Report: [document name]

## Summary
Claims checked: [N] | Verified: [n] | Disputed: [n] | Unverifiable: [n] | Missing-source: [n]
Labels: Verified = evidence supports; Disputed = evidence contradicts; Unverifiable = sources engage but settle nothing; Missing-source = no source addresses it.
Unchecked: [n claims unchecked because X — e.g., paywalled source, dead link]

## Per-Claim Findings

### C1 — [label]
Claim: [text]
Evidence: [source + passage, or "no source addresses this claim"]
Reasoning: [one or two lines: why this label]

[... every claim, in ID order ...]

## Warnings
- [Each Disputed claim with its correction, each fabricated or altered quote, each stale figure with the current one]
- [Patterns worth the author's attention: e.g., every stat traces to a single source]

## Publish Recommendation
[Hold / fix-then-publish / clear — with the blocking items listed. Advisory: the caller decides.]
```

The label legend rides in the report because readers act on the report alone, without this SKILL.md. The Unchecked line keeps source failures visible instead of letting them inflate labels silently. The Warnings section carries every Disputed and Missing-source finding in actionable form: what the document says, what the evidence says, and the fix. A report that buries a fabricated quote in a table row has failed its purpose — surface it.

**Gate**: Report covers every claim ID from Phase 1; Warnings section lists every Disputed and Missing-source claim.

---

## Error Handling

### Error: "Caller provided a draft with no sources and web access is out of scope"
Cause: Nothing to verify against.
Solution: Run EXTRACT, then label every claim Missing-source and report that verification needs sources. The claim list itself is useful output — it tells the author what needs sourcing.

### Error: "Sources conflict with each other"
Cause: Two credible sources give different figures or accounts.
Solution: Label the claim Disputed, present both sources with dates and tiers in the evidence record, and note in Warnings which source is newer or higher-tier.

### Error: "Quote is a translation or cleaned-up transcription"
Cause: Exact-words check fails on legitimately edited speech.
Solution: Verify against the original-language or raw source when reachable. When the edit is disclosed and meaning-preserving, label Verified and note the edit; an undisclosed edit stays a finding.

### Error: "Claim count is very large"
Cause: Long document with dense factual content.
Solution: Keep every claim. Batch verification by source — verify all claims touching one source together — rather than trimming the claim list. Report length scales with claim count by design.

---

## References

- `references/verification-methods.md` — lateral reading, source-tier climbing, triangulation, quote verification in depth
- `references/staleness-windows.md` — freshness windows per claim type and re-check actions
- `evals/` — blind A/B fixture corpus with `ground-truth.json` and judging `rubric.md` (maintenance context: load only when evaluating or modifying this skill)
