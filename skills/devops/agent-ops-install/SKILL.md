---
name: agent-ops-install
description: "Install AgentOps into a new or existing project. Handles .agent/ setup and .github/ merging."
category: setup
invokes: [agent-ops-interview]
invoked_by: []
state_files:
  read: []
  write: [constitution.md, memory.md, focus.md, baseline.md, issues/*.md]
---

# AgentOps Installation

## Purpose
Install the AgentOps framework into any project—new or existing—with intelligent merging.

## Installation Modes

### Mode 1: Fresh Install (empty or new folder)
Creates full structure from scratch.

### Mode 2: Merge Install (existing .github/)
Preserves existing content, adds AgentOps alongside it.

### Mode 3: Update Install (existing AgentOps)
Updates skills/prompts to latest versions without touching state files.

---

## Pre-Installation Checklist

Before installing, gather:

1. **Project type** — What language/framework? (affects gitignore suggestions)
2. **Existing CI/CD** — Any workflows in .github/workflows/?
3. **Existing instructions** — Is there a copilot-instructions.md?
4. **Git status** — Is this a git repo? Any uncommitted changes?

---

## Installation Structure

### .agent/ (State - Created Fresh)

```
.agent/
├── constitution.md      # Project-specific rules (from template)
├── memory.md            # Empty, grows over time
├── focus.md             # Empty, session state
├── baseline.md          # Empty, captured on first baseline
├── docs/                # Agent-generated documentation
├── issues/
│   ├── critical.md      # P0 issues
│   ├── high.md          # P1 issues
│   ├── medium.md        # P2 issues
│   ├── low.md           # P3 issues
│   ├── history.md       # Archived issues
│   ├── references/      # Detailed specs for complex issues
│   │   └── README.md
│   └── .counter         # Issue ID counter (starts at 0)
└── specs/               # Requirement specifications
```

### .github/ (Framework - Merged)

```
.github/
├── copilot-instructions.md   # MERGE with existing or create
├── SKILL-TIERS.md            # Skill hierarchy reference
├── skills/                   # All AgentOps skills
│   ├── agent-ops-baseline/
│   ├── agent-ops-constitution/
│   ├── agent-ops-critical-review/
│   ├── agent-ops-dependencies/
│   ├── agent-ops-docs/
│   ├── agent-ops-focus-scan/
│   ├── agent-ops-git/
│   ├── agent-ops-guide/
│   ├── agent-ops-housekeeping/
│   ├── agent-ops-implementation/
│   ├── agent-ops-improvement-discovery/
│   ├── agent-ops-install/
│   ├── agent-ops-interview/
│   ├── agent-ops-planning/
│   ├── agent-ops-recovery/
│   ├── agent-ops-retrospective/
│   ├── agent-ops-spec/
│   ├── agent-ops-state/
│   ├── agent-ops-tasks/
│   ├── agent-ops-testing/
│   └── agent-ops-validation/
├── prompts/                  # Prompt files (additive)
│   ├── agent-*.prompt.md
│   └── ... 
├── agents/                   # Agent definitions
│   └── AgentOps.md
└── reference/                # Reference documents
    ├── api-guidelines.md
    ├── cautious-reasoning.md
    └── code-review-framework.md
```

---

## Merge Strategy for copilot-instructions.md

### If NO existing file:
Create from AgentOps template.

### If existing file WITHOUT AgentOps:
```markdown
# Original content preserved above

---

# AgentOps Protocol (appended)

[AgentOps instructions here]
```

### If existing file WITH older AgentOps:
Replace AgentOps section only, preserve user customizations above the `---` separator.

---

## Installation Procedure

### Step 1: Detect Environment
```
□ Check if .agent/ exists
□ Check if .github/ exists  
□ Check if copilot-instructions.md exists
□ Check if git repository
□ Identify project type (package.json, pyproject.toml, etc.)
```

### Step 2: Report & Confirm
```
📦 AgentOps Installation

Target: /path/to/project
Mode: [Fresh | Merge | Update]

Will create:
  ✚ .agent/ (full structure)
  ✚ .github/skills/ (21 skills)
  ✚ .github/prompts/ (17 prompts)
  ✚ .github/agents/AgentOps.md
  ✚ .github/reference/ (3 docs)

Will merge:
  ⊕ .github/copilot-instructions.md (append AgentOps section)

Will preserve:
  ○ .github/workflows/ (untouched)
  ○ .github/CODEOWNERS (untouched)
  ○ Existing prompts with same names (skip)

Proceed? [Y/n]
```

### Step 3: Create .agent/ Structure
Always created fresh (never merge state files).

### Step 4: Copy/Merge .github/ Content
- Skills: Copy all (overwrite if updating)
- Prompts: Copy new only (skip existing with same name)
- Agents: Copy AgentOps.md
- Reference: Copy all
- Instructions: Merge per strategy above

### Step 5: Post-Install Setup
```
□ Run initial constitution interview (optional)
□ Capture baseline (optional)
□ Add .agent/ paths to .gitignore if desired
□ Create initial focus.md entry
```

### Step 6: Verify Installation
```
□ All required files exist
□ copilot-instructions.md valid
□ Skills readable
□ Report success
```

---

## Invocation

### Interactive (recommended for first install)
```
/agent-install
```
Walks through options, asks questions, confirms before acting.

### Quick Install (defaults)
```
/agent-install --quick
```
Uses defaults, minimal prompts, good for experienced users.

### Update Only
```
/agent-install --update
```
Updates skills/prompts/references only, doesn't touch .agent/ state.

### Dry Run
```
/agent-install --dry-run
```
Shows what would be created/modified without making changes.

---

## Gitignore Recommendations

Suggest adding to .gitignore:

```gitignore
# AgentOps state (optional - some teams prefer to track)
# .agent/

# Always ignore (contains sensitive session data)
.agent/focus.md
.agent/baseline.md

# Or track everything for team visibility:
# (no ignores)
```

**Decision factors:**
- Solo project → ignore .agent/ (personal state)
- Team project → track .agent/ (shared context)
- Open source → ignore .agent/ (contributor-specific)

---

## Uninstall

To remove AgentOps:
```
□ Delete .agent/ folder
□ Delete .github/skills/agent-ops-*/ folders
□ Delete .github/prompts/agent-*.prompt.md files
□ Delete .github/agents/AgentOps.md
□ Delete .github/reference/ folder
□ Remove AgentOps section from copilot-instructions.md
□ Delete .github/SKILL-TIERS.md
```

---

## Troubleshooting

### "Skills not loading"
- Check copilot-instructions.md has skill references
- Verify skill files have correct frontmatter
- Restart VS Code / Copilot

### "Prompts not appearing"
- Prompts need `.prompt.md` extension
- Check prompts are in `.github/prompts/`
- Verify frontmatter format

### "Agent mode not available"
- Check `.github/agents/AgentOps.md` exists
- Verify VS Code Copilot Chat extension is current
- Agent mode may need enabling in settings
