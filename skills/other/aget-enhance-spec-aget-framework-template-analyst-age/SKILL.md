---
name: aget-enhance-spec
description: Guide through the 7-phase specification enhancement lifecycle (Phases 0-6 from L622). Governs creating, updating, wiring, and validating AGET specifications.
version: 1.1.0
---

# /aget-enhance-spec

Guide agents through the core specification enhancement lifecycle. Provides governed workflow for spec creation, updates, cross-reference wiring, and validation.

## Purpose

Replace ad-hoc specification enhancement with a repeatable, governed 7-phase process derived from 5 independent plans across 3 agents (L622). This is the Generator layer (ADR-008 step 3), built on SOP_specification_enhancement.md (Advisory) and SKILL-041 spec (Strict).

## Input

$ARGUMENTS - Enhancement category and optional spec path.

Format: `<CATEGORY> [spec-path] [--version <target-version>]`

Categories: NEW, UPDATE, ADD-REQ, WIRE, CONSOLIDATE, DEPRECATE

Examples:
- `/aget-enhance-spec NEW specs/AGET_FOO_SPEC.md`
- `/aget-enhance-spec UPDATE aget/specs/AGET_SOP_SPEC.md --version 1.2.0`
- `/aget-enhance-spec WIRE aget/specs/SKILL_NAMING_CONVENTION_SPEC.md`
- `/aget-enhance-spec ADD-REQ aget/specs/AGET_SOP_SPEC.md`

## Phase Selection

Not all categories require all phases. Use this table to determine which phases to execute:

| Category | Required Phases |
|----------|:---------------:|
| NEW | 0, 1, 2, 3, 4, 5, 6 (all) |
| UPDATE | 0, 1, 2, 3, 4, 5, 6 (all) |
| ADD-REQ | 0, 1, 2, 3, 4, 5, 6 |
| WIRE | 0, 1, 5, 6 |
| CONSOLIDATE | 0, 1, 2, 3, 4, 5, 6 + reference SOP_specification_consolidation.md |
| DEPRECATE | 0, 1, 3, 6 |

## Execution

### Step 1: Parse Input

```
IF no arguments provided:
  Prompt: "What type of enhancement? (NEW, UPDATE, ADD-REQ, WIRE, CONSOLIDATE, DEPRECATE)"
  Prompt: "Path to spec? (leave blank for NEW)"

IF category not in valid list:
  Error: "Invalid category. Valid: NEW, UPDATE, ADD-REQ, WIRE, CONSOLIDATE, DEPRECATE"

IF category in (UPDATE, ADD-REQ, WIRE) AND no spec path:
  Error: "Spec path required for {category} enhancements"
```

Determine phase list from Phase Selection table above.

### Step 2: Phase 0 — Trigger & Diagnosis

**Objective**: Identify the specification gap and gather evidence.

Execute:
1. If spec path provided, read the spec file and extract current version, status, requirement count
2. Search for related L-docs:
   ```bash
   grep -l "<topic_keywords>" .aget/evolution/L*.md
   ```
3. Search for related specs:
   ```bash
   ls specs/ aget/specs/ 2>/dev/null | grep -i "<topic>"
   ```
4. Document findings as evidence table:
   ```
   | Evidence | Source | Impact |
   |----------|--------|--------|
   | <finding> | <L-doc or spec> | <why this matters> |
   ```

5. **Governance classification** (L624, R-ENHANCE-SPEC-031/032):
   ```
   Determine governance level:
   IF spec path is under aget/ or aget-framework/ (public):
     IF category is UPDATE or NEW:
       REQUIRE: PROJECT_PLAN before proceeding past Phase 0
       Check: does PROJECT_PLAN exist for this enhancement?
       IF not: "PROJECT_PLAN required for public framework UPDATE/NEW. Create one first."
     ELSE (ADD-REQ, WIRE):
       Enhancement_Decision_Log (produced at Step 9) is sufficient
   ELSE (private agent spec):
     Enhancement_Decision_Log is sufficient
   ```

**USER CHECKPOINT**: Present evidence table and governance level, then ask:
```
Enhancement Category: <CATEGORY>
Target: <spec path or "new spec">
Evidence: <count> sources found
Governance: <PROJECT_PLAN required | Enhancement_Decision_Log sufficient>

Confirm category and proceed? (yes/adjust category/abort)
```

**Exit Criteria**: Category confirmed. Evidence documented. Gap clearly stated. Governance level determined.

### Step 2.5: Phase 0.5 — Maturity Assessment (L682)

**Objective**: Score the target spec's current maturity level to inform enhancement scope.

Execute:
1. If spec exists (UPDATE, ADD-REQ, WIRE), assess against RUBRIC_specification_maturity_v1.0:
   ```
   Content:     C_ (0=Implicit, 1=Intent, 2=Structured, 3=Grounded, 4=Verified, 5=Wired)
   Enforcement: E_ (0=Unenforceable, 1=Advisory, 2=Detectable, 3=Preventable, 4=Structural)
   Adoption:    A_ (0=Unaware, 1=Aware, 2=Compliant, 3=Internalized, 4=Forward)
   Process:     P_ (0=Ad-hoc, 1=Documented, 2=Procedural, 3=Specified, 4=Automated)
   Governance:  G_ (0=Ungoverned, 1=Tracked, 2=Planned, 3=Governed, 4=Auditable)
   ```
2. Identify the **constraining dimension** (lowest level)
3. For NEW specs, record baseline as C0/E0/A0/P0/G0
4. Note target maturity profile for this enhancement (what level should each dimension reach?)

Present:
```
Current Maturity: C_/E_/A_/P_/G_ (effective: L_)
Constraining Dimension: [dimension] at level [N]
Target After Enhancement: C_/E_/A_/P_/G_
```

**Note**: This phase is informational — it guides effort allocation but does not gate progression. Skip if spec doesn't exist yet (NEW category without prior version).

### Step 3: Phase 1 — Governing Spec Verification

**Objective**: Read governing spec(s) before modifying anything.

Execute:
1. Identify governing spec(s) for the artifact type:
   - Skill specs → read SKILL_NAMING_CONVENTION_SPEC (in `aget/specs/`; note: AGET_SKILLS_SPEC is archived)
   - SOPs → read AGET_SOP_SPEC
   - General specs → read AGET_SPEC_FORMAT (if exists)
2. Read each governing spec — extract specific requirements (CAP-xxx-nnn)
3. Verify cross-reference targets in governing spec are not stale:
   ```bash
   # For each referenced file in the governing spec
   test -f "<referenced_path>" && echo "OK" || echo "STALE: <path>"
   ```
4. If stale targets found, flag for remediation at Phase 5a

**Anti-Pattern Check**: Decorative Spec Basis
- After reading governing spec, verify you can cite specific CAP requirements
- If you declared a spec basis but can't cite specific requirements → STOP and re-read

**Exit Criteria**: Governing spec(s) read and cited. Cross-reference targets verified.

### Step 4: Phase 2 — Census & Classification

**Objective**: Inventory all artifacts that need enhancement.

Execute:
1. Enumerate all specs/artifacts in scope
2. For each artifact, read the file to get current version and status (NEVER assert from memory — L611)
3. Identify dependency order
4. Produce census table:
   ```
   | Artifact | Current Version | Category | Dependencies | Priority |
   |----------|:---------------:|----------|--------------|:--------:|
   | <spec path> | <from file read> | <category> | <specs it references> | <1-N> |
   ```

**USER CHECKPOINT**: Present census table and ask:
```
Census: <count> artifacts in scope
Dependencies: <dependency chain summary>

Approve census and proceed? (yes/add artifact/remove artifact/abort)
```

**Exit Criteria**: All artifacts inventoried. Dependencies mapped. Priority assigned.

### Step 5: Phase 3 — Draft/Update Spec

**Objective**: Write or update the specification content.

Execute:
1. Update spec header (version, status, date)
2. Write requirements in EARS patterns:
   - Ubiquitous: `The SYSTEM shall...`
   - Conditional: `IF condition THEN the SYSTEM shall...`
   - Event-driven: `WHEN event THEN the SYSTEM shall...`
   - Optional: `WHERE condition, the SYSTEM should...`
   - Prohibited: `The SYSTEM shall NOT...`
   - Unwanted: `artifact shall NOT...`
3. Assign unique requirement IDs: R-{DOMAIN}-{NNN}
4. If new vocabulary terms introduced, add SKOS vocabulary section
5. If applicable, use "codify existing behavior" approach (fastest — L622 evidence)

**USER CHECKPOINT**: Present draft spec content and ask:
```
Spec: <path>
Version: <current> → <target>
Requirements: <count> total (<new_count> new, <modified_count> modified)

Review spec content. Approve and proceed? (yes/edit/abort)
```

**Exit Criteria**: Spec content written. All requirements have IDs and EARS patterns.

### Step 6: Phase 4 — Structural Validation

**Objective**: Verify spec meets structural requirements.

Execute:
1. Check required sections present per governing spec format
2. Check naming conventions
3. Validate EARS pattern compliance for all requirements:
   ```
   For each requirement:
   - Has unique R-{DOMAIN}-{NNN} ID? ✓/✗
   - Uses EARS pattern keyword? ✓/✗
   - Pattern type recorded? ✓/✗
   ```
4. Verify version number follows semantic versioning
5. Run structural validators if available:
   ```bash
   python3 .aget/patterns/sync/validate_spec_compliance.py <spec_path> 2>/dev/null
   ```

Report results:
```
Structural Validation: <PASS/FAIL>
  Sections: <count>/<expected> present
  Requirements: <count> with valid EARS patterns
  Naming: <PASS/FAIL>
  Version: <PASS/FAIL>
  Validator: <PASS/FAIL/not available>
```

**Exit Criteria**: Spec passes structural validation. No format errors.

### Step 7: Phase 5 — Cross-Reference Wiring

**Objective**: Connect spec to related artifacts with bidirectional traceability.

#### Phase 5a: Stale Artifact Remediation

Before wiring, verify all targets are current:
```
For each cross-reference target:
1. File exists? ✓/✗
2. Version/status current? ✓/✗
3. If stale → flag for update before wiring
```

If stale targets found, present remediation plan before proceeding.

#### Phase 5b: Primary Cross-Wiring

For each requirement:
1. Link to evidence L-doc(s) — why does this requirement exist?
2. Link to V-test — how is this requirement enforced?
3. Link to related specs (broader/narrower/related)

Produce cross-reference report:
```
| Requirement | Evidence (L-doc) | Enforcement (V-test) | Related Specs |
|-------------|-----------------|---------------------|---------------|
| R-XXX-001 | L### | V-XXX-001 | SPEC_Y |
```

#### Phase 5c: Bidirectional Verification

For each outgoing reference, verify target acknowledges this spec.
For each incoming reference, verify this spec acknowledges source.

**USER CHECKPOINT**: Present cross-reference report and ask:
```
Cross-References: <count> requirements mapped
Stale targets: <count> (remediated: <count>)
Bidirectional gaps: <count>

Approve wiring and proceed? (yes/fix gaps/abort)
```

**Exit Criteria**: All requirements trace to evidence and enforcement. Bidirectional references verified.

### Step 8: Phase 6 — Self-Compliance Check

**Objective**: Verify the enhancement complies with its own specs.

Execute — these checks are MANDATORY (C3 — no skip option):

1. **Bootstrapping paradox check** (L560):
   - Does the spec enhancement comply with the lessons it references?
   - Does the output comply with its own requirements?
   ```
   For each R-requirement in the spec:
   - Does this enhancement process follow this requirement? ✓/✗
   ```

2. **Spec self-compliance**:
   - Does the spec meet the format requirements of its governing spec?

3. **Vocabulary compliance**:
   - Are all terms used consistently with controlled vocabulary?

Report:
```
Self-Compliance Check:
  Bootstrapping paradox: <PASS/FAIL — details>
  Spec self-compliance: <PASS/FAIL — details>
  Vocabulary compliance: <PASS/FAIL — details>
  Overall: <PASS/FAIL>
```

**USER CHECKPOINT**: Present compliance results and ask:
```
Self-compliance: <PASS/FAIL>
<details of any failures>

Acknowledge results? (acknowledge/fix and re-check/abort)
```

**Exit Criteria**: Self-compliance confirmed. No bootstrapping paradox detected.

### Step 9: Produce Outputs

Generate final deliverables:
1. **Updated/New Spec**: The spec file (already written in Phase 3, validated in Phase 4)
2. **Cross-Reference Report**: From Phase 5b (formatted table)
3. **Enhancement Decision Log**:
   ```
   Enhancement Decision Log:
     Category: <category>
     Governing Spec: <spec> (CAP citations: <list>)
     Census: <count> artifacts
     Requirements: <count> (EARS: <breakdown>)
     Self-Compliance: <PASS/FAIL>
     Completed Phases: <list>
     Skipped Phases: <list with justification>
   ```
4. **Stale Artifact Report**: From Phase 5a (if any)

Present summary:
```
=== /aget-enhance-spec Complete ===

Category: <CATEGORY>
Target: <spec path>
Version: <previous> → <new>
Requirements: <count>
Cross-References: <count> mapped
Self-Compliance: <PASS/FAIL>
Phases Executed: <list>

Outputs:
  - Spec: <path>
  - Cross-Ref Report: <inline or path>
  - Decision Log: <inline>
```

## Constraints

These are INVIOLABLE — you MUST NOT violate these constraints:

1. **C1**: NEVER skip Phase 1 (Governing Spec Verification)
2. **C2**: NEVER assert spec state from memory — always read files (L611)
3. **C3**: NEVER skip Phase 6 (Self-Compliance Check) — no skip option exists
4. **C4**: NEVER execute deployment phases 7-10 (template, tooling, fleet, post-deploy)
5. **C5**: ALWAYS present user checkpoint before proceeding past Phases 0, 2, 3, 5, 6
6. **C6**: ALWAYS produce cross-reference report as output
7. **C7**: ALWAYS cite governing spec requirements (CAP-xxx-nnn) in deliverables
8. **C8**: ALWAYS use EARS patterns for requirements
9. **C9**: ALWAYS assign unique R-{DOMAIN}-{NNN} IDs to requirements

## Anti-Pattern Detection

The skill actively checks for these anti-patterns:

| Anti-Pattern | Phase | Detection |
|--------------|:-----:|-----------|
| Decorative Spec Basis | 1 | Spec basis declared but no CAP citations in deliverables |
| Memory-Based Assertions (L611) | 2 | Version/status claimed without file read |
| Bootstrapping Paradox (L560) | 6 | Output violates its own requirements |
| Certainty Bias (L555) | 6 | Self-compliance check skipped |
| ADR-008 Progression Skip | 0 | Generating skill artifacts without SOP/spec layers |

## Related Skills

- `/aget-create-project` — Create project plan for enhancement work
- `/aget-propose-skill` — Propose new skills (used in this project at G3)
- `/aget-record-lesson` — Capture lessons discovered during enhancement
- `/aget-review-project` — Review enhancement project progress
- `/aget-study-topic` — Research topic before enhancing


### Step 10: Skill Completion Signal (D71 Layer 3)

**Purpose**: Make skill execution completeness structurally visible. If this signal is absent, the skill execution is incomplete.

The skill MUST output this signal as the LAST section of the report:

```markdown
## Skill Completion Signal
**Self-Compliance**: PASS | FAIL (items: [list])
**Cross-References**: PASS (N mapped) | SKIP (justification)
**Phases Completed**: 0→1→2→3→4→5→6→9→10
```

If Phase 6 (Self-Compliance Check) was not executed, the signal MUST report FAIL. Per C3, Phase 6 has no skip option.

**Enforcement**: Strict (ADR-008, D71). Signal absence = incomplete execution.

## Traceability

| Link | Reference |
|------|-----------|
| Spec | SKILL-041 (`aget/.aget/specs/skills/SKILL-041_aget-enhance-spec.yaml`) |
| SOP | `sops/SOP_specification_enhancement.md` v1.0.0 |
| L-docs | L622 (lifecycle), L623 (meta-governance gap), L560, L557, L555, L611 |
| Proposal | SP-002 (`planning/skill-proposals/PROPOSAL_aget-enhance-spec.md`) |
| Project | `planning/PROJECT_PLAN_aget_enhance_spec_skill_v1.0.md` |
| ADR-008 | L-docs → SOP (Advisory) → Spec (Strict) → Skill (Generator) |
| Verb | "enhance" — 25th approved verb, 4th domain innovation |

---

*aget-enhance-spec v1.1.0*
*Category: Governance*
*ADR-008 Position: Generator (step 3 of Advisory → Strict → Generator)*
*"Five plans, three agents, one skill."*
