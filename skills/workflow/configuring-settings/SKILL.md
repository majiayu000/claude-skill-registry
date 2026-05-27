---
name: configuring-settings
description: Use this skill when configure kata workflow toggles and model profile. Triggers include "settings".
metadata:
  version: "0.1.0"
user-invocable: false
disable-model-invocation: false
allowed-tools:
  - Read
  - Write
  - Bash
---

<user_command>/kata:configure-settings</user_command>


<objective>
Allow users to toggle workflow agents on/off and select model profile via interactive settings.

Updates `.planning/config.json` with workflow preferences and model profile selection.

**Handles missing config keys:** If config.json is missing any expected keys (e.g., `pr_workflow`, `commit_docs`), prompts user for preferences and adds them.
</objective>

<process>

## 1. Validate Environment

```bash
ls .planning/config.json 2>/dev/null
```

**If not found:** Error - run `/kata:new-project` first.

## 2. Read Current Config and Detect Missing Keys

```bash
cat .planning/config.json
```

Parse current values with defaults:
- `mode` — yolo or interactive (default: `yolo`)
- `depth` — quick, standard, or comprehensive (default: `standard`)
- `parallelization` — run agents in parallel (default: `true`)
- `model_profile` — which model each agent uses (default: `balanced`)
- `commit_docs` — commit planning artifacts to git (default: `true`)
- `pr_workflow` — use PR-based release workflow (default: `false`)
- `display.statusline` — show Kata statusline (default: `true`)
- `workflow.research` — spawn researcher during phase-plan (default: `true`)
- `workflow.plan_check` — spawn plan checker during phase-plan (default: `true`)
- `workflow.verifier` — spawn verifier during phase-execute (default: `true`)

**Detect missing keys:**

Check if these keys exist in config.json:
- `commit_docs`
- `pr_workflow`
- `display.statusline`

If any are missing, note them for step 3.

## 3. Present Settings (Including New Options)

**If missing keys were detected:**

Display notification:
```
⚠️  New config options available: {list missing keys}
   Adding these to your settings...
```

Use AskUserQuestion with current values shown:

```
AskUserQuestion([
  {
    question: "Which model profile for agents?",
    header: "Model",
    multiSelect: false,
    options: [
      { label: "Quality", description: "Opus everywhere except verification (highest cost)" },
      { label: "Balanced (Recommended)", description: "Opus for planning, Sonnet for execution/verification" },
      { label: "Budget", description: "Sonnet for writing, Haiku for research/verification (lowest cost)" }
    ]
  },
  {
    question: "Commit planning docs to git?",
    header: "Commit Docs",
    multiSelect: false,
    options: [
      { label: "Yes (Recommended)", description: "Track planning artifacts in git history" },
      { label: "No", description: "Keep planning private (add .planning/ to .gitignore)" }
    ]
  },
  {
    question: "Use PR-based release workflow?",
    header: "PR Workflow",
    multiSelect: false,
    options: [
      { label: "Yes (Recommended)", description: "Protect main, create PRs, tag via GitHub Release" },
      { label: "No", description: "Commit directly to main, create tags locally" }
    ]
  },
  {
    question: "Spawn Plan Researcher? (researches domain before planning)",
    header: "Research",
    multiSelect: false,
    options: [
      { label: "Yes", description: "Research phase goals before planning" },
      { label: "No", description: "Skip research, plan directly" }
    ]
  },
  {
    question: "Spawn Plan Checker? (verifies plans before execution)",
    header: "Plan Check",
    multiSelect: false,
    options: [
      { label: "Yes", description: "Verify plans meet phase goals" },
      { label: "No", description: "Skip plan verification" }
    ]
  },
  {
    question: "Spawn Execution Verifier? (verifies phase completion)",
    header: "Verifier",
    multiSelect: false,
    options: [
      { label: "Yes", description: "Verify must-haves after execution" },
      { label: "No", description: "Skip post-execution verification" }
    ]
  },
  {
    question: "Enable Kata statusline?",
    header: "Statusline",
    multiSelect: false,
    options: [
      { label: "Yes (Recommended)", description: "Show model, context usage, update status in statusline" },
      { label: "No", description: "Use default Claude Code statusline" }
    ]
  }
])
```

**Pre-select based on current config values (use defaults for missing keys).**

## 4. Update Config

Merge new settings into existing config.json (preserving existing keys like `mode`, `depth`, `parallelization`):

```json
{
  "mode": "yolo|interactive",
  "depth": "quick|standard|comprehensive",
  "parallelization": true|false,
  "model_profile": "quality|balanced|budget",
  "commit_docs": true|false,
  "pr_workflow": true|false,
  "display": {
    "statusline": true|false
  },
  "workflow": {
    "research": true|false,
    "plan_check": true|false,
    "verifier": true|false
  }
}
```

Write updated config to `.planning/config.json`.

**If `display.statusline` changed to `true`:**

Update `.claude/settings.json` with statusline configuration:

```bash
# Ensure .claude directory exists
mkdir -p .claude

# Check if settings.json exists and has statusLine
if [ -f .claude/settings.json ]; then
  # Check if statusLine already configured
  if grep -q '"statusLine"' .claude/settings.json; then
    echo "Statusline already configured in .claude/settings.json"
  else
    # Add statusLine to existing settings using node
    node -e "
      const fs = require('fs');
      const settings = JSON.parse(fs.readFileSync('.claude/settings.json', 'utf8'));
      settings.statusLine = {
        type: 'command',
        command: 'node \"\$CLAUDE_PROJECT_DIR/.claude/hooks/kata-statusline.js\"'
      };
      fs.writeFileSync('.claude/settings.json', JSON.stringify(settings, null, 2));
    "
    echo "✓ Statusline enabled in .claude/settings.json"
  fi
else
  # Create new settings.json with statusLine
  cat > .claude/settings.json << 'SETTINGS_EOF'
{
  "statusLine": {
    "type": "command",
    "command": "node \"$CLAUDE_PROJECT_DIR/.claude/hooks/kata-statusline.js\""
  }
}
SETTINGS_EOF
  echo "✓ Created .claude/settings.json with statusline"
fi
```

The statusline hook will be automatically installed on next session start by Kata's SessionStart hook.

**If `display.statusline` changed to `false`:**

Remove statusline from `.claude/settings.json`:

```bash
if [ -f .claude/settings.json ]; then
  node -e "
    const fs = require('fs');
    const settings = JSON.parse(fs.readFileSync('.claude/settings.json', 'utf8'));
    delete settings.statusLine;
    fs.writeFileSync('.claude/settings.json', JSON.stringify(settings, null, 2));
  "
  echo "✓ Statusline disabled in .claude/settings.json"
fi
```

**If `commit_docs` changed to `false`:**
- Add `.planning/` to `.gitignore` (create if needed)
- Note: User should run `git rm -r --cached .planning/` if already tracked

## 5. Confirm Changes

Display:


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 Kata ► SETTINGS UPDATED
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

| Setting            | Value                     |
| ------------------ | ------------------------- |
| Model Profile      | {quality/balanced/budget} |
| Commit Docs        | {On/Off}                  |
| PR Workflow        | {On/Off}                  |
| Statusline         | {On/Off}                  |
| Plan Researcher    | {On/Off}                  |
| Plan Checker       | {On/Off}                  |
| Execution Verifier | {On/Off}                  |

These settings apply to future /kata:plan-phase and /kata:execute-phase runs.

Quick commands:
- /kata:set-profile <profile> — switch model profile
- /kata:plan-phase --research — force research
- /kata:plan-phase --skip-research — skip research
- /kata:plan-phase --skip-verify — skip plan check


</process>

<success_criteria>
- [ ] Current config read
- [ ] Missing keys detected and user notified
- [ ] User presented with 7 settings (profile + commit_docs + pr_workflow + statusline + 3 toggles)
- [ ] Config updated with complete schema
- [ ] .claude/settings.json updated if statusline toggled
- [ ] Changes confirmed to user
</success_criteria>
