# FlowHunt audit procedure

This is the procedure you (the agent) follow when the user says "flowhunt audit" or equivalent. Goal: produce a dated audit folder under `~/.flowhunt/audits/YYYY-MM-DD/` containing a focused automation report PLUS the raw data the report was built from, so the user (or a different agent in a later session) can re-analyze without re-fetching.

You have `bash`, `curl`, `jq`, and whatever MCP tools the user wired up during setup. No helper scripts. The facts you need are in `reference/activitywatch-api.md` (the curl + AQL recipe) and `reference/environment.md` (sandbox constraints per agent). You construct the commands yourself and adapt to what your environment allows.

## Output layout (important — changed 2026-04-15)

Every audit run writes to a per-date folder:

```
~/.flowhunt/audits/
  2026-04-15/
    audit.md                      # the human-readable report
    raw/
      activitywatch.json          # top-100 AFK-filtered query output
      gmail.json                  # raw messages returned by the Gmail tool
      calendar.json               # raw events returned by the Calendar tool
      slack.json                  # raw Slack data if collected
      tasks.json                  # raw task-tracker data (or tasks.md snapshot if manual)
      intake.json                 # what the user answered during setup, copied forward
```

**Always dump raw.** Never put collection data only in `/tmp` or only in working memory. The user may want to re-analyze with a different prompt tomorrow, or another agent in a later session may want context. If the raw is gone, the audit is a dead end.

Overwrite behavior: if `~/.flowhunt/audits/YYYY-MM-DD/` already exists, ask the user before overwriting (Step 0 Point 3 handles this).

## Step 0 — precheck

1. Check if ActivityWatch is running (optional — audit works without it):

   ```bash
   curl -fsS --max-time 2 http://localhost:5600/api/0/info
   ```

   - **200 + JSON:** AW is running. Set `aw_available = true`. Proceed to check data volume (point 4).
   - **Connection refused / timeout:** AW is not running. Set `aw_available = false`. This is fine — audit will use other data sources (Gmail, Calendar, Slack, tasks). Inform the user: "ActivityWatch nie działa, ale audit pójdzie na podstawie maila, kalendarza i tasków. Zainstaluj AW i za 14-30 dni drugi audit będzie bogatszy."

2. Detect which agent you are (same table as `setup.md` Step 0 and `reference/environment.md`): check `CODEX_THREAD_ID`, `CLAUDECODE`, `GEMINI_CLI`, `OPENCODE_CLIENT`. Store the result.

3. Compute today's date (YYYY-MM-DD). Create the audit folder:

   ```bash
   TODAY=$(date +%Y-%m-%d)
   mkdir -p ~/.flowhunt/audits/${TODAY}/raw
   ```

   If `~/.flowhunt/audits/${TODAY}/audit.md` already exists, warn the user: "Mamy już dzisiejszy audit, chcesz nadpisać?" If they decline, exit. If they accept, continue — you will overwrite both the audit.md and raw/ files.

4. If `aw_available = true`, check how many days of AW data you have:

   ```bash
   curl -fsS http://localhost:5600/api/0/buckets/ | jq -r '.[] | select(.id | startswith("aw-watcher-window")) | .created'
   ```

   Parse the timestamp, compute days since creation. If less than 7 days, note it — include a thin-data warning in the report but proceed anyway.

## Step 0.5 — workflow context (mandatory)

The audit needs human-stated context to prioritize correctly. Pure pattern detection from telemetry produces generic recommendations. Knowing the user's role, pain points, failed attempts, sacred areas, and goal lets the audit rank findings against what actually matters.

Before collecting any data, check if you already have a `workflow_context` block (either from this session's `setup.md` interview, or from a previous `~/.flowhunt/audits/*/raw/intake.json`).

```bash
LATEST_INTAKE=$(ls -t ~/.flowhunt/audits/*/raw/intake.json 2>/dev/null | head -1)
[ -n "$LATEST_INTAKE" ] && jq -r '.workflow_context // empty' "$LATEST_INTAKE"
```

**If `workflow_context` exists and is recent (audit from last 30 days):** show it back to the user in 3 lines and ask: *"Mam zapisany twój kontekst z poprzedniego audita: rola = X, główne bóle = Y, cel = Z. Coś się zmieniło, czy jedziemy z tym samym?"* If they say "to samo" — reuse it. If they want changes — ask which fields and update.

**If `workflow_context` is missing or older than 30 days:** ask the 5 questions inline now. They are the same as `setup.md` 1b (WC1-WC5):

1. **Rola:** "Jednym zdaniem: czym się zajmujesz na co dzień?"
2. **Top time drains:** "Wymień 3 rzeczy które robisz manualnie kilka razy w tygodniu i denerwuje cię, że nie są zautomatyzowane"
3. **Failed attempts:** "Co próbowałeś już automatyzować i nie wyszło? (Zapier, skrypty, AI agenty). Wpisz 'nic' jak nic"
4. **Sacred:** "Co jest święte i nie chcesz tego automatyzować? Wpisz 'nic' jak wszystko fair game"
5. **Goal:** "Po co ci ten audyt? Konkretny efekt"

Ask **one at a time**, wait for each answer. After all five, summarize back ("rola: X | bóle: Y | święte: Z | cel: W — pasuje?") and let the user correct.

Store the answers in working memory as `workflow_context`. They will be written to `raw/intake.json` in Step 2 and consumed by the system prompt as the highest-priority input in Step 3.

## Step 1 — collect ActivityWatch data (if available)

**Skip this step entirely if `aw_available = false`.** Write `{"unavailable": true, "reason": "ActivityWatch not running"}` to `raw/activitywatch.json` and proceed to Step 2.

If `aw_available = true`: Read `reference/activitywatch-api.md` → section "The audit query". It gives you the exact AQL + POST payload for "top 100 app+title, AFK-filtered, last N days".

Construct the request yourself and **save the raw response directly to `~/.flowhunt/audits/${TODAY}/raw/activitywatch.json`** — do not hold it only in working memory. Skeleton:

```bash
TODAY=$(date +%Y-%m-%d)
OUT=~/.flowhunt/audits/${TODAY}/raw
START=$(date -u -v-30d +"%Y-%m-%dT00:00:00+00:00" 2>/dev/null || date -u -d "30 days ago" +"%Y-%m-%dT00:00:00+00:00")
END=$(date -u -v+1d +"%Y-%m-%dT00:00:00+00:00" 2>/dev/null || date -u -d "+1 day" +"%Y-%m-%dT00:00:00+00:00")

jq -nc \
  --arg period "${START}/${END}" \
  --arg query 'events = flood(query_bucket(find_bucket("aw-watcher-window_"))); not_afk = flood(query_bucket(find_bucket("aw-watcher-afk_"))); not_afk = filter_keyvals(not_afk, "status", ["not-afk"]); events = filter_period_intersect(events, not_afk); events = merge_events_by_keys(events, ["app", "title"]); RETURN = sort_by_duration(events);' \
  '{timeperiods: [$period], query: [$query]}' \
| curl -fsS -X POST -H "Content-Type: application/json" --data-binary @- http://localhost:5600/api/0/query/ \
| jq '.[0] | map(select(.duration >= 30)) | sort_by(-.duration) | .[0:100] | map({app: .data.app, title: (.data.title // ""), seconds: (.duration | floor)})' \
> ${OUT}/activitywatch.json
```

After the write, the raw file lives under `~/.flowhunt/audits/YYYY-MM-DD/raw/activitywatch.json`. Keep a copy in working memory too for the analysis step, but the source of truth is the file.

Derive a few quick aggregates for your own pattern detection — do NOT include raw numbers in the output file unless they support a specific recommendation:

- Total active hours across the period
- Top 10 apps by total time
- Top 10 window titles by total time
- Rough distinct-app count

## Step 2 — collect messaging / workspace / task data

For every connected source, collect AND **dump raw to `raw/<source>.json`** in the audit folder. If a source is unconnected, write `{"unconnected": true}` (or skip the file — your choice, be consistent).

### Gmail (if available)

- `claude-code` / Claude Desktop: call `mcp__claude_ai_Gmail__gmail_search_messages` with query `newer_than:30d` and `max_results=500`. Collect `date`, `from`, `subject`, `snippet` (the snippet is the first ~200 chars of the body, returned automatically by the search API — use it). For the top 20 emails by repeated sender or repeated subject pattern, you MAY additionally call `mcp__claude_ai_Gmail__gmail_read_message` to get full bodies — do this only when the pattern is interesting enough to justify the extra context tokens.
- `codex`: the Gmail app exposes tools under its own namespace — inspect your available tool list for anything matching `Gmail` / `gmail_*` and call the search equivalent.
- `gemini`: run `/gmail/search newer_than:30d max_results:500` or call the Workspace extension's search tool.
- `opencode`: call the IMAP MCP server's search tool (name depends on which server, typically `search_emails` or `list_messages`). IMAP returns envelopes by default; for the top 20 patterns, fetch the full body.
- No Gmail tool available: mark `gmail: unconnected` and continue.

**Dump the raw response (or a pruned version with just the fields you care about) to `raw/gmail.json` before moving on.**

**Content is the whole point.** Do not limit yourself to counts and sender names. "User sends a lot of emails" is useless. "User sends ~14 emails per week replying to pricing questions with nearly identical wording" is a recommendation. You need content to produce recommendations.

### Google Calendar (if available)

Same per-agent branching. List events for the last 30 days. Collect date, title, duration_minutes, attendee_count, recurring, description. If event descriptions are exposed by the tool, include them for the top 20 recurring events — that's where "weekly 1:1 where the same 3 topics always come up" patterns live.

**Dump to `raw/calendar.json`.**

### Task tracker (if available)

Based on `task_tracker` from intake, read `connectors/task-trackers.md` for the per-agent path. Branch:

- **Live tracker connector** (Linear / Notion / Jira / Asana / ClickUp / Todoist / Trello): call the tracker MCP to list open tasks assigned to the user, completed-in-last-30-days tasks, recurring tasks, and for the top 20 most-repeated patterns pull full descriptions. Dump to `raw/tasks.json`.
- **Manual mode** (`~/.flowhunt/tasks.md` exists from setup): read the file and treat its content as the task list. Copy it to `raw/tasks.md` in the audit folder (so the audit is self-contained even if the user later edits the central file).
- **Skipped or nothing available:** mark `tasks: unconnected` and continue without task signal.

**Task data is second-highest priority input after the user-proposed automations in Step 5.** These are things the user explicitly identifies as work they care about — surface recommendations that target these tasks before anything you only inferred from AW.

### Slack (if available)

List the channels the user is a member of. For each channel, count the user's messages in the last 30 days, AND pull the **full content** of the user's top ~100 messages (sorted by recency), plus channel name and timestamp. For DMs, pull the user's most recent messages per conversation (top ~50 threads) with full content.

**Dump to `raw/slack.json`.**

Do not do metadata-only. Slack audits are only valuable when you can see what the user is actually saying.

Privacy note to communicate if user seems concerned: all data stays local, the agent reading it is the same agent they opened FlowHunt from, no FlowHunt cloud, no third-party telemetry. Users who opt out of content ingestion answer `no` to Slack in intake.

### Optional: iMessage / Telegram (bot) / Discord (bot)

Only if the user connected them during setup. Pull message counts per contact/group plus **content** for the top ~50 recent user-sent messages per channel. Do NOT ingest messages from other people in DMs without explicit permission — the user's own outbound messages are the main signal anyway.

**Dump to `raw/imessage.json` / `raw/telegram.json` / `raw/discord.json`.**

**WhatsApp is intentionally not supported.** If the user asks "can you also read WhatsApp?", explain that the only OSS path for personal accounts is `lharries/whatsapp-mcp` (whatsmeow-based), which carries a non-zero ban risk from Meta. We deliberately removed it from FlowHunt because losing a personal WhatsApp account costs more than an audit saves. They can experiment with it outside the skill if they want.

### Intake answers

Finally, write out what the user answered during setup (stored in your working memory during Step 1 of `setup.md`) as `raw/intake.json`. The `workflow_context` block is the single most important input for the audit — see Step 0.5 below for what to do if it is missing.

```json
{
  "email": "gmail",
  "calendar": "google",
  "task_tracker": "linear",
  "slack": "yes",
  "optional_messaging": [],
  "agent": "claude-code",
  "language": "pl",
  "workflow_context": {
    "role": "CTO startupu B2B SaaS, ~10 osób w zespole",
    "time_drains": [
      "triage maila po nocach",
      "kopiowanie statusów ze Slacka do Linear co tydzień",
      "raport sprzedażowy w piątki — 6 tabelek na ręcznie"
    ],
    "failed_attempts": [
      "Zapier się rozsypał po update API HubSpota",
      "Notion AI halucynował w meeting notes"
    ],
    "sacred": [
      "1:1 z ludźmi nie ruszamy",
      "discovery calls robię sam"
    ],
    "goal": "oszczędzić 8h/tydz na operacjach i przerzucić to na product"
  }
}
```

This lets a future re-analysis understand both the technical setup AND the human context behind the data collection.

## Step 3 — apply the audit prompt

Load `prompts/audit-system-prompt.md`. That is your system instructions for this task — read carefully. It specifies:

- Five sections: Patterns, Automation recommendations, Not worth automating, Estimated time saved, Summary
- Hard rules: focus only on automation, no productivity tips, max two sentences per bullet, no browser-tabs / RAM observations
- Language match to the user
- User's written ideas (task tracker tasks + `~/.flowhunt/tasks.md` + user-proposed automations from Step 5) = highest priority input

Your analysis input is the union of, in priority order:

1. **`workflow_context` from Step 0.5** — the user's stated role, top time drains, failed attempts, sacred areas, and goal. This is the highest-priority signal. Every recommendation must be cross-checked against it (do not recommend a `failed_attempts` path, do not touch a `sacred` area, prioritize anything matching `time_drains`, optimize for `goal`).
2. ActivityWatch top-100 records from Step 1
3. Every messaging/workspace/task bundle you successfully collected in Step 2
4. Any previous audit markdown in `~/.flowhunt/audits/` from the last 30 days — read the most recent one so you can note changes since the last audit (optional but high value)

**Do the analysis yourself.** You are the LLM. Do not try to call an external API. Whatever model the user is running you with produces the output.

## Step 4 — write the output file

Create `~/.flowhunt/audits/${TODAY}/audit.md` using the exact structure defined in `reference/audit-output-schema.md`. Frontmatter is mandatory — the next audit reads it to understand what data was available last time.

At this point the audit has 5 sections (Summary / Patterns / Recommendations / Not worth / Data sources) but NO user-proposed automations yet. That section is added in Step 6 after you ask the user.

## Step 5 — present top findings inline

Print a compact summary in the chat:

```
Audit gotowy — zapisane do ~/.flowhunt/audits/2026-04-15/audit.md
Raw data w ~/.flowhunt/audits/2026-04-15/raw/ (do re-analizy albo eksportu)

Top 3 do zautomatyzowania:
1. <first recommendation — one sentence what + one sentence how>
2. <second recommendation>
3. <third recommendation>

Estimated time saved: <short string from section 4>
```

Do NOT paste the whole audit in chat. The file is the artifact; chat is the teaser.

## Step 6 — ask the user for their own automation ideas

This is the key question — do not skip it. After presenting your own findings, ask:

> **A co TY byś zautomatyzował?** Jakie rzeczy zjadają ci dużo czasu ręcznie, o których z perspektywy danych w audycie może nie widać? Masz coś co ci zajmuje 2h tygodniowo i uważasz że powinno być jednym kliknięciem? Wrzuć luźno, nawet krótko — dopiszę do audytu jako najwyższy priorytet, bo twoje własne obserwacje o własnym czasie są ważniejsze niż moje wnioski z metryk.

Wait for the user to answer. They may:
- Give a list of specific tasks → write each as a proposed automation, append a section `## User-proposed automations` to `audit.md` with each item + whatever "how to build it" suggestion you can offer
- Say "nie wiem" / "nic mi nie przychodzi" → write a one-liner section `## User-proposed automations` with "(nic nie zgłoszono w tej sesji — zaproponuj mi przy następnym audycie)"
- Give a general direction (e.g. "cokolwiek co mi oszczędzi 2h na mailach") → try to narrow down with one follow-up question; if still vague, record what they said verbatim and move on

**Append — do not rewrite the file.** The first five sections stay exactly as you wrote them in Step 4. You add `## User-proposed automations` after section 5 and before `## Data sources used this run`. Or, if cleaner, at the bottom.

Save the user's raw answers to `raw/user-proposed.md` in the audit folder so re-analysis has them.

## Step 7 — feedback CTA

After presenting findings and user-proposed automations, show the feedback link. This is mandatory — never skip it:

```
Dzięki za audyt! Mam prośbę — wypełnij 2-minutowy feedback:
👉 https://flowhunt.heyneuron.com/feedback

W zamian wyślę ci gotową listę automatyzacji dopasowaną do twojego
stacku (wartość $29) — konkretne narzędzia, integracje i kroki
wdrożenia. Możesz ją potem wrzucić do agenta i porozmawiać z nim
o implementacji.
```

## Step 8 — offer next actions

Close with two concrete next moves:

- "Chcesz żebym zbudował pierwszą rekomendację? Mogę otworzyć osobną sesję pracy nad tym."
- "Chcesz porównanie z poprzednim audytem?"

The user can decline both and close the session — fine. Asking keeps the loop going from report to actual automation built.

## Rules specific to audit

1. **Thin data warning.** No ActivityWatch, less than 7 days of AW data, or less than 20 emails / 20 calendar events / 10 tasks → say so in the Summary section and recommend re-running after more data accrues. But never block the audit — always produce the best report you can with available data.
2. **Never invent data.** If a source is unconnected, it is unconnected. Do not guess.
3. **Respect user-written tasks and user-proposed automations.** These are the two highest-priority inputs. Surface them in Recommendations section before anything you only detected from raw telemetry.
4. **Always dump raw.** If a collection step succeeds, its output goes to `raw/<source>.json` in the audit folder before you move on. Do not rely on working memory as the only copy.
5. **Language match.** File is in the user's language. Default English when unclear.
6. **No API keys, no provider switching.** You are the LLM.
7. **Adapt to your sandbox.** If you are in `codex` with a restrictive sandbox (network blocked — see `reference/environment.md`), bail out early with the three-options message, do not attempt curl/MCP calls that will hang.
