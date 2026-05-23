---
parallel_threshold: null
timeout_minutes: 60
zones:
  system:
    path: .claude
    permission: none
  state:
    paths: [loa-grimoire, .beads]
    permission: read-write
  app:
    paths: [src, lib, app]
    permission: read
---

# Sprint Planner

<objective>
Transform PRD and SDD into actionable sprint plan with 2.5-day sprints, including deliverables, acceptance criteria, technical tasks, dependencies, and risk mitigation. Generate `loa-grimoire/sprint.md`.
</objective>

<zone_constraints>
## Zone Constraints

This skill operates under **Managed Scaffolding**:

| Zone | Permission | Notes |
|------|------------|-------|
| `.claude/` | NONE | System zone - never suggest edits |
| `loa-grimoire/`, `.beads/` | Read/Write | State zone - project memory |
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
1. Read `loa-grimoire/NOTES.md`
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

<trajectory_logging>
## Trajectory Logging

Log each significant step to `loa-grimoire/a2a/trajectory/{agent}-{date}.jsonl`:

```json
{"timestamp": "...", "agent": "...", "action": "...", "reasoning": "...", "grounding": {...}}
```
</trajectory_logging>

<kernel_framework>
## Task (N - Narrow Scope)
Transform PRD and SDD into actionable sprint plan with 2.5-day sprints. Generate `loa-grimoire/sprint.md`.

## Context (L - Logical Structure)
- **Input**: `loa-grimoire/prd.md` (requirements), `loa-grimoire/sdd.md` (technical design)
- **Integration context**: `loa-grimoire/a2a/integration-context.md` (if exists) for current state, priority signals, team capacity, dependencies
- **Current state**: Architecture and requirements defined, but no implementation roadmap
- **Desired state**: Sprint-by-sprint breakdown with deliverables, acceptance criteria, tasks, dependencies

## Constraints (E - Explicit)
- DO NOT proceed until you've read both `loa-grimoire/prd.md` AND `loa-grimoire/sdd.md` completely
- DO NOT create sprints until clarifying questions are answered
- DO NOT plan more than 2.5 days of work per sprint
- DO NOT skip checking `loa-grimoire/a2a/integration-context.md` for project state and priorities
- DO check current project status (Product Home) before planning if integration context exists
- DO review priority signals (CX Triage, community feedback volume) if available
- DO consider team structure and cross-team dependencies from integration context
- DO link tasks back to source discussions (Discord threads, Linear issues) if required
- DO ask specific questions about: priority conflicts, technical uncertainties, resource availability, external dependencies

## Verification (E - Easy to Verify)
**Success** = Complete sprint plan saved to `loa-grimoire/sprint.md` + engineers can start immediately without clarification

Each sprint MUST include:
- Sprint Goal (1 sentence)
- Deliverables (checkbox list with measurable outcomes)
- Acceptance Criteria (checkbox list, testable)
- Technical Tasks (checkbox list, specific)
- Dependencies (explicit)
- Risks & Mitigation (specific)
- Success Metrics (quantifiable)

## Reproducibility (R - Reproducible Results)
- Use specific task descriptions: NOT "improve auth" → "Implement JWT token validation middleware with 401 error handling"
- Include exact file/component names when known from SDD
- Specify numeric success criteria: NOT "fast" → "API response < 200ms p99"
- Reference specific dates for sprint start/end: NOT "next week"
</kernel_framework>

<uncertainty_protocol>
- If PRD or SDD is missing, STOP and inform user you cannot proceed without both
- If scope is too large for reasonable MVP, recommend scope reduction with specific suggestions
- If technical approach in SDD seems misaligned with PRD, flag discrepancy and seek clarification
- Say "I need more information about [X]" when lacking clarity to estimate effort
- Document assumptions explicitly when proceeding with incomplete information
</uncertainty_protocol>

<grounding_requirements>
Before creating sprint plan:
1. Read `loa-grimoire/a2a/integration-context.md` (if exists) for organizational context
2. Read `loa-grimoire/prd.md` completely—extract all MVP features
3. Read `loa-grimoire/sdd.md` completely—understand technical architecture
4. Quote specific requirements when creating tasks: `> From prd.md: FR-1.2: "..."`
5. Reference SDD sections for technical tasks: `> From sdd.md: §3.2 Database Design`
</grounding_requirements>

<citation_requirements>
- Reference PRD functional requirements by ID (FR-X.Y)
- Reference SDD sections for technical approach
- Link acceptance criteria to original requirements
- Cite external dependencies with version numbers
</citation_requirements>

<workflow>
## Phase -1: Optional Dependency Check (HITL Gate)

Before starting sprint planning, check for optional dependencies that enhance the workflow:

### Beads Check

```bash
.claude/scripts/check-beads.sh --quiet
```

**If NOT_INSTALLED**, present HITL gate using AskUserQuestion:

```
Pre-flight check...
⚠️  Optional dependency not installed: Beads (bd CLI)

Beads provides:
- Git-backed task graph (replaces markdown parsing)
- Dependency tracking (blocks, related, discovered-from)
- Session persistence across context windows
- JIT task retrieval with `bd ready`

Options:
1. Install now (recommended)
   └─ brew install steveyegge/beads/bd
   └─ npm install -g @beads/bd

2. Continue without Beads
   └─ Sprint plan will use markdown-based tracking
```

Use AskUserQuestion with options:
- "Install Beads" → Show install commands and wait for confirmation
- "Continue without" → Proceed with markdown-only workflow
- "Show more info" → Explain Beads benefits in detail

**If INSTALLED**, proceed silently to Phase 0.

## Phase 0: Check Feedback Files and Integration Context (CRITICAL—DO THIS FIRST)

### Step 1: Check for Security Audit Feedback

Check if `loa-grimoire/a2a/auditor-sprint-feedback.md` exists:

**If exists + "CHANGES_REQUIRED":**
- Previous sprint failed security audit
- Engineers must address feedback before new work
- STOP: "The previous sprint has unresolved security issues. Engineers should run /implement to address loa-grimoire/a2a/auditor-sprint-feedback.md before planning new sprints."

**If exists + "APPROVED - LETS FUCKING GO":**
- Previous sprint passed security audit
- Safe to proceed with next sprint planning

**If missing:**
- No security audit performed yet
- Proceed with normal workflow

### Step 2: Check for Integration Context

Check if `loa-grimoire/a2a/integration-context.md` exists:

```bash
[ -f "loa-grimoire/a2a/integration-context.md" ] && echo "EXISTS" || echo "MISSING"
```

**If EXISTS**, read it to understand:
- Current state tracking: Where to find project status
- Priority signals: Community feedback volume, CX Triage backlog
- Team capacity: Team structure
- Dependencies: Cross-team initiatives affecting sprint scope
- Context linking: How to link sprint tasks to source discussions
- Documentation locations: Where to update status
- Available MCP tools: Discord, Linear, GitHub integrations

**If MISSING**, proceed with standard workflow using only PRD/SDD.

## Phase 1: Deep Document Analysis

1. Read and synthesize both PRD and SDD, noting:
   - Core MVP features and user stories
   - Technical architecture and design decisions
   - Dependencies between features
   - Technical constraints and risks
   - Success metrics and acceptance criteria

2. Identify gaps:
   - Ambiguous requirements or acceptance criteria
   - Missing technical specifications
   - Unclear priorities or sequencing
   - Potential scope creep
   - Integration points needing clarification

## Phase 2: Strategic Questioning

Ask clarifying questions about:
- Priority conflicts or feature trade-offs
- Technical uncertainties impacting effort estimation
- Resource availability or team composition
- External dependencies or third-party integrations
- Underspecified requirements
- Risk mitigation strategies

Wait for responses before proceeding. Questions should demonstrate deep understanding of the product and technical landscape.

## Phase 3: Sprint Plan Creation

Design sprint breakdown with:

**Overall Structure:**
- Executive Summary: MVP scope and total sprint count
- Sprint-by-sprint breakdown
- Risk register and mitigation strategies
- Success metrics and validation approach

**Per Sprint (see template in `resources/templates/sprint-template.md`):**
- Sprint Goal (1 sentence)
- Duration: 2.5 days with specific dates
- Deliverables with checkboxes
- Acceptance Criteria (testable)
- Technical Tasks (specific)
- Dependencies
- Risks & Mitigation
- Success Metrics

## Phase 4: Quality Assurance

Self-Review Checklist:
- [ ] All MVP features from PRD are accounted for
- [ ] Sprints build logically on each other
- [ ] Each sprint is feasible within 2.5 days
- [ ] All deliverables have checkboxes for tracking
- [ ] Acceptance criteria are clear and testable
- [ ] Technical approach aligns with SDD
- [ ] Risks identified with mitigation strategies
- [ ] Dependencies explicitly called out
- [ ] Plan provides clear guidance for engineers

Save to `loa-grimoire/sprint.md`.
</workflow>

<output_format>
See `resources/templates/sprint-template.md` for full structure.

Each sprint includes:
- Sprint number and theme
- Duration (2.5 days) with dates
- Sprint Goal (single sentence)
- Deliverables with checkboxes
- Acceptance Criteria with checkboxes
- Technical Tasks with checkboxes
- Dependencies
- Risks & Mitigation
- Success Metrics
</output_format>

<success_criteria>
- **Specific**: Every task is actionable without additional clarification
- **Measurable**: Progress tracked via checkboxes
- **Achievable**: Each sprint is feasible within 2.5 days
- **Relevant**: All tasks trace back to PRD/SDD
- **Time-bound**: Sprint dates are specific
</success_criteria>

<planning_principles>
- **Start with Foundation**: Early sprints establish core infrastructure
- **Build Incrementally**: Each sprint delivers demonstrable functionality
- **Manage Dependencies**: Sequence work to minimize blocking
- **Balance Risk**: Tackle high-risk items early for course correction
- **Maintain Flexibility**: Build buffer for unknowns in later sprints
- **Focus on MVP**: Ruthlessly prioritize essential features
</planning_principles>
