---
name: skeptical-triage
description: Reusable 3-round self-challenge + arbiter pattern for filtering false positives from findings/verdicts. Use when the cost of a false-positive gate block exceeds the cost of ~4 extra LLM turns.
when_to_use: |
  Apply skeptical triage when:
  - A finding could block a gate (gate:code, gate:ship, gate:qa, gate:arch) and flipping it wrongly wastes CTO time
  - A verdict is about to be written to a report that downstream agents will trust (CSO, QA, ADR)
  - Multiple signals disagree (one reviewer says VALID, another says INVALID) — arbiter resolves cleanly
  Do NOT apply to:
  - P2 findings or advisory notes (cost > benefit)
  - Hard findings (secrets in source/git, confirmed CVEs, failing tests) — these are facts, not judgments
  - Quick factual lookups ("does this file exist?", "what version is pinned?")
effort: medium
allowed-tools: Read, Grep, Bash, Glob
paths:
  - "docs/**"
  - "src/**"
  - "lib/**"
  - "app/**"
---

# Skeptical Triage

Filter false positives from multi-angle review, security audit, QA regression flags, or any high-stakes judgment before it turns into a blocker.

Three rounds of skeptical self-review + an impartial arbiter, with a confidence score from the vote.

## When to invoke

| Caller | Finding type | Apply triage? |
|--------|--------------|---------------|
| `/review` | Angle 2/4/7/9 P0/P1 (security, SQL, privacy, concurrency) | Yes |
| `/review --deep` | Any angle P0/P1 | Yes |
| `security-officer` | CSO audit P0/P1 | Yes |
| `security-officer` | Secret in source/git, confirmed CVE | **No** — hard finding |
| `qa-engineer` | Flaky-test verdict (is this a regression or flake?) | Yes |
| `architect` | ADR trade-off dispute (option A vs. B when both look reasonable) | Yes |
| Any | P2/advisory | No |

## The 4-step pattern

Run these sequentially. Each round sees prior reasoning. Arbiter sees all rounds.

### Round 1 — Reachability / Premise

Question: **is the premise true?**
- For security/reliability: can an external attacker reach this code path with untrusted input? Trace input flow backward from the bug site to its origin. If only trusted internal callers → lean INVALID.
- For regressions: does the failing behavior reproduce from a clean state on the target branch?
- For ADR trade-offs: is the constraint that forces the choice actually binding? (e.g. "we need <10ms p99" — is that real or aspirational?)

Output: `{round: 1, verdict: VALID|INVALID|UNCERTAIN, reasoning: "...", crux: "single key fact"}`

### Round 2 — Verify cited defenses / counter-evidence

Question: **are claimed defenses real and sufficient?**
- Every cited defense → use `Grep` to find its actual implementation line.
- Resolve constant names to numeric values. `MAX_BUF_SIZE` is not a verified bound — `#define MAX_BUF_SIZE 64` is.
- For regressions: is the cited "test covers this" actually asserting the right invariant?
- For ADR: is the cited benchmark/precedent real (grep for it, read it), or rumored?

If you cannot point to the line that enforces the defense, **it does not exist.**

Output: same JSON shape, with `grep_used: true/false`.

### Round 3 — Missed angles

Question: **what did Rounds 1-2 not consider?**
- Error paths, integer overflow, race windows, different callers, platform differences
- Do NOT rehash prior rounds — add new evidence or concede
- For QA: retry logic masking the failure? Test pollution from another test?
- For ADR: option C that neither reviewer raised?

Output: same JSON shape.

### Arbiter

Input: all 3 rounds + original finding/question + source code.

Question: **final call — which side has the stronger evidence?**
- Deliver single `verdict: VALID|INVALID` (no UNCERTAIN — make the call).
- Deliver one-sentence `crux` — the key fact the verdict turns on.
- If 3 prior rounds all said the same thing, only override with overwhelming new evidence and explain why.

Output:
```json
{
  "verdict": "VALID",
  "crux": "memcpy at auth.c:142 copies network-controlled len bytes into 64-byte stack buffer with no bound check",
  "reasoning": "Rounds 1 and 3 verified attacker reach; Round 2 found no size check in 50 LOC radius; arbiter confirms no caller clamps len."
}
```

## Hard rules

Burn these into every round's prompt:

1. **Absence of defense → VALID, not UNCERTAIN.** If you searched for a defense and did not find one, that is the answer. "Other code probably handles this" is not a valid defense.
2. **A constant name is not a verified bound — only its resolved value is.** Grep for the `#define` / `const` declaration.
3. **Name the line or it does not exist.** Vague references to "assumptions in this codebase" do not count.
4. **Do not contradict your own conclusion in the same response.** If you verified a defense is insufficient, that is the verdict. Stop searching for reasons to flip.
5. **Code quality issue ≠ security vulnerability.** Data race on diagnostic state, NULL check on internal-only API, UB only in debug builds → INVALID.
6. **Trust your own reasoning.** If you see the crux on first read, don't manufacture a counter-argument.

## Confidence scoring

```
confidence = valid_rounds_before_arbiter / 3
```

- `100%` (VVV) — 3/3 rounds VALID. Arbiter rubber-stamps unless it finds something brand-new.
- `67%` (VVI or VIV or IVV) — majority VALID. Arbiter breaks tie with new evidence.
- `33%` (IIV or IVI or VII) — majority INVALID. Arbiter usually confirms INVALID.
- `0%` (III) — 3/3 INVALID. Arbiter rarely overrides.

Arbiter **overrides** the final verdict; confidence reflects the round vote for transparency. Record both in the output so humans can see where the arbiter diverged.

## Applying triage results to severity

Once the arbiter returns:

| Arbiter verdict | Confidence | Severity action |
|-----------------|------------|-----------------|
| `VALID` | ≥ 50% | Keep original severity |
| `VALID` | < 50% | Demote: P0→P1, P1→P2 |
| `INVALID` | any | Remove from gate tally, record as `[FILTERED]` in report for audit |
| `UNCERTAIN` (only if arbiter could not decide) | n/a | Keep original severity, flag for manual CTO review |

## Output schema

Every caller logs triage results to `.great_cto/triage-log.jsonl` (append-only, one JSON per line):

```json
{
  "timestamp": "2026-04-19T12:34:56Z",
  "caller": "review|security-officer|qa-engineer|architect",
  "finding_id": "SEC-042",
  "file": "src/auth.c:142",
  "original_severity": "P0",
  "rounds": [
    {"round": 1, "verdict": "VALID",   "crux": "..."},
    {"round": 2, "verdict": "VALID",   "crux": "...", "grep_used": true},
    {"round": 3, "verdict": "INVALID", "crux": "..."}
  ],
  "arbiter": {"verdict": "VALID", "crux": "..."},
  "confidence": 0.67,
  "final_severity": "P0"
}
```

This log is how we measure whether triage earns its keep. Review it weekly:

```bash
# False-positive rate: how many findings the arbiter flipped to INVALID
jq 'select(.arbiter.verdict=="INVALID")' .great_cto/triage-log.jsonl | wc -l

# Average rounds-to-consensus (did we need all 3 or did R1+R2 agree?)
jq '[.rounds[].verdict] | unique | length' .great_cto/triage-log.jsonl
```

If FP rate < 10% after 50 triages — triage is filtering noise that wasn't there. Lower threshold or skip triage for that angle. If FP rate > 40% — original review prompt is too trigger-happy; tighten the angle rules.

## Token budget

Per triaged finding: ~4 LLM turns (3 rounds + arbiter). At typical review sizes (~5-10 triaged findings per PR), total budget: 20-40 extra turns per `/review`. Batch when possible — one arbiter can handle multiple findings in a single call if their cruxes are independent.

For cost-sensitive runs (`approval-level: auto` on a huge PR), consider: triage only P0, leave P1 untriaged. Re-tune based on `.great_cto/triage-log.jsonl` data.

## Anti-patterns

- **Don't triage P2/advisory findings.** The whole point is gate decisions. P2 is advisory — let the author see it and move on.
- **Don't let rounds rehash each other.** Round 3 prompt must say "add NEW evidence or concede." If 3 rounds produce identical reasoning, you wasted 2 turns.
- **Don't skip the arbiter on UNCERTAIN.** If all 3 rounds say UNCERTAIN, the arbiter's job is to decide — not to join the fog.
- **Don't hide arbiter overrides.** When the arbiter flips the majority vote, record both `confidence` (the vote) and `final_verdict` (the arbiter). Humans deserve to see the disagreement.
