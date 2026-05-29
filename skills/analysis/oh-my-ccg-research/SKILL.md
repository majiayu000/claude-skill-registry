---
name: oh-my-ccg-research
description: RPI 研究阶段 — 需求转化为约束集
---

# oh-my-ccg Research Phase

You are executing the RPI Research phase. Transform requirements into verifiable constraint sets.

## Prerequisites
- RPI state must exist (run `/oh-my-ccg:init` first)
- A requirement description must be provided

## Workflow

### Step 1: Restore State
Use the **oh-my-ccg-tools** MCP server's `rpi_state_read` tool.
Confirm current phase allows transition to RESEARCH.

### Step 2: Create OpenSpec Change (Optional)
If OpenSpec CLI is available:
```bash
npx openspec new change "<requirement-name>"
```
If OpenSpec is not installed, skip this step — artifacts will be managed via file system in `.oh-my-ccg/plans/`.

### Step 3: Codebase Exploration
Use the `explore` agent to scan the codebase for:
- Existing patterns related to the requirement
- Files that will be affected
- Dependencies and interfaces involved

### Step 4: Multi-Model Constraint Exploration (PARALLEL)
Launch both models **simultaneously in a single message** using MCP tools:

**Codex** (backend perspective) — use `ask_codex` tool:
- `agent_role`: "analyst"
- `prompt`: Describe the requirement and ask for backend/logic constraints
- `context_files`: Relevant source files from Step 3
- `background`: true

**Gemini** (frontend perspective) — use `ask_gemini` tool:
- `agent_role`: "designer"
- `prompt`: Describe the requirement and ask for UI/UX constraints
- `files`: Relevant source files from Step 3
- `background`: true

Then use `check_job_status` for both job IDs to collect results.

### Step 5: Synthesize Constraints
Merge findings from explore + Codex + Gemini into a unified constraint set:
- Classify each as Hard or Soft
- Define verification criteria
- Resolve any conflicts between models

### Step 6: User Interaction
Present constraints to user. Ask for:
- Confirmation of hard constraints
- Prioritization of soft constraints
- Clarification of any ambiguities

### Step 7: Persist State
Use the **oh-my-ccg-tools** MCP server's `rpi_state_write` tool to save:
- Updated constraints array
- Phase transition to "research"
- Change ID (if OpenSpec was used)

If OpenSpec is available, also generate `proposal.md` in the change directory.

### Step 8: Report
Output summary: constraint count (Hard/Soft), key findings, and instructions to `/clear` then `/oh-my-ccg:plan`.
