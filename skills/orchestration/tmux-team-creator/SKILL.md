---
name: tmux-team-creator
description: This skill should be used when users want to create a multi-agent tmux team for their project. It provides battle-tested templates for setting up autonomous AI agent teams that collaborate via tmux. Use this skill when users ask to create AI teams, set up multi-agent workflows, or build autonomous coding teams. The skill includes 4 sample team templates (2 software development + 2 research) that can be customized for any domain.
---

# Tmux Team Creator

## Overview

This skill enables creating powerful multi-agent AI teams that run autonomously in tmux sessions. The architecture is battle-tested on complex projects and can be customized for any domain.

**Key Insight**: Sample teams are TEMPLATES, not exact copies. When creating a team, customize roles, prompts, and workflows for the specific project.

---

## ⚠️ CRITICAL: Tmux Pane Detection Bug (EXTREMELY COMMON)

**THIS BUG WILL WASTE HOURS IF NOT PREVENTED!**

### The Bug

When agents need to determine which tmux pane they're running in, **NEVER use `tmux display-message -p '#{pane_index}'`** - this command returns the **ACTIVE/FOCUSED pane** (where the user's cursor is), NOT the pane where the agent is actually running!

### The Fix

**Always use the `$TMUX_PANE` environment variable:**

```bash
# WRONG - Returns active cursor pane, not your pane
tmux display-message -p '#{pane_index}'

# CORRECT - Returns YOUR actual pane
echo $TMUX_PANE
# Then look up this pane ID to get your role
tmux list-panes -a -F '#{pane_id} #{pane_index} #{@role_name}' | grep $TMUX_PANE
```

### Why This Matters

- In multi-agent teams, each pane has a specific role (PO, TL, DEV, etc.)
- Messages must route correctly based on pane roles
- If agents misidentify their pane, they send messages to wrong agents
- This causes hours of debugging "why is PO acting like DEV?"

### Where to Check

When creating a new team from templates, verify these files use `$TMUX_PANE`:

1. **Role prompt files** (`prompts/*_PROMPT.md`) - Should document correct pane detection
2. **Init commands** (`commands/init-role.md`) - Should use `$TMUX_PANE` for role detection
3. **Setup scripts** (`setup-team.sh`) - Should set `@role_name` on correct panes
4. **Hook scripts** (`hooks/*.sh`, `hooks/*.py`) - **CRITICAL:** Must use `$TMUX_PANE`
   - **Bash hooks:** `ROLE=$(tmux show-options -t "$TMUX_PANE" -qv @role_name)`
   - **Python hooks:** `tmux_pane = os.environ.get("TMUX_PANE")` then `["tmux", "show-options", "-pt", tmux_pane, "-qv", "@role_name"]`
   - **WRONG:** `tmux show-options -pv @role_name` (queries cursor pane!)
   - **FIX APPLIED:** `hooks/session_start_team_docs.py` (2026-01-02) - All new teams now use correct detection

### Prevention Checklist

When creating a new team, add this to ALL role prompts:

```markdown
## Tmux Pane Configuration & Role Detection

**CRITICAL: Correct Pane Detection**

**NEVER use `tmux display-message -p '#{pane_index}'`** - it returns the active/focused pane, not YOUR pane!

**Always use $TMUX_PANE environment variable:**

\`\`\`bash
# Find YOUR actual pane ID
echo "My pane: $TMUX_PANE"

# Look up your pane's role
tmux list-panes -a -F '#{pane_id} #{pane_index} #{@role_name}' | grep $TMUX_PANE
\`\`\`
```

**This bug has already been fixed in all sample team templates.** When creating new teams, copy the corrected patterns.

---

## FIRST: Ask User Which Team Template

**Before creating any team, ask the user which template they want to use.**

### Available Templates

#### Software Development Teams

| Template | Best For | Roles | Key Features |
|----------|----------|-------|--------------|
| **scrum-team** | Standard Scrum projects | PO, SM, TL, BE, FE, QA | Full Scrum framework, SM owns process improvement, Sprint-based |
| **scrum-minimal-team** | Small projects, MVPs | PO, SM, EX | Lightweight 3-person Scrum, EX combines TL+DEV+QA |
| **game-dev-team** | Game development projects | PM, GD, FE, BE, QA | Game-focused with design→implementation flow |

#### Research & Analysis Teams

| Template | Best For | Roles | Key Features |
|----------|----------|-------|--------------|
| **mckinsey-research-team** | Market research, competitive analysis | EM, RL, PR, SR, DA, QR | McKinsey 7-step methodology, MECE structuring, Pyramid Principle |
| **pg-insights-team** | Consumer insights, brand strategy | IM, MR, IA, SL, QR | P&G Three-Step Formula, human-centric, goosebumps test |

### Selection Logic

**If user specifies:**
- "Scrum team" / "standard Scrum" / "with Scrum Master" → Use `scrum-team`
- "minimal Scrum" / "small team" / "solo dev" / "MVP" / "lightweight" → Use `scrum-minimal-team`
- "game" / "game development" / "game project" → Use `game-dev-team`
- "market research" / "competitive analysis" / "McKinsey" / "research team" → Use `mckinsey-research-team`
- "consumer insights" / "P&G" / "brand strategy" / "emotional research" → Use `pg-insights-team`

**If user doesn't specify:**
Ask: "Which team template would you like to use?"

**Software Development:**
- **scrum-team** (Recommended for dev) - Full Scrum with PO, SM, TL, BE, FE, QA. SM owns process improvement.
- **game-dev-team** - Game development with PM, GD, FE, BE, QA. Design-first workflow.

**Research & Analysis:**
- **mckinsey-research-team** - McKinsey-style research with EM, RL, PR, SR, DA, QR. Hypothesis-driven, MECE structured.
- **pg-insights-team** - P&G-style consumer insights with IM, MR, IA, SL, QR. Human-centric, emotional + logical.

### Template Descriptions

#### 1. scrum-team (Recommended for most projects)

**Roles:** PO (Product Owner), SM (Scrum Master), TL (Tech Lead), BE (Backend), FE (Frontend), QA (Tester)

**Key Features:**
- Full Scrum framework adapted for AI teams
- SM owns process improvement with 4-checkpoint monitoring mechanism
- Sprint-based workflow with Planning, Review, Retrospective
- Black-box QA testing
- Prompt hygiene rules (add after 2-3 recurring issues, remove when learned)

**Best for:** Teams that want structured improvement, multiple sprints, quality focus

#### 2. scrum-minimal-team (Lightweight Scrum)

**Roles:** PO (Product Owner), SM (Scrum Master), EX (Executive = TL + DEV + QA)

**Key Features:**
- Minimal overhead for small projects
- EX combines architecture, development, and testing
- Same Sprint-based workflow as full Scrum
- SM still owns process improvement
- 3-pane tmux layout

**Best for:** Solo developers, MVPs, prototypes, personal projects wanting Scrum structure

#### 3. game-dev-team (Game Development)

**Roles:** DS (Game Designer), SM (Scrum Master), AR (Game Architect), DV (Game Developer), QA (Game QA)

**Key Features:**
- BMGD (BMAD Game Development) methodology + Scrum practices
- Design→Architecture→Implementation→Testing flow
- 60fps is non-negotiable - performance is a feature
- Playable increments every Sprint
- Design from player experience first

**Workflow:**
1. DS: Create Game Brief and GDD (mechanics, systems, content)
2. AR: Select engine, plan architecture, define performance budgets
3. DV: Implement Sprint stories with TDD
4. QA: Automated tests, playtests, performance profiling

**Best for:** Game development projects, interactive applications, real-time simulations

#### 4. mckinsey-research-team (McKinsey-style research)

**Roles:** EM (Engagement Manager), RL (Research Lead), PR (Primary Researcher), SR (Secondary Researcher), DA (Data Analyst), QR (Quality Reviewer)

**Key Features:**
- McKinsey 7-step problem-solving process
- MECE structuring (Mutually Exclusive, Collectively Exhaustive)
- Pyramid Principle for communication (lead with answer)
- Triangulation (multiple sources for key findings)
- EM owns process improvement with 4-checkpoint monitoring

**Workflow:**
1. Define Problem (EM ↔ Client)
2. Structure Problem (RL - MECE issue tree)
3. Prioritize Issues (EM + RL)
4. Plan Analysis (EM)
5. Conduct Analysis (PR, SR, DA in parallel)
6. Synthesize Findings (RL)
7. Communicate Recommendations (EM + RL → QR → Client)

**Best for:** Market research, competitive analysis, industry analysis, due diligence, strategy research

#### 5. pg-insights-team (P&G-style consumer insights)

**Roles:** IM (Insights Manager), MR (Moments Researcher), IA (Insight Analyst), SL (Strategy Lead), QR (Quality Reviewer)

**Key Features:**
- P&G Three-Step Insights Formula
- Human-centric research (everyday moments)
- Logic + Emotion connection
- Goosebumps test for insight validation
- IM owns process improvement with 4-checkpoint monitoring

**Workflow:**
1. Find Everyday Moments That Matter (MR)
2. Find How Brand Matters in Those Moments (IA)
3. Find the Brand Idea That Makes Moments Matter More (SL)

**Best for:** Consumer insights, brand strategy, product innovation, emotional brand positioning

---

## Core Concepts

### What is a Tmux Team?

A tmux team is multiple Claude Code instances running in different tmux panes, each with a specialized role:

- **PM (Project Manager)** - Central coordinator, routes all communication
- **Architect** (SA in sample) - Designs solutions, API contracts, guards progressive approach
- **Implementers** (BE/FE in sample) - Code the solutions progressively
- **Code Reviewer** (CR) - Quality gatekeeper, reviews implementations

### Key Principles

1. **PM is the Hub** - All communication flows through PM, never direct agent-to-agent
2. **Sprint-based Workflow** - 10-step sprint process from idea to delivery
3. **Git as Progress Tracker** - Commits show real progress, not chat logs
4. **Progressive Implementation** - Build incrementally (small → medium → full)
5. **Boss Appears After Step 10** - Team self-coordinates during sprint
6. **Two-Enter Rule** - Tmux messages require two SEPARATE commands for reliable delivery

## Team Creation Workflow

### Step 0: Select Team Template

**Ask the user which template to use** (see "FIRST: Ask User Which Team Template" above).

If user doesn't specify, recommend `scrum-team` for most projects.

### Step 1: Understand User's Project

Before creating a team, understand:
1. **Domain** - What type of project? (web app, data pipeline, trading system, etc.)
2. **Team Roles** - What specialists are needed? (may differ from template)
3. **Working Directory** - Absolute path to the project
4. **Selected Template** - Which of the 3 templates to use

### Step 2: Create Project Structure

Create the following structure in the user's project:

```
{project_root}/
├── .claude/
│   ├── commands/
│   │   └── init-role.md              # Slash command to initialize agent roles
│   ├── hooks/
│   │   └── session_start_team_docs.py  # SessionStart hook (CRITICAL - injects role context)
│   └── settings.json                 # Hook configuration
└── docs/
    └── tmux/
        └── {team-name}/
            ├── workflow.md # Agent workflow documentation
            ├── WHITEBOARD.md         # Collaboration tool (PM maintains)
            └── prompts/
                ├── PM_PROMPT.md      # PM role prompt
                ├── {ROLE2}_PROMPT.md # Other role prompts
                └── ...
```

### Step 3: Customize from Selected Template

Use the selected template from `sample_team/` and customize:

1. **Copy selected template** to user's project:
   - `scrum-team/` → for Scrum projects
   - `game-dev-team/` → for game development
   - `mckinsey-research-team/` → for market research
   - `pg-insights-team/` → for consumer insights
2. **Rename roles** to match user's domain (if needed):
   - AR → Architect / Designer
   - BE/FE/DV → Implementer / Developer / Engineer
   - Keep SM and QA (universal roles)
3. **Update prompts** with project-specific:
   - Working directory paths
   - Domain-specific responsibilities
   - Communication protocols
4. **Create setup script** based on template's `setup-team.sh`
5. **Copy improvement docs** (if using scrum-team or pm-retro):
   - `sm/` or `pm/` folder with IMPROVEMENT_BACKLOG.md, etc.

### Step 4: Configure Hooks and Commands

#### init-role.md (Slash Command)

Create `{project}/.claude/commands/init-role.md`:

```markdown
# Initialize Agent Role

You are initializing as a member of the [TEAM_NAME] Multi-Agent Team.

## Step 1: Read System Documentation

First, read the system overview to understand the multi-agent workflow:

**File**: `docs/tmux/{team-name}/workflow.md`

## Step 2: Read Your Role Prompt

Based on the role argument `$ARGUMENTS`, read your specific role prompt:

- **PM** (Project Manager): `docs/tmux/{team-name}/prompts/PM_PROMPT.md`
- **SA** (Architect): `docs/tmux/{team-name}/prompts/SA_PROMPT.md`
- **BE/FE** (Implementers): `docs/tmux/{team-name}/prompts/{ROLE}_PROMPT.md`
- **CR** (Code Reviewer): `docs/tmux/{team-name}/prompts/CR_PROMPT.md`

## Step 3: Understand Your Mission

After reading both files:
1. Confirm your role and responsibilities
2. Verify your communication pane IDs are configured
3. Check the WHITEBOARD for current sprint status
4. Be ready to execute your role in the workflow
```

#### session_start_team_docs.py (SessionStart Hook - CRITICAL)

This hook automatically injects team overview and role prompts when agents start or auto-compact. **Without this hook, agents lose context after auto-compact.**

**Step 1**: Copy the template from this skill to your project:

```bash
cp ~/.claude/skills/tmux-team-creator/hooks/session_start_team_docs.py \
   {project}/.claude/hooks/session_start_team_docs.py
chmod +x {project}/.claude/hooks/session_start_team_docs.py
```

**Step 2**: Edit the `TEAM_CONFIGS` section in the copied file:

```python
TEAM_CONFIGS = {
    "your-session-name": {
        "docs_dir": os.path.join(PROJECT_ROOT, "docs/tmux/your-team"),
        "roles": {"PM", "SA", "BE", "FE", "CR"},
    },
}
```

Example for scrum-team:
```python
TEAM_CONFIGS = {
    "scrum-team": {
        "docs_dir": os.path.join(PROJECT_ROOT, "docs/tmux/scrum-team"),
        "roles": {"PO", "SM", "TL", "FE", "BE", "QA"},
    },
}
```

**Step 3**: Create `{project}/.claude/settings.json`:

```json
{
  "hooks": {
    "SessionStart": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/session_start_team_docs.py",
            "timeout": 10
          }
        ]
      }
    ]
  }
}
```

**What this hook does:**
1. Detects current tmux session name
2. Looks up team config (docs_dir, valid roles)
3. Reads `@role_name` from tmux pane option
4. Injects `workflow.md` + `{ROLE}_PROMPT.md` into agent context

**Why it's critical:** Without this hook, agents forget their role and team workflow after auto-compact, leading to confusion and wrong behavior.

### Step 5: Create Setup Script

Create `docs/tmux/{team-name}/setup-team.sh`:

```bash
#!/bin/bash
# [TEAM_NAME] - Automated Setup Script

set -e

PROJECT_ROOT="/path/to/project"
SESSION_NAME="team-name"
PROMPTS_DIR="$PROJECT_ROOT/docs/tmux/{team-name}/prompts"

echo "Starting [TEAM_NAME] Setup..."

# Kill existing session if exists
if tmux has-session -t $SESSION_NAME 2>/dev/null; then
    tmux kill-session -t $SESSION_NAME
fi

# Create session
cd "$PROJECT_ROOT"
tmux new-session -d -s $SESSION_NAME

# Create N-pane layout (adjust for number of agents)
tmux split-window -h -t $SESSION_NAME
tmux split-window -h -t $SESSION_NAME
tmux split-window -h -t $SESSION_NAME
tmux select-layout -t $SESSION_NAME even-horizontal

# Set pane titles (visual display)
tmux select-pane -t $SESSION_NAME:0.0 -T "PM"
tmux select-pane -t $SESSION_NAME:0.1 -T "[ROLE2]"
tmux select-pane -t $SESSION_NAME:0.2 -T "[ROLE3]"
tmux select-pane -t $SESSION_NAME:0.3 -T "Code-Reviewer"

# Set @role_name options (stable - won't be overwritten by Claude Code)
tmux set-option -p -t $SESSION_NAME:0.0 @role_name "PM"
tmux set-option -p -t $SESSION_NAME:0.1 @role_name "[ROLE2]"
tmux set-option -p -t $SESSION_NAME:0.2 @role_name "[ROLE3]"
tmux set-option -p -t $SESSION_NAME:0.3 @role_name "Code-Reviewer"

# Start Claude Code in each pane
tmux send-keys -t $SESSION_NAME:0.0 "cd $PROJECT_ROOT && claude" C-m
tmux send-keys -t $SESSION_NAME:0.1 "cd $PROJECT_ROOT && claude" C-m
tmux send-keys -t $SESSION_NAME:0.2 "cd $PROJECT_ROOT && claude" C-m
tmux send-keys -t $SESSION_NAME:0.3 "cd $PROJECT_ROOT && claude" C-m

sleep 15

# Initialize roles
tmux send-keys -t $SESSION_NAME:0.0 "/init-role PM" C-m
tmux send-keys -t $SESSION_NAME:0.0 C-m
tmux send-keys -t $SESSION_NAME:0.1 "/init-role [ROLE2]" C-m
tmux send-keys -t $SESSION_NAME:0.1 C-m
tmux send-keys -t $SESSION_NAME:0.2 "/init-role [ROLE3]" C-m
tmux send-keys -t $SESSION_NAME:0.2 C-m
tmux send-keys -t $SESSION_NAME:0.3 "/init-role CODE_REVIEWER" C-m
tmux send-keys -t $SESSION_NAME:0.3 C-m

sleep 10

# Get pane IDs and update prompts
PANE_IDS=$(tmux list-panes -t $SESSION_NAME -F "#{pane_id}")
PM_PANE=$(echo "$PANE_IDS" | sed -n '1p')
# ... update prompt files with pane IDs

echo "Setup Complete! Attach: tmux attach -t $SESSION_NAME"
```

## Team Composition

### Core Pattern (Universal)

All teams share these patterns regardless of roles:
- **PM is the Hub** - All communication flows through PM
- **WHITEBOARD** - PM maintains for collaboration and session resumption
- **Git as Progress Tracker** - Commits show real progress
- **Two-Enter Rule** - Tmux messages require two SEPARATE commands
- **10-Step Sprint Workflow** - From idea to delivery
- **Code Review Phase** - Quality gate before completion

### Required Roles (Every Team)

1. **PM (Project Manager)** - Central coordinator
   - Receives ideas from Boss
   - Routes all agent communication
   - Maintains WHITEBOARD and specs
   - Monitors Git progress
   - Verifies work independently

2. **Code Reviewer** - Quality gatekeeper
   - Reviews implementations
   - Validates correctness
   - Provides actionable feedback

3. **BOSS (User/Human)** - Sprint supervisor (OUTSIDE tmux)
   - NOT an automated agent - this is the human user
   - Operates from a **separate terminal outside the tmux session** (Boss Terminal)
   - Provides initial ideas/requirements to PM (before step 1)
   - **DOES NOT intervene during steps 1-10** - team self-coordinates
   - Appears ONLY after step 10 to:
     - Review sprint summary from PM
     - Approve or reject sprint
     - Request external Validator if needed
     - Provide next sprint ideas/priorities
   - Uses `>>>` prefix to send messages to PM (see Boss Terminal section below)

### Example Team Compositions

Teams can have different specialist roles based on the project:

**Example 1: AI Controller Team (sample_team)**
```
PM → SA (Solution Architect) → BE (Backend) → FE (Frontend) → CR → DK
```
- SA: Architecture design, API contracts, guards progressive approach
- BE: Backend implementation (backend/)
- FE: Frontend adaptation (frontend/)
- DK: Documentation sync (docs/)

**Example 2: Full-Stack Web App Team**
```
PM → SA → Frontend Dev → Backend Dev → CR
```

**Example 3: Data Pipeline Team**
```
PM → Data Architect → Data Engineer → CR
```

**Example 4: ML Project Team**
```
PM → ML Researcher → ML Engineer → Data Engineer → CR
```

**Example 5: Mobile App Team**
```
PM → UX Designer → iOS Dev → Android Dev → CR
```

### Designing Your Team

When creating a team:

1. **Always include PM and Code Reviewer** - Universal roles
2. **Identify specialists** - What expertise does the project need?
3. **Define communication flow** - All through PM
4. **Create role prompts** - Specific responsibilities for each role
5. **Keep team size reasonable** - 3-5 agents typically optimal

## Communication Patterns

### Stable Role Names with @role_name (CRITICAL)

**Problem**: Tmux pane titles (`#{pane_title}`) change dynamically when Claude Code runs tasks. For example, "PM" becomes "✳ API Mismatch Bug" based on current task.

**Solution**: Use tmux pane user options (`@role_name`) which are stable and won't be overwritten by running processes.

```bash
# Set stable role names during setup
tmux set-option -p -t $SESSION_NAME:0.0 @role_name "PM"
tmux set-option -p -t $SESSION_NAME:0.1 @role_name "SA"
tmux set-option -p -t $SESSION_NAME:0.2 @role_name "CR"

# Read role name (for APIs, scripts, etc.)
tmux show-option -p -t $SESSION_NAME:0.0 -v @role_name  # Returns: PM
```

**Key Points**:
- `@role_name` is a user-defined pane option (prefix with `@`)
- Set with `tmux set-option -p -t target @role_name "VALUE"`
- Read with `tmux show-option -p -t target -v @role_name`
- Persists for the session lifetime, survives pane title changes
- Fall back to `#{pane_title}` if `@role_name` not set

### Two-Enter Rule (CRITICAL)

All tmux messages require two **SEPARATE** tmux commands:

```bash
# CORRECT: Two separate commands
tmux send-keys -t [pane_id] "PM [HH:mm]: [message]" C-m
tmux send-keys -t [pane_id] C-m   # Second Enter in SEPARATE command!
sleep 5
tmux capture-pane -t [pane_id] -p | tail -40

# WRONG: C-m C-m in single command does NOT work!
tmux send-keys -t [pane_id] "message" C-m C-m  # DON'T DO THIS
```

### Update-Then-Notify Order

Always write/update files FIRST, then notify:

```bash
# 1. Write file (spec, code, etc.)
# 2. THEN notify agent (two separate commands!)
tmux send-keys -t %FE "PM [10:30]: Sprint assigned. See docs/specs/feature.md" C-m
tmux send-keys -t %FE C-m
```

### Message Format

`[ROLE] [HH:mm]: [Brief message]. See [reference].`

Examples:
- `PM [23:11]: Sprint assigned to FE. See docs/specs/feature.md`
- `FE [22:10]: Task complete. Tests: 42/42 passing. See Git commits.`

## 10-Step Sprint Workflow

1. **Ideas → PM**: Boss provides ideas to PM
2. **PM → Expert**: Strategy/design discussion
3. **Expert → PM**: Finalize specification
4. **PM → Implementer**: Sprint assignment with spec
5. **Implementer**: Progressive implementation
6. **Implementer ↔ PM ↔ Expert**: Clarification loop
7. **Continue clarifications as needed**
8. **Implementer → PM**: Sprint completion report
9. **PM → Code Reviewer**: Review request
10. **Review Loop**: Reviewer ↔ PM ↔ Implementer until approved

**Boss appears ONLY after step 10** - team self-coordinates during sprint.

## After Step 10: Boss Entry

When sprint completes (Code Reviewer approves), PM prepares Sprint Summary for Boss.

### Boss Reviews

Boss (human user) evaluates:
- **Sprint Summary** from PM (deliverables, metrics, decisions made)
- **Git commit history** (primary progress measure - shows progressive development)
- **Code Reviewer approval report** (quality gate passed)
- **WHITEBOARD** (current status, any blockers encountered)

### Boss Decisions

After review, Boss can:

1. **Approve Sprint** - Work is complete, merge to main branch
2. **Request Changes** - Send back to team with specific feedback
3. **Request External Validator** - For critical work, get independent verification
4. **Prioritize Next Sprint** - Provide ideas/requirements for next iteration

### Boss Terminal (CRITICAL)

The Boss operates from a **separate terminal outside the tmux session** (typically where a Claude Code instance runs to assist the Boss).

**Communication Protocol**:
- When Boss types `>>> [message]`, the message is sent to PM pane with prefix:
  ```
  BOSS [HH:MM]: [original_message]
  ```
- Example: Boss types `>>> start sprint 1` → PM receives `BOSS [14:30]: start sprint 1`

**Implementation**: Configure in the project's CLAUDE.md:
```markdown
**>>> PREFIX - CRITICAL COMMUNICATION RULE**:
When user types `>>> [message]`, ALWAYS send ONLY to PM (pane %0), NOT to any other agent!
- `>>>` means: Send to PM pane (%0) with prefix "BOSS [HH:mm]: [exact message]"
- DO NOT send to Code-Reviewer, Coder, or anyone else
- PM will relay to appropriate agent if needed
```

**Boss Terminal Commands**:
```bash
# Send message to PM (pane %0)
tmux send-keys -t {session}:0.0 "BOSS [HH:MM]: your message here" C-m
tmux send-keys -t {session}:0.0 C-m  # Two-Enter rule

# View PM pane output
tmux capture-pane -t {session}:0.0 -p | tail -50

# Attach to session (to observe all agents)
tmux attach -t {session}
```

**Boss Responsibilities from Boss Terminal**:
- Provide initial sprint goals to PM via `>>>`
- Run LLM tests manually when notified (if applicable)
- Approve/reject sprint completions
- Can intervene anytime via `>>>` prefix

### Boss Non-Intervention Rule

**CRITICAL**: Boss should NOT intervene during steps 1-10 unless:
- Team is completely stuck (no progress for hours)
- Critical business requirement change
- Emergency situation

Let the team self-coordinate. Trust PM to manage the sprint.

## Sample Team Reference

The `sample_team/` directory contains 6 complete working templates (4 software development + 2 research):

```
sample_team/
├── scrum-team/                      # RECOMMENDED: Full Scrum framework
│   ├── workflow.md        # Scrum workflow documentation
│   ├── WHITEBOARD.md                # Sprint status
│   ├── SPRINT_BACKLOG.md            # Current sprint items
│   ├── PRODUCT_BACKLOG.md           # PO's backlog
│   ├── setup-team.sh                # Automated setup (verifies global tm-send)
│   ├── sm/                          # Scrum Master's workspace
│   │   ├── IMPROVEMENT_BACKLOG.md   # Process issues (with evidence log)
│   │   ├── RETROSPECTIVE_LOG.md     # Historical lessons
│   │   └── ACTION_ITEMS.md          # Improvement tracking
│   └── prompts/
│       ├── PO_PROMPT.md             # Product Owner
│       ├── SM_PROMPT.md             # Scrum Master (4-checkpoint monitoring)
│       ├── TL_PROMPT.md             # Tech Lead
│       ├── BE_PROMPT.md             # Backend Developer
│       ├── FE_PROMPT.md             # Frontend Developer
│       └── QA_PROMPT.md             # Tester (black-box)
│
├── scrum-minimal-team/              # Lightweight 3-person Scrum
│   ├── workflow.md                  # Minimal Scrum workflow
│   ├── WHITEBOARD.md                # Sprint status
│   ├── SPRINT_BACKLOG.md            # Current sprint items
│   ├── PRODUCT_BACKLOG.md           # PO's backlog
│   ├── setup-team.sh                # 3-pane setup
│   ├── sm/                          # Scrum Master's workspace
│   │   ├── IMPROVEMENT_BACKLOG.md   # Process issues
│   │   └── RETROSPECTIVE_LOG.md     # Historical lessons
│   └── prompts/
│       ├── PO_PROMPT.md             # Product Owner
│       ├── SM_PROMPT.md             # Scrum Master
│       └── EX_PROMPT.md             # Executive (TL+DEV+QA)
│
├── game-dev-team/                   # Game development team
│   ├── workflow.md        # BMGD + Scrum workflow
│   ├── WHITEBOARD.md                # Sprint status
│   ├── setup-team.sh                # Automated setup (sets @role_name on panes)
│   ├── sm/                          # SM's workspace
│   │   ├── IMPROVEMENT_BACKLOG.md   # Process issues
│   │   └── RETROSPECTIVE_LOG.md     # Historical lessons
│   └── prompts/
│       ├── DS_PROMPT.md             # Game Designer
│       ├── SM_PROMPT.md             # Scrum Master
│       ├── AR_PROMPT.md             # Game Architect
│       ├── DV_PROMPT.md             # Game Developer
│       └── QA_PROMPT.md             # Game QA
│
├── mckinsey-research-team/          # McKinsey-style research
│   ├── workflow.md        # 7-step McKinsey workflow
│   ├── WHITEBOARD.md                # Engagement status
│   ├── setup-team.sh                # Automated setup (verifies global tm-send)
│   ├── em/                          # Engagement Manager's workspace
│   │   ├── IMPROVEMENT_BACKLOG.md   # Process issues (with evidence log)
│   │   ├── RETROSPECTIVE_LOG.md     # Historical lessons
│   │   └── ACTION_ITEMS.md          # Improvement tracking
│   └── prompts/
│       ├── EM_PROMPT.md             # Engagement Manager (coordinator)
│       ├── RL_PROMPT.md             # Research Lead (MECE, synthesis)
│       ├── PR_PROMPT.md             # Primary Researcher (interviews)
│       ├── SR_PROMPT.md             # Secondary Researcher (desk research)
│       ├── DA_PROMPT.md             # Data Analyst (market sizing)
│       └── QR_PROMPT.md             # Quality Reviewer (MECE, Pyramid)
│
├── pg-insights-team/                # P&G-style consumer insights
│   ├── workflow.md        # Three-Step Formula workflow
│   ├── WHITEBOARD.md                # Project status
│   ├── setup-team.sh                # Automated setup (verifies global tm-send)
│   ├── im/                          # Insights Manager's workspace
│   │   ├── IMPROVEMENT_BACKLOG.md   # Process issues (with evidence log)
│   │   ├── RETROSPECTIVE_LOG.md     # Historical lessons
│   │   └── ACTION_ITEMS.md          # Improvement tracking
│   └── prompts/
│       ├── IM_PROMPT.md             # Insights Manager (coordinator)
│       ├── MR_PROMPT.md             # Moments Researcher (Step 1)
│       ├── IA_PROMPT.md             # Insight Analyst (Step 2)
│       ├── SL_PROMPT.md             # Strategy Lead (Step 3)
│       └── QR_PROMPT.md             # Quality Reviewer (goosebumps test)
│
├── commands/
│   └── init-role.md                 # Slash command for role init
├── hooks/
│   └── session_start_team_docs.py   # SessionStart hook template (CRITICAL)
└── settings.json                    # Hook configuration template

# NOTE: tm-send is a GLOBAL tool at ~/.local/bin/tm-send
# It is NOT included in project directories
# Role mapping uses @role_name pane options (dynamic, no static file)
```

### Key Differences Between Templates

#### Software Development Teams

| Feature | scrum-team | scrum-minimal-team | game-dev-team |
|---------|------------|-------------------|---------------|
| Roles | 6 (PO, SM, TL, BE, FE, QA) | 3 (PO, SM, EX) | 5 (DS, SM, AR, DV, QA) |
| Improvement Owner | SM | SM | SM |
| Workflow | Sprint-based | Sprint-based | Design→Arch→Impl→Test |
| Monitoring | 4 checkpoints + evidence log | Lightweight | Sprint-based improvement |
| QA Approach | Black-box (QA role) | Integrated (EX role) | Automated tests + playtests |
| Backlog | Product + Sprint | Product + Sprint | WHITEBOARD |
| Best For | Large projects | Small/solo projects | Game development |

#### Research Teams

| Feature | mckinsey-research-team | pg-insights-team |
|---------|----------------------|------------------|
| Improvement Owner | EM (Engagement Manager) | IM (Insights Manager) |
| Workflow | McKinsey 7-step | P&G Three-Step |
| Monitoring | 4 checkpoints + evidence log | 4 checkpoints + evidence log |
| QA Approach | MECE + Pyramid Principle (QR) | Goosebumps test + validation (QR) |
| Backlog | WHITEBOARD | WHITEBOARD |
| Retrospective | Engagement end | Project end |
| Unique Features | Hypothesis-driven, triangulation, issue trees | Human-centric, logic+emotion, everyday moments |

### tm-send Script (GLOBAL TOOL)

The `tm-send` script is CRITICAL for reliable agent communication.

**IMPORTANT: tm-send is a GLOBAL tool, NOT project-specific!**
- Installed once at `~/.local/bin/tm-send`
- Works for ALL projects on the machine
- Uses tmux `@role_name` pane options (dynamic lookup, no static files)
- **DO NOT copy tm-send into project directories**

**Features:**
- **Dynamic Role Lookup** - Queries `@role_name` pane options directly via tmux
- **Session Isolation** - Prevents cross-team message contamination
- **Auto-detect Session** - From TMUX env, project directory, or `-s` flag
- **Two-Enter Rule** - Enforced automatically

**Usage:**
```bash
tm-send PM "FE -> PM: Task complete."           # Auto-detect session
tm-send -s other_project PM "Cross-project msg"  # Explicit session
tm-send --list                                   # List roles in session
```

**Session Isolation Details**:
- Pane IDs (like `%109`) can exist in multiple sessions
- `tm-send` verifies pane belongs to correct session before sending
- Never sends to wrong project

**Never use raw `tmux send-keys`** - always use `tm-send` for agent communication.

**Pre-requisite**: tm-send must be installed globally at `~/.local/bin/tm-send` before running any team setup script.

Read the sample_team files to understand the complete structure before customizing for user's domain.

## Best Practices

1. **Keep PM as hub** - Never allow direct agent-to-agent communication
2. **Use WHITEBOARD** - Critical for session resumption after restarts
3. **Git is truth** - Monitor commits, not chat messages
4. **Progressive implementation** - Small incremental steps
5. **Verify independently** - PM should run tests, not just trust reports
6. **Two-Enter rule** - Always use two SEPARATE tmux commands for messages
7. **Update-Then-Notify** - Write files before sending notifications
8. **Use @role_name** - Set stable role names via `tmux set-option -p @role_name` (pane titles change dynamically)
9. **Session Isolation** - Always use `tm-send` which enforces `session:pane` format to prevent cross-team message contamination when running multiple teams

## Available Skills for Agents

Agents can invoke standard skills for specialized tasks. **Include these in role prompts where applicable.**

### Frontend Roles (FE)

```bash
/frontend-design [description]
```

**Use for:** Interface layout, web components, dashboards, styling, accessibility, high-quality visual design.

**Add to FE prompts:**
```markdown
## UI/UX Design Support

**When working on UI/UX design decisions**, invoke the `/frontend-design` skill:

\`\`\`bash
/frontend-design [description of what you need]
\`\`\`

**Use for:**
- Interface layout decisions
- Web components, pages, dashboards
- Styling and beautifying UI
- Accessibility concerns
- High-quality visual design
```

### Research Roles (PR, SR)

```bash
/quick-research [topic]
```

**Use for:** Complex research requiring multiple sources, comparative analyses, deep exploration.

### Documentation Roles (DK)

```bash
/doc-coauthoring
```

**Use for:** Structured workflow for co-authoring documentation, proposals, technical specs.

### All Roles

```bash
/think-hard [problem]
```

**Use for:** Complex problems requiring deep reasoning.

## Customization Guide

To create a team for a new domain:

1. **Select template** based on user's needs (see "FIRST: Ask User Which Team Template")
2. **Read selected template** to understand the structure
3. **Identify roles** needed for the domain (keep PM/SM and CR/QA)
4. **Copy and rename** files from selected template
5. **Update paths** in all files to match user's project
6. **Customize prompts** with domain-specific responsibilities
7. **Create setup script** with correct role names
8. **Test communication** with two-Enter pattern
9. **Verify improvement docs** (if using scrum-team or pm-retro)

### Template Selection Quick Reference

#### Software Development

| User Says | Use Template |
|-----------|--------------|
| "Scrum team" / "standard Scrum" / "Scrum Master" | `scrum-team` |
| "minimal" / "small team" / "solo dev" / "MVP" / "lightweight" | `scrum-minimal-team` |
| "game" / "game development" / "game project" | `game-dev-team` |
| Nothing specified (software dev) | Ask, recommend `scrum-team` (or `scrum-minimal-team` for small projects) |

#### Research & Analysis

| User Says | Use Template |
|-----------|--------------|
| "market research" / "competitive analysis" / "McKinsey" | `mckinsey-research-team` |
| "industry analysis" / "due diligence" / "research team" | `mckinsey-research-team` |
| "consumer insights" / "P&G" / "brand strategy" | `pg-insights-team` |
| "emotional research" / "product innovation" | `pg-insights-team` |

#### Cross-Domain

When user's project spans multiple domains, consider:
- Combining elements from multiple templates
- Creating custom roles that blend responsibilities
- Using the closest template as a starting point and customizing heavily
