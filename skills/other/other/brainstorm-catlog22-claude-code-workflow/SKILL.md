---
name: brainstorm
description: Unified brainstorming skill with dual-mode operation - auto pipeline and single role analysis. Triggers on "brainstorm", "头脑风暴".
allowed-tools: Skill(*), Task(conceptual-planning-agent, context-search-agent), AskUserQuestion(*), TodoWrite(*), Read(*), Write(*), Edit(*), Glob(*), Bash(*)
---

# Brainstorm

Unified brainstorming skill combining interactive framework generation, multi-role parallel analysis, and cross-role synthesis into a single entry point with two operational modes.

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    /brainstorm                                │
│         Unified Entry Point + Interactive Routing             │
└───────────────────────┬─────────────────────────────────────┘
                        │
              ┌─────────┴─────────┐
              ↓                   ↓
    ┌─────────────────┐  ┌──────────────────┐
    │   Auto Mode     │  │ Single Role Mode │
    │  (自动模式)      │  │ (单角色分析模式)   │
    └────────┬────────┘  └────────┬─────────┘
             │                    │
    ┌────────┼────────┐          │
    ↓        ↓        ↓          ↓
 Phase 2  Phase 3  Phase 4    Phase 3
Artifacts  N×Role  Synthesis  1×Role
 (7步)    Analysis  (8步)    Analysis
           并行               (4步)
```

**Data Flow**:
```
Auto Mode:
  Phase 2 (artifacts) → guidance-specification.md + selected_roles[]
    → Phase 3 (N × role-analysis) → {role}/analysis*.md (immutable)
      → Phase 4 (synthesis) → feature-specs/ + feature-index.json + synthesis-changelog.md

Single Role Mode:
  Phase 3 (1 × role-analysis) → {role}/analysis*.md
```

## Key Design Principles

1. **Dual-Mode Routing**: Interactive mode selection via AskUserQuestion, with parameter-based auto-detection
2. **Progressive Phase Loading**: Phase files loaded on-demand via `Ref:` markers, not all at once
3. **Task Attachment/Collapse**: Sub-tasks attached during phase execution, collapsed after completion
4. **Session Continuity**: All phases share session state via workflow-session.json
5. **Auto-Continue Execution**: Phases chain automatically without user intervention between them

## Auto Mode

When `--yes` or `-y`: Auto-select auto mode, skip interactive routing question, auto-select recommended roles, skip all clarification questions, use default answers.

## Execution Flow

### Phase 1: Mode Detection & Interactive Routing
   Ref: phases/01-mode-routing.md

Parse arguments, detect mode from flags/parameters, or ask user via AskUserQuestion.

**Mode Detection Rules**:
1. If `--yes` or `-y` flag present → **Auto Mode** (no question asked)
2. If first arg matches a known role name → **Single Role Mode** (no question asked)
3. If `--session` flag present without role name → **Ask user**
4. Otherwise → **Ask user via AskUserQuestion**

**Output**: `execution_mode` ("auto" | "single-role"), parsed parameters

---

### Auto Mode Execution (execution_mode = "auto")

#### Phase 2: Interactive Framework Generation
   Ref: phases/02-artifacts.md

Seven-phase interactive workflow: Context collection → Topic analysis → Role selection → Role questions → Conflict resolution → Final check → Generate specification.

**Input**: topic description, --count N, --yes flag
**Output**: guidance-specification.md, workflow-session.json (selected_roles[], session_id)

**TodoWrite**: Attach 7 sub-tasks (Phase 0-5), execute sequentially, collapse on completion.

#### Phase 3: Parallel Role Analysis
   Ref: phases/03-role-analysis.md

Execute role analysis for EACH selected role in parallel.

**Input**: selected_roles[] from Phase 2, session_id, guidance-specification.md
**Output**: {role}/analysis*.md for each role

**Parallel Execution**: Launch N role-analysis calls simultaneously (one message with multiple Skill invokes). Each role with `--skip-questions` flag.

For ui-designer: append `--style-skill {package}` if provided.

**TodoWrite**: Attach N parallel sub-tasks, execute concurrently, collapse on completion.

#### Phase 4: Synthesis Integration
   Ref: phases/04-synthesis.md

Six-phase synthesis: Discovery → File discovery → Cross-role analysis → User interaction → Spec generation (single agent, sequential) + Conditional review → Finalization. Role analysis files are read-only (never modified). Spec is the final synthesis artifact.

**Input**: session_id from Phase 2, all role analysis files from Phase 3 (read-only)
**Output**: feature-specs/, feature-index.json, synthesis-changelog.md

**TodoWrite**: Attach synthesis sub-tasks, execute sequentially, collapse on completion.

---

### Single Role Mode Execution (execution_mode = "single-role")

#### Phase 3: Single Role Analysis
   Ref: phases/03-role-analysis.md

Execute role analysis for ONE specified role with optional interactive context gathering.

**Input**: role_name, --session, --update, --include-questions, --skip-questions, --style-skill
**Output**: {role}/analysis*.md

**TodoWrite**: Attach 4 sub-tasks (Detection → Context → Agent → Validation), execute sequentially.

---

**Phase Reference Documents** (read on-demand when phase executes):

| Phase | Document | Purpose | Used By |
|-------|----------|---------|---------|
| 1 | [phases/01-mode-routing.md](phases/01-mode-routing.md) | Parameter parsing, mode detection, interactive routing | Both modes |
| 2 | [phases/02-artifacts.md](phases/02-artifacts.md) | Interactive framework generation (7 phases) | Auto mode only |
| 3 | [phases/03-role-analysis.md](phases/03-role-analysis.md) | Role-specific analysis generation | Both modes |
| 4 | [phases/04-synthesis.md](phases/04-synthesis.md) | Cross-role synthesis and feature specs | Auto mode only |

## Core Rules

1. **Start with Mode Detection**: First action is Phase 1 (parse args + detect mode)
2. **Interactive Routing**: If mode cannot be determined from args, ASK user via AskUserQuestion
3. **No Preliminary Analysis**: Do not analyze topic before Phase 2 - artifacts handles all analysis
4. **Parse Every Output**: Extract selected_roles from workflow-session.json after Phase 2
5. **Auto-Continue via TodoList**: Check TodoList status to execute next pending phase automatically
6. **Task Attachment Model**: Skill and Task executes attach sub-tasks to current workflow
7. **⚠️ CRITICAL: DO NOT STOP**: Continuous multi-phase workflow in auto mode. After executing all attached tasks, immediately collapse them and execute next phase
8. **Parallel Execution**: Auto mode Phase 3 attaches multiple agent tasks simultaneously for concurrent execution
9. **Single Role Independence**: Single role mode operates independently without requiring artifacts or synthesis

## Input Processing

### Parameter Parsing

```javascript
// Parse from user input (argument string)
const args = parseArguments(user_input);

// Flags
const auto_yes = args.includes('--yes') || args.includes('-y');
const count = extractFlag(args, '--count', 3);  // default 3, max 9
const session_id = extractFlag(args, '--session', null);
const update_mode = args.includes('--update');
const include_questions = args.includes('--include-questions');
const skip_questions = args.includes('--skip-questions');
const style_skill = extractFlag(args, '--style-skill', null);

// Role detection
const VALID_ROLES = [
  'data-architect', 'product-manager', 'product-owner', 'scrum-master',
  'subject-matter-expert', 'system-architect', 'test-strategist',
  'ui-designer', 'ux-expert'
];
const first_arg = args[0]; // first non-flag argument
const is_role = VALID_ROLES.includes(first_arg);

// Mode detection
if (auto_yes) {
  execution_mode = 'auto';
  topic = extractTopic(args);
} else if (is_role) {
  execution_mode = 'single-role';
  role_name = first_arg;
} else {
  execution_mode = null;  // Ask user
  topic = extractTopic(args);
}
```

### Usage Examples

```bash
# Auto mode - full pipeline
/brainstorm "Build real-time collaboration platform" --count 3
/brainstorm -y "GOAL: Build platform SCOPE: 100 users" --count 5
/brainstorm "Design payment system" --style-skill material-design

# Single role mode - individual analysis
/brainstorm system-architect --session WFS-xxx
/brainstorm ux-expert --include-questions
/brainstorm ui-designer --session WFS-xxx --update --style-skill material-design
/brainstorm product-manager --skip-questions

# Ambiguous - will ask interactively
/brainstorm --session WFS-xxx
/brainstorm
```

## Data Flow

```
Phase 1 (Mode Routing):
  Input:  user arguments
  Output: execution_mode, parsed_params
          ↓
  ┌───────┴───────┐
  Auto            Single Role
  ↓               ↓
Phase 2:          Phase 3:
  Input:  topic, count, auto_yes
  Output: session_id ─────────────→ Input: role_name, session_id
          selected_roles[]                  skip/include questions
          guidance-specification.md         style_skill
          ↓                         Output: {role}/analysis*.md
Phase 3:
  Input:  selected_roles[], session_id
          guidance-specification.md
          style_skill (for ui-designer)
  Output: {role}/analysis*.md (N files, immutable after this point)
          ↓
Phase 4:
  Input:  session_id, all analysis files (read-only)
  Output: feature-specs/F-{id}-{slug}.md
          feature-index.json
          synthesis-changelog.md
```

## TodoWrite Pattern

### Auto Mode Lifecycle

```
Initial → Phase 1 Mode Routing (completed)
       → Phase 2 Artifacts (in_progress)
           → 7 sub-tasks ATTACHED (Phase 0-5)
           → Execute sequentially
           → Sub-tasks COLLAPSED
       → Phase 3 Parallel Role Analysis (in_progress)
           → N role sub-tasks ATTACHED simultaneously
           → Execute concurrently
           → Sub-tasks COLLAPSED
       → Phase 4 Synthesis (in_progress)
           → 8 sub-tasks ATTACHED
           → Execute sequentially
           → Sub-tasks COLLAPSED
       → All completed
```

### Single Role Mode Lifecycle

```
Initial → Phase 1 Mode Routing (completed)
       → Phase 3 Role Analysis (in_progress)
           → 4 sub-tasks ATTACHED (Detection → Context → Agent → Validation)
           → Execute sequentially
           → Sub-tasks COLLAPSED
       → Completed
```

### Initial TodoWrite (Auto Mode)

```json
[
  {"content": "Phase 1: Mode detection and parameter parsing", "status": "in_progress", "activeForm": "Detecting mode"},
  {"content": "Phase 2: Interactive Framework Generation", "status": "pending", "activeForm": "Generating framework"},
  {"content": "Phase 3: Parallel Role Analysis", "status": "pending", "activeForm": "Executing parallel analysis"},
  {"content": "Phase 4: Synthesis Integration", "status": "pending", "activeForm": "Executing synthesis"}
]
```

### Initial TodoWrite (Single Role Mode)

```json
[
  {"content": "Phase 1: Mode detection and parameter parsing", "status": "in_progress", "activeForm": "Detecting mode"},
  {"content": "Phase 3: Single role analysis for {role_name}", "status": "pending", "activeForm": "Executing role analysis"}
]
```

## Session Management

**⚡ FIRST ACTION**: Check `.workflow/active/` for existing sessions

**Multiple Sessions Support**:
- Different Claude instances can have different brainstorming sessions
- If multiple sessions found, prompt user to select
- If single session found, use it
- If no session exists:
  - Auto mode: Create `WFS-[topic-slug]`
  - Single role mode: ERROR if no session (must run auto mode first)

**Session Continuity**: All phases share session state via `workflow-session.json`

## Available Roles

| Role ID | Title | Focus Area |
|---------|-------|------------|
| `data-architect` | 数据架构师 | Data models, storage strategies, data flow |
| `product-manager` | 产品经理 | Product strategy, roadmap, prioritization |
| `product-owner` | 产品负责人 | Backlog management, user stories, acceptance criteria |
| `scrum-master` | 敏捷教练 | Process facilitation, impediment removal |
| `subject-matter-expert` | 领域专家 | Domain knowledge, business rules, compliance |
| `system-architect` | 系统架构师 | Technical architecture, scalability, integration |
| `test-strategist` | 测试策略师 | Test strategy, quality assurance |
| `ui-designer` | UI设计师 | Visual design, mockups, design systems |
| `ux-expert` | UX专家 | User research, information architecture, journey |

**Role Selection**: Auto mode → handled by artifacts (Phase 2). Single role mode → user specifies directly.

## Output Structure

```
.workflow/active/WFS-{topic}/
├── workflow-session.json              # Session metadata ONLY
├── .process/
│   └── context-package.json           # Phase 0 output (auto mode)
└── .brainstorming/
    ├── guidance-specification.md      # Framework (Phase 2, auto mode)
    ├── feature-index.json             # Feature index (Phase 4, auto mode, feature_mode)
    ├── synthesis-changelog.md         # Synthesis decisions audit trail (Phase 4, auto mode)
    ├── feature-specs/                 # Feature specs (Phase 4, auto mode, feature_mode)
    │   ├── F-001-{slug}.md
    │   └── F-00N-{slug}.md
    ├── {role}/                        # Role analyses (IMMUTABLE after Phase 3)
    │   ├── {role}-context.md          # Interactive Q&A responses
    │   ├── analysis.md                # Main/index document
    │   ├── analysis-cross-cutting.md  # Cross-feature (feature_mode)
    │   └── analysis-F-{id}-{slug}.md  # Per-feature (feature_mode)
    └── synthesis-specification.md     # Integration (Phase 4, non-feature_mode only)
```

## Error Handling

| Error | Recovery | Mode |
|-------|----------|------|
| Invalid role name | Show valid roles list, ask again | Single Role |
| No active session | Auto mode: create new. Single role: error with guidance | Both |
| Role selection failure | Default to product-manager | Auto |
| Agent execution failure | Agent-specific retry with minimal dependencies | Both |
| Template loading issues | Graceful degradation | Both |
| Synthesis conflicts | Highlight disagreements without forced resolution | Auto |
| Context overflow (>100KB) | Read only analysis.md index files | Auto |

**Context Overflow Protection**:
- Per-role limits: < 3000 words main, < 2000 words sub-docs, max 5 sub-docs
- Synthesis protection: If total > 100KB, read only `analysis.md` (not sub-documents)
- Recovery: reduce scope (--count 2) → use --summary-only → manual synthesis

## Coordinator Checklist

**Pre-Phase Actions**:
- [ ] Read Phase document via `Ref:` marker
- [ ] Verify prerequisites (session exists, required files present)
- [ ] Mark phase as `in_progress` in TodoWrite
- [ ] Attach sub-tasks if applicable

**Post-Phase Actions**:
- [ ] Validate phase outputs exist
- [ ] Collapse sub-tasks to phase summary
- [ ] Mark phase as `completed` in TodoWrite
- [ ] Auto-continue to next pending phase (auto mode)
- [ ] Report completion (single role mode)

## Related Commands

**Prerequisites**:
- `/workflow:session:start` - Start a new workflow session (optional, brainstorm creates its own)

**Follow-ups** (after brainstorm completes):
- `/workflow:plan --session {sessionId}` - Generate implementation plan
- `/workflow:brainstorm:synthesis --session {sessionId}` - Run synthesis standalone (if skipped)

## Reference Information

**Template Source**: `~/.ccw/workflows/cli-templates/planning-roles/`
**Style SKILL Packages**: `.claude/skills/style-{package-name}/`
