---
name: vf-rtl
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
[ -f "$ARGUMENTS/.veriflow/eda_env.sh" ] && source "$ARGUMENTS/.veriflow/eda_env.sh"
```

Read the output to determine: new project or resuming. If resuming, skip stages in `stages_completed`.

### Stale-Stage Recovery (resume only)

When resuming, if a stage is STARTED but not COMPLETE, the pipeline may have been
interrupted or crashed. Before re-dispatching that stage, check if the output files
already exist by looking for completion markers (`.veriflow/done_<stage>*`):

```bash
cd "$ARGUMENTS"
# For spec_golden: check if both outputs exist and marker is present
if [ -f ".veriflow/done_spec_golden" ] && [ -f "workspace/docs/spec.json" ] && [ -f "workspace/docs/golden_model.py" ]; then
    echo "[RECOVERY] spec_golden outputs exist — running hook to mark complete"
    python3 "${CLAUDE_SKILL_DIR}/state.py" "$ARGUMENTS" "spec_golden" \
        --hook="test -f workspace/docs/spec.json && test -f workspace/docs/golden_model.py"
fi

# For codegen: check if ALL module .v files and TB files exist
if ls .veriflow/done_codegen_* >/dev/null 2>&1; then
    echo "[RECOVERY] codegen completion markers found — verifying outputs"
    python3 "${CLAUDE_SKILL_DIR}/state.py" "$ARGUMENTS" "codegen" \
        --hook="ls workspace/rtl/*.v >/dev/null 2>&1 && (test -f workspace/tb/test_*.py || test -f workspace/tb/tb_*.v)" \
        --journal-outputs="workspace/rtl/*.v, workspace/tb/test_*.py, workspace/tb/tb_*.v" \
        --journal-notes="Recovered from interrupted codegen via completion markers"
fi
```

If the hook passes, the stage is marked COMPLETE and the pipeline advances. If it
fails, stale markers are cleaned up and the stage is re-dispatched normally:

```bash
rm -f .veriflow/done_codegen_* .veriflow/done_spec_golden .veriflow/done_tb_gen
```

### Permission Check (sub-agent tools)

Sub-agents cannot interact with the user — any permission prompt will hang the pipeline.
Check that the following tools are pre-approved in the project's `.claude/settings.json`:

> **Heads-up — the allow-list below is the minimum.** Sub-agents also run shell
> commands like `source`, `cd`, `iverilog`, `vvp`, `yosys`, `mkdir`, `ls`,
> `xargs`. Those are NOT auto-added here because the right scope is environment-
> dependent. Two ways to keep the pipeline from hanging on a permission prompt:
>
> 1. Launch Claude Code with `--permission-mode acceptEdits` (or rely on
>    `~/.claude/settings.json` setting `skipDangerousModePermissionPrompt: true`).
> 2. Or, extend `.claude/settings.json` allow-list with the patterns above
>    (e.g. `"Bash(source*)"`, `"Bash(iverilog*)"`, `"Bash(yosys*)"`).
>
> If Stage 2/3/4 hangs silently, the cause is almost always one of these
> unlisted commands waiting on an invisible permission dialog.

```bash
SETTINGS=".claude/settings.json"
if [ ! -f "$SETTINGS" ]; then
    echo '{"permissions":{"allow":[]}}' > "$SETTINGS"
fi
python3 -c "
import json
s = json.load(open('$SETTINGS'))
allow = s.setdefault('permissions', {}).setdefault('allow', [])
# Tools that sub-agents need (must not trigger permission dialog):
# - WebSearch: main session only (sub-agents do not have it)
# - Bash(python*): all agents run python for hook validation
# - Bash(test*): agents run 'test -f ...' for file existence checks
# - Write: agents write output files (spec.json, golden_model.py, etc.)
needed = [
    'Bash(python*)',
    'Bash(python3*)',
    'Bash(test*)',
]
added = []
for tool in needed:
    if not any(tool in rule for rule in allow):
        allow.append(tool)
        added.append(tool)
if added:
    json.dump(s, open('$SETTINGS','w'), indent=2)
    print(f'[PERM] Added to allowlist: {added}')
else:
    print('[PERM] All sub-agent tools already allowed')
"
```

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
[ -f "$PROJECT_DIR/.veriflow/eda_env.sh" ] && source "$PROJECT_DIR/.veriflow/eda_env.sh" && $PYTHON_EXE "${CLAUDE_SKILL_DIR}/state.py" "$PROJECT_DIR" "<STAGE>" --start
```

**Execute:** dispatch agents (Stages 1/2/4) or run inline (Stage 3)

**Post-stage:**
```bash
[ -f "$PROJECT_DIR/.veriflow/eda_env.sh" ] && source "$PROJECT_DIR/.veriflow/eda_env.sh" && $PYTHON_EXE "${CLAUDE_SKILL_DIR}/state.py" "$PROJECT_DIR" "<STAGE>" --hook="<HOOK_CMD>" --journal-outputs="<FILES>" --journal-notes="<NOTES>"
```
Then: `TaskUpdate` mark the stage task as completed.

---

## Stage 1: spec_golden

### Pre-stage: Web Research

**Read requirement.md** (run in main session) to decide if WebSearch is needed.
Do NOT read templates or other input files — the agent will read them itself.

**Web Research** (run in main session, only if needed):

After reading requirement.md, judge whether WebSearch is needed:
- If `requirement.md` + `context/*.md` already contain: algorithm specification, test vectors,
  pin/protocol definitions, and enough detail to build spec.json and golden_model.py →
  **skip WebSearch**. Write a note to `$PROJECT_DIR/.veriflow/web_research.md`:
  ```
  # Web research skipped — input files provide sufficient detail
  Algorithm: <name>, source: <which files had the info>
  ```
- Otherwise, extract the algorithm/design name from `requirement.md`, then use WebSearch:
  - `"<algorithm_name> specification test vectors"` — for spec.json constraints
  - `"<algorithm_name> Verilog RTL reference"` — for coder patterns
  Store results in `$PROJECT_DIR/.veriflow/web_research.md`

### Agent Dispatch: Single spec-golden agent

**Build INPUT_FILES list** (paths only, no content):
```
INPUT_FILES:
- $PROJECT_DIR/requirement.md
- $PROJECT_DIR/constraints.md (if exists)
- $PROJECT_DIR/design_intent.md (if exists)
- $PROJECT_DIR/context/*.md (if any)
- $PROJECT_DIR/.veriflow/clarifications.md
- $PROJECT_DIR/.veriflow/web_research.md (if exists)
```

**Run vf-spec-golden** (single Agent call):

- **vf-spec-golden** (subagent_type: general-purpose)
  - Prompt includes: PROJECT_DIR, TEMPLATES_DIR (path to `${CLAUDE_SKILL_DIR}/templates`),
    INPUT_FILES (list of paths), CLARIFICATIONS path
  - DO NOT embed template content or input file content in the prompt.
  - The agent reads all files itself using its Read tool, then generates
    **both** spec.json and golden_model.py in one pass,
    with timing alignment done internally (it writes spec.json first, then uses
    its cycle_timing to align golden_model.py trace cycles).

After it returns:

1. Read `workspace/docs/spec.json` and `workspace/docs/golden_model.py` to verify.

**Golden model self-check** (pre-codegen gate — run FIRST to catch syntax errors):

Before proceeding to Stage 2, verify that golden_model.py passes its own test
vectors. This catches algorithmic and syntax bugs before RTL is generated.

```bash
cd "$PROJECT_DIR"
if [ -f workspace/docs/golden_model.py ]; then
    $PYTHON_EXE "${CLAUDE_SKILL_DIR}/iverilog_runner.py" \
        --golden-check workspace/docs/golden_model.py 2>&1 | tee logs/golden_selfcheck.log
    # ${PIPESTATUS[0]} reads the runner's exit, not tee's. Bash-only.
    if [ "${PIPESTATUS[0]}" -ne 0 ]; then
        echo "[GOLDEN] Self-check FAILED — fix golden_model.py before proceeding."
        $PYTHON_EXE "${CLAUDE_SKILL_DIR}/state.py" "$PROJECT_DIR" "spec_golden" --fail
        echo "[GOLDEN] Stage 1 marked failed; Stage 2 will not run. Main session: fix golden_model.py and re-run Stage 1."
        exit 1
    fi
fi
```

**Timing contract check** (pre-verification, before codegen):
```bash
$PYTHON_EXE "${CLAUDE_SKILL_DIR}/timing_contract_checker.py" \
    --spec workspace/docs/spec.json \
    --golden workspace/docs/golden_model.py \
    --output logs/timing_check.json
```
If this reports errors, **auto-fix first** — the checker can correct most common timing contract mistakes (registered→combinational delays, missing handshake fields, latency mismatches):
```bash
$PYTHON_EXE "${CLAUDE_SKILL_DIR}/timing_contract_checker.py" \
    --fix \
    --spec workspace/docs/spec.json \
    --golden workspace/docs/golden_model.py \
    --output logs/timing_check.json
```
Re-run the checker after `--fix` to confirm all errors are resolved. Only if errors remain after auto-fix, review `logs/timing_check.json` and manually fix spec.json or golden_model.py. Errors indicate timing contradictions that will cause RTL bugs.


**Streaming fill latency check** (pre-codegen gate):

If any module in spec.json has a non-zero `pipeline_delay_cycles` but is missing
`streaming_fill_latency_cycles`, verify whether the module has a fill/buffering
phase (line buffer, FIFO, shift-register window). If it does, the orchestrator
MUST ensure that downstream delay-matching paths use `total_latency_cycles`
(= `pipeline_delay_cycles + streaming_fill_latency_cycles`), not just the raw
`pipeline_delay_cycles`.

```bash
$PYTHON_EXE -c "
import json
spec = json.load(open('workspace/docs/spec.json'))
for m in spec.get('modules', []):
    tc = m.get('timing_contract', {})
    pd = tc.get('pipeline_delay_cycles', 0)
    sf = tc.get('streaming_fill_latency_cycles')
    name = m.get('module_name', '')
    if sf is None:
        print(f'[INFO] {name}: pipeline_delay_cycles={pd}, no streaming_fill_latency_cycles declared')
    else:
        print(f'[OK] {name}: pipeline_delay_cycles={pd}, streaming_fill={sf}')
    if sf is None and pd > 0:
        print(f'[CHECK] {name}: verify whether this module has a fill phase before first output. If yes, add streaming_fill_latency_cycles to its timing_contract.')
"
```
If any module has `pd > 0` and no `streaming_fill_latency_cycles`, the
orchestrator reviews its architecture to determine whether a fill phase exists.
Do NOT proceed to Stage 2 with shortcut/delay paths that ignore fill latency.



```bash
$PYTHON_EXE "${CLAUDE_SKILL_DIR}/state.py" "$PROJECT_DIR" "spec_golden" --hook="test -f workspace/docs/spec.json && test -f workspace/docs/golden_model.py" --journal-outputs="workspace/docs/spec.json, workspace/docs/golden_model.py" --journal-notes="spec.json interface + golden_model.py behavior"
```
TaskUpdate complete.

---

## Stage 2: codegen

Read spec.json, golden_model.py, and coding_style.md (parallel Read calls) to include inline in prompts.

**Single-path dispatch**: All modules go through AI Assembly (vf-coder).

### AI Assembly

- **One vf-coder per module** in spec.json (subagent_type: general-purpose)
  - Prompt includes: MODULE_NAME, OUTPUT_FILE path
  - `GOLDEN_MODEL`: the relevant Python functions from golden_model.py that
    describe this module's behavior. The orchestrator extracts these by matching
    the module name against function names/classes in golden_model.py. Include
    the full Python implementation — vf-coder translates it into Verilog.
  - `MODULE_SPEC`: this module's ports/parameters/timing_contract from spec.json
  - `TIMING_TABLE`: main session builds a cycle-accurate timing table from
    spec.json `cycle_timing` and `timing_contract`, showing:
    - Registered outputs (use `output wire` + `reg` + `assign`)
    - Combinational outputs (use `output wire` + `assign` directly)
    - Pipeline stages and latency
  - `WEB_RESEARCH`: content from `.veriflow/web_research.md` — **only if the file
    has substantive content** (more than just "skipped" or "unavailable"). If
    minimal, omit this field entirely to save prompt tokens.
  - `PREV_FAILURE` (only on Stage 3 retry — see Stage 3 step 5b): a
    **prescriptive** fix directive containing ROOT CAUSE + concrete FIX steps
    (file, line, exact change). When present, vf-coder MUST execute the fix
    directly — no analysis, no exploring alternatives. See vf-coder.md for rules.
  - Condensed coding_style.md content
  - For top modules: include submodule port definitions from spec.json

### TB Generation + All Agent Dispatch

Dispatch ALL agents in parallel (single message):

- One vf-coder agent per module
- **One vf-tb-gen** (subagent_type: general-purpose)
  - Prompt includes: PROJECT_DIR, DESIGN_NAME, spec.json content, golden_model.py content, COCOTB_AVAILABLE flag, `${CLAUDE_SKILL_DIR}/templates` path
  - **DRIVE_PHASE_CYCLES**: Read from `spec.json timing_convention.golden_to_rtl_offset_cycles`. If not set, fall back to `max(pipeline_delay_cycles)` from timing_contract.
  - **CRITICAL**: The Verilog testbench MUST respect input hold time derived from spec.json `module_connectivity` timing_contract. Data inputs MUST remain stable for at least `DRIVE_PHASE_CYCLES + 1` cycles after the valid pulse.

After ALL return, verify outputs exist:
```bash
ls "$PROJECT_DIR/workspace/rtl/"*.v "$PROJECT_DIR/workspace/tb/"*.v "$PROJECT_DIR/workspace/tb/"*.py 2>/dev/null
```
```bash
$PYTHON_EXE "${CLAUDE_SKILL_DIR}/state.py" "$PROJECT_DIR" "codegen" --hook="ls workspace/rtl/*.v >/dev/null 2>&1 && (test -f workspace/tb/test_*.py || test -f workspace/tb/tb_*.v)" --journal-outputs="workspace/rtl/*.v, workspace/tb/test_*.py, workspace/tb/tb_*.v" --journal-notes="RTL and testbench generated in parallel"
```
TaskUpdate complete.

---

## Stage 3: verify_fix (inline — runs in main session)

**IMPORTANT**: This stage runs inline because error recovery needs main session context for Edit tool.

**Verification order (project policy — do NOT reverse):**
1. cocotb runs FIRST when `cocotb-config` is on PATH — it is the primary
   verification path. The per-cycle VPI comparison and FIRST DIVERGENCE
   report are the main diagnostic signal for error recovery.
2. The pure-Verilog testbench runs SECOND as a fallback / cross-check.
   When cocotb is unavailable, it is the only path.

Pre-stage:
```bash
[ -f "$PROJECT_DIR/.veriflow/eda_env.sh" ] && source "$PROJECT_DIR/.veriflow/eda_env.sh" && $PYTHON_EXE "${CLAUDE_SKILL_DIR}/state.py" "$PROJECT_DIR" "verify_fix" --start
```

### Golden Model Self-Check (BEFORE simulation)

If golden_model.py exists, verify it passes its own test vectors first.
This catches golden model bugs BEFORE wasting time on RTL debugging.

```bash
[ -f "$PROJECT_DIR/.veriflow/eda_env.sh" ] && source "$PROJECT_DIR/.veriflow/eda_env.sh"
cd "$PROJECT_DIR"
if [ -f workspace/docs/golden_model.py ]; then
    $PYTHON_EXE "${CLAUDE_SKILL_DIR}/iverilog_runner.py" \
        --golden-check workspace/docs/golden_model.py 2>&1 | tee logs/golden_selfcheck.log
    # ${PIPESTATUS[0]} reads the runner's exit, not tee's. Bash-only.
    if [ "${PIPESTATUS[0]}" -ne 0 ]; then
        echo "[GOLDEN] Self-check FAILED — the reference model has bugs."
        echo "[GOLDEN] Fix golden_model.py FIRST. The problem is NOT in the RTL."
        # Do NOT consume retry budget — this is a golden model issue.
        # Mark stage failed AND abort so the main session is forced to fix
        # golden_model.py before any RTL debugging.
        $PYTHON_EXE "${CLAUDE_SKILL_DIR}/state.py" "$PROJECT_DIR" "verify_fix" --fail
        echo "[GOLDEN] verify_fix marked failed. Main session: fix golden_model.py, then re-run /vf-rtl."
        exit 1
    fi
fi
```

### Cocotb per-cycle verification (if cocotb available)

Before running Verilog simulation, run cocotb with per-cycle internal signal
comparison. This is the PRIMARY debugging tool — it finds the FIRST divergence
point automatically, instead of only checking final outputs.

Uses `cocotb_runner.py` (no Makefile required) — it handles build, test,
VCD capture, and JSON result output via `cocotb_tools.runner.Icarus`.

```bash
if command -v cocotb-config &>/dev/null; then
    TOP_MODULE=$($PYTHON_EXE -c "
import json
for m in json.load(open('workspace/docs/spec.json')).get('modules', []):
    if m.get('module_type') == 'top': print(m['module_name']); break
")
    $PYTHON_EXE "${CLAUDE_SKILL_DIR}/cocotb_runner.py" \
        --rtl-dir workspace/rtl \
        --tb-dir workspace/tb \
        --module $TOP_MODULE \
        --build-dir workspace/sim_cocotb \
        --results-file logs/cocotb_results.xml \
        --verbose 2>&1 | tee logs/cocotb.log
    # cocotb_runner.py exits 0=pass, 1=fail, 2=env error
    # JSON summary is on stdout (last line), details in cocotb.log
    if grep -q "FIRST DIVERGENCE" logs/cocotb.log; then
        echo "[COCOTB] Internal signal mismatch found — see cocotb.log for details"
        # Extract first divergence info — this is the PRIMARY diagnostic
        # for error_recovery.md. Do NOT guess the root cause.
    fi
fi
```

If cocotb is not available, proceed with Verilog simulation as before.

### Parameter consistency check (before simulation)

When the DUT has Verilog parameters (e.g., `DATA_WIDTH`, `IMG_WIDTH`, `DEPTH`)
that may differ from test vector dimensions, verify that the cocotb testbench
has set `VERILOG_PARAMS` correctly. This catches the "0 outputs" failure mode
where the DUT compiles with wrong dimensions.

```bash
# Check if DUT has parameters and test file has VERILOG_PARAMS
cd "$PROJECT_DIR"
HAS_PARAMS=$($PYTHON_EXE -c "
import json
spec = json.load(open('workspace/docs/spec.json'))
params = []
for m in spec.get('modules', []):
    params.extend(p['name'] for p in m.get('parameters', []))
print(' '.join(params) if params else '')
")
if [ -n "$HAS_PARAMS" ]; then
    # DUT has parameters — check that cocotb test file defines VERILOG_PARAMS
    TB_FILE=$(ls workspace/tb/test_*.py 2>/dev/null | head -1)
    if [ -n "$TB_FILE" ] && ! grep -q "VERILOG_PARAMS" "$TB_FILE"; then
        echo "[WARN] DUT has parameters ($HAS_PARAMS) but cocotb test file has no VERILOG_PARAMS."
        echo "[WARN] If test vector dimensions differ from default parameters, cocotb will get 0 outputs."
        echo "[WARN] Add VERILOG_PARAMS = {\"PARAM_NAME\": value, ...} to the cocotb test file."
    fi
fi
```

### Run simulation

```bash
[ -f "$PROJECT_DIR/.veriflow/eda_env.sh" ] && source "$PROJECT_DIR/.veriflow/eda_env.sh"
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
$PYTHON_EXE "${CLAUDE_SKILL_DIR}/state.py" "$PROJECT_DIR" "verify_fix" --hook="grep -q 'ALL TESTS PASSED' logs/sim.log" --journal-outputs="logs/sim.log" --journal-notes="Simulation passed"
```
TaskUpdate complete. Go to Stage 4.

### If FAIL

1. **Run timing diagnostic + expected trace** (BEFORE manual analysis):
```bash
[ -f "$PROJECT_DIR/.veriflow/eda_env.sh" ] && source "$PROJECT_DIR/.veriflow/eda_env.sh"
LOG_FILE=$(test -f logs/cocotb.log && echo logs/cocotb.log || echo logs/sim.log)
$PYTHON_EXE "${CLAUDE_SKILL_DIR}/timing_diagnostic.py" \
    --log "$LOG_FILE" \
    --golden workspace/docs/golden_model.py \
    --spec workspace/docs/spec.json \
    --output logs/timing_diagnostic.json
```

   Then, generate the expected per-cycle register trace from golden_model.py.
   This complements the bug-class output of `timing_diagnostic.py` with
   concrete `expected[cycle][reg]` values to compare against the VCD-derived
   `actual[cycle][reg]` table. Cycle count is derived from `spec.json`
   (max `pipeline_delay_cycles + 4`, fallback 16):
```bash
cd "$PROJECT_DIR"
EXPECTED_TRACE_CYCLES=$($PYTHON_EXE -c "
import json
try:
    spec = json.load(open('workspace/docs/spec.json'))
    explicit = spec.get('constraints', {}).get('verification', {}).get('trace_cycles')
    if isinstance(explicit, int):
        print(explicit)
    else:
        delays = []
        for m in spec.get('modules', []):
            d = m.get('timing_contract', {}).get('pipeline_delay_cycles')
            if isinstance(d, (int, float)):
                delays.append(int(d))
        print(max(delays) + 4 if delays else 16)
except Exception:
    print(16)
")
$PYTHON_EXE "${CLAUDE_SKILL_DIR}/expected_trace_gen.py" \
    --golden workspace/docs/golden_model.py \
    --cycles "$EXPECTED_TRACE_CYCLES" \
    --skip-cycles 1 \
    --output logs/expected_trace_golden.md \
    2>&1 | tee logs/expected_trace_gen.log
```

   Post-check: verify expected trace was generated:
```bash
if [ ! -s "$PROJECT_DIR/logs/expected_trace_golden.md" ]; then
    echo "[WARN] Expected trace not generated — error recovery will lack per-cycle reference"
fi
```
   Read `logs/expected_trace_golden.md` along with the simulation divergence
   report — `expected[cycle][reg] vs actual[cycle][reg]` is the fastest way
   to localise the wrong NBA assignment in the RTL.

2. **Read** `logs/timing_diagnostic.json` — this contains the classification
   (B_late/B_early/A/D) and `fix_suggestion` with precise instructions.
   **Follow the fix_suggestion directly** — you do NOT need to understand NBA timing.

3. **If no diagnosis** (tool returns "No FIRST DIVERGENCE found"):
   **Read** `${CLAUDE_SKILL_DIR}/error_recovery.md` — follow the full procedure
   **Collect data**: read `logs/sim.log`, run vcd2table diff, classify bug type
   **5-point root cause analysis** → write to `logs/stage_journal.md`

4. **Fix RTL** using Edit tool

5. **Record this failure signature** before re-running (lets the loop detector
   see repeats):
```bash
SIG=$($PYTHON_EXE -c "
import json, pathlib
p = pathlib.Path('logs/timing_diagnostic.json')
if p.exists():
    d = json.loads(p.read_text())
    div = d.get('divergence', {})
    print(f\"cycle:{div.get('cycle','?')}:signal:{div.get('signal','?')}\")
else:
    print('no-diagnostic')
")
$PYTHON_EXE "${CLAUDE_SKILL_DIR}/state.py" "$PROJECT_DIR" "verify_fix" \
    --fail --error-sig="$SIG"
```

5b. **Build the failure-summary file** for the next vf-coder retry.
This MUST be a **prescriptive fix directive** — not just a description of what
went wrong. The main session MUST diagnose the root cause and write concrete
fix steps (file, line number, exact code change) before rolling back to codegen.

**Format** (vf-coder expects this exact structure):
```
PREV_FAILURE:
  ROOT CAUSE: <one-sentence diagnosis referencing specific file and line>
  BUG CLASS: <timing_diagnostic bug_class>
  DIVERGENCE: cycle <N>, signal <name>, expected=<hex>, actual=<hex>
  FIX (mandatory — do NOT explore alternatives):
  1. <file:line> — <exact change description>
  2. <file:line> — <exact change description>
  CONSTRAINTS: <any constraints on the fix, e.g. "only modify FSM logic">
```

The main session generates this by:
1. Running the diagnostic script below to extract raw divergence data
2. Reading the RTL file(s) at the divergence point to identify the root cause
3. Writing the concrete FIX steps — this is the main session's diagnosis, not
   the agent's job. The agent should ONLY execute.

```bash
$PYTHON_EXE - <<'PY' 2>&1 | tee logs/prev_failure_summary_raw.md
import json, pathlib

diag = pathlib.Path("logs/timing_diagnostic.json")
expected = pathlib.Path("logs/expected_trace_golden.md")

print("# Raw failure data (main session: add ROOT CAUSE and FIX steps below)")
print()

if not diag.exists():
    print("(no logs/timing_diagnostic.json — `timing_diagnostic.py` did not produce a report)")
else:
    d = json.loads(diag.read_text())
    div = d.get("divergence", {}) or {}
    print(f"- **First divergence cycle**: {div.get('cycle', '?')}")
    print(f"- **Signal**: `{div.get('signal', '?')}`")
    print(f"- **Expected**: `{div.get('expected', '?')}`")
    print(f"- **Actual**: `{div.get('actual', '?')}`")
    print(f"- **Bug class**: {d.get('bug_class', '?')}  ({d.get('confidence', '?')})")
    fix = d.get("fix_suggestion") or {}
    if fix:
        print()
        print("## Suggested fix direction (from timing_diagnostic.py)")
        for k, v in fix.items():
            print(f"- **{k}**: {v}")

if expected.exists():
    print()
    print("## Expected trace (first 8 cycles, from golden_model.py)")
    lines = expected.read_text().splitlines()
    body = [ln for ln in lines if ln.strip() and not ln.startswith("##")][:10]
    print("\n".join(body))

print()
print("---")
print("## MAIN SESSION: Fill in ROOT CAUSE and FIX below before passing to vf-coder")
print()
print("ROOT CAUSE: <diagnose by reading the RTL at the divergence point>")
print("FIX:")
print("1. <file>:<line> — <specific change>")
print("2. <file>:<line> — <specific change>")
PY
```

**CRITICAL**: The raw data above is NOT sufficient as PREV_FAILURE. The main
session MUST read the RTL file(s), identify the root cause, and write concrete
FIX steps in the `logs/prev_failure_summary.md` file before any rollback to
codegen. The filled-in `prev_failure_summary.md` is what gets passed as
PREV_FAILURE to vf-coder. If the main session cannot determine the root cause,
ask the user rather than rolling back with a vague description.

6. **Check whether we are looping on the same bug** BEFORE consuming another
   retry slot. If the same divergence signature has fired 2+ times, fixing
   RTL is not converging — rollback to codegen instead of burning more attempts:
```bash
$PYTHON_EXE "${CLAUDE_SKILL_DIR}/state.py" "$PROJECT_DIR" "verify_fix" \
    --check-loop="$SIG"
LOOP_STATUS=$?
if [ "$LOOP_STATUS" -eq 2 ]; then
    echo "[STAGE3] Detected fix-loop on '$SIG' — rolling back to codegen."
    $PYTHON_EXE "${CLAUDE_SKILL_DIR}/state.py" "$PROJECT_DIR" --reset codegen
    # Main session: BEFORE re-dispatching Stage 2, read the RTL at the
    # divergence point, diagnose root cause, write concrete FIX steps into
    # logs/prev_failure_summary.md. Then pass it as PREV_FAILURE — the agent
    # should ONLY execute the fix, not explore alternatives.
fi
```

7. **Re-run simulation** (go back to "Run simulation" above)

8. **Retry budget**: 3 attempts total
   - 1st fail: fix RTL, retry
   - 2nd fail: `state.py --reset codegen`, restart from Stage 2
   - 3rd fail: STOP, notify user
   - At ANY attempt: if step 6's loop detector returns 2, jump straight to
     `state.py --reset codegen` and re-run Stage 2 without waiting for the
     3rd attempt.

---

## Stage 4: lint_synth

Dispatch 2 parallel agents (single message):

- **vf-linter** (subagent_type: general-purpose) — include PROJECT_DIR, EDA_ENV path, PYTHON_EXE, SKILL_DIR
- **vf-synthesizer** (subagent_type: general-purpose) — include PROJECT_DIR, SPEC path, EDA_ENV path, PYTHON_EXE, SKILL_DIR

After BOTH return:

If lint failed → fix syntax errors in main session, re-run lint only.
If synth failed → check report, fix if needed.

```bash
$PYTHON_EXE "${CLAUDE_SKILL_DIR}/state.py" "$PROJECT_DIR" "lint_synth" --hook="test -f logs/lint.log && test -f workspace/synth/synth_report.txt" --journal-outputs="logs/lint.log, workspace/synth/synth_report.txt" --journal-notes="Lint and synthesis complete"
```
TaskUpdate complete. Pipeline done.

---

## Design Rules Summary

See `${CLAUDE_SKILL_DIR}/design_rules.md` for full rules.

- Synchronous active-high reset named `rst`
- Port naming: `_n` suffix for active-low, `_i`/`_o` for direction
- **Verilog-2005 only** — NO SystemVerilog
- Interface Lock: port names, handshake protocols, and module hierarchy are frozen after Stage 1
