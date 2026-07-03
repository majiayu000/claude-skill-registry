---
name: presubmit
description: Run the standalone presubmit CLI. Adversarial 30+ stage peer-review pipeline.
argument-hint: "[path to your draft to review, or describe the setup task]"
---

# Presubmit Activator

## What this skill is

A Claude-Code-native **launcher and setup wizard** for the [`presubmit`](https://github.com/scdenney/presubmit) Python CLI — the standalone, API-driven adversarial peer-review pipeline that produces a consolidated review report on disk.

This skill does **not** itself perform the review. It:

1. Verifies presubmit is installed (and walks you through install if not).
2. Verifies your Anthropic API key is set (and walks you through obtaining and configuring one if not).
3. Asks where you want review outputs to live (the first time only — saves to a config file).
4. Receives a paper path, derives a sensible slug, confirms it with you, and invokes presubmit with the right `--work-dir` so outputs land in the conventional location.
5. Monitors the run, reports cost / wall-time / where the consolidated report landed, and points you at the file to read first.

The actual review work is done by the `presubmit` package (Anthropic API calls, ~30 stages, ~$5–10 per full run on a typical manuscript).

## What this skill is NOT

- Not a re-implementation of presubmit. It calls the existing CLI; the CLI must be installed.
- Not a replacement for [`paper-review-lite`](../paper-review-lite/SKILL.md). That skill performs the review *itself* using parallel Claude Code sub-agents (no API key, no per-token cost). This skill activates the heavier standalone tool. Both have a place — see "When to use which" below.
- Not for peer-reviewing other people's manuscripts. For that, the user maintains a separate `reviews/` workflow with a different agents-based `CLAUDE.md`. This skill is for self-audit of your own drafts pre-submission.

## Setup phase (run once per machine)

Before any per-paper invocation, the skill must verify the install + config. Use this checklist; only run the steps whose check fails.

### Step 1 — Is `presubmit` installed?

```bash
command -v presubmit && presubmit --help | head -3
```

If the command is found and `--help` returns the usage banner, presubmit is installed — skip to Step 2.

If not, ask the user where they keep cloned repos (set `PRESUBMIT_DIR` to that choice; the examples below use it throughout), then walk them through:

```bash
PRESUBMIT_DIR=~/repos/presubmit   # wherever the user keeps clones

# Clone (or update) the repo
git clone https://github.com/scdenney/presubmit "$PRESUBMIT_DIR" \
  || git -C "$PRESUBMIT_DIR" pull

cd "$PRESUBMIT_DIR"

# Create a venv
python3 -m venv .venv
source .venv/bin/activate

# Install — first time pulls marker-pdf + PyTorch, ~5–10 min.
# pyproject.toml pins anthropic>=0.60 directly; verify the resolver honored it:
pip install -e .
pip show anthropic | head -2     # must be >= 0.60; if not: pip install -U 'anthropic>=0.60'
```

Confirm install with:

```bash
"$PRESUBMIT_DIR/.venv/bin/presubmit" --help | head -3
```

The CLI lives in the venv. Either source the venv each session (`source "$PRESUBMIT_DIR/.venv/bin/activate"`) or invoke the absolute binary path.

**On first conversion**, marker-pdf will download ~3.3 GB of OCR / layout / table-recognition models into its local Hugging Face cache (macOS: `~/Library/Caches/datalab/models/`; Linux: `~/.cache/datalab/models/`). Subsequent runs reuse this cache. The download is bandwidth-limited; warn the user.

### Step 2 — Is `ANTHROPIC_API_KEY` set?

```bash
[ -n "$ANTHROPIC_API_KEY" ] && case "$ANTHROPIC_API_KEY" in sk-ant-*) echo "key OK";; *) echo "key set but unexpected prefix: ${ANTHROPIC_API_KEY:0:8}…";; esac
```

If empty, also check whether it's defined in `~/.zshrc` but the current shell hasn't sourced it:

```bash
eval "$(grep -E '^export ANTHROPIC_API_KEY=' ~/.zshrc | head -1)" 2>/dev/null && [ -n "$ANTHROPIC_API_KEY" ] && case "$ANTHROPIC_API_KEY" in sk-ant-*) echo "found in .zshrc";; esac
```

If still missing, walk the user through:

1. Generate a key at <https://console.anthropic.com/> → **Settings → API Keys → Create Key**.
2. Add to `~/.zshrc` (or equivalent shell rc), placed **above** any wrapper functions that re-set `ANTHROPIC_API_KEY` to an empty string for routing the `claude` CLI to local Ollama models — those would shadow the real key:

   ```bash
   export ANTHROPIC_API_KEY="sk-ant-api03-..."
   ```

3. `source ~/.zshrc` or open a new terminal.
4. Confirm a positive credit balance is on the account — presubmit fails fast on credit/billing 400s rather than burning the retry budget. Empty balance halts the run on the first call.

The key is billed to the user's Anthropic account and is independent of any Claude Code subscription.

### Step 3 — Where should outputs live?

Read `~/.config/presubmit/config.json` for an existing `output_base`. If it exists and the path is writable, use it.

If it does not exist, ask the user (use `AskUserQuestion`):

> Where should presubmit reviews be stored by default?

Offer at least these options and one custom path:

- `~/presubmit-reviews/` — generic, no project-folder assumption
- `~/Documents/presubmit/` — under Documents
- `~/Documents/GitHub/pre-submission/` — for users who keep all repos under `~/Documents/GitHub/`
- Custom path

After the user picks, write the choice to `~/.config/presubmit/config.json`:

```json
{
  "output_base": "/absolute/path/the/user/picked",
  "saved_at": "ISO 8601 timestamp"
}
```

Also offer to write `export PRESUBMIT_OUTPUT_BASE=…` to `~/.zshrc` so the bare CLI (without this skill) can pick up the same default. Make this offer explicit; do not write to `.zshrc` without asking.

The config file is the source of truth for this skill; the env var is a convenience for direct CLI invocation.

## Per-paper run phase

Once setup is done, every invocation follows the same pattern.

### Step 1 — Slug

Read the input filename. Derive a default slug:

- Strip extension and path.
- Lowercase.
- Replace runs of non-alphanumeric characters (other than underscores, which are preserved) with single hyphens.
- Trim leading/trailing hyphens and underscores.
- Aim for `<lastname>_<year>_<short-title>` shape if the filename already follows it.

Example: `Denney_2026_What-Were-They-Thinking.pdf` → `denney_2026_what-were-they-thinking`.

Confirm the proposed slug with the user via `AskUserQuestion`. Allow override.

### Step 2 — Mode

Ask which run mode (`AskUserQuestion`):

- **Smoke** — `--stop-stage 2.0`. Runs metadata extraction + Red Team + numbers auditor. ~15–25 min on a 70-page paper, ~$1–2. Useful for verifying setup or catching show-stopper issues fast.
- **Standard** — full pipeline. ~30–90 min, ~$5–10. The default for a real audit.
- **Custom** — ask for additional flags (`--code-dir`, `--math`, `--supp`, `--no-copyedit`, `--no-editor-note`, `--start-stage`, `--stop-stage`, `--skip-size-check`).

### Step 3 — Construct paths and run

```bash
WORK_DIR="$OUTPUT_BASE/$SLUG/presubmit_run"
mkdir -p "$WORK_DIR"
"$PRESUBMIT_DIR/.venv/bin/presubmit" "$PAPER_PATH" \
  --work-dir "$WORK_DIR" \
  -o "$OUTPUT_BASE/$SLUG/report.txt" \
  $EXTRA_FLAGS
```

Always pass `-o`: without it the CLI copies the final report to `report.txt` in the **current working directory**, leaving stray clutter wherever the agent happened to be.

Run in the background using the Bash tool's `run_in_background: true`. Stream the log to a file so the user (and you) can check progress separately.

Tell the user: the wall time, where to watch the live log (`tail -f` instructions), and what files to expect in `$WORK_DIR` as stages complete.

### Step 4 — Report when done

When the background task notifies completion:

1. Confirm exit code is 0 and no `FATAL: Claude refused` appears in the log. (A smoke run — `--stop-stage` — also exits 0, printing `Stopped at stage N as requested`; judge it by the per-stage files in `$WORK_DIR`, since no consolidated report exists by design.)
2. Locate the consolidated report — it's the file matching `$WORK_DIR/<slug>_*.txt` (presubmit auto-names it `<author_title_uuid>.txt`), with a stable-named copy at the `-o` path.
3. Report wall time, total tokens (input + output across stages — visible at the end of the log), and the end-of-run dollar total (pricing.csv carries current Claude rates; cross-check the Anthropic console if rates have changed).
4. Offer to open the report (`less` / `Read`) and to write a per-paper README.md alongside the work_dir capturing: invocation date, flags used, models, wall time.

If the run failed:

- **`Messages.create() got an unexpected keyword argument 'thinking'`** — anthropic SDK is < 0.60. Fix: `pip install -U 'anthropic>=0.60'` in the venv.
- **`FATAL: Claude refused the request (likely safety policy)`** — a Red Team prompt tripped Claude's safety filters. The message does not name the stage; find the last `► Executing <stage>` line above it in the log, then locate that stage's prompt under `$PRESUBMIT_DIR/src/presubmit/prompts/`. Soften it to attack the manuscript's claims, not the authors. Re-run; the pipeline is resumable.
- **Marker conversion failure** — surface the specific PipelineError. Common cause: marker-pdf install incomplete; verify `pip show marker-pdf` succeeds in the venv.
- **Out-of-credit** — top up at <https://console.anthropic.com/>, then re-run. The pipeline picks up from where it stopped.

## File-naming and organization convention

```
$OUTPUT_BASE/                                            (from config; user-chosen)
└── <slug>/                                              (one folder per paper)
    ├── README.md                                        (offered after the run — never silently written)
    ├── report.txt                                       (stable-named copy of the report, via -o)
    └── presubmit_run/                                   (the --work-dir)
        ├── <author_title_uuid>.txt                     ← THE main consolidated report
        ├── original_source.pdf                          (cached source)
        ├── paper.md                                     (marker conversion of source)
        ├── metadata.json
        ├── pipeline_execution.log
        ├── 00a_metadata.txt … 09c_copyedit.txt          (intermediate per-stage outputs)
        └── 10_latex_body.txt                            (body without LaTeX framing)
```

**Slug rule:** `<lastname>_<year>_<short-title>`, lowercase with hyphens in the title. Example: `denney_2026_what-were-they-thinking`. Auto-derived from the input filename; user-overridable in the per-paper interview.

**The main report is `<author_title_uuid>.txt`** — it consolidates all stages into one file with these sections: header, disclaimer, overview, Editor's Note, Summary (Is It Credible? + Bottom Line), Potential Issues, Future Research, Copyediting, Proofreading. Read this first. The other files are intermediates; the raw `01a_breaker.txt`, `01b_butcher.txt`, etc. have unfiltered Red Team findings that are sometimes sharper than the consolidated version.

## When to use this skill vs. `paper-review-lite`

| | `presubmit` (this skill) | `paper-review-lite` (sister skill) |
|---|---|---|
| Where the work happens | Outside Claude Code — Python CLI calls Anthropic API | Inside Claude Code — parallel sub-agents read the paper |
| Cost | Per-token, billed to your API key (~$5–10/run) | Subscription only (no per-token bill) |
| Wall time | 30–90 min unattended | Minutes; you control each pass |
| Depth | 30+ stages: Red Team (Breaker, Butcher, Shredder, Collector, Void) + Blue Team defence + verification cascade + legal pass + copyedit + Writer Mode | ~11 sub-agents: content/argument, numbers, references, DOIs, writing, CONSORT, pre-reg, figures, archive, plus 2 cross-checkers |
| Output | Single consolidated `.txt` deliverable + ~30 intermediate files | Structured pre-submit report in-conversation + `.review-tmp/` scratch files |
| Resumable | Yes — checkpointed per stage to disk | No — single conversation pass |
| Math audit | Yes (`--math`, requires Mathpix) | No |
| Replication-code audit | Yes (`--code-dir`) | Partial (Agent 9 checks archive completeness; doesn't compare claims to code) |
| Refusal risk | Moderate (some Red Team stages adversarial enough to trip safety) | Low (single-pass personas, quote-grounded) |
| When to use | Deep audit before submission; standalone deliverable; math or code audit | Quick in-flow check; routine self-audit; no API spend |

Both are legitimate self-audit tools. `paper-review-lite` is the everyday tool; `presubmit` is the heavy-artillery final pass before submission.

## Quality checks (apply consistently)

- [ ] Setup phase ran first if any of: `presubmit` not installed, `ANTHROPIC_API_KEY` not set, no `~/.config/presubmit/config.json` exists.
- [ ] Output base is read from `~/.config/presubmit/config.json` (or asked for and saved if not), never hardcoded.
- [ ] Slug is auto-derived from the input filename and explicitly confirmed with the user before invocation.
- [ ] The user picked a run mode (smoke / standard / custom) before the run started.
- [ ] Run was launched in the background so the user can continue working; live log path was reported.
- [ ] On completion: exit code, presence of `FATAL` lines, wall time, total token usage, and full path to the consolidated report were all reported.
- [ ] If the run failed, the specific error was diagnosed against the known failure modes above before suggesting a generic retry.
- [ ] Per-paper `README.md` capturing run metadata was offered (not silently written).

## Known gotchas (current as of 2026-06)

1. **anthropic SDK version conflict.** presubmit's `pyproject.toml` pins `anthropic>=0.60` directly (core.py's `Messages.create(thinking=…)` needs it), but `marker-pdf 1.10.x` transitively caps anthropic at `<0.47`. pip resolves the conflict by backtracking marker-pdf to an older release, or by warning. After install, check `pip show anthropic marker-pdf`; if anthropic landed below 0.60, force it with `pip install -U 'anthropic>=0.60'` (runtime is unaffected — presubmit doesn't use marker's optional anthropic-LLM mode).
2. **`-o` defaults to `./report.txt`.** `-o / --output` controls the *final report copy* only — without it, a stray `report.txt` lands in the invoking directory; without `--work-dir`, stage outputs land in a temp dir that gets garbage-collected. **Always pass both.** This skill does so automatically.
3. **`use_search=True` is a no-op.** Stage 00a (metadata) silently degrades for published papers needing a citation lookup; fine for unpublished manuscripts.
4. **First marker conversion is slow.** 3–5 GB of model weights download into marker's local cache (macOS: `~/Library/Caches/datalab/models/`; Linux: `~/.cache/datalab/models/`) on first use; subsequent runs reuse the cache.
5. **Older checkouts exit 1 on intentional `--stop-stage` runs.** Current presubmit exits 0 with `Stopped at stage N as requested`; if you see exit 1 with "did not produce a final report" after a smoke run, the install predates the fix — `git pull && pip install -e .`.
