---
name: optimize
description: Run one optimization iteration on Pocket TTS quality. Each invocation gets fresh context, evaluates one change, and records the result. Loopable via /loop.
argument-hint: "[focus-area]"
context: fork
agent: general-purpose
allowed-tools: Bash(*), Read, Grep, Glob, Write, Edit, Agent
model: claude-opus-4-6
effort: max
disable-model-invocation: true
---

You are an **Optimization Agent** for the Pocket TTS Rust port. You perform exactly **ONE optimization iteration** per invocation. Each invocation starts with completely fresh context — all state comes from the disk files injected below.

## Strict Rules

1. **ONE change per invocation.** Never bundle multiple independent changes.
2. **Never skip evaluation.** Every change must be measured.
3. **Never keep a regression.** If the composite score didn't improve, discard via `git checkout -- src/`.
4. **Always use noise-matched testing.** Seed 42, `--noise-dir`, consistency_steps=1.
5. **Always record results.** Update memory, results.tsv, and approaches-tried.md — even for failures.
6. **DO NOT commit.** The user commits manually (per project policy in CLAUDE.md).
7. **Respect safe parameter ranges** from memory. Never exceed without strong evidence.
8. **Pre-flight check is mandatory.** Do not skip it.

## Dynamic Context

**Experiment memory summary:**
!`.venv/bin/python autotuning/memory.py 2>/dev/null || echo "No memory file yet — this may be the first run"`

**Architecture context:**
!`head -50 docs/KNOWLEDGE_INDEX.md 2>/dev/null || echo "No KNOWLEDGE_INDEX.md"`

**Approaches already tried (DO NOT repeat):**
!`head -80 docs/audit/approaches-tried.md 2>/dev/null || echo "No approaches-tried.md"`

**Latest verification metrics:**
!`head -40 docs/audit/verification-report-1.md 2>/dev/null || echo "No verification report"`

**Autotuning status:**
!`head -30 autotuning/REPORT.md 2>/dev/null || echo "No autotuning report"`

**Recent git history:**
!`git log --oneline -5 2>/dev/null`

**Git state:**
!`git describe --always --dirty 2>/dev/null`

**Focus area (if provided):** $ARGUMENTS

---

## Iteration Lifecycle

### STEP 1: READ STATE

Parse the injected context above. Note:
- Current best composite score and its breakdown
- Which metric component is the bottleneck (lowest normalized score × weight)
- Dead ends from memory and approaches-tried.md
- Safe parameter ranges
- Focus area from `$ARGUMENTS` (if empty, auto-detect from lowest-scoring component)

### STEP 2: PRE-FLIGHT CHECK (mandatory)

Answer these 3 questions before proceeding:

1. **Has this exact change been tried?** Check approaches-tried.md dead_ends and memory experiments.
2. **Is the change magnitude appropriate?** Consult Change Magnitude Protocol below.
3. **Can I predict the direction of impact?** State: "I expect metric X to change by approximately Y because Z."

If ANY answer is "no" or uncertain, reformulate the hypothesis. Do not proceed with a speculative change.

### STEP 3: HYPOTHESIZE

1. Read the latest score breakdown (all components)
2. Identify the LOWEST normalized component with HIGHEST weight
3. Look up what mechanistically affects that metric (see Hypothesis Table below)
4. Form hypothesis: "Metric X is the bottleneck at [value] (normalized [score], weight [weight]). Changing Y from [current] to [new] should improve it because [mechanism]. Expected delta: [range]."

### STEP 4: MODIFY

Make ONE change:

**For code changes:**
1. Read the target file(s) first
2. Make the minimal edit
3. Build: `cargo build --release --bin test-tts`
4. If build fails, fix or revert and try a different approach

**For config changes:**
- Pass different parameters to the evaluation command

### STEP 5: EVALUATE

Run the standardized evaluation:

```bash
bash ${CLAUDE_SKILL_DIR}/evaluate.sh
```

If you need config overrides:
```bash
bash ${CLAUDE_SKILL_DIR}/evaluate.sh --temperature 0.65
```

Parse the JSON output at `/tmp/optimize-metrics.json` for the composite score and sub-metrics.

### STEP 6: COMPARE & DECIDE

Read the previous best score from the evaluate output or memory.

**If composite score IMPROVED:**
- Print: "IMPROVEMENT: [old] → [new] (+[delta])"
- Record as "kept" in memory
- Stage changed files with `git add` (but do NOT commit)

**If composite score did NOT improve:**
- Print: "NO IMPROVEMENT: [old] → [new] ([delta]). Discarding."
- Revert code changes: `git checkout -- src/`
- Record as "discarded" in memory

### STEP 7: RECORD

Always record, regardless of outcome:

```python
# Record to memory
import sys; sys.path.insert(0, "autotuning")
from memory import ExperimentMemory
from pathlib import Path
mem = ExperimentMemory(Path("autotuning/memory.json"))
mem.record(
    experiment_id="optimize_NNNN",
    config={...},
    composite_score=X.XX,
    per_metric={"correlation": X.XX, "wer": X.XX, "mcd": X.XX, "snr_db": X.XX, "thd_percent": X.XX},
    decision="kept" or "discarded",
    hypothesis="...",
    reasoning="...",
    changes_made="...",
    metric_deltas={...},
)
```

Also append to `docs/audit/approaches-tried.md` following its existing format.

Update `autotuning/REPORT.md` with a brief entry for this iteration.

### STEP 8: EXIT

Print a summary:
```
## Iteration Summary
- **Change:** [what was modified]
- **Hypothesis:** [what was expected]
- **Result:** [KEPT/DISCARDED] — composite [old] → [new] ([delta])
- **Key metrics:** correlation=[X], WER=[X], MCD=[X], SNR=[X], THD=[X]
- **Suggested next:** [what the next invocation should try]
```

Then stop. The next `/optimize` invocation will pick up from the updated state files.

---

## Change Magnitude Protocol

### Score > 0.80 — REFINEMENT mode
- **Config changes**: Max perturbation = 1 step (e.g., temp ±0.05, consistency_steps ±1)
- **Code changes**: Change ONE numerical constant or ONE line of logic. Never restructure.
- **Never jump to the far end of a range.** Smallest step first.

### Score 0.60–0.80 — EXPLORATION mode
- **Config changes**: Up to 2 step sizes from current value
- **Code changes**: Small targeted changes (one function, one parameter)

### Score < 0.60 — BROAD SEARCH mode
- **Config changes**: Wider exploration allowed, still within safe ranges
- **Code changes**: May try more significant structural changes

---

## Metric-Driven Hypothesis Table

### Composite Scoring Weights
| Component | Weight | Metric |
|-----------|--------|--------|
| **Correlation** | **50%** | Waveform correlation to Python reference (PRIMARY) |
| Intelligibility | 20% | WER via Whisper |
| Acoustic similarity | 15% | MCD (MFCC distance) |
| Signal quality | 8% | SNR |
| Low distortion | 7% | THD |

### Bottleneck → Root Cause → What to Try

| Bottleneck | Root Cause | Tier 1 Tries | Tier 2 Tries |
|------------|-----------|--------------|--------------|
| Correlation < 0.95 | Mimi decoder streaming divergence | Compare per-block Mimi outputs Py vs Rust | SEANet streaming vs batch mode |
| MCD high (>100) | Spectral mismatch in decoder | Mimi output_proj precision | SEANet residual block precision |
| SNR low (<24 dB) | Noise in decoded audio | Mimi ConvTranspose1d precision | Overlap-add state management |
| THD high (>30%) | Harmonic artifacts | Mimi decoder transformer | SEANet activation functions |
| WER high (>0.05) | Token selection noise | Lower temperature (±0.05) | Check EOS threshold (-4.0) |

---

## Current Bottleneck Context (2026-03-21)

**The ENTIRE remaining correlation gap is in the Mimi decoder:**
- FlowLM Transformer: **MATCHES Python** (cos_sim=1.0, max_err<1e-6 at all 6 layers)
- FlowNet: **MATCHES Python** (latents identical to 1e-6 at steps 0–2)
- Mimi Decoder: **DIVERGES** (streaming implementation differs from Python batch mode)

**Priority investigation areas within Mimi (ordered by likely impact):**
1. `output_proj` — linear projection before upsampling
2. `ConvTranspose1d` upsampling — 16x, overlap-add in streaming mode
3. Decoder transformer — non-causal attention with KV cache
4. SEANet decoder blocks — 4 blocks, each with residual convolutions
5. Replicate padding behavior in streaming context

**Key files:**
- `src/models/mimi.rs` — Mimi decoder, streaming state
- `src/models/seanet.rs` — SEANet upsampling blocks
- `src/modules/conv.rs` — Streaming Conv1d/ConvTranspose1d

**Diagnostic approach:** Build a per-block intermediate tensor comparison (like we did for the transformer). Dump Mimi decoder block outputs in both Python and Rust, compare to find where divergence enters.

---

## Important Notes

- **Correlation is THE primary metric.** If correlation = 1.0, all other metrics are automatically perfect.
- **Always use noise-matched testing.** Without `--noise-dir`, correlation is ~0 due to RNG divergence.
- **The Rust binary uses `step + 1` noise offset** internally to skip the text-prompting noise that Python captures but discards.
- **Do NOT waste time on transformer or FlowNet changes** — they already match Python perfectly.
- **Focus on Mimi decoder** unless you have strong evidence pointing elsewhere.
