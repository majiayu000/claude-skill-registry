---
name: architect-agent
description: Coordinates planning, delegation, and evaluation across architect and code agent workspaces. Use when asked to "write instructions for code agent", "initialize architect workspace", "grade code agent work", "send instructions", or "verify code agent setup".
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
  - Task
metadata:
  version: 3.1.0
  last-updated: 2025-12-31
---

# Architect Agent Workflow Skill

Coordinate planning, delegation, and evaluation across architect and code agent workspaces.

**Quick Start:** Say "write instructions for code agent", "initialize workspace", "grade work", or "send instructions". For automated setup, see [Quick Setup](#quick-setup-template-based).

## Table of Contents

- [Intent Classification](#intent-classification)
- [Decision Tree](#decision-tree)
- [Resource Loading Policy](#resource-loading-policy)
- [Critical Protocol: File Locations](#critical-protocol-file-locations)
- [Quick Setup](#quick-setup-template-based)
- [DO NOT Trigger For](#do-not-trigger-for)
- [Reference Directory](#reference-directory)
- [Guides Directory](#guides-directory)

## Intent Classification

Route requests based on user intent:

| Intent | Trigger Phrases | Action |
|--------|-----------------|--------|
| **Create Instructions** | "write instructions", "create instructions", "delegate to code agent" | → Load `guides/workflows/create-instructions.md` |
| **Initialize Workspace** | "set up architect agent", "initialize workspace", "new architect agent" | → Load `guides/workflows/initialize-workspace.md` |
| **Grade Work** | "grade the work", "evaluate completed work", "review implementation" | → Load `guides/workflows/grade-work.md` |
| **Send Instructions** | "send instructions", "send to code agent" | → Load `guides/workflows/send-instructions.md` |
| **Add OpenCode Support** | "migrate to OpenCode", "add OpenCode support" | → Load `references/opencode_integration_quickstart.md` |
| **Verify Setup** | "verify setup", "test hooks", "check logging" | → Load `references/workspace_verification_protocol.md` |
| **Setup Permissions** | "set up permissions", "fix permission prompts" | → Load `references/permissions_setup_protocol.md` |
| **Upgrade Workspace** | "upgrade workspace", "migrate to v3.0" | → Load `references/upgrade.md` |

## Decision Tree

| User Intent | Pre-condition | Action |
|-------------|---------------|--------|
| "write/create instructions", "delegate" | `instructions/` exists | Load `guides/workflows/create-instructions.md` |
| "write/create instructions", "delegate" | `instructions/` missing | Suggest workspace initialization first |
| "set up/initialize" workspace | Directories don't exist | Load `guides/workflows/initialize-workspace.md` |
| "set up/initialize" workspace | Directories exist | Warn: already initialized |
| "grade", "evaluate" work | `grades/` exists | Load `guides/workflows/grade-work.md` |
| "grade", "evaluate" work | `grades/` missing | Suggest workspace initialization first |
| "send instructions" | — | Load `guides/workflows/send-instructions.md` (bash copy, no agents) |
| "verify", "test hooks" | — | Load `references/workspace_verification_protocol.md` |
| "OpenCode", "dual-mode" | — | Load `references/opencode_integration_quickstart.md` |
| "permissions" | — | Load `references/permissions_setup_protocol.md` |
| "upgrade", "migrate" | — | Load `references/upgrade.md` |

## Resource Loading Policy

**Load ONLY when needed:**
- Workflow guides: When intent is classified
- Reference docs: When user needs detailed protocol
- Templates: When creating workspace or files
- Never load all references "just in case"

**Core Resources by Intent:**

| Intent | Primary Resource | Supporting Resources |
|--------|-----------------|---------------------|
| Create Instructions | `guides/workflows/create-instructions.md` | `references/instruction_structure.md`, `references/human_instruction_structure.md`, `references/file_naming.md` |
| Initialize Workspace | `guides/workflows/initialize-workspace.md` | `references/workspace_setup_complete.md` |
| Grade Work | `guides/workflows/grade-work.md` | `references/grading_rubrics.md`, `references/decision_types.md` |
| Send Instructions | `guides/workflows/send-instructions.md` | (none - simple bash copy) |
| Verify Setup | `references/workspace_verification_protocol.md` | `references/pre_work_checklist.md` |
| Setup Permissions | `references/permissions_setup_protocol.md` | - |
| OpenCode Support | `references/opencode_integration_quickstart.md` | `references/opencode_setup_guide.md` |

## Critical Protocol: File Locations

**The architect agent operates in its own workspace, NOT the code agent workspace.**

| Artifact | Architect Writes To | Code Agent Location |
|----------|--------------------|--------------------|
| Instructions | `[ARCHITECT]/instructions/` | Reads from `debugging/instructions/` |
| Human Instructions | `[ARCHITECT]/human/` | N/A (for manual execution) |
| Grades | `[ARCHITECT]/grades/` | N/A |
| Logs | N/A | Writes to `[CODE_AGENT]/debugging/logs/` |

**Human Instructions = Executable Documentation** (not summaries!)

Human instructions must enable manual execution when code agents are unavailable. Include copy-pasteable commands, expected output, and troubleshooting. See `references/human_instruction_structure.md`.

**Guard Rail:** If about to write to the code agent's workspace, stop and verify the operation.

## Quick Setup (Template-Based)

For fastest setup, use templates:

```bash
cd ~/.claude/skills/architect-agent/templates/

# Create code agent workspace
./setup-workspace.sh code-agent ~/projects/my-code-agent

# Create architect workspace
./setup-workspace.sh architect ~/projects/my-architect \
    --code-agent-path ~/projects/my-code-agent
```

**Time:** <5 minutes
**See:** `templates/README.md`

## DO NOT Trigger For

- General architecture discussions
- Brainstorming or exploration
- Reading/analyzing existing code
- Research tasks
- Any work that isn't explicit instruction creation, grading, or setup

## Reference Directory

All detailed protocols are in `references/`. Load only what is needed for the current task.

### Core References (Instruction & Grading)

| Reference | Purpose |
|-----------|---------|
| `instruction_structure.md` | Code agent instruction template |
| `human_instruction_structure.md` | Human-executable instruction template |
| `grading_rubrics.md` | 6-category grading criteria |
| `instruction_grading_workflow.md` | Full grading workflow |
| `decision_types.md` | decision, rationale, investigation, verification, deviation, milestone |
| `file_naming.md` | Timestamp and naming conventions |

### Setup & Configuration

| Reference | Purpose |
|-----------|---------|
| `installation.md` | Skill installation guide |
| `quick_start.md` | Fast-track setup |
| `workspace_setup_complete.md` | Full workspace initialization |
| `workspace_verification_protocol.md` | Verify setup is correct |
| `permissions_setup_protocol.md` | Cross-workspace permissions |
| `upgrade.md` | Upgrade to latest version |

### Logging & Debugging

| Reference | Purpose |
|-----------|---------|
| `logging_protocol.md` | Hybrid logging v2.0 |
| `hybrid_logging_protocol.md` | Detailed hybrid logging spec |
| `hook_configuration_critical.md` | Hook setup requirements |
| `hook_logger_enhancements.md` | Hook logger improvements |
| `pre_work_checklist.md` | Code agent pre-work verification |
| `get_unstuck_protocol.md` | Recovery from blockers |
| `resilience_protocol.md` | Error recovery patterns |
| `testing_protocol.md` | Progressive testing requirements |

### OpenCode Integration

| Reference | Purpose |
|-----------|---------|
| `opencode_integration_quickstart.md` | Dual-mode quick start |
| `opencode_setup_guide.md` | Full OpenCode setup |
| `opencode_migration_guide.md` | Migrate to OpenCode |
| `opencode_logging_protocol.md` | OpenCode-specific logging |
| `opencode_wrapper_setup.md` | Wrapper script setup |
| `claude_vs_opencode_comparison.md` | Feature comparison |

### Agent Configuration

| Reference | Purpose |
|-----------|---------|
| `agent_specialization.md` | Agent role configuration |
| `code_agent_claude_template.md` | CLAUDE.md template for code agents |
| `code_agent_agents_template.md` | AGENTS.md template for code agents |

### Project Management

| Reference | Purpose |
|-----------|---------|
| `git_pr_management.md` | Git and PR workflow |
| `ticket_tracking_pr_management.md` | Ticket and PR tracking |

## Guides Directory

Step-by-step workflows in `guides/workflows/`:

| Guide | Trigger |
|-------|---------|
| `create-instructions.md` | "write instructions for code agent" |
| `grade-work.md` | "grade the code agent's work" |
| `send-instructions.md` | "send instructions to code agent" |
| `initialize-workspace.md` | "set up architect agent workspace" |

### Templates

Ready-to-use workspace templates in `templates/`:

| Template | Purpose |
|----------|---------|
| `setup-workspace.sh` | Automated workspace creation script |
| `architect-workspace/` | Complete architect agent workspace template |
| `code-agent-workspace/` | Complete code agent workspace template |

**See:** `templates/README.md` for usage instructions.

---