---
name: prompt-generator
description: Generate or convert Claude Code prompt files — command orchestrators, skill files, agent role definitions, or style conversion of existing files. Follows GSD-style content separation with built-in quality gates. Triggers on "create command", "new command", "create skill", "new skill", "create agent", "new agent", "convert command", "convert skill", "convert agent", "prompt generator", "优化".
allowed-tools: Read, Write, Edit, Bash, Glob, AskUserQuestion
---

<purpose>
Generate or convert Claude Code prompt files with concrete, domain-specific content. Four modes:

- **Create command** — new orchestration workflow at `.claude/commands/` or `~/.claude/commands/`
- **Create skill** — new skill file at `.claude/skills/*/SKILL.md` (progressive loading, no @ refs)
- **Create agent** — new role + expertise file at `.claude/agents/`
- **Convert** — restyle existing command/skill/agent to GSD conventions with zero content loss

Content separation principle (from GSD): commands/skills own orchestration flow; agents own domain knowledge. Skills are a variant of commands but loaded progressively inline — they CANNOT use `@` file references.

Invoked when user requests "create command", "new command", "create skill", "new skill", "create agent", "new agent", "convert command", "convert skill", "convert agent", "prompt generator", or "优化".
</purpose>

<required_reading>
- @.claude/skills/prompt-generator/specs/command-design-spec.md
- @.claude/skills/prompt-generator/specs/agent-design-spec.md
- @.claude/skills/prompt-generator/specs/conversion-spec.md
- @.claude/skills/prompt-generator/templates/command-md.md
- @.claude/skills/prompt-generator/templates/agent-md.md
</required_reading>

<process>

## 1. Determine Artifact Type

Parse `$ARGUMENTS` to determine what to generate.

| Signal | Type |
|--------|------|
| "command", "workflow", "orchestrator" in args | `command` |
| "skill", "SKILL.md" in args, or path contains `.claude/skills/` | `skill` |
| "agent", "role", "worker" in args | `agent` |
| "convert", "restyle", "refactor", "optimize", "优化" + file path in args | `convert` |
| Ambiguous or missing | Ask user |

**Convert mode detection:** If args contain a file path (`.md` extension) + conversion keywords, enter convert mode. Extract `$SOURCE_PATH` from args. Auto-detect source type from path:
- `.claude/commands/` → command
- `.claude/skills/*/SKILL.md` → skill
- `.claude/agents/` → agent

**Skill vs Command distinction:** Skills (`.claude/skills/*/SKILL.md`) are loaded **progressively inline** into the conversation context. They CANNOT use `@` file references — only `Read()` tool calls within process steps. See `@specs/command-design-spec.md` → "Skill Variant" section.

If ambiguous:

```
AskUserQuestion(
  header: "Artifact Type",
  question: "What type of prompt file do you want to generate?",
  options: [
    { label: "Command", description: "New orchestration workflow — process steps, user interaction, agent spawning" },
    { label: "Skill", description: "New skill file — progressive loading, no @ refs, inline Read() for external files" },
    { label: "Agent", description: "New role definition — identity, domain expertise, behavioral rules" },
    { label: "Convert", description: "Restyle existing command/agent/skill to GSD conventions (zero content loss)" }
  ]
)
```

Store as `$ARTIFACT_TYPE` (`command` | `skill` | `agent` | `convert`).

## 2. Validate Parameters

**If `$ARTIFACT_TYPE` is `convert`:** Skip to Step 2c.

Extract from `$ARGUMENTS` or ask interactively:

**Common parameters (create mode):**

| Parameter | Required | Validation | Example |
|-----------|----------|------------|---------|
| `$NAME` | Yes | `/^[a-z][a-z0-9-]*$/` | `deploy`, `gsd-planner` |
| `$DESCRIPTION` | Yes | min 10 chars | `"Deploy to production with rollback"` |

**Command-specific parameters:**

| Parameter | Required | Validation | Example |
|-----------|----------|------------|---------|
| `$LOCATION` | Yes | `"project"` or `"user"` | `project` |
| `$GROUP` | No | `/^[a-z][a-z0-9-]*$/` | `issue`, `workflow` |
| `$ARGUMENT_HINT` | No | any string | `"<phase> [--skip-verify]"` |

**Agent-specific parameters:**

| Parameter | Required | Validation | Example |
|-----------|----------|------------|---------|
| `$TOOLS` | No | comma-separated tool names | `Read, Write, Bash, Glob` |
| `$SPAWNED_BY` | No | which command spawns this agent | `/plan-phase orchestrator` |

Normalize: trim + lowercase for `$NAME`, `$LOCATION`, `$GROUP`.

## 3. Resolve Target Path

**Command:**

| Location | Base |
|----------|------|
| `project` | `.claude/commands` |
| `user` | `~/.claude/commands` |

```
If $GROUP:
  $TARGET_PATH = {base}/{$GROUP}/{$NAME}.md
Else:
  $TARGET_PATH = {base}/{$NAME}.md
```

**Skill:**

```
$TARGET_PATH = .claude/skills/{$NAME}/SKILL.md
```

**Agent:**

```
$TARGET_PATH = .claude/agents/{$NAME}.md
```

Check if `$TARGET_PATH` exists → `$FILE_EXISTS`.

## 4. Gather Requirements

**4a. Pattern discovery** — Find 3+ similar files in the project for style reference:

```bash
# For commands: scan existing commands
ls .claude/commands/**/*.md 2>/dev/null | head -5

# For agents: scan existing agents
ls .claude/agents/*.md 2>/dev/null | head -5
```

Read 1-2 similar files to extract patterns: section structure, naming conventions, XML tag usage, prompt style.

**4b. Domain inference** from `$NAME`, `$DESCRIPTION`, and context:

| Signal | Extract |
|--------|---------|
| `$NAME` | Action verb → step/section naming |
| `$DESCRIPTION` | Domain keywords → content structure |
| `$ARGUMENT_HINT` | Flags → parse_input logic (command only) |
| `$SPAWNED_BY` | Upstream contract → role boundary (agent only) |

**For commands — determine complexity:**

| Complexity | Criteria | Steps |
|------------|----------|-------|
| Simple | Single action, no flags | 3-5 numbered steps |
| Standard | 1-2 flags, clear workflow | 5-8 numbered steps |
| Complex | Multiple flags, agent spawning | 8-14 numbered steps |

**For agents — determine expertise scope:**

| Scope | Criteria | Sections |
|-------|----------|----------|
| Focused | Single responsibility | `<role>` + 1-2 domain sections |
| Standard | Multi-aspect domain | `<role>` + 2-4 domain sections |
| Expert | Deep domain with rules | `<role>` + 4-6 domain sections |

If unclear, ask user with AskUserQuestion.

## 5. Generate Content

Route to the appropriate generation logic based on `$ARTIFACT_TYPE`.

### 5a. Command Generation

Follow `@specs/command-design-spec.md` and `@templates/command-md.md`.

Generate a complete command file with:

1. **`<purpose>`** — 2-3 sentences: what + when + what it produces
2. **`<required_reading>`** — @ references to context files
3. **`<process>`** — numbered steps (GSD workflow style):
   - Step 1: Initialize / parse arguments
   - Steps 2-N: Domain-specific orchestration logic
   - Each step: banner display, validation, agent spawning via `Agent()`, error handling
   - Final step: status display + `<offer_next>` with next actions
4. **`<success_criteria>`** — checkbox list of verifiable conditions

**Command writing rules:**
- Steps are **numbered** (`## 1.`, `## 2.`) — follow `plan-phase.md` and `new-project.md` style
- Use banners for phase transitions: `━━━ SKILL ► ACTION ━━━`
- Agent spawning uses `Agent({ subagent_type, prompt, description, run_in_background })` pattern
- Prompt to agents uses `<objective>`, `<files_to_read>`, `<output>` blocks
- Include `<offer_next>` block with formatted completion status
- Handle agent return markers: `## TASK COMPLETE`, `## TASK BLOCKED`, `## CHECKPOINT REACHED`
- Shell blocks use heredoc for multi-line, quote all variables
- Include `<auto_mode>` section if command supports `--auto` flag

### 5a-skill. Skill Generation (variant of command)

Follow `@specs/command-design-spec.md` → "Skill Variant" section.

Skills are command-like orchestrators but loaded **progressively inline** — they CANNOT use `@` file references.

Generate a complete skill file with:

1. **`<purpose>`** — 2-3 sentences: what + when + what it produces
2. **NO `<required_reading>`** — skills cannot use `@` refs. External files loaded via `Read()` within process steps.
3. **`<process>`** — numbered steps (GSD workflow style):
   - Step 1: Initialize / parse arguments / set workflow preferences
   - Steps 2-N: Domain-specific orchestration logic with inline `Read("phases/...")` for phase files
   - Each step: validation, agent spawning via `Agent()`, error handling
   - Final step: completion status or handoff to next skill via `Skill()`
4. **`<success_criteria>`** — checkbox list of verifiable conditions

**Skill-specific writing rules:**
- **NO `<required_reading>` tag** — `@` syntax not supported in skills
- **NO `@path` references** anywhere in the file — use `Read("path")` within `<process>` steps
- Phase files loaded on-demand: `Read("phases/01-xxx.md")` within the step that needs it
- Frontmatter uses `allowed-tools:` (not `argument-hint:`)
- `<offer_next>` is optional — skills often chain via `Skill()` calls
- `<auto_mode>` can be inline within `<process>` step 1 or as standalone section

### 5b. Agent Generation

Follow `@specs/agent-design-spec.md` and `@templates/agent-md.md`.

Generate a complete agent definition with:

1. **YAML frontmatter** — name, description, tools, color (optional)
2. **`<role>`** — identity + spawned-by + core responsibilities + mandatory initial read
3. **Domain sections** (2-6 based on scope):
   - `<philosophy>` — guiding principles, anti-patterns
   - `<context_fidelity>` — how to honor upstream decisions
   - `<task_breakdown>` / `<output_format>` — concrete output rules with examples
   - `<quality_gate>` — self-check criteria before returning
   - Custom domain sections as needed
4. **Output contract** — structured return markers to orchestrator

**Agent writing rules:**
- `<role>` is ALWAYS first after frontmatter — defines identity
- Each section owns ONE concern — no cross-cutting
- Include concrete examples (good vs bad comparison tables) in every domain section
- Include decision/routing tables for conditional logic
- Quality gate uses checkbox format for self-verification
- Agent does NOT contain orchestration logic, user interaction, or argument parsing

### 5c. Convert Mode (Restyle Existing File)

**CRITICAL: Zero content loss.** Follow `@specs/conversion-spec.md`.

**Step 5c.1: Read and inventory source file.**

Read `$SOURCE_PATH` completely. Build content inventory:

```
$INVENTORY = {
  frontmatter: { fields extracted },
  sections: [ { name, tag, line_range, line_count, has_code_blocks, has_tables } ],
  code_blocks: count,
  tables: count,
  total_lines: count
}
```

**Step 5c.2: Classify source type.**

| Signal | Type |
|--------|------|
| Path in `.claude/skills/*/SKILL.md` | skill |
| `allowed-tools:` in frontmatter + path in `.claude/skills/` | skill |
| Contains `<process>`, `<step>`, numbered `## N.` steps | command |
| Contains `<role>`, `tools:` in frontmatter, domain sections | agent |
| Flat markdown with `## Implementation`, `## Phase N` + in skills dir | skill (unstructured) |
| Flat markdown with `## Implementation`, `## Phase N` + in commands dir | command (unstructured) |
| Flat prose with role description, no process steps | agent (unstructured) |

**Skill-specific conversion rules:**
- **NO `<required_reading>`** — skills cannot use `@` file references (progressive loading)
- **NO `@path` references** anywhere — replace with `Read("path")` within `<process>` steps
- If source has `@specs/...` or `@phases/...` refs, convert to `Read("specs/...")` / `Read("phases/...")`
- Follow `@specs/conversion-spec.md` → "Skill Conversion Rules" section

**Step 5c.3: Build conversion map.**

Map every source section to its target location. Follow `@specs/conversion-spec.md` transformation rules.

**MANDATORY**: Every line of source content must appear in the conversion map. If a source section has no clear target, keep it as a custom section.

**Step 5c.4: Generate converted content.**

Apply structural transformations while preserving ALL content verbatim:
- Rewrap into GSD XML tags
- Restructure sections to match target template ordering
- Add missing required sections (empty `<quality_gate>`, `<output_contract>`) with `TODO` markers
- Preserve all code blocks, tables, examples, shell commands exactly as-is

**Step 5c.5: Content loss verification (MANDATORY).**

Compare source and output:

| Metric | Source | Output | Pass? |
|--------|--------|--------|-------|
| Total lines | `$SRC_LINES` | `$OUT_LINES` | output >= source × 0.95 |
| Code blocks | `$SRC_BLOCKS` | `$OUT_BLOCKS` | output >= source |
| Tables | `$SRC_TABLES` | `$OUT_TABLES` | output >= source |
| Sections | `$SRC_SECTIONS` | `$OUT_SECTIONS` | output >= source |

If ANY metric fails → STOP, display diff, ask user before proceeding.

Set `$TARGET_PATH = $SOURCE_PATH` (in-place conversion) unless user specifies output path.

### Content quality rules (both types):
- NO bracket placeholders (`[Describe...]`) — all content concrete
- NO generic instructions ("handle errors appropriately") — be specific
- Include domain-specific examples derived from `$DESCRIPTION`
- Every shell block: heredoc for multi-line, quoted variables, error exits

## 6. Quality Gate

**MANDATORY before writing.** Read back the generated content and validate against type-specific checks.

### 6a. Structural Validation (both types)

| Check | Pass Condition |
|-------|---------------|
| YAML frontmatter | Has `name` + `description` |
| No placeholders | Zero `[...]` or `{...}` bracket placeholders in prose |
| Concrete content | Every section has actionable content, not descriptions of what to write |
| Section count | Command: 3+ sections; Agent: 4+ sections |

### 6b. Command-Specific Checks

| Check | Pass Condition |
|-------|---------------|
| `<purpose>` | 2-3 sentences, no placeholders |
| `<process>` with numbered steps | At least 3 `## N.` headers |
| Step 1 is initialization | Parses args or loads context |
| Last step is status/report | Displays results or routes to `<offer_next>` |
| Agent spawning (if complex) | `Agent({` call with `subagent_type` |
| Agent prompt structure | `<files_to_read>` + `<objective>` or `<output>` blocks |
| Return handling | Routes on `## TASK COMPLETE` / `## TASK BLOCKED` markers |
| `<offer_next>` | Banner + summary + next command suggestion |
| `<success_criteria>` | 4+ checkbox items, all verifiable |
| Content separation | No domain expertise embedded — only orchestration |

### 6b-skill. Skill-Specific Checks

| Check | Pass Condition |
|-------|---------------|
| `<purpose>` | 2-3 sentences, no placeholders |
| **NO `<required_reading>`** | Must NOT contain `<required_reading>` tag |
| **NO `@` file references** | Zero `@specs/`, `@phases/`, `@./` patterns in prose |
| `<process>` with numbered steps | At least 3 `## N.` headers |
| Step 1 is initialization | Parses args, sets workflow preferences |
| Phase file loading | Uses `Read("phases/...")` within process steps (if has phases) |
| `<success_criteria>` | 4+ checkbox items, all verifiable |
| Frontmatter `allowed-tools` | Present and lists required tools |
| Content separation | No domain expertise embedded — only orchestration |

### 6c. Agent-Specific Checks

| Check | Pass Condition |
|-------|---------------|
| YAML `tools` field | Lists tools agent needs |
| `<role>` is first section | Appears before any domain section |
| `<role>` has spawned-by | States which command spawns it |
| `<role>` has mandatory read | `<files_to_read>` instruction present |
| `<role>` has responsibilities | 3+ bullet points with verb phrases |
| Domain sections named | After domain concepts, not generic (`<rules>`, `<guidelines>`) |
| Examples present | Each domain section has 1+ comparison table or decision table |
| `<output_contract>` | Defines return markers (COMPLETE/BLOCKED/CHECKPOINT) |
| `<quality_gate>` | 3+ checkbox self-check items |
| Content separation | No `AskUserQuestion`, no banner display, no argument parsing |

### 6d. Quality Gate Result

Count errors and warnings:

| Gate | Condition | Action |
|------|-----------|--------|
| **PASS** | 0 errors, 0-2 warnings | Proceed to write |
| **REVIEW** | 1-2 errors or 3+ warnings | Fix errors, display warnings |
| **FAIL** | 3+ errors | Re-generate from step 5 |

If FAIL and second attempt also fails:

```
AskUserQuestion(
  header: "Quality Gate Failed",
  question: "Generated content failed quality checks twice. How to proceed?",
  options: [
    { label: "Show issues and proceed", description: "Write as-is, fix manually" },
    { label: "Provide more context", description: "I'll give additional details" },
    { label: "Abort", description: "Cancel generation" }
  ]
)
```

## 7. Write and Verify

**If `$FILE_EXISTS`:** Warn user before overwriting.

```bash
mkdir -p "$(dirname "$TARGET_PATH")"
```

Write content to `$TARGET_PATH` using Write tool.

**Post-write verification** — Read back and confirm file integrity:
- File exists and is non-empty
- Content matches what was generated (no corruption)
- File size is reasonable (command: 50-500 lines; agent: 80-600 lines)

**If verification fails:** Fix in-place with Edit tool.

## 8. Present Status

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 PROMPT-GEN ► {COMMAND|AGENT} GENERATED
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Type: {command | agent}
File: {$TARGET_PATH}
Name: {$NAME}

| Section | Status |
|---------|--------|
| {section 1} | concrete |
| {section 2} | concrete |
| ... | ... |

Quality Gate: {PASS | REVIEW (N warnings)}

───────────────────────────────────────────────────────

## Next Up

1. Review: cat {$TARGET_PATH}
2. Test: /{invocation}

**If command + needs an agent:**
  /prompt-generator agent {agent-name} "{agent description}"

**If agent + needs a command:**
  /prompt-generator command {command-name} "{command description}"

───────────────────────────────────────────────────────
```

</process>

<success_criteria>
- [ ] Artifact type determined (command or agent)
- [ ] All required parameters validated
- [ ] Target path resolved correctly
- [ ] 1-2 similar existing files read for pattern reference
- [ ] Domain requirements gathered from description
- [ ] Content generated with concrete, domain-specific logic
- [ ] GSD content separation respected (commands = orchestration, agents = expertise)
- [ ] Quality gate passed (structural + type-specific checks)
- [ ] No bracket placeholders in final output
- [ ] File written and post-write verified
- [ ] Status banner displayed with quality gate result
</success_criteria>
