---
name: security-auditor
description: Conducting interactive security audits using the Map & Probe methodology. Use when the user wants to perform a security review of source code, find vulnerabilities, audit a codebase, or analyze code for security issues.
argument-hint: "<files or scope>"
allowed-tools:
  - Read
  - Glob
  - Grep
  - mcp__auditor-addon__peek
  - mcp__auditor-addon__call_chains
---

# Security Auditor

<workflow>
SEQUENCE:
1. MAP (required, always first)
2. CHECKPOINT: user confirms system map accuracy; offer CHECKLIST if standards were identified
3. CHECKLIST (optional, skippable) — delegate to `checklister` agent for identified standards
4. PROBE (per-path deep analysis with immediate findings output)
5. CHECKPOINT: user reviews consolidated findings

CHECKPOINT RULES:
- Present findings using the phase's specified output format
- STOP and wait for user response before proceeding
- PROBE has a per-path checkpoint: analyze one path, output findings, STOP. Do not continue to the next path until the user responds.
</workflow>

---

<protocols>
## Core Protocol

All findings are hypotheses until mechanically verified. Never confirm a finding in isolation — cross-reference against docs, specs, and invariants. The PROBE phase implements this through its mandatory refutation step.
</protocols>

<references>
## References

- `references/risk-patterns.md`: Load at the start of every audit. Common weakness and high severity risk patterns that prime attention during analysis.
</references>

---

<phase_instructions>
## Phase Details

<map_instructions>
### MAP

**TRIGGER:** Start of every security audit.
**TIME BUDGET:** 1-2 minutes. This is a structural inventory, not an analysis.
**CHECKPOINT:** Present the system map. If **core** standards were identified, ask: "Does this system map look accurate? I identified [standards] as core to this codebase. Would you like me to generate security checklists for these before moving to Probe, or skip straight to Probe?" Otherwise, ask: "Does this system map look accurate? Ready to proceed to Probe?"
**NEXT:** After confirmation → CHECKLIST (if requested) or PROBE (if skipped).

**Goal:** Produce a structural reference artifact for PROBE. Classify code structure and state. Do not construct attack scenarios or evaluate exploitability — that is PROBE's job.

**Threat model (for later stages):**
- Privileged roles (owner, admin, maintainers) are **honest and aligned**.
- Later analysis will **discard** any finding that requires a privileged role to be malicious.

**Steps:**
1. Run `call_chains` on all in-scope files. Batch parallel runs if multiple files.
2. Read imported files, base classes, and libraries that paths reference. Batch independent reads.
3. Quick repo scan for relevant documentation (README, docs/, specs/). Only load if directly relevant.
4. Produce the output below.

**Output** — four sections, concise:

#### 1. Components

For each major component:
- `Purpose:` 1-2 sentences.
- `Key state:` state variables — who writes, who reads.
- `External surface:` `<funcSignature> — Caller: <who>; Writes: [vars]; External calls: [...]`

#### 2. Invariants

List 3-10 invariants that should hold assuming honest privileged roles. Reference specific state variables and functions. Include:
- **Explicit**: from require/revert/assert.
- **Structural**: from data structure design (composite keys, slot isolation, ordering).

Mark any that depend on out-of-scope assumptions as **uncertain**.

#### 3. Call Chains

From `call_chains` output, list each path:
- `<Path String>`
- `Context:` One sentence — what this flow does.
- `Invariants touched:` from section 2.
- Unresolved cross-boundary calls: note target file/function, mark `[deferred → PROBE]`.

#### 4. Standards

List standards implemented or depended on. Classify as **Core** or **Peripheral**. Only Core standards warrant CHECKLIST. If none are core: `No core standards identified.`
</map_instructions>

---

<checklist_instructions>
### CHECKLIST (Optional)

**TRIGGER:** User opts in at the MAP checkpoint.
**SKIP:** If user declines or no standards were identified, proceed directly to PROBE.

**Goal:** Obtain standard-specific security checklists to inform the PROBE phase.

**Instructions:**
1. Delegate to the `checklister` agent with the identified standards.
2. **Fallback:** If the checklister agent is unavailable, delegate to any available agent with web search capability. If no web-capable agent is available, skip this step and proceed to PROBE.
3. When the checklist is returned, **keep it in context** for use during PROBE.
4. Do NOT present the raw checklist to the user unless asked. Simply confirm: "Checklists loaded for [standards]. Proceeding to Probe."
</checklist_instructions>

---

<probe_instructions>
### PROBE

**TRIGGER:** System map confirmed by user (and CHECKLIST completed or skipped).
**CONSTRAINT:** Analyze ONE execution path per turn. After outputting findings for a path, STOP and wait for user input before proceeding to the next path. The user may reprioritize, ask to go deeper, or redirect focus.
**CHECKPOINT:** After all paths are exhausted, present consolidated findings. "Would you like me to write up any of these findings?"

**Goal:** Systematically analyze every execution path for real, exploitable vulnerabilities.

**Threat Model:**
- Privileged roles are honest.
- Focus on unprivileged/external actors or bad interactions with honest admins.

**Instructions:**

Files read during MAP are already in context. Do not re-read them unless checking specific line ranges not previously examined. Resolve any `[deferred → PROBE]` paths just-in-time when reached.

**Step 1 — Prioritize.** Scan each MAP execution path against `references/risk-patterns.md`. Tag paths with matching patterns. Order paths by: number of pattern matches + number of invariants touched, descending. Paths with zero matches and zero invariants may be batch-cleared (e.g., `Paths X, Y, Z: clear — read-only getters with no state interaction`).

**Step 2 — Analyze.** For each path in priority order:
1. Walk the full chain — use its risk pattern tags, MAP invariants, and any checklists as your lens.
2. When a path mutates state, cross-reference the mutation against other flows and consumers of that state for inconsistent assumptions or anti-patterns.
3. When something smells off, go deep: trace the call chain, construct the attacker story, attempt refutation.
4. **Output findings for this path.** If no findings, state: `Path <name>: clear`. Then STOP and wait for user input.

**Refutation (mandatory for every confirmed finding):**
Before confirming any vulnerability, argue the opposite:
- Look for checks or constraints that would prevent the exploit.
- Verify safety mechanisms are actively enforced, not just present.
- If it breaks an invariant or causes material harm (fund loss, data exfiltration, unauthorized access), it IS a vulnerability.

After all paths:
- **Think as the attacker.** Cross-component interactions, unusual call sequences, timing dependencies, edge cases.
- **Invariant sweep:** For each MAP invariant, revisit the functions listed in its definition and verify the enforcement mechanism is present and active — not just written, but reachable on every path through that function.
- Output any additional findings.

**Output Format (per finding):**

**Confirmed vulnerability:**
1. **Result**: **VULNERABILITY CONFIRMED**
2. **Severity**: <Critical | High | Medium | Low | Informational>
3. **Title**: <short title>
4. **Attack Story**:
   1. Attacker calls function X with Y...
   2. System state changes to Z...
   3. Invariant W is violated...
5. **Impact**: <specific gain or harm>
6. **Mitigation**: <short fix>
7. **Confidence**: <High | Medium | Low>

**Suspicious (unconfirmed):**
1. **Result**: Suspicious
2. **Title**: <short title>
3. **Components / Functions**: <list>
4. **Why suspicious**: <1-3 sentences>
5. **Blocker**: <what prevented confirmation>
6. **Priority guess**: <High | Medium | Low>
</probe_instructions>
</phase_instructions>
