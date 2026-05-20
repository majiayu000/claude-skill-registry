---
name: vf-pipeline
description: Use this skill to start or resume the VeriFlow RTL hardware design pipeline (architect to synth). Trigger this when the user asks to "run the RTL flow", "design hardware", or "start the pipeline". Pass the project directory path as the argument.
---

# RTL Pipeline Orchestrator

This skill IS the plan — execute each stage immediately using Read/Write/Bash tools. Do NOT plan before executing.

Project directory path: `$ARGUMENTS`

If `$ARGUMENTS` is empty, ask the user for it.

---

## Step 0: Initialization

Execute immediately:

```bash
PROJECT_DIR="$ARGUMENTS"
ls -la "$PROJECT_DIR/requirement.md" || { echo "ERROR: requirement.md not found"; exit 1; }
cd "$PROJECT_DIR" && mkdir -p workspace/docs workspace/rtl workspace/tb workspace/sim workspace/synth .veriflow logs

# Report available input files
echo "[INPUT] requirement.md: $(test -f requirement.md && echo YES || echo NO)"
echo "[INPUT] constraints.md: $(test -f constraints.md && echo YES || echo NO)"
echo "[INPUT] design_intent.md: $(test -f design_intent.md && echo YES || echo NO)"
echo "[INPUT] context/: $(ls context/*.md 2>/dev/null | wc -l) file(s)"
ls context/*.md 2>/dev/null || true

# Discover Python
PYTHON_EXE=$(which python3 2>/dev/null || which python 2>/dev/null || true)
if [ -z "$PYTHON_EXE" ]; then
    PYTHON_EXE=$(ls /c/Python*/python.exe /c/Users/*/AppData/Local/Programs/Python/*/python.exe 2>/dev/null | head -1)
fi
echo "[ENV] Python: ${PYTHON_EXE:-NOT FOUND}"

# Discover EDA tools — must include bin + lib + lib/ivl (iverilog needs ivlpp.exe and ivl.exe)
EDA_BIN=""
EDA_LIB=""
for base in /c/oss-cad-suite "/c/Program Files/iverilog" "/c/Program Files (x86)/iverilog"; do
    if [ -d "$base/bin" ]; then
        EDA_BIN="$base/bin"
        [ -d "$base/lib" ] && EDA_LIB="$base/lib"
        [ -d "$base/lib/ivl" ] && EDA_LIB="$base/lib:$base/lib/ivl"
        break
    fi
done

# Save env to file so every subsequent Bash call can source it
cat > "$PROJECT_DIR/.veriflow/eda_env.sh" << ENVEOF
export PYTHON_EXE="$PYTHON_EXE"
export EDA_BIN="$EDA_BIN"
export EDA_LIB="$EDA_LIB"
export PATH="$EDA_BIN:$EDA_LIB:\$PATH"
ENVEOF
echo "[ENV] Saved EDA env to .veriflow/eda_env.sh"
echo "[ENV] EDA_BIN=$EDA_BIN  EDA_LIB=$EDA_LIB"

# Verify tools
source "$PROJECT_DIR/.veriflow/eda_env.sh"
which yosys iverilog vvp 2>/dev/null || echo "[WARN] Some EDA tools not found"

# Quick smoke test — exit 127 means iverilog can't find its sub-tools
iverilog -V 2>&1 | head -1 || echo "[WARN] iverilog smoke test failed — check EDA_LIB path"

# Check existing state
if [ -f "$PROJECT_DIR/.veriflow/pipeline_state.json" ]; then
    echo "[STATUS] Existing state — resume from next incomplete stage:"
    cat "$PROJECT_DIR/.veriflow/pipeline_state.json"
else
    echo "[STATUS] New project, starting from Stage 1."
fi
```

If resuming, check `stages_completed` in pipeline_state.json and skip those stages.

### 0a. Initialize stage journal

Use Bash to create or resume `workspace/docs/stage_journal.md`:

```bash
if [ -f "$PROJECT_DIR/workspace/docs/stage_journal.md" ]; then
    printf "\n---\n\n**Session resumed** at $(date -Iseconds)\n\n" >> "$PROJECT_DIR/workspace/docs/stage_journal.md"
else
    cat > "$PROJECT_DIR/workspace/docs/stage_journal.md" << 'EOF'
# VeriFlow Pipeline Stage Journal

This file records the progress, outputs, and key decisions for each pipeline stage.
EOF
fi
```

### 0b. Create pipeline task list (status bar progress)

Use **TaskCreate** to create one task per pipeline stage. Call all 8 in sequence:

```
TaskCreate: subject="Stage 1: Architect — generate spec.json", activeForm="Generating spec.json"
TaskCreate: subject="Stage 2: Microarch — generate micro_arch.md", activeForm="Generating microarchitecture"
TaskCreate: subject="Stage 3: Timing — generate timing model + testbench", activeForm="Generating timing model"
TaskCreate: subject="Stage 4: Coder — generate RTL via sub-agent", activeForm="Generating RTL modules"
TaskCreate: subject="Stage 5: Skill_D — static analysis", activeForm="Running static analysis"
TaskCreate: subject="Stage 6: Lint — iverilog syntax check", activeForm="Running lint"
TaskCreate: subject="Stage 7: Sim — compile and simulate", activeForm="Running simulation"
TaskCreate: subject="Stage 8: Synth — yosys synthesis", activeForm="Running synthesis"
```

If resuming from a previous run, only create tasks for stages NOT in `stages_completed`. Mark already-completed stages' tasks as **completed** using TaskUpdate.

**IMPORTANT**: Every Bash call that uses EDA tools (iverilog, vvp, yosys) MUST start with:
```
source "$PROJECT_DIR/.veriflow/eda_env.sh"
```
Do NOT use bare `iverilog` or `yosys` without sourcing this file first — the PATH does not persist between Bash calls.

---

## State Update Command

After each stage hook passes:

```bash
source "$PROJECT_DIR/.veriflow/eda_env.sh" && $PYTHON_EXE "${CLAUDE_SKILL_DIR}/state.py" "$PROJECT_DIR" "STAGE_NAME"
```

Replace `STAGE_NAME` with: architect, microarch, timing, coder, skill_d, lint, sim, synth.

---

## Design Rules (Apply to ALL stages)

- All modules use **synchronous active-high reset** named `rst`. Reset is checked inside `always @(posedge clk)` only — no async sensitivity list. See `coding_style.md` Section 6 for full rules.
- Port naming: `_n` suffix for active-low, `_i`/`_o` for direction
- Parameterized design: use `parameter` for widths and depths
- Clock domains must be explicitly declared
- **Verilog-2005 only** — NO SystemVerilog (`logic`, `always_ff`, `assert property`, `|->`, `##`)

### Interface Lock

The following fields in spec.json are locked after Stage 1 completes. Stages 2-8 must NOT modify them:
- Port names, widths, and directions
- Reset polarity (`reset_polarity` field: `"active_high"` → port named `rst`, `"active_low"` → port named `rst_n`)
- Handshake protocol (`handshake` field: `"hold_until_ack"` / `"single_cycle"` / `"pulse"`)
- Module hierarchy and connectivity

If a later stage discovers a problem with the interface definition, it must roll back to Stage 1 to redefine.

---

## Stage Dispatch Loop

Execute stages sequentially. For each stage, **Read the stage file first**, then execute its instructions.

**Variable**: `${CLAUDE_SKILL_DIR}` is set by Claude Code to the skill's installed directory. Stage files are at `${CLAUDE_SKILL_DIR}/stages/stage_N.md`.

### Execution pattern for each stage:

1. Use **Read** tool to open `${CLAUDE_SKILL_DIR}/stages/stage_N.md`
2. Execute ALL instructions in that file (read inputs, write outputs, run bash, hooks, state, journal)
3. If the hook passes and state is saved, proceed to the next stage
4. If any step fails, go to **Error Recovery** below

### Stage summary (for quick reference — full instructions are in stage files):

| Stage | Name | Input | Output | Method |
|-------|------|-------|--------|--------|
| 1 | architect | requirement.md, constraints.md, design_intent.md, context/*.md | spec.json, behavior_spec.md | Inline — asks user questions |
| 2 | microarch | spec.json, behavior_spec.md, requirement.md, design_intent.md | micro_arch.md | Inline |
| 3 | timing | spec.json, micro_arch.md | timing_model.yaml, tb_*.v | Inline |
| 4 | coder | spec.json, behavior_spec.md, micro_arch.md | rtl/*.v | Sub-agent (vf-coder) per module |
| 5 | skill_d | rtl/*.v, spec.json | static_report.json | Inline — static checks |
| 6 | lint | rtl/*.v | logs/lint.log | Inline — iverilog -Wall |
| 7 | sim | rtl/*.v, tb/*.v | logs/sim.log | Inline — iverilog + vvp |
| 8 | synth | rtl/*.v, spec.json | synth_report.txt | Inline — yosys |

---

## Error Recovery

When any stage fails (lint errors, sim failure, synth failure):

### Step 1: Diagnose
- Read the error output from the failed stage
- Read the relevant RTL files from `workspace/rtl/`

### Step 1.5: Structured Root Cause Analysis (MANDATORY)

Before modifying ANY file, complete the following analysis and write it to `stage_journal.md`.

#### Step 1.5-A: Read the waveform table (timing errors ONLY)

If the failure is a simulation mismatch (wrong value, wrong cycle, FSM stuck), FIRST read the waveform table generated by Stage 7's `7d-wave` step:

```bash
# Check if waveform table was generated
ls "$PROJECT_DIR/logs/wave_table.txt" "$PROJECT_DIR/logs/wave_"*.txt 2>/dev/null
```

Use **Read** tool to read `logs/wave_table.txt`. Then answer these questions from the table:

| Question | Where to look |
|----------|--------------|
| At the `[FAIL]` cycle, what is the FSM state? | `state_reg` / `state` column |
| Is the FSM in the expected state per timing_model.yaml? | Compare with scenario assertions |
| What is the value of the failing signal at `[FAIL]` cycle? | Named column |
| When did the failing signal LAST CHANGE before `[FAIL]`? | Scan backwards from `[FAIL]` row |
| Is the error an off-by-one (value valid 1 cycle late/early)? | Compare cycle N-1 vs N vs N+1 |
| Is `rst` still asserted at `[FAIL]`? | `rst` column |

**Common timing patterns to identify from the table**:

```
Pattern A — Off-by-one pipeline delay:
  Cycle N:   input valid, data_out = 0x00   ← [FAIL] expected 0xAB
  Cycle N+1: input valid, data_out = 0xAB   ← correct value arrived one cycle late
  → Fix: sample output one cycle later, OR remove extra register stage

Pattern B — Reset not clearing output register:
  Cycle 0: rst=1, data_out = 0xFF   ← [FAIL] expected 0x00 during reset
  Cycle 1: rst=1, data_out = 0xFF   ← output register not in reset path
  → Fix: add output_reg to reset block

Pattern C — FSM stuck / missing transition:
  Cycle N:   state=CALC, done_flag=1    ← should transition to DONE
  Cycle N+1: state=CALC, done_flag=1   ← stuck — transition condition wrong
  → Fix: check FSM transition condition in combinational block

Pattern D — Handshake violation (valid deasserted too early):
  Cycle N:   valid=1, ready=0   ← handshake not yet complete
  Cycle N+1: valid=0, ready=1   ← valid dropped before ready — violates hold_until_ack
  → Fix: hold valid until ready is seen

Pattern E — Counter range error (N vs N-1):
  Expected N iterations of enable=1, but got N-1 or N+1
  → Fix: change loop terminal condition from <= to <, or vice versa
```

#### Step 1.5-B: 5-point root cause analysis

After reading the waveform table, complete:

1. **Error location**: Which `[FAIL]` line? Which cycle number? Which signal?
2. **Signal trace**: Which module drives that signal? Which `always` block? Which line?
3. **Root cause hypothesis**: State the exact RTL line that is wrong. Reference the waveform table pattern (A/B/C/D/E above) if it matches.
4. **Minimal fix plan**: Which file, which lines, what exact change?
5. **Impact scope**: Which other signals/modules are affected?

**Only after completing both 1.5-A and 1.5-B**, proceed to Step 3 (Fix).

**Golden model comparison** (if a Python reference implementation exists in `context/*.py`):
- Run the golden model with the same inputs as the failing test case
- Extract intermediate values at each computation step
- Compare with RTL simulation output to pinpoint the exact step where divergence occurs
- Cross-reference with waveform table: the divergence cycle in the table should match the golden model step

If you cannot form a hypothesis for point 3 after reading the waveform table, STOP and ask the user for help. Do NOT guess-and-fix.

### Step 2: Classify
- **syntax** (lint): typos, missing declarations, port mismatches
- **logic** (sim): incorrect functionality, timing issues, FSM errors
- **timing** (synth): non-synthesizable constructs, timing violations

### Step 3: Fix

Common error patterns:

| Error Pattern | Cause | Fix |
|--------------|-------|-----|
| `cannot be driven by continuous assignment` | `reg` used with `assign` | Change to `wire` or use `always` |
| `Unable to bind wire/reg/memory` | Forward reference or typo | Move declaration or fix typo |
| `Variable declaration in unnamed block` | Variable in `always` without named block | Move to module level |
| `Width mismatch` | Assignment between different widths | Add explicit width cast |
| `is not declared` | Typo or missing declaration | Fix typo or add declaration |
| `Multiple drivers` | Two assignments to same signal | Remove duplicate |
| `Latch inferred` | Incomplete case/if without default | Add default case or else branch |

Fix rules:
- Only modify files that have issues
- Preserve original coding style and design intent
- Do NOT change module interfaces (ports) — see Interface Lock in Design Rules
- **RTL fixes**: Do NOT modify any file in `workspace/tb/`
- **TB bugs**: If simulation fails due to a testbench bug (not an RTL bug), you MAY fix the testbench. But do NOT weaken assertions — only fix TB infrastructure (signal types, timing, connectivity)
- Do NOT add new functionality or remove existing functionality
- **Functional integrity**: A fix must NOT remove, disable, or stub out existing functionality. Replacing a working module with a simplified version that loses functionality is NOT allowed. If the fix is too complex, STOP and ask the user.
- **No testbench modifications**: Do NOT modify any file in `workspace/tb/` during error recovery. If the testbench appears to have a bug, note it in the journal and ask the user — do NOT fix it yourself.
- **No new testbench files**: Error recovery MUST NOT create new `.v` files. Debug by adding `$display` statements to existing testbenches if needed, then remove them after fixing.
- **Cleanup debug artifacts**: After each fix attempt, remove temporary build products (`workspace/sim/*.vvp` except `tb.vvp`, `*.vcd` files in project root)
- **Journal before fix**: Each RTL modification MUST be preceded by a Step 1.5 root cause analysis entry in `stage_journal.md`
- **Verify fix scope**: After fixing, re-read the modified file and confirm: (1) all ports are still present, (2) no functionality was removed, (3) the module still matches its description in spec.json.
- Make minimal changes
- Fix one error at a time
- **Debug budget**: If you spend more than 3 fix-and-retry cycles on the same error without progress, STOP and ask the user for help. Do NOT go in circles

After fixing, re-run the failed stage's Bash command to verify.

### Step 4: Sync upstream documents

If the fix changes architectural behavior (FSM states, timing parameters, sampling points, signal definitions), update the affected upstream documents:
- **Logic fix** → update `workspace/docs/micro_arch.md` to match the actual RTL behavior
- **Timing fix** → update `workspace/docs/timing_model.yaml` if scenarios/assertions are affected
- Always update `micro_arch.md` if FSM states, datapath, or control logic changed

### Step 5: Log recovery to journal

After each fix attempt, append a recovery entry to `stage_journal.md`:

```bash
printf "\n### Recovery: <stage_name>\n**Timestamp**: $(date -Iseconds)\n**Attempt**: <attempt_number>\n**Error type**: <syntax|logic|timing>\n**Fix summary**: <brief description>\n**Result**: <PASS|FAIL|PENDING>\n" >> "$PROJECT_DIR/workspace/docs/stage_journal.md"
```

Replace placeholders with actual values. Update the result after verifying the fix.

### Retry Policy

1. **1st fail**: Fix RTL, retry the stage
2. **2nd fail**: Rollback to earlier stage and re-run sequentially
3. **3rd fail**: STOP and notify user

Rollback targets by error type:

| Error Type | Rollback To | Re-run Path |
|-----------|-------------|-------------|
| syntax | coder | coder → skill_d → lint → sim → synth |
| logic | microarch | microarch → timing → coder → skill_d → lint → sim → synth |
| timing | timing | timing → coder → skill_d → lint → sim → synth |
