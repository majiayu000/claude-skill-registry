---
name: install
description: "Verify VexJoy Agent installation, diagnose issues, and guide first-time setup."
user-invocable: true
allowed-tools:
  - Read
  - Bash
  - Glob
  - Grep
  - Write
  - Edit
  - Agent
routing:
  force_route: true
  not_for: "installing npm packages, pip packages, OS packages, hardware, third-party tools — only for VexJoy Agent toolkit setup verification"
  triggers:
    - "install toolkit"
    - "verify installation"
    - "health check toolkit"
    - "setup toolkit"
    - "diagnose setup"
    - "toolkit health"
  category: meta-tooling
---

# /install — Setup & Health Check

Verify your VexJoy Agent installation, diagnose issues, and get oriented. Use after cloning the repo and running `install.sh`, when something seems broken (hooks not firing, missing commands), for first-time orientation, or after a `git pull` to verify nothing broke.

## Instructions

### Phase 1: DIAGNOSE

**Goal**: Run deterministic health checks and report results.

**Step 1: Run install-doctor.py**

```bash
python3 ~/.claude/scripts/install-doctor.py check
```

If the script is not found at `scripts/install-doctor.py`, try `~/.claude/scripts/install-doctor.py`.

**Step 1b: Run runtime health check**

```bash
python3 ~/.claude/scripts/toolkit-health.py --json
```

If the script is not found at `scripts/toolkit-health.py`, try `~/.claude/scripts/toolkit-health.py`. This surfaces runtime health (hook error rate, stale memory files) that `install-doctor.py` does not cover. It exits 1 when `has_warnings` is true — treat that as "warnings to surface," not a setup failure. Capture the `flags` array for Step 3.

**Step 2: Interpret results**

| Result | Action |
|--------|--------|
| All checks pass | Skip to Phase 3 (Inventory) |
| `~/.claude` missing | Guide user to run `install.sh` — go to Phase 2 |
| Components missing | Guide user to run `install.sh` — go to Phase 2 |
| Hooks not configured | Guide user to run `install.sh` — go to Phase 2 |
| Broken symlinks | Symlink targets moved. Re-run `install.sh --symlink --force` |
| Python deps missing | Run `pip install -r requirements.txt` from the repo directory |
| Permissions wrong | Run `chmod 755` on affected files |

**Step 3: Display results clearly**

Show the check output to the user with a clear pass/fail summary. Display the raw script output without paraphrasing or reformatting, because the script already formats diagnostics for readability and rewriting them risks losing detail or misrepresenting status.

Append the runtime-health result from Step 1b: if `has_warnings` is true, list each entry from the `flags` array as a WARN line in the summary (e.g. stale memory files, elevated hook error rate). When `has_warnings` is false, report runtime health as OK. WARN flags are advisory — they inform the user without blocking the pass/fail verdict for setup.

**Gate**: Health check complete. If issues found, proceed to Phase 2. If clean, skip to Phase 3.

### Phase 2: FIX (only if issues found)

**Goal**: Guide the user through fixing detected issues.

**Step 1: Determine if install.sh needs to run**

If `~/.claude` is missing or components are not installed, the user needs to run install.sh. Tell them:

```
The toolkit hasn't been installed yet. Run this from the repo directory:

  ./install.sh --symlink     # recommended: updates with git pull
  ./install.sh --dry-run     # preview first
```

Wait for the user to confirm they've run it, then re-run the health check. This phase is interactive because installation changes system state -- always show the user what needs fixing and let them choose before acting.

**Step 2: Fix individual issues**

For fixable issues (permissions, missing deps), offer to fix them:

```bash
# Fix permissions
find ~/.claude/hooks -name "*.py" -exec chmod 755 {} \;
find ~/.claude/scripts -name "*.py" -exec chmod 755 {} \;

# Install Python deps (from repo directory)
pip install -r requirements.txt
```

Only run fixes the user approves, because automated fixes to `~/.claude` can break an existing setup if assumptions about the environment are wrong.

**Step 3: Re-check**

After fixes, re-run:
```bash
python3 ~/.claude/scripts/install-doctor.py check
```

**Gate**: All checks pass. Proceed to Phase 3.

### Phase 3: INVENTORY

**Goal**: Show the user what they have installed.

**Step 1: Run inventory**

```bash
python3 ~/.claude/scripts/install-doctor.py inventory
```

**Step 2: Display summary**

Show the actual counts returned by `install-doctor.py inventory` -- never display hardcoded numbers, because component counts change with every install and stale numbers erode trust. Present them as:

```
Your toolkit is ready. Here's what's installed:

  Agents:   [N] specialized domain experts
  Skills:   [N] workflow methodologies ([N] user-invocable)
  Hooks:    [N] automation hooks
  Commands: [N] slash commands
  Scripts:  [N] utility scripts
```

**Gate**: User sees their inventory. Proceed to Phase 3.5.

### Phase 3.5: MCP INVENTORY

**Goal**: Show which MCP servers are available and their status.

**Step 1: Run MCP registry check**

```bash
python3 ~/.claude/scripts/mcp-registry.py list
```

If the script is not found at `scripts/mcp-registry.py`, try `~/.claude/scripts/mcp-registry.py`.

**Step 2: Display MCP status**

Show the MCP inventory as:

```
MCP Servers:

  [✓] Chrome DevTools MCP  — Live browser debugging
      Paired skills: wordpress-live-validation
  [✓] Playwright MCP       — Automated browser testing
      Paired skills: wordpress-live-validation
  [✓] gopls MCP            — Go workspace intelligence
      Paired skills: go-patterns
  [✗] Context7 MCP         — Library documentation lookups
      Install: claude mcp add context7 -- npx @anthropic-ai/mcp-context7@latest
```

Use checkmark for connected MCPs and X for missing ones. For missing MCPs, show the install command.

**Gate**: MCP inventory displayed. Proceed to Phase 4.

### Phase 4: ORIENT

**Goal**: Give the user their bearings -- what to do first.

**Step 1: Show the three essential commands**

```
Getting started:

  /do [describe what you want]    — routes to the right agent + skill
  /comprehensive-review           — 20+ reviewer agents in 3 waves
  /install                        — run this again anytime to check health
```

**Step 2: Show a few practical examples**

```
Try these:

  /do debug this failing test
  /do review my Go code for quality
  /do write a blog post about [topic]
  /do create a voice profile from my writing samples
```

**Step 3: Mention the docs**

```
Documentation:
  docs/QUICKSTART.md   — 30-second overview
  docs/REFERENCE.md    — quick reference card
```

**Gate**: User is oriented. Installation complete.

## Error Handling

### Error: install-doctor.py not found
The script hasn't been installed yet. Check if the user is in the repo directory. If so, run it directly from `scripts/`. If not, guide them to clone and install first.

### Error: Permission denied on install.sh
Run `chmod +x install.sh` first.

### Error: Python not found
The toolkit requires Python 3.10+. Guide the user to install Python for their platform.
