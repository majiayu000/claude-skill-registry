---
name: lit-pm
description: Use when coordinating comprehensive literature reviews requiring multi-stage pipeline (archival setup, scope refinement, parallel review discovery, outline synthesis, section writing, fact-checking, editorial polish). Orchestrates literature-researcher, lit-synthesizer, fact-checker, and editor skills with adaptive checkpoints based on complexity and stakes.
---

# lit-pm: Literature Pipeline Manager

## Overview

lit-pm is a Tier 1 orchestrator skill that coordinates a 9-stage literature review pipeline. It manages parallel review discovery, adaptive checkpoints, and handoffs between specialist skills to produce comprehensive, decision-useful literature reviews.

### Three-Tier Architecture

**Tier 1: Orchestrator (this skill)**
- Coordinates 9-stage pipeline (Stage 0-8)
- Implements adaptive orchestration (complexity detection -> checkpoint plan)
- Manages parallel execution with convergence tracking
- Handles workflow state, handoffs, and quality gates
- Manages session-based intermediate file storage

**Tier 2: Specialized Literature Skills**
- `literature-researcher`: Review discovery, section research (15-30 papers per section)
- `lit-synthesizer`: Senior scientific author, narrative synthesis, introduction/conclusion

**Tier 3: Supporting Skills**
- `fact-checker`: Quick validation + comprehensive review
- `editor`: Final polish
- `requirements-analyst`: Scope refinement

## When to Use This Skill

- **Internal research synthesis**: Decision-focused ("Should we pursue technology X?")
- **Literature surveys**: Landscape mapping ("What are current approaches to Y?")
- **Comprehensive reviews**: Grant proposals, research plans, scientific documents
- **Cross-domain literature**: Topics spanning multiple fields
- **High-stakes deliverables**: When thoroughness and accuracy are critical

## When NOT to Use This Skill

- **Quick literature lookups**: Use researcher directly for single-topic searches
- **Single-paper analysis**: Use researcher for individual paper deep-dives
- **Dependencies missing**: Do NOT use until literature-researcher and lit-synthesizer skills exist
- **Non-scientific literature**: This skill is optimized for scientific/technical literature
- **Time-critical requests**: Pipeline takes 4-24 hours; use researcher for faster turnaround

## Pre-Flight Validation

Before Stage 0 begins, verify all required skills exist:

**Required Skills**:
- [ ] requirements-analyst (Stage 1: Scope refinement)
- [ ] literature-researcher (Stages 2, 3, 5: Review discovery, outline details, section writing)
- [ ] lit-synthesizer (Stages 4, 7: Introduction, synthesis)
- [ ] fact-checker (Stages 6a, 6b: Validation)
- [ ] editor (Stage 8: Editorial polish)
- [ ] devils-advocate (Stages 6c, 7.5: Adversarial review)

**On missing skill**: ABORT immediately with clear error:
"ERROR: Required skill '{skill}' not found. lit-pm requires all dependencies. See references/stage-specifications.md for skill details."

---

## The 9-Stage Pipeline

### Stage 0: Archival Guidelines Review
**Owner**: lit-pm (automatic)
**Checkpoint**: Never (always runs automatically)
**Duration**: 2-5 minutes
**Session Setup**: Creates `/tmp/lit-pm-session-{YYYYMMDD-HHMMSS}-{PID}/`

Initialize workflow session and extract archival guidelines from project CLAUDE.md.

**Process**:
1. **Create session directory**: `/tmp/lit-pm-session-$(date +%Y%m%d-%H%M%S)-$$/`
2. **Read project CLAUDE.md** (if exists in working directory or parent)
3. **Extract archival guidelines**:
   - Repository organization (directory structure)
   - Naming conventions (review-, analysis-, reference-, etc.)
   - Git rules (commit after edits, no version-numbered files)
   - Document structure requirements
   - PDF acquisition paths
4. **Write archival summary** to session directory: `archival-guidelines-summary.md`
5. **Store session path** in workflow state for downstream agents

**Output**:
```yaml
session_setup:
  session_dir: "/tmp/lit-pm-session-{timestamp}-{pid}/"
  archival_summary_path: "{session_dir}/archival-guidelines-summary.md"
  guidelines_found: boolean
  guidelines_source: string  # Path to CLAUDE.md or "defaults"
```

**Archival Summary Format**:
```markdown
# Archival Guidelines Summary
Generated: {timestamp}
Source: {CLAUDE.md path or "project defaults"}

## Directory Structure
- Literature reviews: `docs/literature/<topic>/`
- PDF storage: `docs/literature/<topic>/pdfs/`
- Analysis documents: `docs/reports/` or `docs/literature/<topic>/`

## File Naming Conventions
| Type | Prefix | Example |
|------|--------|---------|
| Literature review | `review-` | `review-topic-name.md` |
| Analysis | `analysis-` | `analysis-topic-name.md` |
| Reference | `reference-` | `reference-topic-name.md` |
| Paper notes | `<author>-<year>-` | `smith-2024-findings.md` |

## Document Structure
1. Title
2. Metadata (version, date, sources)
3. Executive Summary
4. Table of Contents (3+ sections)
5. Body (numbered hierarchically)
6. Key Parameters Table
7. Gaps/Limitations
8. References
9. Revision History

## Git Rules
- Commit after every edit to docs/ or modules/
- No version-numbered files (use git history)
- Edit in place

## Citation Format
- Nature-style inline citations (superscript numbers)
- Full bibliography at end with DOIs
```

**Quality Gate**: Session directory created, archival summary written.

**Failure Handling**:
- CLAUDE.md not found: Use sensible defaults, log warning
- Session directory creation fails: ABORT (cannot proceed without session isolation)

**Session Cleanup**:
- On successful completion (Stage 8 complete): Delete session directory
- On failure/abort: Retain session directory for debugging (log path to user)

### Stage 1: Scope Refinement
**Owner**: requirements-analyst
**Checkpoint**: ALWAYS (required)
**Duration**: 15-30 minutes
**Receives**: Session directory path from Stage 0

Clarify research question, define success criteria, set boundaries. Complexity detection determines checkpoint plan. User approves scope + checkpoint plan.

**Quality Gate**: Specific research question, measurable criteria, clear boundaries.

### Stage 2: Parallel Review Discovery
**Owner**: lit-pm orchestrates 2-3 literature-researcher agents
**Checkpoint**: Only if HIGH-STAKES complexity
**Duration**: 45-90 minutes (parallel)

Launch parallel agents with diverse search strategies. Analyze convergence (reviews found by multiple agents = high signal). Collect 6-9 reviews total.

**Quality Gate**: 6-9 reviews, >=2 show convergence, coverage of major themes.

### Stage 3: Layered Outline Synthesis
**Owner**: lit-pm (structure) + literature-researcher (section details)
**Checkpoint**: MEDIUM/COMPLEX/HIGH-STAKES
**Duration**: 30-60 minutes

Create 3-5 section outline with specific theses. Each section gets detailed subsection proposals and assigned reviews.

**Quality Gate**: 3-5 balanced sections, specific theses, user approval (if checkpoint).

### Stage 4: Introduction Writing
**Owner**: lit-synthesizer + editor (quick polish)
**Checkpoint**: Never (automatic)
**Duration**: 30-45 minutes

lit-synthesizer writes introduction framing research question and previewing structure. Editor applies quick polish.

**Quality Gate**: Clear framing, structure preview matches outline.

### Stage 5: Parallel Section Research & Writing
**Owner**: literature-researcher agents (parallel)
**Checkpoint**: Never (gated by Stage 6a)
**Duration**: 3-5 hours per section (parallel)

Section writers conduct targeted research: 15-30 papers per section with recency survey (last 6-12 months). Writers have moderate autonomy to add subsections.

**Quality Gate**: 15-30 papers cited, recency survey present, thesis addressed.

### Stage 6a: Per-Section Quick Validation (BLOCKING)
**Owner**: fact-checker
**Checkpoint**: Blocking per section
**Duration**: 5-10 minutes per section

Quick checks: paper count, recency survey presence, no placeholders, thesis addressed. Section cannot proceed until PASS.

**Quality Gate**: All automated checks pass, max 3 revision cycles.

### Stage 6b: Comprehensive Fact-Check (NON-BLOCKING)
**Owner**: fact-checker
**Checkpoint**: Never (automatic)
**Duration**: 45-90 minutes

Deep checks: cross-section consistency, citation accuracy (spot-check), quantitative verification. Produces revision list (P0/P1/P2).

**Quality Gate**: Revision list generated for Stage 8.

### Stage 6c: Devil's Advocate Section Review (ALWAYS-ON)
**Owner**: devils-advocate
**Checkpoint**: ACTIVE (always runs, not user approval)
**Duration**: 30 min/section
**Trigger**: All sections pass Stage 6a/6b

Adversarial review of each section: challenges argument quality, tests assumptions, identifies logical gaps. Max 2 exchanges per section. Pass with uncertainty note on timeout.

**Quality Gate**: All strategic challenges addressed OR 2 exchanges complete with uncertainty documented.

**Scope Separation (vs Fact-Checker)**:
- **devils-advocate CAN challenge**: Argument strength, assumption validity, logical coherence, thesis appropriateness, methodology context for claims
- **devils-advocate CANNOT challenge**: Citation accuracy, whether papers exist, whether values match sources (fact-checker domain)

### Stage 7: Active Synthesis & Augmentation
**Owner**: lit-synthesizer (senior author role)
**Checkpoint**: HIGH-STAKES only
**Duration**: 2-4 hours

Senior author reads all sections, identifies cross-cutting themes, restructures for narrative flow, writes conclusion. Authority to add subsections and rewrite transitions. Flags additions >20%.

**Quality Gate**: Logical flow, themes identified, gaps filled, conclusion synthesizes findings.

### Stage 7.5: Devil's Advocate Synthesis Review (CONDITIONAL)
**Owner**: devils-advocate
**Checkpoint**: CONDITIONAL (>=20% additions OR HIGH-STAKES)
**Duration**: 60 min
**Trigger**: (addition_percentage >= 20%) OR (complexity == HIGH-STAKES)

Strategic-level adversarial review of synthesized document: thesis coherence across sections, cross-cutting theme validity, argument flow. Max 2 exchanges.

**Quality Gate**: Document passes strategic review OR 2 exchanges complete with uncertainty documented.

### Stage 8: Editorial Polish
**Owner**: editor
**Checkpoint**: Never (automatic)
**Duration**: 30-60 minutes

Incorporate P0/P1 revisions from Stage 6b, polish for clarity, ensure voice consistency, final formatting.

**Quality Gate**: Revisions incorporated, consistent voice, formatted, final read complete.

---

## Adaptive Orchestration

See `references/adaptive-orchestration.md` for full complexity detection logic.

### Complexity Detection Dimensions

1. **Scope**: Paper count (<10 Simple, 10-30 Medium, 30+ Complex), topic breadth, literature maturity
2. **Stakes**: Keywords ("quick survey" = Low, "grant proposal" = High)
3. **User Hints**: Explicit flags (--review-outline, --full-auto), time constraints

### Checkpoint Plan Table

| Complexity | Stage 1 | Stage 2 | Stage 3 | Stage 6c | Stage 7 | Stage 7.5 | Rationale |
|------------|---------|---------|---------|----------|---------|-----------|-----------|
| Simple | CHECKPOINT | Auto | Auto | ACTIVE | Auto | Conditional* | Scope approval sufficient |
| Medium | CHECKPOINT | Auto | CHECKPOINT | ACTIVE | Auto | Conditional* | Direction check before heavy lifting |
| Complex | CHECKPOINT | Auto | CHECKPOINT | ACTIVE | CHECKPOINT | Conditional* | Multiple approval points |
| High-Stakes | CHECKPOINT | CHECKPOINT | CHECKPOINT | ACTIVE | CHECKPOINT | ACTIVE | Maximum oversight |

**Checkpoint Types**:
- **CHECKPOINT**: User approval required before proceeding
- **Auto**: Runs automatically, no user interaction
- **ACTIVE**: Always runs as quality gate (not user approval)
- **Conditional***: Triggers if synthesis adds >=20% content

### User Override Options

After proposing checkpoint plan, user can:
- **Accept**: Proceed with proposed plan
- **Reduce**: Skip specific checkpoints
- **Add**: Add checkpoints at additional stages
- **Full-auto**: `--full-auto` skips all optional checkpoints

---

## Timeout Configuration

| Stage | Timeout | Exceeded Action |
|-------|---------|-----------------|
| 0 (Archival) | 5 min | ABORT - cannot proceed without session |
| 1 (Scope) | 45 min | Escalate to user |
| 2 (Reviews) | 120 min total | Proceed with available reviews |
| 3 (Outline) | 90 min | Escalate to user |
| 4 (Intro) | 60 min | Escalate to user |
| 5 (Sections) | 6 hours/section | Proceed without section, flag gap |
| 6a (Quick FC) | 15 min/section | Pass with warning |
| 6b (Deep FC) | 120 min | Skip deep check |
| 7 (Synthesis) | 5 hours | Escalate to user |
| 6c (DA Section) | 30 min/section | Pass with uncertainty note |
| 7.5 (DA Synthesis) | 60 min | Proceed to Stage 8 with warning |
| 8 (Editorial) | 90 min | Deliver as-is, cleanup session |

**Per-Agent Timeouts**:
- literature-researcher: 30 min per search strategy
- lit-synthesizer: 60 min per task
- fact-checker: 10 min (quick), 60 min (comprehensive)
- editor: 30 min

**Global Workflow Timeout**: 48 hours

---

## Resource Limits

```yaml
resource_limits:
  max_concurrent_agents: 4       # Hard ceiling
  max_parallel_researchers: 3    # Stage 2: Leave slot for orchestrator
  max_parallel_sections: 3       # Stage 5: Leave slot for fact-checker
  queue_behavior: FIFO           # When limits reached
  queue_timeout: 30 min          # Escalate if not processed
```

---

## Parallel Execution

### Stage 2: Review Discovery (Fan-Out/Fan-In)

```yaml
parallel_execution:
  stage: 2
  pattern: fan_out_fan_in
  max_agents: 3

  strategy_assignment:
    agent_1: "Broad keywords"
    agent_2: "Specific technical terms"
    agent_3: "Application focus"

  convergence_tracking:
    high_priority: "Found by 3/3 agents (must-read)"
    medium_priority: "Found by 2/3 agents"
    unique: "Found by 1 agent (coverage breadth)"
```

### Stage 5: Section Writing (Parallel with Queue)

```yaml
parallel_execution:
  stage: 5
  pattern: parallel_with_queue
  max_agents: 3  # Reserve slot for fact-checker

  completion_handling:
    on_complete: "Send to Stage 6a immediately"
    on_timeout: "Proceed without section, flag gap"
```

---

## Handoffs

See `references/handoff-schema.md` for YAML schema.

### Base Handoff Format

```yaml
handoff:
  version: "1.1"
  stage: integer           # 0-8
  status: enum             # pending | in_progress | complete | failed
  producer: string         # skill that produced handoff
  consumer: string         # skill that receives handoff
  workflow_id: string      # unique identifier
  timestamp: ISO8601       # when created
  session:                 # Added in v1.1
    session_dir: string    # Path to /tmp/lit-pm-session-{...}/
    archival_guidelines_path: string  # Path to archival-guidelines-summary.md
```

Each stage has additional stage-specific fields documented in the schema.

### Session Context Propagation

All downstream agents receive the session context via handoff:

**Agents that use archival guidelines**:
- `literature-researcher`: Uses naming conventions for paper notes, PDF storage paths
- `lit-synthesizer`: Uses document structure requirements, citation format
- `editor`: Uses writing style, formatting rules
- `fact-checker`: Uses citation format for validation

**Handoff includes**:
```yaml
session_context:
  archival_guidelines_path: "{session_dir}/archival-guidelines-summary.md"
  output_directory: string   # Where final document should be written
  pdf_storage_path: string   # Where to store downloaded PDFs
  naming_convention: object  # File prefix rules
```

---

## Quality Gates Overview

See `references/quality-gates.md` for detailed per-stage gates.

### Gate Types

**Automated Gates** (programmatic validation):
- Paper count threshold (>=15 per section)
- Recency survey presence
- Placeholder detection (no "TODO", "[CITE]")
- Word count range

**Human Judgment Gates** (agent assessment):
- Thesis specificity
- Narrative flow
- Cross-cutting theme identification

### Quality Floor (Cannot Override)

Even with `--full-auto`, these checks cannot be skipped:
- Stage 2: minimum 4 reviews, minimum 1 convergence
- Stage 3: minimum 2 sections, max 50% imbalance
- Stage 6c: DA must execute, thesis must be identified for each section

---

## Error Handling Overview

See `references/error-handling.md` for full compensation matrix.

### Key Mechanisms

1. **Saga-Style Compensation**: Per-stage forward and compensation actions
2. **Circuit Breakers**: Open after repeated failures, proceed with partial results
3. **Atomic State Writes**: .tmp -> validate -> rename -> .bak protocol
4. **Interrupt Handling**: Graceful Ctrl+C with partial state preservation

### Workflow State for Resumption

```yaml
workflow_state:
  workflow_id: "lit-review-{topic}-{date}"
  stage_current: integer          # 0-8
  stage_completed: [list]
  checkpoints_remaining: [list]
  session:                        # Added for session management
    session_dir: string           # /tmp/lit-pm-session-{...}/
    archival_guidelines_path: string
    cleanup_on_complete: boolean  # Default true
  artifacts:
    scope: "/path/to/scope.yaml"
    reviews: "/path/to/reviews.yaml"
    outline: "/path/to/outline.yaml"
    sections_complete: [list]
    sections_in_progress: [list]
```

Resume with: `lit-pm --resume workflow-id`

**Session Handling on Resume**:
- If session directory exists: Reuse existing session
- If session directory missing: Re-run Stage 0 to recreate (non-destructive)

---

## References

- `references/stage-specifications.md`: Detailed 8-stage process specifications
- `references/handoff-schema.md`: YAML schema for stage-to-stage communication
- `references/error-handling.md`: Compensation logic, circuit breakers, recovery
- `references/adaptive-orchestration.md`: Complexity detection and checkpoint logic
- `references/quality-gates.md`: Per-stage quality validation criteria

## Examples

- `examples/hepatocyte-review-example.md`: Complete walkthrough of hepatocyte oxygenation review

---

## Invocation

```bash
# Standard invocation
lit-pm "Comprehensive review of [topic] for [purpose]"

# With explicit checkpoint control
lit-pm --review-outline "Survey of current approaches to [topic]"
lit-pm --full-auto "Quick survey of [topic]"

# Resume interrupted workflow
lit-pm --resume workflow-id
```

## Dependencies

This skill requires:
- technical-pm Phase 3 parallel execution capabilities
- literature-researcher skill (enhanced from researcher)
- lit-synthesizer skill (new, senior scientific author)
- fact-checker skill (existing)
- editor skill (existing)
- requirements-analyst skill (existing)
