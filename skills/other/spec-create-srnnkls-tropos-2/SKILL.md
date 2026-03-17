---
name: spec-create
description: Create spec documents (spec.md, context.md, tasks.yaml, dependencies.yaml, validation.yaml). Receives validation data from spec-validate.
---

# Spec Creation Skill

Creates structured tracking documents for complex development tasks.

---

## When to Use

**DO use for:**
- Complex multi-step tasks (3+ distinct phases)
- Non-trivial features requiring careful planning
- After ExitPlanMode when user accepts a plan
- Multi-phase implementation work

**DON'T use for:**
- Single-file changes
- Trivial refactorings
- Simple bug fixes
- Tasks completable in < 30 minutes

---

## Workflow

### Step 1: Check for Validation Data

**If invoked after spec-validate:**
- Issue type, taxonomy coverage, and clarification log are available
- Use this data to populate frontmatter and validation.yaml
- Proceed to Step 2

### Step 2: Determine Task Name

Derive from: git branch name, ExitPlanMode plan name, or user-provided argument.
Format: `kebab-case` (e.g., `add-temporal-joins`). If unclear, ask user.

### Step 3: Gather Context

Read relevant files to understand: task goal, key files, central types, architectural decisions, current vs target state.

### Step 3.5: Detect and Extract Code Artifacts

**If input contains code blocks** (```python, ```rust, etc.):

1. **Extract code blocks** with their language tags
2. **Create resources directory:**
   ```bash
   mkdir -p ./specs/draft/[task-name]/resources/
   ```
3. **Stage extracted content** (held in memory until user chooses):
   - Code blocks with language fences
   - Schema definitions (OpenAPI, JSON Schema, type definitions)
   - Config examples (YAML, TOML, env files)
   - Integration/test patterns

4. **Ask user which resources to create** (use AskUserQuestion with multiSelect):
   ```
   Header: Resources
   Question: Which implementation artifacts should be preserved?
   multiSelect: true
   Options:
   - implementation: Code sketches/examples - patterns to follow (loqui-validated)
   - schemas: API contracts, data models, type definitions
   - config: Configuration examples
   - patterns: Integration and test patterns
   - assets: Diagrams, screenshots, other media
   - none: Skip resources, spec only
   ```

5. **Create selected resources:**
   - Only create directories for selected options
   - Run loqui validation on code (if selected and language has guidelines)
   - Report violations in validation.yaml under `loqui_check` section

6. **Continue with spec generation** using extracted requirements (not code details)

**Resources directory structure** (all subdirectories optional):
```
specs/draft/{spec-name}/
├── spec.md
├── context.md
├── tasks.yaml
├── ...
└── resources/           # Only if user selected any
    ├── implementation.md   # If "implementation" selected
    ├── schemas/         # If "schemas" selected
    ├── config/          # If "config" selected
    ├── patterns/        # If "patterns" selected
    └── assets/          # If "assets" selected
```

### Step 3.6: Configure Implementation Reviewers

**Only for Initiative/Feature** (skip for Task):

**Question 1:** Select reviewers:
```
Header: Reviewers
Question: Which reviewers should analyze implementation batches?
multiSelect: true
Options:
- claude-opus: Claude Opus - native reviewer, comprehensive (Recommended)
- claude-sonnet: Claude Sonnet - faster native review
- openai-gpt5.2: OpenAI GPT-5.2 - base model
- openai-gpt5.2-codex: OpenAI GPT-5.2 Codex - code-specialized
- openai-gpt5.2-pro: OpenAI GPT-5.2 Pro - extended capabilities (Recommended)
- gemini-3-flash: Google Gemini 3 Flash - fast, efficient
- gemini-3-pro: Google Gemini 3 Pro - advanced reasoning (Recommended)
```

**Default selection:** claude-opus, openai-gpt5.2-pro, gemini-3-pro

**Question 2:** Select reasoning effort (if OpenCode reviewers selected):
```
Header: Reasoning
Question: What reasoning effort level for OpenCode reviewers?
multiSelect: false
Options:
- low: Quick responses, minimal deliberation
- medium: Balanced reasoning (Recommended)
- high: Deep analysis, thorough deliberation
- xhigh: Maximum reasoning (GPT-5.2 only)
```

**Default:** medium

Store in `validation.yaml` under `review_config`:
```yaml
review_config:
  reasoning_effort: medium  # low | medium | high | xhigh
  reviewers:
    - type: claude
      model: opus  # or sonnet
    - type: opencode
      model: openai/gpt-5.2
    - type: opencode
      model: google/gemini-3-pro-preview
```

**Variant format:** `{reasoning_effort}-medium` (verbosity fixed at medium)

**Model mapping:**
- `claude-opus` → `{type: claude, model: opus}`
- `claude-sonnet` → `{type: claude, model: sonnet}`
- `openai-gpt5.2` → `{type: opencode, model: openai/gpt-5.2}`
- `openai-gpt5.2-codex` → `{type: opencode, model: openai/gpt-5.2-codex}`
- `openai-gpt5.2-pro` → `{type: opencode, model: openai/gpt-5.2}`
- `gemini-3-flash` → `{type: opencode, model: google/gemini-3-flash-preview}`
- `gemini-3-pro` → `{type: opencode, model: google/gemini-3-pro-preview}`

### Step 4: Create Directory and Documents

```bash
mkdir -p ./specs/draft/[task-name]/
```

Generate these files:

1. **`spec.md`** - Strategic spec (review this)
2. **`context.md`** - Implementation context (update as you work)
3. **`tasks.yaml`** - Work checklist (dignity CLI, TodoWrite sync)
4. **`dependencies.yaml`** - Task dependency graph (parallel dispatch)
5. **`validation.yaml`** - Audit trail and gate checks

**Document scaling by issue type:**

| Document | Initiative | Feature | Task |
|----------|-----------|---------|------|
| spec.md | Full strategic | Standard | Lightweight |
| context.md | High-level | Standard | Skip |
| tasks.yaml | Feature breakdown + phases | Task breakdown | Single task |
| dependencies.yaml | Full DAG | Phase-based | Skip |
| validation.yaml | Full (7 areas + gates) | Full (7 areas) | Skip |

**Task output = 2 files:** spec.md (lightweight) + tasks.yaml

**Frontmatter for spec.md:**

```yaml
---
issue_type: [Initiative|Feature|Task]
created: [Date]
status: Draft
stage: draft
claude_plan: [path to native Claude plan file, if exists]
---
```

If a native Claude plan exists (from EnterPlanMode/ExitPlanMode), include its path in the `claude_plan` field. This links the detailed spec to its originating design document.

### Conditional Sections

Based on validation data and issue type, include optional sections:

**spec.md:**

| Section | Initiative | Feature | Task |
|---------|------------|---------|------|
| User Stories (P1/P2/P3) | Include | Skip | Skip |
| Given/When/Then Acceptance | Full | Standard | Simple |
| API Contract | Include if API work | Opt-in | Skip |
| Implementation Strategy | Include | Skip | Skip |

**context.md:**

| Section | Initiative | Feature | Task |
|---------|------------|---------|------|
| Tech Decisions | Include | Opt-in | (file skipped) |
| Data Model | Include | Opt-in | (file skipped) |

**validation.yaml:**

| Section | Initiative | Feature | Task |
|---------|------------|---------|------|
| Gates | Evaluate all | n/a | (file skipped) |
| Complexity Tracking | If violations | If violations | (file skipped) |
| Markers | Full | Full | (file skipped) |
| Review Config | Full | Full | (file skipped) |

**tasks.yaml:**

| Element | Initiative | Feature | Task |
|---------|------------|---------|------|
| Phases with checkpoints | Full (gates between phases) | Simple (optional checkpoints) | Skip |
| Evidence tracking | Full | Opt-in | Skip |
| Dependencies | Full | Opt-in | Skip |

**tasks.yaml structure:**

```yaml
spec: ${SPEC_NAME}
code: ${CODE}           # Prefix for task IDs (e.g., FEAT → FEAT-001)
next_id: 1
tasks:
  - id: ${CODE}-001
    content: Task description
    status: pending     # pending | in_progress | completed
    active_form: Doing task description
meta:
  created: ${DATE}
  last_updated: ${DATE}
  progress: 0/N
phases:                 # Optional: organize tasks with checkpoints
  - name: "Phase 1: Setup"
    task_ids: [${CODE}-001, ${CODE}-002]
    checkpoint:
      description: Setup complete
      criteria: [...]
      verified: false
```

Used by dignity for task management operations. The `code` field generates sequential IDs (e.g., AUT-001, AUT-002).

### Step 5: Populate TodoWrite from tasks.yaml

Parse the just-created `tasks.yaml` and populate TodoWrite:

1. Read tasks from `tasks.yaml`
2. Create TodoWrite with up to 10 tasks:
   - status: map from tasks.yaml status
   - content: task content field
   - activeForm: task active_form field

**Example:**
```yaml
# tasks.yaml:
tasks:
  - id: IMPL-001
    content: Create implement.md command
    status: pending
    active_form: Creating implement.md command
  - id: IMPL-002
    content: Create docs-implement SKILL.md
    status: pending
    active_form: Creating docs-implement SKILL.md
```

```json
// TodoWrite:
[
  {"content": "Create implement.md command", "status": "pending", "activeForm": "Creating implement.md command"},
  {"content": "Create docs-implement SKILL.md", "status": "pending", "activeForm": "Creating docs-implement SKILL.md"}
]
```

### Step 6: Present Summary

Show user:
- Directory created: `./specs/draft/[task-name]/`
- Human-facing docs: spec.md, context.md (brief overview of each)
- Tooling artifacts: tasks.yaml, dependencies.yaml, validation.yaml (note these are for automation)
- Validation coverage (if from spec-validate)
- Next action: "Run `/spec.review` or `/spec.promote` when ready to activate"

### Step 7: Offer Comprehensive Review (Optional)

After presenting summary, offer spec review:

Use AskUserQuestion:
```
Header: Review
Question: Would you like a comprehensive spec review before implementation?
multiSelect: false
Options:
- Yes: Run multi-agent review (Claude + OpenCode)
- Later: Skip for now, use /spec.review when ready
- Skip: Proceed without review
```

If "Yes": Invoke `spec-review` skill with the just-created spec name.

---

## Output Artifacts

**For humans (review these):**
```
├── spec.md      # WHY & WHAT - Strategic requirements, acceptance criteria
├── context.md   # WHAT WE LEARNED - Key files, decisions, gotchas
└── resources/   # HOW TO BUILD - Implementation details (when provided)
```

**For tooling (infrastructure):**
```
├── tasks.yaml        # Progress tracking, TodoWrite sync
├── dependencies.yaml # Parallel dispatch DAG
└── validation.yaml   # Audit trail, gate checks, reviewer config, loqui validation
```

The YAML files are infrastructure - humans *can* read them for debugging or auditing, but the primary consumers are tooling and automation.

**validation.yaml usage:**
- `review_config.reviewers` - Used by task-dispatch for batch reviews
- `gates` - Pre-implementation gate checks for Initiatives
- `markers` - Unresolved items requiring clarification

### The resources/ Directory

Only created when implementation details are provided in input. Contains structured artifacts:

| Subdirectory | Content |
|-------------|---------|
| `implementation.md` | Code sketches and examples - patterns to follow, not tested/final (loqui-validated) |
| `schemas/` | API contracts, data models, type definitions |
| `config/` | Configuration examples |
| `patterns/` | Integration and test patterns |
| `assets/` | Diagrams, screenshots, other media |

**Review burden:** 2-3 documents (spec.md, context.md, resources/ when present), not 8+.

See [guidelines.md](guidelines.md) for detailed breakdown.

### Native Plan Integration

If a native Claude plan exists (from EnterPlanMode), add a **Native Plan** section to `context.md`:

```markdown
## Native Plan

**Source:** `/path/to/.claude/specs/spec-name.md`

Summary of the original design:
- Goal: [brief goal from native plan]
- Approach: [key approach decisions]
- Open questions resolved: [any clarifications made]
```

This preserves the connection to the original design discussion and rationale.

---

## Templates

Located in `templates/` directory:
- [validation.yaml](templates/validation.yaml)
- [dependencies.yaml](templates/dependencies.yaml)
- [tasks.yaml](templates/tasks.yaml)
- [spec.md](templates/spec.md)
- [context.md](templates/context.md)

---

## Integration

**Invoked by:** `/spec.create` command
- Runs `spec-validate` first, then this skill

**Related commands:**
- `/spec.review` - Review spec with multiple AI reviewers
- `/spec.update` - Sync spec with git history
- `/spec.archive` - Archive completed spec
- `/spec.issues` - Generate GitHub issues from spec
