---
name: operating-loop-workflow
description: Install and run the operating-loop multi-agent Workflow (the seven-move loop) for AgentOps plugin users.
practices:
- pragmatic-programmer
- agile-manifesto
hexagonal_role: driving-adapter
consumes: []
produces:
- git-changes
context_rel: []
skill_api_version: 1
context:
  window: inherit
  intent:
    mode: task
  intel_scope: none
metadata:
  tier: execution
  dependencies: []
output_contract: 'installs ~/.claude/workflows/operating-loop.js, then invokes the operating-loop Workflow; returns its structured result'
---
# /operating-loop-workflow

> **One job:** Make the `operating-loop` multi-agent Workflow available to this install, then run it.

**YOU MUST EXECUTE THIS WORKFLOW. Do not just describe it.**

The seven-move operating loop (shape → plan → pre-flight → implement → capture) ships as a
Claude Code **Workflow-tool** script at `.claude/workflows/operating-loop.js`. Claude Code
plugins do **not** auto-load `.claude/workflows/` from an install — workflows resolve only from
the project cwd or `~/.claude/workflows/`. So this skill installs the bundled script into the
user workflows directory, then invokes it.

## Steps — run in order

1. **Install the workflow (idempotent — only copies when the bundled script is newer or missing):**
   ```bash
   mkdir -p "$HOME/.claude/workflows"
   src="${CLAUDE_PLUGIN_ROOT}/.claude/workflows/operating-loop.js"
   dst="$HOME/.claude/workflows/operating-loop.js"
   if [ -f "$src" ] && { [ ! -f "$dst" ] || [ "$src" -nt "$dst" ]; }; then
     cp "$src" "$dst" && echo "installed operating-loop workflow -> $dst"
   else
     echo "operating-loop workflow already current (or bundle not found)"
   fi
   ```
2. **Run it** via the Workflow tool, passing the user's capability/intent as `args`:
   - Full loop: `Workflow({ name: "operating-loop", args: "<the capability/intent to drive through the loop>" })`
   - Plan-only (the safe Shape → Plan → Pre-flight half, no implementation):
     `Workflow({ name: "operating-loop", args: { mode: "plan", intent: "<intent>" } })`
3. **Report** the returned `intent`, `plan`, pre-flight `verdicts`, and `closeout` to the user.

## Notes

- After step 1 succeeds once, the workflow is invocable directly via the Workflow tool (`Workflow({name:'operating-loop'})`) in future sessions — this skill is the installer + first-run entry point.
- The script is a leaf Workflow (it does not nest other workflows). Source of truth: `.claude/workflows/operating-loop.js`.
- Re-running step 1 is safe and cheap; it copies only when the bundled script is newer.
