---
name: continuous-planner
description: "Create a living 3-file continuous plan (task_plan.md, findings.md, progress.md) with explicit skill sequences. Use when user says '/cp', 'continuous plan', 'living plan', '3-file plan', or 'plan with files'."
allowed-tools: Read, Glob, Grep, Write, Edit, Task, Bash
homepage: https://github.com/OthmanAdi/planning-with-files
metadata: {"oneshot":{"emoji":"\u2139\ufe0f","requires":{"bins":["bd", "python3"]}}}
---

# /cp - Continuous Planner - 3-File Pattern (v9)

**Create a living plan that survives session breaks and enables multi-model coordination with explicit skill sequences.**

## Core Philosophy

```
Context Window = RAM (volatile, limited)
Filesystem = Disk (persistent, unlimited)
→ Anything important gets written to disk.
```

The 3-file pattern keeps plans alive across sessions, /clear operations, and even model switches.

## When To Use

User says:
- `/cp [project]` - Quick shortcut for continuous planner
- "continuous plan", "living plan", "3-file plan", "plan with files"
- "create a continuous plan for [project]"
- "I want a plan that survives /clear"
- "multi-model coordination for [task]"
- "working with subagents on [project]"

---

## The 3 Files

| File | Purpose | When Updated |
|------|---------|--------------|
| `task_plan.md` | Single source of truth: phases, decisions, dependencies | When requirements/decisions change |
| `findings.md` | Research, errors, open questions, discoveries | When discovering new information |
| `progress.md` | Session log, actions taken, test results, next steps | After every action |

---

## File Locations

**Project-based (preferred):**
```
$PROJECT_DIR/.claude/continuous/
├── task_plan.md
├── findings.md
└── progress.md
```

**Fallback for no project:**
```
~/.claude/plans/<name>-continuous/
├── task_plan.md
├── findings.md
└── progress.md
```

---

## Workflow

### For Main Agent (You)

**READ before decisions:**
1. Read `task_plan.md` to understand current state
2. Read `findings.md` for existing research
3. Read `progress.md` for last checkpoint

**UPDATE after actions:**
1. Update `progress.md` with what you did
2. Update `findings.md` with new discoveries
3. Update `task_plan.md` only when requirements change

### For Subagents

**Always inject this context when spawning:**

```python
prompt = f"""
You are working on a continuous planning project.

CRITICAL: You MUST follow this workflow:

1. BEFORE ANY DECISION: Read task_plan.md to understand current state
2. BEFORE INVESTIGATION: Read findings.md for existing research
3. AFTER ANY ACTION: Update progress.md with what you did
4. ON NEW DISCOVERY: Update findings.md with what you learned
5. ON REQUIREMENT CHANGE: Update task_plan.md decisions section

Plan Files Location: {plan_files}

Your Task: {task_description}

Remember: The 3 files are your single source of truth.
"""
```

---

## Creating a New Continuous Plan

### Step 1: Gather Requirements

Ask these questions:
1. **What are you building?** (One sentence)
2. **What problem does this solve?**
3. **Who is the user?**
4. **What does "done" look like?**
5. **Any technical constraints?**

### Step 2: Create Directory Structure

```bash
# Determine location
if [ -n "$PROJECT_DIR" ]; then
    PLAN_DIR="$PROJECT_DIR/.claude/continuous"
else
    PLAN_DIR="$HOME/.claude/plans/$(date +%Y%m%d)-${slugified_name}-continuous"
fi

mkdir -p "$PLAN_DIR"
```

### Step 2.5: Discover Required Skills (v9)

**Use skill discovery to find which skills to use:**

```bash
# Run skill discovery for the goal
python3 ~/.claude/skills/skill_discovery.py "$GOAL"
```

This will:
1. Match local skills to the goal
2. Identify skill gaps
3. Suggest SkillsMP searches if needed

**Add skill sequence to task_plan.md:**

```markdown
## Skill Sequence (The Playbook)

1. **front-door** → requirements
   - Interview and triage
   - Status: ⏸️ Pending

2. **[discovered-skill]** → [output]
   - Description of what it does
   - Status: ⏸️ Pending
```

### Step 3: Initialize Files from Templates

Copy templates and fill in:
- `task_plan.md`: Fill summary, problem, goals, decisions, phases
- `findings.md`: Initialize with empty sections
- `progress.md`: Add first session entry

### Step 4: Sync with Beads

```bash
# Create epic
bd create "Continuous: [project-name]" -t epic --json > /tmp/epic.json
EPIC_ID=$(jq -r '.id' /tmp/epic.json)

# Create phases as subtasks
for phase in "Phase 1" "Phase 2" "Phase 3"; do
    bd create "$phase" --deps parent=$EPIC_ID --json
done
```

---

## Multi-Model Coordination

The 3 files are model-agnostic. Any AI can read/write them:

```
┌─────────────────────────────────────────────────────────┐
│                   Shared Files                          │
│  .claude/continuous/{task_plan,findings,progress}.md   │
└─────────────────────────────────────────────────────────┘
          ▲           ▲           ▲           ▲           ▲
          │           │           │           │           │
     GLM 4.7      Opus 4.5     Codex      Gemini     MCP Tools
   (execution)  (planning)   (code)     (research)   (ZAI)
```

**Coordination flow:**
1. **Opus 4.5** (planning): Reads task_plan.md, updates phases/decisions
2. **GLM 4.7** (execution): Reads task_plan.md, updates progress.md after actions
3. **Codex** (code): Reads findings.md for context, writes code
4. **Gemini** (research): Updates findings.md with research
5. **ZAI Vision MCP**: Analyze screenshots/diagrams, diagnose errors from images
6. **ZAI Web Search MCP**: Real-time research for findings.md
7. **ZAI Zread MCP**: Explore GitHub repos for dependencies and code patterns

---

## MCP Integration for Enhanced Planning

The ZAI MCP servers add powerful capabilities to continuous planning:

### Vision MCP (Image & Video Analysis)

| Tool | When to Use |
|------|-------------|
| `ui_to_artifact` | Turn UI screenshots into code/specs |
| `diagnose_error_screenshot` | Analyze error snapshots |
| `understand_technical_diagram` | Architecture, flow, UML, ER diagrams |
| `analyze_data_visualization` | Charts and dashboards |

**Usage in findings.md:**
```markdown
## Visual Analysis (via Vision MCP)
### [Date] - Screenshot/Diagram Analysis
- **Image**: filename.png
- **Tool Used**: diagnose_error_screenshot
- **Findings**: [analysis results]
```

### Web Search MCP (Real-time Research)

| Tool | When to Use |
|------|-------------|
| `webSearchPrime` | Latest web info, news, docs |

**Usage in findings.md:**
```markdown
### MCP-Enabled Research
#### Web Search (via webSearchPrime)
- **Query**: "[search query]"
- **Results**: [key findings with URLs]
- **Relevance**: [how this applies]
```

### Zread MCP (GitHub Repository Intelligence)

| Tool | When to Use |
|------|-------------|
| `search_doc` | Search repo documentation |
| `get_repo_structure` | Understand project layout |
| `read_file` | Read complete file content |

**Usage in findings.md:**
```markdown
#### Zread Repository Analysis
- **Repo**: owner/repo
- **Documentation**: [key docs found]
- **Code Structure**: [relevant files]
```

### MCP Quota Awareness

| Plan Tier | Web Search + Zread | Vision Pool |
|-----------|-------------------|-------------|
| Lite | 100 total/month | 5 hours |
| Pro | 1,000 total/month | 5 hours |
| Max | 4,000 total/month | 5 hours |

**Check quota before heavy MCP usage.**

---

## Session Recovery

After `/clear` or session break:

1. **Read the 3 files:**
   ```bash
   # Main context
   cat .claude/continuous/task_plan.md
   cat .claude/continuous/findings.md
   cat .claude/continuous/progress.md
   ```

2. **Locate last checkpoint:**
   ```markdown
   ## Checkpoint
   **Context Level**: X%
   **Beads Sync**: Complete
   **Files Committed**: Yes
   ```

3. **Continue from next step:**
   Read "Next Steps" section from progress.md

---

## Beads Integration

### Plan → Beads (on creation)

```bash
# Create epic
bd create "Continuous: [project]" -t epic

# Create phases
bd create "Phase 1: [name]" --deps parent=<epic-id>
bd create "Phase 2: [name]" --deps parent=<epic-id>

# Create steps
bd create "[step 1.1]" --deps parent=<phase1-id>
```

### Beads → Plan (on completion)

```bash
# Update progress.md with checkpoint
echo "## Checkpoint" >> progress.md
echo "**Beads Completed**: $(bd list -s completed | wc -l)" >> progress.md
```

---

## Templates

See `templates/` directory for:
- `task_plan.md` - Plan structure with phases, decisions, dependencies
- `findings.md` - Research log with MCP sections
- `progress.md` - Session log with checkpoints

---

## Best Practices

1. **ALWAYS read before writing**: Don't duplicate work
2. **Update progress.md frequently**: After every action
3. **Keep findings.md organized**: Group by date/topic
4. **Only update task_plan.md for decisions**: Not for every small change
5. **Use MCP tools**: Prefer Web Search MCP over built-in WebSearch
6. **Sync with beads**: Keep plan and beads in sync
7. **Create checkpoints**: Before risky operations

---

## Keywords

continuous plan, living plan, 3-file plan, plan with files, continuous planning, multi-model coordination, persistent plan, session recovery
