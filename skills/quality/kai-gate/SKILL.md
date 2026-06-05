---
name: kai-gate
description: Run Kai CMO Harness quality gates on content. Scores Four U's (Unique/Useful/Ultra-specific/Urgent), checks for banned words and AI slop, runs SEO lint for search content. Use when "score this", "quality check", "run quality gates", "check this content", "four u's score", "banned word check", "SEO lint", or any request to validate content quality before publishing.
---

Run the Kai CMO Harness quality gate pipeline on a piece of content.

## Gate Pipeline

Run all three checks in order:

### 1. Four U's Score

Score each dimension 1-4:

| U | Question | Score |
|---|----------|-------|
| **Unique** | Can only WE write this? Original data, perspective, or experience? | 1-4 |
| **Useful** | Can the reader take action immediately? | 1-4 |
| **Ultra-specific** | Numbers, named tools, concrete examples? | 1-4 |
| **Urgent** | Is there a reason to engage today? | 1-4 |

**Thresholds:** 12/16 for blog/SEO/articles. 10/16 for email/ads.

### 2. Banned Word Check

**Instant reject (Tier 1):** leverage, utilize, synergy, innovative, deep dive, circle back, touch base, moving forward, at the end of the day

**AI slop (also reject):** "In conclusion", "It's important to note", "In today's rapidly evolving", "This comprehensive guide", "Without further ado", "It's worth noting that"

Flag exact locations of violations.

### 3. Voice Pattern Check (programmatic — DO NOT skip)

Binary clichés ("X-not-Y" / "It's not X, it's Y" / "isn't X — it's Y") read as LinkedIn slop and slip past subjective scoring. Run these regexes against the file with the Grep tool. Any match = FAIL.

| Pattern | Catches |
|---|---|
| `, not [a-z]` | "X, not Y" |
| `— not [a-z]` | "X — not Y" |
| `\bisn'?t [a-z][^.\n]+ — it'?s\b` | "isn't X — it's Y" |
| `\baren'?t [a-z][^.\n]+ — they'?re\b` | "aren't X — they're Y" |
| `\bIt'?s (a\|the\|an) [^.\n]+, not (a\|the\|an)\b` | "It's a/the X, not a/the Y" |
| `\bThat'?s (a\|the\|an) [^.\n]+, not (a\|the\|an)\b` | "That's a/the X, not a/the Y" |
| `\bIf you [a-z][^,.]+, [a-z]` | "If you X, Y" rhetorical |
| `\bHere'?s the thing\b` | LinkedIn slop |
| `\bI'?ll be honest\b` | LinkedIn slop |
| `\bLet that sink in\b` | LinkedIn slop |
| `\bHot take\b` | LinkedIn slop |

Skip matches inside HTML comments (`<!-- ... -->`) and code fences (```` ``` ````) — those are scorecard / metadata blocks.

**Replacements that work:**
- Collapse to a single load-bearing claim.
- Use parallel-positive contrast where both halves are positive: *"Description is passive. State is something the agent can act on."*
- Use a metaphor: *"expensive webhook"* not symmetrical reversal.

**Project hook integration:** if the project has `.claude/hooks/voice-gate.py`, that hook fires PostToolUse on Edit/Write and catches these patterns at draft time. The gate step still runs the regexes — belt and suspenders.

### 4. SEO Lint (search content only)

Apply only if the content targets search engines. Check against Algorithmic Authorship rules:
- Conditions after main clause
- Instructions start with verbs
- Sentences under 20 words
- Bold the answer, not query terms
- No links in first sentence of paragraphs

For full rule set, read `E:\Dev2\kai-cmo-harness-work\knowledge\frameworks\content-copywriting\algorithmic-authorship.md`.

### 5. Optional Panel Scoring (advisory)

Use panel scoring only when the user asks for a second opinion or the artifact is high-stakes. It does not replace Kai gates and cannot override a hard fail from banned words, source gaps, policy risk, or missing approval.

Recommended panel roles:
- **Audience reviewer**: checks persona fit and plain-language clarity
- **Channel reviewer**: checks platform fit, format, and norms
- **Proof reviewer**: checks source locations, attribution, and unsupported claims
- **Conversion reviewer**: checks CTA clarity and objection handling

Output panel scores as advisory notes:

| Reviewer | Score | Concern | Suggested fix |
|----------|-------|---------|---------------|
| Audience | 1-5 | ... | ... |

Governance rules:
- Label panel output as simulated review, never expert validation.
- Do not create fake credentials, endorsements, or named reviewers.
- Treat missing source locations as a gate issue, not a panel preference.
- Run panel scoring on drafts first; publishing still requires approval.

## Output Format

```
## Quality Gate Results

**Four U's:** [X]/16 [PASS/FAIL]
- Unique: [X]/4 — [reason]
- Useful: [X]/4 — [reason]
- Ultra-specific: [X]/4 — [reason]
- Urgent: [X]/4 — [reason]

**Banned Words:** [PASS/FAIL]
- [list violations with line numbers, or "None found"]

**AI Slop:** [PASS/FAIL]
- [list violations with line numbers, or "None found"]

**Voice Patterns:** [PASS/FAIL]
- [list X-not-Y / LinkedIn-slop violations with line numbers, or "None found"]

**SEO Lint:** [PASS/FAIL/SKIPPED]
- [list violations, or "All rules pass"]

**Overall:** [PASS/FAIL]
```

If FAIL: list specific fixes needed. Offer to auto-fix and re-score.
