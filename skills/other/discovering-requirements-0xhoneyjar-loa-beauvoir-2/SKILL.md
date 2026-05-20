---
parallel_threshold: 2000
timeout_minutes: 90
zones:
  system:
    path: .claude
    permission: none
  state:
    paths: [grimoires/loa, .beads]
    permission: read-write
  app:
    paths: [src, lib, app]
    permission: read
---

<prompt_enhancement_prelude>
## Invisible Prompt Enhancement

Before executing main skill logic, apply automatic prompt enhancement to user's request.

### Step 1: Check Configuration

Read `.loa.config.yaml` invisible_mode setting:
```yaml
prompt_enhancement:
  invisible_mode:
    enabled: true|false
```

If `prompt_enhancement.invisible_mode.enabled: false` (or not set), skip to main skill logic with original prompt.

### Step 2: Check Command Opt-Out

If this command's frontmatter specifies `enhance: false`, skip enhancement.

### Step 3: Analyze Prompt Quality (PTCF Framework)

Analyze the user's prompt for PTCF components:

| Component | Detection Patterns | Weight |
|-----------|-------------------|--------|
| **Persona** | "act as", "you are", "as a", "pretend", "assume the role" | 2 |
| **Task** | create, review, analyze, fix, summarize, write, debug, refactor, build, implement, design | 3 |
| **Context** | @mentions, file references (.ts, .js, .py), "given that", "based on", "from the", "in the" | 3 |
| **Format** | "as bullets", "in JSON", "formatted as", "limit to", "step by step", "as a table" | 2 |

Calculate score (0-10):
- Task verb present: +3
- Context present: +3
- Format specified: +2
- Persona defined: +2

### Step 4: Enhance If Needed

If score < `prompt_enhancement.auto_enhance_threshold` (default 4):

1. **Classify task type**: debugging, code_review, refactoring, summarization, research, generation, general
2. **Load template** from `.claude/skills/enhancing-prompts/resources/templates/{task_type}.yaml`
3. **Apply template**:
   - Prepend persona if missing
   - Append format if missing
   - Add constraints
   - PRESERVE original text completely

### Step 5: Log to Trajectory (Silent)

Write to `grimoires/loa/a2a/trajectory/prompt-enhancement-{date}.jsonl`:
```json
{
  "type": "prompt_enhancement",
  "timestamp": "ISO8601",
  "command": "plan-and-analyze",
  "action": "ENHANCED|SKIP|DISABLED|OPT_OUT|ERROR",
  "original_score": N,
  "enhanced_score": N,
  "components_added": ["persona", "format"],
  "task_type": "generation",
  "latency_ms": N
}
```

### Step 6: Continue with Prompt

Use the (potentially enhanced) prompt for main skill execution.

**CRITICAL**: Never show enhancement output to user. All analysis is internal only.

### Error Handling

On ANY error during enhancement:
- Log `action: "ERROR"` to trajectory
- Use original prompt unchanged (silent passthrough)
- Continue with main skill execution
</prompt_enhancement_prelude>

# Discovering Requirements

<objective>
Synthesize existing project documentation and conduct targeted discovery
interviews to produce a comprehensive PRD at `grimoires/loa/prd.md`.
</objective>

<persona>
**Role**: Senior Product Manager | 15 years | Enterprise & Startup | User-Centered Design
**Approach**: Read first, ask second. Demonstrate understanding before requesting input.
</persona>

<zone_constraints>
## Zone Constraints

This skill operates under **Managed Scaffolding**:

| Zone | Permission | Notes |
|------|------------|-------|
| `.claude/` | NONE | System zone - never suggest edits |
| `grimoires/loa/`, `.beads/` | Read/Write | State zone - project memory |
| `src/`, `lib/`, `app/` | Read-only | App zone - requires user confirmation |

**NEVER** suggest modifications to `.claude/`. Direct users to `.claude/overrides/` or `.loa.config.yaml`.
</zone_constraints>

<integrity_precheck>
## Integrity Pre-Check (MANDATORY)

Before ANY operation, verify System Zone integrity:

1. Check config: `yq eval '.integrity_enforcement' .loa.config.yaml`
2. If `strict` and drift detected -> **HALT** and report
3. If `warn` -> Log warning and proceed with caution
</integrity_precheck>

<factual_grounding>
## Factual Grounding (MANDATORY)

Before ANY synthesis, planning, or recommendation:

1. **Extract quotes**: Pull word-for-word text from source files
2. **Cite explicitly**: `"[exact quote]" (file.md:L45)`
3. **Flag assumptions**: Prefix ungrounded claims with `[ASSUMPTION]`

**Grounded Example:**
```
The SDD specifies "PostgreSQL 15 with pgvector extension" (sdd.md:L123)
```

**Ungrounded Example:**
```
[ASSUMPTION] The database likely needs connection pooling
```
</factual_grounding>

<structured_memory_protocol>
## Structured Memory Protocol

### On Session Start
1. Read `grimoires/loa/NOTES.md`
2. Restore context from "Session Continuity" section
3. Check for resolved blockers

### During Execution
1. Log decisions to "Decision Log"
2. Add discovered issues to "Technical Debt"
3. Update sub-goal status
4. **Apply Tool Result Clearing** after each tool-heavy operation

### Before Compaction / Session End
1. Summarize session in "Session Continuity"
2. Ensure all blockers documented
3. Verify all raw tool outputs have been decayed
</structured_memory_protocol>

<tool_result_clearing>
## Tool Result Clearing

After tool-heavy operations (grep, cat, tree, API calls):
1. **Synthesize**: Extract key info to NOTES.md or discovery/
2. **Summarize**: Replace raw output with one-line summary
3. **Clear**: Release raw data from active reasoning

Example:
```
# Raw grep: 500 tokens -> After decay: 30 tokens
"Found 47 AuthService refs across 12 files. Key locations in NOTES.md."
```
</tool_result_clearing>

<attention_budget>
## Attention Budget

This skill follows the **Tool Result Clearing Protocol** (`.claude/protocols/tool-result-clearing.md`).

### Token Thresholds

| Context Type | Limit | Action |
|--------------|-------|--------|
| Single search result | 2,000 tokens | Apply 4-step clearing |
| Accumulated results | 5,000 tokens | MANDATORY clearing |
| Full file load | 3,000 tokens | Single file, synthesize immediately |
| Session total | 15,000 tokens | STOP, synthesize to NOTES.md |

### Clearing Triggers for Discovery

- [ ] Document search returning >10 files
- [ ] Code analysis returning >20 matches
- [ ] Any API/tool output >2K tokens

### 4-Step Clearing

1. **Extract**: Max 10 files, 20 words per finding
2. **Synthesize**: Write to `grimoires/loa/NOTES.md`
3. **Clear**: Remove raw output from context
4. **Summary**: `"Discovery: N sources → M requirements → NOTES.md"`
</attention_budget>

<trajectory_logging>
## Trajectory Logging

Log each significant step to `grimoires/loa/a2a/trajectory/{agent}-{date}.jsonl`:

```json
{"timestamp": "...", "agent": "...", "action": "...", "reasoning": "...", "grounding": {...}}
```
</trajectory_logging>

<kernel_framework>
## Task
Produce comprehensive PRD by:
1. Ingesting all context from `grimoires/loa/context/`
2. Mapping existing information to 7 discovery phases
3. Conducting targeted interviews for gaps only
4. Generating PRD with full traceability to sources

## Context
- **Input**: `grimoires/loa/context/*.md` (optional), developer interview
- **Output**: `grimoires/loa/prd.md`
- **Integration**: `grimoires/loa/a2a/integration-context.md` (if exists)

## Constraints
- DO NOT ask questions answerable from provided context
- DO cite sources: `> From vision.md:12: "exact quote"`
- DO present understanding for confirmation before proceeding
- DO ask for clarification on contradictions, not assumptions
- DO limit questions to 2-3 per phase maximum

## Verification
PRD traces every requirement to either:
- Source document (file:line citation)
- Interview response (phase:question reference)
</kernel_framework>

<codebase_grounding>
## Phase -0.5: Codebase Grounding (Brownfield Only)

**Purpose**: Ground PRD creation in codebase reality to prevent hallucinated requirements.

### Configuration

Read configuration from `.loa.config.yaml` (with defaults):

```bash
# Check if codebase grounding is enabled (default: true)
enabled=$(yq eval '.plan_and_analyze.codebase_grounding.enabled // true' .loa.config.yaml 2>/dev/null || echo "true")

# Get staleness threshold in days (default: 7)
staleness_days=$(yq eval '.plan_and_analyze.codebase_grounding.reality_staleness_days // 7' .loa.config.yaml 2>/dev/null || echo "7")

# Get /ride timeout in minutes (default: 20)
timeout_minutes=$(yq eval '.plan_and_analyze.codebase_grounding.ride_timeout_minutes // 20' .loa.config.yaml 2>/dev/null || echo "20")

# Get skip-on-error behavior (default: false)
skip_on_error=$(yq eval '.plan_and_analyze.codebase_grounding.skip_on_ride_error // false' .loa.config.yaml 2>/dev/null || echo "false")
```

If `enabled: false`, skip Phase -0.5 entirely (equivalent to GREENFIELD behavior).

### Decision Tree

When `/plan-and-analyze` runs, check the `codebase_detection` pre-flight result:

```
IF config.enabled == false:
    → Skip to Phase -1 (feature disabled)
    → Do NOT mention codebase grounding to user

ELSE IF codebase_detection.type == "GREENFIELD":
    → Skip to Phase -1 (no codebase to analyze)
    → Do NOT mention codebase grounding to user

ELSE IF codebase_detection.type == "BROWNFIELD":
    IF codebase_detection.reality_exists == true:
        IF codebase_detection.reality_age_days < config.staleness_days:
            → Use cached reality (no /ride needed)
            → Show: "Using recent codebase analysis (N days old)"
        ELSE IF --fresh flag provided:
            → Run /ride regardless of cache
        ELSE:
            → Prompt user with AskUserQuestion:
              - "Re-run /ride for fresh analysis (recommended)"
              - "Proceed with existing analysis (faster)"
    ELSE:
        → Run /ride (Phase -0.5)
        → Show progress: "Analyzing codebase structure..."
```

### Running /ride

Invoke the ride skill (NOT the command) for codebase analysis:

```markdown
CODEBASE GROUNDING PHASE

Analyzing your existing codebase to ground PRD requirements in reality.
This typically takes 5-15 minutes depending on codebase size.

Progress:
- [ ] Extracting component inventory
- [ ] Analyzing architecture patterns
- [ ] Identifying existing requirements
- [ ] Building consistency report
```

### /ride Execution

Use the Skill tool to invoke ride:
```
Skill: ride
```

This will produce:
- `grimoires/loa/reality/extracted-prd.md`
- `grimoires/loa/reality/extracted-sdd.md`
- `grimoires/loa/reality/component-inventory.md`
- `grimoires/loa/consistency-report.md`

### Error Recovery

If /ride fails or times out:

1. **Capture error** in NOTES.md Decision Log:
   ```markdown
   | Date | Decision | Rationale | Source |
   |------|----------|-----------|--------|
   | YYYY-MM-DD | /ride failed during codebase grounding | [error message] | Phase -0.5 |
   ```

2. **Check config for auto-skip**:
   ```bash
   skip_on_error=$(yq eval '.plan_and_analyze.codebase_grounding.skip_on_ride_error // false' .loa.config.yaml)
   ```
   If `skip_on_error: true`, automatically skip to Phase -1 with warning.

3. **Otherwise prompt user** with AskUserQuestion:
   ```yaml
   questions:
     - question: "/ride analysis failed. How would you like to proceed?"
       header: "Recovery"
       options:
         - label: "Retry /ride analysis"
           description: "Re-run codebase analysis (recommended)"
         - label: "Skip codebase grounding"
           description: "Proceed without code-based requirements (not recommended)"
         - label: "Abort"
           description: "Cancel /plan-and-analyze entirely"
       multiSelect: false
   ```

4. **Handle user response**:

   **If "Retry"**:
   - Re-run /ride with fresh attempt
   - If fails again, return to step 3 (max 2 retries)

   **If "Skip"**:
   - Log warning to NOTES.md blockers:
     ```markdown
     - [ ] [BLOCKER] PRD created without codebase grounding - /ride failed: [error]
     ```
   - Proceed to Phase -1 without reality context
   - Add warning banner to generated PRD:
     ```markdown
     > ⚠️ **WARNING**: This PRD was created without codebase grounding.
     > Run `/ride` and `/plan-and-analyze --fresh` for accurate requirements.
     ```

   **If "Abort"**:
   - Log abort decision to trajectory
   - Exit cleanly with message: "Aborting /plan-and-analyze. Run /ride manually and retry."

5. **Preserve partial results** if available:
   - If /ride produced any output files before failing, keep them
   - Use whatever reality context exists for Phase 0

### Timeout Handling

Default timeout: 20 minutes (configurable in `.loa.config.yaml`)

```yaml
plan_and_analyze:
  codebase_grounding:
    ride_timeout_minutes: 20
```

### Greenfield Fast Path

For GREENFIELD projects:
- No progress message about codebase
- No delay
- Proceed directly to Phase -1
- Log detection result to trajectory only (not shown to user)
</codebase_grounding>

<workflow>
## Phase -1: Context Assessment

Run context assessment:
```bash
./.claude/scripts/assess-discovery-context.sh
```

| Result | Strategy |
|--------|----------|
| `NO_CONTEXT_DIR` | Create directory, offer guidance, proceed to full interview |
| `EMPTY` | Proceed to full 7-phase interview |
| `SMALL` (<500 lines) | Sequential ingestion, then targeted interview |
| `MEDIUM` (500-2000) | Sequential ingestion, then targeted interview |
| `LARGE` (>2000) | Parallel subagent ingestion, then targeted interview |

## Phase 0: Context Synthesis

### Context Priority Order

Load and synthesize context in priority order:

| Priority | Source | Citation Format | Trust Level |
|----------|--------|-----------------|-------------|
| 1 | `grimoires/loa/reality/` | `[CODE:file:line]` | Highest (code is truth) |
| 2 | `grimoires/loa/context/` | `> From file.md:line` | High (user-provided) |
| 3 | Interview responses | `(Phase N QN)` | Standard |

**Conflict Resolution**: When reality contradicts context:
- Reality wins (code is authoritative)
- Flag the conflict for user: "Note: [context claim] differs from codebase reality [CODE:file:line]"

### Step 0: Present Codebase Understanding (Brownfield Only)

**If reality files exist** (from /ride or cached):

```markdown
## What I've Learned From Your Codebase

Based on analysis of your existing code:

### Architecture
[CODE:src/index.ts:1-50] Your application uses [pattern] architecture with:
- [list key components with code references]

### Existing Features
From component inventory:
- Feature A [CODE:src/features/a.ts:10-45]
- Feature B [CODE:src/services/b.ts:1-100]

### Current State
From consistency report:
- [summary of code consistency findings]

### Proposed Additions
Based on codebase analysis, the following would integrate well:
- [suggested additions grounded in existing patterns]

---
```

### Step 1: Ingest All Context

Read in priority order:
1. `grimoires/loa/reality/*.md` (if exists)
2. `grimoires/loa/context/*.md` (and subdirectories)

### Step 2: Create Context Map
Internally categorize discovered information:

```xml
<context_map>
  <phase name="problem_vision">
    <reality source="extracted-prd.md:10-30">
      Implicit problem statement from codebase
    </reality>
    <found source="vision.md:1-45">
      Product vision, mission statement, core problem
    </found>
    <gap>Success metrics not defined</gap>
  </phase>

  <phase name="goals_metrics">
    <found source="vision.md:47-52">
      High-level goals mentioned
    </found>
    <gap>No quantifiable success criteria</gap>
    <gap>Timeline not specified</gap>
  </phase>

  <phase name="users_stakeholders">
    <found source="users.md:1-289">
      3 personas defined with jobs-to-be-done
    </found>
    <ambiguity>Persona priorities unclear - which is primary?</ambiguity>
  </phase>

  <phase name="functional_requirements">
    <reality source="component-inventory.md:1-200">
      Existing features extracted from code
    </reality>
    <found source="requirements.md:1-100">
      User-documented requirements
    </found>
    <conflict>User docs mention feature X, but not found in codebase</conflict>
  </phase>

  <!-- Continue for all 7 phases -->
</context_map>
```

### Step 3: Present Understanding

**For brownfield projects**, present codebase understanding FIRST:

```markdown
## What I've Learned From Your Codebase

I've analyzed your existing codebase (N files, X lines).

### Existing Architecture
[CODE:src/index.ts:1-50] Your application uses [pattern] with:
- Component A [CODE:src/components/a.tsx:10]
- Service B [CODE:src/services/b.ts:1]

### Implemented Features
Based on code analysis:
- User authentication [CODE:src/auth/index.ts:1-100]
- Data persistence [CODE:src/db/client.ts:1-50]

---

## What I've Learned From Your Documentation

I've reviewed N files (X lines) from your context directory.

### Problem & Vision
> From vision.md:12-15: "exact quote from document..."

I understand the core problem is [summary]. The vision is [summary].

### Users & Stakeholders
> From users.md:23-45: "description of personas..."

You've defined N personas: [list with 1-line each].

### Conflicts Noted
- [if any conflicts between reality and context]

### What I Still Need to Understand
1. **Success Metrics**: What quantifiable outcomes define success?
2. **Persona Priority**: Which user persona should we optimize for first?
3. **Timeline**: What are the key milestones and deadlines?

Should I proceed with these clarifying questions, or would you like to
correct my understanding first?
```

## Phase 0.5: Targeted Interview

**For each gap/ambiguity identified:**

1. State what you know (with citation)
2. State what's missing or unclear
3. Ask focused question (max 2-3 per phase)

**Example:**
```markdown
### Goals & Success Metrics

I found high-level goals in vision.md:
> "Achieve product-market fit within 12 months"

However, I didn't find specific success metrics.

**Questions:**
1. What metrics would indicate product-market fit for this product?
2. Are there intermediate milestones (3-month, 6-month)?
```

## Phases 1-7: Conditional Discovery

For each phase, follow this logic:

```
IF phase fully covered by context:
  → Summarize understanding with citations
  → Ask: "Is this accurate? Any corrections?"
  → Move to next phase

ELSE IF phase partially covered:
  → Summarize what's known (with citations)
  → Ask only about gaps (max 2-3 questions)
  → Move to next phase

ELSE IF phase not covered:
  → Conduct full discovery for this phase
  → Ask 2-3 questions at a time
  → Iterate until complete
```

### Phase 1: Problem & Vision
- Core problem being solved
- Product vision and mission
- Why now? Why you?

### Phase 2: Goals & Success Metrics
- Business objectives
- Quantifiable success criteria
- Timeline and milestones

### Phase 3: User & Stakeholder Context
- Primary and secondary personas
- User journey and pain points
- Stakeholder requirements

### Phase 4: Functional Requirements
- Core features and capabilities
- User stories with acceptance criteria
- Feature prioritization

#### EARS Notation (Optional)

For high-precision requirements, use EARS notation from
`resources/templates/ears-requirements.md`:

| Pattern | Format | Use When |
|---------|--------|----------|
| Ubiquitous | `The system shall [action]` | Always-true requirements |
| Event-Driven | `When [trigger], the system shall [action]` | Trigger-based behavior |
| Conditional | `If [condition], the system shall [action]` | Precondition-based |

**When to use EARS**: Security-critical features, regulatory compliance, complex triggers.

### Phase 5: Technical & Non-Functional
- Performance requirements
- Security and compliance
- Integration requirements
- Technical constraints

### Phase 6: Scope & Prioritization
- MVP definition
- Phase 1 vs future scope
- Out of scope (explicit)

### Phase 7: Risks & Dependencies
- Technical risks
- Business risks
- External dependencies
- Mitigation strategies

## Phase 8: PRD Generation

Only generate PRD when:
- [ ] All 7 phases have sufficient coverage
- [ ] All ambiguities resolved
- [ ] Developer confirms understanding is accurate

Generate PRD with source tracing:
```markdown
## 1. Problem Statement

[Content derived from vision.md:12-30 and Phase 1 interview]

> Sources: vision.md:12-15, confirmed in Phase 1 Q2
```
</workflow>

<parallel_execution>
## Large Context Handling (>2000 lines)

If context assessment returns `LARGE`:

### Spawn Parallel Ingestors
```
Task(subagent_type="Explore", prompt="
CONTEXT INGESTION: Problem & Vision

Read these files: [vision.md, any *vision* or *problem* files]
Extract and summarize:
- Core problem statement
- Product vision
- Mission/purpose
- 'Why now' factors

Return as structured summary with file:line citations.
")
```

Spawn 4 parallel ingestors:
1. **Vision Ingestor**: Problem, vision, mission
2. **User Ingestor**: Personas, research, journeys
3. **Requirements Ingestor**: Features, stories, specs
4. **Technical Ingestor**: Constraints, stack, integrations

### Consolidate
Merge summaries into unified context map before proceeding.
</parallel_execution>

<output_format>
PRD structure with source tracing - see `resources/templates/prd-template.md`

Each section must include:
```markdown
> **Sources**: vision.md:12-30, users.md:45-67, Phase 3 Q1-Q2
```
</output_format>

<success_criteria>
- **Specific**: Every PRD requirement traced to source (file:line, [CODE:file:line], or phase:question)
- **Measurable**: Questions reduced by 50%+ when context provided
- **Achievable**: Synthesis completes before any interview questions
- **Relevant**: Developer confirms understanding before proceeding
- **Time-bound**: Context synthesis <5 min for SMALL/MEDIUM
- **Grounded**: Brownfield PRDs cite existing code with [CODE:file:line] format
- **Zero Latency**: Greenfield projects experience no codebase detection delay
</success_criteria>

<uncertainty_protocol>
- If context files contradict each other → Ask developer to clarify
- If context is ambiguous → State interpretation, ask for confirmation
- If context seems outdated → Ask if still accurate
- Never assume → Always cite or ask
</uncertainty_protocol>

<grounding_requirements>
Every claim about existing context must include citation:
- Format: `> From {filename}:{line}: "exact quote"`
- Summaries must reference source range: `(vision.md:12-45)`
- PRD sections must list all sources used
</grounding_requirements>

<edge_cases>
| Scenario | Behavior |
|----------|----------|
| No context directory | Create it, add README.md, proceed to full interview |
| Empty context directory | Note it, proceed to full interview |
| Only README.md exists | Treat as empty, proceed to full interview |
| Contradictory information | List contradictions, ask developer to clarify |
| Outdated information | Ask "Is this still accurate?" before using |
| Very large files (>1000 lines) | Summarize key sections, note full file available |
| Non-markdown files | Note existence, explain can't parse |
| Partial coverage | Conduct mini-interviews for gaps only |
| Developer disagrees with synthesis | Allow corrections, update understanding |
| Reality conflicts with context | Reality wins, flag conflict for user review |
| Stale reality (>7 days) | Prompt user to refresh or proceed with cached |
| /ride failed | Log blocker, proceed without grounding (with warning) |
| Brownfield detected but no reality | Run /ride before Phase -1 |
| Greenfield project | Skip codebase grounding entirely, no message |
</edge_cases>

<visual_communication>
## Visual Communication (Optional)

Follow `.claude/protocols/visual-communication.md` for diagram standards.

### When to Include Diagrams

PRDs may benefit from visual aids for:
- **User Journeys** (flowchart) - Show user flows through the product
- **Process Flows** (flowchart) - Illustrate business processes
- **Stakeholder Maps** (flowchart) - Show stakeholder relationships

### Output Format

If including diagrams, use Mermaid with preview URLs:

```markdown
### User Registration Journey

```mermaid
graph LR
    A[Landing Page] --> B{Has Account?}
    B -->|No| C[Sign Up Form]
    B -->|Yes| D[Login]
    C --> E[Email Verification]
    E --> F[Onboarding]
    F --> G[Dashboard]
```

> **Preview**: [View diagram](https://agents.craft.do/mermaid?code=...&theme=github)
```

### Theme Configuration

Read theme from `.loa.config.yaml` visual_communication.theme setting.

Diagram inclusion is **optional** for PRDs - use agent discretion based on complexity.
</visual_communication>
