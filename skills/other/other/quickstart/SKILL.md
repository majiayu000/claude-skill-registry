---
name: quickstart
description: 'Interactive onboarding for new users. Guided RPI cycle on your actual codebase in under 10 minutes. Triggers: "quickstart", "get started", "onboarding", "how do I start".'
metadata:
  tier: session
  dependencies: []
---

# /quickstart — Get Started

> **Purpose:** Walk a new user through the toolbox on their actual codebase. Under 10 minutes to first value. Show that skills are mix-and-match primitives, not a rigid pipeline — and that `/swarm` is the key multiplier.

**YOU MUST EXECUTE THIS WORKFLOW. Do not just describe it.**

**CLI dependencies:** None required. All external CLIs (bd, ao, gt) are optional enhancements.

**References (load as needed):**
- `references/getting-started.md` — Detailed first-time walkthrough
- `references/troubleshooting.md` — Common issues and fixes

## Execution Steps

### Step 0: Pre-flight

Check environment before starting. Failures here are informational, not blocking.

```bash
# 1. Git repo check
if git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  echo "GIT_REPO=true"
else
  echo "GIT_REPO=false"
  echo "Not a git repo. Some features (recent changes, vibe) need git."
  echo "Options: run 'git init' to enable full features, or continue in manual mode."
fi

# 2. ao CLI availability
if command -v ao &>/dev/null; then
  echo "AO_CLI=true"
  ao status 2>/dev/null | head -3
else
  echo "AO_CLI=false — optional, enables persistent knowledge flywheel"
fi

# 3. .agents/ directory
if [ -d ".agents" ]; then
  echo "AGENTS_DIR=exists"
elif mkdir -p .agents 2>/dev/null; then
  echo "AGENTS_DIR=created"
  rmdir .agents 2>/dev/null  # clean up test dir
else
  echo "AGENTS_DIR=no_write — cannot create .agents/ directory (check permissions)"
fi

# 4. Claude Code version (informational)
claude --version 2>/dev/null || echo "Claude Code version: unknown"

# 5. Claude custom agents inventory (informational)
if command -v claude &>/dev/null; then
  claude agents 2>/dev/null | head -20 || echo "Claude agents: unavailable in this environment"
fi
```

**If GIT_REPO=false:** Continue the walkthrough but skip git-dependent steps (Steps 3, 5). Replace them with file-browsing equivalents. Tell the user which steps were adapted and why.

### Step 1: Detect Project

```bash
# Detect language/framework (monorepo-friendly)
# - Uses a shallow scan to avoid walking giant repos
# - Prints the path that triggered detection (helps when you're in the wrong subdir)
ROOT="."
GIT_ROOT=""
if git rev-parse --show-toplevel >/dev/null 2>&1; then
  GIT_ROOT="$(git rev-parse --show-toplevel)"
  ROOT="$GIT_ROOT"
fi

# Pretty-print paths relative to repo root when possible.
relpath() {
  local p="$1"
  if [[ -n "$GIT_ROOT" ]]; then
    echo "${p#"$GIT_ROOT"/}"
    return
  fi
  echo "${p#./}"
}

find_first() {
  # Usage: find_first <name-pattern> (e.g., "go.mod" or "*.py")
  find "$ROOT" -maxdepth 4 \
    -type d \( -name .git -o -name .agents -o -name .beads -o -name node_modules \) -prune \
    -o -type f -name "$1" -print -quit 2>/dev/null
}

python="$(find_first pyproject.toml)"
[[ -n "$python" ]] || python="$(find_first requirements.txt)"
[[ -n "$python" ]] || python="$(find_first setup.py)"
[[ -n "$python" ]] || python="$(find_first '*.py')"
[[ -n "$python" ]] && echo "Python detected ($(relpath "$python"))"

go="$(find_first go.mod)"
[[ -n "$go" ]] || go="$(find_first '*.go')"
[[ -n "$go" ]] && echo "Go detected ($(relpath "$go"))"

ts="$(find_first tsconfig.json)"
[[ -n "$ts" ]] || ts="$(find_first package.json)"
[[ -n "$ts" ]] || ts="$(find_first '*.ts')"
[[ -n "$ts" ]] || ts="$(find_first '*.tsx')"
[[ -n "$ts" ]] && echo "TypeScript detected ($(relpath "$ts"))"

rust="$(find_first Cargo.toml)"
[[ -n "$rust" ]] || rust="$(find_first '*.rs')"
[[ -n "$rust" ]] && echo "Rust detected ($(relpath "$rust"))"

java="$(find_first pom.xml)"
[[ -n "$java" ]] || java="$(find_first build.gradle)"
[[ -n "$java" ]] || java="$(find_first '*.java')"
[[ -n "$java" ]] && echo "Java detected ($(relpath "$java"))"

infra="$(find_first Dockerfile)"
[[ -n "$infra" ]] || infra="$(find_first Makefile)"
[[ -n "$infra" ]] || infra="$(find_first '*.sh')"
[[ -n "$infra" ]] && echo "Shell/Infra detected ($(relpath "$infra"))"
```

**If no language detected:** Tell the user: "I couldn't auto-detect a language. What is the primary language of this project? (Python, Go, TypeScript, Rust, Java, Shell, or other)" Then continue with whatever they choose.

```bash
# Check git state (skip if GIT_REPO=false)
git log --oneline -5 2>/dev/null
git diff --stat HEAD~3 2>/dev/null | tail -5

# Check for existing workflow setup
ls .agents/ 2>/dev/null && echo "Workflow artifacts found"
ls .beads/ 2>/dev/null && echo "Beads issue tracking found"

# Repo-specific instructions (optional but high-signal)
test -f AGENTS.md && echo "AGENTS.md found (repo-specific workflow)"
```

### Step 2: Welcome and Orient

Present this to the user:

```
Welcome! AgentOps gives your coding agent three things it doesn't have:

  Memory    — Every session extracts learnings into .agents/.
              Next session, the best ones are injected automatically.
              Session 50 knows what session 1 learned.

  Judgment  — /council spawns independent judges (Claude + Codex)
              to validate plans and code before shipping.

  Skills    — Standalone primitives you use as-needed:
              /research, /plan, /vibe, /brainstorm, and more.
              Parallelize any of them with /swarm.

Let's do a quick tour using YOUR code.
```

### Step 3: Mini Research

Run a focused research pass on the most recently changed area:

```bash
# Find what changed recently (dirty tree first; fall back to last commit if clean)
if git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  STAGED="$(git diff --name-only --cached 2>/dev/null || true)"
  UNSTAGED="$(git diff --name-only 2>/dev/null || true)"
  UNTRACKED="$(git ls-files --others --exclude-standard 2>/dev/null || true)"

  RECENT_FILES="$(printf "%s\n%s\n%s\n" "$STAGED" "$UNSTAGED" "$UNTRACKED" | sed '/^$/d' | sort -u)"

  # Clean repo: fall back to last commit, then fall back to "some tracked files"
  if [[ -z "$RECENT_FILES" ]] && git rev-parse --verify HEAD >/dev/null 2>&1; then
    RECENT_FILES="$(git show --name-only --pretty="" HEAD 2>/dev/null | sed '/^$/d')"
  fi
  [[ -z "$RECENT_FILES" ]] && RECENT_FILES="$(git ls-files 2>/dev/null | head -50)"

  # Best-effort noise filtering; keep unfiltered list if filtering drops everything
  FILTERED="$(echo "$RECENT_FILES" | grep -Ev '^(\\.agents/|cli/\\.agents/|\\.beads/)' || true)"
  [[ -n "$FILTERED" ]] && RECENT_FILES="$FILTERED"

  echo "$RECENT_FILES" | head -10
else
  echo "Not a git repo; skipping recent-change detection."
fi
```

Read 2-3 of the most recently changed files. Provide a brief summary:
- What area of the codebase is active
- What patterns are used
- One observation about code quality

Tell the user: "This is what `/research` does — deep exploration of your codebase. Use it before planning any significant work."

### Step 4: Mini Plan

Based on the research, suggest ONE concrete improvement:

```
Based on what I found, here's a task we could plan:

  "<specific improvement based on what was found>"

This is what /plan does — decomposes goals into trackable issues with
dependencies and waves.
```

### Step 5: Mini Vibe Check

Run a quick validation on recent changes:

```bash
# Use the same RECENT_FILES list from Step 3.
# If you didn't run Step 3 in the same shell, re-run the Step 3 snippet to rebuild RECENT_FILES.
if [[ -n "${RECENT_FILES:-}" ]]; then
  echo "$RECENT_FILES" | head -10
else
  echo "RECENT_FILES is empty; re-run the Step 3 snippet to rebuild it."
fi
```

Perform a brief inline review (similar to `/council --quick`) of the most recent changes:
- Check for obvious issues
- Note any complexity concerns
- Provide a quick PASS/WARN/FAIL assessment

Tell the user: "This is what `/vibe` does — complexity analysis + multi-model council review. Use it before committing significant changes."

### Step 6: Show How It Fits Together

```
You've just completed a mini RPI cycle:
  Research → Plan → Validate

Those are independent skills. You can use any of them by itself,
or compose them however you want. Here's how they relate:
```

Present the composition map — how skills call each other:

```
                          YOU
                           │
            ┌──────────────┼──────────────┐
            │              │              │
       use one skill    compose a few   /rpi "goal"
       by itself        your way        full pipeline
            │              │              │
            ▼              ▼              ▼
   ┌─────────────────────────────────────────────────────┐
   │              HOW SKILLS COMPOSE                     │
   │                                                     │
   │  JUDGMENT (the foundation)                          │
   │  /council ──────► spawns independent judges         │
   │  /vibe ─────────► /complexity + /council            │
   │  /pre-mortem ───► /council (simulate failures)      │
   │  /post-mortem ──► /council + /retro                 │
   │                                                     │
   │  EXECUTION                                          │
   │  /research ─────► may trigger /brainstorm           │
   │  /plan ─────────► may call /pre-mortem to validate  │
   │  /implement ────► /research + /plan + build + /vibe │
   │  /crank ────────► /swarm ──► /implement (×N per     │
   │                   wave, fresh context each)         │
   │  /swarm ────────► parallelize any skill             │
   │                                                     │
   │  PIPELINE                                           │
   │  /rpi chains:  research → plan → pre-mortem →       │
   │                crank → vibe → post-mortem            │
   │  /evolve loops /rpi against fitness goals            │
   └─────────────────────────────────────────────────────┘
            │
            ▼
   ┌─────────────────┐
   │    .agents/     │  Append-only ledger.
   │    learnings    │  Every session writes.
   │    patterns     │  Freshness decay prunes.
   │    decisions    │  Next session injects the best.
   └─────────────────┘

QUICK REFERENCE
/research     explore and understand code
/council      independent judges validate plans or code
/vibe         code quality review (complexity + council)
/plan         break down a goal into tasks
/implement    execute a single task end-to-end
/crank        run a multi-issue epic in parallel waves
/swarm        parallelize any skill
/rpi          full pipeline — one command
/status       see what you're working on

INTENT ROUTER
What are you trying to do?
│
├─ "Not sure what to do yet"
│   └─ Generate options first ─────► /brainstorm
│
├─ "I have an idea"
│   └─ Understand code + context ──► /research
│
├─ "I know what I want to build"
│   └─ Break it into issues ───────► /plan
│
├─ "Now build it"
│   ├─ Small/single issue ─────────► /implement
│   ├─ Multi-issue epic ───────────► /crank <epic-id>
│   └─ Full flow in one command ───► /rpi "goal"
│
├─ "Fix a bug"
│   ├─ Know which file? ──────────► /implement <issue-id>
│   └─ Need to investigate? ──────► /bug-hunt
│
├─ "Build a feature"
│   ├─ Small (1-2 files) ─────────► /implement
│   ├─ Medium (3-6 issues) ───────► /plan → /crank
│   └─ Large (7+ issues) ─────────► /rpi (full pipeline)
│
├─ "Validate something"
│   ├─ Code ready to ship? ───────► /vibe
│   ├─ Plan ready to build? ──────► /pre-mortem
│   ├─ Work ready to close? ──────► /post-mortem
│   └─ Quick sanity check? ───────► /council --quick validate
│
├─ "Explore or research"
│   ├─ Understand this codebase ──► /research
│   ├─ Compare approaches ────────► /council research <topic>
│   └─ Generate ideas ────────────► /brainstorm
│
├─ "Learn from past work"
│   ├─ What do we know about X? ──► /knowledge <query>
│   ├─ Save this insight ─────────► /learn "insight"
│   └─ Run a retrospective ───────► /retro
│
├─ "Parallelize work"
│   ├─ Multiple independent tasks ► /swarm
│   └─ Full epic with waves ──────► /crank <epic-id>
│
├─ "Ship a release"
│   └─ Changelog + tag ──────────► /release <version>
│
├─ "Session management"
│   ├─ Where was I? ──────────────► /status
│   ├─ Save for next session ─────► /handoff
│   └─ Recover after compaction ──► /recover
│
└─ "First time here" ────────────► /quickstart
```

For the complete catalog, use the Read tool on `skills/quickstart/references/full-catalog.md`.

### Step 8: Prove the Flywheel Works

Show the user that their sessions have already started compounding — and how to verify it:

```bash
# How many learnings have accumulated so far?
ls .agents/learnings/ 2>/dev/null | wc -l

# Surface the most relevant knowledge for this session
if command -v ao &>/dev/null; then
  ao inject --format markdown --max-tokens 1000 2>/dev/null | head -40
else
  # ao not installed: show raw learnings from disk
  ls .agents/learnings/*.md 2>/dev/null | while read -r f; do
    echo "--- $(basename "$f") ---"
    head -8 "$f"
    echo ""
  done
fi
```

**The aha moment.** Explain what just happened:

```
You just ran 'ao inject' — the same command the session-start hook runs automatically.

What it does:
  1. Scans .agents/learnings/ for knowledge from past sessions
  2. Scores by freshness + retrieval history + confidence
  3. Injects the best-scoring knowledge into the current session context

What it means for you:
  - Session 2 already knows what Session 1 learned
  - Session 50 knows what Session 1 through 49 learned
  - Patterns that surface repeatedly get promoted. Old ones decay.

The flywheel is running. You can verify it any time:
  ao inject                    ← see what this session inherited
  ao status                    ← current knowledge inventory
  ls .agents/learnings/        ← raw learning files
```

**If no learnings exist yet**, tell the user:
```
No learnings yet — that's expected on your first session.
Run /rpi "a small goal" to complete one full cycle,
then 'ao inject' in your NEXT session to see what compounded.
```

### Step 7: What's Next

Suggest the next skill to try based on what the user just saw:

```
Try one of the skills you just previewed — on real work:

  /research "something you're building this week"
  /council validate a recent PR or plan
  /vibe recent                              ← check your latest changes

When you want parallelism, /swarm multiplies any of them.
When you want the full pipeline, /rpi chains them all:

  /rpi "goal"              ← research → plan → validate → ship → learn
  ao rpi phased "goal"     ← same thing from the CLI, fresh context per phase

Want hands-free improvement?

  /product → /goals generate → /evolve   ← define goals, fix gaps, compound
```

Then suggest the most useful immediate next action based on project state:

| State | Suggestion |
|-------|------------|
| Recent commits, no tests | "Try `/vibe recent` to check your latest changes" |
| Open issues/TODOs | "Try `/plan` to decompose a goal into trackable issues" |
| Complex codebase, new to it | "Try `/research <area>` to understand a specific area" |
| Bug reports or failures | "Try `/bug-hunt` to investigate systematically" |
| Clean state, looking for work | "Try `/rpi \"<improvement from mini-research>\"` to run the full lifecycle" |

**Graduation hints** (state-aware, based on pre-flight + detection):

```bash
# Gather state from pre-flight (Step 0)
command -v ao &>/dev/null && AO_AVAILABLE=true || AO_AVAILABLE=false
command -v bd &>/dev/null && BD_AVAILABLE=true || BD_AVAILABLE=false
command -v codex &>/dev/null && CODEX_AVAILABLE=true || CODEX_AVAILABLE=false
ls .agents/ &>/dev/null && AGENTS_DIR=true || AGENTS_DIR=false
ls .beads/ &>/dev/null && BEADS_DIR=true || BEADS_DIR=false
git rev-parse --is-inside-work-tree &>/dev/null && GIT_REPO=true || GIT_REPO=false
```

**Present ONLY the row matching current state (do not show all tiers):**

| Current State | Tier | Next Step |
|---------------|------|-----------|
| No git repo | — | "Initialize git with `git init` to unlock change tracking, `/vibe`, and full RPI workflow." |
| Git repo, no `ao`, no `.agents/` | Tier 0 | "You're at Tier 0 — skills work standalone. When you want learnings to persist across sessions, install the `ao` CLI: `brew tap boshu2/agentops https://github.com/boshu2/homebrew-agentops && brew install agentops && ao init --hooks`" |
| `ao` installed, no `.agents/` yet | Tier 0+ | "Run `ao init` to create the `.agents/` directory and .gitignore. Add `--hooks` to also install flywheel hooks (SessionStart + Stop). Your knowledge flywheel starts capturing learnings automatically." |
| `ao` + `.agents/`, no beads | Tier 1 | "Knowledge flywheel is active. When you have multi-issue epics, add beads for issue tracking: `brew install boshu2/agentops/beads && bd init --prefix <your-prefix>`" |
| `ao` + beads, no Codex | Tier 2 | "Full RPI stack. Start with repo instructions (check `AGENTS.md` if present), then try `bd ready` (find work) or `/crank` (run an epic)." |
| `ao` + beads + Codex | Tier 2+ | "Full stack with cross-vendor. Try `/council --mixed` for Claude + Codex consensus, or `/vibe --mixed` for cross-vendor code review." |

---

## Examples

### First-Time User in a Go Project

**User says:** `/quickstart`

**What happens:**
1. Agent runs pre-flight checks (git repo: yes, ao CLI: no, .agents/: no)
2. Agent detects Go (finds go.mod at root)
3. Agent reads recently changed files (auth.go, config.go from last commit)
4. Agent provides mini-research summary: "Active area: authentication. Patterns: standard library HTTP handlers. Observation: missing error wrapping in 3 locations."
5. Agent suggests improvement: "Add error wrapping to auth.go error returns"
6. Agent runs mini-vibe on auth.go: WARN for missing error context
7. Agent displays skill menu and next steps
8. Agent shows Tier 0 graduation hint: "Install ao CLI to enable knowledge flywheel"

**Result:** User completes mini RPI cycle in under 10 minutes, sees real value on their code.

### Non-Git Repository

**User says:** `/quickstart` (in a directory without `.git/`)

**What happens:**
1. Agent runs pre-flight, detects GIT_REPO=false
2. Agent continues walkthrough but skips git-dependent steps (recent commits, vibe)
3. Agent detects Python (finds pyproject.toml)
4. Agent browses recent files using `ls -lt` instead of `git diff`
5. Agent suggests: "Initialize git with `git init` to unlock change tracking and full RPI workflow"
6. Agent completes quickstart with adapted steps

**Result:** Quickstart works without git, user sees value and learns what git unlocks.

### Monorepo with Multiple Languages

**User says:** `/quickstart` (in a monorepo with Go + TypeScript)

**What happens:**
1. Agent detects both Go (go.mod) and TypeScript (tsconfig.json) with relative paths
2. Agent displays: "Go detected (backend/go.mod), TypeScript detected (frontend/tsconfig.json)"
3. Agent asks: "Which area should we explore?" (backend or frontend)
4. User chooses backend. Agent focuses mini-research on Go code
5. Agent completes quickstart scoped to selected area

**Result:** Quickstart adapts to monorepo structure, user picks focus area.

---

## Troubleshooting

| Problem | Cause | Solution |
|---------|-------|----------|
| "No language detected" | Shallow scan missed project files or in wrong directory | Change to project root directory or manually specify language when prompted |
| "Cannot create .agents/ directory" | Permissions issue or read-only filesystem | Check directory permissions or continue without persistent artifacts (functionality reduced) |
| Pre-flight shows all "false" | Running in minimal environment or empty directory | Verify you're in the correct project directory with code files |
| Mini-vibe step skipped | GIT_REPO=false or no recent changes | Expected behavior for non-git repos or clean trees. Vibe requires git history. |
| Graduation hint shows wrong tier | Detection logic using cached state | Re-run pre-flight checks in Step 0 to refresh environment state |

---

## See Also

- `skills/vibe/SKILL.md` — Code validation
- `skills/research/SKILL.md` — Codebase exploration
- `skills/plan/SKILL.md` — Epic decomposition
