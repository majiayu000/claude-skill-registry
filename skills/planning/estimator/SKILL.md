---
name: estimator
description: Conducting project scoping and estimation using logical chunking and metric analysis. Use when the user wants to estimate audit effort, scope a codebase for review, calculate hours for a security engagement, or assess the size of a diff or full repository.
argument-hint: "<scope file or base..head>"
allowed-tools:
  - Read
  - Glob
  - Grep
  - mcp__plugin_auditor-addon_auditor-addon__peek
  - mcp__plugin_auditor-addon_auditor-addon__metrics
  - mcp__plugin_auditor-addon_auditor-addon__diff_metrics
  - mcp__plugin_auditor-addon_auditor-addon__diff
  - mcp__plugin_auditor-addon_auditor-addon__call_chains
---

# Estimator

<workflow>
SEQUENCE:
1. DISCOVERY (required, always first)
2. CHECKPOINT: user confirms "full-scope" or "diff-scope"
3. IF full-scope: EXPLORE (per-chunk) → METRICS → REFLECT → REPORT
   IF diff-scope: DIFF-TRIAGE (per-chunk) → REFLECT → REPORT

CHECKPOINT RULES:
- Present findings using the phase's specified output format
- Ask the checkpoint question explicitly
- STOP and wait for user response before proceeding
- If you analyze multiple chunks without confirmation, STOP and return to last checkpoint
</workflow>

---

<reference_definitions>
## Reference: Categories & Scope

<file_categories>
### File Categories

| Category | Description |
|----------|-------------|
| `business-logic` | Core functionality, value transfer, state changes |
| `infra/glue` | Configuration, interfaces, utilities |
| `presentation` | UI code |
| `tests` | Test files |
| `generated` | Auto-generated bindings |
| `scripts` | Deployment, migration, build scripts |

**Distinguishing business-logic from infra/glue:**
- Affects state transitions, value flows, or protocol invariants → `business-logic`
- Only routes requests, configures settings, or adapts interfaces → `infra/glue`
- Access control that enforces permissions → `business-logic`
- Access control that merely forwards to another module → `infra/glue`
- When uncertain, default to `business-logic` (err toward inclusion)
</file_categories>

<scope_defaults>
### Scope Defaults

| Category | Default Scope | Notes |
|----------|---------------|-------|
| `business-logic` | **in-scope** | Always include |
| `tests` | **out-of-scope** | Unless explicitly requested |
| `generated` | **out-of-scope** | Nothing to audit |
| `scripts` | **out-of-scope** | EXCEPT deployment/initialization scripts → trigger Concern Question |
| `infra/glue` | **Concern Question** | If unclear |
| `presentation` | **Concern Question** | If unclear |
| Deleted files (diff) | **out-of-scope** | Nothing to audit |
</scope_defaults>

<external_dependencies>
### External Dependencies

- Imported libraries (OpenZeppelin, Solmate, Express, gRPC, etc.) → **out-of-scope** by default
- External calls (contract calls, oracles, third-party APIs, message queues) → flag for **Concern Question**
- If in-scope code wraps, extends, or modifies a dependency → ask whether the dependency interaction needs review
</external_dependencies>
</reference_definitions>

<concern_questions>
## Reference: Concern Questions

**Purpose:** When uncertain whether something belongs in scope, ask the user rather than guessing. You lack domain context; the user knows which areas are critical.

**Format:** Frame questions around user priorities, not technical details:
- "Are you concerned that the fee calculation in `Pool.sol` / `BillingService.ts` is correct?"
- "Should the migration scripts be reviewed for data integrity issues?"
- "The access control logic in `Admin.sol` / `AuthMiddleware.go` was modified—is this a critical path?"

**When to use:**
- Files/changes where scope relevance is ambiguous
- Areas that could be important but might also be out of scope
- Anything you would otherwise have to guess about
</concern_questions>

<estimation_baseline>
## Reference: Estimation Baseline

All hour estimates assume a senior auditor who is:
- Proficient in the target language
- Has domain familiarity (e.g., DeFi patterns, authentication flows, distributed systems)

Adjust expectations accordingly for junior auditors or unfamiliar domains.
</estimation_baseline>

<adjustment_reference>
## Reference: Domain Multipliers

The metrics tool accounts for structural complexity and comment density but cannot detect semantic difficulty. Apply explicit multiplier adjustments when domain factors make the work harder or easier than raw metrics suggest.

| Pattern | Typical Multiplier |
|---------|-------------------|
| Inline assembly / low-level bit ops | 1.5x – 2.5x |
| Cryptographic math (ECC, pairings, polynomial commitments, hash circuits) | 1.5x – 3.0x |
| ZK circuit logic (constraint systems, proving/verification details) | 1.5x – 3.0x |
| Dense state machines (many interconnected states, complex transitions) | 1.3x – 2.0x |
| Novel or undocumented protocol logic with no reference implementation | 1.3x – 2.0x |
| Cross-chain / oracle integration points with complex invariants | 1.2x – 1.5x |
| Boilerplate, thin wrappers, repetitive CRUD | 0.6x – 0.8x |

**Formula:** `Adjusted Hours = Tool Hours × Multiplier`

Use the midpoint for moderate cases; upper end when the pattern dominates the file. Skip adjustments smaller than 10% of a file's hours.
</adjustment_reference>

---

<phase_instructions>
## Phase Details

<discovery_instructions>
### DISCOVERY

**TRIGGER:** Start of every estimation.
**CHECKPOINT:** "Does this organization look correct? Are we doing a **full scope** or **diff scope** estimation?"

**Goal:** Discover the scope of the audit and organize files into logical chunks.

**Step 1 — Get file structure:**
- If user provided a scope file → read it
- Otherwise → use `Glob` with patterns like `**/*.sol`, `**/*.ts`, etc.

**Step 2 — Chunk files:**
- **Target size:** 5-15 files per chunk (smaller chunks enable incremental review)
- **Boundaries:** Prefer directory boundaries when cohesion is unclear
- **Cross-cutting files:** Place utilities/helpers in their own "Shared/Utils" chunk
- **Example chunks:** "Core Logic", "Token Implementation", "Auth/Permissions", "API Handlers", "Utils", "Tests", "Scripts"

**Step 3 — Identify patterns:**
For each chunk, note which path patterns are likely in-scope vs out-of-scope:
- In-scope: `src/core/**`, `contracts/**`, `services/**`
- Out-of-scope: `test/**`, `scripts/**`, `mocks/**`

**Step 4 — Present to user:**
- List each chunk with a one-liner description
- Show included files/patterns underneath
- Indicate in-scope vs out-of-scope patterns

**CHECKPOINT:** "Does this organization look correct? Are we doing a **full scope** or **diff scope** estimation?"
</discovery_instructions>

---

<explore_instructions>
### EXPLORE (Full Scope Only)

**TRIGGER:** User confirms full-scope estimation after DISCOVERY.
**CONSTRAINT:** Process ONE chunk at a time. STOP after each chunk and WAIT for confirmation.
**CHECKPOINT:** "Do you agree with this scope? Proceed to next chunk?"
**NEXT:** After final chunk confirmed → METRICS.

**Goal:** For each chunk, categorize files and determine audit relevance.

**Per-Chunk Steps:**

**Step 1 — Prepare:**
- Identify files in the chunk
- **Batch `peek` calls** for ambiguous files
- **Skip `peek`** when path makes category obvious (e.g., `tests/`, `*_test.*`, `generated/`)

**Step 2 — Categorize:**
- Assign each file a category (see File Categories reference)
- If `peek` is insufficient, read up to 200 lines to categorize

**Step 3 — Determine Scope:**
- Apply scope defaults (see Scope Defaults reference)
- Use Concern Questions when unclear

**Step 4 — Report:**
Present summary table:
| File | Category | Scope |
|------|----------|-------|

Include:
- Brief chunk summary
- Any adjustments with justification
- Concern Questions for unclear scope

**CHECKPOINT:** "Do you agree with this scope? Proceed to next chunk?"
</explore_instructions>

---

<metrics_instructions>
### METRICS (Full Scope Only)

**TRIGGER:** All chunks explored and scope confirmed.
**NEXT:** REFLECT.

**Goal:** Calculate metrics and estimate audit effort for all confirmed in-scope files.

**Step 1 — Calculate:**
- Call the `metrics` tool with all confirmed in-scope paths

**Step 2 — Analyze:**
- Review NLoC, Comment Density, Cognitive Complexity (CC), and Estimated Hours
- **Identify anomalies:** Flag files that stand out (unusually high complexity, sparse documentation, outlier size)

**Step 3 — Adjust:**
Apply domain multipliers where needed (see Domain Multipliers reference). Present any adjustments:
```
File: <path>
Multiplier: <Nx>
Adjusted Hours: <X hours>
Reason: <justification>
```

**NEXT:** Proceed to REFLECT.
</metrics_instructions>

---

<diff_triage_instructions>
### DIFF-TRIAGE (Diff Scope Only)

**TRIGGER:** User confirms diff-scope estimation after DISCOVERY.
**CONSTRAINT:** Process ONE chunk at a time. STOP after each chunk and WAIT for confirmation. Skip chunks with no changes.
**CHECKPOINT:** "Do you agree with this scope? Proceed to next chunk?"
**NEXT:** After final chunk confirmed → REFLECT.
</diff_triage_instructions>

**Goal:** For each chunk with changes, calculate diff metrics, classify changes, and determine audit relevance.

**Setup (once, before iterating):**
- Confirm `base` ref with user (e.g., `main`, `v1.0.0`, commit SHA)
- Confirm `head` ref (defaults to `HEAD`)

**Per-Chunk Steps:**

**Step 1 — Calculate Diff Metrics:**
- Call `diff_metrics` with `base`, `head`, and this chunk's paths
- If no changes in chunk → skip to next chunk
- Review NLoC, Comment Density, Cognitive Complexity (CC), and Estimated Hours

**Step 2 — Analyze Changes:**
- Use `diff` with `output: 'signatures'` for structural overview
- Use `diff` with `output: 'full'` when actual code context is needed
- Use judgment: signatures alone are often insufficient for meaningful understanding

**Step 3 — Classify & Adjust:**
For each changed file, determine scope and adjust estimates. Assume **no prior auditor context**.

**Scope:** Apply categories and scope defaults (see references).

**Context burden:** Use `call_chains` to see where touched functions appear in call chains:
- *Isolated* (leaf node, minimal callers, self-contained) → no adjustment
- *Integrated* (multiple paths, shared state, affects invariants) → increase estimate
- *Escalate*: If paths are insufficient, read unchanged files to understand context surface

**Adjust:** Apply domain multipliers where needed (see Domain Multipliers reference).

**Step 4 — Report:**
Present summary table:
| File | Category | Scope | Approach | NLoC | Comment Density | CC | Adjusted Hours |
|------|----------|-------|----------|------|-----------------|-----|----------------|

- **Approach:** `full` (added files, audit entire file) or `diff` (modified files, audit changes only)

Include:
- Adjustments with justification
- Concern Questions for unclear scope

**CHECKPOINT:** "Do you agree with this scope? Proceed to next chunk?"
</diff_triage_instructions>

---

<reflect_instructions>
### REFLECT

**TRIGGER:** METRICS complete (full scope) OR all DIFF-TRIAGE chunks confirmed (diff scope).
**CHECKPOINT:** "Does this estimate look right to you? Should I adjust anything before I write the report?"
**NEXT:** User confirms → REPORT.

**Goal:** Step back from the per-file detail and assess whether the overall estimate is credible.

**Step 1 — Reflect on the full picture:**
- **Proportionality:** Does the total effort feel proportional to the complexity you observed across the codebase?
- **Hard files:** Were there files you found genuinely difficult to follow? Do their hours reflect that difficulty?
- **Depth:** Would the estimated days give an auditor enough time to probe invariants and edge cases — not just read the code?

**Step 2 — Revise or flag:**
For each concern identified, either:
- Revise the estimate on the spot with a short justification, or
- Flag it as an open question for the user to decide

**Step 3 — Present and stop:**
Summarize your reflection and any revisions. Then ask the checkpoint question and wait.
</reflect_instructions>

---

<report_instructions>
### REPORT

**TRIGGER:** User confirms after REFLECT.

Ask: "Would you like a **detailed report** or a **condensed version** (e.g. for Slack)?"

Then produce the chosen format.

---

**Detailed Report:**

**1. Headline:**
- Full scope: "Audit Estimation - <Repository Name>"
- Diff scope: "Audit Estimation - <Repository Name> (<base>...<head>)"

**2. Summary:**
- High-level overview of the repository
- Diff scope: Focus on nature of changes

**3. Chunks Overview:**
- For each chunk: brief description of purpose
- Diff scope: What changed in each chunk

**4. Detailed Table (in-scope files only):**

| Chunk | File Path | Category | NLoC | Comment Density | Complexity | Estimated Hours |
|-------|-----------|----------|------|-----------------|------------|-----------------|

- Diff scope: Add **Approach** column (`full` for added files, `diff` for modified)
- Use adjusted estimates from METRICS (full) or DIFF-TRIAGE (diff)

**5. Adjustments Summary:**
If any adjustments were made, list them:
```
File: <path>
Multiplier: <Nx>
Adjusted Hours: <X hours>
Reason: <justification>
```

**6. Totals:**
- Total NLoC (diff NLoC for diff scope)
- Total Estimated Hours
- Total Estimated Days

**7. Required Domain Expertise:**
- Languages and ecosystems (e.g. Solidity/EVM, Rust/Substrate)
- Protocol knowledge (e.g. AMM mechanics, lending invariants, ZK proof systems)
- Any specialised skills flagged during analysis (e.g. assembly, cryptographic primitives)

**8. Risks & Recommendations:**
- Proposed timeline and order of execution
- Highlighted concerns:
  - Diff scope: removed functions, new entry points, high-complexity changes
  - Full scope: high-risk areas, complex interactions, areas needing extra attention

---

**Condensed Report (Slack-friendly):**

Plain prose, no markdown headings or tables. Use Slack bold (`*text*`) only.

```
*[Repo] — Audit Estimation*

X days (Y hours)

[2-3 sentences: what the codebase does, what was scoped, overall complexity.]

*Challenges:* [key difficulty factors — crypto, novel protocol, missing docs, etc.]

*Required expertise:* [languages, domain knowledge, any specialist skills needed]
```
</report_instructions>
</phase_instructions>
