---
name: phase-transition
description: Transition between session phases (RESEARCH → PLAN → IMPLEMENT → REVIEW → VERIFY)
disable-model-invocation: true
---

# Phase Transition

Manages transitions between structured session phases. Each phase writes output to a file, and `/clear` between phases keeps context fresh.

## Phase Order

RESEARCH → PLAN → IMPLEMENT → REVIEW → VERIFY

## How to Use

1. **Check current phase state:**
   ```bash
   cat .claude/phases/output/current-phase.json 2>/dev/null || echo "No active phase"
   ```

2. **Write current phase output** to the appropriate output file:
   - RESEARCH → `.claude/phases/output/research-<topic>.md`
   - PLAN → `docs/plans/<date>-<topic>-plan.md`
   - IMPLEMENT → `.claude/phases/output/implement-<topic>.md`
   - REVIEW → `.claude/phases/output/review-<topic>.md`
   - VERIFY → `.claude/phases/output/verify-<topic>.md`

3. **Run checkpoint evaluation** (blocks transition if criteria fail):
   ```bash
   $CLAUDE_PROJECT_DIR/.claude/hooks/checkpoint-eval.sh "<current-phase>" "<next-phase>" "<topic>"
   ```
   - If exit code 0: PASS — proceed to update phase state
   - If exit code 1: FAIL — show findings. To override: pass `--force` flag and note the override
   - Eval results saved to `.claude/phases/output/eval-<topic>.json`

4. **Update phase state:**
   ```bash
   mkdir -p .claude/phases/output
   cat > .claude/phases/output/current-phase.json << 'PHASE_EOF'
   {
     "topic": "<topic>",
     "current_phase": "<next-phase>",
     "completed_phases": ["<completed>", ...],
     "started_at": "<ISO-timestamp>",
     "output_files": {
       "<phase>": "<path-to-output>"
     }
   }
   PHASE_EOF
   ```

5. **Suggest to user:** "Phase <current> complete. Output saved to `<path>`. Recommend `/clear` before starting <next> phase."

6. **Tell next session:** "Read `.claude/phases/output/current-phase.json` to see current phase. Load the appropriate context mode from `.claude/contexts/<mode>.md`."

## Starting a New Topic

```bash
mkdir -p .claude/phases/output
cat > .claude/phases/output/current-phase.json << 'PHASE_EOF'
{
  "topic": "<topic-name>",
  "current_phase": "research",
  "completed_phases": [],
  "started_at": "<ISO-timestamp>",
  "output_files": {}
}
PHASE_EOF
```

## Regressing to a Previous Phase

When a phase fails (e.g., REVIEW finds critical issues requiring more implementation):

1. **Log the regression reason:**
   ```bash
   PHASE_FILE=".claude/phases/output/current-phase.json"
   export PT_PHASE_FILE="$PHASE_FILE"
   export PT_TARGET="<target-phase>"
   export PT_REASON="<why regressing>"
   python3 << 'REGRESS_EOF'
   import json, os
   from datetime import datetime

   phase_file = os.environ["PT_PHASE_FILE"]
   target = os.environ["PT_TARGET"]
   reason = os.environ["PT_REASON"]

   with open(phase_file) as f:
       state = json.load(f)

   regressions = state.get("regressions", [])
   regressions.append({
       "from": state["current_phase"],
       "to": target,
       "reason": reason,
       "date": datetime.now().isoformat()
   })
   state["regressions"] = regressions

   # Remove target phase from completed if present
   completed = state.get("completed_phases", [])
   if target in completed:
       completed.remove(target)
   state["completed_phases"] = completed
   state["current_phase"] = target

   with open(phase_file, "w") as f:
       json.dump(state, f, indent=2)
   REGRESS_EOF
   ```

2. **No checkpoint eval needed** — regressions always allowed.

3. **Suggest to user:** "Phase regressed from <current> to <target>. Reason: <reason>. Recommend `/clear` before restarting <target> phase."

### Common Regression Scenarios

| From | To | When |
|------|----|------|
| REVIEW | IMPLEMENT | Critical/high issues found in review |
| VERIFY | IMPLEMENT | E2E tests failing, needs code fix |
| VERIFY | REVIEW | Found issues during verification that need re-review |

## Completing All Phases

After VERIFY passes, clean up:
```bash
rm -f .claude/phases/output/current-phase.json
# Keep output files for reference — they're gitignored
```
