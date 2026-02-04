---
name: framework
description: Expert on SpecWeave framework structure, rules, and spec-driven development conventions. Use when learning SpecWeave best practices, understanding increment lifecycle, or configuring hooks. Covers source-of-truth discipline, tasks.md/spec.md formats, living docs sync, and file organization patterns.
allowed-tools: Read, Grep, Glob
user-invocable: false
---

# SpecWeave Framework Expert

I am an expert on the SpecWeave framework - a spec-driven development framework for Claude Code (and other AI coding assistants). I have deep knowledge of its structure, rules, conventions, and best practices.

## Core Philosophy

SpecWeave follows **spec-driven development** with **increment-based workflows**:

1. **Specification First** - Write WHAT and WHY before HOW
2. **Incremental Delivery** - Ship small, complete features
3. **Living Documentation** - Docs update automatically via hooks
4. **Source of Truth Discipline** - Single source, zero duplication
5. **Multi-Tool Support** - Works with Claude, Cursor, Copilot, and generic AI

## Increment-Based Development

### What is an Increment?

An **increment** = a complete feature with:
- `spec.md` - Product requirements (WHAT and WHY) — **required**
- `plan.md` - Technical architecture (HOW to implement) — **optional**, for complex features only
- `tasks.md` - Task breakdown (WORK to do) — **required**
- `metadata.json` - State tracking — **required**

> **When to skip plan.md**: Bug fixes, simple migrations, hotfixes, and straightforward tasks where spec.md already describes the approach.

### spec.md Mandatory Fields

**CRITICAL**: spec.md YAML frontmatter MUST include project (and board for 2-level structures):

```yaml
# 1-level structure (single-project or multiProject):
---
increment: 0001-feature-name
project: my-project          # REQUIRED
---

# 2-level structure (ADO area paths, JIRA boards, umbrella teams):
---
increment: 0001-feature-name
project: acme-corp           # REQUIRED
board: digital-operations    # REQUIRED for 2-level
---
```

**Why?** Ensures increment syncs to correct location in living docs. Without explicit project/board, sync-specs may fail or place specs in wrong folder.

**Detection**: Use `src/utils/structure-level-detector.ts` to determine if 1-level or 2-level structure is needed.

**See**: [ADR-0190](/internal/architecture/adr/0190-spec-project-board-requirement.md)

### Increment Naming Convention

**CRITICAL RULE**: All increments MUST use descriptive names, not just numbers!

**Format**: `####-descriptive-kebab-case-name`

**Examples**:
- ✅ `0001-core-framework`
- ✅ `0002-core-enhancements`
- ✅ `0003-intelligent-model-selection`
- ✅ `0004-plugin-architecture`
- ✅ `0006-llm-native-i18n`
- ❌ `0003` (too generic, rejected!)
- ❌ `0004` (no description, rejected!)

**Rationale**:
- Clear intent at a glance
- Easy to reference in conversation
- Better git history
- Searchable by feature name
- Self-documenting increment folders

### Increment Lifecycle

```
1. Plan    → /sw:inc "feature-name"
            ↓ PM agent creates spec.md, plan.md, tasks.md, tests.md

2. Execute → /sw:do
            ↓ Selects next task, executes, marks complete

3. Validate → /sw:validate 0001
            ↓ Checks spec compliance, test coverage

4. Close   → /sw:done 0001
            ↓ Creates COMPLETION-SUMMARY.md, archives
```

### Increment Discipline

**THE IRON RULE**: Cannot start increment N+1 until increment N is DONE!

**Enforcement**:
- `/sw:inc` **blocks** if previous increments incomplete
- Use `/sw:status` to check all increments
- Use `/sw:close` to close incomplete work
- `--force` flag for emergencies (logged, should be rare)

**What "DONE" Means**:
1. All tasks in `tasks.md` marked `[x] Completed`, OR
2. `COMPLETION-SUMMARY.md` exists with "✅ COMPLETE" status, OR
3. Explicit closure via `/sw:close`

**Three Options for Closing**:
1. **Adjust Scope** - Remove features from spec.md, regenerate tasks
2. **Move Scope** - Transfer incomplete tasks to next increment
3. **Extend Existing** - Update spec.md, add tasks, continue in same increment

**Example**:
```bash
# Check status
/sw:status
# Shows: 0002 (73% complete), 0003 (50% complete)

# Try to start new increment
/sw:inc "0004-new-feature"
# ❌ Blocked! "Close 0002 and 0003 first"

# Close previous work
/sw:close
# Interactive: Choose force-complete, move tasks, or reduce scope

# Now can proceed
/sw:inc "0004-new-feature"
# ✅ Works! Clean slate
```

## Directory Structure

### Root-Level .specweave/ Folder (MANDATORY)

**CRITICAL ARCHITECTURE RULE**: SpecWeave ONLY supports root-level `.specweave/` folders.

**Correct Structure**:
```
my-project/
├── .specweave/              ← ONE source of truth (root-level)
│   ├── increments/
│   │   ├── 0001-core-framework/
│   │   │   ├── spec.md
│   │   │   ├── plan.md
│   │   │   ├── tasks.md
│   │   │   ├── tests.md
│   │   │   ├── logs/        ← Session logs
│   │   │   ├── scripts/     ← Helper scripts
│   │   │   └── reports/     ← Analysis files
│   │   └── _backlog/
│   ├── docs/
│   │   ├── internal/        ← Strategic docs (NEVER published)
│   │   │   ├── strategy/    ← Business strategy
│   │   │   ├── architecture/ ← ADRs, RFCs, diagrams
│   │   │   └── delivery/    ← Implementation notes
│   │   └── public/          ← User-facing docs (can publish)
│   └── logs/
├── frontend/
├── backend/
└── infrastructure/
```

**WRONG** (nested .specweave/ folders - NOT SUPPORTED):
```
my-project/
├── .specweave/              ← Root level
├── backend/
│   └── .specweave/          ← ❌ NESTED - PREVENTS THIS!
└── frontend/
    └── .specweave/          ← ❌ NESTED - PREVENTS THIS!
```

**Why Root-Level Only?**
- ✅ Single source of truth
- ✅ Cross-cutting features natural (frontend + backend + infra)
- ✅ No duplication or fragmentation
- ✅ Clear ownership
- ✅ Simplified living docs sync

**Multi-Repo Solution**:
For huge projects with multiple repos, create a **parent folder**:
```
my-big-project/              ← Create parent folder
├── .specweave/              ← ONE source of truth for ALL repos
├── auth-service/            ← Separate git repo
├── payment-service/         ← Separate git repo
├── frontend/                ← Separate git repo
└── infrastructure/          ← Separate git repo
```

## Source of Truth Discipline

**CRITICAL PRINCIPLE**: SpecWeave has strict source-of-truth rules!

### Three Directories, Three Purposes

```
src/                         ← SOURCE OF TRUTH (version controlled)
├── skills/                  ← Source for skills
├── agents/                  ← Source for agents
├── commands/                ← Source for slash commands
├── hooks/                   ← Source for hooks
├── adapters/                ← Tool adapters (Claude/Cursor/Copilot/Generic)
└── templates/               ← Templates for user projects

.claude/                     ← INSTALLED (gitignored in user projects)
├── skills/                  ← Installed from src/skills/
├── agents/                  ← Installed from src/agents/
├── commands/                ← Installed from src/commands/
└── hooks/                   ← Installed from src/hooks/

.specweave/                  ← FRAMEWORK DATA (always present)
├── increments/              ← Feature development
├── docs/                    ← Strategic documentation
└── logs/                    ← Logs and execution history
```

### Golden Rules

1. **✅ ALWAYS edit files in `src/`** (source of truth)
2. **✅ Run install scripts to sync changes to `.claude/`**
3. **❌ NEVER edit files in `.claude/` directly** (they get overwritten)
4. **❌ NEVER create new files in project root** (use increment folders)

**Example Workflow**:
```bash
# CORRECT: Edit source
vim src/skills/increment-planner/SKILL.md

# Sync to .claude/
npm run install:skills

# Test (skill activates from .claude/)
/sw:inc "test feature"

# WRONG: Edit installed file
vim .claude/skills/increment-planner/SKILL.md  # ❌ Gets overwritten!
```

### File Organization Rules

**✅ ALLOWED in Root**:
- `CLAUDE.md` (this file)
- `README.md`, `CHANGELOG.md`, `LICENSE`
- Standard config files (`package.json`, `tsconfig.json`, `.gitignore`)
- Build artifacts (`dist/`, only if needed temporarily)

**❌ NEVER Create in Root** (pollutes repository):
All AI-generated files MUST go into increment folders:

```
❌ WRONG:
/SESSION-SUMMARY-2025-10-28.md          # NO!
/ADR-006-DEEP-ANALYSIS.md               # NO!
/ANALYSIS-MULTI-TOOL-COMPARISON.md      # NO!

✅ CORRECT:
.specweave/increments/0002-core-enhancements/
├── reports/
│   ├── SESSION-SUMMARY-2025-10-28.md
│   ├── ADR-006-DEEP-ANALYSIS.md
│   └── ANALYSIS-MULTI-TOOL-COMPARISON.md
├── logs/
│   └── execution-2025-10-28.log
└── scripts/
    └── migration-helper.sh
```

**Why?**
- ✅ Complete traceability (which increment created which files)
- ✅ Easy cleanup (delete increment folder = delete all files)
- ✅ Clear context (all files for a feature in one place)
- ✅ No root clutter

## Hook System

### What are Hooks?

Hooks are shell scripts that fire automatically on SpecWeave events:
- `post-task-completion` - After EVERY task completion via TodoWrite
- `pre-task-plugin-detect` - Before task execution (plugin detection)
- `post-increment-plugin-detect` - After increment creation
- `pre-implementation` - Before implementation starts

### Current Hook: post-task-completion

**Fires**: After EVERY TodoWrite call
**Purpose**: Notify when work completes

**What it does**:
- ✅ Detects session end (inactivity-based, 15s threshold)
- ✅ Plays notification sound (macOS/Linux/Windows)
- ✅ Shows completion message
- ✅ Logs to `.specweave/logs/hooks-debug.log`
- ✅ Debounces duplicate fires (2s window)

**What it does NOT do yet**:
- ⏳ Update `tasks.md` completion status
- ⏳ Sync living docs automatically
- ⏳ Consolidate GitHub/Jira tasks
- ⏳ Calculate increment progress percentage

**Smart Session-End Detection**:
```
Problem: Claude creates multiple todo lists → sound plays multiple times
Solution: Track inactivity gaps between TodoWrite calls
- Rapid completions (< 15s gap) = Claude still working → skip sound
- Long gap (> 15s) + all done = Session ending → play sound!
```

### Hook Configuration

**File**: `.specweave/config.json`

```json
{
  "hooks": {
    "post_task_completion": {
      "enabled": true,
      "update_tasks_md": false,
      "sync_living_docs": false,
      "play_sound": true,
      "show_message": true
    }
  }
}
```

### Manual Actions

Until hooks are fully automated, **YOU MUST**:
- Update `CLAUDE.md` when structure changes
- Update `README.md` for user-facing changes
- Update `CHANGELOG.md` for API changes
- Update `tasks.md` completion status manually (or use TodoWrite carefully)

## Plugin Architecture

### Core vs. Plugin

**Core Framework** (always loaded):
- 8 core skills (increment-planner, spec-generator, context-loader, etc.)
- 3 core agents (PM, Architect, Tech Lead)
- 7 core commands (/sw:inc, /sw:do, etc.)

**Plugins** (opt-in):
- `specweave-github` - GitHub integration (issue sync, PR creation)
- `specweave-jira` - Jira integration (task sync)
- `specweave-kubernetes` - K8s deployment (planned)
- `specweave-frontend-stack` - React/Vue/Angular (planned)
- `specweave-ml-ops` - Machine learning (planned)

### Context Reduction

**Before plugins**:
- Simple React app: 50K tokens (ALL 44 skills + 20 agents loaded)
- Backend API: 50K tokens
- ML pipeline: 50K tokens

**After plugins**:
- Simple React app: Core + frontend-stack + github ≈ **16K tokens** (68% reduction!)
- Backend API: Core + nodejs-backend + github ≈ **15K tokens** (70% reduction!)
- ML pipeline: Core + ml-ops + github ≈ **18K tokens** (64% reduction!)

### Four-Phase Plugin Detection

1. **Init-Time** (during `specweave init`):
   - Scans package.json, directories, env vars
   - Suggests plugins: "Found React. Enable frontend-stack? (Y/n)"

2. **First Increment** (during `/sw:inc`):
   - Analyzes increment description for keywords
   - Suggests before creating spec: "This needs kubernetes plugin. Enable? (Y/n)"

3. **Pre-Task** (before task execution):
   - Hook scans task description
   - Non-blocking suggestion: "This task mentions K8s. Consider enabling plugin."

4. **Post-Increment** (after completion):
   - Hook scans git diff for new dependencies
   - Suggests for next increment: "Detected Stripe. Enable payment-processing plugin?"

### Hybrid Plugin System

SpecWeave plugins support **dual distribution**:

1. **NPM Package** (SpecWeave CLI):
   - `npm install -g specweave`
   - `specweave plugin install sw-github`
   - Works with ALL tools (Claude, Cursor, Copilot, Generic)

2. **Claude Code Marketplace** (Native `/plugin`):
   - `/plugin marketplace add https://github.com/anton-abyzov/specweave`
   - `/plugin install sw-github@specweave`
   - Best UX for Claude Code users (use HTTPS URL for public repos!)

**Plugin Manifests** (both required):
- `plugin.json` - Claude Code native format
- `manifest.json` - SpecWeave custom format (richer metadata)

## Multi-Tool Support

SpecWeave works with multiple AI coding assistants:

### Claude Code (⭐⭐⭐⭐⭐ 100%)
- Native `.claude/` installation
- Skills auto-activate
- Hooks fire automatically
- Slash commands work natively
- Agents isolate context
- **BEST EXPERIENCE**

### Cursor 2.0 (⭐⭐⭐⭐ 85%)
- `AGENTS.md` compilation
- Team commands via dashboard
- `@context` shortcuts
- Shared agent context (8 parallel agents)
- Manual hook triggers

### GitHub Copilot (⭐⭐⭐ 60%)
- `.github/copilot/instructions.md` compilation
- Natural language instructions only
- Manual workflows
- No hooks or slash commands

### Generic (⭐⭐ 40%)
- `SPECWEAVE-MANUAL.md` for copy-paste
- Manual workflows
- No automation

**Recommendation**: Use Claude Code for SpecWeave. Other tools work, but you'll miss the magic.

## Key Commands

### Increment Lifecycle
- `/sw:inc "feature-name"` - Plan new increment (PM-led process)
- `/sw:do` - Execute next task (smart resume)
- `/sw:progress` - Show progress, PM gate status, next action
- `/sw:validate 0001` - Validate spec, tests, quality
- `/sw:done 0001` - Close increment (PM validation)
- `/sw:next` - Auto-close if ready, suggest next work

### Increment Discipline
- `/sw:status` - Show all increments and completion status
- `/sw:close` - Interactive closure of incomplete increments

### Documentation Sync
- `/sw:sync-docs review` - Review strategic docs before implementation
- `/sw:sync-docs update` - Update living docs from completed increments

### External Platform Sync
- `/sw:sync-github` - Bidirectional GitHub sync
- `/sw:sync-jira` - Bidirectional Jira sync

## Common Questions

### Q: Where do I create a new increment?
**A**: Use `/sw:inc "####-descriptive-name"`. It creates:
```
.specweave/increments/####-descriptive-name/
├── spec.md
├── plan.md
├── tasks.md
└── tests.md
```

### Q: Where do I put analysis files?
**A**: In the increment's `reports/` folder:
```
.specweave/increments/0002-core-enhancements/reports/
└── ANALYSIS-XYZ.md
```

### Q: How do I know what tasks are left?
**A**: Use `/sw:progress` or read `.specweave/increments/####/tasks.md`

### Q: Can I start a new increment before finishing the current one?
**A**: NO! The framework **blocks** you. Use `/sw:status` to check, `/sw:close` to close.

### Q: Where do I edit skills/agents/commands?
**A**: Edit in `src/` (source of truth), then run `npm run install:all` to sync to `.claude/`

### Q: How do I know if a plugin is needed?
**A**: SpecWeave auto-detects! It will suggest plugins during init or increment creation.

### Q: Why does the hook play a sound?
**A**: Session-end detection! If all tasks complete AND you've been idle > 15s, it assumes you're done. Configurable in `.specweave/config.json`.

### Q: How do I disable a hook?
**A**: Edit `hooks/hooks.json` and set `"enabled": false` for that hook.

## Activation Keywords

I activate when you ask about:
- SpecWeave rules / conventions / best practices
- Increment naming / structure / lifecycle
- Where files go / directory structure
- Source of truth / what to edit
- Hook system / automation
- Plugin architecture / context reduction
- How to use SpecWeave / getting started
- What is spec.md / plan.md / tasks.md
- Living docs sync
- Increment discipline / closure
- Multi-tool support (Claude/Cursor/Copilot)

## When to Use Other Skills/Agents

- **increment-planner** - Planning NEW increments (/sw:inc)
- **PM agent** - Leading increment creation (auto-invoked by /sw:inc)
- **Architect agent** - Designing system architecture
- **Tech Lead agent** - Code review, best practices
- **spec-generator** - Creating detailed technical RFCs
- **context-loader** - Explaining context efficiency
- **diagrams-architect** - Creating C4/Mermaid diagrams

I focus on **framework knowledge**. For **increment execution**, use the PM agent and commands!

---

Let me help you understand and use SpecWeave correctly! 🚀

## Project-Specific Learnings

**Before starting work, check for project-specific learnings:**

```bash
# Check if skill memory exists for this skill
cat .specweave/skill-memories/framework.md 2>/dev/null || echo "No project learnings yet"
```

Project learnings are automatically captured by the reflection system when corrections or patterns are identified during development. These learnings help you understand project-specific conventions and past decisions.

