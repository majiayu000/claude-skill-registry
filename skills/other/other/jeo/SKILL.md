---
name: jeo
description: "JEO — Integrated AI agent orchestration skill. Plan with ralph+plannotator, execute with team/bmad, verify browser behavior with agent-browser, apply UI feedback with agentation(annotate), auto-cleanup worktrees after completion. Supports Claude, Codex, Gemini CLI, and OpenCode. Install: ralph, omc, omx, ohmg, bmad, plannotator, agent-browser, agentation."
compatibility: "Requires git, node>=18, bash. Optional: bun, docker."
allowed-tools: Read Write Bash Grep Glob Task
metadata:
  tags: jeo, orchestration, ralph, plannotator, agentation, annotate, agentui, UI-review, team, bmad, omc, omx, ohmg, agent-browser, multi-agent, workflow, worktree-cleanup, browser-verification, ui-feedback
  platforms: Claude, Codex, Gemini, OpenCode
  keyword: jeo
  version: 1.3.1
  source: supercent-io/skills-template
---


# JEO — Integrated Agent Orchestration

> Keyword: `jeo` · `annotate` · `UI-review` · `agentui (deprecated)` | Platforms: Claude Code · Codex CLI · Gemini CLI · OpenCode
>
> A unified skill providing fully automated orchestration flow:
> Plan (ralph+plannotator) → Execute (team/bmad) → UI Feedback (agentation/annotate) → Cleanup (worktree cleanup)

## Control Layers

JEO uses one cross-platform abstraction for orchestration:

- `settings`: platform/runtime configuration such as Claude hooks, Codex `config.toml`, Gemini `settings.json`, MCP registration, and prompt parameters
- `rules`: policy constraints that must hold on every platform
- `hooks`: event callbacks that enforce those rules on each platform

The key JEO rules are:

- do not reopen the PLAN gate when the current plan hash already has a terminal result
- only a revised plan resets `plan_gate_status` to `pending`
- do not process agentation annotations before explicit submit/onSubmit opens the submit gate

The authoritative state is `.omc/state/jeo-state.json`. Hooks may help advance the workflow, but they must obey the state file.

---

## 0. Agent Execution Protocol (follow immediately upon `jeo` keyword detection)

> The following are commands, not descriptions. Execute them in order. Each step only proceeds after the previous one completes.

### STEP 0: State File Bootstrap (required — always first)

```bash
mkdir -p .omc/state .omc/plans .omc/logs
```

If `.omc/state/jeo-state.json` does not exist, create it:

<!-- NOTE: The `worktrees` array was removed from the initial schema as it is not yet implemented.
     Add it back when multi-worktree parallel execution tracking is needed.
     worktree-cleanup.sh queries git worktree list directly, so it works without this field. -->
```json
{
  "phase": "plan",
  "task": "<detected task>",
  "plan_approved": false,
  "plan_gate_status": "pending",
  "plan_current_hash": null,
  "last_reviewed_plan_hash": null,
  "last_reviewed_plan_at": null,
  "plan_review_method": null,
  "team_available": null,
  "retry_count": 0,
  "last_error": null,
  "checkpoint": null,
  "created_at": "<ISO 8601>",
  "updated_at": "<ISO 8601>",
  "agentation": {
    "active": false,
    "session_id": null,
    "keyword_used": null,
    "submit_gate_status": "idle",
    "submit_signal": null,
    "submit_received_at": null,
    "submitted_annotation_count": 0,
    "started_at": null,
    "timeout_seconds": 120,
    "annotations": { "total": 0, "acknowledged": 0, "resolved": 0, "dismissed": 0, "pending": 0 },
    "completed_at": null,
    "exit_reason": null
  }
}
```

Notify the user:
> "JEO activated. Phase: PLAN. Add the `annotate` keyword if a UI feedback loop is needed."

---

### STEP 0.1: Error Recovery Protocol (applies to all STEPs)

**Checkpoint recording — immediately after entering each STEP:**
```python
# Execute immediately at the start of each STEP (agent updates jeo-state.json directly)
python3 -c "
import json, datetime, os, subprocess, tempfile
try:
    root = subprocess.check_output(['git', 'rev-parse', '--show-toplevel'], stderr=subprocess.DEVNULL).decode().strip()
except:
    root = os.getcwd()
f = os.path.join(root, '.omc/state/jeo-state.json')
if os.path.exists(f):
    import fcntl
    with open(f, 'r+') as fh:
        fcntl.flock(fh, fcntl.LOCK_EX)
        try:
            d = json.load(fh)
            d['checkpoint']='<current_phase>'   # 'plan'|'execute'|'verify'|'cleanup'
            d['updated_at']=datetime.datetime.utcnow().isoformat()+'Z'
            fh.seek(0)
            json.dump(d, fh, ensure_ascii=False, indent=2)
            fh.truncate()
        finally:
            fcntl.flock(fh, fcntl.LOCK_UN)
" 2>/dev/null || true
```

**last_error recording — on pre-flight failure or exception:**
```python
python3 -c "
import json, datetime, os, subprocess, fcntl
try:
    root = subprocess.check_output(['git', 'rev-parse', '--show-toplevel'], stderr=subprocess.DEVNULL).decode().strip()
except:
    root = os.getcwd()
f = os.path.join(root, '.omc/state/jeo-state.json')
if os.path.exists(f):
    with open(f, 'r+') as fh:
        fcntl.flock(fh, fcntl.LOCK_EX)
        try:
            d = json.load(fh)
            d['last_error']='<error message>'
            d['retry_count']=d.get('retry_count',0)+1
            d['updated_at']=datetime.datetime.utcnow().isoformat()+'Z'
            fh.seek(0)
            json.dump(d, fh, ensure_ascii=False, indent=2)
            fh.truncate()
        finally:
            fcntl.flock(fh, fcntl.LOCK_UN)
" 2>/dev/null || true
```

**Checkpoint-based resume on restart:**
```python
# If jeo-state.json already exists, resume from checkpoint
python3 -c "
import json, os, subprocess
try:
    root = subprocess.check_output(['git', 'rev-parse', '--show-toplevel'], stderr=subprocess.DEVNULL).decode().strip()
except:
    root = os.getcwd()
f = os.path.join(root, '.omc/state/jeo-state.json')
if os.path.exists(f):
    d=json.load(open(f))
    cp=d.get('checkpoint')
    err=d.get('last_error')
    if err: print(f'Previous error: {err}')
    if cp: print(f'Resuming from: {cp}')
" 2>/dev/null || true
```

> **Rule**: Before `exit 1` in pre-flight, always update `last_error` and increment `retry_count`.
> If `retry_count >= 3`, ask the user whether to abort.

---

### STEP 1: PLAN (never skip)

**Pre-flight (required before entering):**
```bash
# Record checkpoint
python3 -c "
import json,datetime,os,subprocess,fcntl,tempfile
try:
    root=subprocess.check_output(['git','rev-parse','--show-toplevel'],stderr=subprocess.DEVNULL).decode().strip()
except:
    root=os.getcwd()
f=os.path.join(root,'.omc/state/jeo-state.json')
if os.path.exists(f):
    with open(f,'r+') as fh:
        fcntl.flock(fh,fcntl.LOCK_EX)
        try:
            d=json.load(fh)
            d.update({'checkpoint':'plan','updated_at':datetime.datetime.utcnow().isoformat()+'Z'})
            fh.seek(0); json.dump(d,fh,ensure_ascii=False,indent=2); fh.truncate()
        finally:
            fcntl.flock(fh,fcntl.LOCK_UN)
" 2>/dev/null || true

# NOTE: Claude Code — skip this entire bash block.
# plannotator is a hook-only binary; calling it directly always fails.
# For Claude Code: call EnterPlanMode → write plan → call ExitPlanMode.
# The ExitPlanMode PermissionRequest hook fires plannotator automatically.
# The following script is for Codex / Gemini / OpenCode only.

# GUARD: enforce no-repeat PLAN review by plan hash.
# same hash + terminal gate status => skip reopening the plan gate
# revised plan.md content => reset gate to pending and review again
PLAN_GATE_STATUS=$(python3 -c "
import json, os
try:
    s = json.load(open('.omc/state/jeo-state.json'))
    print(s.get('plan_gate_status', 'pending'))
except Exception:
    print('pending')
" 2>/dev/null || echo "pending")

HASH_MATCH=$(python3 -c "
import hashlib, json, os
try:
    s = json.load(open('.omc/state/jeo-state.json'))
    if not os.path.exists('plan.md'):
        print('no-match')
    else:
        current_hash = hashlib.sha256(open('plan.md', 'rb').read()).hexdigest()
        print('match' if current_hash == (s.get('last_reviewed_plan_hash') or '') else 'no-match')
except Exception:
    print('no-match')
" 2>/dev/null || echo "no-match")

if [[ "$HASH_MATCH" == "match" && "$PLAN_GATE_STATUS" =~ ^(approved|manual_approved)$ ]]; then
  echo "✅ Current plan hash already approved. Skipping re-review."
  exit 0
fi

# BUG FIX (v1.3.1): feedback_required + same hash must NOT exit 0 (approved).
# The plan has outstanding feedback and must be revised before re-opening plannotator.
# Exiting 0 here would cause JEO to proceed to EXECUTE with an unapproved plan.
if [[ "$HASH_MATCH" == "match" && "$PLAN_GATE_STATUS" == "feedback_required" ]]; then
  echo "❌ Feedback pending for this plan hash — revise plan.md content (new hash required) before re-opening plannotator."
  echo "   Check .omc/state/jeo-state.json → plannotator_feedback for the recorded feedback."
  exit 1
fi

if [[ "$HASH_MATCH" == "match" && "$PLAN_GATE_STATUS" == "infrastructure_blocked" ]]; then
  echo "⚠️ Infrastructure blocked for current plan hash. Use manual TTY gate or set plan_gate_status='manual_approved' in jeo-state.json."
  exit 32
fi

# plannotator is mandatory for the PLAN step (Codex/Gemini/OpenCode).
# If missing, JEO auto-installs it before opening the PLAN gate.
# Resolve the JEO scripts directory (works from any CWD)
_JEO_SCRIPTS=""
for _candidate in \
  "${JEO_SKILL_DIR:-}/scripts" \
  "$HOME/.agent-skills/jeo/scripts" \
  "$HOME/.codex/skills/jeo/scripts" \
  "$(pwd)/.agent-skills/jeo/scripts" \
  "scripts" \
  ; do
  if [ -f "${_candidate}/plannotator-plan-loop.sh" ]; then
    _JEO_SCRIPTS="$_candidate"
    break
  fi
done

if [ -z "$_JEO_SCRIPTS" ]; then
  echo "❌ JEO scripts not found. Re-run: bash setup-codex.sh (or setup-gemini.sh)"
  exit 1
fi

if ! bash "${_JEO_SCRIPTS}/ensure-plannotator.sh"; then
  echo "❌ plannotator auto-install failed: cannot proceed with PLAN step."
  echo "   Retry: bash ${_JEO_SCRIPTS}/../scripts/install.sh --with-plannotator"
  exit 1
fi

# Required PLAN gate (Codex / Gemini / OpenCode):
# - Must wait until approve/feedback is received
# - Auto-restart on session exit (up to 3 times)
# - After 3 exits, ask user whether to end PLAN
FEEDBACK_DIR=$(python3 -c "import hashlib,os; h=hashlib.md5(os.getcwd().encode()).hexdigest()[:8]; d=f'/tmp/jeo-{h}'; os.makedirs(d,exist_ok=True); print(d)" 2>/dev/null || echo '/tmp')
FEEDBACK_FILE="${FEEDBACK_DIR}/plannotator_feedback.txt"
bash "${_JEO_SCRIPTS}/plannotator-plan-loop.sh" plan.md "$FEEDBACK_FILE" 3
PLAN_RC=$?

if [ "$PLAN_RC" -eq 0 ]; then
  echo "✅ Plan approved"
elif [ "$PLAN_RC" -eq 10 ]; then
  echo "❌ Plan not approved — apply feedback, revise plan.md, and retry"
  exit 1
elif [ "$PLAN_RC" -eq 32 ]; then
  echo "⚠️ plannotator UI unavailable (sandbox/CI). Entering Conversation Approval Mode:"
  echo "   1. Output plan.md content to user in conversation"
  echo "   2. Ask user: 'approve' to proceed or provide feedback"
  echo "   3. DO NOT proceed to EXECUTE until user explicitly approves"
  exit 32
elif [ "$PLAN_RC" -eq 30 ] || [ "$PLAN_RC" -eq 31 ]; then
  echo "⛔ PLAN exit decision (or awaiting confirmation). Confirm with user before retrying."
  exit 1
else
  echo "❌ plannotator PLAN gate failed (code=$PLAN_RC)"
  exit 1
fi
mkdir -p .omc/plans .omc/logs
```

1. Write `plan.md` (include goal, steps, risks, and completion criteria)
2. **Invoke plannotator** (per platform):
   - **Claude Code (hook mode — only supported method)**:
     `plannotator` is a hook-only binary. It cannot be called via MCP tool or CLI directly.
     Call `EnterPlanMode`, write the plan content in plan mode, then call `ExitPlanMode`.
     The `ExitPlanMode` PermissionRequest hook fires the JEO Claude plan-gate wrapper automatically.
     That wrapper must skip re-entry when the current plan hash already has a terminal review result.
     Wait for the hook to return before proceeding — approved or feedback will arrive via the hook result.
   - **Codex / Gemini / OpenCode**: run blocking CLI (never use `&`):
     ```bash
     # _JEO_SCRIPTS must be resolved first via the dynamic path discovery block in the pre-flight above
     bash "${_JEO_SCRIPTS}/plannotator-plan-loop.sh" plan.md /tmp/plannotator_feedback.txt 3
     ```
     If `plannotator` is missing, JEO must auto-run `bash "${_JEO_SCRIPTS}/ensure-plannotator.sh"` first and continue only after the CLI is available.
3. Check result:
   - `approved: true` (Claude Code: hook returns approved) → update `jeo-state.json` `phase` to `"execute"` and `plan_approved` to `true` → **enter STEP 2**
   - Not approved (Claude Code: hook returns feedback; others: `exit 10`) → read feedback, revise `plan.md` → repeat step 2
   - Infrastructure blocked (`exit 32`) → localhost bind unavailable (e.g., sandbox/CI). Use manual gate in TTY; confirm with user and retry outside sandbox in non-TTY
   - Session exited 3 times (`exit 30/31`) → ask user whether to end PLAN and decide to abort or resume

**NEVER: enter EXECUTE without `approved: true`. NEVER: run with `&` background.**
**NEVER: reopen the same unchanged plan after `approved` or `manual_approved` — it is already approved.**
**NEVER: treat `feedback_required` as approved — it means the plan was REJECTED and must be revised.**
**When `feedback_required` + same hash → exit 1 (not 0), revise plan content to get a new hash, then re-open plannotator.**

---

### STEP 2: EXECUTE

**Pre-flight (auto-detect team availability):**
```bash
# Record checkpoint
python3 -c "
import json,datetime,os,subprocess,fcntl
try:
    root=subprocess.check_output(['git','rev-parse','--show-toplevel'],stderr=subprocess.DEVNULL).decode().strip()
except:
    root=os.getcwd()
f=os.path.join(root,'.omc/state/jeo-state.json')
if os.path.exists(f):
    with open(f,'r+') as fh:
        fcntl.flock(fh,fcntl.LOCK_EX)
        try:
            d=json.load(fh)
            d.update({'checkpoint':'execute','updated_at':datetime.datetime.utcnow().isoformat()+'Z'})
            fh.seek(0); json.dump(d,fh,ensure_ascii=False,indent=2); fh.truncate()
        finally:
            fcntl.flock(fh,fcntl.LOCK_UN)
" 2>/dev/null || true

TEAM_AVAILABLE=false
if [[ "${CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS:-}" =~ ^(1|true|True|yes|YES)$ ]]; then
  TEAM_AVAILABLE=true
elif python3 -c "
import json, os, sys
try:
    s = json.load(open(os.path.expanduser('~/.claude/settings.json')))
    val = s.get('env', {}).get('CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS', '')
    sys.exit(0 if str(val) in ('1', 'true', 'True', 'yes') else 1)
except Exception:
    sys.exit(1)
" 2>/dev/null; then
  TEAM_AVAILABLE=true
fi
export TEAM_AVAILABLE_BOOL="$TEAM_AVAILABLE"
python3 -c "
import json,os,subprocess,fcntl
try:
    root=subprocess.check_output(['git','rev-parse','--show-toplevel'],stderr=subprocess.DEVNULL).decode().strip()
except:
    root=os.getcwd()
f=os.path.join(root,'.omc/state/jeo-state.json')
if os.path.exists(f):
    with open(f,'r+') as fh:
        fcntl.flock(fh,fcntl.LOCK_EX)
        try:
            d=json.load(fh)
            d['team_available']=os.environ.get('TEAM_AVAILABLE_BOOL','false').lower()=='true'
            fh.seek(0); json.dump(d,fh,ensure_ascii=False,indent=2); fh.truncate()
        finally:
            fcntl.flock(fh,fcntl.LOCK_UN)
" 2>/dev/null || true
```

1. Update `jeo-state.json` `phase` to `"execute"`
2. **Team available (Claude Code + omc)**:
   ```
   /omc:team 3:executor "<task>"
   ```
3. **Claude Code but no team**:
   ```
   echo "❌ JEO requires Claude Code team mode. Re-run bash scripts/setup-claude.sh, restart Claude Code, and confirm CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1."
   exit 1
   ```
   Never fall back to single-agent execution in Claude Code.
4. **No omc (BMAD fallback — Codex / Gemini / OpenCode only)**:
   ```
   /workflow-init   # Initialize BMAD
   /workflow-status # Check current step
   ```

---

### STEP 3: VERIFY

1. Update `jeo-state.json` `phase` to `"verify"`
2. **Basic verification with agent-browser** (when browser UI is present):
   ```bash
   agent-browser snapshot http://localhost:3000
   ```
3. `annotate` keyword detected → **enter STEP 3.1**
4. Otherwise → **enter STEP 4**

---

### STEP 3.1: VERIFY_UI (only when `annotate` keyword is detected)

1. Pre-flight check (required before entering):
   ```bash
   # Auto-start server, auto-install package, auto-inject component (see §3.3.1 for full script)
   bash scripts/ensure-agentation.sh --project-dir "${PROJECT_DIR:-$PWD}" --endpoint "http://localhost:4747" || true
   # If agentation-mcp server is still not healthy after pre-flight → graceful skip to STEP 4
   if ! curl -sf --connect-timeout 2 http://localhost:4747/health >/dev/null 2>&1; then
     python3 -c "
import json,os,subprocess,fcntl,time
try:
    root=subprocess.check_output(['git','rev-parse','--show-toplevel'],stderr=subprocess.DEVNULL).decode().strip()
except:
    root=os.getcwd()
f=os.path.join(root,'.omc/state/jeo-state.json')
if os.path.exists(f):
    with open(f,'r+') as fh:
        fcntl.flock(fh,fcntl.LOCK_EX)
        try:
            d=json.load(fh)
            d['last_error']='agentation-mcp not running; VERIFY_UI skipped'
            d['updated_at']=time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime())
            fh.seek(0); json.dump(d,fh,ensure_ascii=False,indent=2); fh.truncate()
        finally:
            fcntl.flock(fh,fcntl.LOCK_UN)
" 2>/dev/null || true
     # Proceed to STEP 4 CLEANUP (no exit 1 — graceful skip)
   fi
   ```
2. Update `jeo-state.json`: `phase = "verify_ui"`, `agentation.active = true`, `agentation.submit_gate_status = "waiting_for_submit"`
3. Wait for explicit human submit:
   - **Claude Code**: wait for `UserPromptSubmit` after the user presses **Send Annotations** / `onSubmit`
   - **Codex / Gemini / OpenCode**: wait until the human confirms submission and the agent emits `ANNOTATE_READY` (or compatibility alias `AGENTUI_READY`)
4. Before that submit signal arrives, do not read `/pending`, do not acknowledge annotations, and do not start the fix loop
5. After submit arrives, switch `agentation.submit_gate_status = "submitted"` and record `submit_signal`, `submit_received_at`, and `submitted_annotation_count`
6. **Claude Code (MCP)**: blocking call to `agentation_watch_annotations` (`batchWindowSeconds:10`, `timeoutSeconds:120`)
7. **Codex / Gemini / OpenCode (HTTP)**: polling loop via `GET http://localhost:4747/pending`
8. Process each annotation: `acknowledge` → navigate code via `elementPath` → apply fix → `resolve`
9. `count=0` or timeout → reset the submit gate or finish the sub-phase → **enter STEP 4**

**NEVER: process draft annotations before submit/onSubmit.**

---

### STEP 4: CLEANUP

**Pre-flight (check before entering):**
```bash
# Record checkpoint
python3 -c "
import json,datetime,os,subprocess,fcntl
try:
    root=subprocess.check_output(['git','rev-parse','--show-toplevel'],stderr=subprocess.DEVNULL).decode().strip()
except:
    root=os.getcwd()
f=os.path.join(root,'.omc/state/jeo-state.json')
if os.path.exists(f):
    with open(f,'r+') as fh:
        fcntl.flock(fh,fcntl.LOCK_EX)
        try:
            d=json.load(fh)
            d.update({'checkpoint':'cleanup','updated_at':datetime.datetime.utcnow().isoformat()+'Z'})
            fh.seek(0); json.dump(d,fh,ensure_ascii=False,indent=2); fh.truncate()
        finally:
            fcntl.flock(fh,fcntl.LOCK_UN)
" 2>/dev/null || true

if ! git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  echo "⚠️ Not a git repository — skipping worktree cleanup"
else
  UNCOMMITTED=$(git status --porcelain 2>/dev/null | wc -l | tr -d ' ')
  [[ "$UNCOMMITTED" -gt 0 ]] && echo "⚠️ ${UNCOMMITTED} uncommitted change(s) — recommend commit/stash before cleanup"
fi
```

1. Update `jeo-state.json` `phase` to `"cleanup"`
2. Worktree cleanup:
   ```bash
   bash scripts/worktree-cleanup.sh || git worktree prune
   ```
3. Update `jeo-state.json` `phase` to `"done"`

---

## 1. Quick Start

> **Source of truth**: `https://github.com/supercent-io/skills-template`
> Local paths like `~/.claude/skills/jeo/` are copies installed via `npx skills add`.
> To update to the latest version, reinstall using the command below.

```bash
# Install JEO (npx skills add — recommended)
npx skills add https://github.com/supercent-io/skills-template --skill jeo

# Full install (all AI tools + all components)
bash scripts/install.sh --all

# Check status
bash scripts/check-status.sh

# Individual AI tool setup
bash scripts/setup-claude.sh      # Claude Code plugin + hooks
bash scripts/setup-codex.sh       # Codex CLI developer_instructions
bash scripts/setup-gemini.sh      # Gemini CLI hooks + GEMINI.md
bash scripts/setup-opencode.sh    # OpenCode plugin registration
```

---

## 2. Installed Components

Tools that JEO installs and configures:

| Tool | Description | Install Command |
|------|------|-----------|
| **omc** (oh-my-claudecode) | Claude Code multi-agent orchestration | `/plugin marketplace add https://github.com/Yeachan-Heo/oh-my-claudecode` |
| **omx** | Multi-agent orchestration for OpenCode | `bunx oh-my-opencode setup` |
| **ohmg** | Multi-agent framework for Gemini CLI | `bunx oh-my-ag` |
| **bmad** | BMAD workflow orchestration | Included in skills |
| **ralph** | Self-referential completion loop | Included in omc or install separately |
| **plannotator** | Visual plan/diff review | Auto-installed during PLAN via `bash scripts/ensure-plannotator.sh` (or preinstall with `bash scripts/install.sh --with-plannotator`) |
| **agentation** | UI annotation → agent code fix integration (`annotate` keyword, `agentui` compatibility maintained) | `bash scripts/install.sh --with-agentation` |
| **agent-browser** | Headless browser for AI agents — **primary tool for browser behavior verification** | `npm install -g agent-browser` |
| **playwriter** | Playwright-based browser automation (optional) | `npm install -g playwriter` |

---

## 3. JEO Workflow

### Full Flow

```
jeo "<task>"
    │
    ▼
[1] PLAN (ralph + plannotator)
    Draft plan with ralph → visual review with plannotator → Approve/Feedback
    │
    ▼
[2] EXECUTE
    ├─ team available? → /omc:team N:executor "<task>"
    │                    staged pipeline: plan→prd→exec→verify→fix
    └─ no team?       → /bmad /workflow-init → run BMAD steps
    │
    ▼
[3] VERIFY (agent-browser — default behavior)
    Verify browser behavior with agent-browser
    → capture snapshot → confirm UI/functionality is working
    │
    ├─ with annotate keyword → [3.3.1] VERIFY_UI (agentation watch loop)
    │   agentation_watch_annotations blocking → annotation ack→fix→resolve loop
    │
    ▼
[4] CLEANUP
    After all work is done → bash scripts/worktree-cleanup.sh
    git worktree prune
```

### 3.1 PLAN Step (ralph + plannotator)

> **Platform note**: The `/ralph` slash command is only available in Claude Code (omc).
> Use the "alternative method" below for Codex/Gemini/OpenCode.

**Claude Code (omc):**
```bash
/ralph "jeo-plan: <task>" --completion-promise="PLAN_APPROVED" --max-iterations=5
```

**Codex / Gemini / OpenCode (alternative):**
```bash
# Session-isolated feedback directory (prevents concurrent run conflicts)
FEEDBACK_DIR=$(python3 -c "import hashlib,os; h=hashlib.md5(os.getcwd().encode()).hexdigest()[:8]; d=f'/tmp/jeo-{h}'; os.makedirs(d,exist_ok=True); print(d)" 2>/dev/null || echo '/tmp')
FEEDBACK_FILE="${FEEDBACK_DIR}/plannotator_feedback.txt"

# 1. Write plan.md directly, then review with plannotator (blocking — no &)
PLANNOTATOR_RUNTIME_HOME="${FEEDBACK_DIR}/.plannotator"
mkdir -p "$PLANNOTATOR_RUNTIME_HOME"
touch /tmp/jeo-plannotator-direct.lock && python3 -c "
import json
print(json.dumps({'tool_input': {'plan': open('plan.md').read(), 'permission_mode': 'acceptEdits'}}))
" | env HOME="$PLANNOTATOR_RUNTIME_HOME" PLANNOTATOR_HOME="$PLANNOTATOR_RUNTIME_HOME" plannotator > "$FEEDBACK_FILE" 2>&1
# ↑ Run without &: waits until user clicks Approve/Send Feedback in browser

# 2. Check result and branch
if python3 -c "
import json, sys
try:
    d = json.load(open('$FEEDBACK_FILE'))
    sys.exit(0 if d.get('approved') is True else 1)
except Exception:
    sys.exit(1)
" 2>/dev/null; then
  echo "PLAN_APPROVED"   # → enter EXECUTE step
else
  echo "PLAN_FEEDBACK"   # → read \"$FEEDBACK_FILE\", replan, repeat above
fi
```

> **Important**: Do not run with `&` (background). Must run blocking to receive user feedback.

Common flow:
- Generate plan document (`plan.md`)
- Run plannotator blocking → browser UI opens automatically
- Review plan in browser → Approve or Send Feedback
- Approve (`"approved":true`) → enter [2] EXECUTE step
- Feedback → read `/tmp/plannotator_feedback.txt` annotations and replan (loop)
- **exit 32 (sandbox/CI — Conversation Approval Mode)**:
  1. Output full `plan.md` content to user
  2. Ask: "⚠️ plannotator UI unavailable. Reply 'approve' to proceed or provide feedback."
  3. **WAIT for user response — do NOT proceed to EXECUTE**
  4. On approval → update `jeo-state.json` `plan_approved=true, plan_gate_status="manual_approved"` → EXECUTE
  5. On feedback → revise `plan.md`, retry loop, repeat

**Claude Code manual run:**
```
Shift+Tab×2 → enter plan mode → plannotator runs automatically when plan is complete
```

### 3.2 EXECUTE Step

**When team is available (Claude Code + omc):**
```bash
/omc:team 3:executor "jeo-exec: <task based on approved plan>"
```
- staged pipeline: team-plan → team-prd → team-exec → team-verify → team-fix
- Maximize speed with parallel agent execution

**When Claude Code team mode is unavailable:**
```bash
echo "❌ JEO requires /omc:team in Claude Code. Run bash scripts/setup-claude.sh, restart Claude Code, then retry."
exit 1
```
- Do not degrade to single-agent mode

**When team is unavailable (BMAD fallback — Codex / Gemini / OpenCode):**
```bash
/workflow-init   # Initialize BMAD workflow
/workflow-status # Check current step
```
- Proceed in order: Analysis → Planning → Solutioning → Implementation
- Review documents with plannotator after each step completes

### 3.3 VERIFY Step (agent-browser — default behavior)

When browser-based functionality is present, verify behavior with `agent-browser`.

```bash
# Capture snapshot from the URL where the app is running
agent-browser snapshot http://localhost:3000

# Check specific elements (accessibility tree ref method)
agent-browser snapshot http://localhost:3000 -i
# → check element state using @eN ref numbers

# Save screenshot
agent-browser screenshot http://localhost:3000 -o verify.png
```

> **Default behavior**: Automatically runs the agent-browser verification step when browser-related work is complete.
> Backend/CLI tasks without a browser UI skip this step.

### 3.3.1 VERIFY_UI Step (annotate — agentation watch loop)

Runs the agentation watch loop when the `annotate` keyword is detected. (The `agentui` keyword is also supported for backward compatibility.)
This follows the same pattern as plannotator operating in `planui` / `ExitPlanMode`.

**Prerequisites (auto-resolved by pre-flight):**
1. `npx agentation-mcp server` (HTTP :4747) is running — **auto-started if not running**
2. `agentation` npm package installed in the project — **auto-installed if absent**
3. `<Agentation endpoint="http://localhost:4747" />` is mounted in the app — **auto-injected into entry point if absent**

**Pre-flight Check (required before entering — common to all platforms):**
```bash
# ── Step 1: Auto-start agentation-mcp server if not running ─────────────────
JEO_AGENTATION_ENDPOINT="${JEO_AGENTATION_ENDPOINT:-http://localhost:4747}"
JEO_AGENTATION_PORT="${JEO_AGENTATION_PORT:-4747}"

if ! curl -sf --connect-timeout 2 "${JEO_AGENTATION_ENDPOINT}/health" >/dev/null 2>&1; then
  echo "[JEO][ANNOTATE] agentation-mcp not running — attempting auto-start on port ${JEO_AGENTATION_PORT}..."
  if command -v npx >/dev/null 2>&1; then
    npx -y agentation-mcp server --port "${JEO_AGENTATION_PORT}" >/tmp/agentation-mcp.log 2>&1 &
    AGENTATION_MCP_PID=$!
    echo "[JEO][ANNOTATE] started agentation-mcp (PID ${AGENTATION_MCP_PID})"
    # Wait up to 8 seconds for server to become healthy
    for i in $(seq 1 8); do
      sleep 1
      if curl -sf --connect-timeout 1 "${JEO_AGENTATION_ENDPOINT}/health" >/dev/null 2>&1; then
        echo "[JEO][ANNOTATE] ✅ agentation-mcp server ready"
        break
      fi
    done
    if ! curl -sf --connect-timeout 2 "${JEO_AGENTATION_ENDPOINT}/health" >/dev/null 2>&1; then
      echo "[JEO][ANNOTATE] ⚠️  agentation-mcp failed to start — skipping VERIFY_UI"
      python3 -c "
import json,os,subprocess,fcntl,time
try:
    root=subprocess.check_output(['git','rev-parse','--show-toplevel'],stderr=subprocess.DEVNULL).decode().strip()
except:
    root=os.getcwd()
f=os.path.join(root,'.omc/state/jeo-state.json')
if os.path.exists(f):
    with open(f,'r+') as fh:
        fcntl.flock(fh,fcntl.LOCK_EX)
        try:
            d=json.load(fh)
            d['last_error']='agentation-mcp failed to start; VERIFY_UI skipped'
            d['updated_at']=time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime())
            fh.seek(0); json.dump(d,fh,ensure_ascii=False,indent=2); fh.truncate()
        finally:
            fcntl.flock(fh,fcntl.LOCK_UN)
" 2>/dev/null || true
      # Proceed to STEP 4 CLEANUP (no exit 1 — graceful skip)
    fi
  else
    echo "[JEO][ANNOTATE] ⚠️  npx not found — cannot auto-start agentation-mcp. Skipping VERIFY_UI."
    python3 -c "
import json,os,subprocess,fcntl,time
try:
    root=subprocess.check_output(['git','rev-parse','--show-toplevel'],stderr=subprocess.DEVNULL).decode().strip()
except:
    root=os.getcwd()
f=os.path.join(root,'.omc/state/jeo-state.json')
if os.path.exists(f):
    with open(f,'r+') as fh:
        fcntl.flock(fh,fcntl.LOCK_EX)
        try:
            d=json.load(fh)
            d['last_error']='npx not found; agentation-mcp auto-start skipped; VERIFY_UI skipped'
            d['updated_at']=time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime())
            fh.seek(0); json.dump(d,fh,ensure_ascii=False,indent=2); fh.truncate()
        finally:
            fcntl.flock(fh,fcntl.LOCK_UN)
" 2>/dev/null || true
    # Proceed to STEP 4 CLEANUP (no exit 1 — graceful skip)
  fi
fi

# ── Step 2: Auto-install agentation package + inject <Agentation> if needed ──
# Only runs when server is confirmed healthy
if curl -sf --connect-timeout 2 "${JEO_AGENTATION_ENDPOINT}/health" >/dev/null 2>&1; then
  SESSIONS=$(curl -sf "${JEO_AGENTATION_ENDPOINT}/sessions" 2>/dev/null || echo "[]")
  S_COUNT=$(echo "$SESSIONS" | python3 -c "import sys,json; print(len(json.load(sys.stdin)))" 2>/dev/null || echo 0)

  if [ "$S_COUNT" -eq 0 ]; then
    echo "[JEO][ANNOTATE] No active sessions — running ensure-agentation.sh to install package and inject component..."

    # Locate ensure-agentation.sh (try common installation paths)
    ENSURE_SCRIPT=""
    for candidate in \
      "$(dirname "${BASH_SOURCE[0]:-$0}")/ensure-agentation.sh" \
      "$HOME/.claude/skills/jeo/scripts/ensure-agentation.sh" \
      "$HOME/.agent-skills/jeo/scripts/ensure-agentation.sh" \
      "$HOME/.codex/skills/jeo/scripts/ensure-agentation.sh"; do
      if [[ -f "$candidate" ]]; then
        ENSURE_SCRIPT="$candidate"
        break
      fi
    done

    if [[ -n "$ENSURE_SCRIPT" ]]; then
      ENSURE_EXIT=0
      bash "$ENSURE_SCRIPT" \
        --project-dir "${PROJECT_DIR:-$PWD}" \
        --endpoint "${JEO_AGENTATION_ENDPOINT}" || ENSURE_EXIT=$?

      if [ "$ENSURE_EXIT" -eq 0 ]; then
        echo "[JEO][ANNOTATE] ensure-agentation completed — waiting up to 15s for browser to reconnect..."
        # Wait for dev server hot-reload and browser reconnection
        for i in $(seq 1 15); do
          sleep 1
          NEW_S_COUNT=$(curl -sf "${JEO_AGENTATION_ENDPOINT}/sessions" 2>/dev/null | \
            python3 -c "import sys,json; print(len(json.load(sys.stdin)))" 2>/dev/null || echo 0)
          if [ "$NEW_S_COUNT" -gt 0 ]; then
            echo "[JEO][ANNOTATE] ✅ Browser session established (${NEW_S_COUNT} session(s))"
            S_COUNT=$NEW_S_COUNT
            break
          fi
        done
        if [ "$S_COUNT" -eq 0 ]; then
          echo "[JEO][ANNOTATE] ⚠️  Component injected but no browser session yet."
          echo "   → Refresh the browser at your app URL, then re-run annotate."
        fi
      elif [ "$ENSURE_EXIT" -eq 2 ]; then
        echo "[JEO][ANNOTATE] ℹ️  Not a Node.js project — mount <Agentation endpoint='${JEO_AGENTATION_ENDPOINT}' /> manually."
      else
        echo "[JEO][ANNOTATE] ⚠️  ensure-agentation.sh failed (exit $ENSURE_EXIT) — mount <Agentation endpoint='${JEO_AGENTATION_ENDPOINT}' /> manually."
      fi
    else
      echo "[JEO][ANNOTATE] ⚠️  ensure-agentation.sh not found — mount <Agentation endpoint='${JEO_AGENTATION_ENDPOINT}' /> manually."
    fi
  fi

  echo "[JEO][ANNOTATE] ✅ agentation ready — server OK, ${S_COUNT} session(s)"
fi
```

> After passing pre-flight (`else` branch), update jeo-state.json `phase` to `"verify_ui"`, set `agentation.active` to `true`, and set `agentation.submit_gate_status` to `"waiting_for_submit"`.
> Do not call `/pending` yet. Draft annotations are not actionable until the user explicitly submits them.

**Claude Code (direct MCP tool call):**
```
# annotate keyword detected (or agentui — backward compatible)
# 1. wait for UserPromptSubmit after the user clicks Send Annotations / onSubmit
# 2. the JEO submit-gate hook records submit_gate_status="submitted"
# 3. only then run the blocking agentation watch loop
#
# batchWindowSeconds:10 — receive annotations in 10-second batches
# timeoutSeconds:120   — auto-exit after 120 seconds with no annotations
#
# Per-annotation processing loop:
# 1. agentation_acknowledge_annotation({id})           — show 'processing' in UI
# 2. navigate code via annotation.elementPath (CSS selector) → apply fix
# 3. agentation_resolve_annotation({id, summary})      — mark 'done' + save summary
#
# Loop ends when annotation count=0 or timeout
```

> **Important**: `agentation_watch_annotations` is a blocking call. Do not run with `&` background.
> Same as plannotator's `approved:true` loop: annotation count=0 or timeout = completion signal.
> `annotate` is the primary keyword. `agentui` is a backward-compatible alias and behaves identically.

**Codex / Gemini / OpenCode (HTTP REST API fallback):**
```bash
START_TIME=$(date +%s)
TIMEOUT_SECONDS=120

# Required gate: do not enter the loop until the human has clicked Send Annotations
# and the platform has opened agentation.submit_gate_status="submitted".
while true; do
  # Timeout check
  NOW=$(date +%s)
  ELAPSED=$((NOW - START_TIME))
  if [ $ELAPSED -ge $TIMEOUT_SECONDS ]; then
    echo "[JEO] agentation polling timeout (${TIMEOUT_SECONDS}s) — some annotations may remain unresolved"
    break
  fi

  SUBMIT_GATE=$(python3 -c "
import json
try:
    print(json.load(open('.omc/state/jeo-state.json')).get('agentation', {}).get('submit_gate_status', 'idle'))
except Exception:
    print('idle')
" 2>/dev/null || echo "idle")
  if [ "$SUBMIT_GATE" != "submitted" ]; then
    sleep 2
    continue
  fi

  COUNT=$(curl -sf --connect-timeout 3 --max-time 5 http://localhost:4747/pending 2>/dev/null | python3 -c "import sys,json; data=sys.stdin.read(); d=json.loads(data) if data.strip() else {}; print(d.get('count', len(d.get('annotations', [])) if isinstance(d, dict) else 0))" 2>/dev/null || echo 0)
  [ "$COUNT" -eq 0 ] && break

  # Process each annotation:
  # a) Acknowledge (show as in-progress)
  curl -X PATCH http://localhost:4747/annotations/<id> \
    -H 'Content-Type: application/json' \
    -d '{"status": "acknowledged"}'

  # b) Navigate code via elementPath (CSS selector) → apply fix

  # c) Resolve (mark done + fix summary)
  curl -X PATCH http://localhost:4747/annotations/<id> \
    -H 'Content-Type: application/json' \
    -d '{"status": "resolved", "resolution": "<fix summary>"}'

  sleep 3
done
```

### 3.4 CLEANUP Step (automatic worktree cleanup)

```bash
# Runs automatically after all work is complete
bash scripts/worktree-cleanup.sh

# Individual commands
git worktree list                         # List current worktrees
git worktree prune                        # Clean up worktrees for deleted branches
bash scripts/worktree-cleanup.sh --force  # Force cleanup including dirty worktrees
```

> Default run removes only clean extra worktrees; worktrees with changes are left with a warning.
> Use `--force` only after review.

---

## 4. Platform Plugin Configuration

### 4.1 Claude Code

```bash
# Automatic setup
bash scripts/setup-claude.sh

# Or manually:
/plugin marketplace add https://github.com/Yeachan-Heo/oh-my-claudecode
/plugin install oh-my-claudecode
/omc:omc-setup

# Add plannotator hook
bash .agent-skills/plannotator/scripts/setup-hook.sh
```

**Config file**: `~/.claude/settings.json`
```json
{
  "hooks": {
    "PermissionRequest": [{
      "matcher": "ExitPlanMode",
      "hooks": [{
        "type": "command",
        "command": "python3 ~/.agent-skills/jeo/scripts/claude-plan-gate.py",
        "timeout": 1800
      }]
    }]
  }
}
```

**agentation MCP config** (`~/.claude/settings.json` or `.claude/mcp.json`):
```json
{
  "mcpServers": {
    "agentation": {
      "command": "npx",
      "args": ["-y", "agentation-mcp", "server"]
    }
  },
  "hooks": {
    "UserPromptSubmit": [{
      "matcher": "*",
      "hooks": [{
        "type": "command",
        "command": "python3 ~/.agent-skills/jeo/scripts/claude-agentation-submit-hook.py",
        "timeout": 300
      }]
    }]
  }
}
```

`bash ~/.agent-skills/jeo/scripts/setup-claude.sh` migrates stale `~/.agent-skills/omg/...` hook paths to the active JEO install and installs compatibility shims for legacy Claude setups.


### 4.2 Codex CLI

```bash
# Automatic setup
bash scripts/setup-codex.sh

# What gets configured:
# - developer_instructions: ~/.codex/config.toml
# - prompt file: ~/.codex/prompts/jeo.md
# - notify hook: ~/.codex/hooks/jeo-notify.py
# - [tui] notifications: agent-turn-complete
```

**agentation MCP config** (`~/.codex/config.toml`):
```toml
[mcp_servers.agentation]
command = "npx"
args = ["-y", "agentation-mcp", "server"]
```


**notify hook** (`~/.codex/hooks/jeo-notify.py`):
- Detects `PLAN_READY` signal in `last-assistant-message` when agent turn completes
- Confirms `plan.md` exists, compares the current hash against `last_reviewed_plan_hash`, and skips the gate when the plan was already reviewed
- Saves result to `/tmp/plannotator_feedback.txt`
- Detects `ANNOTATE_READY` signal (or backward-compatible `AGENTUI_READY`) only in `verify_ui`
- Opens `agentation.submit_gate_status="submitted"` first, then polls `http://localhost:4747/pending`

**`~/.codex/config.toml`** config:
```toml
developer_instructions = """
# JEO Orchestration Workflow
# ...
"""

notify = ["python3", "~/.codex/hooks/jeo-notify.py"]

[tui]
notifications = ["agent-turn-complete"]
notification_method = "osc9"
```

> `developer_instructions` must be a **top-level string**.
> Writing it as a `[developer_instructions]` table may cause Codex to fail on startup with `invalid type: map, expected a string`.
> `notify` and `[tui].notifications` must also be set correctly for the PLAN/ANNOTATE follow-up loop to actually work.

Using in Codex:
```bash
/prompts:jeo    # Activate JEO workflow
# Agent writes plan.md and outputs "PLAN_READY" → notify hook runs automatically
```

### 4.3 Gemini CLI

```bash
# Automatic setup
bash scripts/setup-gemini.sh

# What gets configured:
# - AfterAgent backup hook: ~/.gemini/hooks/jeo-plannotator.sh
# - Instructions (MANDATORY loop): ~/.gemini/GEMINI.md
```

**Key principle**: The agent must call plannotator **directly in blocking mode** to receive feedback in the same turn.
The AfterAgent hook serves only as a safety net (runs after turn ends → injected in next turn).

**AfterAgent backup hook** (`~/.gemini/settings.json`):
```json
{
  "hooks": {
    "AfterAgent": [{
      "matcher": "",
      "hooks": [{
        "name": "plannotator-review",
        "type": "command",
        "command": "bash ~/.gemini/hooks/jeo-plannotator.sh",
        "description": "Run plannotator when plan.md is detected (AfterAgent backup)"
      }]
    }]
  }
}
```

**PLAN instructions added to GEMINI.md (mandatory loop)**:
```
1. Write plan.md
2. Run plannotator blocking (no &) → /tmp/plannotator_feedback.txt
3. approved=true → EXECUTE / Not approved → revise and repeat step 2
NEVER proceed to EXECUTE without approved=true.
```

**agentation MCP config** (`~/.gemini/settings.json`):
```json
{
  "mcpServers": {
    "agentation": {
      "command": "npx",
      "args": ["-y", "agentation-mcp", "server"]
    }
  }
}
```

> **Note**: Gemini CLI hook events use `BeforeTool` and `AfterAgent`.
> `ExitPlanMode` is a Claude Code-only hook.

> [Hooks Official Guide](https://developers.googleblog.com/tailor-gemini-cli-to-your-workflow-with-hooks/)

### 4.4 OpenCode

```bash
# Automatic setup
bash scripts/setup-opencode.sh

# Added to opencode.json:
# "@plannotator/opencode@latest" plugin
# "@oh-my-opencode/opencode@latest" plugin (omx)
```

OpenCode slash commands:
- `/jeo-plan` — plan with ralph + plannotator
- `/jeo-exec` — execute with team/bmad
- `/jeo-annotate` — start agentation watch loop (annotate; `/jeo-agentui` is a deprecated alias)
- `/jeo-cleanup` — worktree cleanup




**plannotator integration** (MANDATORY blocking loop):
```bash
# Write plan.md then run PLAN gate (no &) — receive feedback in same turn
bash scripts/plannotator-plan-loop.sh plan.md /tmp/plannotator_feedback.txt 3
# - Must wait until approve/feedback is received
# - Auto-restart on session exit (up to 3 times)
# - After 3 exits, confirm with user whether to abort or resume
# - exit 32 if localhost bind unavailable (replace with manual gate in TTY)

# Branch based on result
# approved=true  → enter EXECUTE
# not approved   → apply feedback, revise plan.md → repeat above
```


**agentation MCP config** (`opencode.json`):
```json
{
  "mcp": {
    "agentation": {
      "type": "local",
      "command": ["npx", "-y", "agentation-mcp", "server"]
    }
  }
}
```


---

## 5. Memory & State

JEO stores state at the following paths:

```
{worktree}/.omc/state/jeo-state.json   # JEO execution state
{worktree}/.omc/plans/jeo-plan.md      # Approved plan
{worktree}/.omc/logs/jeo-*.log         # Execution logs
```

**State file structure:**
```json
{
  "mode": "jeo",
  "phase": "plan|execute|verify|verify_ui|cleanup|done",
  "session_id": "<uuid>",
  "task": "current task description",
  "plan_approved": true,
  "plan_gate_status": "pending|approved|feedback_required|infrastructure_blocked|manual_approved",
  "plan_current_hash": "<sha256 or null>",
  "last_reviewed_plan_hash": "<sha256 or null>",
  "last_reviewed_plan_at": "2026-02-24T00:00:00Z",
  "plan_review_method": "plannotator|manual|null",
  "team_available": true,
  "retry_count": 0,
  "last_error": null,
  "checkpoint": "plan|execute|verify|verify_ui|cleanup",
  "created_at": "2026-02-24T00:00:00Z",
  "updated_at": "2026-02-24T00:00:00Z",
  "agentation": {
    "active": false,
    "session_id": null,
    "keyword_used": null,
    "submit_gate_status": "idle|waiting_for_submit|submitted",
    "submit_signal": "claude-user-prompt-submit|codex-notify|gemini-manual|null",
    "submit_received_at": "2026-02-24T00:00:00Z",
    "submitted_annotation_count": 0,
    "started_at": null,
    "timeout_seconds": 120,
    "annotations": {
      "total": 0, "acknowledged": 0, "resolved": 0, "dismissed": 0, "pending": 0
    },
    "completed_at": null,
    "exit_reason": null
  }
}
```

> **agentation fields**: `active` — whether the watch loop is running (used as hook guard), `session_id` — for resuming,
> `submit_gate_status` — prevents processing draft annotations before submit/onSubmit, `submit_signal` — which platform opened the gate,
> `submit_received_at` / `submitted_annotation_count` — audit trail for the submitted batch, `exit_reason` — `"all_resolved"` | `"timeout"` | `"user_cancelled"` | `"error"`
>
> **dismissed annotations**: When a user dismisses an annotation in the agentation UI (status becomes `"dismissed"`),
> the agent should skip code changes for that annotation, increment `annotations.dismissed`, and continue to the next pending annotation.
> Dismissed annotations are counted but not acted upon. The watch loop exits normally when `pending == 0` (resolved + dismissed covers all).
>
> **`plan_review_method`**: set to `"plannotator"` when approved via UI, `"manual"` when approved via TTY fallback gate.
>
> **`cleanup_completed`**: set to `true` by `worktree-cleanup.sh` after successful worktree prune.

> **Error recovery fields**:
> - `retry_count` — number of retries after an error. Increments +1 on each pre-flight failure. Ask user to confirm if `>= 3`.
> - `last_error` — most recent error message. Used to identify the cause on restart.
> - `checkpoint` — last phase that was started. Resume from this phase on restart (`plan|execute|verify|cleanup`).

**Checkpoint-based resume flow:**
```bash
# Check checkpoint on restart
python3 -c "
import json, os, subprocess
try:
    root = subprocess.check_output(['git', 'rev-parse', '--show-toplevel'], stderr=subprocess.DEVNULL).decode().strip()
except:
    root = os.getcwd()
f = os.path.join(root, '.omc/state/jeo-state.json')
if os.path.exists(f):
    d=json.load(open(f))
    cp=d.get('checkpoint')
    err=d.get('last_error')
    rc=d.get('retry_count',0)
    print(f'Resume from: {cp or \"beginning\"}')
    if err: print(f'Previous error ({rc} time(s)): {err}')
    if rc >= 3: print('⚠️ Retry count exceeded 3 — user confirmation required')
"
```

Restore after restart:
```bash
# Check status and resume
bash scripts/check-status.sh --resume
```

---

## 6. Recommended Workflow

```
# Step 1: Install (once)
bash scripts/install.sh --all
bash scripts/check-status.sh

# Step 2: Start work
jeo "<task description>"           # Activate with keyword
# Or in Claude: Shift+Tab×2 → plan mode

# Step 3: Review plan with plannotator
# Approve or Send Feedback in browser UI

# Step 4: Automatic execution
# team or bmad handles the work

# Step 5: Cleanup after completion
bash scripts/worktree-cleanup.sh
```

---

## 7. Best Practices

1. **Plan first**: always review the plan with ralph+plannotator before executing (catches wrong approaches early)
2. **Team first**: omc team mode is most efficient in Claude Code
3. **bmad fallback**: use BMAD in environments without team (Codex, Gemini)
4. **Worktree cleanup**: run `worktree-cleanup.sh` immediately after work completes (prevents branch pollution)
5. **State persistence**: use `.omc/state/jeo-state.json` to maintain state across sessions
6. **annotate**: use the `annotate` keyword to run the agentation watch loop for complex UI changes (precise code changes via CSS selector). `agentui` is a backward-compatible alias.

---

## 8. Troubleshooting

| Issue | Solution |
|------|------|
| plannotator not running | JEO first auto-runs `bash scripts/ensure-plannotator.sh`; if it still fails, run `bash .agent-skills/plannotator/scripts/check-status.sh` |
| plannotator not opening in Claude Code | plannotator is hook-only. Do NOT call it via MCP or CLI. Use `EnterPlanMode` → write plan → `ExitPlanMode`; the hook fires automatically. Verify hook is set: `cat ~/.claude/settings.json \| python3 -c "import sys,json;h=json.load(sys.stdin).get('hooks',{});print(h.get('PermissionRequest','missing'))"` |
| plannotator feedback not received | Remove `&` background execution → run blocking, then check `/tmp/plannotator_feedback.txt` (Codex/Gemini/OpenCode only) |
| Same plan is repeatedly re-reviewed in Codex | Compare `last_reviewed_plan_hash` in `jeo-state.json` with the current `plan.md` hash. If they match and `plan_gate_status` is terminal, do not re-run |
| Codex startup failure (`invalid type: map, expected a string`) | Re-run `bash scripts/setup-codex.sh` and confirm `developer_instructions` in `~/.codex/config.toml` is a top-level string |
| Gemini feedback loop missing | Add blocking direct call instruction to `~/.gemini/GEMINI.md` |
| worktree conflict | `git worktree prune && git worktree list` |
| team mode not working | JEO requires team mode in Claude Code. Run `bash scripts/setup-claude.sh`, restart Claude Code, and verify `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1` before retrying |
| omc install failed | Run `/omc:omc-doctor` |
| agent-browser error | Check `agent-browser --version` |
| annotate (agentation) not opening | Check `curl http://localhost:4747/health` and `curl http://localhost:4747/sessions`. JEO waits for explicit submit/onSubmit before polling `/pending` |
| annotation not reflected in code | Confirm `summary` field is present when calling `agentation_resolve_annotation` |
| `agentui` keyword not activating | Use the `annotate` keyword (new). `agentui` is a deprecated alias but still works. |
| MCP tool not registered (Codex/Gemini) | Re-run `bash scripts/setup-codex.sh` / `setup-gemini.sh` |

---

## 9. References

- [oh-my-claudecode](https://github.com/Yeachan-Heo/oh-my-claudecode) — Claude Code multi-agent
- [plannotator](https://plannotator.ai) — visual plan/diff review
- [BMAD Method](https://github.com/bmad-dev/BMAD-METHOD) — structured AI development workflow
- [Agent Skills Spec](https://agentskills.io/specification) — skill format specification
- [agentation](https://github.com/benjitaylor/agentation) — UI annotation → agent code fix integration (`annotate`; `agentui` backward compatible)
