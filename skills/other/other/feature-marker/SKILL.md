---
name: feature-marker
description: >
  End-to-end feature development orchestrator that automates the full lifecycle
  from requirements to pull request. Generates PRD, Tech Spec, and Task
  breakdown artifacts, then executes a 4-phase workflow: Analysis →
  Implementation → Tests → Commit & PR. Supports 5 execution modes: Full
  Workflow (generate all artifacts + run all phases), Tasks Only (skip
  generation, use existing files), Ralph Loop (autonomous self-correcting
  execution), Spec-Driven (multi-agent review with worktree isolation), and
  Test Only (run tests phase exclusively). Includes checkpoint/resume so work
  can be paused and resumed at any phase, and auto-detects GitHub, Azure DevOps,
  or GitLab for PR creation. Platform-agnostic with auto stack detection for
  iOS/Swift, Node.js/TypeScript, Rust, Python, and Go.

  ALWAYS use this skill when the user says "implement this feature", "build
  feature X", "start a new feature", "create a PRD", "generate tech spec",
  "break down tasks", "feature workflow", "plan this feature", "implement
  from spec", "run the full workflow", "resume feature", "continue where I
  left off", asks to go from requirements to implementation, wants to automate
  feature development end-to-end, mentions PRD-to-PR pipelines, or says
  "/feature-marker" — even if they just say "I need to build X" without
  explicitly mentioning a workflow. Also trigger when the user mentions
  "Ralph Loop", "spec-driven mode", "checkpoint", or asks to generate tasks
  from a PRD or tech spec.
tools: Read, Write, Edit, Grep, Glob, Bash, TodoWrite, Skill
---

# feature-marker

Automates feature development with a 5-phase workflow:

1. **Inputs Gate** - Validates `prd.md`, `techspec.md`, `tasks.md` exist; generates them via `~/.claude/commands/` if missing.
2. **Analysis & Planning** - Auto-installs product-manager skill if missing; reads docs, creates implementation plan.
3. **Implementation** - Executes tasks with progress tracking.
4. **Tests & Validation** - Runs platform-appropriate test suites and build validation.
   Auto-detects: Swift/Xcode (+ XcodeBuildMCP simulator), Node.js, Rust, Python, Go.
5. **Commit & PR** - Auto-installs enhanced commit command if missing; commits changes using professional workflow and creates PR (auto-detects git platform).

## Platform Support

feature-marker works with any tech stack:

- 🍎 **iOS/Swift** — `swift test` + SwiftLint + XcodeBuildMCP simulator validation
- 🟨 **Node.js/TypeScript** — auto-detects npm/yarn/pnpm/bun + Jest/Vitest
- 🦀 **Rust** — `cargo test` + `cargo clippy`
- 🐍 **Python** — `pytest` + ruff/flake8
- 🐹 **Go** — `go test` + `go vet`

iOS/Xcode projects get additional simulator validation via XcodeBuildMCP (optional, non-blocking).
The platform is auto-detected once at workflow start and cached — no configuration required.

## Usage

```
/feature-marker <feature-slug>
```

**Example**:

```
/feature-marker prd-user-authentication
```

### Interactive Mode

```
/feature-marker --interactive <feature-slug>
```

Opens a menu to select execution mode:

- **Full Workflow** - Default, generates missing files and executes all phases
- **Tasks Only** - Uses existing files, skips generation phase
- **Ralph Loop** - Autonomous continuous execution with ralph-wiggum
- **Spec-Driven** - Multi-agent review + worktree isolation via spec-workflow
- **Test Only** - Runs tests phase exclusively using platform-appropriate test guidance (Swift Testing for iOS, Jest/Vitest for Node.js, etc.)

Works both in terminal (TTY menu) and Claude CLI (AskUserQuestion prompt).

**Direct mode selection** (skip menu):

```
/feature-marker --mode full <feature-slug>
/feature-marker --mode tasks-only <feature-slug>
/feature-marker --mode ralph-loop <feature-slug>
/feature-marker --mode spec-driven <feature-slug>
/feature-marker --mode test-only <feature-slug>
```

## Prerequisites

### Commands

The following commands must be available in `~/.claude/commands/`:

- `create-prd.md` - Creates a new PRD from requirements discussion
- `generate-spec.md` - Generates technical specification from PRD
- `generate-tasks.md` - Breaks down feature spec into implementable tasks

### Templates

The commands above read templates from `~/.claude/docs/specs/` to generate structured documents.

Required templates:

- `~/.claude/docs/specs/prd-template.md` - Product Requirements Document template
- `~/.claude/docs/specs/techspec-template.md` - Technical Specification template
- `~/.claude/docs/specs/tasks-template.md` - Tasks breakdown template

**Template Format**: Templates should be markdown files with placeholders and structure that commands will use to generate feature-specific documents.

**Setup**: Ensure these templates exist before running feature-marker:

```bash
ls ~/.claude/docs/specs/
# Should show: prd-template.md, techspec-template.md, tasks-template.md
```

**Note**: If templates are missing, commands in `~/.claude/commands/` will fail to generate files.

### Project Structure

**Feature Documents** (generated in project):

```
./tasks/
└── prd-{feature-name}/
    ├── prd.md            ← Generated from ~/.claude/docs/specs/prd-template.md
    ├── techspec.md       ← Generated from ~/.claude/docs/specs/techspec-template.md
    ├── tasks.md          ← Generated from ~/.claude/docs/specs/tasks-template.md
    └── {num}_task.md     ← Individual task files (optional)
```

**State Directory** (checkpoint & progress):

```
.claude/feature-state/{feature-name}/
├── checkpoint.json
├── analysis.md
├── plan.md
├── progress.md
├── test-results.md
└── pr-url.txt
```

**User Configuration** (required setup):

```
~/.claude/
├── commands/           ← Commands that generate files
│   ├── create-prd.md
│   ├── generate-spec.md
│   └── generate-tasks.md
└── docs/
    └── specs/          ← Templates used by commands
        ├── prd-template.md
        ├── techspec-template.md
        └── tasks-template.md
```

## Behavior

When invoked, the skill:

1. **Validates inputs** - Checks if `./tasks/prd-{feature-slug}/` contains required files
   - If all files exist → Skips to step 3
   - If any file is missing → Proceeds to step 2
2. **Generates ONLY missing files** - Existing files are never overwritten:
   - Missing PRD → `/create-prd`
   - Missing Tech Spec → `/generate-spec {feature-slug}`
   - Missing Tasks → `/generate-tasks {feature-slug}`
3. **Auto-installs missing dependencies**:
   - **Phase 1**: Checks for `product-manager` skill
     - If missing: Installs via `npx skills add https://github.com/aj-geddes/claude-code-bmad-skills --skill product-manager`
     - If user already has it: Uses user's version
     - If installation fails: Continues without it (non-blocking)
   - **Phase 4**: Checks for `/commit` command
     - If missing: Copies from bundled `resources/commit.md` to `~/.claude/commands/commit.md`
     - If user already has it: Uses user's version
     - If installation fails: Falls back to standard commit workflow
4. **Executes 5-phase workflow** via the `feature-marker` agent
5. **Persists state** - Saves checkpoints after each phase/task for resume capability

**Important**: The workflow is smart about file detection and dependencies:

- ✅ Files/skills/commands exist → Uses them directly, no regeneration or reinstallation
- ⚠️ Missing → Installs/generates only what's needed
- 🔒 Never overwrites existing content
- 👤 **User's versions always have priority** over bundled/auto-installed versions

## Auto-Installed Dependencies

Feature-marker automatically installs missing dependencies to enhance the workflow:

### Product Manager Skill (Phase 1)

**What it does**: Provides advanced PRD analysis, requirements validation, and product management capabilities.

**Installation**:

- **Check**: Phase 1 checks for `~/.claude/skills/product-manager/SKILL.md`
- **Install**: If missing and `npx` available, runs:
  ```bash
  npx skills add https://github.com/aj-geddes/claude-code-bmad-skills --skill product-manager
  ```
- **Priority**: Uses user's existing skill if already installed
- **Fallback**: Continues without it if installation fails (non-blocking)

**Benefits**:

- Enhanced requirement analysis
- Better PRD validation
- Improved feature planning

### Enhanced Commit Command (Phase 4)

**What it does**: Professional commit workflow with validation, splitting, and conventional commit format.

**Installation**:

- **Check**: Phase 4 checks for `~/.claude/commands/commit.md`
- **Install**: If missing, copies from bundled `resources/commit.md` to `~/.claude/commands/commit.md`
- **Priority**: Uses user's existing command if already installed
- **Fallback**: Uses standard commit workflow if installation fails

**Features**:

- Pre-commit validation (lint, build, docs)
- Intelligent commit splitting
- Conventional commit format with emojis
- Smart file staging
- No Co-Authored-By footer (as per command design)

**Example Output**:

```bash
✨ feat: add user authentication system
🐛 fix: resolve memory leak in rendering process
📝 docs: update API documentation
♻️ refactor: simplify error handling logic
```

### Manual Installation

If auto-installation fails, you can install manually:

**Product Manager Skill**:

```bash
npx skills add https://github.com/aj-geddes/claude-code-bmad-skills --skill product-manager
```

**Commit Command**:

```bash
cp ~/.claude/skills/feature-marker/resources/commit.md ~/.claude/commands/commit.md
```

## Template Setup Guide

### Template Directory Structure

Commands in `~/.claude/commands/` read templates from a centralized location:

```
~/.claude/docs/specs/
├── prd-template.md          # Product Requirements Document template
├── techspec-template.md     # Technical Specification template
└── tasks-template.md        # Task breakdown template
```

### Why Templates in ~/.claude/docs/specs?

- **Centralized**: All projects share the same templates
- **User-controlled**: Users can customize their own templates
- **Portable**: Commands reference templates via standard path
- **Separation**: Templates are not in project repositories

### Template Content

Each template should be a markdown file with:

- Clear section structure
- Placeholder text or variables
- Examples and formatting guidelines

Commands read these templates and populate them with feature-specific content.

### Setup Verification

To verify your setup is complete:

```bash
# Check templates exist
ls -l ~/.claude/docs/specs/

# Check commands exist
ls -l ~/.claude/commands/

# Test feature-marker
/feature-marker --interactive prd-test-feature
```

If templates are missing, create them in `~/.claude/docs/specs/` before running feature-marker.

## Plan Mode Integration

When the user has used Claude's built-in plan mode before invoking feature-marker, the agent automatically:

1. **Detects the most recent plan** from `~/.claude/plans/` (sorted by modification time)
2. **Reads project conventions** from `./CLAUDE.md` at the project root (if present)
3. **Uses both as rich context** to enhance PRD generation and reduce redundant clarification questions

This is automatic and requires no additional flags or options. If no plan or CLAUDE.md exists, the workflow proceeds normally.

**Recommended flow**:

```
1. Use Claude plan mode to explore the codebase and think through the feature
2. Exit plan mode
3. Run /feature-marker --interactive <feature-slug>
4. Select "Full Workflow"
5. The plan content automatically enriches PRD generation
```

## Checkpoint & Resume

If interrupted (Ctrl+C, session crash, etc.), re-invoke with the same feature slug to resume:

```
/feature-marker prd-user-authentication
```

The skill will:

- Detect existing checkpoint
- Show current progress (phase, task index)
- Ask if you want to resume or start fresh

## Platform Detection

In Phase 4, the skill auto-detects your git platform and selects the appropriate PR skill:

| Platform     | Detection                     | PR Skill      |
| ------------ | ----------------------------- | ------------- |
| GitHub       | `github.com` in remote URL    | `checking-pr` |
| Azure DevOps | `dev.azure.com` in remote URL | `azure-pr`    |
| GitLab       | `gitlab.com` in remote URL    | `checking-pr` |
| Bitbucket    | `bitbucket.org` in remote URL | `checking-pr` |
| Other        | (fallback)                    | `checking-pr` |

## Configuration

Override default behavior with `.feature-marker.json` in your repository root:

```json
{
  "pr_skill": "custom-pr-skill",
  "skip_pr": false,
  "test_command": "npm run test:ci",
  "docs_path": "./tasks",
  "state_path": ".claude/feature-state"
}
```

## Error Handling

| Scenario             | Behavior                              |
| -------------------- | ------------------------------------- |
| Missing files        | Auto-generate via commands            |
| No git repo          | Fail early with helpful message       |
| No tests             | Skip Phase 3 with warning             |
| Test failures        | Report issues, allow fix, offer retry |
| Unknown platform     | Fallback to `checking-pr`             |
| PR skill unavailable | Commit only, log manual instructions  |

## Example Sessions

### Example 1: All Files Exist (No Generation Needed)

```
> /feature-marker prd-user-authentication

Checking for existing checkpoint...
No checkpoint found. Starting new workflow.

Phase 0: Inputs Gate
✓ prd.md exists
✓ techspec.md exists
✓ tasks.md exists
✅ All files present. Skipping generation.

Phase 1: Analysis & Planning
Reading existing documents...
Creating implementation plan...
Checkpoint saved.

Phase 2: Implementation
[1/6] Create User entity... ✓
[2/6] Add authentication service... ✓
...
```

### Example 2: Partial Files (Generates Only Missing)

```
> /feature-marker prd-payment-integration

Checking for existing checkpoint...
No checkpoint found. Starting new workflow.

Phase 0: Inputs Gate
✓ prd.md exists
✗ techspec.md missing → Generating via /generate-spec...
✓ tasks.md exists

✅ Generated missing file. All inputs ready.

Phase 1: Analysis & Planning
Reading documents...
Creating implementation plan...
Checkpoint saved.
...
```

### Example 3: Complete Workflow with Auto-Install

```
> /feature-marker prd-new-feature

Phase 0: Inputs Gate
✗ prd.md missing → Generating via /create-prd...
✗ techspec.md missing → Generating via /generate-spec...
✗ tasks.md missing → Generating via /generate-tasks...

Phase 1: Analysis & Planning
⚙️  Installing product-manager skill...
✓ product-manager skill installed successfully
Reading PRD, Tech Spec, and Tasks...
Creating implementation plan...
Checkpoint saved.

Phase 2: Implementation
[1/6] Create User entity... ✓
[2/6] Add authentication service... ✓
[3/6] Implement login endpoint... ✓
[4/6] Add JWT token handling... ✓
[5/6] Create logout endpoint... ✓
[6/6] Add session management... ✓
Checkpoint saved.

Phase 3: Tests & Validation
✅ Platform detected: Node.js / Next.js (pnpm)
Running: jest --findRelatedTests src/api/users.ts
✅ 14 passed, 0 failed
Lint: pnpm run lint ✅
Checkpoint saved.

Phase 4: Commit & PR
⚙️  Installing commit command...
✓ commit command installed successfully
Using enhanced commit workflow (/commit)...
✨ feat: implement user authentication system
Detected platform: GitHub
Creating PR via /checking-pr...

✓ Feature complete!
PR URL: https://github.com/user/repo/pull/42
```

### Example 4: Using Existing User Tools

```
> /feature-marker prd-payment-feature

Phase 0: Inputs Gate
✓ All inputs validated.

Phase 1: Analysis & Planning
✓ product-manager skill already installed (using user's version)
...

Phase 4: Commit & PR
✓ commit command already exists (using user's version)
...
```
