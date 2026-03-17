---
name: audit-source
description: White-box security audit. Blue-teamer evaluates defensive posture, then red-teamers attack informed by defensive gaps. Iterates when exploit chains are discovered. Heavy and thorough by design.
model: opus
---

# Audit Source — White-Box Security Audit

Orchestrates a comprehensive security assessment of the project's source code using both defensive and offensive analysis. A blue-teamer evaluates the defensive posture first, then a lead red-teamer performs reconnaissance informed by the defensive gaps. Dedicated red-teamers investigate each attack vector in depth. Findings are synthesized, exploit chains are explored, and the process iterates until no new chains emerge.

**This is deliberately heavy.** Thoroughness is the priority, not speed. A complete audit may spawn many agents and take significant time. That's the point — shallow security reviews miss the vulnerabilities that matter.

## Workflow Overview

```
┌──────────────────────────────────────────────────────┐
│                   AUDIT WORKFLOW                     │
├──────────────────────────────────────────────────────┤
│  1. Determine scope                                  │
│  2. Spawn blue-teamer (defense evaluation)           │
│     └─ Output: control inventory + gaps + depth      │
│  3. Spawn lead red-teamer (reconnaissance)           │
│     └─ Input: blue-teamer's defense evaluation       │
│     └─ Output: attack surface + ranked vector list   │
│  4. For each high-confidence vector:                 │
│     └─ Spawn focused red-teamer (deep investigation) │
│  5. Synthesize findings                              │
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

### 2. Defense Evaluation — Blue-Teamer

**Spawn a `sec-blue-teamer` agent for full defense evaluation:**

```
You are the blue-teamer for a white-box security audit. Your defense evaluation
will be passed to the red team to inform their attack planning.

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

Pay special attention to CONSISTENCY. The red team will exploit every gap where
a control exists but isn't applied universally.

Output your full report in your standard format. Your findings will be passed
directly to the lead red-teamer to inform reconnaissance.
```

**When the blue-teamer reports back:** Review the defense evaluation. The control inventory, gap analysis, and defense-in-depth assessment become critical input for the red team.

### 3. Reconnaissance — Lead Red-Teamer

**Spawn a `sec-red-teamer` agent in broad recon mode, informed by the blue-team evaluation:**

```
You are the lead red-teamer for a white-box security audit. The blue team has
already evaluated the defensive posture. Use their findings to focus your
reconnaissance on the weakest defenses.

Scope: [entire codebase | user-specified scope]
User concerns: [any areas of concern mentioned by user, or "none specified"]

## BLUE TEAM DEFENSE EVALUATION
[Full blue-teamer report — control inventory, gaps, defense-in-depth assessment]

Perform phases 1–3 of your methodology:
1. Reconnaissance — map the full attack surface (every entry point, what it
   accepts, who can reach it). Cross-reference with the blue team's control
   inventory to identify which entry points lack defenses.
2. Data flow tracing — for each entry point, trace input to its final
   destination. The blue team identified consistency gaps — verify whether
   those gaps are exploitable.
3. Trust boundary mapping — identify where trust transitions occur. The blue
   team flagged single points of security failure — these are your priority
   boundaries.

Do NOT perform deep exploitation yet. Your job is to survey the landscape and
produce a prioritized target list. The blue team's findings should make your
recon significantly more targeted.

Output a structured report:

## ATTACK SURFACE
[Entry points discovered, ranked by exposure]
[Note which entry points the blue team identified as unprotected or
inconsistently protected]

## TRUST BOUNDARIES
[Trust boundaries identified, noting implicit/unguarded ones]
[Cross-reference with blue team's defense-in-depth assessment]

## TARGET LIST
For each promising attack vector, provide:
- Target: [entry point or code path]
- Files: [specific files and line ranges to focus on]
- Hypothesis: [what you think might be exploitable and why]
- Blue team context: [relevant defensive gaps from blue team report]
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

**When the lead reports back:** Review the target list. This is the basis for the deep-dive phase.

### 4. Deep Investigation — Focused Red-Teamers

**For each target in the lead's list (ALL priorities), spawn a dedicated `sec-red-teamer` agent:**

```
You are a focused red-teamer investigating a single attack vector.

## YOUR TARGET
Target: [from lead's report]
Files: [from lead's report]
Hypothesis: [from lead's report]
Blue team context: [defensive gaps relevant to this target]
Context: [from lead's report]
Investigation approach: [from lead's report]

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

### 5. Synthesize and Chain

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
Vectors investigated: [N of M targets from recon]
Findings: N (X critical, Y high, Z medium, W low)
Exploit chains: N

## DEFENSE POSTURE (from blue-teamer)
[Summary of control inventory and key gaps]
[Defense-in-depth assessment — where security relies on a single control]

## ATTACK SURFACE (from lead red-teamer)
[Entry points discovered, ranked by exposure]

## FINDINGS

### CRITICAL
- **[file:line — target]** — [vulnerability description]
  - Attack: [concrete exploitation path]
  - Impact: [what the attacker gets]
  - Data flow: [entry] → [transformations] → [sink]
  - Defensive gap: [what the blue team identified that enabled this]
  - Fix: [remediation guidance]
  - Discovered by: [blue team | lead recon | focused agent for <target> | chain analysis]

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

**Sequential execution within each phase.** The blue-teamer runs first, then the lead red-teamer (with blue-team input), then focused red-teamers run sequentially so findings accumulate for chain analysis.

**Fresh instances for every agent.** Each agent gets a clean context window dedicated entirely to its task. This is the core design principle — full context dedicated to a single concern.

**State to maintain (as orchestrator):**
- Blue-teamer's defense evaluation (passed to lead red-teamer and included in final report)
- Lead red-teamer's attack surface report and target list
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

## Integration with Other Skills

**Relationship to `/bugfix`:**
- `/bugfix` invokes `sec-blue-teamer` for scoped security review of changed code
- `/audit-source` is a dedicated, full-depth security audit
- Use `/audit-source` proactively; `/bugfix` handles security reactively

**Relationship to `/implement`:**
- `/implement` may invoke `sec-blue-teamer` as part of its review phase
- `/audit-source` is independent and deeper — run it when security assurance matters, not as part of routine development

**Relationship to `/review-release`:**
- `/review-release` includes basic security checks (secrets, debug artifacts)
- `/audit-source` is a comprehensive pre-release security audit — run it before major releases or after significant feature additions

## Example Session

```
> /audit-source

What is the scope of the audit?
> Entire codebase

Anything you're particularly concerned about?
> We just added OAuth support and I'm worried about the token handling

Any areas to skip?
> vendor/ and testdata/

Starting white-box security audit...

[Phase 1 — Defense Evaluation]
Spawning blue-teamer...

Blue-teamer report:
  Controls inventoried: 8
  Key gaps:
  - Auth middleware missing on 3 of 14 routes (/internal/*, /ws/*, /api/export)
  - No parameterized queries — ORM used for 11 of 14 queries, 3 use raw SQL
  - CSRF protection on POST only, not PUT/DELETE
  - No rate limiting on /api/auth/* endpoints
  - OAuth state parameter generated but never validated on callback
  Defense-in-depth: Single-layer defense on 4 critical paths

[Phase 2 — Reconnaissance]
Spawning lead red-teamer (with blue-team findings)...

Lead red-teamer report:
  Attack surface: 14 entry points (8 API, 3 WebSocket, 2 CLI, 1 file upload)
  Trust boundaries: 5 identified (2 implicit — database trust, env var trust)
  Targets identified: 7 (3 critical, 3 high, 1 medium)
  Note: Blue team's finding about missing auth on /internal/* routes
  and unvalidated OAuth state confirmed as high-priority targets.

Target list:
  CRITICAL-1: POST /api/auth/callback — OAuth state not validated (blue team flagged)
  CRITICAL-2: POST /api/upload — file upload with path construction from user input
  CRITICAL-3: WebSocket /ws/chat — auth middleware gap (blue team flagged)
  HIGH-1: GET /api/users/:id — IDOR candidate, auth present but no ownership check
  HIGH-2: POST /api/search — raw SQL query (blue team flagged as consistency gap)
  HIGH-3: PUT /api/settings — admin endpoint, middleware inconsistently applied
  MEDIUM-1: GET /api/export — CSV generation with user-controlled column names
  LOW-1: GET /api/health — verbose error messages expose internal paths

[Phase 3 — Deep Investigation]

Spawning focused red-teamer for CRITICAL-1 (OAuth callback)...
  Finding: OAuth state parameter not validated — CSRF on auth callback
  allows attacker to link victim's account to attacker's OAuth identity.
  Severity: CRITICAL
  Defensive gap: Blue team identified state generation without validation.

Spawning focused red-teamer for CRITICAL-2 (file upload)...
  Finding: Path traversal in upload destination. Filename from multipart
  form used directly in path.join() — ../../etc/cron.d/backdoor writes
  to arbitrary location.
  Severity: CRITICAL

Spawning focused red-teamer for CRITICAL-3 (WebSocket)...
  Finding: Dead end. WebSocket handler does check auth via upgrade
  headers. Blue team's middleware gap finding was about a different
  middleware layer. No finding.

Spawning focused red-teamer for HIGH-1 (IDOR)...
  Finding: Confirmed. GET /api/users/:id returns full user record
  including email, hashed password, and API keys for any valid user ID.
  Severity: HIGH (requires authentication)

Spawning focused red-teamer for HIGH-2 (SQL injection)...
  Finding: Confirmed. Search parameter reaches raw SQL via template
  string. POST /api/search with body {"q": "' UNION SELECT * FROM
  users--"} dumps user table.
  Severity: CRITICAL (upgraded from HIGH — unauthenticated endpoint)
  Defensive gap: Blue team identified 3 raw SQL queries bypassing ORM.

Spawning focused red-teamer for HIGH-3 (admin settings)...
  Finding: PUT /api/settings/theme has admin middleware. PUT
  /api/settings/notifications does not. Regular user can modify
  notification settings for all users.
  Severity: HIGH

Spawning focused red-teamer for MEDIUM-1 (CSV export)...
  Finding: Column name parameter reflected in CSV output without
  escaping. Formula injection possible — =CMD() in column name
  executes when opened in Excel.
  Severity: MEDIUM

Spawning focused red-teamer for LOW-1 (health endpoint)...
  Finding: Confirmed. Stack traces in error responses expose internal
  file paths and dependency versions. Information disclosure only.
  Severity: LOW

[Phase 4 — Chain Analysis]

Analyzing 5 findings for chains...

Chain found: IDOR (HIGH-1) + OAuth CSRF (CRITICAL-1)
  → Attacker reads victim's email via IDOR, initiates OAuth link for
  that email, sends CSRF callback to victim. Result: attacker gains
  OAuth access to victim's account without knowing their password.

Spawning chain investigator...
  Chain confirmed. Full exploitation path validated.
  Combined severity: CRITICAL

No further chains discovered. Audit converging.

## Security Audit Summary
Scope: entire codebase (excluding vendor/, testdata/)
Defense evaluation: 8 controls inventoried, 5 gaps found
Attack surface: 14 entry points
Vectors investigated: 8 of 8 targets
Findings: 8 (3 critical, 2 high, 1 medium, 1 low)
Exploit chains: 1

[Detailed findings presented to user...]

Would you like to route these findings to agents for remediation?
> Yes, let's fix the criticals

[Routing CRITICAL findings to appropriate SMEs...]
```
