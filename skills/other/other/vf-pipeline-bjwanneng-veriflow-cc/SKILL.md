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

Execute immediately:

```bash
PROJECT_DIR="$ARGUMENTS"
ls -la "$PROJECT_DIR/requirement.md" || echo "[FATAL ERROR] requirement.md not found. STOP and ask the user for the file."
cd "$PROJECT_DIR" && mkdir -p workspace/docs workspace/rtl workspace/tb workspace/sim workspace/synth .veriflow logs

# Report available input files
echo "[INPUT] requirement.md: $(test -f requirement.md && echo YES || echo NO)"
echo "[INPUT] constraints.md: $(test -f constraints.md && echo YES || echo NO)"
echo "[INPUT] design_intent.md: $(test -f design_intent.md && echo YES || echo NO)"
echo "[INPUT] context/: $(ls context/*.md 2>/dev/null | wc -l) file(s)"
ls context/*.md 2>/dev/null || true

# Discover Python (cross-platform: smoke-test each candidate)
_discover_python() {
    local candidates=(
        "$(which python3 2>/dev/null)"
        "$(which python 2>/dev/null)"
        /c/Python*/python.exe
        /c/Users/*/AppData/Local/Programs/Python/*/python.exe
        /usr/bin/python3
        /usr/local/bin/python3
    )
    for p in "${candidates[@]}"; do
        [ -z "$p" ] && continue
        [ -f "$p" ] || continue
        if echo "$p" | grep -q "WindowsApps"; then continue; fi
        if "$p" --version >/dev/null 2>&1; then
            echo "$p"
            return 0
        fi
    done
    return 1
}
PYTHON_EXE=$(_discover_python) || true
echo "[ENV] Python: ${PYTHON_EXE:-NOT FOUND}"

# Discover cocotb
COCOTB_AVAILABLE="false"
if [ -n "$PYTHON_EXE" ] && $PYTHON_EXE -c "import cocotb; import cocotb_tools.runner" 2>/dev/null; then
    COCOTB_AVAILABLE="true"
    echo "[ENV] cocotb: AVAILABLE"
else
    echo "[ENV] cocotb: NOT AVAILABLE"
fi

# Discover EDA tools
EDA_BIN=""
EDA_LIB=""
for base in "/c/oss-cad-suite" "/c/Program Files/iverilog" "/c/Program Files (x86)/iverilog" "/opt/oss-cad-suite" "/usr/local" "/usr" "$HOME/.local"; do
    if [ -d "$base/bin" ] && { [ -f "$base/bin/iverilog" ] || [ -f "$base/bin/iverilog.exe" ]; }; then
        EDA_BIN="$base/bin"
        [ -d "$base/lib" ] && EDA_LIB="$base/lib"
        [ -d "$base/lib/ivl" ] && EDA_LIB="$base/lib:$base/lib/ivl"
        break
    fi
done
if [ -z "$EDA_BIN" ] && command -v iverilog >/dev/null 2>&1; then
    EDA_BIN=$(dirname "$(command -v iverilog)")
    if [ "$EDA_BIN" = "/usr/bin" ]; then EDA_LIB="/usr/lib:/usr/lib/ivl"; fi
fi

cat > "$PROJECT_DIR/.veriflow/eda_env.sh" << ENVEOF
export PYTHON_EXE="$PYTHON_EXE"
export EDA_BIN="$EDA_BIN"
export EDA_LIB="$EDA_LIB"
export COCOTB_AVAILABLE="$COCOTB_AVAILABLE"
export PATH="$EDA_BIN:$EDA_LIB:\$PATH"
ENVEOF
echo "[ENV] EDA_BIN=$EDA_BIN  EDA_LIB=$EDA_LIB"

source "$PROJECT_DIR/.veriflow/eda_env.sh"
which yosys iverilog vvp 2>/dev/null || echo "[WARN] Some EDA tools not found"
iverilog -V 2>&1 | head -1 || echo "[WARN] iverilog smoke test failed"

# Check existing state
if [ -f "$PROJECT_DIR/.veriflow/pipeline_state.json" ]; then
    echo "[STATUS] Existing state — resume from next incomplete stage:"
    cat "$PROJECT_DIR/.veriflow/pipeline_state.json"
else
    echo "[STATUS] New project, starting from Stage 1."
fi
```

If resuming, check `stages_completed` and skip those stages.

### 0a. Initialize stage journal and pipeline start time

```bash
if [ -f "$PROJECT_DIR/workspace/docs/stage_journal.md" ]; then
    printf "\n---\n\n**Session resumed** at $(date -Iseconds)\n\n" >> "$PROJECT_DIR/workspace/docs/stage_journal.md"
else
    cat > "$PROJECT_DIR/workspace/docs/stage_journal.md" << 'EOF'
# VeriFlow Pipeline Stage Journal

This file records the progress, outputs, and key decisions for each pipeline stage.
EOF
    # Record pipeline start time for first run
    printf "\n## Pipeline Start\n**Timestamp**: $(date -Iseconds)\n" >> "$PROJECT_DIR/workspace/docs/stage_journal.md"
fi
```

### 0b. Batch Requirements Clarification

Read ALL input files in parallel (single message with multiple Read calls):
- `$PROJECT_DIR/requirement.md` (required)
- `$PROJECT_DIR/constraints.md` (optional)
- `$PROJECT_DIR/design_intent.md` (optional)
- `$PROJECT_DIR/context/*.md` files

After reading, systematically check for missing/ambiguous information across these sections:

**A. Functional clarity**: Module functionality, interface protocol, data format, FSM behavior, clock domain crossings
**B. Constraint clarity**: Clock frequency, target platform, area/power budget, reset strategy, IO standards
**C. Design intent**: Architecture style, module partitioning, interface preferences, IP reuse, key decisions
**D. Algorithm & protocol**: Algorithm reference, pseudocode, key formulas, test vectors
**E. Timing completeness**: Cycle-level behavior, latency, throughput, interface timing, reset recovery, backpressure
**F. Domain knowledge**: Design domain, standard reference, prerequisite concepts, test vectors
**G. Information completeness**: Implicit assumptions, missing scenarios

**Smart filtering**: For each item in A-G, check if input files already answer it. If answered → note "confirmed from input" and skip. Only ask about what's truly missing or ambiguous.

**Batch questions**: Use AskUserQuestion with up to 4 questions per call. Group related questions together. Repeat until all sections are resolved.

### 0c. Write clarifications.md

After all questions are resolved, use Write to create `$PROJECT_DIR/.veriflow/clarifications.md`:

```markdown
# Requirements Clarifications
## A. Functional Clarity
- Module functionality: [answer or "confirmed from requirement.md"]
- Interface protocol: [answer]
...
## B. Constraint Clarity
...
```

### 0d. Create pipeline task list

Use TaskCreate to create one task per pipeline stage. If resuming, only create tasks for stages NOT in `stages_completed`.

**IMPORTANT**: Every Bash call that uses EDA tools MUST start with:
```bash
source "$PROJECT_DIR/.veriflow/eda_env.sh"
```

---

## Design Rules

See `${CLAUDE_SKILL_DIR}/design_rules.md` for full rules. Summary:
- Synchronous active-high reset named `rst`
- Port naming: `_n` suffix for active-low, `_i`/`_o` for direction
- **Verilog-2005 only** — NO SystemVerilog
- Interface Lock: port names, handshake protocols, and module hierarchy are frozen after Stage 1

---

## Combined State + Hook + Journal Command

After each subagent completes, run ONE combined command:

```bash
source "$PROJECT_DIR/.veriflow/eda_env.sh" && $PYTHON_EXE "${CLAUDE_SKILL_DIR}/state.py" "$PROJECT_DIR" "<STAGE>" --start
```

Then after subagent returns:

```bash
source "$PROJECT_DIR/.veriflow/eda_env.sh" && $PYTHON_EXE "${CLAUDE_SKILL_DIR}/state.py" "$PROJECT_DIR" "<STAGE>" --hook="<HOOK_COMMAND>" --journal-outputs="<OUTPUT_FILES>" --journal-notes="<NOTES>"
```

---

## Stage Dispatch

The pipeline has 4 stages: **spec_golden → codegen → verify_fix → lint_synth**

### Stage 1: spec_golden (2 parallel subagents — vf-spec-gen + vf-golden-gen)

Generate spec.json (interface only) + golden_model.py in parallel. No behavior_spec.md or micro_arch.md.

Two independent agents run in parallel because spec.json and golden_model.py have no dependency on each other — both consume the same requirement inputs independently.

1. Record start time:
```bash
source "$PROJECT_DIR/.veriflow/eda_env.sh" && $PYTHON_EXE "${CLAUDE_SKILL_DIR}/state.py" "$PROJECT_DIR" "spec_golden" --start
```

2. Read all input files (requirement.md, constraints.md, design_intent.md, context/*.md) into context.

3. Dispatch TWO subagents in parallel (single message with two Agent calls):
   - **Agent 1: vf-spec-gen** (subagent_type: general-purpose)
     - **Prompt must include**: PROJECT_DIR path, CLARIFICATIONS path, TEMPLATES_DIR path
     - **Inline in prompt**: Full contents of requirement.md, constraints.md (if exists), design_intent.md (if exists), context/*.md (if any)
   - **Agent 2: vf-golden-gen** (subagent_type: general-purpose)
     - **Prompt must include**: PROJECT_DIR path, CLARIFICATIONS path, TEMPLATES_DIR path
     - **Inline in prompt**: Full contents of requirement.md, constraints.md (if exists), design_intent.md (if exists), context/*.md (if any)

4. After BOTH agents return, validate outputs exist:
```bash
test -f "$PROJECT_DIR/workspace/docs/spec.json" || { echo "[HOOK] FAIL: spec.json missing"; exit 1; }
test -f "$PROJECT_DIR/workspace/docs/golden_model.py" || { echo "[HOOK] FAIL: golden_model.py missing"; exit 1; }
```

5. Run combined hook + state + journal:
```bash
source "$PROJECT_DIR/.veriflow/eda_env.sh" && $PYTHON_EXE "${CLAUDE_SKILL_DIR}/state.py" "$PROJECT_DIR" "spec_golden" --hook="test -f workspace/docs/spec.json && test -f workspace/docs/golden_model.py" --journal-outputs="workspace/docs/spec.json, workspace/docs/golden_model.py" --journal-notes="Specification and golden model generated in parallel"
```

6. Mark Stage 1 task as completed via TaskUpdate.

### Stage 2: codegen (parallel subagents — vf-coder per module + testbench generator)

Generate all RTL modules AND testbench in parallel from spec.json + golden_model.py.

Testbench generation depends only on spec.json (port names, widths, handshake) and golden_model.py (test vectors, expected outputs) — NOT on the actual RTL code. Therefore it can run in parallel with RTL codegen.

1. Record start time:
```bash
source "$PROJECT_DIR/.veriflow/eda_env.sh" && $PYTHON_EXE "${CLAUDE_SKILL_DIR}/state.py" "$PROJECT_DIR" "codegen" --start
```

2. Read spec.json and golden_model.py (parallel Read calls) to include inline in prompts.

3. Dispatch ALL module agents AND the testbench agent in parallel (single message with multiple Agent calls):
   - For each module in spec.json, dispatch a **vf-coder** subagent (subagent_type: general-purpose):
     - **Prompt must include**: MODULE_NAME, OUTPUT_FILE path, spec.json content, golden_model.py content
     - **For top modules**: include submodule port definitions from spec.json
     - **For leaf modules**: include only that module's spec entry
   - Dispatch ONE **vf-tb-gen** subagent (subagent_type: general-purpose) for testbench generation:
     - **Prompt must include**: PROJECT_DIR path, DESIGN_NAME (top module name), spec.json content, golden_model.py content, COCOTB_AVAILABLE flag, TEMPLATES_DIR path
     - This agent generates BOTH `workspace/tb/test_<design_name>.py` (cocotb) AND `workspace/tb/tb_<design_name>.v` (Verilog TB) always
     - The Verilog TB embeds pre-computed expected values from golden_model.py test vectors, making it self-checking without any Python/cocotb dependency

4. After ALL agents return, verify outputs:
```bash
echo "[CODEGEN] RTL files generated:"
ls -la "$PROJECT_DIR/workspace/rtl/"*.v 2>/dev/null
echo "[CODEGEN] Testbench files generated:"
ls -la "$PROJECT_DIR/workspace/tb/" 2>/dev/null
```

5. Run combined hook + state + journal:
```bash
source "$PROJECT_DIR/.veriflow/eda_env.sh" && $PYTHON_EXE "${CLAUDE_SKILL_DIR}/state.py" "$PROJECT_DIR" "codegen" --hook="test -f workspace/rtl/*.v && (test -f workspace/tb/test_*.py || test -f workspace/tb/tb_*.v)" --journal-outputs="workspace/rtl/*.v, workspace/tb/test_*.py, workspace/tb/tb_*.v" --journal-notes="RTL and testbench generated in parallel"
```

6. Mark Stage 2 task as completed via TaskUpdate.

### Stage 3: verify_fix (inline — runs in main session)

Compile RTL, run simulation, compare with golden model, fix errors in a loop. This stage runs inline because error recovery needs main session context.

**Simulation strategy**: Use Verilog testbench by default (fast, no cocotb dependency). Fall back to cocotb only if `COCOTB_AVAILABLE=true` AND the user has not opted out. The Verilog TB is self-checking with pre-computed expected values embedded during codegen.

1. Record start time:
```bash
source "$PROJECT_DIR/.veriflow/eda_env.sh" && $PYTHON_EXE "${CLAUDE_SKILL_DIR}/state.py" "$PROJECT_DIR" "verify_fix" --start
```

2. **Compile with iverilog**:
```bash
source "$PROJECT_DIR/.veriflow/eda_env.sh"
cd "$PROJECT_DIR"

# Discover all RTL files
RTL_FILES=$(ls workspace/rtl/*.v 2>/dev/null | sort)

if [ -z "$RTL_FILES" ]; then
    echo "[VERIFY] ERROR: No RTL files found"
    exit 1
fi

echo "[VERIFY] RTL files:"
echo "$RTL_FILES"

# Get top module from spec.json
TOP_MODULE=$($PYTHON_EXE -c "
import json
spec = json.load(open('workspace/docs/spec.json'))
mods = spec.get('modules', {})
if isinstance(mods, dict):
    for k, v in mods.items():
        if v.get('module_type') == 'top':
            print(v.get('module_name', k)); break
elif isinstance(mods, list):
    for m in mods:
        if m.get('module_type') == 'top':
            print(m['module_name']); break
")
echo "[VERIFY] Top module: $TOP_MODULE"
```

3. **Run Verilog TB simulation** (default — always available if iverilog is installed):
```bash
source "$PROJECT_DIR/.veriflow/eda_env.sh"
cd "$PROJECT_DIR"

# Check if Verilog TB exists
VERILOG_TB=$(ls workspace/tb/tb_*.v 2>/dev/null | head -1)

if [ -n "$VERILOG_TB" ]; then
    echo "[VERIFY] Using Verilog testbench: $VERILOG_TB"

    # Use the iverilog runner
    $PYTHON_EXE "${CLAUDE_SKILL_DIR}/iverilog_runner.py" \
        --module $TOP_MODULE \
        --rtl-dir workspace/rtl \
        --tb-file "$VERILOG_TB" \
        --build-dir workspace/sim \
        --verbose 2>&1 | tee logs/sim.log

    # Check result
    if grep -q "ALL TESTS PASSED" logs/sim.log 2>/dev/null && ! grep -q "\[FAIL\]" logs/sim.log 2>/dev/null; then
        echo "[VERIFY] PASS — Verilog TB simulation passed"
    else
        echo "[VERIFY] FAIL — Verilog TB simulation errors detected"
        grep -E "\[FAIL\]|ERROR|error:" logs/sim.log 2>/dev/null | head -20
    fi
else
    echo "[VERIFY] No Verilog TB found"
fi
```

4. **If Verilog TB passed**, skip cocotb and go to step 7.

5. **If Verilog TB failed OR not available**, try cocotb simulation (if available):
```bash
source "$PROJECT_DIR/.veriflow/eda_env.sh"
cd "$PROJECT_DIR"

if [ "$COCOTB_AVAILABLE" = "true" ]; then
    echo "[VERIFY] Trying cocotb simulation as fallback..."

    # Run cocotb via runner
    $PYTHON_EXE "${CLAUDE_SKILL_DIR}/cocotb_runner.py" \
        --module $TOP_MODULE \
        --rtl-dir workspace/rtl \
        --tb-dir workspace/tb \
        --build-dir workspace/sim \
        --verbose 2>&1 | tee -a logs/sim.log

    # Check result
    if grep -q '"failed": 0' logs/sim.log 2>/dev/null && ! grep -q '"failed": [1-9]' logs/sim.log 2>/dev/null; then
        echo "[VERIFY] PASS — cocotb tests passed"
    else
        echo "[VERIFY] FAIL — cocotb simulation errors detected"
        grep -E "\[FAIL\]|ERROR|error:|traceback" logs/sim.log 2>/dev/null | head -20
    fi
else
    echo "[VERIFY] cocotb not available — cannot run cocotb simulation"
fi
```

6. **If simulation fails**, enter the fix loop:

   a. **Read error output** from `logs/sim.log`
   b. **Collect diagnostic data** — run vcd2table golden model diff (see Error Recovery Step 0 below)
   c. **Run structured root cause analysis** (see Error Recovery below)
   d. **Fix RTL** using Edit tool in main session
   e. **Re-run simulation** (go back to step 3)
   f. **Retry budget**: 3 attempts, then STOP and ask user

7. **If simulation passes**, run combined hook + state + journal:
```bash
source "$PROJECT_DIR/.veriflow/eda_env.sh" && $PYTHON_EXE "${CLAUDE_SKILL_DIR}/state.py" "$PROJECT_DIR" "verify_fix" --hook="grep -q 'ALL TESTS PASSED' logs/sim.log || grep -q '\"failed\": 0' logs/sim.log" --journal-outputs="logs/sim.log" --journal-notes="Simulation passed"
```

8. Mark Stage 3 task as completed via TaskUpdate.

### Stage 4: lint_synth (parallel subagents — vf-linter + vf-synthesizer)

Run lint and synthesis in parallel.

1. Record start times:
```bash
source "$PROJECT_DIR/.veriflow/eda_env.sh" && $PYTHON_EXE "${CLAUDE_SKILL_DIR}/state.py" "$PROJECT_DIR" "lint_synth" --start
```

2. Dispatch BOTH agents in a **single message** with two Agent tool calls:
   - Agent 1: vf-linter
   - Agent 2: vf-synthesizer

3. After BOTH return, check results:

   If lint failed → fix syntax errors in main session, re-run lint only.
   If synth failed → check synthesis report for issues, fix if needed.

4. Run combined hook + state + journal:
```bash
source "$PROJECT_DIR/.veriflow/eda_env.sh" && $PYTHON_EXE "${CLAUDE_SKILL_DIR}/state.py" "$PROJECT_DIR" "lint_synth" --hook="test -f logs/lint.log && test -f workspace/synth/synth_report.txt" --journal-outputs="logs/lint.log, workspace/synth/synth_report.txt" --journal-notes="Lint and synthesis complete"
```

5. Mark Stage 4 task as completed via TaskUpdate.

---

## Error Recovery

When Stage 3 (verify_fix) or Stage 4 (lint_synth) fails:

### Subagent Stage Error Recovery

For stages that use subagents, the error recovery flow:

1. **Subagent runs and reports** — returns a text summary. All artifacts written to disk.
2. **Main session reads artifacts** — reads diagnostic files (sim.log, wave_table.txt, etc.)
3. **Main session diagnoses** — Error Recovery Step 1.5 runs in main session, which has full design context.
4. **Main session fixes RTL** — Edit tool modifies the relevant RTL file(s).
5. **Re-run the failed stage** — go back to the failed stage's execution step.
6. **Retry budget** — 3-retry policy applies at orchestrator level.

**Key principle**: Subagents are **stateless workers** — they generate artifacts but do NOT diagnose or fix. The main session is the **only entity that modifies RTL**.

### Step 0: Data Collection + Bug Type Classification (MANDATORY)

Before forming ANY root cause hypothesis, collect objective diagnostic data. This step prevents the most common debug failure mode: guessing the wrong direction.

**0a. Collect data**:

1. Read `logs/sim.log` — extract all `[FAIL]` lines with cycle numbers
2. Extract VCD path and top module from sim.log:
```bash
source "$PROJECT_DIR/.veriflow/eda_env.sh"
cd "$PROJECT_DIR"
TOP_MODULE=$($PYTHON_EXE -c "
import json
spec = json.load(open('workspace/docs/spec.json'))
mods = spec.get('modules', {})
if isinstance(mods, dict):
    for k, v in mods.items():
        if v.get('module_type') == 'top':
            print(v.get('module_name', k)); break
elif isinstance(mods, list):
    for m in mods:
        if m.get('module_type') == 'top':
            print(m['module_name']); break
")
VCD_FILE=$(ls workspace/sim/*.vcd 2>/dev/null | head -1)
```
3. Run vcd2table golden model diff (if golden_model.py exists AND VCD is available):
```bash
if [ -f workspace/docs/golden_model.py ] && [ -n "$VCD_FILE" ] && [ -f "$VCD_FILE" ]; then
    $PYTHON_EXE "${CLAUDE_SKILL_DIR}/vcd2table.py" \
        --vcd "$VCD_FILE" \
        --golden-model workspace/docs/golden_model.py \
        --module $TOP_MODULE 2>&1 | tee logs/wave_diff.txt
elif [ -n "$VCD_FILE" ] && [ -f "$VCD_FILE" ]; then
    $PYTHON_EXE "${CLAUDE_SKILL_DIR}/vcd2table.py" \
        --vcd "$VCD_FILE" \
        --module $TOP_MODULE 2>&1 | tee logs/wave_table.txt
else
    echo "[VERIFY] No VCD file available — skipping waveform analysis. Rely on sim.log [FAIL] lines only."
fi
```
4. Read the diff/table output — identify first divergence cycle and signal

**0b. Classify bug type**:

| Type | Symptom | Direction |
|------|---------|-----------|
| **A. Computation error** | Output value wrong (not zero) or zero when expected non-zero | Trace datapath: formula, condition, index. Check golden model per-cycle comparison. |
| **B. Timing error** | Correct value but wrong cycle (early/late by 1) | Check pipeline alignment, register stages |
| **C. Protocol violation** | valid/ready timing violates handshake spec | Check handshake protocol, FSM transitions |
| **D. Initialization error** | First operation's output offset by constant | Check register init values, algorithm IV loading |

**0c. Anti-pattern warning**:

- **Do NOT assume timing issues without data.** If the golden model diff shows the divergent value is zero or a constant → Type A or D (logic/init error), NOT timing.
- If value is correct-but-wrong-cycle → Type B (timing)
- If valid/ready behavior violates spec → Type C (protocol)
- **Most bugs in synchronous single-clock-domain designs are Type A or D, not Type B.**

### Step 1: Diagnose
- Read the error output from the failed stage
- Read the relevant RTL files from `workspace/rtl/`
- **Reference `bug_patterns.md`** for a catalog of known bug patterns

### Step 1.5: Structured Root Cause Analysis (MANDATORY)

Before modifying ANY file, complete the analysis and write it to `stage_journal.md`.

#### 5-point root cause analysis

1. **Error location**: Which `[FAIL]` line? Which cycle? Which signal?
2. **Signal trace**: Which module drives it? Which `always` block?
3. **Root cause hypothesis**: Exact RTL line that is wrong.
4. **Minimal fix plan**: File, lines, exact change.
5. **Impact scope**: Which other signals/modules affected?

If you cannot form a hypothesis, STOP and ask the user. Do NOT guess-and-fix.

**Common simulation patterns**:

```
Pattern A — VPI timing (wide signals): cocotb + iverilog delays wide signal writes.
  → Fix: use 2-RisingEdge VPI-safe pattern in testbench

Pattern B — Off-by-one pipeline delay:
  → Fix: sample output one cycle later, OR remove extra register stage

Pattern C — Reset not clearing output register:
  → Fix: add output_reg to reset block

Pattern D — FSM stuck / missing transition:
  → Fix: check FSM transition condition

Pattern E — Handshake violation (valid deasserted too early):
  → Fix: hold valid until ready is seen

Pattern F — Data value mismatch (algorithm error):
  → Diagnose: compare RTL with golden model cycle-by-cycle
```

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
- Do NOT change module interfaces (ports) — Interface Lock
- Do NOT add/remove functionality
- **Functional integrity**: fix must NOT remove, disable, or stub out existing functionality
- Make minimal changes, fix one error at a time
- **Debug budget**: 3 fix-and-retry cycles max, then STOP and ask user

After fixing, re-run the failed stage to verify.

### Step 4: Log recovery to journal

```bash
printf "\n### Recovery: <stage_name>\n**Timestamp**: $(date -Iseconds)\n**Attempt**: <N>\n**Error type**: <syntax|logic|timing>\n**Fix summary**: <description>\n**Result**: <PASS|FAIL|PENDING>\n" >> "$PROJECT_DIR/workspace/docs/stage_journal.md"
```

### Retry Policy

1. **1st fail**: Fix RTL, retry the stage
2. **2nd fail**: Rollback to codegen and re-run from Stage 2
3. **3rd fail**: STOP and notify user

Rollback target (all error types):
- Always roll back to `codegen` — re-generate RTL from spec + golden_model

To perform a rollback:
```bash
$PYTHON_EXE "${CLAUDE_SKILL_DIR}/state.py" "$PROJECT_DIR" --reset codegen
```
