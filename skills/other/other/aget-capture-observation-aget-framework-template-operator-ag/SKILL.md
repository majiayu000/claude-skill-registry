---
name: aget-capture-observation
description: Capture research observations into AGET KB without committing specs. Use when discovering vocabulary candidates, RQ proposals, web findings, patterns, or observations mid-session that should be preserved before continuing.
---

## Capture Protocol (v2 - Autonomous-Explicit Continuum)

You are capturing research observations for the AGET knowledge base.

**Renamed**: `/aget-capture-observation` → `/aget-capture-observation` per S-V-O naming convention (L584) and ACM SIGSOFT "Observation" grounding.

### Input

$ARGUMENTS

### Mode Detection

Detect the input mode based on $ARGUMENTS:

| Input Pattern | Mode | Behavior |
|---------------|------|----------|
| Empty or blank | **Autonomous** | Scan session, identify and capture valuable signals (~2 min) |
| Time pattern: `5min`, `10 min`, `20min`, `30 min` | **Time-Budget** | Scan session with depth scaled to time budget |
| Text with signal keywords | **Explicit** | Capture the specific signal provided |
| Other text | **Explicit** | Capture as general observation |

### Mode 1: Autonomous (no args)

When invoked as `/aget-capture-observation` with no arguments:

1. **Scan** recent session conversation for valuable signals
2. **Identify** vocabulary candidates, patterns, RQs, findings, gaps
3. **Prioritize** by novelty and AGET governance value
4. **Capture** top 3-5 signals to session file with classification
5. **Report** what was captured

### Mode 2: Time-Budget (duration arg)

When invoked as `/aget-capture-observation <duration>` (e.g., `/aget-capture-observation 10min`):

| Time Budget | Depth | Actions |
|-------------|-------|---------|
| 2-5 min | Shallow | Scan + capture raw signals to session file |
| 10 min | Medium | Classify + link signals to existing vocabulary terms |
| 20 min | Deep | Interlink + propose RQs + draft L-doc candidates |
| 30+ min | Full | Formalize with traceability, update session summary |

### Mode 3: Explicit (signal arg)

When invoked as `/aget-capture-observation "<signal>"`:

Classify the input and route to appropriate target:

| Signal Type | Indicator Keywords | Target Location |
|-------------|-------------------|-----------------|
| Vocabulary candidate | "term:", "concept:", "definition:", "vocabulary" | Session file - Vocabulary Candidates section |
| Research question | "RQ:", "question:", "how does", "why does", "what is" | Session file - Research Questions section |
| Web research finding | "source:", "URL:", "according to", "web search" | Session file - Web Findings section |
| L-doc draft | "finding:", "lesson:", "L-doc", "learned:" | Session file - Findings section |
| Pattern observation | "pattern:", "anti-pattern:", "noticed:", "observed:" | Session file - Patterns section |
| Process gap | "gap:", "missing:", "SOP:", "template:" | Session file - Process Gaps section |
| General observation | (default) | Session file - Observations section |

### Output Format

Append to current session file (if exists in `sessions/session_YYYY-MM-DD_*.md`):

```markdown
### [Signal Type] - [ISO Timestamp]

**Source**: [User input / Session scan / Analysis]

**Content**:
[Captured signal]

**Status**: Captured (pending review at wind_down)
```

If no session file exists, create capture note in scratchpad with timestamp.

### Constraints

These are INVIOLABLE - you MUST NOT violate these constraints:

1. **NEVER** modify `specs/CLI_VOCABULARY.md` - vocabulary requires deliberate enhancement session per SOP_ONTOLOGY_ENHANCEMENT.md
2. **NEVER** modify `specs/CLI_SUBSYSTEM_SPEC.md` - specs require deliberate enhancement session
3. **NEVER** modify `planning/RESEARCH_BACKLOG.md` directly - use session capture, formalize at wind_down
4. **NEVER** create L-docs directly - capture findings, create L-doc at wind_down if warranted
5. **DO** append to current session file if one exists in `sessions/`
6. **DO** create timestamped capture note if no session file exists
7. **DO** include source attribution for web findings
8. **DO** tag with appropriate signal type from classification table
9. **DO** use ISO 8601 timestamp format

### Rationale

Per AGET theoretical grounding:
- **Stigmergy** (Grasse): Incremental artifact modification enables coordination
- **Extended Mind** (Clark/Chalmers): Externalizing signal prevents cognitive loss
- **Wind_Down_Protocol**: Captured signal feeds into formal session closure
- **Evidence-First Design** (L289): Capture evidence before committing to specs
- **Autonomous-Explicit Continuum** (L575): Support agent-driven and user-driven modes

This skill implements the "capture early, commit deliberately" pattern with adaptive depth.

### Traceability

| Link | Reference |
|------|-----------|
| Vocabulary | Capture_Protocol (CLI_VOCABULARY.md v1.30.0) |
| Requirements | R-CLI-082, R-CLI-083 (CLI_SUBSYSTEM_SPEC.md v1.10.0) |
| Skill Spec | SKILL-004 |
| L-docs | L570, L571, L574 |
| RQ | RQ-058, RQ-059, RQ-060 |
| Pattern | Autonomous-Explicit Continuum (POC-013) |
