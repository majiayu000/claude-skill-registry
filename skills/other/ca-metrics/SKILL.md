---
name: ca-metrics
description: Read-only 3-metric governance glance — override rate, small-lane rate, sprint low-confidence ratio — each with a trend arrow vs. the prior 20-commit window.
argument-hint: "[--window N]"
---

# $ca-metrics — governance trend glance

A bare-numbers summary of the three governance-health metrics that `_metricslib.py`
tracks across commit windows. Each metric shows its value for the **current** 20-commit
window and a direction arrow (↑/↓/→) relative to the immediately preceding window.

This is NOT a second `$ca-audit` packet. It prints numbers and arrows only — no
verbatim override lines, no commit list, no file write. Use it to spot a trend at a
glance; reach for `$ca-audit` when you need the full evidentiary packet.

## Flow

1. **Invoke the helper.** Call the thin entry hook `metrics.py`, which wraps
   `compute` from `_metricslib.py`, via a Windows-safe `python3 … || python …`
   fallback. Pass `<project-root>` as `--root`. If `--window N` was
   supplied, pass it through as `--window N`; otherwise omit it (the helper
   applies the default of 20).

   ```
   python3 "${CLAUDE_PLUGIN_ROOT}/hooks/metrics.py" --root "<project-root>" || python "${CLAUDE_PLUGIN_ROOT}/hooks/metrics.py" --root "<project-root>"
   ```

   > **`ensure_ascii` note — do not remove this.** `metrics.py` calls `json.dumps`
   > with its default `ensure_ascii=True`. This ASCII-escapes the arrow glyphs
   > (↑↓→) in the subprocess stdout, which avoids a `UnicodeEncodeError` on Windows
   > `cp1252` consoles that cannot encode those code-points raw. The rendered output
   > you present to the user (step 2 below) uses the real glyphs — they are written
   > by the assistant, not piped through the subprocess stdout. Do NOT add
   > `ensure_ascii=False` here.

   With a custom window size:
   ```
   python3 "${CLAUDE_PLUGIN_ROOT}/hooks/metrics.py" --root "<project-root>" --window N || python "${CLAUDE_PLUGIN_ROOT}/hooks/metrics.py" --root "<project-root>" --window N
   ```
   Replace `N` with the integer the user supplied.

2. **Render the glance.** Parse the returned JSON dict. Present exactly three lines,
   one per metric, in this order:

   ```
   override rate:          <current>  <arrow>  (prior: <prior>)
   small-lane rate:        <current>  <arrow>  (prior: <prior>)
   sprint low-conf ratio:  <current>  <arrow>  (prior: <prior>)
   ```

   - Use the real glyphs ↑, ↓, → in your message (not the JSON-escaped forms).
   - For `sprint_low_conf_ratio`, the `current` or `prior` value may be the string
     `"n/a"` — render it literally (e.g. `n/a ↑`).
   - ↑ on `override_rate` and `sprint_low_conf_ratio` is a worsening signal; state
     this briefly below the table so the reader does not have to guess.

3. **State the window.** Append one line naming the window size used, e.g.
   `Window: 20 commits (default)` or `Window: N commits (--window N)`.

## Hard gate

- Read-only. MUST NOT write, create, or modify any file. MUST NOT stage or commit.
  `git status` MUST be unchanged after a run.
- Emits ONLY the fixed 3-metric glance: `override_rate`, `small_lane_rate`,
  `sprint_low_conf_ratio`. MUST NOT emit verbatim override log lines, verbatim
  triage entries, commit lists, or any other content from the governance logs.
- MUST NOT require `$ca-init` to have been run. The helper degrades gracefully on
  absent logs (counts return 0 / ratio returns `"n/a"`); surface the degraded
  values as-is rather than blocking.
- If the helper subprocess fails entirely (import error, Python not found), report
  the error and stop — do not fabricate metric values.

## When NOT to use

- Full governance packet with verbatim overrides and audit trail → `$ca-audit`.
- Live project state (active sprint, open confirms, hook health) → `$ca-status`.
