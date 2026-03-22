---
name: aget-create-project
description: Create research projects with context-aware scaffolding. Reads AGET identity, searches prior work, pre-populates Due Diligence. Use when starting any formal AGET project.
---

# /aget-create-project

Create a new AGET project with research-informed scaffolding per PROJECT_PLAN_AGET_CREATE_PROJECT_V2.md.

## Input

$ARGUMENTS

## Mode Detection

| Input Pattern | Mode | Behavior |
|---------------|------|----------|
| Empty or blank | **Interactive** | Prompt for type and name |
| `<type> <name>` | **Explicit** | Create project of specified type |
| `<topic>` only | **Inference** | Infer type from topic and AGET domain |
| Input contains evidence statements (interview data, gap analysis, L-doc citations, cross-reference synthesis) | **Evidence-rich** | Abbreviated research phase — use provided evidence, skip redundant searches |

### Evidence-Rich Mode

**Detection**: Input contains 2+ of: specific L-doc references (L###), quantitative data (percentages, counts, session numbers), named sources (supervisor interviews, audit results), or cross-reference synthesis ("both supervisors agree...").

**Behavior**: Research Phase (Step 3) still executes per C-CP-003, but in abbreviated form:
- Step 3.1 (identity): **Runs** — always needed for project context
- Step 3.2 (L-docs): **Abbreviated** — search only L-docs explicitly cited in input, don't broad-search by topic keywords
- Step 3.3 (sessions): **Abbreviated** — note current session only (evidence was gathered in-session)
- Step 3.4 (similar projects): **Runs** — conflict check always needed
- Step 3.5 (vocabulary): **Runs** — vocabulary grounding always needed

**Rationale**: When the user provides rich evidence context (e.g., from supervisor interviews or gap analysis conducted in the same session), broad keyword searches duplicate work already done. The abbreviated research phase respects C-CP-003 (research is NOT skipped) while avoiding redundancy.

## Supported Project Types

| Type | Template | Output Location |
|------|----------|-----------------|
| `research` | `templates/poc/RESEARCH_PROJECT_PLAN.template.md` | `planning/PROJECT_PLAN_<NAME>.md` |
| `poc` | `templates/poc/PROPOSAL.template.md` | `planning/poc-proposals/POC-XXX-<name>.md` |

## Project Creation Process

### Step 0: Scope-Fit Validation (#295)

**Purpose**: Verify the proposed project falls within this agent's domain and scope boundaries before investing in research or scaffolding.

1. Read `.aget/identity.json` — extract `domain`, `north_star`, `archetype`
2. Read `governance/SCOPE_BOUNDARIES.md` — extract in-scope and out-of-scope areas
3. Evaluate alignment between the project topic and the agent's domain/scope
4. If **misaligned**: WARN with explanation and allow user override:
   ```
   WARN: Scope-fit concern.
   Project topic: "<topic>"
   Agent domain: "<domain from identity.json>"
   Concern: <specific misalignment>

   Override? The principal may proceed if this is intentional.
   ```
5. If **aligned**: proceed silently (no output needed)

**Rationale**: L616 — projects created outside an agent's domain waste effort and produce artifacts that don't integrate with the KB. Scope-fit validation is the cheapest possible check (2 file reads) with the highest leverage.

### Step 1: Input Analysis

Parse $ARGUMENTS to determine:
- Project type (research, poc, or infer from topic)
- Project name
- If empty in interactive mode, prompt user

**Headless mode**: If no arguments and headless, return error:
```
Error: Project type and name required in headless mode.
Usage: /aget-create-project <type> <name>
Types: research, poc
```

### Step 2: Conflict Check

Check for existing project:
```bash
ls planning/ | grep -qi "<name>"
```

If project exists, WARN and ask for confirmation before proceeding.

### Step 3: Research Phase (KEY DIFFERENTIATOR)

Before scaffolding, gather AGET context:

#### 3.1 Read AGET Identity
```bash
cat .aget/identity.json
```
Extract:
- `north_star`: Agent's purpose
- `domain`: Research focus areas
- `archetype`: Agent type

#### 3.2 Search Relevant L-docs
```bash
grep -l "<topic_keywords>" .aget/evolution/*.md
```
For each found L-doc, extract:
- L-doc ID and title
- Key lesson
- Application to this project

#### 3.3 Search Prior Sessions
```bash
grep -l "<topic_keywords>" sessions/*.md
```
Note related sessions for Traceability.

#### 3.4 Search Similar Projects
```bash
grep -l "<topic_keywords>" planning/PROJECT_PLAN_*.md
```
If similar project exists, WARN about potential duplication.

#### 3.5 Extract Vocabulary Terms
```bash
grep -B2 -A5 "<topic_keywords>" specs/CLI_VOCABULARY.md
```
Identify vocabulary terms for Traceability section.

### Step 3.6: Spec-First Conformance Baseline (L616, L617, #313)

**Purpose**: If the project targets a spec-governed artifact, read the governing spec and create a conformance baseline BEFORE designing gates. This enforces deductive (spec conformance) before inductive (peer comparison) planning per MP-1.

1. Determine if the project will create or modify a spec-governed artifact
2. If **spec-governed**:
   a. Read the governing spec (e.g., `aget/specs/AGET_PROJECT_PLAN_SPEC.md`)
   b. Extract all SHALL/SHOULD requirements relevant to the target artifact
   c. Create a conformance matrix: requirement ID → current status (met/unmet/partial)
   d. Include the conformance matrix in Phase -1 of the scaffolded plan
   e. Design gates to address unmet requirements in priority order (SHALL before SHOULD)
3. If **greenfield** (no governing spec exists):
   a. Note "No governing spec identified — greenfield project" in Phase -1
   b. Proceed to Step 3.7

**Rationale**: L617 — inductive planning (looking at peer projects for gate structure) bypasses spec conformance. The spec defines what the artifact MUST do; gates should be derived from spec requirements, not from what similar projects did.

### Step 3.7: ADR-008 Precondition Check (#313)

**Purpose**: Verify the ADR-008 prerequisite chain is satisfied before creating a plan that assumes infrastructure exists.

**ADR-008 ordering**: L-doc evidence → SOP → Spec → Skill/Tool (Generator)

1. Determine the artifact type the project will produce (SOP, spec, skill, template, etc.)
2. Check prerequisites for that artifact type:
   - **Skill**: requires governing spec + SOP to exist
   - **Spec**: requires SOP or L-doc evidence to exist
   - **SOP**: requires L-doc evidence (2+ executions or 3+ L-docs per L436)
   - **L-doc**: no prerequisites (generates evidence)
   - **Research project**: exempt (generates the evidence other types require)
3. If **prerequisites missing**: WARN with specific gaps:
   ```
   WARN: ADR-008 precondition gap.
   Target artifact: <type>
   Missing prerequisite(s):
   - <missing item 1>
   - <missing item 2>

   Consider: Create prerequisites first, or note gap in project plan.
   ```
4. If **prerequisites met**: proceed silently

**Rationale**: L624 — skills modified without SOPs or specs create governance gaps. ADR-008 defines the progression; this step enforces it structurally.

### Step 3.8: Artifact Type Fitness Assessment (#315)

**Purpose**: Cross-reference the proposed artifact type with the domain's ADR-008 maturity level to assess fitness.

1. Identify the proposed artifact type and its domain
2. Assess domain maturity:
   - **Mature domain** (3+ L-docs, SOP exists, spec exists): any artifact type appropriate
   - **Emerging domain** (1-2 L-docs, no SOP/spec): recommend research project or L-doc first
   - **Novel domain** (0 L-docs): recommend research project only
3. If **artifact type exceeds domain maturity**: WARN with recommendation:
   ```
   WARN: Artifact type may exceed domain maturity.
   Proposed: <artifact type> (requires <ADR-008 level>)
   Domain maturity: <assessment> (<N> L-docs, <SOP status>, <spec status>)

   Recommendation: Consider <lower-level artifact> first to build evidence base.
   ```
4. If **appropriate**: proceed silently

**Rationale**: L617, ADR-008 — creating a spec for a domain with no L-doc evidence produces speculative requirements. Maturity assessment prevents premature abstraction (L103).

### Step 4: Template Selection and Scope Estimation (#391)

**4a: Scope Estimation** (before template routing):

Estimate project scope based on deliverables, complexity, and evidence from research phase:
- **Small** (<1 day): Single artifact, few gates, well-understood domain
- **Medium** (<2 weeks): Multiple artifacts, 3-5 gates, some research needed
- **Large** (2+ weeks): Cross-cutting changes, 5+ gates, significant research

If scope suggests a **smaller template** would be more appropriate (e.g., a 1-day task routed to RESEARCH_PROJECT_PLAN):
```
WARN: Scope-template mismatch.
Estimated scope: <Small / Medium / Large>
Selected template: <template name>
Concern: <e.g., "Small scope may not warrant full research project structure">

Note: Smaller templates (GATE_PLAN, ENHANCEMENT_PLAN) are not yet available.
Proceeding with current template. Consider simplifying gate structure.
```

**4b: Template Verification**:

Verify template exists:
```bash
test -f templates/poc/RESEARCH_PROJECT_PLAN.template.md
```

If template missing, STOP with error:
```
Error: Template not found: templates/poc/RESEARCH_PROJECT_PLAN.template.md
Cannot create project without template.
```

### Step 4.5: Template Spec-Conformance Verification

**Purpose**: Prevent scaffolding from a template that violates its governing spec (L644).

1. Read the selected template
2. Check for `**Governing Spec**:` field in the header
3. If `Governing Spec:` is present:
   a. Read the referenced spec (e.g., `aget/specs/AGET_PROJECT_PLAN_SPEC.md`)
   b. Identify all SHALL requirements for plan sections
   c. Verify the template includes a section or placeholder for each SHALL requirement
   d. If template violates any SHALL requirement, STOP with error:
   ```
   Error: Template violates governing spec.
   Template: templates/poc/RESEARCH_PROJECT_PLAN.template.md
   Governing Spec: AGET_PROJECT_PLAN_SPEC v1.2.0
   SHALL violations:
   - [list each missing section and CAP requirement]
   Cannot scaffold from a non-conformant template.
   ```
4. If `Governing Spec:` is absent, WARN and proceed (template predates this check)

**Rationale**: L644 found that template-spec drift is silent — the template IS the agent's model of compliance. This step catches drift before it propagates to new plans.

### Step 5: Scaffold Generation

Read template and populate:

#### 5.1 Header
```markdown
**Version**: 1.0.0
**Status**: Phase -1 (Due Diligence)
**Created**: <today's date>
**Author**: <AGET name from identity.json>
**Template**: `templates/poc/RESEARCH_PROJECT_PLAN.template.md`
```

#### 5.2 Hypothesis
Generate hypothesis ID: `H-<PREFIX>-000` where PREFIX is derived from project name.

#### 5.3 Phase -1 (Pre-populated)
Fill L-doc Review table with results from Step 3.2:
```markdown
| L-doc | Title | Key Lesson | Application |
|-------|-------|------------|-------------|
| <from research> | <from research> | <from research> | <from research> |
```

#### 5.4 Traceability
Include:
- Template reference
- Vocabulary terms from Step 3.5
- Related L-docs from Step 3.2
- Related sessions from Step 3.3
- Identity reference

### Step 6: Write Output

Write to appropriate location:
- Research: `planning/PROJECT_PLAN_<NAME>.md`
- POC: `planning/poc-proposals/POC-XXX-<name>.md`

### Step 7: Report

Output summary:
```markdown
## Project Created: <name>

**Type**: <type>
**Location**: <output path>

**Research Summary**:
- Identity: <north_star excerpt>
- Related L-docs: <count> found
- Related sessions: <count> found
- Similar projects: <count> found (warnings if any)

**Pre-populated**:
- Phase -1: L-doc Review table filled
- Traceability: Vocabulary and L-doc links added

**Next Steps**:
1. Review generated project plan
2. Refine hypothesis statement
3. Execute Phase -1 due diligence checklist
```

### Step 7.5: Post-Scaffolding Self-Verification

**Purpose**: Prevent the "describing a principle ≠ applying it" failure (L644, Descriptive Compliance anti-pattern).

1. If the created plan has a `Governing Spec:` field:
   a. Verify the plan includes ALL sections present in the template (no sections dropped during scaffolding)
   b. Verify completion sections are present: Retrospective, Closure Checklist, Velocity Analysis, Finalization Checklist
   c. Verify Success Metrics uses the spec-required column format
2. If any section is missing, add it before writing the output
3. Report verification result in Step 7 summary:
   ```
   **Self-Verification**: PASS (all template sections present in scaffolded plan)
   ```
   or:
   ```
   **Self-Verification**: FIXED (added missing sections: [list])
   ```

### Step 8: Principle-Aware Gate Ordering Check

**Purpose**: Verify the scaffolded plan's gates follow spec-first → verification → coherence ordering (MP-1, L617).

1. Review the gate structure in the scaffolded plan
2. Verify ordering follows this precedence:
   - **Gate -1**: Governing spec verification (deductive, spec-first) — MUST come first
   - **Gate 0**: Evidence/prerequisite collection
   - **Implementation gates**: Actual work deliverables
   - **Verification gates**: Conformance checks, V-tests
   - **Coherence gates**: Cross-artifact alignment
   - **Integration gates**: Traceability, tracking, closure
3. If **ordering violates spec-first**: WARN with specific issue:
   ```
   WARN: Gate ordering concern.
   Issue: <specific ordering problem>
   Expected: Spec verification (Gate -1) → evidence → implementation → verification → coherence → integration
   Found: <actual ordering>

   Recommendation: Reorder gates to follow spec-first principle.
   ```
4. If **ordering is correct**: proceed silently

**Rationale**: L617 — inductive planning produces gates ordered by discovery sequence (what we found first), not by principle (what we should verify first). This check catches the pattern structurally.

## Output Format

```markdown
## Project Created: <name>

**Type**: research
**Location**: planning/PROJECT_PLAN_<NAME>.md

**Research Summary**:
- Identity: CLI agent subsystem research
- Related L-docs: 5 found
- Related sessions: 2 found
- Similar projects: 0 found

**Pre-populated**:
- Phase -1: L-doc Review table filled with 5 entries
- Traceability: 3 vocabulary terms, 5 L-doc links

**Next Steps**:
1. Review generated project plan
2. Refine hypothesis statement
3. Execute Phase -1 due diligence checklist
```

## Constraints

These are INVIOLABLE - you MUST NOT violate these constraints:

1. **NEVER** scaffold from a template that violates SHALL requirements of its governing spec (L644)
2. **NEVER** create project without valid template
3. **NEVER** overwrite existing project without explicit confirmation
4. **NEVER** modify specs/, governance/, or .aget/ directly
5. **NEVER** skip the Research Phase (Step 3)
6. **NEVER** create project in headless mode without explicit type and name
7. **DO** read .aget/identity.json before scaffolding
8. **DO** search for relevant L-docs and include in Phase -1
9. **DO** warn about similar existing projects
10. **DO** include Traceability section with vocabulary links
11. **DO** use prohibitive form for constraints per L561
12. **NEVER** scaffold a plan with gates ordered implementation-first when a governing spec exists — spec verification gate (Gate -1) MUST precede implementation gates (L617)
13. **DO** check scope-fit against identity.json and SCOPE_BOUNDARIES.md before investing in research (Step 0)
14. **DO** read the governing spec for the target artifact and create a conformance baseline before designing gates, when a governing spec exists (Step 3.6, MP-1)

## Rationale

Per AGET theoretical grounding:
- **Stigmergy** (Grasse): Project artifacts enable cross-session coordination
- **Extended Mind** (Clark/Chalmers): Research phase extends agent's project-creation capability with prior knowledge
- **Evidence-First Design** (L289): Research before scaffolding
- **Ontology-Driven Creation** (L481): Vocabulary terms inform project structure

Per AGET governance principles:
- **MP-1 (Spec-First + Verification)**: Steps 3.6 and 8 enforce deductive (spec conformance) before inductive (peer comparison) planning. Gate -1 is standard for all project types.
- **MP-5 (Infrastructure Over Memory)**: Steps 0, 3.6-3.8, and 8 embed critical principles as structural gates, not passive CLAUDE.md warnings. This moves the skill from ADR-008 Advisory to Strict for principle enforcement.
- **ADR-008 (Advisory → Strict → Generator)**: Step 3.7 verifies the prerequisite chain (L-doc → SOP → Spec → Skill) is satisfied before creating artifacts that assume infrastructure exists.

This skill implements the "research-informed project creation" pattern per PROJECT_PLAN_AGET_CREATE_PROJECT_V2.md, enhanced with principle enforcement per PROJECT_PLAN_create_project_principles_enforcement_v1.0.md (D62).


### Step 9: Skill Completion Signal (D71 Layer 3)

**Purpose**: Make skill execution completeness structurally visible. If this signal is absent from the skill output, the skill execution is incomplete.

The skill MUST output this signal as the LAST section of the report:

```markdown
## Skill Completion Signal
**Self-Verification**: PASS | FIXED (N items) | FAIL (items: [list])
**Gate Ordering**: PASS | WARN (issue: [description])
**Steps Completed**: 0→1→2→3→3.6→3.7→3.8→4→4.5→5→6→7→7.5→8→9
```

If Step 7.5 or Step 8 were skipped or failed, the signal MUST report FAIL with the specific items.

**Enforcement**: Strict (ADR-008, D71). Signal absence = incomplete execution.

## Traceability

| Link | Reference |
|------|-----------|
| Vocabulary | Project, Agent_Skill, AGET_Skill (CLI_VOCABULARY.md) |
| Requirements | R-SKILL-006-001 through R-SKILL-006-021 |
| Skill Spec | SKILL-006 |
| SOP | SOP_skill_enhancement.md |
| Template | templates/poc/RESEARCH_PROJECT_PLAN.template.md (v1.5.0) |
| L-docs | L474, L561, L567, L582, L584, L616 (spec-first gate failure), L617 (inductive planning bypass), L618 (citing lesson while repeating), L620 (template structural completeness), L644 (template-spec conformance) |
| Issues | #295 (Step 0), #313 (Steps 3.6/3.7), #315 (Step 3.8), #391 (Step 4 scope estimation), #356 (template Gate -1 — addressed in template v1.5.0), #382 (validator — partial, see D24) |
| Governance | MP-1 (Spec-First + Verification), MP-5 (Infrastructure Over Memory), ADR-008 (Advisory → Strict → Generator) |
| Project | PROJECT_PLAN_AGET_CREATE_PROJECT_V2.md |
| Remediation | PROJECT_PLAN_create_project_principles_enforcement_v1.0.md (D62) |
| Hypotheses | H-ACP-000 through H-ACP-006, H-CPE-001 |
