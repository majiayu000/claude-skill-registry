---
name: workflow-skill-designer
description: Meta-skill for designing orchestrator+phases structured workflow skills. Creates SKILL.md coordinator with progressive phase loading, TodoWrite patterns, and data flow. Triggers on "design workflow skill", "create workflow skill", "workflow skill designer".
allowed-tools: Agent, AskUserQuestion, TodoWrite, Read, Write, Edit, Bash, Glob, Grep
---

# Workflow Skill Designer

Meta-skill for creating structured workflow skills following the orchestrator + phases pattern. Generates complete skill packages with SKILL.md as coordinator and phases/ folder for execution details.

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│  Workflow Skill Designer                                         │
│  → Analyze requirements → Design orchestrator → Generate phases  │
└───────────────┬─────────────────────────────────────────────────┘
                │
    ┌───────────┼───────────┬───────────┐
    ↓           ↓           ↓           ↓
┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐
│ Phase 1 │ │ Phase 2 │ │ Phase 3 │ │ Phase 4 │
│ Require │ │  Orch   │ │ Phases  │ │ Valid   │
│ Analysis│ │ Design  │ │ Design  │ │ & Integ │
└─────────┘ └─────────┘ └─────────┘ └─────────┘
     ↓           ↓           ↓           ↓
  workflow    SKILL.md    phases/     Complete
  config     generated   0N-*.md     skill pkg
```

## Target Output Structure

The skill this meta-skill produces follows this structure:

```
.claude/skills/{skill-name}/
├── SKILL.md                    # Orchestrator: coordination, data flow, TodoWrite
├── phases/
│   ├── 01-{phase-name}.md      # Phase execution detail (full content)
│   ├── 02-{phase-name}.md
│   ├── ...
│   └── 0N-{phase-name}.md
├── specs/                      # [Optional] Domain specifications
└── templates/                  # [Optional] Reusable templates
```

## Core Design Patterns

Patterns extracted from successful workflow skill implementations (workflow-plan, project-analyze, etc.):

### Pattern 1: Orchestrator + Progressive Loading

**SKILL.md** = Pure coordinator. Contains:
- Architecture diagram (ASCII)
- Execution flow with `Ref: phases/0N-xxx.md` markers
- Phase Reference Documents table (read on-demand)
- Data flow between phases
- Core rules and error handling

**Phase files** = Full execution detail. Contains:
- Complete agent prompts, bash commands, code implementations
- Validation checklists, error handling
- Input/Output specification
- Next Phase link

**Key Rule**: SKILL.md references phase docs via `Ref:` markers. Phase docs are read **only when that phase executes**, not all at once.

### Pattern 2: TodoWrite Attachment/Collapse

```
Phase starts:
  → Sub-tasks ATTACHED to TodoWrite (in_progress + pending)
  → Orchestrator executes sub-tasks sequentially

Phase ends:
  → Sub-tasks COLLAPSED back to high-level summary (completed)
  → Next phase begins
```

### Pattern 3: Inter-Phase Data Flow

```
Phase N output → stored in memory/variable → Phase N+1 input
                  └─ or written to session file for persistence
```

Each phase receives outputs from prior phases via:
- In-memory variables (sessionId, contextPath, etc.)
- Session directory files (.workflow/active/{sessionId}/...)
- Planning notes (accumulated constraints document)

### Pattern 4: Conditional Phase Execution

```
Phase N output contains condition flag
  ├─ condition met → Execute Phase N+1
  └─ condition not met → Skip to Phase N+2
```

### Pattern 5: Input Structuring

User input (free text) → Structured format before Phase 1:
```
GOAL: [objective]
SCOPE: [boundaries]
CONTEXT: [background/constraints]
```

### Pattern 6: Interactive Preference Collection (SKILL.md Responsibility)

Workflow preferences (auto mode, force explore, etc.) MUST be collected via AskUserQuestion in SKILL.md **before** dispatching to phases. Phases reference these as `workflowPreferences.{key}` context variables.

**Anti-Pattern**: Command-line flags (`--yes`, `-e`, `--explore`) parsed within phase files via `$ARGUMENTS.includes(...)`.

```javascript
// CORRECT: In SKILL.md (before phase dispatch)
const prefResponse = AskUserQuestion({
  questions: [
    { question: "是否跳过确认？", header: "Auto Mode", options: [
      { label: "Interactive (Recommended)", description: "交互模式" },
      { label: "Auto", description: "跳过所有确认" }
    ]}
  ]
})
workflowPreferences = { autoYes: prefResponse.autoMode === 'Auto' }

// CORRECT: In phase files (reference only)
const autoYes = workflowPreferences.autoYes

// WRONG: In phase files (flag parsing)
const autoYes = $ARGUMENTS.includes('--yes') || $ARGUMENTS.includes('-y')
```

### Pattern 7: Direct Phase Handoff

When one phase needs to invoke another phase within the same skill, read and execute the phase document directly. Do NOT use Skill() routing back through SKILL.md.

```javascript
// CORRECT: Direct handoff (executionContext already set)
Read("phases/02-lite-execute.md")
// Execute with executionContext (Mode 1)

// WRONG: Skill routing (unnecessary round-trip)
Skill(skill="workflow-lite-plan", args="--in-memory")
```

### Pattern 8: Phase File Hygiene

Phase files are internal execution documents. They MUST NOT contain:

| Prohibited | Reason | Correct Location |
|------------|--------|------------------|
| Flag parsing (`$ARGUMENTS.includes(...)`) | Preferences collected in SKILL.md | SKILL.md via AskUserQuestion |
| Invocation syntax (`/skill-name "..."`) | Not user-facing docs | Removed or SKILL.md only |
| Conversion provenance (`Source: Converted from...`) | Implementation detail | Removed |
| Skill routing for inter-phase (`Skill(skill="...")`) | Use direct phase read | Direct `Read("phases/...")` |

### Pattern 9: Compact Recovery (Phase Persistence)

Multi-phase workflows span long conversations. Context compression (compact) will naturally summarize earlier phase documents. The strategy uses **双重保险**: TodoWrite 跟踪 active phase 保护其不被压缩，sentinel 作为兜底在压缩发生时触发恢复。

**Design principle**: TodoWrite `in_progress` = active phase → protect from compact | Sentinel = re-read fallback if protection fails.

**Double insurance mechanism**:

| Layer | Role | Mechanism |
|-------|------|-----------|
| **1. Active Phase Protection** | 预防 | TodoWrite `in_progress` 标记当前 phase → compact 时保留该 phase 完整内容，不压缩 |
| **2. Sentinel Re-read** | 恢复 | Phase 文件嵌入标识符 → 若仍被压缩，检测到 sentinel-only 状态时立即 re-read |

**When to apply**: 任何通过 direct handoff (Pattern 7) 跨 phase 执行的场景，尤其是后续 phase 包含复杂执行协议（多 Step、agent 调度、CLI 编排）时。

---

#### Layer 1: Active Phase Protection (TodoWrite 联动)

TodoWrite 已经跟踪每个 phase 的执行状态。利用此信息驱动 compact 策略：

```
TodoWrite status → Compact behavior:
  ┌─ completed  → ✅ 可压缩（已完成，不再需要完整内容）
  ├─ in_progress → 🛡️ 禁止压缩（正在执行，必须保留完整协议）
  └─ pending    → ✅ 可压缩（尚未加载，无内容）
```

**SKILL.md Execution Flow** 中标注 compact 联动:
```markdown
## Execution Flow

> **⚠️ COMPACT DIRECTIVE**: Context compression MUST check TodoWrite phase status.
> The phase currently marked `in_progress` is the active execution phase — preserve its FULL content.
> Only compress phases marked `completed` or `pending`.

Phase 1: Requirements Analysis    ← TodoWrite tracks status
   └─ Ref: phases/01-xxx.md
Phase 2: Execution Engine         ← TodoWrite tracks status
   └─ Ref: phases/02-xxx.md
...
```

**TodoWrite 状态转换** 时自动更新 compact 保护范围:
```
Phase 1: in_progress 🛡️  →  completed ✅   (compact 可压缩 Phase 1)
Phase 2: pending ✅       →  in_progress 🛡️ (compact 保护 Phase 2)
```

---

#### Layer 2: Sentinel Re-read (兜底恢复)

即使有 Layer 1 保护，compact 仍可能在极端场景（超长上下文、多轮 agent 调度）下压缩 active phase。Sentinel 确保恢复能力：

**Phase 文件顶部嵌入 sentinel**:
```markdown
> **📌 COMPACT SENTINEL [Phase N: {phase-name}]**
> This phase contains {M} execution steps (Step N.1 — N.{M}).
> If you can read this sentinel but cannot find the full Step protocol below, context has been compressed.
> Recovery: `Read("phases/0N-xxx.md")`
```

Sentinel 设计特点：
- 结构化、醒目 → compact 会将其作为关键信息保留在摘要中
- 包含 step 数量 → 提供自检依据（"应该看到 M 个 Step，但只有摘要"）
- 包含 re-read 路径 → 无需查表即可恢复

---

#### Phase Reference Table (整合双重保险)

```markdown
| Phase | Document | Purpose | Compact |
|-------|----------|---------|---------|
| 1 | phases/01-xxx.md | Planning | TodoWrite 驱动 |
| 2 | phases/02-xxx.md | Execution | TodoWrite 驱动 + 🔄 sentinel |

**Compact Rules**:
1. **TodoWrite `in_progress`** → 保留完整内容，禁止压缩
2. **TodoWrite `completed`** → 可压缩为摘要
3. **🔄 sentinel fallback** → 带此标记的 phase 包含 compact sentinel；若 compact 后仅存 sentinel 而无完整 Step 协议，**必须立即 `Read("phases/0N-xxx.md")` 恢复后再继续**
```

---

#### Checkpoint (执行步骤前双重验证)

```markdown
> **⚠️ CHECKPOINT**: Before proceeding, verify:
> 1. This phase is TodoWrite `in_progress` (active phase protection)
> 2. Full protocol (Step N.X — N.{M}) is in active memory, not just sentinel
> If only sentinel remains → `Read("phases/0N-xxx.md")` now.
```

#### Handoff 注释

```javascript
// Phase N is tracked by TodoWrite — active phase protection applies.
// Sentinel fallback: if compressed despite protection, re-read triggers automatically.
Read("phases/0N-xxx.md")
```

## Execution Flow

```
Phase 1: Requirements Analysis
   └─ Ref: phases/01-requirements-analysis.md
      ├─ Input source: commands, descriptions, user interaction
      └─ Output: workflowConfig (phases, data flow, agents, conditions)

Phase 2: Orchestrator Design (SKILL.md)
   └─ Ref: phases/02-orchestrator-design.md
      ├─ Input: workflowConfig
      └─ Output: .claude/skills/{name}/SKILL.md

Phase 3: Phase Files Design
   └─ Ref: phases/03-phase-design.md
      ├─ Input: workflowConfig + source content
      └─ Output: .claude/skills/{name}/phases/0N-*.md

Phase 4: Validation & Integration
   └─ Ref: phases/04-validation.md
      └─ Output: Validated skill package
```

**Phase Reference Documents** (read on-demand):

| Phase | Document | Purpose |
|-------|----------|---------|
| 1 | [phases/01-requirements-analysis.md](phases/01-requirements-analysis.md) | Analyze workflow requirements from various sources |
| 2 | [phases/02-orchestrator-design.md](phases/02-orchestrator-design.md) | Generate SKILL.md with orchestration patterns |
| 3 | [phases/03-phase-design.md](phases/03-phase-design.md) | Generate phase files preserving full execution detail |
| 4 | [phases/04-validation.md](phases/04-validation.md) | Validate structure, references, and integration |

## Input Sources

This meta-skill accepts workflow definitions from multiple sources:

| Source | Description | Example |
|--------|-------------|---------|
| **Existing commands** | Convert `.claude/commands/` orchestrator + sub-commands | `plan.md` + `session/start.md` + `tools/*.md` |
| **Text description** | User describes workflow in natural language | "Create a 3-phase code review workflow" |
| **Requirements doc** | Structured requirements file | `requirements.md` with phases/agents/outputs |
| **Existing skill** | Refactor/redesign an existing skill | Restructure a flat skill into phases |

## Frontmatter Conversion Rules

When converting from command format to skill format:

| Command Field | Skill Field | Transformation |
|---------------|-------------|----------------|
| `name` | `name` | Prefix with group: `plan` → `workflow-plan` |
| `description` | `description` | Append trigger phrase: `Triggers on "xxx"` |
| `argument-hint` | _(removed)_ | Arguments handled in Input Processing section |
| `examples` | _(removed)_ | Examples moved to inline documentation |
| `allowed-tools` | `allowed-tools` | Expand wildcards: `Skill(*)` → `Skill`, add commonly needed tools |
| `group` | _(removed)_ | Embedded in `name` prefix |

## Orchestrator Content Mapping

What goes into SKILL.md vs what goes into phase files:

### SKILL.md (Coordinator)

| Section | Content | Source |
|---------|---------|--------|
| Frontmatter | name, description, allowed-tools | Command frontmatter (converted) |
| Architecture Overview | ASCII diagram of phase flow | Derived from execution structure |
| Key Design Principles | Coordination rules | Extracted from command coordinator role |
| Execution Flow | Phase sequence with `Ref:` markers + Phase Reference table | Command execution process |
| Core Rules | Orchestration constraints | Command core rules |
| Input Processing | Structured format conversion | Command input processing |
| Data Flow | Inter-phase data passing | Command data flow |
| TodoWrite Pattern | Attachment/collapse lifecycle | Command TodoWrite sections |
| Post-Phase Updates | Planning notes / state updates between phases | Command inter-phase update code |
| Error Handling | Failure recovery | Command error handling |
| Coordinator Checklist | Pre/post phase actions | Command coordinator checklist |
| Related Commands | Prerequisites and follow-ups | Command related commands |

### Phase Files (Execution Detail)

| Content | Rule |
|---------|------|
| Full agent prompts | Preserve verbatim from source command |
| Bash command blocks | Preserve verbatim |
| Code implementations | Preserve verbatim |
| Validation checklists | Preserve verbatim |
| Error handling details | Preserve verbatim |
| Input/Output spec | Add if not present in source |
| Phase header | Add `# Phase N: {Name}` |
| Objective section | Add `## Objective` with bullet points |
| Next Phase link | Add `## Next Phase` with link to next |

**Critical Rule**: Phase files must be **content-faithful** to their source. Do NOT summarize, abbreviate, or simplify. The phase file IS the execution instruction - every bash command, every agent prompt, every validation step must be preserved.

## SKILL.md Template

```markdown
---
name: {skill-name}
description: {description}. Triggers on "{trigger1}", "{trigger2}".
allowed-tools: {tools}
---

# {Title}

{One-paragraph description of what this skill does and what it produces.}

## Architecture Overview

{ASCII diagram showing phases and data flow}

## Key Design Principles

1. **{Principle}**: {Description}
...

## Interactive Preference Collection

Collect workflow preferences via AskUserQuestion before dispatching to phases:
{AskUserQuestion code with preference derivation → workflowPreferences}

## Auto Mode Defaults

When `workflowPreferences.autoYes === true`: {auto-mode behavior}.

## Execution Flow

{Phase sequence with Ref: markers}

**Phase Reference Documents** (read on-demand when phase executes):

| Phase | Document | Purpose | Compact |
|-------|----------|---------|---------|
| 1 | [phases/01-xxx.md](phases/01-xxx.md) | ... | TodoWrite 驱动 |
| N | [phases/0N-xxx.md](phases/0N-xxx.md) | ... | TodoWrite 驱动 + 🔄 sentinel |
...

**Compact Rules**:
1. **TodoWrite `in_progress`** → 保留完整内容，禁止压缩
2. **TodoWrite `completed`** → 可压缩为摘要
3. **🔄 sentinel fallback** → 带此标记的 phase 包含 compact sentinel；若 compact 后仅存 sentinel 而无完整 Step 协议，必须立即 `Read()` 恢复

## Core Rules

1. {Rule}
...

## Input Processing

{How user input is converted to structured format}

## Data Flow

{Inter-phase data passing diagram}

## TodoWrite Pattern

{Attachment/collapse lifecycle description with examples}

## Post-Phase Updates

{State updates between phases}

## Error Handling

{Failure recovery rules}

## Coordinator Checklist

{Pre/post phase action list}

## Related Commands

{Prerequisites and follow-ups}
```

## Phase File Template

```markdown
# Phase N: {Phase Name}

> **📌 COMPACT SENTINEL [Phase N: {phase-name}]**
> This phase contains {M} execution steps (Step N.1 — N.{M}).
> If you can read this sentinel but cannot find the full Step protocol below, context has been compressed.
> Recovery: `Read("phases/0N-xxx.md")`
> _(Include for phases marked 🔄 in SKILL.md Phase Reference table — see Pattern 9)_

{One-sentence description of this phase's goal.}

## Objective

- {Goal 1}
- {Goal 2}

## Execution

### Step N.1: {Step Name}

{Full execution detail: commands, agent prompts, code}

### Step N.2: {Step Name}

> **⚠️ CHECKPOINT**: Before proceeding, verify:
> 1. This phase is TodoWrite `in_progress` (active phase protection)
> 2. Full protocol (Step N.X — N.{M}) is in active memory, not just sentinel
> If only sentinel remains → `Read("phases/0N-xxx.md")` now.
> _(Add checkpoints before critical execution steps: agent dispatch, CLI launch, review — see Pattern 9)_

{Full execution detail}

## Output

- **Variable**: `{variableName}` (e.g., `sessionId`)
- **File**: `{output file path}`
- **TodoWrite**: Mark Phase N completed, Phase N+1 in_progress

## Next Phase

Return to orchestrator, then auto-continue to [Phase N+1: xxx](0N+1-xxx.md).
```

## Design Decision Framework

When designing a new workflow skill, answer these questions:

| Question | Impact | Example |
|----------|--------|---------|
| How many phases? | Directory structure | 3-7 phases typical |
| Which phases are conditional? | Orchestrator logic | "Phase 3 only if conflict_risk >= medium" |
| What data flows between phases? | Data Flow section | sessionId, contextPath, configFlags |
| Which phases use agents? | Phase file complexity | Agent prompts need verbatim preservation |
| What's the TodoWrite granularity? | TodoWrite Pattern | Some phases have sub-tasks, others are atomic |
| Is there a planning notes pattern? | Post-Phase Updates | Accumulated state document across phases |
| What's the error recovery? | Error Handling | Retry once then report, vs rollback |
| Does it need preference collection? | Interactive Preference Collection | Collect via AskUserQuestion in SKILL.md, pass as workflowPreferences |
| Does phase N hand off to phase M? | Direct Phase Handoff (Pattern 7) | Read phase doc directly, not Skill() routing |
| Will later phases run after long context? | Compact Recovery (Pattern 9) | Add sentinel + checkpoints, mark 🔄 in Phase Reference table |
