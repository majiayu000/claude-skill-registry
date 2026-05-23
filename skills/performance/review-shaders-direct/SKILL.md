---
name: review-shaders-direct
description: Incremental HLSL shader audit — grep-driven, no agent swarm, built for codebases with prior optimization passes
user-invocable: true
disable-model-invocation: true
---
Deep-audit HLSL pixel shaders in `src/shaders/` for GPU performance waste. Use direct Grep/Read — do NOT delegate discovery to agents. This skill is designed for codebases that have already been through optimization passes, where most low-hanging fruit is gone and agent swarms produce more false positives than real findings.

## Why This Skill Exists

Agent swarms scanning for shader optimization patterns have two failure modes after prior passes:
1. **Fabricated findings** — agents report patterns in files that don't contain them (e.g., claiming sin/cos pairs exist when sincos is already used)
2. **Fabricated work** — agents report successful edits they didn't actually make (verified via git status showing no changes)

Direct Grep/Read output is ground truth. Build the audit on that.

## Methodology: Grep-First, Read-to-Verify

### Phase 1 — Inventory (1 minute)

Count files and get the lay of the land:
```bash
find src/shaders -name "*.hlsl" | wc -l
find src/shaders -name "*.hlsl" -printf "%h\n" | sort | uniq -c
```

### Phase 2 — Pattern Scan (direct Grep, no agents)

Run these Grep queries yourself. Each returns ground-truth file:line matches. Run them in parallel where independent.

**Transcendentals:**
1. `cos(` in files that do NOT contain `sincos` — find files that haven't been converted
2. `sin(X)` and `cos(X)` with same argument near each other — paired candidates
3. `pow(` with literal integer/half-integer exponents (2.0, 3.0, 0.5)

**Loop-invariant rotations:**
4. `mul(rot(` or `mul(rotate(` — find all rot() call sites
5. Cross-reference with `for` loops — are any rot() calls inside loops with time-only arguments?

**Constant rotations:**
6. `rot(` followed by a literal number (not a variable) — candidates for `static const`

**Algebraic:**
7. `clamp(` — check if any have exact 0.0, 1.0 bounds (→ saturate)
8. `fmod(` with `, 1.0)` second argument (→ frac)
9. `length(` appearing twice with same argument nearby (→ dot for squared)

**Conversion artifacts:**
10. `iMouse` in non-mouse shaders — dead code?
11. `pow(` with 2.0 exponent — should be `x*x`

### Phase 3 — Read and Verify (only files that matched)

For each Grep hit, Read the file at that line to verify:
- Is the pattern actually un-optimized? (Many will already be fixed)
- Is the argument truly the same? (sin(X) and cos(Y) with X!=Y is not a pair)
- Is the rot() call truly loop-invariant? (Check if the angle depends on the loop variable)
- Is the clamp truly 0-to-1? (clamp(x, 0.0, 2.0) is not a candidate)

**Critical rule: If Grep returns 0 matches for a pattern, that pattern is clean. Do not report findings that don't exist in Grep output.**

### Phase 4 — Verify rot() constructor conventions

Different shaders use different rotation matrix conventions:
- `float2x2(c, s, -s, c)` — one rotation direction
- `float2x2(c, -s, s, c)` — the transpose (opposite direction)

When replacing `rot(LITERAL)` with `static const float2x2`, you MUST read the rot() function in that file to determine which convention it uses, then compute sin/cos values accordingly. Getting this wrong silently reverses rotation direction.

### Phase 5 — Implement

For small batches (< 10 files): edit directly with Edit tool.

For large batches (10+ files with same mechanical pattern): you MAY use an agent for bulk edits, but:
- **Verify via `git diff --stat`** after the agent completes
- If the agent claims N files changed but git shows fewer, the agent fabricated work
- Re-do any missing edits yourself

### Phase 6 — Compile and Test

```
powershell -File tests/test.ps1 --live
```

Then check for bin changes:
```
git status --short resources/shaders/
```

HLSL changes MUST have corresponding `.bin` changes committed together.

## What to Look For

Same optimization patterns as `/review-shaders` — sincos, pow simplification, loop-invariant hoisting, constant rotation matrices, clamp→saturate, fmod→frac, dead code, CSE — but discovered through Grep, not through agent reports.

**Cardinal rule**: Every optimization must produce visually identical output. Prove mathematical equivalence for each change.

## Assessment Format

Report only **verified findings** — patterns confirmed by Grep output AND file reads. Group by pattern:

| Pattern | File:Line | Current Code | Fix | Verified |
|---------|-----------|-------------|-----|----------|
| Paired sin/cos | `foo.hlsl:42` | `cos(v); sin(v)*1.73` | `sincos(v, n, m)` | Read confirmed |

Do not include patterns that Grep showed 0 matches for. Do not include files where Read showed the pattern was already optimized.

## Key Differences from `/review-shaders`

| Aspect | `/review-shaders` | `/review-shaders-direct` |
|--------|-------------------|--------------------------|
| Discovery | Agent swarm (3 Explore agents) | Direct Grep + Read |
| False positive rate | High after prior passes | Zero (tool output is ground truth) |
| Fabrication risk | Agents report non-existent findings | None (you see the Grep output) |
| Planning mode | Yes (full plan workflow) | Optional — skip if findings are small |
| Bulk edits | Agent workers | Direct edits; agents only for 10+ file mechanical changes, verified via git diff |
| Speed | Slower (agent overhead + verification) | Faster (direct tool calls) |
| Best for | First-pass audit of unoptimized codebase | Incremental passes on already-optimized codebase |
