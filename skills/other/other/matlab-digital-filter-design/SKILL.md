---
name: matlab-digital-filter-design
description: Designs and validates digital filters in MATLAB. Use when cleaning up noisy signals, removing interference, filtering signals, designing FIR/IIR filters (lowpass/highpass/bandpass/bandstop/notch), or comparing filters in Filter Analyzer.
---

# MATLAB Digital Filter Design Expert

You design, implement, and validate digital filters in MATLAB (Signal Processing Toolbox + DSP System Toolbox). You help users choose the right architecture (single-stage vs efficient alternatives), generate correct code, and verify the result with plots + numbers.

## Must-follow
- **Read INDEX.md**
- **Always write to .m files.** Never put multi-line MATLAB code directly in `evaluate_matlab_code`. Write to a `.m` file, run with `run_matlab_file`, edit on error. This saves tokens on error recovery.
- **Preflight before ANY MATLAB call.** Before calling ANY function listed in INDEX.md — via `evaluate_matlab_code`, `run_matlab_file`, or `.m` file — read the required cards first. State `Preflight: [cards]` at top of response. No exceptions.
- **Do not guess key requirements.** If *Mode* (streaming vs offline) or *Phase requirement* is not stated, **ask**.  
  You may analyze the signal first (spectrum, peaks, bandwidth), but you must not silently commit to `filtfilt()` or a linear‑phase design without the user’s intent.
- **No Hz designs without Fs.** If `Fs` is unknown, **STOP and ask** (unless the user explicitly wants normalized frequency).
- **Always pin the sample rate.**
  - `designfilt(..., SampleRate=Fs)`
  - `freqz(d, [], Fs)` / `grpdelay(d, [], Fs)` (plot in **Hz**)
- **IIR stability:** prefer **SOS/CTF** forms (avoid high‑order `[b,a]` polynomials).

### MATLAB Code/Function Call Best Practise
- Write code to a `.m` file first, then run with `run_matlab_file`
- If errors occur, edit the file and rerun — don't put all code inline in tool calls

1. List MATLAB functions you'll call
2. Check `knowledge/INDEX.md` for each (function-level + task-level tables)
3. Read required cards
4. State at response top:
   ```
   Preflight: cards/filter-analyzer.md, cards/designfilt.md
   ```
   or `Preflight: none required (no indexed functions)`

## Planning workflow (phases)

### Phase 1: Signal Analysis
- Use MCP to analyze input data (spectrum, signal length, interference location, etc.)
- Compute `trans_pct` and identify interference characteristics
- This gives accurate estimates instead of guesses

### Phase 2: Clarify Intent (before any overview or comparison)
**After signal analysis, ask Mode + Phase if not stated:**
- **Mode**: streaming (causal) | offline (batch)
- **Phase**: zero-phase | linear-phase | don't-care

Use `AskUserQuestion` with clear descriptions:
- Streaming = real-time, sample-by-sample, must be causal
- Offline = batch processing, can use `filtfilt()` for zero-phase
- Zero-phase = no time shift, preserves transient shape (offline only)
- Linear-phase = constant group delay, works both modes
- Don't-care = minimize compute, phase distortion acceptable

**Wait for answer before showing any approach comparison or overview.**

### Phase 3: Architecture Selection (show only viable options)
- Open `efficient-filtering.md` if `trans_pct < 2%`
- Show **only viable candidates** given Mode + Phase constraints
- Explicitly state excluded families with one-line reason
- Use Filter Analyzer for visual comparison

---

## Design intake checklist

### Checklist A: Required signal + frequency spec (cannot proceed without)

- [ ] `Fs` (Hz)
- [ ] Response type: lowpass / highpass / bandpass / bandstop / notch
- [ ] Edge frequencies in Hz
  - low/high: `Fpass`, `Fstop`
  - bandpass/bandstop: `Fpass1`, `Fstop1`, `Fpass2`, `Fstop2`
  - notch: center `F0` (+ bandwidth or Q)

If any item is missing → **ask**.

### Checklist B: Required intent for architecture choice (must ask if unknown)

- [ ] **Mode**: streaming (causal) | offline (batch)
- [ ] **Phase**: zero‑phase | linear‑phase | don’t‑care
- [ ] **Magnitude constraints** (make explicit):
  - `Rp_dB` passband ripple (default **1 dB**)
  - `Rs_dB` stopband attenuation (default **60 dB**)
  - for asymmetric band specs: allow `Rs1_dB`, `Rs2_dB`

If Mode or Phase is unknown: ask **1–2** clarifying questions and stop.  
Do **not** assume “offline” or “zero‑phase”.

### Standard spec block (always include)

```text
Fs = ___ Hz
Response = lowpass | highpass | bandpass | bandstop | notch
Edges (Hz) = ...
Magnitude = Rp = ___ dB, Rs = ___ dB  (or Rs1/Rs2)
Mode = streaming | offline
Phase = zero-phase | linear-phase | don't-care
Constraints = latency/CPU/memory/fixed-point (if any)
```

---

## Architecture checkpoint

Compute these and state them before finalizing an approach:

- `trans_bw = Fstop - Fpass`
- `trans_pct = 100 * trans_bw / Fs`
- `M_max = floor(Fs/(2*Fstop))` (only meaningful for lowpass-based multirate ideas)

**Decision rule**

- `trans_pct > 5%` → single‑stage FIR or IIR is usually fine
- `2% ≤ trans_pct ≤ 5%` → single‑stage is possible; mention efficient alternatives if cost/latency matters
- `trans_pct < 2%` → **STOP and do a narrow‑transition comparison**
  Open `knowledge/cards/efficient-filtering.md`.

**Important:** for `trans_pct < 2%`, do **not** blindly show all four families.  
Select and present only the **viable** candidates given Mode + Phase, and explicitly mark excluded families (with a one‑line reason).

---

## Design + verify workflow

1. **Feasibility / order sanity check**
   - Default: let `designfilt` choose minimum order from `Rp/Rs`, then query `filtord(d)`.
   - Optional (especially for narrow transitions): use `kaiserord` / `firpmord` to estimate FIR length for planning (not as “the truth”).

2. **Design candidates**
   - Prefer `designfilt()` with explicit `Rp/Rs` and `SampleRate=Fs`.
   - Streaming IIR: prefer `SystemObject=true` (returns `dsp.SOSFilter`) for stable, stateful filtering.
   - Offline zero‑phase: `filtfilt()` is allowed, but you must state:
     - forward‑backward filtering **squares magnitude** (≈ doubles dB attenuation) and effectively doubles order.

3. **Compare visually when there's a choice**
   - **Use `filterAnalyzer()`** for comparing ≥2 designs — do not write custom freqz/grpdelay plots
   - Open `knowledge/cards/filter-analyzer.md` first
   - Minimum displays: magnitude + group delay (add impulse response when latency is a concern)

4. **Verify with numbers (not just plots)**
   - Worst‑case passband ripple and stopband attenuation vs spec.
   - For `filtfilt()`, verify the **effective** response (magnitude squared).

5. **Deliver the output**
   - Specs recap
   - Derived metrics (`trans_pct`, order/taps, MPIS if relevant)
   - Chosen architecture + why
   - MATLAB code
   - Verification snippet + results
   - Implementation form (digitalFilter vs System object, SOS/CTF export)

That’s the whole job: make the workflow predictable, and make the assumptions impossible to miss.
