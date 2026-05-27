---
name: dialogue-assess-phase
description: Assess readiness to transition between SDLC phases. Aggregates component assessments and generates PROCEED/PROCEED_WITH_CAUTION/DEFER recommendation. Triggers on "assess phase", "phase readiness", "ready to proceed", "phase transition check", "can we move to phase".
allowed-tools: Bash, AskUserQuestion, Read, Glob
---

# Dialogue: Phase Readiness Assessment

Assess readiness to transition from one SDLC phase to the next. This composite assessment aggregates component assessments and evaluates overall readiness, generating a recommendation that requires human approval.

## Framework Grounding

This skill operationalises:
- **Phase transitions**: 35-55% information loss at transitions requires explicit checkpoints
- **Theory-building**: Validates sufficient understanding exists before proceeding
- **STS joint optimisation**: Human approval ensures both technical and social readiness

## When to Use

Use this skill at phase transition points:
- Phase 1 (Initiation/Conception) → Phase 2 (Planning)
- Phase 2 (Planning) → Phase 3 (Analysis/Requirements)
- Phase 3 (Analysis/Requirements) → Phase 4 (Design/Architecture)
- And so on through Phase 7 (Deployment/Operations)

## Phase Readiness Dimensions

The assessment evaluates four readiness dimensions:

| Dimension | What It Measures | Key Inputs |
|-----------|------------------|------------|
| `documentation_readiness` | Are phase artefacts complete? | Required documents exist |
| `knowledge_transfer_readiness` | Is knowledge documented/shared? | Theory captured, decisions logged |
| `stakeholder_readiness` | Are stakeholders aligned? | Alignment assessment, approvals |
| `technical_readiness` | Are technical prerequisites met? | Tests pass, dependencies resolved |

## Recommendation Outcomes

| Recommendation | Meaning | Action |
|----------------|---------|--------|
| `PROCEED` | All dimensions satisfactory | Human approves, transition proceeds |
| `PROCEED_WITH_CAUTION` | Minor gaps identified | Human reviews gaps, may proceed with mitigations |
| `DEFER` | Significant gaps present | Address blockers before transitioning |

## How to Assess Phase Readiness

### Step 1: Gather Context

First, gather information about the current state:

```bash
# Check for recent problem framing assessment
ls -la ${CLAUDE_PROJECT_DIR}/.dialogue/logs/assessments/ASSESS-*.yaml | tail -5

# Check for recent daily checks
grep -l "assessment_type: DAILY_CHECK" ${CLAUDE_PROJECT_DIR}/.dialogue/logs/assessments/*.yaml | tail -5

# Check decision log activity
ls -la ${CLAUDE_PROJECT_DIR}/.dialogue/logs/decisions/ | tail -10
```

### Step 2: Interactive Assessment

Ask the user to evaluate each dimension using AskUserQuestion:

1. **Documentation readiness** (1-5): Are required phase artefacts complete?
2. **Knowledge transfer readiness** (1-5): Is knowledge documented and shared?
3. **Stakeholder readiness** (1-5): Are stakeholders aligned on proceeding?
4. **Technical readiness** (1-5): Are technical prerequisites met?

Then ask:
5. What is the current phase? (1-7)
6. What is the target phase? (2-7)
7. Are there any blockers? (optional free text)
8. Are there any risks to proceeding? (optional free text)

### Step 3: Reference Component Assessments

If available, reference recent component assessments:
- Problem framing assessment ID (if exists)
- Stakeholder alignment assessment ID (if exists, from FW-041)
- TTKM assessment ID (if exists, from FW-041)
- Recent daily check IDs

### Step 4: Log the Assessment

```bash
${CLAUDE_PLUGIN_ROOT}/skills/dialogue-assess-phase/scripts/log-assess-phase.sh \
  <assessor> \
  <current_phase> <target_phase> \
  <documentation_readiness> <knowledge_transfer_readiness> \
  <stakeholder_readiness> <technical_readiness> \
  [problem_framing_ref] [blockers] [risks]
```

### Parameters

| Parameter | Values | Description |
|-----------|--------|-------------|
| `assessor` | `ai:claude` or `human:<id>` | Who performed the assessment |
| `current_phase` | `1-7` | Current SDLC phase |
| `target_phase` | `2-7` | Target phase (must be > current) |
| `documentation_readiness` | `1-5` | Documentation completeness |
| `knowledge_transfer_readiness` | `1-5` | Knowledge sharing quality |
| `stakeholder_readiness` | `1-5` | Stakeholder alignment |
| `technical_readiness` | `1-5` | Technical prerequisites |
| `problem_framing_ref` | string (optional) | ASSESS-... ID of framing assessment |
| `blockers` | string (optional) | Blocking issues (comma-separated) |
| `risks` | string (optional) | Identified risks (comma-separated) |
| `context` | string (optional) | Situational context |
| `tags` | string (optional) | Comma-separated categorisation tags |

## Recommendation Logic

The script computes a recommendation based on dimension scores:

```
Average score = (doc + knowledge + stakeholder + technical) / 4

If average >= 4.0 AND no blockers AND problem_framing exists:
  → PROCEED
Else if average >= 3.0 AND blockers are manageable:
  → PROCEED_WITH_CAUTION
Else:
  → DEFER
```

**Special conditions:**
- Missing problem framing assessment: Maximum recommendation is PROCEED_WITH_CAUTION
- Any dimension score of 1: Forces DEFER
- Blockers present: Maximum recommendation is PROCEED_WITH_CAUTION

## DEFER Remediation Guidance

When the recommendation is DEFER, the assessment includes a `defer_guidance` block that provides actionable remediation advice based on two factors:

### Factor 1: Phase Tacit Percentage

The current phase's information composition determines remediation character:

| Phase | Tacit % | Remediation Character |
|-------|---------|----------------------|
| 1. Initiation | 75% | Primarily dialogue-based |
| 2. Planning | 55% | Dialogue-dominant |
| 3. Requirements | 50% | Balanced |
| 4. Design | 40% | Balanced, slightly artifact-weighted |
| 5. Implementation | 35% | Artifact-dominant |
| 6-7. Testing/Ops | 30% | Primarily artifact/process |

### Factor 2: Gap Dimension

The lowest-scoring dimension identifies what type of gap to address:

| Gap | Meaning | Natural Remediation |
|-----|---------|---------------------|
| `documentation` | Artifacts incomplete | Review/create documents |
| `knowledge` | Tacit understanding not shared | Dialogue, pairing, mentoring |
| `stakeholder` | Alignment issues | Facilitation, workshops |
| `technical` | Blockers, dependencies | Technical resolution |

### Recommended Approach

The combination produces a `recommended_approach`:

- **DIALOGUE**: High-tacit phase or knowledge/stakeholder gaps → convene sessions, elicit understanding
- **MIXED**: Medium-tacit phase or mixed gaps → balance dialogue with artifact work
- **ARTIFACT**: Low-tacit phase with documentation/technical gaps → focus on specifications, resolution

### Example DEFER Output

```yaml
defer_guidance:
  primary_gap: knowledge
  primary_gap_score: 2
  secondary_gaps: []
  phase_tacit_percentage: 75
  recommended_approach: DIALOGUE
  specific_actions:
    - "Conduct knowledge transfer sessions with domain experts"
    - "Pair with experienced team members"
    - "Facilitate stakeholder interviews to capture tacit understanding"
  restart_point:
    phase: 1
    phase_name: "Initiation/Conception"
    focus: "Address knowledge gaps before re-assessing"
```

## Human Approval Workflow

Phase transitions require human approval:

1. AI presents assessment summary with recommendation
2. Human reviews:
   - Component assessment references
   - Dimension scores and rationale
   - Identified blockers and risks
3. Human decides: approve, approve with conditions, or defer
4. Decision is logged with approval metadata

### Example Approval Flow

```
AI: Phase readiness assessment complete.

    Current Phase: 1 (Problem Definition)
    Target Phase:  2 (Requirements)

    Dimension Scores:
    - Documentation:       4/5 (requirements doc drafted)
    - Knowledge Transfer:  4/5 (decisions logged, theory captured)
    - Stakeholder:         3/5 (one stakeholder pending review)
    - Technical:           5/5 (no blockers)

    Component Assessments:
    - Problem Framing: ASSESS-20260122-140000 (5/6, confidence 4)

    Blockers: None
    Risks: Stakeholder review may surface new requirements

    Recommendation: PROCEED_WITH_CAUTION

    Do you approve proceeding to Phase 2?
    [Options: Approve / Approve with conditions / Defer]

User: Approve with conditions - complete stakeholder review within 48 hours

AI: Approved with conditions. Logging the decision...
    [Logs DEC-... with approval and conditions]

    Phase transition approved. Moving to Phase 2 (Planning).
    Condition: Complete stakeholder review within 48 hours.
```

## Output

The script returns the generated assessment ID (e.g., `ASSESS-20260122-150000`).

The assessment is stored in `.dialogue/logs/assessments/` and creates:
- Assessment YAML file with full readiness data
- Context graph node (ARTIFACT with artifact_type: ASSESSMENT)
- CREATED edge from assessor to assessment
- ASSESSES edges to referenced component assessments

## Example Direct Invocation

```bash
${CLAUDE_PLUGIN_ROOT}/skills/dialogue-assess-phase/scripts/log-assess-phase.sh \
  "human:pidster" \
  1 2 \
  4 4 3 5 \
  "ASSESS-20260122-140000" \
  "" \
  "Stakeholder review may surface new requirements"
```

## Phase-Specific Considerations

### Phase 1 → 2 (Initiation/Conception → Planning)

Critical inputs:
- Problem framing assessment (strongly encouraged)
- Stakeholder alignment on business case
- Strategic rationale documented

### Phase 2 → 3 (Planning → Analysis/Requirements)

Critical inputs:
- Project plan and resource allocations
- Risk register established
- Governance structure defined

### Phase 3 → 4 (Analysis/Requirements → Design/Architecture)

Critical inputs:
- Requirements documented and reviewed
- Stakeholders approved requirements
- Key technical constraints identified

### Phase 4 → 5 (Design/Architecture → Implementation/Construction)

Critical inputs:
- Architecture decisions documented (ADRs)
- Technical feasibility validated
- Performance/scalability requirements addressed

### Later Phases

Similar patterns—each transition validates that:
1. Phase artefacts are complete
2. Knowledge is captured and shared
3. Stakeholders are aligned
4. Technical prerequisites are met

## Schema Reference

See [Assessment Schema](../dialogue-daily-check/schema.md) for the complete PHASE_READINESS response schema and validation rules.