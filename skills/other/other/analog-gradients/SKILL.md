# skill.md

How-to guide for this repository.

---

## Quick Start

```bash
source setup_cadence.sh
./build.sh all
```

---

## Run Spectre Simulation

```bash
cd results/<name>
spectre /path/to/netlists/<name>.scs -raw <name>.raw +log spectre.log
```

Check: `grep "completes with 0 errors" spectre.log`

---

## Run OCEAN Verification

```bash
ocean -nograph < ocean/test_<name>.ocn
cat results/<name>_test.txt
```

---

## Run SKILL Replay (Virtuoso Headless-Friendly)

```bash
./scripts/virtuoso_replay.sh skill/L5_inverter.il
```

---

## Create a New Gate

### 1. Write the netlist

`netlists/and2.scs`:
```
simulator lang=spectre
parameters vdd_val=1.8

model nch mos1 type=n vth=0.4 kp=120u
model pch mos1 type=p vth=-0.4 kp=40u

V_VDD (vdd 0) vsource dc=vdd_val
V_A (a 0) vsource type=pulse val0=0 val1=1.8 delay=10n rise=100p fall=100p width=10n period=20n
V_B (b 0) vsource type=pulse val0=0 val1=1.8 delay=20n rise=100p fall=100p width=20n period=40n

// AND2 = NAND2 + Inverter
// NAND stage
MP0 (nand_out a vdd vdd) pch w=2u l=1u
MP1 (nand_out b vdd vdd) pch w=2u l=1u
MN0 (nand_out a mid 0) nch w=2u l=1u
MN1 (mid b 0 0) nch w=2u l=1u

// Inverter stage
MP2 (out nand_out vdd vdd) pch w=2u l=1u
MN2 (out nand_out 0 0) nch w=1u l=1u

tran_test tran stop=80n
save out a b
```

### 2. Write the test

`ocean/test_and2.ocn`:
```lisp
out = outfile("/home/v71349/analog-gradients/results/and2_test.txt" "w")
fprintf(out "=== AND2 Verification ===\n")

simulator('spectre)
openResults("/home/v71349/analog-gradients/results/and2/and2.raw")
selectResult("tran_test-tran")

vout = v("out")
vth_low = 0.36
vth_high = 1.44
pass = t

; A=0,B=0 -> 0
v = value(vout 5n)
fprintf(out "A=0,B=0: %.3f " v)
if(v < vth_low then fprintf(out "[PASS]\n") else fprintf(out "[FAIL]\n") pass=nil)

; A=1,B=0 -> 0
v = value(vout 15n)
fprintf(out "A=1,B=0: %.3f " v)
if(v < vth_low then fprintf(out "[PASS]\n") else fprintf(out "[FAIL]\n") pass=nil)

; A=0,B=1 -> 0
v = value(vout 25n)
fprintf(out "A=0,B=1: %.3f " v)
if(v < vth_low then fprintf(out "[PASS]\n") else fprintf(out "[FAIL]\n") pass=nil)

; A=1,B=1 -> 1
v = value(vout 35n)
fprintf(out "A=1,B=1: %.3f " v)
if(v > vth_high then fprintf(out "[PASS]\n") else fprintf(out "[FAIL]\n") pass=nil)

if(pass then fprintf(out "\n=== PASS ===\n") else fprintf(out "\n=== FAIL ===\n"))
close(out)
exit()
```

### 3. Run it

```bash
mkdir -p results/and2
cd results/and2
spectre ../../netlists/and2.scs -raw and2.raw +log spectre.log
cd ../..
ocean -nograph < ocean/test_and2.ocn
cat results/and2_test.txt
```

---

## Compose Circuits

Instantiate subcircuits in netlists:

```
// Include subcircuit definition or define inline
subckt inverter (in out vdd)
  MP0 (out in vdd vdd) pch w=2u l=1u
  MN0 (out in 0 0) nch w=1u l=1u
ends inverter

// Instantiate
I0 (a a_inv vdd) inverter
I1 (b b_inv vdd) inverter
```

---

## Debug Tips

- Check `spectre.log` for simulation errors
- PSF results named `tran_test-tran` (with hyphen)
- OCEAN needs: `selectResult("tran_test-tran")` (quoted string)
- Voltage thresholds: LOW < 0.36V, HIGH > 1.44V (for VDD=1.8V)

---

## CMC Cloud Access

```bash
ssh -Y -p 31487 v71349@130.15.52.59
source /CMC/scripts/cadence.ic23.10.140.csh  # if using tcsh
# or
source setup_cadence.sh  # if using bash
```

---

## Field Notes (OCEAN / Spectre / SKILL)

Short, forum-ready answers distilled from real runs.

### Licensing (LMC-01902)

If Spectre says the license search path is `<none>`, set a license variable:

```bash
export CDS_LIC_FILE=6055@licaccess.cmc.ca   # CMC host default observed
# or
export LM_LICENSE_FILE=27000@license.server
```

Then re-run:

```bash
source setup_cadence.sh
./build.sh inverter
```

### OCEAN in batch mode

- Always write output to a file (stdout is buffered).
- `selectResult("tran_test-tran")` must be a **string** because of the hyphen.
- Avoid fancy SKILL constructs in batch (e.g., lambdas). Explicit checks are more reliable.

### Spectre netlist gotchas

- Keep `subckt` pin lists **on one line**. Multi-line pin lists caused parse errors.
- Use simple `mos1` models (per repo templates) to avoid PDK dependencies.
- Use `save` statements to ensure OCEAN can access signals.

### Virtuoso automation

- Headless replay helper: `./scripts/virtuoso_replay.sh`
- If `DISPLAY` is unset, the runner will try `xvfb-run` if available.
- SKILL-based schematic creation still needs X11 on CMC; netlist flow is the stable path.

### Full-flow demo operations (DC -> Innovus -> Calibre)

- Use `scripts/run_fullflow_smoke.sh` for the standard replay path.
- If DC is license-blocked (`DCSH-1`), the flow can continue using:
  `implementation/fullflow_demo/rtl/alu4_flow_demo_fallback_mapped.v`.
- Calibre license failures are recorded explicitly in:
  `implementation/fullflow_demo/work/calibre/alu4_flow_demo_calibre_license.warn`.
- For CI or strict gating, use:
  `env FULLFLOW_STRICT=1 scripts/run_fullflow_smoke.sh`
  (returns non-zero when any stage is blocked).

### Demo asset generation

- One-command visual refresh:
  `scripts/run_competition_visuals.sh`
- Coupled-tile waveform assets are generated under:
  - `competition/plots/neuro_tile4_coupled_spikes.svg`
  - `competition/plots/neuro_tile4_coupled_mems.svg`
- Before recording, pre-run long flows and verify artifact existence so the
  live capture can focus on the key moments (PASS cascade, waveform evidence,
  GDS output).

### Recording workflow

- Build scene-organized assets with:
  `scripts/build_recording_pack.sh`
- Guided pacing for one-take capture:
  `scripts/demo_narrator.sh`
- Fast rehearsal without long tool runtime:
  `DEMO_SKIP_LONG=1 scripts/demo_narrator.sh`

### LaTeX paper workflow

- Prepare parsed paper datasets:
  `python3 scripts/prepare_paper_data.py`
- Build paper (if LaTeX engine is installed):
  `scripts/build_paper.sh`
- Main source:
  `competition/paper/neurocore_workthrough.tex`
- Plot style choice for evidence: dark background + unsmoothed raw data points.

### Founder-thesis tracking

- Canonical thesis reference:
  `competition/founder-thesis.md`
- Keep claims tied to reproducible evidence:
  - ODE fit
  - timing sensitivity (`dt_spike/dparameter`)
  - energy per event
- Current analysis commands:
  - `python3 scripts/analyze_lif_ode_fit.py`
  - `python3 scripts/analyze_temporal_sensitivity.py`
  - `scripts/analyze_lif_energy.sh`
- Mixed-signal smoke command:
  - `./build.sh neuro_tile4_mixed_signal`
