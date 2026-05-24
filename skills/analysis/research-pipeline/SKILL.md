---
name: research-pipeline
version: 1.0
last_updated: 2026-02-03
description: Use when you need a complete research workflow from initial literature search to polished, fact-checked document. Chains researcher -> synthesizer -> devils-advocate -> fact-checker -> editor automatically.
prerequisites:
  - Research topic or question clearly defined
  - Access to literature databases (PubMed, bioRxiv, OpenAlex)
  - Target output format (review, analysis, summary)
  - Estimated scope (comprehensive vs focused)
success_criteria:
  - Literature reviewed and synthesized into cohesive document
  - Arguments challenged and strengthened via adversarial review
  - All citations verified and properly formatted
  - Prose polished and ready for publication/archival
  - Pipeline completion with no manual handoffs required
estimated_duration: 4-8 hours (comprehensive review), 2-4 hours (focused summary)
---

# Research Pipeline Skill

## Purpose

The research-pipeline skill automates the complete research workflow by chaining five specialized skills in sequence. Instead of manually invoking researcher, synthesizer, devils-advocate, fact-checker, and editor with handoffs between each, this skill handles the entire pipeline with structured context passing.

This represents the "pipeline pattern" for skill orchestration: a predefined sequence of skills that together accomplish a complex goal requiring multiple specialized capabilities.

## When to Use This Skill

Invoke the research-pipeline when:

1. **Complete research workflow needed**: You need to go from research question to polished document
2. **Quality matters**: The output must withstand scrutiny (adversarial review, fact-checking)
3. **Hands-off execution desired**: You want to set the goal and receive the final product
4. **Standard research pipeline fits**: The researcher -> synthesizer -> review -> edit flow matches your needs

### Clear Indicators for Use

- User says "write a literature review on X"
- User says "research X and give me a polished summary"
- Task requires finding sources, synthesizing findings, and producing publication-quality output
- Multi-hour research effort with quality requirements

### When NOT to Use

Do not use this skill when:

- You only need part of the pipeline (use individual skills instead)
- Output is exploratory/draft-only (skip adversarial review and editing)
- Custom skill order is needed (use technical-pm orchestration instead)
- Parallel research streams are required (use technical-pm with Task tool)
- Rapid iteration with user feedback between stages is needed

## Personality

You are **orchestration-focused and quality-driven**. You ensure each pipeline stage receives proper context from the previous stage, validate outputs before proceeding, and maintain the user's original goal throughout the workflow. You are patient with long-running tasks but vigilant about quality gates.

You understand that the pipeline is a convenience, not a constraint. If a stage fails validation or requires user input, you pause and escalate rather than producing low-quality output.

## Pipeline Architecture

### Stage Sequence

```
researcher
    |
    | [handoff: research findings, citations, gaps]
    v
synthesizer
    |
    | [handoff: synthesized document, themes, tensions]
    v
devils-advocate
    |
    | [handoff: reviewed document, challenges addressed]
    v
fact-checker
    |
    | [handoff: verified citations, issues flagged]
    v
editor
    |
    | [final: polished document]
    v
OUTPUT
```

### Stage Responsibilities

| Stage | Skill | Key Output | Quality Gate |
|-------|-------|------------|--------------|
| 1 | researcher | Literature review draft with citations | Has citations, addresses topic |
| 2 | synthesizer | Integrated analysis with themes | Cross-cutting insights present |
| 3 | devils-advocate | Strengthened arguments | Challenges addressed or documented |
| 4 | fact-checker | Verified citations | All claims have valid citations |
| 5 | editor | Polished prose | CLAUDE.md style compliant |

## Workflow

### Step 1: Initialize Pipeline

**Parse user goal**:
- Extract research topic or question
- Determine scope (comprehensive vs focused)
- Identify any constraints (time, page count, specific focus areas)
- Generate workflow_id for tracking

**Create initial context**:
```yaml
pipeline:
  workflow_id: "research-{uuid}"
  goal: "{user's original goal}"
  topic: "{extracted topic}"
  scope: comprehensive | focused
  constraints:
    max_pages: {N}
    focus_areas: [list]
    time_limit: {hours}
  current_stage: 1
  started_at: "{timestamp}"
```

### Step 2: Execute Stage 1 - Researcher

**Invoke**: `Skill(researcher, topic="{topic}", constraints={...})`

**Researcher executes**:
- Literature search via PubMed, bioRxiv, OpenAlex
- Paper reading and note-taking
- Draft literature review with Nature-style citations

**Validate output**:
- [ ] Document exists at expected location
- [ ] Contains inline citations (superscripts)
- [ ] Addresses the stated topic
- [ ] Minimum length achieved (varies by scope)

**If validation fails**: Pause pipeline, report issue to user with options:
- Retry researcher with narrowed scope
- Accept partial output and continue
- Abort pipeline

**Create handoff document** (see Handoff Format section)

### Step 3: Execute Stage 2 - Synthesizer

**Invoke**: `Skill(synthesizer, handoff="{handoff-file}")`

**Synthesizer executes**:
- Read researcher's output via handoff
- Identify cross-cutting themes
- Highlight tensions and contradictions
- Draw project-specific implications
- Create synthesis document

**Validate output**:
- [ ] Document exists
- [ ] Adds value beyond summary (themes, tensions, implications)
- [ ] Maintains citations from source
- [ ] Addresses original goal

**Create handoff document**

### Step 4: Execute Stage 3 - Devil's Advocate

**Invoke**: `Skill(devils-advocate, handoff="{handoff-file}")`

**Devil's Advocate executes**:
- Identify thesis of synthesized document
- Evaluate strategic coherence
- Challenge thesis-critical claims
- Propose counter-arguments
- Document exchange with synthesizer (up to 2 rounds)

**Validate output**:
- [ ] Review report generated
- [ ] Challenges addressed or uncertainty documented
- [ ] Synthesizer has responded to critical challenges

**Create handoff document** including:
- Which challenges were addressed
- Which uncertainties remain
- Devil's advocate approval status

### Step 5: Execute Stage 4 - Fact-Checker

**Invoke**: `Skill(fact-checker, handoff="{handoff-file}")`

**Fact-Checker executes**:
- Inventory all quantitative claims
- Verify each citation exists and supports claim
- Check citation format (superscripts in text)
- Flag missing or incorrect citations
- Generate verification report

**Validate output**:
- [ ] Verification report generated
- [ ] All critical citations verified
- [ ] Issues flagged for correction

**If issues found**:
- Minor issues: Correct inline and proceed
- Major issues: Return to synthesizer for corrections, then re-verify

**Create handoff document**

### Step 6: Execute Stage 5 - Editor

**Invoke**: `Skill(editor, handoff="{handoff-file}")`

**Editor executes**:
- Apply CLAUDE.md style guidelines
- Convert bullets to prose where appropriate
- Add bridging transitions
- Verify glossary placement
- Final polish for publication

**Validate output**:
- [ ] CLAUDE.md checklist passed
- [ ] Document flows smoothly
- [ ] Ready for archival/publication

### Step 7: Complete Pipeline

**Generate completion report**:
```markdown
# Research Pipeline Complete

**Workflow ID**: {workflow_id}
**Original Goal**: {goal}
**Duration**: {total time}
**Stages Completed**: 5/5

## Final Output
**Location**: {path to final document}

## Pipeline Summary
| Stage | Duration | Status | Notes |
|-------|----------|--------|-------|
| Researcher | 2h 15m | Complete | 8 papers reviewed |
| Synthesizer | 45m | Complete | 3 themes identified |
| Devil's Advocate | 30m | Complete | 2 challenges, 1 uncertainty |
| Fact-Checker | 20m | Complete | 12 citations verified |
| Editor | 25m | Complete | CLAUDE.md compliant |

## Quality Indicators
- Citations verified: 12/12
- Challenges addressed: 2/2
- Uncertainties documented: 1
- Style compliance: PASS

## Output Files
- Final document: {path}
- Researcher notes: {path}
- Synthesis draft: {path}
- Review report: {path}
- Fact-check report: {path}
```

## Handoff Format

Each stage-to-stage transition uses the standardized handoff format from technical-pm:

```yaml
handoff:
  version: "1.0"
  source_skill: "{previous skill}"
  target_skill: "{next skill}"
  timestamp: "{ISO8601}"
  workflow_id: "{pipeline workflow_id}"

deliverable:
  type: document
  location: "{path to output file}"
  format: markdown
  summary: "{50+ char description of what was produced}"
  checksum: "{sha256}"

context:
  original_goal: "{user's original goal}"
  completed_skills: [list of completed stages]
  focus_areas: [key topics/themes]
  known_gaps: [limitations identified]
  open_questions: [unresolved items]

quality:
  completion_status: complete | partial
  confidence: high | medium | low
  warnings: [concerns for downstream]
```

**Validation before each handoff**:
1. Schema validation: All required fields present
2. Content validation: Summary >= 50 chars, file exists
3. Checksum validation: Recompute and compare

**On validation failure**: STOP pipeline, report to user

## Configuration Options

### Scope Settings

**Comprehensive** (default):
- Researcher: Full literature review (8+ papers)
- Synthesizer: Multi-theme analysis
- Devil's Advocate: 2 exchange rounds
- Fact-Checker: All citations verified
- Editor: Full CLAUDE.md polish

**Focused**:
- Researcher: Targeted review (3-5 papers)
- Synthesizer: Single-theme summary
- Devil's Advocate: 1 exchange round
- Fact-Checker: Critical citations only
- Editor: Essential polish only

### Skip Options

For experienced users who want to skip stages:

```
research-pipeline topic="X" --skip=devils-advocate
research-pipeline topic="X" --skip=fact-checker,editor
```

**Warning**: Skipping stages reduces quality guarantees. Pipeline will note skipped stages in completion report.

### Output Location

Default: `docs/literature/{topic}/`

Override: `research-pipeline topic="X" --output="{custom path}"`

## Error Handling

### Stage Failure

If any stage fails:

1. **Preserve completed work**: All previous stage outputs kept
2. **Save partial output**: Current stage's work-in-progress saved
3. **Pause pipeline**: Do NOT proceed to next stage
4. **Report to user**:

```
Pipeline paused: Stage 3 (devils-advocate) failed

Error: Could not identify thesis in synthesizer output

Completed outputs preserved:
- docs/literature/topic/researcher-draft.md
- docs/literature/topic/synthesis.md (partial)

Options:
(A) Retry devils-advocate with clarified thesis
(B) Add thesis statement to synthesis, then retry
(C) Skip devils-advocate, proceed to fact-checker
(D) Abort pipeline (keep completed outputs)
```

### Timeout Handling

For long-running stages (especially researcher):

- **Progress updates**: Every 30 minutes during researcher stage
- **Timeout threshold**: 4 hours for researcher, 1 hour for other stages
- **On timeout**: Pause pipeline, show progress, offer options

### Interruption Recovery

Pipeline state is saved after each stage completion:

**Location**: `/tmp/pipeline-state-{workflow_id}.yaml`

**On resume**:
```
Found interrupted pipeline: research-abc123
Topic: "hepatocyte oxygenation"
Progress: 3/5 stages complete

Completed:
- [x] Researcher
- [x] Synthesizer
- [x] Devil's Advocate
- [ ] Fact-Checker
- [ ] Editor

Options:
(A) Resume from Fact-Checker
(B) Restart pipeline from beginning
(C) Abort (keep completed outputs)
```

## Outputs

### Primary Output
- Final polished document: `docs/literature/{topic}/review-{topic}.md`

### Intermediate Outputs (preserved for reference)
- Researcher draft: `docs/literature/{topic}/researcher-draft.md`
- Paper notes: `docs/literature/{topic}/notes/`
- Synthesis document: `docs/literature/{topic}/synthesis-{topic}.md`
- Devil's advocate review: `docs/literature/{topic}/review-report.md`
- Fact-check report: `docs/literature/{topic}/fact-check-report.md`

### Pipeline Artifacts
- Handoff documents: `/tmp/handoff-{workflow_id}-*.yaml`
- State file: `/tmp/pipeline-state-{workflow_id}.yaml`
- Completion report: Displayed to user, optionally saved

## Integration with Other Skills

### When to Escalate to technical-pm

Use technical-pm instead of research-pipeline when:
- Multiple independent research streams needed (parallel execution)
- Custom skill ordering required
- Non-research skills needed in the workflow
- Complex dependency management required

### Handoff to archive-workflow

After pipeline completion, user may want to invoke archive-workflow separately for project organization:
```
Skill(archive-workflow, project="{project root}")
```

Pipeline does NOT automatically invoke archive-workflow to give user control over organization decisions.

## Example Invocations

### Basic Research Review

**User**: "Research hepatocyte oxygenation and write a comprehensive literature review"

**Pipeline executes**:
1. Researcher: Reviews 8-10 papers on hepatocyte oxygen consumption
2. Synthesizer: Identifies themes (measurement methods, culture conditions, species variations)
3. Devil's Advocate: Challenges assumption that in vitro values apply to bioreactor design
4. Fact-Checker: Verifies all K_oA values trace to primary sources
5. Editor: Polishes into CLAUDE.md-compliant document

**Output**: `docs/literature/hepatocyte-oxygenation/review-hepatocyte-oxygenation.md`

### Focused Summary

**User**: "Give me a quick summary of hollow fiber bioreactor designs for liver support"

**Pipeline executes** (focused mode):
1. Researcher: Reviews 3-4 key papers
2. Synthesizer: Single-theme summary
3. Devil's Advocate: 1 exchange round
4. Fact-Checker: Critical citations only
5. Editor: Essential polish

**Output**: `docs/literature/hollow-fiber-bioreactor/review-hollow-fiber-bioreactor.md`

### With Constraints

**User**: "Research Matrigel alternatives for hepatocyte culture, focus on chemical approaches, max 5 pages"

**Pipeline parses**:
- Topic: Matrigel alternatives for hepatocyte culture
- Focus: Chemical approaches (not biological)
- Constraint: 5 pages max

**Adjusts behavior**:
- Researcher: Filters for chemical/synthetic matrix papers
- Synthesizer: Respects page limit in synthesis
- All stages: Honor focus constraint

## Common Pitfalls

1. **Scope creep in researcher stage**
   - **Symptom**: Researcher spends 6+ hours on "quick summary" request
   - **Fix**: Set explicit scope at pipeline init (comprehensive vs focused)

2. **Thesis drift between stages**
   - **Symptom**: Final document doesn't answer original question
   - **Fix**: Handoff includes original_goal; each stage checks alignment

3. **Citation format inconsistency**
   - **Symptom**: Mixed citation formats (superscripts and brackets)
   - **Fix**: Fact-checker enforces format; editor normalizes

4. **Skipping stages reduces quality**
   - **Symptom**: Unchallenged arguments, unverified citations in final output
   - **Fix**: Warn user when stages are skipped; note in completion report

## Handoffs

| Condition | Hand off to |
|-----------|-------------|
| Pipeline complete | **User** (with completion report) |
| Pipeline complete, organization needed | **archive-workflow** (manual invocation) |
| Stage failure, needs diagnosis | **User** (with error context) |
| Custom workflow needed | **technical-pm** (for flexible orchestration) |
| Parallel research streams | **technical-pm** with Task tool |

---

## Supporting Resources

See `examples/` directory for:
- `pipeline-invocation-example.md` - Sample pipeline run with all stages
- `completion-report-example.md` - Example completion report format
