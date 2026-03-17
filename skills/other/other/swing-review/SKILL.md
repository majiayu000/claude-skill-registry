---
name: swing-review
description: Devil's Advocate stress-testing for code, architecture, PRs, and decisions. Surfaces hidden flaws through structured adversarial analysis with metacognitive depth. Use for high-stakes review, stress-testing choices, or when the user wants problems found deliberately. NOT for routine code review (use engineering:code-review). Triggers on "스트레스 테스트", "stress test", "devil's advocate", "반론", "이거 괜찮아", "문제 없을까", "깊은 리뷰", "critical review", "adversarial".
argument-hint: "[code/decision/PR to stress-test]"
allowed-tools: Read, Grep, Glob, Bash, Agent
---

# Adversarial Review

Structured Devil's Advocate analysis that surfaces hidden flaws, edge cases, and blind spots.


## Rules (Absolute)

1. **Default to finding problems.** Conduct rigorous analysis across all three vectors. Report every genuine issue found — do not downplay or omit real concerns. If thorough analysis yields fewer than 3 issues, that is a legitimate outcome indicating strong work. Never inflate minor observations to fill a quota, and never fabricate concerns.
2. **Attack the strongest points.** Don't waste time on trivial issues. Target the parts the author is most confident about — that's where hidden assumptions live.
3. **Separate severity levels.** Not all issues are equal. Clearly distinguish critical from minor.
4. **Propose alternatives.** Every criticism must include a concrete alternative or mitigation.
5. **Steel-man first.** Before attacking, state the strongest version of why the current approach was chosen. This prevents straw-man critiques.
6. **No ad hominem.** Critique the work, not the author. Be sharp but constructive.

## Ambiguous Input Handling

If the subject under review is unclear or too broad, **ask one clarifying question before proceeding.** Do not review a vague target. Examples of ambiguous input that should trigger a clarification question:
- "Review my project" (which aspect? architecture? security? specific files?)
- "Is this okay?" with no context (what is "this"?)
- A topic so broad that a meaningful adversarial review would be unfocused

One question. Get the answer. Then proceed.

## Process

### Phase 1: Steel-Man

Before any criticism, articulate:
- **Why was this approach chosen?** (Best possible justification)
- **What does it optimize for?** (Performance? Simplicity? Time-to-market?)
- **Under what conditions is this the right choice?**

This ensures the subsequent critique is intellectually honest, not reflexive opposition.

### Phase 2: Adversarial Attack (3 Vectors)

Apply three independent attack vectors simultaneously:

#### Vector A: Logical Soundness
**Scope: Does the REASONING hold?** Examine premises, conclusions, logical flow.
- Are there logical contradictions or circular reasoning?
- Are conclusions actually supported by the stated premises?
- What unstated assumptions does the reasoning depend on?
- Is there confirmation bias in the evidence selection?
Do NOT examine implementation structure — that's Vector C.

#### Vector B: Edge Case Assault
**Scope: Does it SURVIVE reality?** Test against real-world conditions.
- What happens at boundaries? (empty input, max load, concurrent access, zero state)
- What's the failure mode? (graceful degradation vs. catastrophic failure)
- What happens in 6 months? (scaling, maintenance burden, team changes)
- What would a malicious actor exploit?
Test behavior and outcomes, not internal structure.

#### Vector C: Structural Integrity
**Scope: Is the STRUCTURE sound?** Examine architecture and design.
- Does each component have a single, clear responsibility?
- Where are the coupling points and dependency chains?
- What is the weakest structural link?
- Which component, if changed, would cause the most cascading failures?
Examine architecture, not logical reasoning.

### Phase 3: Severity Classification

Classify every finding:

| Severity | Symbol | Meaning | Action Required |
|----------|--------|---------|-----------------|
| Critical | `🔴` | Will cause production issues, security vulnerabilities, or data loss | Must fix before merge/deploy |
| Major | `🟠` | Significant risk, performance issue, or maintainability problem | Should fix, blocking for merge |
| Minor | `🟡` | Code smell, style issue, or small optimization opportunity | Consider fixing, non-blocking |
| Note | `💡` | Observation, alternative approach, or future consideration | Informational only |

### Phase 4: Counter-Proposal

For each Critical and Major finding, provide:
1. **What's wrong** (1-2 sentences)
2. **Why it matters** (concrete impact)
3. **Suggested fix** (code snippet or approach)
4. **Trade-off of the fix** (nothing is free — what does the fix cost?)

## Output Format

```markdown
## Adversarial Review: [Subject]

### Steel-Man
> [Why this approach makes sense — strongest justification]

### Findings

#### 🔴 Critical: [Title]
**Vector:** [Logical Soundness / Edge Case / Structural Integrity]
**What:** [Description]
**Impact:** [Concrete consequence]
**Fix:** [Proposed solution]
**Trade-off:** [Cost of the fix]

#### 🟠 Major: [Title]
...

#### 🟡 Minor: [Title]
...

#### 💡 Note: [Title]
...

### Summary
| Severity | Count |
|----------|-------|
| 🔴 Critical | N |
| 🟠 Major | N |
| 🟡 Minor | N |
| 💡 Note | N |

### Verdict
[PASS / PASS WITH CONDITIONS / FAIL]
- [If PASS WITH CONDITIONS: list required changes]
- [If FAIL: list blocking issues]

### Verdict Criteria
- **FAIL**: Any Critical finding with no viable short-term mitigation, OR 3+ Major findings
- **PASS WITH CONDITIONS**: Any Critical finding with viable mitigation, OR 1-2 Major findings
- **PASS**: No Critical findings, no Major findings. Minor and Notes only.
These thresholds ensure consistent verdicts across invocations.

### Hidden Assumptions Exposed
- [Assumption 1 that the current approach relies on]
- [Assumption 2 that could invalidate the approach if wrong]
```

## Quality Calibration

### BAD Adversarial Review (Don't Do This)
```
## Adversarial Review: User Auth Module

### Steel-Man
> It works.

### Findings

#### 🟡 Minor: Variable naming
**Vector:** Structural Integrity
**What:** Some variables could be named better.
**Impact:** Readability.
**Fix:** Rename them.
**Trade-off:** Time.

#### 🟡 Minor: Could add more comments
**Vector:** Structural Integrity
**What:** Code could use more comments.
**Impact:** Future developers might be confused.
**Fix:** Add comments.
**Trade-off:** None.

#### 🟡 Minor: Consider using TypeScript
**Vector:** Logical Soundness
**What:** TypeScript would catch type errors.
**Impact:** Fewer runtime bugs.
**Fix:** Migrate to TypeScript.
**Trade-off:** Migration effort.

### Verdict: PASS
```

**Why this is bad:**
- Steel-man is lazy — no genuine engagement with design intent
- All findings are shallow nitpicks, not substantive concerns
- No Critical or Major issues even considered — no real stress-testing happened
- Vectors are misapplied ("variable naming" is not Structural Integrity)
- Fixes are vague ("rename them", "add comments") with no specifics
- "Consider using TypeScript" is a preference, not a flaw found through analysis

### GOOD Adversarial Review (Do This)
```
## Adversarial Review: User Auth Module

### Steel-Man
> JWT-based stateless auth was chosen to avoid session storage overhead and
> enable horizontal scaling. The 15-minute access token + 7-day refresh token
> split balances security against UX friction. Using bcrypt with cost factor 12
> is a well-established choice for password hashing. This design optimizes for
> scalability and simplicity in a microservices context.

### Findings

#### 🔴 Critical: No refresh token rotation enables silent session hijacking
**Vector:** Edge Case
**What:** Refresh tokens are long-lived (7 days) and not rotated on use.
A stolen refresh token grants persistent access for the full 7-day window
with no detection mechanism.
**Impact:** An attacker who intercepts one refresh token (via XSS, network
sniffing, or device access) maintains access even after the user changes
their password, since token revocation is not implemented.
**Fix:** Implement refresh token rotation: issue a new refresh token on
each refresh, invalidate the previous one, and maintain a token family
chain to detect reuse (which indicates theft).
**Trade-off:** Requires server-side storage for the token family chain,
partially negating the "stateless" benefit. Adds ~50ms per refresh request.

#### 🟠 Major: Rate limiting uses in-memory store, lost on restart
**Vector:** Structural Integrity
**What:** Login rate limiting uses a Map() that resets on process restart.
**Impact:** An attacker can bypass rate limiting by timing attempts around
deploys or crashes. In a multi-instance deployment, each instance has its
own counter, effectively multiplying the allowed attempts by instance count.
**Fix:** Move rate limit state to Redis with TTL-based expiry.
**Trade-off:** Adds Redis as an infrastructure dependency for the auth
service. ~2ms latency per rate limit check.

### Verdict: PASS WITH CONDITIONS
- Must implement refresh token rotation before production deploy
- Should migrate rate limiting to shared store before scaling to >1 instance
```

**Why this is good:**
- Steel-man genuinely engages with the design rationale and trade-offs
- Findings target real security risks, not style preferences
- Each finding has specific, concrete impact (not "readability" or "confusion")
- Fixes include implementation direction AND quantified trade-offs
- Vectors are correctly applied and don't overlap
- Verdict follows directly from the severity thresholds

## Specialized Modes

### Code Review Mode
When reviewing code (files, PRs, diffs):
- Read all changed files with the Read tool
- Check for OWASP Top 10 vulnerabilities
- Verify error handling completeness
- Assess test coverage of edge cases
- Review naming, structure, and abstraction levels

### Architecture Decision Mode
When reviewing architecture/design decisions:
- Evaluate scalability assumptions
- Test with 10x and 100x current load mentally
- Check for single points of failure
- Assess vendor lock-in risks
- Consider team capability alignment

### PR Review Mode
When reviewing pull requests:
- Focus on behavioral changes, not style
- Check for breaking changes to public APIs
- Verify backward compatibility
- Assess rollback strategy
- Check migration paths for data changes

## When to Use

- Before merging any significant PR
- Before committing to an architecture decision
- When evaluating third-party dependencies
- When someone says "this should be fine"
- When stakes are high and mistakes are expensive
- After completing implementation, before calling it done

## When NOT to Use

- Trivial changes (typos, formatting)
- When exploration is needed first (use `swing-research`)
- When generating alternatives (use `swing-options`)
- When you need neutral, exhaustive analysis without a verdict (use `deep-dive-analyzer` — it understands; this skill *challenges*)
- Personal preferences or subjective design choices

## Integration Notes

- **With swing-clarify:** Run swing-clarify first on ambiguous requests before invoking this skill. Clarified scope produces better results.
- **With swing-options:** After adversarial review reveals problems, use swing-options to generate alternative approaches
- **With swing-research:** Use research to verify claims made during review (e.g., "is this really a security risk?"). For a full-rigor workflow: `swing-research` → `swing-review`
- **With deep-dive-analyzer:** For understanding before challenging: `deep-dive-analyzer` (understand) → `swing-review` (challenge). This skill focuses on finding flaws; deep-dive focuses on neutral exhaustive analysis.
- **With orchestrator strategy team:** Complements the strategy team's Devil's Advocate agent with structured methodology
