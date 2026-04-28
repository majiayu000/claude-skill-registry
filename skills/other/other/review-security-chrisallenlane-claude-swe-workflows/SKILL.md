---
name: review-security
description: White-box security audit. Blue-teamer and lead red-teamer run in parallel isolation for an independent first pass — neither sees the other's output during reconnaissance. A synthesis step categorizes findings into four prescriptive buckets (anchoring-suppressed, convergent, blue-flagged-unverified, divergent), producing a unified target list. Focused red-teamers then deep-dive each target. Iterates when exploit chains are discovered. Heavy and thorough by design.
model: opus
---

# Review Security — White-Box Security Audit

Orchestrates a comprehensive security assessment of the project's source code using both defensive and offensive analysis. A blue-teamer and a lead red-teamer run in parallel, in isolation — neither sees the other's output during the first pass. The orchestrator then synthesizes their territories into a unified target list with four prescriptive categories, surfacing what each team alone would have missed. Focused red-teamers deep-dive each target. Findings are synthesized, exploit chains are explored, and the process iterates until no new chains emerge.

**This is deliberately heavy.** Thoroughness is the priority, not speed. A complete audit may spawn many agents and take significant time. That's the point — shallow security reviews miss the vulnerabilities that matter.

The parallel-isolated first pass is the load-bearing discipline of this skill. The previous design ran blue first, then red informed by blue. That design embedded an anchoring failure mode: whatever the blue team flagged as "the defensive territory" became the salient territory for the red team. Real attackers don't get a defensive briefing — they look at the system fresh and find what defenders missed. Independent reconnaissance surfaces the territory the old design suppressed.

## Workflow Overview

```
┌──────────────────────────────────────────────────────┐
│                   AUDIT WORKFLOW                     │
├──────────────────────────────────────────────────────┤
│  1. Determine scope                                  │
│  2. Independent first pass (parallel, isolated)      │
│     ├─ Blue-teamer (defense evaluation)              │
│     │   └─ Output: control inventory + gaps + depth  │
│     └─ Lead red-teamer (reconnaissance)              │
│         └─ Input: scope only (no blue-team output)   │
│         └─ Output: attack surface + target list      │
│  3. Reconnaissance synthesis                         │
│     ├─ Categorize: anchoring-suppressed,             │
│     │   convergent, blue-flagged-unverified,         │
│     │   divergent                                    │
│     └─ Output: unified target list (≤25)             │
│  4. For each target on unified list:                 │
│     └─ Spawn focused red-teamer (deep investigation) │
│        └─ Includes blue-team context iff target      │
│           origin includes blue-team data             │
│  5. Findings synthesis + chain analysis              │
│     ├─ If exploit chains found → goto 4 (new vector) │
│     └─ If no new chains → proceed                    │
│  6. Present consolidated findings to user            │
│  7. Optionally route findings to fixers              │
└──────────────────────────────────────────────────────┘
```

## Workflow Details

### 1. Determine Scope

**Default:** Production code only. The following are excluded by default:
- Test code (test files, test fixtures, test helpers)
- Dev-only dependencies and tooling (build tools, linters, bundler configs)
- Generated code, vendored code

Inform the user of these exclusions when presenting the scope. If the user wants to include any of them, respect that.

**If user specifies scope:** Respect it (directory, files, module, feature area). Pass scope to all spawned agents.

**Ask the user:**
- "What is the scope of the audit?" (entire codebase, specific module, specific feature)
- "Is there anything you're particularly concerned about?" (auth, file handling, a recent change, etc.)
- "Are there any areas I should skip beyond the defaults?" (additional exclusions)

User concerns inform the prioritization of vectors in later steps, but the blue-teamer and lead red-teamer still perform full analysis — user intuition supplements, not replaces, systematic analysis.

### 2. Independent First Pass — Parallel and Isolated

**Spawn the blue-teamer and lead red-teamer in parallel.** Neither agent sees the other's output during this phase. This is the load-bearing discipline of the skill: independent reconnaissance prevents the blue team's defensive map from anchoring the red team's attack planning, and surfaces the territory each side alone would miss.

#### 2a. Blue-Teamer — Defense Evaluation

Spawn a `sec-blue-teamer` agent for full defense evaluation:

```
You are the blue-teamer for a white-box security audit. You are running in
parallel with the lead red-teamer; you will not see their output during
this phase. Perform your evaluation from defenders' first principles.

Scope: [entire codebase | user-specified scope]
User concerns: [any areas of concern mentioned by user, or "none specified"]

Perform your full methodology:
1. Inventory security controls — map every defense that exists (auth, authz,
   input validation, CSRF, headers, rate limiting, crypto, secrets, logging)
2. Evaluate each control — correctness, consistency, failure mode
3. Identify missing controls — what should exist but doesn't, given the
   application type?
4. Assess defense-in-depth — where does security rely on a single control?
5. Review configuration — are security features properly configured?
6. Dependency hygiene — run available tooling, check for CVEs and supply chain
   concerns
7. Secrets and credentials — check for secrets in the wrong places

Pay special attention to CONSISTENCY. Gaps where a control exists but isn't
applied universally are the highest-value defensive findings.

Output your full report in your standard format.
```

#### 2b. Lead Red-Teamer — Independent Reconnaissance

Spawn a `sec-red-teamer` agent in broad recon mode. **Do not pass any blue-team output.** The lead red-teamer in this phase performs reconnaissance with no defensive briefing — pure attacker perspective on the codebase.

```
You are the lead red-teamer for a white-box security audit. You are running
in parallel with the blue-teamer; you will not see their output during this
phase. Perform reconnaissance from attackers' first principles — fresh eyes
on the codebase, no defensive briefing.

Scope: [entire codebase | user-specified scope]
User concerns: [any areas of concern mentioned by user, or "none specified"]

Perform phases 1–3 of your methodology:
1. Reconnaissance — map the full attack surface (every entry point, what it
   accepts, who can reach it).
2. Data flow tracing — for each entry point, trace input to its final
   destination.
3. Trust boundary mapping — identify where trust transitions occur, including
   implicit / unguarded ones.

Do NOT perform deep exploitation yet. Your job is to survey the landscape and
produce a prioritized target list.

Output a structured report:

## ATTACK SURFACE
[Entry points discovered, ranked by exposure]

## TRUST BOUNDARIES
[Trust boundaries identified, noting implicit/unguarded ones]

## TARGET LIST
For each promising attack vector, provide:
- Target: [entry point or code path]
- Files: [specific files and line ranges to focus on]
- Hypothesis: [what you think might be exploitable and why]
- Context: [relevant framework protections, validation observed, transformations]
- Priority: [CRITICAL / HIGH / MEDIUM / LOW]
- Investigation approach: [what the focused red-teamer should try]

Rank targets by a combination of exposure (how easy to reach) and potential
impact (how bad if exploited). Include up to 25 targets — but this is a
MAXIMUM, not a quota. Report only targets that genuinely warrant
investigation. A short list is fine. An empty list means the codebase is
well-defended — that is a positive outcome, not a failure. Do not
manufacture or inflate targets to fill slots.
```

**When both agents report back:** review the blue-team's defense evaluation and the red-team's target list. They are now inputs to step 3 (reconnaissance synthesis). Do not yet act on either independently.

### 3. Reconnaissance Synthesis

Pool the blue-team's defense evaluation and the red-team's target list. **The orchestrator (you) performs this synthesis directly — not via a sub-agent.** The categorization rules are mechanical, the orchestrator already holds both reports, and avoiding an extra agent saves cost and round-trip time.

Categorize each item from the combined material into one of four prescriptive buckets:

#### anchoring-suppressed (highest-value bucket)

Red team flagged this as a target, **but blue team did not account for it in their defensive map**. These are the gaps anchoring would have suppressed under the old sequential design. The red team found them precisely because they had no defensive briefing.

Examples:
- File-upload path-traversal risk where the blue team's inventory listed "upload exists" but did not enumerate the path-construction sink
- Spreadsheet formula injection in CSV exports where the blue team did not enumerate spreadsheet sinks
- Verbose error responses exposing internals where the blue team's logging analysis didn't extend to error-response disclosure

These targets get **the highest priority** in the unified list. They are the discipline's payoff.

#### convergent

Both teams independently identified this territory as risky — red team listed it as a target, **and** blue team flagged a defensive gap covering it. High confidence; investigate.

Examples:
- OAuth state validation flagged by blue as "state generated but not validated" and by red as "state handling looks suspicious"
- Raw SQL queries flagged by blue as "3 queries bypass ORM" and by red as "string-built query"

Convergent targets are robust — both perspectives agreed independently. They merit deep investigation.

#### blue-flagged-unverified

Blue team called out a defensive gap, **but red team did not reach this area in independent recon**. Worth investigating to confirm exploitability.

Two interpretations are possible: (a) the gap exists on paper but is not reachable in practice, or (b) the gap is reachable in ways the red team's first pass missed. Focused investigation discriminates.

Examples:
- Auth middleware missing on internal-only routes that may not be internet-facing
- Rate-limiting absence on endpoints the red team didn't probe in first pass
- CSRF protection inconsistency the red team didn't enumerate state-changing endpoints to surface

#### divergent

One team flagged the area, but the other team explicitly cleared it (red team noted controls present and adequate, or blue team examined the area and found defenses sound). Surface for the report; orchestrator judges priority.

Divergent items are usually low-priority but occasionally significant — when one team is wrong about clearance, divergent findings expose the error.

#### Building the Unified Target List

Merge items across categories. Each entry on the list carries metadata:

- **Origin category** (one of the four above)
- **Origin** (red-team-only, blue-team-only, both)
- **Priority** (CRITICAL / HIGH / MEDIUM / LOW)
- **Files / line ranges** to focus on
- **Hypothesis** (for red-team-origin items) or **defensive gap description** (for blue-team-origin items)
- **Investigation approach**
- **Blue-team context** (the relevant slice of blue-team data, if origin includes blue team) — passed verbatim to the focused red-teamer that takes this target

**Cap the unified list at 25 targets.** When the merged list exceeds 25, triage using category prioritization:

1. **All anchoring-suppressed targets are kept** (highest priority — these are the discipline's payoff).
2. **Convergent targets next** (high confidence, both teams agreed).
3. **Blue-flagged-unverified next** (worth verifying to discriminate paper-only gap from real-world reachability).
4. **Divergent last** (often dropped if over capacity).

A short or empty unified list is a valid outcome. It means both teams found little to attack, independently. Do not manufacture targets to fill slots.

### 4. Deep Investigation — Focused Red-Teamers

**For each target on the unified list, spawn a dedicated `sec-red-teamer` agent:**

```
You are a focused red-teamer investigating a single attack vector.

## YOUR TARGET
Target: [from unified list]
Files: [from unified list]
Synthesis category: [anchoring-suppressed | convergent | blue-flagged-unverified | divergent]
Hypothesis: [from unified list]
Defensive context: [included ONLY if the target's origin includes blue-team data —
                    relevant defensive gaps from the blue-team report. Omit
                    for anchoring-suppressed targets and red-team-only divergent
                    targets.]
Context: [from unified list]
Investigation approach: [from unified list]

## PRIOR FINDINGS (if any)
[Findings from other focused red-teamers that might be relevant — especially for chain analysis]

## YOUR MISSION
Go deep on this one target. You have the full methodology available, but your scope is narrow: this single attack vector. Dedicate your full attention to it.

Perform phases 4–7 of your methodology on this target:
4. Break assumptions — systematically challenge what the developer assumed about input to this entry point
5. Exploit error paths — trigger errors in this code path and see what breaks
6. Attack state and timing — look for race conditions, replay, sequence bypass specific to this target
7. Git archaeology — check the history of these specific files for security smells

For each finding:
- Describe the concrete attack (specific enough to reproduce)
- Assess exploitability (how hard is this to actually pull off?)
- Assess impact (what does the attacker get?)
- Note any dependencies on other findings (for chain analysis)

If this vector is a dead end, say so. Don't manufacture findings. A clean report on a well-defended target is valuable.
```

**Run focused agents sequentially, not in parallel.** Each agent's findings may inform the next (chain analysis depends on accumulating findings).

**Pass prior findings to each new agent.** As findings accumulate, each subsequent focused agent receives a summary of what prior agents found. This enables chain discovery — agent 3 might realize that agent 1's low-severity information disclosure combines with agent 2's SSRF to create a critical chain.

### 5. Findings Synthesis and Chain Analysis

After all focused agents have reported, synthesize their findings.

**Chain analysis:**
- Review all findings together. Can any be combined into an exploit chain?
- A chain is two or more individually low/medium-severity findings that combine to create a higher-severity exploit.
- Common chains:
  - Information disclosure + SSRF = access to internal services with knowledge of their endpoints
  - Open redirect + OAuth flow = token theft
  - Low-privilege IDOR + privilege escalation = full account takeover
  - XSS + CSRF = authenticated action without user consent
  - Path traversal + file upload = arbitrary file write → RCE

**If chains are discovered:**
- Create new target entries for each chain
- Return to step 4 with a focused red-teamer dedicated to validating and fully exploiting the chain
- The chain investigator receives all relevant findings from the individual agents and attempts to demonstrate the full chain

**Convergence:** The loop terminates when a synthesis pass produces no new chains. Typically this takes 1–2 chain iterations. If chain analysis keeps producing new chains after 3 iterations, present current findings and let the user decide whether to continue.

### 6. Present Consolidated Findings

Compile all findings from all agents into a single report:

```
## Security Audit Summary

Scope: [what was audited]
Defense evaluation: [summary — N controls inventoried, M gaps found]
Attack surface: [N entry points identified]
Reconnaissance synthesis: N targets across the four categories
  (X anchoring-suppressed, Y convergent, Z blue-flagged-unverified, W divergent)
  [Note any targets dropped during 25-cap triage]
Vectors investigated: [N of M targets from unified list]
Findings: N (X critical, Y high, Z medium, W low)
Exploit chains: N

## DEFENSE POSTURE (from blue-teamer, independent first pass)
[Summary of control inventory and key gaps]
[Defense-in-depth assessment — where security relies on a single control]

## ATTACK SURFACE (from lead red-teamer, independent first pass)
[Entry points discovered, ranked by exposure]

## RECONNAISSANCE SYNTHESIS

### Anchoring-suppressed targets: N
[Targets the red team flagged independently that the blue team's defensive
map did not account for. Highest-value discipline output. List each with
a one-line rationale for why blue team didn't surface it.]

### Convergent targets: N
[Targets both teams flagged independently. List each with the convergent
evidence from both reports.]

### Blue-flagged-unverified targets: N
[Targets blue team called as defensive gaps that red team did not reach in
first-pass recon. List each with the blue-team gap description and a note
on why focused investigation was warranted.]

### Divergent targets: N
[Targets one team flagged that the other team examined and cleared. List
each with both the flag and the clear rationale.]

### Targets dropped during triage (if any): N
[If the merged list exceeded the 25 cap, note which categories were
triaged out. Anchoring-suppressed and convergent are kept first;
blue-flagged-unverified and divergent are dropped first.]

## FINDINGS

### CRITICAL
- **[file:line — target]** — [vulnerability description]
  - Attack: [concrete exploitation path]
  - Impact: [what the attacker gets]
  - Data flow: [entry] → [transformations] → [sink]
  - Defensive gap: [included if blue-team data was relevant to discovery]
  - Fix: [remediation guidance]
  - Discovered by: [blue team independent | red team independent |
                    synthesis (anchoring-suppressed) | focused agent for <target> |
                    chain analysis]

### HIGH
[same format]

### MEDIUM
[same format]

### LOW
[same format]

## EXPLOIT CHAINS
- **[chain name]** — [description of the combined attack]
  - Components: [finding A] + [finding B] + ...
  - Combined impact: [what the chain achieves that individual findings don't]
  - Fix: [which component to fix to break the chain — usually the cheapest link]

## TOOLING RECOMMENDATIONS
[Security tools the project should adopt]

## AREAS NOT COVERED
[Entry points that were deprioritized, limitations of static analysis, things that need runtime testing]
```

**Present to user interactively.** Walk through CRITICAL findings first. For each, explain the attack, the impact, and the recommended fix. Let the user ask questions and discuss before moving to the next finding.

The `Discovered by:` field is meant to make the discipline visible to the user. *Synthesis (anchoring-suppressed)* attribution is especially important — over time, this field provides empirical signal about whether the parallel-isolated first pass is producing value the old sequential design would have suppressed.

### 7. Route to Fixers (Optional)

After presenting findings, ask the user: "Would you like to route these findings to agents for remediation?"

**If yes:**
- For each finding, determine the appropriate fixer:
  - Web vulnerabilities (XSS, CSRF, clickjacking) → `swe-sme-html`, `swe-sme-javascript`, or `swe-sme-css` depending on the fix
  - Injection vulnerabilities (SQL, command, path) → language-appropriate SME
  - Auth/crypto issues → `sec-blue-teamer` for defensive remediation guidance, then language SME for implementation
  - For exploit chains → fix the cheapest link (the component that's easiest to remediate and breaks the chain)

- Spawn the appropriate agent with the finding details and remediation guidance
- After each fix, spawn `qa-engineer` to verify the fix doesn't break functionality
- Commit each fix atomically

**If no:** The audit report stands on its own. The user can act on findings at their discretion.

## Agent Coordination

**Parallel execution within phase 2 (independent first pass).** The blue-teamer and lead red-teamer run simultaneously, in isolation — neither receives the other's output. This is the discipline gate.

**Orchestrator-direct synthesis at phase 3.** The reconnaissance synthesis is performed by the orchestrator, not a sub-agent. The categorization rules are mechanical, the orchestrator already holds both reports, and avoiding an extra agent saves cost and round-trip time.

**Sequential execution within all other phases.** Focused red-teamers (phase 4) run sequentially so findings accumulate for chain analysis.

**Fresh instances for every agent.** Each agent gets a clean context window dedicated entirely to its task. This is the core design principle — full context dedicated to a single concern.

**State to maintain (as orchestrator):**
- Blue-teamer's defense evaluation (from phase 2a; passed selectively to focused red-teamers in phase 4 and included in final report)
- Lead red-teamer's attack surface report and target list (from phase 2b)
- Synthesis categorization for each target on the unified list (from phase 3)
- Each focused agent's findings (accumulating)
- Chain analysis results
- Current iteration count (for convergence limit)
- Running totals for the summary

## Abort Conditions

**Abort focused investigation:**
- Agent produces no actionable findings after full investigation (dead end — expected and fine)

**Abort entire workflow:**
- User interrupts
- 3 chain iterations with new chains still being discovered (present findings, ask user)
- Critical system error

**Do NOT abort for:**
- Individual dead-end vectors (skip and continue)
- Low confidence findings (include in report as LOW)
- An empty unified target list at phase 3 (this is a positive outcome — the codebase is well-defended; present the synthesis report and stop)

## Integration with Other Skills

**Relationship to `/bug-fix`:**
- `/bug-fix` invokes `sec-blue-teamer` for scoped security review of changed code
- `/review-security` is a dedicated, full-depth security audit
- Use `/review-security` proactively; `/bug-fix` handles security reactively

**Relationship to `/implement`:**
- `/implement` may invoke `sec-blue-teamer` as part of its review phase
- `/review-security` is independent and deeper — run it when security assurance matters, not as part of routine development

**Relationship to `/review-release`:**
- `/review-release` includes basic security checks (secrets, debug artifacts)
- `/review-security` is a comprehensive pre-release security audit — run it before major releases or after significant feature additions

**Relationship to `/review-deep`:**
- `/review-deep` runs `/review-security` as one phase of a full pre-release sweep across every `/review-*` dimension
- Use `/review-deep` when you want the full sweep; use `/review-security` alone when security assurance is the specific goal

## Example Session

```
> /review-security

What is the scope of the audit?
> Entire codebase

Anything you're particularly concerned about?
> We just added OAuth support and I'm worried about the token handling

Any areas to skip?
> vendor/ and testdata/

Starting white-box security audit...

[Phase 2 — Independent First Pass]
Spawning blue-teamer and lead red-teamer in parallel (no cross-talk)...

Blue-teamer report:
  Controls inventoried: 8
  Key gaps:
  - Auth middleware missing on 3 of 14 routes (/internal/*, /ws/*, /api/export)
  - No parameterized queries — ORM used for 11 of 14 queries, 3 use raw SQL
  - CSRF protection on POST only, not PUT/DELETE
  - No rate limiting on /api/auth/* endpoints
  - OAuth state parameter generated but never validated on callback
  Defense-in-depth: Single-layer defense on 4 critical paths

Lead red-teamer report (independent recon, no blue-team briefing):
  Attack surface: 14 entry points (8 API, 3 WebSocket, 2 CLI, 1 file upload)
  Trust boundaries: 5 identified (2 implicit — database trust, env var trust)
  Targets identified: 6
    - POST /api/auth/callback — OAuth state handling looks suspicious;
      no validation visible in code path
    - POST /api/upload — file upload with path construction from user input
    - POST /api/search — user input flows into a string-built query (raw SQL)
    - GET /api/users/:id — IDOR candidate; auth middleware present but
      ownership check not visible
    - GET /api/export — CSV export with user-controlled column names
    - GET /api/health — verbose error messages exposing internal paths

[Phase 3 — Reconnaissance Synthesis]

Pooling and categorizing...

ANCHORING-SUPPRESSED (red team found, blue team didn't account for):
- POST /api/upload (path traversal)
  Blue-team inventory listed file upload but did not flag path-construction
  risk. The defensive map had "upload exists"; the attacker view immediately
  saw the path-construction sink.
- GET /api/export (formula injection in CSV)
  Blue-team report did not enumerate spreadsheet-formula sinks. Defenses
  for output encoding focused on HTML; CSV was outside the inventory.
- GET /api/health (verbose errors)
  Blue-team report flagged "logging" but not error-response disclosure.
  Defensive analysis didn't extend to what's leaked when things break.

CONVERGENT (both teams flagged):
- POST /api/auth/callback (OAuth state)
  Blue: "state generated but not validated."
  Red: "state handling looks suspicious; no validation visible."
- POST /api/search (raw SQL)
  Blue: "3 raw SQL queries bypassing ORM."
  Red: "user input flows into string-built query."
- GET /api/users/:id (IDOR)
  Blue: "ownership check missing on resource access."
  Red: "auth middleware present but no ownership validation visible."

BLUE-FLAGGED-UNVERIFIED (blue team flagged, red team didn't reach):
- WebSocket /ws/chat — blue team flagged middleware gap; red team's
  recon focused on HTTP entry points and didn't probe WebSocket auth.
- PUT /api/settings — blue team flagged inconsistent admin middleware
  application; red team did not enumerate PUT endpoints in first pass.
- /api/auth/* (no rate limiting) — blue team flagged absence; red team
  did not probe brute-force scenarios in first pass.
- /internal/* routes — blue team: "auth middleware missing"; red team
  did not surface (network-level or deployment-level constraint may
  prevent reach; warrants verification).

DIVERGENT:
- (no divergent items in this audit — both teams arrived at the same
  conclusion on every area where their analysis overlapped. Divergent
  items are the rarest of the four categories in practice; they emerge
  when teams reach a shared conclusion through different reasoning,
  with one team explicitly clearing what the other flagged.)

Unified target list (13 targets, well under the 25 cap):
  CRITICAL-1: POST /api/auth/callback (convergent)
  CRITICAL-2: POST /api/upload (anchoring-suppressed)
  CRITICAL-3: POST /api/search (convergent)
  HIGH-1: GET /api/users/:id (convergent)
  HIGH-2: PUT /api/settings (blue-flagged-unverified)
  HIGH-3: WebSocket /ws/chat (blue-flagged-unverified)
  MEDIUM-1: GET /api/export (anchoring-suppressed)
  MEDIUM-2: /api/auth/* rate limiting (blue-flagged-unverified)
  LOW-1: GET /api/health (anchoring-suppressed)
  LOW-2: /internal/* routes (blue-flagged-unverified)
  [3 lower-priority items abbreviated]

[Phase 4 — Deep Investigation]

Spawning focused red-teamers sequentially...

CRITICAL-2: POST /api/upload (anchoring-suppressed)
  No blue-team context passed (anchoring-suppressed targets receive none —
  the blue team's map didn't include this territory).
  Finding: Path traversal in upload destination. Filename from multipart
  form used directly in path.join() — ../../etc/cron.d/backdoor writes
  to arbitrary location.
  Severity: CRITICAL

CRITICAL-1: POST /api/auth/callback (convergent)
  Blue-team context passed: "state generated but not validated."
  Finding: OAuth state parameter not validated — CSRF on auth callback
  allows attacker to link victim's account to attacker's OAuth identity.
  Severity: CRITICAL

CRITICAL-3: POST /api/search (convergent)
  Blue-team context passed: "3 raw SQL queries bypassing ORM."
  Finding: Search parameter reaches raw SQL via template string.
  POST /api/search with body {"q": "' UNION SELECT * FROM users--"}
  dumps user table.
  Severity: CRITICAL (upgraded — endpoint is unauthenticated)

HIGH-1: GET /api/users/:id (convergent)
  Finding: Confirmed. Returns full user record including hashed password
  and API keys for any valid user ID with valid auth.
  Severity: HIGH

HIGH-3: WebSocket /ws/chat (blue-flagged-unverified)
  Blue-team context passed: "middleware gap on WebSocket handlers."
  Finding: Dead end. WebSocket handler does check auth via upgrade headers.
  Blue team's middleware gap finding referred to a different middleware
  layer that doesn't apply to the WebSocket authentication path. No finding.

HIGH-2: PUT /api/settings (blue-flagged-unverified)
  Blue-team context passed: "admin middleware applied inconsistently to
  PUT endpoints."
  Finding: PUT /api/settings/theme has admin middleware. PUT
  /api/settings/notifications does not. Regular user can modify
  notification settings for all users.
  Severity: HIGH

MEDIUM-1: GET /api/export (anchoring-suppressed)
  Finding: Column name parameter reflected in CSV output without escaping.
  Formula injection possible — =CMD() in column name executes when opened
  in Excel.
  Severity: MEDIUM

LOW-1: GET /api/health (anchoring-suppressed)
  Finding: Confirmed. Stack traces in error responses expose internal
  file paths and dependency versions. Information disclosure only.
  Severity: LOW

LOW-2: /internal/* routes (blue-flagged-unverified)
  Blue-team context passed: "auth middleware missing."
  Finding: Routes are mounted on a separate listener bound to localhost
  only. Reachable only from within the host. Blue team's flag is correct
  (no auth) but red team's first-pass non-reach was also correct (not
  network-exposed). Defense-in-depth recommendation: add auth even on
  internal routes for layered protection.
  Severity: LOW (defense-in-depth concern, not exploitable as stated)

[Phase 5 — Findings Synthesis and Chain Analysis]

Analyzing 6 findings for chains...

Chain found: IDOR (HIGH-1) + OAuth CSRF (CRITICAL-1)
  → Attacker reads victim's email via IDOR, initiates OAuth link for that
  email, sends CSRF callback to victim. Result: attacker gains OAuth
  access to victim's account without knowing their password.

Spawning chain investigator...
  Chain confirmed. Full exploitation path validated.
  Combined severity: CRITICAL

No further chains discovered. Audit converging.

## Security Audit Summary
Scope: entire codebase (excluding vendor/, testdata/)
Defense evaluation: 8 controls inventoried, 5 gaps found
Attack surface: 14 entry points
Reconnaissance synthesis: 13 targets (3 anchoring-suppressed, 3 convergent,
                                       4 blue-flagged-unverified, 0 divergent,
                                       3 abbreviated for brevity)
Vectors investigated: 9 of 13 targets (4 abbreviated)
Findings: 8 (3 critical, 2 high, 1 medium, 1 low)
Exploit chains: 1

[Detailed findings presented to user. The Discovered by: tags reveal
that 3 of the 8 findings — including the upload path traversal and the
CSV formula injection — emerged from the anchoring-suppressed bucket
that the old sequential design would have suppressed.]

Would you like to route these findings to agents for remediation?
> Yes, let's fix the criticals

[Routing CRITICAL findings to appropriate SMEs...]
```
