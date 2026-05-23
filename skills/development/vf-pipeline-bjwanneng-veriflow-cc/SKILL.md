---
name: vf-pipeline
description: Use this skill to start or resume the VeriFlow RTL hardware design pipeline (architect to synth). Trigger this when the user asks to "run the RTL flow", "design hardware", or "start the pipeline". Pass the project directory path as the argument.
---

# RTL Pipeline Orchestrator

This skill IS the plan — execute each stage immediately using Read/Write/Bash/Agent tools. Do NOT plan before executing.

Project directory path: `$ARGUMENTS`

If `$ARGUMENTS` is empty, ask the user for it.

**Variable**: `${CLAUDE_SKILL_DIR}` is set by Claude Code to the skill's installed directory.

---

## Step 0: Initialization

Run the initialization script:

```bash
PY_INIT="${PYTHON_EXE:-python}"
cd "$ARGUMENTS" && "$PY_INIT" "${CLAUDE_SKILL_DIR}/init.py" "$ARGUMENTS"
source "$ARGUMENTS/.veriflow/eda_env.sh"
```

Read the output to determine: new project or resuming. If resuming, skip stages in `stages_completed`.

## Step 0b: Requirements Clarification

Read ALL input files in parallel (single message with multiple Read calls):
- `$ARGUMENTS/requirement.md` (required)
- `$ARGUMENTS/constraints.md` (optional)
- `$ARGUMENTS/design_intent.md` (optional)
- `$ARGUMENTS/context/*.md` files

Check each category below. If input files already answer it → note "confirmed" and skip. Only ask about what's missing or ambiguous. Use AskUserQuestion with up to 4 questions per call.

**A.** Functional clarity: module functionality, interface protocol, data format, FSM behavior, clock domain crossings
**B.** Constraint clarity: clock frequency, target platform, area/power budget, reset strategy, IO standards
**C.** Design intent: architecture style, module partitioning, interface preferences, IP reuse, key decisions
**D.** Algorithm & protocol: algorithm reference, pseudocode, key formulas, test vectors
**E.** Timing completeness: cycle-level behavior, latency, throughput, interface timing, reset recovery, backpressure
**F.** Domain knowledge: design domain, standard reference, prerequisite concepts, test vectors
**G.** Information completeness: implicit assumptions, missing scenarios

After resolved, write `$ARGUMENTS/.veriflow/clarifications.md` with all answers.

## Step 0c: Create task list

Create one task per pipeline stage (skip if resuming and already completed):

- `Stage 1: spec_golden`
- `Stage 2: codegen`
- `Stage 3: verify_fix`
- `Stage 4: lint_synth`

---

## Stage Pattern (ALL stages follow this)

Every stage MUST execute these 3 steps in order:

**Pre-stage:**
```bash
source "$PROJECT_DIR/.veriflow/eda_env.sh" && $PYTHON_EXE "${CLAUDE_SKILL_DIR}/state.py" "$PROJECT_DIR" "<STAGE>" --start
```

**Execute:** dispatch agents (Stages 1/2/4) or run inline (Stage 3)

**Post-stage:**
```bash
source "$PROJECT_DIR/.veriflow/eda_env.sh" && $PYTHON_EXE "${CLAUDE_SKILL_DIR}/state.py" "$PROJECT_DIR" "<STAGE>" --hook="<HOOK_CMD>" --journal-outputs="<FILES>" --journal-notes="<NOTES>"
```
Then: `TaskUpdate` mark the stage task as completed.

---

## Stage 1: spec_golden

Run **vf-spec-gen** first. The cycle_timing and timing_contract fields in
spec.json are the timing source of truth for both golden_model.py and RTL.

- **vf-spec-gen** (subagent_type: general-purpose)
  - Prompt includes: PROJECT_DIR, CLARIFICATIONS path, `${CLAUDE_SKILL_DIR}/templates` path, all input file contents inline

After vf-spec-gen returns, read `workspace/docs/spec.json`.

Then run **vf-golden-gen**:

- **vf-golden-gen** (subagent_type: general-purpose)
  - Prompt includes: PROJECT_DIR, CLARIFICATIONS path, SPEC_JSON content, `${CLAUDE_SKILL_DIR}/templates` path, all input file contents inline

After vf-golden-gen returns:

**Timing contract check** (pre-verification, before codegen):
```bash
$PYTHON_EXE "${CLAUDE_SKILL_DIR}/timing_contract_checker.py" \
    --spec workspace/docs/spec.json \
    --golden workspace/docs/golden_model.py \
    --output logs/timing_check.json
```
If this reports errors, review `logs/timing_check.json` and fix spec.json or golden_model.py before proceeding. The check is non-blocking but errors indicate timing contradictions that will cause RTL bugs.

```bash
state.py "$PROJECT_DIR" "spec_golden" --hook="test -f workspace/docs/spec.json && test -f workspace/docs/golden_model.py" --journal-outputs="workspace/docs/spec.json, workspace/docs/golden_model.py" --journal-notes="Specification generated first; golden model aligned to spec timing"
```
TaskUpdate complete.

---

## Stage 2: codegen

Read spec.json, golden_model.py, and coding_style.md (parallel Read calls) to include inline in prompts.

Dispatch ALL agents in parallel (single message):

- **One vf-coder per module** in spec.json (subagent_type: general-purpose)
  - Prompt includes: MODULE_NAME, OUTPUT_FILE path, spec.json content, golden_model.py content, coding_style.md content
  - For top modules: include submodule port definitions from spec.json
  - For leaf modules: include only that module's spec entry
- **One vf-tb-gen** (subagent_type: general-purpose)
  - Prompt includes: PROJECT_DIR, DESIGN_NAME, spec.json content, golden_model.py content, COCOTB_AVAILABLE flag, `${CLAUDE_SKILL_DIR}/templates` path

After ALL return, verify outputs exist:
```bash
ls "$PROJECT_DIR/workspace/rtl/"*.v "$PROJECT_DIR/workspace/tb/"*.v "$PROJECT_DIR/workspace/tb/"*.py 2>/dev/null
```
```bash
state.py "$PROJECT_DIR" "codegen" --hook="ls workspace/rtl/*.v >/dev/null 2>&1 && (test -f workspace/tb/test_*.py || test -f workspace/tb/tb_*.v)" --journal-outputs="workspace/rtl/*.v, workspace/tb/test_*.py, workspace/tb/tb_*.v" --journal-notes="RTL and testbench generated in parallel"
```
TaskUpdate complete.

---

## Stage 3: verify_fix (inline — runs in main session)

**IMPORTANT**: This stage runs inline because error recovery needs main session context for Edit tool.

Pre-stage:
```bash
source "$PROJECT_DIR/.veriflow/eda_env.sh" && $PYTHON_EXE "${CLAUDE_SKILL_DIR}/state.py" "$PROJECT_DIR" "verify_fix" --start
```

### Golden Model Self-Check (BEFORE simulation)

If golden_model.py exists, verify it passes its own test vectors first.
This catches golden model bugs BEFORE wasting time on RTL debugging.

```bash
source "$PROJECT_DIR/.veriflow/eda_env.sh"
cd "$PROJECT_DIR"
if [ -f workspace/docs/golden_model.py ]; then
    $PYTHON_EXE "${CLAUDE_SKILL_DIR}/iverilog_runner.py" \
        --golden-check workspace/docs/golden_model.py 2>&1 | tee logs/golden_selfcheck.log
    if [ $? -ne 0 ]; then
        echo "[GOLDEN] Self-check FAILED — the reference model has bugs."
        echo "[GOLDEN] Fix golden_model.py FIRST. The problem is NOT in the RTL."
        # Do NOT consume retry budget — this is a golden model issue
        state.py "$PROJECT_DIR" "verify_fix" \
            --hook="test -f workspace/docs/golden_model.py" \
            --journal-outputs="logs/golden_selfcheck.log" \
            --journal-notes="Golden model self-check failed — golden model has bugs"
        # STOP and notify user to fix the golden model before retrying
    fi
fi
```

### Cocotb per-cycle verification (if cocotb available)

Before running Verilog simulation, run cocotb with per-cycle internal signal
comparison. This is the PRIMARY debugging tool — it finds the FIRST divergence
point automatically, instead of only checking final outputs.

```bash
if command -v cocotb-config &>/dev/null; then
    cd "$PROJECT_DIR/workspace/tb"
    make SIM=icarus 2>&1 | tee "$PROJECT_DIR/logs/cocotb.log"
    cd "$PROJECT_DIR"
    if grep -q "FIRST DIVERGENCE" logs/cocotb.log; then
        echo "[COCOTB] Internal signal mismatch found — see cocotb.log for details"
        # Extract first divergence info — this is the PRIMARY diagnostic
        # for error_recovery.md. Do NOT guess the root cause.
    fi
fi
```

If cocotb is not available, proceed with Verilog simulation as before.

### Run simulation

```bash
source "$PROJECT_DIR/.veriflow/eda_env.sh"
cd "$PROJECT_DIR"
TOP_MODULE=$($PYTHON_EXE -c "
import json
for m in json.load(open('workspace/docs/spec.json')).get('modules', []):
    if m.get('module_type') == 'top': print(m['module_name']); break
")
VERILOG_TB=$(ls workspace/tb/tb_*.v 2>/dev/null | head -1)
$PYTHON_EXE "${CLAUDE_SKILL_DIR}/iverilog_runner.py" \
    --module $TOP_MODULE --rtl-dir workspace/rtl --tb-file "$VERILOG_TB" \
    --build-dir workspace/sim --verbose 2>&1 | tee logs/sim.log
```

### If PASS

```bash
state.py "$PROJECT_DIR" "verify_fix" --hook="grep -q 'ALL TESTS PASSED' logs/sim.log" --journal-outputs="logs/sim.log" --journal-notes="Simulation passed"
```
TaskUpdate complete. Go to Stage 4.

### If FAIL

1. **Read** `${CLAUDE_SKILL_DIR}/error_recovery.md` — follow the full procedure
2. **Collect data**: read `logs/sim.log`, run vcd2table diff, classify bug type
3. **5-point root cause analysis** → write to `stage_journal.md`
4. **Fix RTL** using Edit tool
5. **Re-run simulation** (go back to "Run simulation" above)
6. **Retry budget**: 3 attempts total
   - 1st fail: fix RTL, retry
   - 2nd fail: `state.py --reset codegen`, restart from Stage 2
   - 3rd fail: STOP, notify user

---

## Stage 4: lint_synth

Dispatch 2 parallel agents (single message):

- **vf-linter** (subagent_type: general-purpose) — include PROJECT_DIR, EDA_ENV path, PYTHON_EXE, SKILL_DIR
- **vf-synthesizer** (subagent_type: general-purpose) — include PROJECT_DIR, SPEC path, EDA_ENV path, PYTHON_EXE, SKILL_DIR

After BOTH return:

If lint failed → fix syntax errors in main session, re-run lint only.
If synth failed → check report, fix if needed.

```bash
state.py "$PROJECT_DIR" "lint_synth" --hook="test -f logs/lint.log && test -f workspace/synth/synth_report.txt" --journal-outputs="logs/lint.log, workspace/synth/synth_report.txt" --journal-notes="Lint and synthesis complete"
```
TaskUpdate complete. Pipeline done.

---

## Design Rules Summary

See `${CLAUDE_SKILL_DIR}/design_rules.md` for full rules.

- Synchronous active-high reset named `rst`
- Port naming: `_n` suffix for active-low, `_i`/`_o` for direction
- **Verilog-2005 only** — NO SystemVerilog
- Interface Lock: port names, handshake protocols, and module hierarchy are frozen after Stage 1
