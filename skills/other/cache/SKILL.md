---
name: cache
description: Use this skill when the user asks to "enable cache protection", "block on cache miss", "avoid cache expiration cost", "/ar:cache", "protect against compaction", "cache pressure guard", "cache hit ratio threshold", or "set cache-miss threshold". Covers the /ar:cache slash command family for blocking tool use when the Claude Code prompt cache is cold or context is near compaction.
---

# /ar:cache — Cache Miss / Compaction Protection Skill

A PreToolUse gate that blocks commands when the prompt cache is effectively
cold — saving tokens by preventing full-rate re-reads of context that has
just fallen out of the 5-minute prompt-cache TTL. **Off by default.**

## When to use this skill

Invoke when the user asks about any of:

- setting a cache-miss / cache-hit-ratio threshold
- protecting against compaction-triggered context loss
- `/ar:cache`, `/ar:cache on`, `/ar:cache ok 5m`, `/ar:cache set …`
- "how do I stop Claude from burning tokens after idle time"
- "what is the cache gate", "cache protection"

## 1. Philosophy

- **Off by default.** No block fires unless the user runs `/ar:cache on`.
- **Fail-open.** If usage data is unavailable (old Claude Code version, Gemini
  CLI without cache-token fields, malformed JSONL), the gate allows.
- **Reuse, don't reinvent.** The gate uses the same `ScopedAllow` grants,
  `parse_scope_args` grammar, `session_state` filelock backend, and
  `check_blocked_commands` block UX that `/ar:ok` / `/ar:no` already use.
- **Stay out of the statusline.** The gate does **not** install or modify the
  user's `statusLine` setting. An optional one-line tap exists for users who
  want to feed their statusline's rich JSON into the gate themselves.

## 2. Commands

```
/ar:cache                       # show status
/ar:cache on [5m|1h|perm]       # enable
/ar:cache off [5m|1h|perm]      # disable (temporarily or until re-enabled)

/ar:cache set ratio 0.3         # block when cache hit ratio < 30%
/ar:cache set read 50k          # block when cache_read_tokens < 50,000
/ar:cache set age 10m           # block when last cache hit older than 10 min
/ar:cache set full 0.9          # block when total_input / window > 90%

/ar:cache ok 5m                 # override for 5 minutes
/ar:cache ok 3                  # override next 3 tool uses
/ar:cache ok perm               # override until axis clears / session end
/ar:cache no                    # clear outstanding overrides
```

Units: tokens accept `50000`, `50,000`, `50_000`, `50k`, `.5M`, `1.5M`.
Percent: `85%` or bare decimal `0.85`. Durations: `5m`, `1h`, `2h30m`, `perm`.

## 3. Grammar decision: `/ar:cache ok` not `/ar:ok cache`

The two grammars are semantically distinct. `/ar:ok <pattern>` allows a
command-string pattern; `/ar:cache ok <scope>` overrides the feature gate.
Overloading `/ar:ok cache` would silently collide with any user command named
`cache`. Decision in plan §6.5.1 is: no `/ar:ok cache` alias in v1. A sigil-based
alias (e.g. `/ar:ok @cache`) is backwards-compatible to add later if users ask.

## 4. How the decision flows (PreToolUse)

```
 tool use
     │
     ▼
 FeatureToggle("cache").is_enabled()  ──► false → ALLOW (default)
     │ true
     ▼
 CacheGuard._read_usage:
   1) cache/last_usage memo (2 s TTL) — reuse on burst calls
   2) cache/statusline_snapshot       — opt-in fast path
   3) JSONL tail (64 KB reverse scan) — find last assistant message.usage
     │   none available → ALLOW (fail-open)
     ▼
 CacheThreshold axes:
   - cache_hit_ratio_min     (cache_read / (input + cache_read + cache_creation))
   - cache_read_tokens_min   (raw cache_read_input_tokens floor)
   - cache_age_max_seconds   (age of last assistant timestamp)
   - compaction_used_max     (total_input / context_window)
   - rate_limit_5h_max       (from statusline snapshot; rate-limit wording)
   - rate_limit_7d_max       (from statusline snapshot; rate-limit wording)
     │ none tripped → ALLOW
     ▼
 ScopedAllow override active? (/ar:cache ok …)
   yes → consume + ALLOW
   no  → BLOCK with copy-paste override hints
```

## 5. Cross-CLI matrix

| Capability                          | Claude Code       | Gemini CLI           |
|-------------------------------------|-------------------|----------------------|
| hook stdin `transcript_path`        | yes               | yes                  |
| `message.usage.cache_read_*` in JSONL | yes             | unknown schema; probe |
| Compaction event name               | `PreCompact` / `PostCompact` / `SessionStart(compact)` | `PreCompress` (advisory) / `SessionStart` |
| `cache_hit_ratio_min` axis          | active            | fail-open (no data)  |
| `cache_read_tokens_min` axis        | active            | fail-open            |
| `cache_age_max_seconds` axis        | active            | active               |
| `compaction_used_max` axis          | active (with snapshot) | active when total tokens available |
| `rate_limit_*_max` axes             | only with statusline tap | unavailable  |

`/ar:cache status` prints which axes are inactive for the current CLI.

## 6. Multiprocess safety

The gate uses `session_state()` — a single shared JSON file with prefixed
keys and filelock + atomic tempfile rename. All writes are serialised; reads
re-load inside the lock. Parallel hook invocations (e.g. rtk-spawned) inherit
the same `_PARALLEL_GRACE_SECONDS = 1.0` s window that `ScopedAllow` already
uses. No new state file, no new lock.

## 7. Files

| Path                                                     | Role                                  |
|----------------------------------------------------------|---------------------------------------|
| `plugins/autorun/src/autorun/cache_guard.py`             | Single-file feature (~500 LOC).       |
| `plugins/autorun/tests/test_cache_guard.py`              | Full test matrix (parser → multiprocess). |
| `plugins/autorun/commands/cache.md`                      | `/ar:cache` command definition.       |
| `plugins/autorun/skills/cache/SKILL.md`                  | This file.                            |

## 8. Troubleshooting

- **"Gate doesn't fire."** Run `/ar:cache status` — is it enabled? Are any axes
  configured? Set at least one axis (`/ar:cache set ratio 0.5`) after enabling.
- **"Blocked when I didn't want it."** `/ar:cache ok 5m` or `/ar:cache off`.
- **"Gemini says axes unavailable."** Correct — Gemini CLI hooks do not surface
  cache-token fields. Use `age` axis instead; it works on both CLIs.
- **"I want the rich statusline numbers."** Add one line to your *own*
  statusline script: `printf '%s' "$INPUT" | autorun --cache-snapshot >/dev/null 2>&1 &`.

## 9. Plan reference

Full design: `~/.claude/plans/make-a-plan-to-sunny-sparkle.md`. Key sections:
§6.1 (reused magic classes), §6.5 (usage detection), §6.5.1 (grammar decision),
§6.7 (block message), §6.8 (multiprocess), §7 (ASCII diagrams).
