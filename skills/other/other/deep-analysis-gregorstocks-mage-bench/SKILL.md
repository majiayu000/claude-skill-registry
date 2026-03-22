---
name: deep-analysis
description: Investigate a game from raw logs, trace bugs to source code, and file detailed issues. Use for deeper debugging than export-only analysis.
---

# Deep Analysis

Deep analysis of game logs — reads all raw log files, traces bugs to source code, and files detailed issues. For quick triage, use `/fast-analysis` instead.

## Workflow

### Step 1: Select the game

Determine which game to analyze:

- If the user specified a game ID (e.g. `game_20260211_080409`), use that.
- If the user said "most recent" or similar, find the latest:

  ```bash
  uv run python scripts/list_recent_games.py
  ```

- If the user mentioned a config name (e.g. "round-robin-commander", "jumpstart-dumb", "modern-staller"), use the corresponding symlink:

  ```bash
  uv run python scripts/list_recent_games.py --config {config}
  ```

  where `{config}` might be `round-robin-commander`, `jumpstart-dumb`, `modern-staller`, etc. Check what symlinks exist with `--symlinks`.
- **If no game specified at all**, find the most recent unanalyzed game:

  ```bash
  uv run python scripts/analysis/find_unanalyzed.py --type deep --count 1
  ```

Set `GAME_DIR=~/.mage-bench/logs/{game_id}`.

If the full log directory doesn't exist but the game export exists in `website/public/games/` (`.json` or `.json.gz`), tell the user the full logs aren't available and offer to run a fast analysis from the export instead. Stop here unless the user wants the fast analysis.

### Step 2: Bootstrap from gz (if available)

If `website/public/games/${GAME_ID}.json` or `.json.gz` exists (either on the current branch or generatable from the logs), extract a quick overview before diving into raw logs:

```bash
uv run python scripts/game_gz_bootstrap.py ${GAME_ID}
```

This gives you a roadmap — you'll know which players had errors, roughly when, and what to look for in the raw logs.

Bootstrap caveat: `game_gz_bootstrap.py` currently overcounts failed tool calls because it substring-matches normal fields like `required`, and its auto-export fallback still checks `~/mage-bench-logs` instead of `~/.mage-bench/logs`. Treat its failure count as advisory and run `uv run python scripts/export_game.py ${GAME_ID}` manually if the export is missing.

**Check the `errors` array first**: The export may contain an `errors` field with critical issues surfaced from the per-player error logs (loop detection, uncaught exceptions, short ID collisions). These are high-signal bug indicators — always check and call them out before diving into raw logs.

**Check for existing annotations**: If the export has an `annotations` array, blunder analysis has already been run. Reference these annotations to guide your investigation — they identify specific decisions that were likely mistakes and explain why.

Retry caveat: if an annotation claims a timeout/default choice on `GAME_CHOOSE_CHOICE`, verify it against raw `*_llm.jsonl`. `scripts/export_game.py` can currently record the first failed `choose_action` attempt and drop the later successful retry into a blank follow-up decision, which makes the annotation look like a timeout when the model actually recovered.

Crash-accounting caveat: if a player's export summary says `toolCallsFailed=0` but the game clearly ended on a bad tool call, compare the tail of `*_llm.jsonl` and `*_pilot.log`. A final `llm_response` with no matching `tool_call` usually means the MCP request crashed before it could be logged. Those pilot-only crashes currently do not surface into export `errors` unless they also hit `*_errors.log`.

**Check the `decisions` array**: If the export has a `decisions` array, use `extract_decisions.py` to view structured decision records with board state, available choices, reasoning, and what happened next. Pass the export path, not just the game ID (for example: `uv run python scripts/analysis/extract_decisions.py website/public/games/${GAME_ID}.json`). This is often more useful than manually correlating events across log files.

### Step 3: Read game metadata

Read `config.json` and `game_meta.json` — understand who played, what models/decks were used, and the game outcome (winner, turn count, life totals).

### Step 4: Check existing issues

```bash
uv run python scripts/query_issues.py
```

### Step 5: Analyze log files in parallel

**Use parallel agents** to analyze different log types simultaneously.

**Pay particular attention to chat messages** — they're the most human-readable signal about what went wrong. XMage sends game-state information, error messages, and rule explanations through chat. Players also chat when confused or stuck. Always read chat messages early and use them to guide your investigation of other log files.

- **Chat messages**: Extract `player_chat` events from `game_events.jsonl` (`jq 'select(.type=="player_chat")' game_events.jsonl`). Look for XMage system messages about illegal actions, failed spell resolutions, mana payment problems, and rule enforcement. Look for player messages that reveal confusion or frustration. Chat messages often point directly at the root cause before you even open error logs.
- **Error logs**: Read `*_errors.log` files. Look for Java exceptions (NPE, IndexOutOfBounds, ClassCast), MCP tool failures, and stack traces. Note the exact filename and line numbers.
- **Pilot logs**: Read `*_pilot.log` files. Look for LLM decision failures, repeated tool call patterns (loops), models sending wrong parameters, empty responses, and context trimming warnings. **Pay close attention to what models complain about in their reasoning/thinking traces** — when a model says "this doesn't make sense", "the tool returned wrong data", or "why can't I cast this", those are often smoking guns for real platform bugs rather than model confusion. Also check for **personality infection**: if the reasoning/thinking is full of in-character narrative (dramatic monologues, villain speeches, valley-girl speak) instead of game analysis, the chat personality is bleeding into gameplay decisions. Note the personality and flag affected decisions.
  - If a model appears to hallucinate IDs or misunderstand a prompt, compare the exact rendered tool text in `*_llm_trace.jsonl` against the structured MCP/export payload. This catches renderer bugs where the raw JSON has the needed field (for example `incoming_attackers`) but the prompt text shown to the model omits it.
  - If `*_llm_trace.jsonl` tells the model `pass with answer=false`, localize that stale instruction to the pilot state-bridge text in `puppeteer/src/puppeteer/pilot.py`, not to the live bridge tool schema.
  - If a triggered ability prompt only shows `Stack: [Ability -> {'name': 'Player (you)', ...}]`, compare `*_llm.jsonl` / `*_llm_trace.jsonl` against exported snapshots. If the export has `source_card` / `ability_text`, localize the bug to bridge stack serialization plus `decision_renderer.py`, not the underlying game state.
  - If a pilot exits before any LLM activity with `Bridge MCP HTTP server did not start ... (rc=1)`, inspect the embedded log tail or matching `*_mcp.log` before blaming the model. A common pre-game failure is the Java bridge dying during startup (for example `BridgeClient.loadDeck()` rejecting a generated `.dck` file such as line 1 `NAME:...`), so the HTTP port never opens.
- **Bridge logs**: Read `*_bridge.jsonl` files. Look for repeated identical MCP calls (loop signatures), failed actions, "Index out of range" errors, and action sequences that suggest confusion (e.g., cast → cancel → cast → cancel).
  - If `GAME_CHOOSE_ABILITY` shows descriptions like `1. ...` but `respond_with` still says `choice=0, choice=1, etc.`, trace the mismatch through `AbilityPickerView` plus `BridgeCallbackHandler` before classifying it as model misuse.
  - If a pilot calls `pass_priority(until="stack_resolved")` and then stalls, compare `*_llm.jsonl`, `*_bridge.jsonl`, and `*_mcp.log`. A final `GAME_SELECT` followed only by `GAME_UPDATE` / `GAME_UPDATE_AND_INFORM` plus long `pendingAction=false` waits means the bridge only re-checks `stack_resolved` while an actionable callback is pending.
  - For stale-choice race monitoring, use the Grep tool for `choose_action out-of-range diagnostic` in the game directory's `*_mcp.log` files and classify each hit:
    - likely model misuse: `last_choices_response=boolean` with `index>=0`, or negative index
    - suspicious race: `last_choices_count >= 0` with tiny `last_choices_age_ms` and rapid action-type flips
  - Use the Grep tool (not bash `rg`) for searching log files:
    - `choose_action out-of-range diagnostic` in `$GAME_DIR` with glob `*_mcp.log`
    - `Index .* out of range` in `$GAME_DIR` with glob `*_errors.log` or `*_pilot.log`
  - For output schema validation errors (OpenAI structured outputs), grep for `Invalid structured content returned by tool` in `*_pilot.log`. These mean the bridge returned data that doesn't match the tool's output schema — the action succeeds server-side but the model gets an error. See `doc/investigating-game-logs.md` for details.
- **Game events**: Read `game_events.jsonl`. Look for stalls (long gaps between events), excessive auto-passes, turn timeouts, and game flow anomalies. For targeted investigation, use `scripts/analysis/toolbox/game_timeline.py` from the export — it supports `--turns`, `--player`, `--mana`, and `-v` flags to drill into specific turns or mana behavior. Caveat: some v7 exports omit `snapshots[].ts`, which currently makes `game_timeline.py --turns ...` misclassify every event as the final turn or print zero events. Fresh v8 exports without blunder annotations can also crash `game_timeline.py` with `missing annotations` because it currently uses the post-annotation loader. Sanity-check the output before relying on that filter; if it crashes, fall back to `game_events.jsonl` or `extract_decisions.py`.

### Step 6: Cross-reference findings

A single bug often shows up across multiple log files. For example, an NPE in error logs corresponds to a failed tool call in bridge logs and a confused retry loop in pilot logs. Group these into one issue, not three.

### Step 7: Distinguish code bugs from model issues

- **Code bugs** (file issues — the specimen appears to be broken): NPEs, wrong tool behavior, missing error handling, incorrect game state reporting — these need code fixes in Java or Python.
- **Model behavior** (note but don't file unless extreme): Passive play, bad threat assessment, suboptimal targeting — these are model quality issues. Only file if a model is completely non-functional (e.g., never plays spells, always passes).
- **Personality infection** (file as P3, label `pilot`): Check whether the player's chat personality is bleeding into their internal reasoning/thinking traces, causing worse gameplay decisions. This is a known antipattern where dramatic or expressive personalities (dramatist, villain, valley-girl, philosopher, etc.) cause the model to spend reasoning tokens on in-character narrative instead of board state analysis. Symptoms: reasoning full of dramatic monologue instead of game analysis; the model narrating intended plays in-character but timing out or picking wrong actions; the model interpreting normal game prompts as adversarial because the personality frames things dramatically (e.g. calling the game engine "broken" or "gaslighting"). If you see this, file an issue noting the personality, the specific decisions affected, and how the in-character reasoning led to the bad play. Analytical personalities (spike, analyst, detective) are generally clean.
- **Toolset mismatches** (file as P3): Look for tools that specific models are consistently hopeless with — always calling with wrong params, getting confused by responses, or wasting context on. Flag these as candidates for toolset changes in `presets.json` (each preset references a named toolset from `toolsets.json`). Note the model and the problematic tool so we can track patterns across games and decide whether to revoke that tool from weaker models' toolsets or design simpler alternative tools.
- **Already handled** (skip): Transient API errors with successful retries, empty responses caught by retry logic, one-off mistakes the model recovers from.

### Step 8: Trace bugs to source code

For each code bug, read the relevant Java/Python files to identify the exact line and root cause. Include in the issue:

- The game log path: `~/.mage-bench/logs/game_YYYYMMDD_HHMMSS/`
- Specific log files and approximate line numbers where the bug manifests
- The source code file and line where the fix should go (e.g., `BridgeCallbackHandler.java:1407`)
- A brief description of the root cause and suggested fix direction

### Step 9: Create issue files

Before filing a new issue, check whether the bug has already been fixed since the game was played. Compare the game date against recent commits:

```bash
git log --oneline --since="YYYY-MM-DD" origin/master  # date of the game
```

If a commit clearly fixes the bug, skip filing the issue. If unsure, file it and note the possibly-relevant commit in the description.

Create issue files in `issues/`:

- Filename: `issues/p{priority}-short-kebab-summary.json5`
- Use `issues/blocked-short-kebab-summary.json5` only when Gregor explicitly says the issue has manual preconditions; those files should also include `"blocked": true`

```json5
{
  "title": "Short summary",
  "description": "Full description with root cause analysis.\n\nEvidence:\n- ~/.mage-bench/logs/game_.../Player_errors.log: NPE at line 42\n- ~/.mage-bench/logs/game_.../Player_bridge.jsonl: repeated cast-cancel pattern\n\nSource: BridgeCallbackHandler.java:1407 — cv.getDisplayName() returns null\n\nSuggested fix: null-guard displayName before passing to StringBuilder",
  "status": "open",
  "priority": N,
  "type": "task",
  "labels": ["relevant-labels"],
  "created_at": "YYYY-MM-DDTHH:MM:SS.000000-08:00",
  "updated_at": "YYYY-MM-DDTHH:MM:SS.000000-08:00"
}
```

Priority guide:

- **P1**: Crashes or bugs that break core game actions (NPEs during targeting, spells fizzling due to code bugs)
- **P2**: Bugs causing major waste (infinite loops, stalling, repeated errors that block a player)
- **P3**: Suboptimal tool behavior or missing features (bad descriptions, missing info in prompts)
- **P4**: Minor issues (cosmetic, transient, or rare edge cases)

Labels: `bridge`, `puppeteer`, `pilot`, `spectator`

### Step 10: Focus on a single game

Only analyze the game selected in step 1. Do not look at older games — each analysis run should be scoped to one game to keep context focused and output actionable.

### Step 11: Present summary

Present a summary of all issues created, grouped by priority. For model-only issues, mention them in the summary but note they don't need code fixes.

### Step 12: Create reusable analysis scripts

If you need to write any non-trivial log analysis logic (more than a simple jq one-liner), create a Python script in `scripts/analysis/toolbox/` rather than writing throwaway one-off code. Run these scripts with `uv run python scripts/analysis/toolbox/your_script.py`. These scripts accumulate over time into a reusable analysis toolkit. Check what already exists in `scripts/analysis/toolbox/` before creating something new — you may be able to reuse or extend an existing script. Key scripts already available: `game_timeline.py`, `mcp_errors.py`, `mana_tapping.py`, `extract_decisions.py` (note: `extract_decisions.py` is in `scripts/analysis/`, not `toolbox/`).

### Step 13: Document investigation tricks

If you discovered any useful jq queries, grep patterns, cross-referencing techniques, or other tricks for investigating game logs during this analysis, append them to `doc/investigating-game-logs.md`. Don't duplicate what's already there — read the file first.

### Step 14: Log the analysis

Create a file in `doc/claudes/analyses/deep/` for the game analyzed (see `doc/claudes/analyses/README.md` for the template). This marks the game as deep-analyzed so future runs skip it.

### Step 15: Update this skill

If you discovered new recurring patterns, useful analysis techniques, broken scripts, or better workflows during this run, **update this file** before finishing. This skill improves over time as more games are analyzed. Examples of things to add:

- New bug classes or error patterns to search for (add to Step 5 log analysis guidance)
- New model error patterns that are clearly not platform bugs
- Scripts that are broken or have known limitations
- Workflow improvements (e.g. better parallelization, useful cross-referencing techniques)
- New analysis scripts you created in `scripts/analysis/toolbox/`

Do **not** add issue-specific bug notes to the skill if you already filed them in `issues/`. The skill should capture reusable investigation technique, tooling caveats, and durable workflow guidance, not duplicate the issue tracker.
