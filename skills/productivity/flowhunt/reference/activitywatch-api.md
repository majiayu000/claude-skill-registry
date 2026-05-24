# ActivityWatch API cheat sheet

You (the agent) interact with ActivityWatch directly via its local HTTP API. Do not expect a helper script — write the curl / jq yourself using this reference. This gives you the freedom to adapt to whatever sandbox your environment imposes (Codex seatbelt refuses some syscalls, OpenCode may restrict ports, etc.) without fighting shell wrappers.

Base URL: `http://localhost:5600/api/0` (always localhost, always port 5600, no auth)

## Health check

```bash
curl -fsS --max-time 2 http://localhost:5600/api/0/info
```

**Expected response (AW running):**
```json
{
  "hostname": "MacBook-Pro-3",
  "version": "v0.13.2",
  "testing": false,
  "device_id": "..."
}
```

**Interpretation:**
- HTTP 200 with JSON: AW server is up. Go to bucket check next.
- `Connection refused` / `Couldn't connect`: AW server is not running. Ask the user to launch it (see `../setup.md` Step 2 for the per-environment launch branch).
- `command not found: curl`: system is missing curl. Rare — ask the user to install it.
- Anything else: treat as "not running" and fall through to launch flow.

## Bucket check (server up, but is the window watcher registered?)

```bash
curl -fsS http://localhost:5600/api/0/buckets/ | jq -r 'keys[]'
```

You want to see at least one bucket name starting with `aw-watcher-window_`. If you only see the server but no window watcher, the tray app started but the watcher processes crashed or never launched. Tell the user to click the ActivityWatch tray icon → Open Dashboard, which kicks the watchers back on. Wait 10s and re-check.

For full health, also expect `aw-watcher-afk_<hostname>` (AFK detection, required for the audit query below) and ideally `aw-watcher-web-<browser>` (browser extension — critical for URL/page title capture; see `../connectors/activitywatch.md`).

## The audit query (top 100 app+title, AFK-filtered, last N days)

The canonical AQL query ported from the original Next.js FlowHunt app's `activitywatch.ts`. It:
1. Loads window events (app + title) for the period
2. Loads AFK events and filters to "not-afk" only
3. Intersects window events with not-afk periods (drops time while user was away)
4. Merges events by (app, title) to collapse noise
5. Sorts descending by duration

**AQL (one string, statements separated by `;`):**

```
events = flood(query_bucket(find_bucket("aw-watcher-window_")));
not_afk = flood(query_bucket(find_bucket("aw-watcher-afk_")));
not_afk = filter_keyvals(not_afk, "status", ["not-afk"]);
events = filter_period_intersect(events, not_afk);
events = merge_events_by_keys(events, ["app", "title"]);
RETURN = sort_by_duration(events);
```

Note: `find_bucket("aw-watcher-window_")` resolves the hostname suffix automatically — do not hardcode the hostname.

**Time period format:** `<start>/<end>` where start/end are ISO8601 UTC with offset, typically midnight UTC. Example: `2026-03-16T00:00:00+00:00/2026-04-15T00:00:00+00:00` for a 30-day window ending today.

**POST request:**

```bash
START=$(date -u -v-30d +"%Y-%m-%dT00:00:00+00:00" 2>/dev/null || date -u -d "30 days ago" +"%Y-%m-%dT00:00:00+00:00")
END=$(date -u -v+1d +"%Y-%m-%dT00:00:00+00:00" 2>/dev/null || date -u -d "+1 day" +"%Y-%m-%dT00:00:00+00:00")

jq -nc \
  --arg period "${START}/${END}" \
  --arg query 'events = flood(query_bucket(find_bucket("aw-watcher-window_"))); not_afk = flood(query_bucket(find_bucket("aw-watcher-afk_"))); not_afk = filter_keyvals(not_afk, "status", ["not-afk"]); events = filter_period_intersect(events, not_afk); events = merge_events_by_keys(events, ["app", "title"]); RETURN = sort_by_duration(events);' \
  '{timeperiods: [$period], query: [$query]}' \
| curl -fsS -X POST -H "Content-Type: application/json" --data-binary @- http://localhost:5600/api/0/query/
```

**Response shape:** array with one element per timeperiod (we sent one, so one element). Each element is an array of event objects sorted by duration descending:

```json
[
  [
    {"timestamp": "2026-04-14T...", "duration": 2016.3, "data": {"app": "Warp", "title": "..."}},
    ...
  ]
]
```

**Post-processing recipe (top 100, drop sub-30s noise):**

```bash
jq '.[0]
  | map(select(.duration >= 30))
  | sort_by(-.duration)
  | .[0:100]
  | map({
      app: .data.app,
      title: (.data.title // ""),
      seconds: (.duration | floor)
    })'
```

Feed the resulting JSON (or the individual fields) into the audit prompt as "detailed app usage with window titles".

## Data volume check (how many days of data exist?)

```bash
curl -fsS http://localhost:5600/api/0/buckets/ | jq -r '.[] | select(.id | startswith("aw-watcher-window")) | .created'
```

Returns the ISO timestamp when the window watcher bucket was first created, which is effectively "how long AW has been running". Compare to today; if less than 7 days, warn the user that the audit will be thin.

## Nuances and gotchas

- **Localhost only, no auth.** Anyone on the local machine can read the data. For FlowHunt this is fine — we run as the user, and there's no "remote" use case.
- **Browser extension data appears in `aw-watcher-web-<browser>` buckets**, not in the window watcher. The window watcher only sees "Brave - some tab title"; the web watcher sees actual URLs. For richer audits, also query those buckets with a separate AQL call if you want URL-level grouping. For v1 FlowHunt, window-title aggregation is sufficient — the title usually contains enough to infer what the user was doing.
- **Timestamps are UTC** in the API. When displaying "hours per day" to the user, convert to their local timezone before formatting.
- **Short events (<30s)** are mostly noise: alt-tabbing, toolbars, briefly clicked menus. Filter them out.
- **The AFK watcher is strict by default** — 3 minutes of no keyboard/mouse marks you AFK. Meeting time (listening, not typing) gets filtered out. This is correct for FlowHunt because meetings are captured separately via the Calendar connector.
