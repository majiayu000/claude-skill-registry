---
name: fast-analysis
description: Analyze exported game files to assess gameplay, model decisions, and likely bugs without raw logs. Use for quick game triage.
---

# Fast Game Analysis

Quickly analyze a game using only the exported game file (`.json` or `.json.gz`). This covers ~85-90% of what the full analysis finds — game narrative, LLM decision quality, error patterns, bug identification — without needing the raw log directory.

## Workflow

### Step 1: Select the games

Determine which game(s) to analyze:

- If the user specified game ID(s), use those.
- If the user said "most recent" or similar, find the latest:

  ```bash
  uv run python scripts/list_recent_games.py
  ```

- If the user mentioned a config name (e.g. "round-robin-commander", "jumpstart-dumb", "modern-staller"), use the corresponding symlink:

  ```bash
  uv run python scripts/list_recent_games.py --config {config}
  ```

  where `{config}` might be `round-robin-commander`, `jumpstart-dumb`, `modern-staller`, etc. Check what symlinks exist with `--symlinks`.
- **If no game specified at all**, find the most recent unanalyzed games:

  ```bash
  make list-games-to-analyze
  ```

  This cross-references all game exports in `website/public/games/` (both `.json` and `.json.gz`) against existing analysis files in `doc/claudes/analyses/fast/` and prints the unanalyzed ones newest-first. Use `ARGS="--count N"` to change the number. Games are automatically skipped if 30+ fast-analysis runs have been done on newer games — at that point, any bugs from the old game have almost certainly already been identified. Use `ARGS="--max-staleness 0"` to disable this filter.

When analyzing multiple games, **parallelize aggressively**: run `game_overview.py`, `llm_events.py`, `game_narrative.py`, and `llm_reasoning.py` across 4+ games simultaneously rather than finishing one game before starting the next. Check errors/annotations arrays in bulk too. Write all analysis files at the end. Only drill into individual games (with `mcp_errors.py`, `extract_decisions.py`, etc.) when the initial parallel pass reveals something interesting.

### Step 2: Resolve the game file path

```bash
GAME_ID=game_YYYYMMDD_HHMMSS  # from step 1
GAME_PATH=website/public/games/${GAME_ID}.json  # or .json.gz
```

a. Check if `website/public/games/${GAME_ID}.json` or `.json.gz` exists on the current branch. (If using `find_unanalyzed.py`, it already outputs the full path — use that directly.)
b. If not, check if `~/.mage-bench/logs/${GAME_ID}/game_events.jsonl` exists. If so, generate the export:

   ```bash
   uv run python scripts/export_game.py ${GAME_ID}
   ```

c. If neither exists, tell the user and stop.

### Step 3: Use reusable analysis scripts

All analysis logic lives in `scripts/analysis/`. Standalone investigation tools live in `scripts/analysis/toolbox/`. Check what already exists before creating anything new — reuse or extend existing scripts. Run all scripts with `uv run python`.

If a script you need doesn't exist yet, **create it in `scripts/analysis/toolbox/`** and check it in. Do NOT write inline `python3 -c "..."` one-liners. These scripts accumulate over time into a reusable analysis toolkit.

Each script accepts a game file path (`.json` or `.json.gz`) as an argument:

```bash
uv run python scripts/analysis/toolbox/game_overview.py $GAME_PATH
uv run python scripts/analysis/toolbox/game_narrative.py $GAME_PATH
uv run python scripts/analysis/toolbox/llm_events.py $GAME_PATH
uv run python scripts/analysis/toolbox/llm_reasoning.py $GAME_PATH
```

The scripts should cover:

- **game_overview.py**: Game ID, format, turns, winner, player names/models/costs/placements/tool call counts/thinking time. Also shows critical errors from the `errors` array if present.
- **game_narrative.py**: Turn-boundary board states (life, hand size, battlefield) and key actions (plays, casts, attacks, blocks, damage, etc.). Include chat messages prefixed with `[CHAT]`.
- **llm_events.py**: Event type counts by player, failed tool calls (with args and error messages), stalls/resets/auto-pilot/llm_error counts, token/cost summaries, and game-level errors from the `errors` array.
- **llm_reasoning.py**: Sample 3-4 reasoning excerpts per player from `llm_response` events (checks both `reasoning` and `thinking` fields for extended-thinking models) to assess decision quality (mulligan, combat, spell targeting).

**Additional scripts** for targeted investigation when the core scripts reveal something interesting:

- **game_timeline.py**: Chronological event viewer with filtering by `--turns`, `--player`, `--mana`, and `-v` for verbose output. More powerful than `game_narrative.py` for drilling into specific turns or mana behavior. `--turns` accepts a single turn (`3`) or hyphen range (`3-5`); comma-separated lists like `9,10,11` raise `ValueError`. **Known issue**: `find_turn_at_ts` can assign events to the last turn, which breaks `--turns` filtering and can also mislabel the default unfiltered output with the final turn/phase. Use it only for rough chronology; if exact turn attribution matters, prefer `extract_decisions.py` or direct `jq` on the `decisions` array.
- **mcp_errors.py**: MCP tool error analysis — error frequencies by error_code, retry outcomes, per-model breakdowns, and "least helpful error messages" (where models retry with the same error). Run this when `llm_events.py` shows many failed tool calls.
- **mana_tapping.py**: Mana behavior analysis — mana_plan usage/success, auto-tap effectiveness, GAME_CHOOSE_ABILITY handling, spell cancellations. Run this when you see mana-related errors or spell cancellations.
- **extract_decisions.py**: Structured decision extraction — outputs each decision point with board state, available choices, what was chosen, reasoning, and what happened next. Useful for evaluating specific decisions in depth. Caveat: it has no real CLI parser; pass only the game path and do any filtering outside the script.

**Critical errors**: The `errors` array in the export surfaces critical issues from the game's error logs — loop detector interventions, uncaught exceptions, server short ID collisions, etc. These indicate genuine bugs rather than normal LLM mistakes. **Always check and explicitly call out any entries in the `errors` array** — they are high-signal indicators of platform bugs that need investigation.

**Smoking guns in reasoning and chat**: Pay close attention to what models complain about in their thinking traces and chat messages. When a model says things like "this doesn't make sense", "the tool returned wrong data", "I keep getting errors", or "why can't I cast this" — those are often smoking guns for platform bugs, not just model confusion. Cross-reference these complaints with the failed tool calls from `llm_events.py` to distinguish real bugs from model misunderstandings.

**Personality infection of reasoning**: Check whether the player's chat personality is bleeding into their internal reasoning/thinking traces, not just their chat messages. This is a known antipattern where dramatic or expressive personalities (e.g. dramatist, villain, valley-girl, philosopher) cause the model to spend reasoning tokens on in-character narrative instead of game analysis, leading to missed land drops, wrong plays, or refusal to interact with valid game prompts. Symptoms include: reasoning full of dramatic monologue instead of board state analysis; the model narrating what it *wants* to do in-character but then timing out or picking the wrong action; the model interpreting normal game prompts as adversarial because the personality frames things dramatically. If you see this, report it as a **personality-infection** issue — note the personality, the specific decisions affected, and contrast the in-character reasoning with what the model should have been thinking about. Analytical personalities (spike, analyst, detective) are generally clean; highly expressive ones are the risk.

**Decisions array**: The export may contain a `decisions` array with structured decision records — each one has the board state snapshot, available choices, what was chosen, `pilotContext` (untapped lands, playable cards, combat state), `subsequentActions` (what actually happened next), and `castRolledBack` (whether a spell was cancelled during mana payment). Use `extract_decisions.py` to view these in a readable format. This is the best data for evaluating decision quality — much more structured than reading raw reasoning.

**Existing annotations**: Check whether the export already has an `annotations` array (added by `annotate_game.py`). If blunder annotations already exist, you can reference them directly rather than re-evaluating decisions from scratch. **Check annotations early** — they're free structured data with severity levels (major/moderate/minor/questionable) and are more reliable than re-evaluating decisions yourself.

**Annotation caveat after retries**: If `llmEvents` show a failed `choose_action` followed by a successful retry on the same pending action, the exported `decisions`/`annotations` can sometimes stick to the failed attempt and drop the recovery into a blank follow-up decision. If an annotation claims a timeout, default choice, or other outcome that contradicts the later tool-call stream, trust `llmEvents`/tool results over the annotation and call out the mismatch explicitly.

**Annotation caveat with overlapping target prompts**: Even without retries, be careful when a turn contains multiple adjacent `Select a creature` / `Select target` prompts from different spells or abilities. The export/annotation pipeline can sometimes attach the target choice to the wrong card (for example, confusing a landfall trigger target with a later combat trick target). If an annotation says `Cast X targeting Y`, confirm the nearby `decisions[].actionResult.stack` / `subsequentActions` before trusting it.

**Models with no reasoning**: Some models (Gemini Flash Lite, some GPT variants) produce no reasoning/thinking traces. `llm_reasoning.py` will return "(no reasoning samples)" — this is expected, not a bug. Don't waste time investigating empty reasoning output; just note it in the analysis and move on.

### Known model error patterns (not platform bugs)

These are **recurring model behavior issues** seen across many games and models. Don't file issues for these — they're expected LLM limitations, not platform bugs. Note them in analysis files for tracking but don't investigate further unless the error rate is exceptional:

- **Thriving land color text**: Models pass `text="White"` or the full oracle text instead of `index=N` for Thriving land color choices. Recovery rate ~67%. Seen across G31FL, GPT5, Llama4, MstLg, MiniMx, MstMed.
- **GAME_CHOOSE_ABILITY forced choice**: Models send `choice="no"` or empty args `{}` trying to decline a forced ability choice that requires `index=N`. Especially common with single-option abilities. Weaker models (G31FL, GptOSS, MiniMx) get stuck; stronger models recover quickly.
- **Stale pN IDs**: All models send permanent IDs that are no longer valid (creature died, returned to hand, etc.). Some models (Grok, MstLg) are especially persistent, retrying the same stale ID 3-4 times.
- **"attackers" in wrong phase**: Models send `attackers=` parameter during GAME_SELECT (priority) phases instead of `choice=pN`. Universal across models.
- **"choice=all"**: Models try `choice="all"` or `attackers="all"` — neither is valid. Must list specific IDs or use the declared attack phase.
- **Hallucinated engine bugs**: GptOSS-120b specifically hallucinates that the game engine is broken ("tool is broken", "bug in simulation", "server glitch") rather than recognizing its own errors.
- **GptOSS echoing tool results as args**: GptOSS-120b sometimes sends the full JSON tool result object back as its next tool call args (e.g. `{"success": true, "action_taken": "selected_0", "game_seq": 460, ...}`). The model confuses tool outputs with tool inputs. This creates a cascade of failures since the bridge rejects the malformed args. Seen in game_20260304_191003_g1 (7+ occurrences in late game).

**When IS it a platform bug?** If the error message is actively misleading (telling the model to do something that doesn't work), if the game state is demonstrably wrong (life totals, card positions), or if the `errors` array has entries — those are platform bugs worth investigating.

### Step 4: Check existing issues and verify bugs still exist

**You are likely analyzing a game that was played days or weeks ago.** Bugs you find may have already been fixed in the interim. You MUST check before filing.

```bash
uv run python scripts/query_issues.py
```

For every potential bug you identify:

1. **Check if there's already an open issue** for the same bug (from the list above).
2. **Check if it was fixed since the game was played.** Compare the game date against recent commits:

   ```bash
   git log --oneline --since="YYYY-MM-DD" origin/master  # date of the game
   ```

   Look for commits that mention the same area (bridge, MCP tools, mana, combat, etc.). If a commit clearly fixes the bug, **skip it** — note in your analysis that the bug existed but has since been fixed, and move on.
   If an older analysis references an `issues/*.json5` file that no longer exists on the current branch, treat that as a strong hint that a fix commit deleted the issue file after landing the fix. Confirm with `git log --all -- issues/<filename>` or `git show <commit>`, then mention the fix instead of re-filing.
3. **If unsure whether a fix applies**, file the issue but note the possibly-relevant commit in the description so the next person can verify quickly.

Only file issues for bugs that appear to **still be present** on `origin/master`. The point of fast-analysis is to find bugs we haven't caught yet, not to re-document known/fixed ones.

For each **code bug** found (not model behavior issues), create an issue in `issues/`:

- Filename: `issues/p{priority}-short-kebab-summary.json5`
- Use `issues/blocked-short-kebab-summary.json5` only when Gregor explicitly says the issue has manual preconditions; those files should also include `"blocked": true`

```json5
{
  "title": "Short summary",
  "description": "Description with evidence from gz analysis.\n\nEvidence:\n- game {game_id}: [error pattern description]\n- llmEvents tool_call failures: [count and pattern]\n\nSuggested fix: ...",
  "status": "open",
  "priority": N,
  "type": "task",
  "labels": ["relevant-labels"],
  "created_at": "YYYY-MM-DDTHH:MM:SS.000000-08:00",
  "updated_at": "YYYY-MM-DDTHH:MM:SS.000000-08:00"
}
```

Priority: P1 = crashes/broken actions, P2 = loops/stalling/repeated errors, P3 = bad tool descriptions/missing features, P4 = minor/cosmetic.

Labels: `bridge`, `puppeteer`, `pilot`, `spectator`

### Step 5: Log the analysis

Create a file in `doc/claudes/analyses/fast/` for each game analyzed (see `doc/claudes/analyses/README.md` for the template). This marks the game as fast-analyzed so future runs skip it.

### Step 6: Present summary

Summarize findings: game outcome, key plays, LLM quality assessment, bugs found (with issue filenames), and any model-only issues noted.

### Step 7: Update this skill

If you discovered new recurring patterns, useful analysis techniques, broken scripts, or better workflows during this run, **update this file** before finishing. This skill improves over time as more games are analyzed. Examples of things to add:

- New model error patterns that are clearly not platform bugs (add to "Known model error patterns")
- Scripts that are broken or have known limitations (add caveats)
- Workflow improvements (e.g. better parallelization strategies)
- New analysis scripts you created in `scripts/analysis/toolbox/`

Do **not** add issue-specific bug notes to the skill if you already filed them in `issues/`. The skill should capture reusable workflow guidance, script/tool caveats, and stable recurring model-only patterns, not duplicate the issue tracker.

## What this skill does NOT do

- Read raw pilot logs, bridge logs, error logs, or server logs
- Trace bugs to specific source code lines
- Update `doc/investigating-game-logs.md`

For deeper analysis with source code tracing, use `/deep-analysis` instead.
