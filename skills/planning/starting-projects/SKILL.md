---
name: starting-projects
description: Use this skill when initialize a new project with deep context gathering and project.md. Triggers include "new project", "start project", "initialize project", "create project", "begin project", "setup project".
metadata:
  version: "0.1.0"
user-invocable: false
disable-model-invocation: false
allowed-tools:
  - Read
  - Bash
  - Write
  - Task
  - AskUserQuestion
---

<user_command>/kata:new-project</user_command>


<objective>

Initialize a new project with deep context gathering and workflow configuration.

This is the most leveraged moment in any project. Deep questioning here means better plans, better execution, better outcomes.

**Creates:**
- `.planning/PROJECT.md` — project context
- `.planning/config.json` — workflow preferences

**After this command:** Run `/kata:add-milestone` to define your first milestone.

</objective>

<execution_context>

@./references/questioning.md
@./references/ui-brand.md
@./references/project-template.md

</execution_context>

<process>

## Phase 1: Setup

**MANDATORY FIRST STEP — Execute these checks before ANY user interaction:**

1. **Abort if project exists:**
   ```bash
   [ -f .planning/PROJECT.md ] && echo "ERROR: Project already initialized. Use /kata:check-progress" && exit 1
   ```

2. **Initialize git repo in THIS directory** (required even if inside a parent repo):
   ```bash
   if [ -d .git ] || [ -f .git ]; then
       echo "Git repo exists in current directory"
   else
       git init
       echo "Initialized new git repo"
   fi
   ```

3. **Detect existing code (brownfield detection):**
   ```bash
   CODE_FILES=$(find . -name "*.ts" -o -name "*.js" -o -name "*.py" -o -name "*.go" -o -name "*.rs" -o -name "*.swift" -o -name "*.java" 2>/dev/null | grep -v node_modules | grep -v .git | head -20)
   HAS_PACKAGE=$([ -f package.json ] || [ -f requirements.txt ] || [ -f Cargo.toml ] || [ -f go.mod ] || [ -f Package.swift ] && echo "yes")
   HAS_CODEBASE_MAP=$([ -d .planning/codebase ] && echo "yes")
   ```

   **You MUST run all bash commands above using the Bash tool before proceeding.**

## Phase 2: Brownfield Offer

**If existing code detected and .planning/codebase/ doesn't exist:**

Check the results from setup step:
- If `CODE_FILES` is non-empty OR `HAS_PACKAGE` is "yes"
- AND `HAS_CODEBASE_MAP` is NOT "yes"

Use AskUserQuestion:
- header: "Existing Code"
- question: "I detected existing code in this directory. Would you like to map the codebase first?"
- options:
  - "Map codebase first" — Run /kata:map-codebase to understand existing architecture (Recommended)
  - "Skip mapping" — Proceed with project initialization

**If "Map codebase first":**
```
Run `/kata:map-codebase` first, then return to `/kata:new-project`
```
Exit command.

**If "Skip mapping":** Continue to Phase 3.

**If no existing code detected OR codebase already mapped:** Continue to Phase 3.

## Phase 3: Deep Questioning

**Display stage banner:**


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 Kata ► QUESTIONING
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


**Open the conversation:**

Ask inline (freeform, NOT AskUserQuestion):

"What do you want to build?"

Wait for their response. This gives you the context needed to ask intelligent follow-up questions.

**Follow the thread:**

Based on what they said, ask follow-up questions that dig into their response. Use AskUserQuestion with options that probe what they mentioned — interpretations, clarifications, concrete examples.

Keep following threads. Each answer opens new threads to explore. Ask about:
- What excited them
- What problem sparked this
- What they mean by vague terms
- What it would actually look like
- What's already decided

Consult `questioning.md` for techniques:
- Challenge vagueness
- Make abstract concrete
- Surface assumptions
- Find edges
- Reveal motivation

**Check context (background, not out loud):**

As you go, mentally check the context checklist from `questioning.md`. If gaps remain, weave questions naturally. Don't suddenly switch to checklist mode.

**Decision gate:**

When you could write a clear PROJECT.md, use AskUserQuestion:

- header: "Ready?"
- question: "I think I understand what you're after. Ready to create PROJECT.md?"
- options:
  - "Create PROJECT.md" — Let's move forward
  - "Keep exploring" — I want to share more / ask me more

If "Keep exploring" — ask what they want to add, or identify gaps and probe naturally.

Loop until "Create PROJECT.md" selected.

## Phase 4: Write PROJECT.md

Synthesize all context into `.planning/PROJECT.md` using the template from `@./references/project-template.md`.

**For greenfield projects:**

Initialize requirements as hypotheses:

```markdown
## Requirements

### Validated

(None yet — ship to validate)

### Active

- [ ] [Requirement 1]
- [ ] [Requirement 2]
- [ ] [Requirement 3]

### Out of Scope

- [Exclusion 1] — [why]
- [Exclusion 2] — [why]
```

All Active requirements are hypotheses until shipped and validated.

**For brownfield projects (codebase map exists):**

Infer Validated requirements from existing code:

1. Read `.planning/codebase/ARCHITECTURE.md` and `STACK.md`
2. Identify what the codebase already does
3. These become the initial Validated set

```markdown
## Requirements

### Validated

- ✓ [Existing capability 1] — existing
- ✓ [Existing capability 2] — existing
- ✓ [Existing capability 3] — existing

### Active

- [ ] [New requirement 1]
- [ ] [New requirement 2]

### Out of Scope

- [Exclusion 1] — [why]
```

**Key Decisions:**

Initialize with any decisions made during questioning:

```markdown
## Key Decisions

| Decision                  | Rationale | Outcome   |
| ------------------------- | --------- | --------- |
| [Choice from questioning] | [Why]     | — Pending |
```

**Last updated footer:**

```markdown
---
*Last updated: [date] after initialization*
```

Do not compress. Capture everything gathered.

**Commit PROJECT.md:**

```bash
mkdir -p .planning
git add .planning/PROJECT.md
git commit -m "$(cat <<'EOF'
docs: initialize project

[One-liner from PROJECT.md What This Is section]
EOF
)"
```

## Phase 5: Workflow Preferences

**Round 1 — Core workflow settings (4 questions):**

```
questions: [
  {
    header: "Mode",
    question: "How do you want to work?",
    multiSelect: false,
    options: [
      { label: "YOLO (Recommended)", description: "Auto-approve, just execute" },
      { label: "Interactive", description: "Confirm at each step" }
    ]
  },
  {
    header: "Depth",
    question: "How thorough should planning be?",
    multiSelect: false,
    options: [
      { label: "Quick", description: "Ship fast (3-5 phases, 1-3 plans each)" },
      { label: "Standard", description: "Balanced scope and speed (5-8 phases, 3-5 plans each)" },
      { label: "Comprehensive", description: "Thorough coverage (8-12 phases, 5-10 plans each)" }
    ]
  },
  {
    header: "Execution",
    question: "Run plans in parallel?",
    multiSelect: false,
    options: [
      { label: "Parallel (Recommended)", description: "Independent plans run simultaneously" },
      { label: "Sequential", description: "One plan at a time" }
    ]
  },
  {
    header: "Git Tracking",
    question: "Commit planning docs to git?",
    multiSelect: false,
    options: [
      { label: "Yes (Recommended)", description: "Planning docs tracked in version control" },
      { label: "No", description: "Keep .planning/ local-only (add to .gitignore)" }
    ]
  },
  {
    header: "PR Workflow",
    question: "Use PR-based release workflow?",
    multiSelect: false,
    options: [
      { label: "Yes (Recommended)", description: "Protect main, create PRs, tag via GitHub Release" },
      { label: "No", description: "Commit directly to main, create tags locally" }
    ]
  },
  {
    header: "GitHub Tracking",
    question: "Enable GitHub Milestone/Issue tracking?",
    multiSelect: false,
    options: [
      { label: "Yes (Recommended)", description: "Create GitHub Milestones for Kata milestones, optionally create Issues for phases" },
      { label: "No", description: "Keep planning local to .planning/ directory only" }
    ]
  }
]

# If GitHub Tracking = Yes, ask follow-up:
{
  header: "Issue Creation",
  question: "When should GitHub Issues be created for phases?",
  multiSelect: false,
  options: [
    { label: "Auto", description: "Create Issues automatically for each phase (no prompting)" },
    { label: "Ask per milestone", description: "Prompt once per milestone, decision applies to all phases" },
    { label: "Never", description: "Only create Milestones, no phase-level Issues" }
  ]
}
```

**GitHub Repository Check (conditional):**

**If GitHub Tracking = Yes:**

After confirming GitHub preferences, check for existing remote:

```bash
# Check if gh CLI is authenticated
GH_AUTH=$(gh auth status &>/dev/null && echo "true" || echo "false")

# Check for GitHub remote
HAS_GITHUB_REMOTE=$(git remote -v 2>/dev/null | grep -q 'github\.com' && echo "true" || echo "false")
```

**If `HAS_GITHUB_REMOTE=false` and user selected GitHub Tracking = Yes:**

Use AskUserQuestion:
- header: "GitHub Repository"
- question: "GitHub tracking enabled, but no GitHub repository is linked. Create one now?"
- options:
  - "Create public repo" — Run `gh repo create --source=. --public --push`
  - "Create private repo" — Run `gh repo create --source=. --private --push`
  - "Skip for now" — Disable GitHub tracking (can enable later with `gh repo create`)

**If "Create public repo":**
```bash
if [ "$GH_AUTH" = "true" ]; then
  gh repo create --source=. --public --push && echo "GitHub repository created" || echo "Warning: Failed to create repository"
else
  echo "Warning: GitHub CLI not authenticated. Run 'gh auth login' first, then 'gh repo create --source=. --public --push'"
fi
```
Continue with `github.enabled: true`.

**If "Create private repo":**
```bash
if [ "$GH_AUTH" = "true" ]; then
  gh repo create --source=. --private --push && echo "GitHub repository created" || echo "Warning: Failed to create repository"
else
  echo "Warning: GitHub CLI not authenticated. Run 'gh auth login' first, then 'gh repo create --source=. --private --push'"
fi
```
Continue with `github.enabled: true`.

**If "Skip for now":**
- Set `github.enabled: false` in config.json (override user's earlier selection)
- Display note: "GitHub tracking disabled — no repository configured. Run `gh repo create --source=. --public` to enable later, then update `.planning/config.json`."

**If `HAS_GITHUB_REMOTE=true`:**
- Proceed normally with user's GitHub preferences
- No additional prompts needed

**Round 2 — Workflow agents:**

These spawn additional agents during planning/execution. They add tokens and time but improve quality.

| Agent            | When it runs               | What it does                                          |
| ---------------- | -------------------------- | ----------------------------------------------------- |
| **Researcher**   | Before planning each phase | Investigates domain, finds patterns, surfaces gotchas |
| **Plan Checker** | After plan is created      | Verifies plan actually achieves the phase goal        |
| **Verifier**     | After phase execution      | Confirms must-haves were delivered                    |

All recommended for important projects. Skip for quick experiments.

```
questions: [
  {
    header: "Research",
    question: "Research before planning each phase? (adds tokens/time)",
    multiSelect: false,
    options: [
      { label: "Yes (Recommended)", description: "Investigate domain, find patterns, surface gotchas" },
      { label: "No", description: "Plan directly from requirements" }
    ]
  },
  {
    header: "Plan Check",
    question: "Verify plans will achieve their goals? (adds tokens/time)",
    multiSelect: false,
    options: [
      { label: "Yes (Recommended)", description: "Catch gaps before execution starts" },
      { label: "No", description: "Execute plans without verification" }
    ]
  },
  {
    header: "Verifier",
    question: "Verify work satisfies requirements after each phase? (adds tokens/time)",
    multiSelect: false,
    options: [
      { label: "Yes (Recommended)", description: "Confirm deliverables match phase goals" },
      { label: "No", description: "Trust execution, skip verification" }
    ]
  },
  {
    header: "Model Profile",
    question: "Which AI models for planning agents?",
    multiSelect: false,
    options: [
      { label: "Balanced (Recommended)", description: "Sonnet for most agents — good quality/cost ratio" },
      { label: "Quality", description: "Opus for research/roadmap — higher cost, deeper analysis" },
      { label: "Budget", description: "Haiku where possible — fastest, lowest cost" }
    ]
  },
  {
    header: "Statusline",
    question: "Enable Kata statusline? (shows model, context usage, update status)",
    multiSelect: false,
    options: [
      { label: "Yes (Recommended)", description: "Display live session info in Claude Code statusline" },
      { label: "No", description: "Use default Claude Code statusline" }
    ]
  }
]
```

Create `.planning/config.json` with all settings:

```json
{
  "mode": "yolo|interactive",
  "depth": "quick|standard|comprehensive",
  "parallelization": true|false,
  "commit_docs": true|false,
  "pr_workflow": true|false,
  "model_profile": "quality|balanced|budget",
  "display": {
    "statusline": true|false
  },
  "workflow": {
    "research": true|false,
    "plan_check": true|false,
    "verifier": true|false
  },
  "github": {
    "enabled": true|false,
    "issueMode": "auto|ask|never"
  }
}
```

**GitHub Tracking conditional logic:**

**If GitHub Tracking = Yes:**
- Ask the Issue Creation follow-up question
- Check for GitHub remote (see GitHub Repository Check above)
- Set `github.enabled` based on final state (true if remote exists or was created, false if skipped)
- Set `github.issueMode` based on Issue Creation choice:
  - "Auto" → `"auto"`
  - "Ask per milestone" → `"ask"`
  - "Never" → `"never"`
- Display note based on outcome:
  - If remote exists/created: "GitHub integration enabled. Milestones will be created via `gh` CLI."
  - If skipped: "GitHub tracking disabled — no repository configured."

**If GitHub Tracking = No:**
- Skip the Issue Creation question
- Skip the GitHub Repository Check
- Set `github.enabled: false`
- Set `github.issueMode: "never"`

**If commit_docs = No:**
- Set `commit_docs: false` in config.json
- Add `.planning/` to `.gitignore` (create if needed)

**If commit_docs = Yes:**
- No additional gitignore entries needed

**Commit config.json:**

```bash
git add .planning/config.json
git commit -m "$(cat <<'EOF'
chore: add project config

Mode: [chosen mode]
Depth: [chosen depth]
Parallelization: [enabled/disabled]
Workflow agents: research=[on/off], plan_check=[on/off], verifier=[on/off]
EOF
)"
```

**Note:** Run `/kata:configure-settings` anytime to update these preferences.

**If pr_workflow = Yes:**

Ask about GitHub Actions release workflow:

```
AskUserQuestion([
  {
    header: "GitHub Actions",
    question: "Scaffold a GitHub Actions workflow to auto-publish on release?",
    multiSelect: false,
    options: [
      { label: "Yes (Recommended)", description: "Create .github/workflows/release.yml for npm publish" },
      { label: "No", description: "I'll set up CI/CD myself" }
    ]
  }
])
```

**If "Yes":**

Create `.github/workflows/release.yml`:

```bash
mkdir -p .github/workflows
```

Write the workflow file:

```yaml
name: Publish to npm

on:
  push:
    branches:
      - main

jobs:
  publish:
    runs-on: ubuntu-latest
    permissions:
      contents: write
    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20'
          registry-url: 'https://registry.npmjs.org'

      - name: Get package info
        id: package
        run: |
          LOCAL_VERSION=$(node -p "require('./package.json').version")
          PACKAGE_NAME=$(node -p "require('./package.json').name")
          echo "local_version=$LOCAL_VERSION" >> $GITHUB_OUTPUT
          echo "package_name=$PACKAGE_NAME" >> $GITHUB_OUTPUT

          # Get published version (returns empty if not published)
          PUBLISHED_VERSION=$(npm view "$PACKAGE_NAME" version 2>/dev/null || echo "")
          echo "published_version=$PUBLISHED_VERSION" >> $GITHUB_OUTPUT

          echo "Local version: $LOCAL_VERSION"
          echo "Published version: $PUBLISHED_VERSION"

      - name: Check if should publish
        id: check
        run: |
          LOCAL="${{ steps.package.outputs.local_version }}"
          PUBLISHED="${{ steps.package.outputs.published_version }}"

          if [ -z "$PUBLISHED" ]; then
            echo "Package not yet published, will publish"
            echo "should_publish=true" >> $GITHUB_OUTPUT
          elif [ "$LOCAL" != "$PUBLISHED" ]; then
            echo "Version changed ($PUBLISHED -> $LOCAL), will publish"
            echo "should_publish=true" >> $GITHUB_OUTPUT
          else
            echo "Version unchanged ($LOCAL), skipping publish"
            echo "should_publish=false" >> $GITHUB_OUTPUT
          fi

      - name: Publish to npm
        if: steps.check.outputs.should_publish == 'true'
        run: npm publish --access public
        env:
          NODE_AUTH_TOKEN: ${{ secrets.NPM_TOKEN }}

      - name: Create GitHub Release
        if: steps.check.outputs.should_publish == 'true'
        uses: softprops/action-gh-release@v2
        with:
          tag_name: v${{ steps.package.outputs.local_version }}
          name: v${{ steps.package.outputs.local_version }}
          generate_release_notes: true
          make_latest: true
```

Commit the workflow:

```bash
git add .github/workflows/release.yml
git commit -m "$(cat <<'EOF'
ci: add npm publish workflow

Publishes to npm and creates GitHub Release when:
- Push to main
- package.json version differs from published version

Requires NPM_TOKEN secret in repository settings.
EOF
)"
```

Display setup instructions:

```
✓ Created .github/workflows/release.yml

## Setup Required

Add NPM_TOKEN secret to your GitHub repository:
1. Go to repo Settings → Secrets and variables → Actions
2. Click "New repository secret"
3. Name: NPM_TOKEN
4. Value: Your npm access token (from npmjs.com → Access Tokens)

The workflow will auto-publish when you merge PRs that bump package.json version.
```

**If statusline = Yes:**

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

**If statusline = No:**

No changes to `.claude/settings.json`.

## Phase 5.5: Resolve Model Profile

Read model profile for agent spawning:

```bash
MODEL_PROFILE=$(cat .planning/config.json 2>/dev/null | grep -o '"model_profile"[[:space:]]*:[[:space:]]*"[^"]*"' | grep -o '"[^"]*"$' | tr -d '"' || echo "balanced")
```

Default to "balanced" if not set.

**Model lookup table:**

| Agent                     | quality | balanced | budget |
| ------------------------- | ------- | -------- | ------ |
| kata-project-researcher   | opus    | sonnet   | haiku  |
| kata-research-synthesizer | sonnet  | sonnet   | haiku  |
| kata-roadmapper           | opus    | sonnet   | sonnet |

Store resolved models for use in Task calls if milestone research/roadmapping is needed later.

## Phase 6: Done

**Commit PROJECT.md and config.json (if not already committed):**

Check if uncommitted changes exist and commit them:

```bash
# Check for uncommitted planning files
if git status --porcelain .planning/PROJECT.md .planning/config.json 2>/dev/null | grep -q '.'; then
  git add .planning/PROJECT.md .planning/config.json
  git commit -m "$(cat <<'EOF'
docs: initialize project

Project context and workflow configuration.
EOF
)"
fi
```

**Display completion banner:**


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 Kata ► PROJECT INITIALIZED ✓
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

**[Project Name]**

| Artifact | Location                |
| -------- | ----------------------- |
| Project  | `.planning/PROJECT.md`  |
| Config   | `.planning/config.json` |

Ready for milestone planning ✓

───────────────────────────────────────────────────────────────

## ▶ Next Up

**Define your first milestone**

`/kata:add-milestone` — research, requirements, and roadmap

<sub>`/clear` first → fresh context window</sub>

───────────────────────────────────────────────────────────────


</process>

<output>

- `.planning/PROJECT.md`
- `.planning/config.json`

</output>

<success_criteria>

- [ ] .planning/ directory created
- [ ] Git repo initialized
- [ ] Brownfield detection completed
- [ ] Deep questioning completed (threads followed, not rushed)
- [ ] PROJECT.md captures full context → **committed**
- [ ] config.json has workflow mode, depth, parallelization → **committed**
- [ ] User knows next step is `/kata:add-milestone`

**Atomic commits:** PROJECT.md and config.json are committed. If context is lost, artifacts persist.

</success_criteria>
