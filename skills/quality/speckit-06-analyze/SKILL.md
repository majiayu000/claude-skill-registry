---
name: speckit-06-analyze
description: Validate cross-artifact consistency between spec, plan, and tasks
---

# Spec-Kit Analyze

Perform a non-destructive cross-artifact consistency and quality analysis across spec.md, plan.md, and tasks.md after task generation.

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty).

## Operating Constraints

**STRICTLY READ-ONLY**: Do **not** modify any files. Output a structured analysis report. Offer an optional remediation plan (user must explicitly approve before any editing).

**Constitution Authority**: The project constitution (`.specify/memory/constitution.md`) is **non-negotiable** within this analysis scope. Constitution conflicts are automatically CRITICAL and require adjustment of the spec, plan, or tasks--not dilution, reinterpretation, or silent ignoring of the principle.

## Constitution Loading (REQUIRED)

Before ANY action, load the project constitution:

1. Read constitution:
   ```bash
   cat .specify/memory/constitution.md 2>/dev/null || echo "NO_CONSTITUTION"
   ```

2. If file doesn't exist:
   ```
   ERROR: Project constitution not found at .specify/memory/constitution.md

   STOP - Cannot proceed without constitution.
   Run /speckit-00-constitution first to define project principles.
   ```

3. Extract principle names and MUST/SHOULD normative statements.

## Prerequisites Check

1. Run prerequisites check:
   ```bash
   .specify/scripts/bash/check-prerequisites.sh --json --require-tasks --include-tasks
   ```

2. Parse JSON for `FEATURE_DIR` and `AVAILABLE_DOCS`.

3. Derive absolute paths:
   - SPEC = FEATURE_DIR/spec.md
   - PLAN = FEATURE_DIR/plan.md
   - TASKS = FEATURE_DIR/tasks.md

4. Abort with error if any required file is missing.

## Execution Steps

### 1. Load Artifacts (Progressive Disclosure)

Load only minimal necessary context from each artifact:

**From spec.md:**
- Overview/Context
- Functional Requirements
- Non-Functional Requirements
- User Stories
- Edge Cases

**From plan.md:**
- Architecture/stack choices
- Data Model references
- Phases
- Technical constraints

**From tasks.md:**
- Task IDs
- Descriptions
- Phase grouping
- Parallel markers [P]
- Referenced file paths

### 2. Build Semantic Models

Create internal representations (do not include raw artifacts in output):

- **Requirements inventory**: Each functional + non-functional requirement with stable key
- **User story/action inventory**: Discrete user actions with acceptance criteria
- **Task coverage mapping**: Map each task to one or more requirements or stories
- **Constitution rule set**: Principle names and normative statements

### 3. Detection Passes (Token-Efficient Analysis)

Focus on high-signal findings. Limit to 50 findings total.

#### A. Duplication Detection
- Identify near-duplicate requirements
- Mark lower-quality phrasing for consolidation

#### B. Ambiguity Detection
- Flag vague adjectives (fast, scalable, secure, intuitive, robust) lacking measurable criteria
- Flag unresolved placeholders (TODO, TKTK, ???, `<placeholder>`)

#### C. Underspecification
- Requirements with verbs but missing object or measurable outcome
- User stories missing acceptance criteria alignment
- Tasks referencing files or components not defined in spec/plan

#### D. Constitution Alignment
- Any requirement or plan element conflicting with a MUST principle
- Missing mandated sections or quality gates from constitution

#### E. Phase Separation Violations (CRITICAL)

Check each artifact for content that belongs elsewhere:

**Constitution violations (tech in governance):**
- Programming languages, frameworks, databases mentioned
- Specific tools or versions
- Infrastructure or deployment details

**Spec violations (implementation in requirements):**
- Framework or library references
- API implementation details (REST endpoints, GraphQL schemas)
- Database schemas or table structures
- Architecture patterns (microservices, serverless)
- Code organization or file structures

**Plan violations (governance in technical):**
- Project-wide principles or "laws" (should reference constitution)
- Non-negotiable rules that apply beyond this feature
- Team workflow or process requirements
- Quality standards not specific to this implementation

**Report format:**
```
PHASE SEPARATION VIOLATIONS:
- [CRITICAL] constitution.md line 45: "Use Python 3.11" (tech in governance)
- [CRITICAL] spec.md line 120: "REST API endpoint /users" (impl in spec)
- [HIGH] plan.md line 30: "All code must have tests" (governance in plan)
```

#### G. Coverage Gaps
- Requirements with zero associated tasks
- Tasks with no mapped requirement/story
- Non-functional requirements not reflected in tasks

#### H. Inconsistency
- Terminology drift (same concept named differently across files)
- Data entities referenced in plan but absent in spec (or vice versa)
- Task ordering contradictions
- Conflicting requirements

### 4. Severity Assignment

- **CRITICAL**: Violates constitution MUST, phase separation violation, missing core spec artifact, or requirement with zero coverage that blocks baseline functionality
- **HIGH**: Duplicate or conflicting requirement, ambiguous security/performance attribute, untestable acceptance criterion
- **MEDIUM**: Terminology drift, missing non-functional task coverage, underspecified edge case
- **LOW**: Style/wording improvements, minor redundancy

### 5. Produce Analysis Report

Output a Markdown report (no file writes):

```markdown
## Specification Analysis Report

| ID | Category | Severity | Location(s) | Summary | Recommendation |
|----|----------|----------|-------------|---------|----------------|
| A1 | Duplication | HIGH | spec.md:L120-134 | Two similar requirements ... | Merge phrasing |

**Coverage Summary Table:**

| Requirement Key | Has Task? | Task IDs | Notes |
|-----------------|-----------|----------|-------|

**Phase Separation Violations:** (if any)
| Artifact | Line | Violation | Severity |
|----------|------|-----------|----------|

**Constitution Alignment Issues:** (if any)

**Unmapped Tasks:** (if any)

**Metrics:**
- Total Requirements
- Total Tasks
- Coverage % (requirements with >=1 task)
- Ambiguity Count
- Duplication Count
- Critical Issues Count
```

### 6. Next Actions

At end of report, output a concise Next Actions block:

- If CRITICAL issues exist: Recommend resolving before `/speckit-07-implement`
- If only LOW/MEDIUM: User may proceed, but provide improvement suggestions
- Provide explicit command suggestions

### 7. Offer Remediation

Ask the user: "Would you like me to suggest concrete remediation edits for the top N issues?" (Do NOT apply them automatically.)

## Operating Principles

### Context Efficiency
- **Minimal high-signal tokens**: Focus on actionable findings
- **Progressive disclosure**: Load artifacts incrementally
- **Token-efficient output**: Limit findings table to 50 rows
- **Deterministic results**: Rerunning should produce consistent IDs and counts

### Analysis Guidelines
- **NEVER modify files** (this is read-only analysis)
- **NEVER hallucinate missing sections** (report accurately)
- **Prioritize constitution violations** (always CRITICAL)
- **Use examples over exhaustive rules** (cite specific instances)
- **Report zero issues gracefully** (emit success report with coverage statistics)

## Next Steps

After analysis:
- If CRITICAL issues: Resolve them first, then re-run `/speckit-06-analyze`
- If no CRITICAL issues: Run `/speckit-07-implement` to execute the implementation

The implement skill will perform its own prerequisite checks before proceeding.
