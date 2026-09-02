---
name: csift
description: >-
  Read, search and analyze Claude Code session transcripts (the .jsonl under
  ~/.claude/projects). Use this INSTEAD of grep/ripgrep/cat/jq/python: the format has
  documented traps that return plausible wrong answers, no error (a user-role
  filter overcounts human turns 3x; a sixth of human turns hide inside tool_result
  payloads; an AUQ answer can read (notes only) with the words in annotations).
  Reach for it when you would hand-scan a session jsonl or shadow session facts in
  your own state file - and BEFORE asserting something does not exist / was never
  done, or re-deriving a harness mechanism from binaries: past sessions usually
  derived it already. Search any regex across ALL sessions with
  timestamps and lines; read records by line, turn or uuid; what a session is doing
  now; tools, tokens, models, files changed; extract pasted images to files; recover
  a file or plan even when deleted; restore the verbatim turns a compaction
  clipped. Read-only, sub-second, safe inside hooks. Pure regex, not
  semantic search.
---

# csift — ripgrep for Claude Code session transcripts

Surface: **v0.10.0** (must == `csift --version`). MECHANICAL GUARD: at first use after any compaction or context restore, run `csift --version` — if it differs from this Surface line, the copy you are reading is a stale in-context echo, and the installed SKILL.md is the one that matches the binary: Read it before anything else. Same diagnosis when an invocation you were CONFIDENT about errors (an older surface from prefill/summary/habit); never fall back to hand-parsing the jsonl.

Rust CLI over CC session `.jsonl` under `~/.claude/projects/<encoded-cwd>/`. Built for an LLM consumer: token-lean text, uniform JSON, pure regex (RE2-class, linear-time; no backrefs/lookaround — they fail to compile by design). Smart-case: a pattern is case-insensitive unless it carries an uppercase; `-i` forces insensitive. `csift <cmd> --help` is the authoritative flag manual. Flag order is genuinely free — before/after the subcommand, before/after positionals, all equivalent.

## Why not hand-roll this format

Every row below is measured, not hypothetical, and none of them threw an exception: a
hand-written pass returns a plausible number that is wrong in a direction you cannot see.

| what a hand-written pass does | what it actually returns | the csift move |
|---|---|---|
| filters `type:"user"` for human turns | **3.03x overcount** (3,607 vs 1,191 corpus-wide; 8.6x in the most multi-agent lane): peer-session inbox messages and harness notifications are `type:"user"` too | `-t user.message` |
| reads text blocks, skips `tool_result` | **16.5% of human turns extract as zero characters** (197 of 1,191); direction and approval turns ride inside tool_result payloads | `-t user.answer -t user.rejection` |
| one AskUserQuestion record, one answer | **121 records carry 166 question-answer pairs**; 30 of them (24.8%) carry more than one, hiding 45 interventions and shrinking every denominator 5.5% | `-t user.answer` renders the whole Q+options+answer unit |
| reads the AUQ answer field | it can read `(notes only)` / `(no option selected)` while the operator's actual words sit in `annotations[question].notes` | csift renders the notes as the answer |
| guesses AUQ field names | `chosenOption` / `answer` / `selected` **do not exist** (the real keys are `answers`, `questions`, `annotations`), so a regex fallback silently yields empty answers | never guess: `show --line N` renders it |
| flattens an AUQ turn to `Q: ... CHOSE: ...` | every option label and description is discarded. On 2026-08-28 that turned an eval corpus into a trivial cue: **74 of 137 rows wrong, 22% of the text gone, a 20-point improvement that did not exist**, verdict inverted on rebuild | `show --line N --format json` |
| concatenates the payload body as human text | **51 records** are harness rejection boilerplate (22 also carrying a harness memory note) counted as the operator's words | the label is the authorship boundary |
| parses one session file | **+82 human turns** live in that session's subagent transcripts, which a single-file parse never opens | spanning is the default; `--no-subagents` opts out |
| reads text only | **about 1 in 5 human turns carries a pasted image** (159 of 774 records, 528 image blocks) and a text reader drops it with no marker | `image --id <ID> --out DIR`, then read the file |
| greps the file after a compaction | the summary replaced the turns; the words are gone from the live transcript | `verbatim` reconstructs them |
| greps for a tool's output | large outputs are externalised to `tool-results/<id>.txt`, leaving a pointer the regex matches instead of the content | `search --resolve-persisted` |

`search "" TARGET --count-by label` prints the carrier distribution before you write a line
of parsing. The engineer in the 2026-08-28 incident put it best afterwards: *"it would also
have told me the carrier distribution before I wrote a single line of parsing. I never
asked."*

Hand-rolling a genuinely special case is fine, and csift is read-only so it will not stop
you. What this section exists to prevent is hand-rolling as the DEFAULT, where every trap
above fails quietly and the number you report is wrong in a direction you cannot see.

## Route by QUESTION — one question ⇒ one command

| you want to know… | run |
|---|---|
| where does text X appear (regex, full round-trips) | `search PATTERN [target…]` |
| read exact record(s) — by line, turn, or uuid | `show TARGET (--line SPEC \| --turn SPEC \| --uuid U)` |
| read a session's recent turns ("what's it doing now") | `show TARGET --turn -3..` |
| what record-types live here, and how many | `search "" TARGET --count-by label` |
| which tools ran, how often (per-record census) | `search "" TARGET --count-by tool` — or `stats` (per-CALL counts) |
| what did I almost send (esc-recalled drafts) | `search "" TARGET -t user.unsent` |
| what I typed into the queue while a turn ran (queued, recalled, absorbed) | `search "" TARGET -t user.queued` — label zone shows `[enqueue]`/`[popAll]`/`[remove · reason]` |
| how long each turn took; was background work still pending at turn end | `search "" TARGET -t harness.meta.turn-duration` (pendingBackgroundAgentCount / pendingWorkflowCount) |
| the recap I saw when I came back after being away | `search "" TARGET -t harness.meta.away-summary` |
| which Stop hooks ran at turn end, how long, did one block the turn | `search "" TARGET -t harness.meta.stop-hooks` |
| when a tracked file's version bumped (a silent settings.json rewrite) | `search "settings\.json@v" TARGET -t harness.meta.snapshot` |
| any pending / unanswered tool calls | `search "" T --count-by pairing` (the count) — or `agents` (per-lane detail: which tool, since when, escalation-blocked vs awaiting) |
| which model(s) produced the replies | `search "" TARGET --count-by model` |
| which CC version(s) a session ran under, where an upgrade landed | `search "" TARGET --count-by version` |
| what non-record lines fill the jsonl (attachments, snapshots) | `stats TARGET` — the `types` census |
| where did this conversation fork (rewind / retry / parallel) | `show TARGET --branch-points` |
| CC's own rewind checkpoints of a file (the file-history store) | `recover --file /abs/P --list-backups` |
| edits parked in a plan file the session does NOT own | `plan [target] --audit` |
| hits per turn (a histogram) | `search PATTERN TARGET --count-by turn` |
| tokens burned · tool totals · turn count · time span | `stats [target…]` |
| what files changed, when; mutation timeline | `files [target…] --by file` / `--by timeline` |
| the FULL text of matched records (no clipping) | `search PATTERN … --no-truncate` |
| any field csift does not render (usage, stop_reason, …) | `search PATTERN … --raw \| jq` / `show T --line N --raw` |
| which sessions matched → scope the NEXT command | `search P -l \| csift <cmd> --sessions-from -` |
| which session is this / who am I | `list` / `whoami` |
| was this question answered / mechanism derived before | `search PATTERN` unscoped — BEFORE asserting absence or re-deriving |
| rebuild a file (even deleted) from history | `recover TARGET --file P` |
| restore turns a compaction summary CLIPPED | `verbatim TARGET…` (only when a compaction ate them) |
| subagent tree: lifecycle · status · frozen lanes | `agents [target]` |
| the session's bound plan file | `plan [target]` |
| pasted images: list / extract to a file you can Read | `image [target] --out DIR` |
| has this session truly stopped? (LIVE verdict + evidence) | `status TARGET` |
| block until it stops / asks / reads a file (a monitor) | `wait TARGET --until COND --timeout S` (timeout REQUIRED; `--background-since now` to ignore what already dangles) |
| which background tasks are still dangling, how old, which never return by design | `status TARGET` — the `bg` rows; `--ignore-background RE` for the known services |

Two commands read transcript content — pick by intent: `show` fetches from the live transcript (this includes the tail-peek `show T --turn -3..`); `verbatim` reconstructs what a compaction summary already discarded (budget-bounded, crosses boundaries). Everything you want to READ is `show`; `verbatim` is only for compaction-clipped history — and it tells you (stderr note) when you use it on a session with no compaction.

## Wrong assumptions that cost real sessions

| you might assume | actually |
|---|---|
| empty pattern `""` matches nothing | it matches EVERYTHING — the base filter for `-t`/time/turn/census |
| what I typed but esc-recalled is gone | a sent-then-esc-recalled draft IS on disk — `-t user.unsent` finds it (7 in one real session, one a 2.48M-char paste). What is genuinely gone from user RECORDS: a QUEUED message edited before dispatch — but its bytes are on disk in a `queue-operation` line, searchable since v0.10.0 as `-t user.queued` (measured over 6 sessions: 19-28% of the human's enqueued texts never became a user record; an earlier 61% figure counted every queue operation, remove lines included, over 3 sessions) |
| every thinking block is the model's reasoning | since CC 2.1.170 the API can add a SECOND thinking block per message: a narration-tagged one-sentence SUMMARY (same wire shape; tag hidden in the signature). csift labels it `agent.thinking.narration`; `-t agent.thinking` selects both, pure reasoning is `-t agent.thinking -T agent.thinking.narration`. And NO thinking block is raw chain of thought — the API documents all thinking text as summarized |
| `-c` counts matching records/lines | it counts EXCHANGES (round-trips); per-record counts = `--count-by` |
| `-l` lists every matching transcript | it lists OWNING session uuids (re-feedable); per-transcript detail = JSON summary `transcript_ids` |
| `--sessions-from` scopes to exactly the listed ids | the ids then EXPAND to their subagents (span default) — add `--no-subagents` to pin |
| turn and line share a numbering | `turn` = 0-based logical (the `tN` search prints); `line` = 1-based physical jsonl (`Lnnnn`); read both from output, never compute |
| a line number works with any session id | line numbers are per-FILE: `show --line` must target the row's own `session_id` (a parent uuid + a subagent line silently fetches the wrong record); prefer running the row's `refetch` verbatim |
| `-t user -T user.message` is contradictory | it is set subtraction (→ `user.answer` + `user.rejection`); a selector typo is a parse error with suggestions, never a silent empty |
| an excerpt is a summary | it is a match-centered FRAGMENT (~400 chars); full text = `--no-truncate` (lifts the JSON `excerpt` too) or the hit's `refetch` |
| `--raw` and `--format json` combine | they exclude each other (`--raw` IS machine output: verbatim jsonl lines) |
| zero matches means your syntax failed | it is a DEFINITIVE absence (exit 0) and search says so on stderr — read the diagnosis; when a `-t` excluded the hits it NAMES the label they live under |
| a stopped teammate needs TaskStop / pkill | teammates are in-process: `SendMessage` by name with `{"type":"shutdown_request"}` — TaskStop rejects every teammate id form |
| `completed_utc` = "when it stopped" | non-null ONLY when `status:"completed"` — a frozen/running lane carries null; its tail instant is `last_activity_utc/_local` (every timestamped lane; == `pending_since_utc` when frozen) |
| the pairing census needs `-t agent.tool.use` | pairing rides the tool BLOCK through the communication views — a frozen `SendMessage` counts as `pending` with no `-t` at all |
| timestamps need timezone arithmetic | text timestamps are already LOCAL with the offset inline — `2026-07-11 15:33 AEST(UTC+10)`; UTC lives only in JSON `ts_utc` |
| a hook that needs a session fact needs its own state file | the transcript already records it - before persisting anything (last prompt time, ids, activity markers) ask: does the jsonl already have this? Query csift from the hook (read-only, sub-second, safe inside hooks); a shadow store duplicates ground truth and drifts |
| "previous prompt" from a UserPromptSubmit hook = the newest `-t user` hit | at that instant the CURRENT prompt's record may or may not be flushed yet (both observed live) - drop hits younger than now-3s (the measured main-lane flush window is ~1-3.4s) and take the newest survivor; the @trap MAIN-thread flush race, different consumer |
| `@trap` failing = you mistyped the marker | maybe, but from the MAIN thread a first use normally misses anyway: the main record is an async flush of the completed assistant message landing ~1-3.4s after dispatch, and csift finishes inside that window (a subagent flushes per block and resolves first try). A miss means EITHER wrong lane (`@main` is the direct answer) OR a non-literal marker; a FRESH marker just restarts the race |
| a same-script retry counts as a second attempt | it does not: both attempts run inside the SAME not-yet-landed window, whose width is invisible from inside the script. A retry must be a NEW, SEPARATE shell-tool invocation — but from the main thread the answer is `@main`, not a retry |
| a fresh nonce string is reliably absent from the corpus | not from YOUR OWN live session: using it as a search pattern writes it into your transcript the moment that tool call flushes — the next unscoped/`@main` search finds your own earlier invocation (a self-echo, label `agent.tool.use`). Absence checks: scope away from your own session, or only trust the FIRST use |
| piping text output through `head -N` is safe | excerpts keep a record's LITERAL newlines (a multiline Bash command renders as-is) — `head` can cut mid-record and hide overflow pointers; the line-safe form is `--format json` (one object per line) |
| `stats` and `--count-by tool` should agree | three count units, three commands: `-c` = EXCHANGES, `--count-by` = RECORDS, `stats` tools = CALLS. A call = tool_use record + tool_result carrier, so `--count-by tool` reads ≈2× the `stats` tally (an answered AskUserQuestion re-homes its carrier to `user.answer`, so AUQ stays ≈1×) — a unit difference, not a bug |
| image `#N` handles run densely 1..N | `#N` is inherited from CC's paste-time `[Image #N]` numbering — handles can start past #1 and carry HOLES (that number's image never landed in this transcript); a `--id` miss errors naming the handles that DO exist |
| `.hits[]` flattening loses the ids | not anymore: the id trio rides EVERY hit row too (matching the exchange row), so `jq '.hits[] \| {session_id, label}'` carries real ids bare; a hit's `refetch` stays the preferred single-record fetch |
| zero matches for a rollout/steering keyword proves the model never saw it | steering PROSE is often not persisted while its CONFIG attachment is (e.g. `auto_mode`/`auto_mode_exit` carrying `{bashFirst, steerOnly, bypass}`) — census the types first (`search "" T --count-by attachment`), then search the payload under `--attachments` |
| `ScheduleWakeup` calls live under `harness.schedule.*` | a tool CALL classifies by role — arming a wakeup is `agent.tool.use` like any other tool; `harness.schedule.wakeup` is only the FIRED tick (the harness-injected, marker-carrying wakeup prompt), and a custom-prompt tick lands as an isMeta record (excluded, like all isMeta) |
| `csift turns` reads a session's turns | `turns` was RENAMED `verbatim` in v0.4 (compaction reconstruction only); the old name never runs — it errors naming the successor. Plain turn READING is `show <target> --turn -3..` |
| csift only reads CC's exact compact serialization | candidate detection is serialization-TOLERANT (since v0.6.9): a reserialized `"role": "user"` line (json.dumps defaults, a jq round-trip) is a full citizen — same previews, counts, matches. The framing law still stands: one record per LINE (pretty-printed multi-line JSON breaks jsonl framing and counts as malformed) |
| the file-history store is a full edit history | it is a pruned, tool-layer checkpoint store: @vN counters reset per session dir and get reused (only the backup instant orders), and bash/manual edits never land there — `recover --list-backups` lists it with those bounds stated; absence proves nothing |
| csift can tell which rewind branch is live vs abandoned | not computable from the jsonl (parallel tool fan-out leaves the same shape) — `show --branch-points` reports the fork facts ranked by inter-child gap; you judge |
| search found fewer user turns than a raw grep | esc-edit DRAFTS: a superseded opener is collapsed from turn reconstruction (and DISCLOSED in the footer + `superseded_drafts`); fetch one with `show --line`. A raw grep also overcounts the other way (3.03x — see Why not hand-roll) |
| `files --by timeline` lists every mutation of a path | only TOOL-recorded ones plus the settings-family snapshot inference — CC's own settings writes (`/model`, `/config`, plugin toggles) leave no tool record; for other paths check `recover --coverage` (the snapshot comparison catches them) or `recover --file P --list-backups` |
| every top-level transcript is an independent session | a background-job FORK is a byte-copy of another session at a compaction point (uuids preserved, slug stripped): `list` detects it (first timestamped record = a compact_boundary) and names the origin (`clone_of`), but every spanning surface still DOUBLE-COUNTS the inherited records until you scope the clone away |
| `list skipped_lines: 0` = the file is clean | `list` reads only the head/tail lines it needs (the fast-overview contract), so its count covers the LINES READ — a mid-file tear is outside its windows BY DESIGN, and the text note says so. The whole-file corruption census is `stats` (full scan; search/files/recover agree with it). Each `agents` row's `skipped_lines` is the same window census (lifecycle reads the transcript's edges) |

## Five laws (all commands)

1. **Exit law**: an ADDRESS that misses = hard error, exit≠0 (`show --line 99`, `show --turn 99`, `--uuid`, a pinned `@id`, `--agent`, `recover --file`, `image --id`). A FILTER that matches nothing = honest empty, exit 0 (`search`, time windows, open/from-end ranges) — and a zero-match `search` self-diagnoses on stderr: definitive absence + active filters + (under `-t`/`-T`) the labels the pattern DOES occur under. Never re-derive syntax because a result came back empty. ONE exit-code exception, `wait`'s timeout = **124** (the GNU timeout convention): a monitor's timeout is a normal outcome a script must branch on; it never extends to any other command or outcome.
2. **One range grammar, two axes**: every range flag (`--line` / `--turn` / `--file-lines`) takes `N` · `A..B` · `N..` · `..N` · `-k` (k-th from the END; `-3..` = last 3) · `..` (all), inclusive. `A-B` hard-errors with the correct spelling; a statically reversed `9..3` errors at parse. Axes: `turn`/`tN` = 0-based logical turn; `line`/`Lnnnn` = 1-based physical jsonl line; `--file-lines` (recover) = the reconstructed FILE's lines. On `show`, an explicit `--turn N`/`A..B` is an address (law 1); open/from-end forms clamp. `--turn` (windowing) ∧ `--since/--until` intersect (AND) everywhere.
3. **Span law**: subagents included by default; `--no-subagents` restricts; both switches exist everywhere (contradictory pair = parse error). `verbatim` is the one opt-IN (`--subagents`; its budget multiplies per session) and the one command that REQUIRES a target. `agents` rejects both (it LISTS subagents).
4. **Caps law — no silent truncation**: every cap reports its drop and how to get more. Defaults: `list` 50 rows on an unscoped all-projects run; `show` 200 record units (the drop prints the exact continuation command); `search`/`stats` uncapped until `--max-count N`. `--max-count 0 = uncapped`, uniformly. Malformed lines are counted (`N malformed line(s) skipped`), never hidden — including obviously-corrupt lines the byte prefilters never parse (free-text garbage, crash-truncation: any non-blank line that isn't `{…}`-framed); the one undetectable residue is a `{…}`-framed line whose INTERIOR is invalid JSON on a non-candidate line (validating those would repeal the perf contract). SCOPE of the count: the full-scan commands (`search`/`stats`/`show`/`files`/`recover`/`verbatim`/`image`) census the whole file; the head/tail readers (`list` rows, `agents` rows) census the LINES THEY READ — booked exactly once (the two windows are disjoint), scope-qualified in the text note, and never a whole-file verdict (that is `stats`). A sidecar marker line the current schema cannot read (schema skew — e.g. a pre-release fossil) counts as malformed too; it never merges and never vanishes.
5. **Time law**: every TEXT timestamp is local — `YYYY-MM-DD HH:MM:SS[.mmm] <TZAB>(UTC±offset)`, e.g. `2026-07-11 15:33:37 AEST(UTC+10)`, `IST(UTC+05:30)`. The marker is a format, not a value: name + offset derive from the machine zone at that instant (DST-correct), so the only mental step is "shift by the given offset". No UTC copies in text. Machine time = JSON, always paired: `ts_utc`+`ts_local` for a record's own instant, `<name>_utc`+`<name>_local` for named instants (`first_*`, `trigger_*`, …). Raw bytes = `--raw`.

## Targeting (positional, every command; `whoami` optional)

`@<uuid>` one session · `@<uuid-prefix>` (4-11 hex, unique else error) · `@main` calling top-level (env) · `@trap:<marker>` calling SUBAGENT (§trap) · `@<agent-id>` a subagent + its subtree (ids from `agents`; bare hex ≥12 or teammate form `aVSRepro-68a2…` — a teammate name may itself carry dashes, `aP1-engine-9cf2…`) · `.`/real path/encoded dir (`-Users-…`; Windows `C--Users-…`; UNC via `@--server-…`) ⇒ project(s) · `*.jsonl` one transcript · 0 targets ⇒ ALL projects (`list` caps the unscoped flood; `verbatim` REQUIRES a target).
- A bare id without `@` errors with "did you mean '@…'?" — ids always take `@`.
- An unrecognized `@`-shape (a 1-3-char prefix, a dashed fragment, a non-id token) errors naming the grammar — it never falls through to path resolution.
- `--sessions-from <FILE|->` (every multi-target command): scope to an id list — whitespace-separated uuid/prefix/agent-id tokens, bare or `@`-prefixed (exactly what `search -l` emits); UNION with positionals, per-id fail-loud, an explicitly empty list = empty scope (exit 0 — a pipeline that found nothing propagates nothing).
- `search` is the one command whose FIRST positional is PATTERN; targets follow: `csift search P @<uuid>`. A pattern starting `@` errors (escape `\@`); a uuid-shaped pattern prints a stderr note.
- `show` targets exactly ONE transcript: `@<uuid>` = that top-level file (never spans), `@<agent-id>` = that subagent's file.

### @trap:<marker> — "which subagent am I?"
**Scope: this is the subagent-only tool.** A running subagent cannot read its own id from env; the top-level thread already has `@main` (env-based, no race, always correct) — reach for `@trap` only when you cannot name yourself. Invent a fresh marker, put it literally IN the csift command; csift finds the transcript whose shell tool_use carries it (Bash — or Windows' separate `PowerShell` tool, same `command` field). Grammar (enforced): exactly 3 CamelCase words + exactly 4 non-trivial trailing digits, hand-invented, context-independent — shaped like `@trap:JollyShinyBrook4283`, which is a RESERVED example csift hard-rejects (invent your own; never script-generate or reuse). TIMING: a subagent's transcript flushes per content block, so its launching command is on disk at dispatch and a **first try resolves** — that is the whole design. Diagnostic: from the MAIN thread a first use normally misses instead (the main record is an async flush of the completed message landing ~1-3.4s after dispatch, and csift beats it) — a miss therefore means EITHER you are the main thread (use `@main`) OR your marker was not literal; in neither branch is retrying `@trap` the answer. When @trap does resolve to the main transcript, csift says so on stderr. One-shot means one marker per identity question, not one per attempt (a fresh marker restarts the race). UNIQUENESS is conversation-wide: in a team/multi-subagent setting the marker must be unique across ALL concurrently-running agents, not just your own retries — a marker that lands in two transcripts (e.g. relayed to a peer in a message) errors AMBIGUOUS, fail-loud, never a silent wrong match. `whoami @trap:<marker>` returns the full upstream ancestry chain.

## Labels (`-t/--label` · `-T/--label-not`) — dotted `role.class.sub`, 3 roles, 33 leaves

Selector = dot-segment prefix, THREE forms (v0.9.4): a bare ROLE (`-t user`) = the role's **LLM-visible** leaves only — the conversation as the model receives/produces it; a GLOB (`-t 'user.*'`, quote it from the shell) = every leaf under the prefix, visibility ignored; an intermediate prefix (`-t agent.tool` = use+result, `-t harness.compaction` = summary+boundary) or a full leaf = its full set, a deliberate drill-down. No `-t` ⇒ all labels (drafts and boundaries stay searchable by default, with disclosure). `-T` EXCLUDES with the same grammar (effective set = includes minus excludes; a combination excluding everything it includes errors). Multi-label records emit once under the richest surviving view (an AUQ answer → `user.answer`; a SendMessage/spawn/`<result>` pulse → `agent.communication.*`; a slash-command-with-args → `user.message` rendered `/name args`). The complete rule is MECHANICAL, not a lookup table: JSON `labels[]` is always ordered richest-first, and the rendered view is simply the FIRST label in `labels[]` that survives your `-t`/`-T` — for any unlisted combination, read it off `labels[]`. Don't guess a record's leaf — run `--count-by label` to see the distribution.

```
user     .message   genuine human prose (incl. slash-command args, rendered `/name args`)
         .answer    AskUserQuestion answer (Q+options+answer unit)
         .rejection plan/tool reject + typed instruction
         .unsent    [not LLM-visible: outside `-t user`; reach via `-t user.unsent` or `-t 'user.*'`]
                    a SUPERSEDED draft: sent, esc-recalled, edited, re-sent — the original
                    stays on disk sharing the resend's parentUuid, OUTSIDE turn numbering,
                    never counted as user.message. LIMITS: a recalled-then-ABANDONED
                    message has no resend sibling and is undetectable; a QUEUED text
                    edited before dispatch never becomes a user record at all (its
                    queue-operation line is `.queued`, below)
         .queued    [not LLM-visible · GATED: parsed only under an explicit selector —
                    `-t user.queued` / `-t 'user.*'`; never by a bare scan, `-t user`,
                    or `--count-by label` without -t]
                    the human's text as it sat in the input QUEUE: a queue-operation
                    line with content — `[enqueue]` (typed while a turn ran), `[popAll]`
                    (recalled to the input box), `[remove · <reason>]` (consumed:
                    absorbed_mid_turn / delivered_to_agent). The label zone shows the
                    event. A queued <task-notification> / peer message is NOT the human
                    and carries no label; a content-less dequeue carries nothing. The
                    queue line has NO join key (measured: 4-6 keys, no promptId/uuid),
                    so `dispatched` is never asserted — a dispatched text simply also
                    exists as a later user.message; match by text if you must
agent    .message · .thinking (redacted → "[redacted thinking]") · .tool.use · .tool.result
         .thinking.narration   an API-issued one-sentence SUMMARY of the reasoning beside it
                               (tag hidden in the signature; renders "[narration summary]";
                               NOT the model's reasoning — pure reasoning = -t agent.thinking
                               -T agent.thinking.narration; excluded from verbatim replay)
         .communication.{inbox,sent,signal}   peer msgs — rendered `from ⇨ to` (self = owner)
harness  .notification.{workflow,monitor,subagent,background-command,task}  ← <task-notification>
                    (.subagent also carries the harness's agents-stopped notice
                    "N background agents were stopped by the user: …" — plain text,
                    no XML, not the human, never a turn opener, renders
                    "[subagent stopped] …"; .monitor = the Monitor tool's own
                    pulses and termination notices ONLY — since v0.10.0 a
                    `Background command "…"` pulse is always .background-command,
                    whatever its quoted name says)
         .compaction.{summary,boundary}   boundary renders its compactMetadata (trigger=…);
                    boundary is [not LLM-visible: outside `-t harness`; reach via
                    `-t harness.compaction` or the full leaf] — a metrics-only system record
         .command.{invocation,stdout} · .interrupt.{user,tool}
         .schedule.{wakeup,continuation} · .meta.{hook,loop,attachment}
         .meta.turn-duration   [not LLM-visible · GATED] the end-of-turn telemetry record:
                    `[turn duration: 1m 5s · durationMs=64911 messageCount=908
                    pendingBackgroundAgentCount=2]` — the structured body behind the
                    REPL's "Done in Ns" / "Waiting for N agents" lines (which never
                    land on disk). Present fields only; a turn that straddled a resume
                    gap reads as days, honestly. The pending counts cover background
                    agents and workflows ONLY: a turn that ended with a background SHELL
                    still running wrote no pending field at all (measured), so an EOT
                    record is never evidence that the session is done — that is
                    `csift status`
         .meta.away-summary    [not LLM-visible · GATED] the model-generated recap shown
                    when you return after 5+ minutes away (config-gated); verbatim text
         .meta.stop-hooks      [not LLM-visible · GATED] the Stop-hook execution ledger:
                    `[stop hooks: count=N errors=M prevented=false]` + one
                    `command (Nms)` line per hook — which hooks ran, how long, whether
                    one blocked the turn. NOT .meta.hook (that is text a hook INJECTED)
         .meta.snapshot        [not LLM-visible · GATED] a file-history snapshot
                    (`[file-history snapshot at <ts>: <path>@vN, …]`, every tracked
                    path) or delta (`[file-history delta at <ts>: <path>@vN
                    backup=<name>]`, one path's bump) — the v0.9.4 recover instrument,
                    searchable: "when did settings.json's version jump?"
```
LLM-VISIBILITY (v0.9.4, extended v0.10.0): SEVEN leaves are outside the bare-role selectors — `user.unsent` (a superseded draft is NOT in the surviving conversation: CC's own `preservedMessages` accounting excludes every draft uuid; say "not in the surviving conversation", never "the model never saw it" — a few drafts drew replies before the esc), `harness.compaction.boundary` (no message field at all), and the five v0.10.0 promoted leaves `user.queued` + `harness.meta.{turn-duration,away-summary,stop-hooks,snapshot}` — the same instrument: ZERO of the promoted line types carries a `message{}` field (every user/assistant record does), and CC's own source labels them REPL-render internals. Two instruments that do NOT decide visibility: parentUuid threading (a later user record names a turn_duration uuid as its parent — chain continuity, not delivery) and `preservedMessages` membership (a tail window listing these uuids at the same rate as messages). Everything else a role selector reaches is delivered-or-produced conversation. `-t user` therefore restores the 0.7-era contract ("what the human actually sent"): 0.9.2..0.9.3 briefly included drafts under it, which poisoned a real last-human-touch hook (a draft 12s before the real submit). `isMeta` is an AUTHORSHIP flag and `isVisibleInTranscriptOnly` a summary display flag — neither is a visibility instrument.
Gated meta leaves: `harness.meta.hook` needs `search --additional-context` (or the superset `--attachments`); `harness.meta.attachment` (any OTHER attachment payload — edited_text_file, compact_file_reference, file snapshots …) needs `--attachments` or `--count-by attachment` — a default scan never parses attachment lines; an explicit `show --line/--uuid` address renders any of them flag-free.
GATED PROMOTED LEAVES (v0.10.0): `user.queued` and `harness.meta.{turn-duration,away-summary,stop-hooks,snapshot}` need an EXPLICIT `-t` that reaches them — the full path, a glob (`-t 'user.*'`, `-t 'harness.*'`), or the `harness.meta` prefix. A bare scan, a bare role, a `-T`-only filter and `--count-by label` without `-t` never parse those lines (most queued content is a duplicate automation pulse; every promoted line is a non-message line), so the default surface stays the conversation and costs nothing extra. A zero-match run without such a selector says so on stderr (JSON summary `gated_leaves_unreached:true`) — that absence does not cover the gated lines. `show --line/--uuid` renders any of them flag-free; `--raw` still prints the bytes.
Glyphs: `◂` user · `▸` agent · `⚙` harness · `·` sibling · `▹` tool use↔result pair (unreturned → `(no result — pending)`; orphan → `(use not in scope)`) · `⇨` comm direction. Turn boundary = genuine user ∨ AUQ answer ∨ typed rejection ∨ inbound peer message; slash-command wrappers, interrupts, `<local-command-stdout>`, compaction summaries never open a turn.

---

## search — find round-trips

```
csift search PATTERN [target…] [-t SEL]… [-T SEL]… [-i] [--multiline] [--since W] [--until W]
  [--turn N|A..B|N..|-k] [--max-count ±N] [-c | -l | --count-by AXIS] [--raw] [--siblings]
  [--no-truncate] [--resolve-persisted] [--additional-context] [--attachments] [--sessions-from F] [--no-subagents] [--format json]
```
Empty `""` pattern = pure filter. A hit returns the complete round-trip (tool_use with its result; user turn with reply; an answered AUQ as one Q+A unit). Terminal modes (mutually exclusive): `-c` prints one integer (EXCHANGES, `--max-count` drops added back) · `-l` prints the distinct owning session uuids, one per line, uncapped — pipes into `--sessions-from -` · `--count-by AXIS` prints a census (below).
- `--count-by AXIS` — a per-key census of the matched RECORDS along ONE closed axis (not a query language; a record whose several sections match still counts once): `label` (per leaf; a record counts under every leaf it carries THAT SURVIVES your `-t`/`-T` — a dual-labeled record never leaks its filtered-out twin into the keys, so `-t user -T user.message --count-by label` shows user.* keys only; with no filter that is the full label set — run with `""` and no `-t` before guessing any `-t`) · `tool` (per tool name) · `turn` (ascending histogram) · `session` (per transcript) · `pairing` (paired | pending | orphan, joined by tool_use_id; rides the tool block through the communication views, so a frozen SendMessage is `pending` — "any pending tools?" needs no `-t`) · `model` (per assistant model — the raw `message.model` value; CC's `<synthetic>` placeholder, a fabricated stand-in assistant record such as an API-error notice, is reported verbatim) · `attachment` (per attachment payload type — IMPLIES the `--attachments` gate, so the census needs no separate flag) · `version` (per CC version stamp — where an upgrade landed mid-session) · `result` (per tool-result error state, `ok` | `error` — `pairing` answers "did a result come back", `result` answers "was it good": "any failed reads?" is `search "" T --count-by result`; an errored result also renders an inline `[error]` and carries JSON `is_error`). Records outside an axis's domain are excluded and the excluded count is reported.
- Excerpts are ~400-char match-centered fragments; when anything clipped, text prints a caution + JSON summary `excerpts_truncated:true`. Full text: `--no-truncate` (also un-clips JSON `excerpt`) or the hit's `refetch`.
- `--siblings` (zero-arg): also render the turn's other records — messages always, thinking≤2 · thinking.narration≤1 · tool.use≤3 · tool.result≤3 · harness≤2 per leaf — the caps apply to NON-matching context records only; your actual hits always render in full, so a block can legitimately show more than the cap count of same-leaf lines. Overflow prints `(+N more · csift show @<id> --line A..B)` — run it verbatim.
- `--raw`: the matched records' VERBATIM jsonl lines on the whole filter surface — stdout pure jsonl for `jq` (notes → stderr; sidecar-merged hits have no physical line and are omitted with a note). The answer to any unrendered-field question.
- `--resolve-persisted`: inline `tool-results/<id>.txt` files before matching (regex reaches externalized output); under `--raw` it affects matching only.
- `--additional-context`: ALSO scan hook-injected additionalContext (the `attachment` records a SessionStart/UserPromptSubmit/... hook writes — where `<stamp>`-style injected context lives). Off by default (machinery; echoes prompts/files wholesale). Hits surface under `harness.meta.hook`; the printed `csift show @<id> --line N` refetch renders one WITHOUT the flag (explicit address always works).
- `--attachments`: scan EVERY `type:"attachment"` record — a SUPERSET of `--additional-context` (hook payloads stay `harness.meta.hook`; every other payload surfaces under `harness.meta.attachment` with its VERBATIM payload JSON as the matchable text). Off by default: attachment lines are the bulk of many transcripts' bytes and embed whole files. An explicit `show` address renders any attachment record without the flag.
- `--multiline` sets `(?s)(?m)`. Caveat: EVERY tool_use's matchable text is its name + the RE-SERIALIZED JSON input (not only AskUserQuestion's), so a real newline inside e.g. a Bash `input.command` is already the two-character sequence `\n` by match time — match the literal `\\n`; `--multiline` is correctly irrelevant there. It helps only where rendered text keeps real newlines (message text, thinking, tool_result bodies).
- OUTPUT GEOMETRY (text): exchanges emit oldest-first (stable chronological across every transcript in scope; undated exchanges last). Each exchange header opens with a STABLE id-prefix token `<tok>·t<N>` — `<tok>` = the first 8 chars of the owning transcript id, directly usable as an `@` target, identical across invocations (a within-output collision lengthens the colliding group to 12 chars, then the full id; a teammate id renders whole); a subagent exchange carries `(parent <first-8-of-owning-uuid>)` on EVERY header. The head carries scope + match totals + direction (`matches  N exchanges · M sessions · oldest first[· showing earliest|latest K][· undated last]`); the tail repeats the totals and adds integrity notes + refetch guidance; each over-long fragment marks its own truncation inline (`(+N chars)`). To limit output, prefer `--max-count N` (earliest N) or `--max-count -N` (latest N) over piping into `head`/`tail` — a capped run keeps every note; a pipe amputates one end of the ledger.
- Regex patterns WITH metacharacters are prefiltered too (v0.9.4): a necessity-only literal extraction (every branch of an alternation must demand one safe needle) lets `search "TodoWrite.*legacy|legacy.*TodoWrite"` scan at near-literal speed — no flag, no semantic change, matches are byte-identical.
- `--max-count` is SIGNED: `N` keeps the EARLIEST N of the chronological stream, `-N` the LATEST N, `0` = uncapped; the kept exchanges still emit oldest-first among themselves. The footer names the dropped side (`N later|earlier dropped by --max-count`).
- Superseded drafts (esc-edit resends: an opener replaced by a later same-parent sibling) stay OUTSIDE turn numbering but are fully searchable under their own leaf: a matching draft emits as its own annotated `<tok>·draft` unit labeled `user.unsent` (JSON `superseded_draft:true`, null `turn_index`), the footer prints `(N superseded draft(s) outside turn numbering — … searchable as -t user.unsent …)`, the JSON summary carries `superseded_drafts`, and a `--turn` window suppresses draft units (they belong to no numbered turn). `show --line/--uuid` always fetches one.
- Zero matches: stderr prints "0 matches — a DEFINITIVE absence (exit 0), NOT an error" + active filters + the malformed-line count when >0 (the absence is definitive for parseable lines only) + (under `-t`/`-T`) `⚠ but "X" DOES occur — N record(s) under: <labels>`. JSON summary: `definitive_absence`/`active_filters`/`excluded_by_label`/`gated_leaves_unreached` (true when no selector reached a gated promoted leaf — those lines were never scanned; the stderr note says the same).

```bash
csift search "panic" @<uuid> -t agent --since 6h
csift search "" @<uuid> --count-by pairing                     # any pending tools?
csift search "todo" . -l | csift stats --sessions-from -       # aggregate matching sessions
csift search "" @<uuid> -t agent -T agent.thinking             # agent role minus thinking
csift search "X" --max-count 1                                 # when did X FIRST happen? (earliest exchange, local ts on the header)
csift search "X" --max-count -1                                # most recent occurrence of X
# find a phrase across ALL sessions, then read one hit in full:
#   copy <tok> and L<n> from the hit → csift show @<tok> --line <n>   (or --turn <N> for the whole turn)
```

## show — fetch records by line / turn / uuid (the reader; also the raw escape hatch)

```
csift show TARGET ( (--line N|A..B|N..|-k,…)… | --turn N|A..B|N..|-k | (--uuid U,…)… | --branch-points )
  [--raw] [--max-count N] [--format json]
```
- TARGET = exactly one transcript — `show` is the ONE targeting command with NO subagent-span pair (`--no-subagents`/`--subagents` are rejected with the rule, not a typo guess); to read a subagent, target its own `@<agent-id>`. One addressing mode is REQUIRED (no selector = a teaching error; csift never dumps a whole transcript by accident). `--turn N` fetches EVERY record of that turn — its whole back-and-forth — in the same numbering `search` prints (a `<tok>·t270` header ⇒ `--turn 270`, and the header's `<tok>` is the `@` target); `--turn -3..` is the tail-peek. A "turn" is everything since the last human-authored boundary — on a heavily-agentic session one turn can be DOZENS of records (a whole autonomous investigation); the 200-unit cap + drop report keep even a huge turn context-safe.
- A superseded-draft record (see search's collapse disclosure) FETCHES by explicit `--line`/`--uuid`: it renders as its own annotated unit (`(superseded draft — … outside turn numbering)`; JSON `superseded_draft:true`, `turn_index:null`) — never a fabricated t<N>.
- The v0.10.0 promoted non-record lines (a queue-operation with text, turn_duration, away_summary, stop_hook_summary, file-history-snapshot/-delta) render by explicit `--line`/`--uuid` address with no flag, labeled by their leaf. Still `--raw`-only: the session-state cache lines (last-prompt, mode, ai-title, agent-name, permission-mode), a content-less queue dequeue, and the unpromoted system subtypes; the miss error names them.
- Address misses error with the domain: `no such turn(s): t99 — the transcript has 2 turn(s) (t0..t1)`; open/from-end forms clamp (a `--turn -9..` on a 2-turn session is fine).
- Renders FULL records through search's pipeline (labels, pairing, plan pointers, sidecar merge). A metadata/attachment line is not a record — a range covering some prints `N line(s) in the addressed range are not records (… — inspect with --raw)`; a single-line miss error points at `--raw`.
- Cap: 200 record units by default; the drop prints `+N more record unit(s) … · continue: csift show @<id> --line A..B` (JSON `dropped_by_cap` + `refetch_remainder`). `--max-count N` / `0` = uncapped. `--raw` caps by line with the same stderr continuation.
- `--raw`: verbatim jsonl bytes — for unrendered fields (usage, stop_reason, model, any new field) and torn lines; excludes `--format json`.
- `--branch-points`: the transcript's FORK facts — every record with 2+ conversation children (a later parentUuid re-attach: a rewind, a retry, or a parallel lane), children with lines + timestamps, ranked by the widest inter-child time gap (a rewind usually shows a wide gap; a parallel lane near zero; an undated seam = honest-unknown, ranked last). Tool-result carriers, isMeta records, and compaction summaries never count as children, so a parallel tool fan-out is not a fork. FACTS only: which side is live is not computable from the jsonl — csift ranks, never classifies. Each fork prints a ready-to-run `show --line` at its latest child.

```bash
csift show @<uuid> --turn -3..              # the last 3 turns — tail-peek a session
csift show @<uuid> --line 46550             # the record search cited as L46550
csift show @<agent-id> --line 88,495..500   # from a subagent transcript (its OWN id)
csift show @<uuid> --line 46550 --raw       # exact bytes (all fields)
csift show @<uuid> --branch-points          # where did this conversation fork?
```

## list — which session is this?

```
csift list [target…] [--since W] [--until W] [--max-count N] [--sessions-from F]
  [--no-subagents] [--format json]
```
Head+tail read only (fast at any size). Unscoped all-projects run caps at the 50 most-recently-active rows (drop reported; a scoped query is uncapped; `--max-count N` overrides, `0` = uncapped) — the scope banner / JSON header `sessions_in_scope` stay the PRE-cap resolved range ("how big is my corpus" reads off line 1; only the ROWS are capped). `--since/--until` keep a session iff its [first, last] activity span intersects the window. Rows: cwd (FIRST-seen on purpose: the record cwd follows the tracked shell cwd, so last-seen could be a transient subdirectory) + branch + CC version — `git_branch`/`version` are LAST-seen (what the session is on NOW; the opening values ride `git_branch_first`/`version_first`, and text shows a drift arrow `branch a->b, CC x->y` when they moved mid-session); first ◂ / last ◂ / last ▸ excerpts (200 chars) + timestamps; subagent rows read `SUBAGENT <hex> · parent SESSION <uuid>`; pending elicitations annotate. CLONE LINEAGE: a transcript whose FIRST timestamped record is a compaction boundary was minted by COPYING another session there (a background-job fork: record uuids preserved, timestamps predating the file, slug stripped) — the row prints `clone    forked from SESSION <origin> at compaction boundary <uuid>` (origin = the sibling where that boundary natively lives; a prose quote of the uuid or a co-clone can never win the join), and JSON carries `is_clone`/`clone_of` (null when the origin is gone)/`clone_boundary_uuid`. JSON adds the sidecar tri-state: `sidecar_present:true` + pendings = blocked; `true` + none = provably not blocked on an elicitation; `false` = hook not installed, cannot conclude. `skipped_lines` is a census of the lines list actually READ (head/tail windows, each line booked once) — never a whole-file verdict; the whole-file corruption census is `stats`.

## whoami — identify the caller (false-positive-safe)

```
csift whoami [@main|@trap:<marker>] [--format json]
```
Reads `$CLAUDE_CODE_SESSION_ID` (alias `$CODEX_COMPANION_SESSION_ID`). Neither set ⇒ errors with guidance — never guesses by mtime. LANE HONESTY (v0.8.2): the env names the TOP-LEVEL session in EVERY lane, so the env form reports `is_subagent`/`parent_session_id`/`depth` as **null** (unknowable, never a fabricated false/0), prints a `lane unknown from env alone` text line, and notes the resolution path on stderr; every `@main` resolution likewise prints an unconditional stderr lane note. A first-try `@trap` HIT is lane PROOF; a miss proves nothing. Subagent caveat: current CC hands an Agent-tool subagent the PARENT session's id (the subagent's OWN id is withheld from env; workflow `agent()` likewise; older builds handed a Task subagent its own id) — so from a subagent, plain `whoami` usually resolves the ROOT; `@trap` resolves the true self env-independently and returns the full upstream chain (self depth 0 → root). @trap timing: a subagent resolves first try; a MAIN-thread first use normally misses — the answer there is `@main`, not a retry (§trap).

## stats — aggregates (tokens · tools · turns · span)

```
csift stats [target…] [--since W] [--until W] [--turn N|A..B|N..|-k] [--max-count N]
  [--sessions-from F] [--no-subagents] [--format json]
```
Per session: lines, user/assistant record counts, turns, compactions, first→last span + duration, tokens per model (input/output/cache_read/cache_creation — counted ONCE per API message: CC repeats the identical usage object on every per-block record, so per-record sums over-read 2-3.5x, which is exactly what pre-0.9.2 csift printed), narration blocks per model (API summaries, `agent.thinking.narration`; the token split is not derivable so only blocks are counted; a non-thinking non-narration tag shows as `unknown_thinking_tags`), tool CALLS by name (the tool-frequency ranking), and a whole-file `types` census — every physical line counted by its top-level `type` (`user`, `assistant`, `attachment`, `file-history-snapshot`, `system`, …): the answer to "what else fills this jsonl", since non-record lines are the bulk of many transcripts and no other surface parses them. `--turn` windows the aggregates on the turn axis — token burn of the last N turns is `stats @main --turn -N..` (everything windows EXCEPT `lines` and the `types` census — file facts, not window facts). Scope total block when >1 session; JSON summary carries scope totals (`tail -1 | jq .tokens`).

## files — what changed, when

Two different "which sessions touched X?" questions, two commands: sessions that EDITED the file = `files --glob '**/X'` (structural — Edit/Write/MultiEdit authoritative, Bash marked `heuristic`); sessions that merely MENTION it = `search "X" -l` (text recall, catches discussion too). Default to `files` for mutations, `search -l` for provenance/chatter.

```
csift files [target…] [--by summary|dir|file|timeline] [--regex RE] [--glob PAT]
  [--turn N|A..B|N..|-k] [--since W] [--until W] [--sessions-from F] [--no-subagents] [--format json]
```
Authoritative for Edit/Write/MultiEdit/NotebookEdit (create-vs-edit from the paired result); Bash mutations are lexical-heuristic and always tagged `(heuristic)`; failed STRUCTURED ops excluded, while a bash mutation from a partially-failed chain is kept and flagged `command_errored` (which arms ran is unknowable). A bash operand is RESOLVED against the record's own `cwd` (the shell cwd Claude Code stamps on every record), so relative and absolute spellings of one file share a bucket; each timeline row carries `resolution` (`absolute` | `cwd-joined` = record cwd, zero inference | `cd-tracked` = literal in-command cds | `unresolved` = kept verbatim, never guessed) + `path_verbatim` when the typed spelling differs. Commands that mutate files they never name surface as class markers (`git:<sub>`, `fmt:<tool>`, `interp:<lang>`, `pkg:<manager>`, `extract:<tool>`) — flags, never paths. `--by`: summary = top-prefix rollup (default) · dir · file · timeline (one line per mutation). `--regex` (full absolute path, case-exact) ∧ `--glob` (`**` crosses `/`) filter before rollup. An `external write` timeline row (v0.9.4) is a SNAPSHOT-INFERRED mutation — the tracked file's file-history version jumped with no tool record in the interval (CC rewrote it on `/model`/`/config`/plugin toggles, or an outside editor); reported ONLY for the settings family (`.claude/settings*.json`) — the tracked set spans thousands of ordinary paths and wider reporting would flood every timeline; the row detail names the version transition + interval, JSON op `external_write` with `heuristic:false` + `detail`. An Edit-before-Read boundaries section always follows — out-of-band changes (formatter/git/editor) that forced a re-Read; the "risky to recover" signal (then `recover --coverage`).

```bash
csift files @<uuid> --by file --format json | jq -r 'select(.kind=="file" and (.heuristic|not)).path'
csift files --glob '**/foo.rs' --by file      # which sessions touched foo.rs (all projects)
```

## recover — rebuild a file (or a deleted plan) from the transcript

```
csift recover TARGET --file <ABS|SUFFIX|@plan> [--salvage|--patches|--at WHEN|--coverage|--list-backups]
  [--out PATH] [--file-lines N|A..B|N..|-k] [--turn N|A..B|N..|-k] [--since W] [--until W]
  [--files-from MANIFEST --out-dir DIR [--force]] [--sessions-from F] [--no-subagents] [--format json]
```
Replays the file's Read/Write/Edit stream into a sparse buffer — absent lines are explicit gaps, never fabricated. `--file` matches exact or component-aligned trailing suffix (`app.py`≡`src/app.py`; `b.rs`≠`ab.rs`); bash events join through their RESOLVED paths, so an absolute `--file` matches a relative operand recorded under the same cwd. Five exclusive modes: **restore** (default; hard-fails if partial, naming covered+missing ranges + the recipe) · **--salvage** (never-fails fragment; gaps marked `??? lines A..B unknown`) · **--patches** (unified diffs; 3 anti-fabrication anchor checks gate every hunk) · **--at WHEN** (point-in-time; WHEN = ISO | `2h` | `@turn:N` | `@line:N` — a TRANSCRIPT line | `@latest`) · **--coverage** (scoping dry-run; run before trusting a salvage). `--file @plan` resolves the session-bound plan (rebuilds even a deleted one). Batch: `--files-from` manifest + `--out-dir`, one corpus scan (the TSV carries boundaries/bash_file/bash_opaque columns).

BASH CONTENT ANCHORS (v0.9.4): the DETERMINISTIC shell subset replays as first-class content, not boundaries. Writes: a quoted-delimiter heredoc via `cat`/`tee` (the body is byte-verbatim in the transcript; unquoted only with an expansion-free body), literal `echo`/`printf`, `truncate -s 0` — per SEGMENT, so the dominant "write the file, then run it" compound command anchors (a compound command additionally demands a CLEAN result echo: empty stderr + not interrupted, since only the last segment owns the exit code and a failing write always says so on stderr). Reads: `cat F` / `head -n N F` / `sed -n 'A,Bp' F` as SINGLE commands under the same clean-echo gate — the stdout IS the file window (an EOF-reached window from line 1 = the whole file). Every gate refuses toward a boundary, never toward a wrong anchor: variable targets, pipes, substitutions, interpreter heredocs (scripts, not content), ssh heredocs (remote fs), a second same-file touch in the command, `tail` (unplaceable), `sed -i` (measured zero literal yield). A byte-known `>>` append places only onto a COMPLETE newline-terminated buffer, else it discloses as `bash_append_unplaced`. Coverage counts `bash-read-anchor`/`bash-write-anchor`; segment provenance names `bash-heredoc`/`bash-cat`/`bash-write`. A file written ONLY through the shell — previously "no recoverable history" — now restores when its writes pass the gates.

WINDOW ACCOUNTING (v0.8.0): every mode counts what the replay could NOT include — bash mutations of the file (disclosed as boundaries), opaque mutating-class commands (formatter/pkg/extract/interpreter markers: real mutations, unknowable file sets), PowerShell commands (never parsed) — and prints a ready-to-run time-bounded `csift search` for the window. `complete` = complete FROM THE TOOL STREAM; only the explicit clean-window note means nothing else ran. Claude Code's own signals are adopted: a Bash result's `staleReadFileStateHint` (CC names the modified files itself) = a hard `hint_modified` boundary — the one signal that pins a formatter rewrite to concrete files; `staleRecovered` on a successful Edit = a `stale_recovered` annotation (disk drifted, edit still applied); an external-edit boundary with a formatter-class command in its window names that command in its detail. Boundaries split hard (invalidating) vs soft (annotation/heuristic); `fragments = hard + 1`. ABSENCE-OF-SIGNAL LIMIT: a change that produced none of these signals (read-first, changed outside, never re-touched) leaves NO transcript trace — a clean ledger is strong evidence, not proof. PowerShell command text is never parsed (counted only).

`--list-backups`: list Claude Code's OWN file-history checkpoint store for `--file` (a literal absolute path — the store key is sha256 of it): one row per checkpoint (backup instant, bytes, @vN, store path), ordered by backup instant. Provenance bounds, stated in the output: tool-layer only (bash and manual edits never land there), pruned over time, and @vN counters reset per session dir (never an order key) — absence proves nothing, and the listing is NOT a history. csift never merges checkpoint content into a reconstruction (no transcript anchor); copy a store path yourself to inspect one.

FILE-HISTORY SNAPSHOTS (v0.9.4): CC backs every Edit/Write-tracked file up per prompt and bumps its `version` only when bytes changed — the version sequence records DISK TRUTH, incl. writes with NO tool record (CC rewriting settings on `/model`/`/config`, an outside editor; measured: half of all settings.json mutations are silent). recover compares the replayed buffer to the snapshot content at each version change (store blob accepted only when its mtime matches the recorded backup instant — the `@vN` name collides across a mid-session counter reset): a disagreement = an authoritative HARD `external_write` boundary and the replay REBASES on the snapshot bytes, so a silent write no longer yields a never-existed "100% complete" state; without the blob, a jump with no tool write since the previous snapshot discloses the same boundary content-less. A merged interval (tool write + silent write in one bump) is only caught by the content comparison, not the number.

Pre-trust recipe: `--coverage` first; read the hard/soft boundary split + the opaque-in-window list; run the printed `csift search` if any; only then trust a restore/salvage.

```bash
csift recover @<uuid> --file /abs/gone.py --salvage
csift recover @<uuid> --file @plan --out /tmp/plan.md
```

## plan — locate the bound plan file

```
csift plan [target] [--reverse PLAN.md] [--audit] [--no-subagents] [--format json]
```
TWO binding laws, in precedence order (never path heuristics): the `plan_mode` attachment when one exists; else the FIRST slug-carrying record — Claude Code's own rule, which is how a forked clone (attachments stripped, slugs kept) still gets its plan re-injected. Rows carry `binding_source` (`plan_mode` | `slug-only`) and `minted_at_compaction` (true when the slug's first carrier is a compaction boundary — the fork mint site). No target ⇒ the calling session (env). `--reverse <file>` inverts: which session(s) bind this plan. Locates only — then pick by question: what's on DISK now → `cat` the path; what the SESSION last had (or the plan is deleted) → `recover --file @plan`. The two can differ. `--audit`: every structured mutation (Write/Edit/MultiEdit/NotebookEdit) the scope made to a file SOME session binds as its plan, with a warning when the mutating session does not bind it — only the BOUND plan is re-injected in full after a compaction, so content parked in another session's plan file does not come back. Plan files are identified by joining the corpus's bindings (one prefiltered scan), never by guessing a plans directory; bash-side edits are outside the audit.

## verbatim — restore turns a compaction summary clipped

```
csift verbatim TARGET… [--budget N] [--round-trip-fraction F] [--agent-msgs longest|eot-only|rich|all]
  [--profile heavy|light] [--max-compactions N] [--subagents] [--turn N|A..B|N..|-k] [--since W] [--until W]
  [--sessions-from F] [--slice N [--slices N] [--window N]] [--out PATH] [--format json]
```
Not the tail-peek tool — that is `show --turn -N..`. A compaction summary keeps task state but loses turn fidelity; `verbatim` re-emits the verbatim user/assistant turns (each `Lnnnnn`), selected backward from EOF, printed ascending, transparent across many boundaries. On a session with NO compaction it tells you so (stderr note pointing at `show --turn`) — nothing was clipped there.
- A target is REQUIRED (the `--budget` is per-session; a bare run would multiply it across every project).
- `--budget N` = CHARS per session (default 40000; ≈4 chars/token). The header's `spanned K of N compaction boundaries in scope` is budget-relative on K (what the backward-from-EOF selection crossed — a small budget can honestly read `0 of 4`); N is the session's true total (== `stats`' unwindowed `compactions`). `--round-trip-fraction F` (default .5) reserves a floor for human round-trips. `--agent-msgs longest` (default) · `eot-only` · `rich` · `all`; `--profile heavy|light` is the whole tuning surface.
- Collapsed runs render `△ L{a}-L{b} [X agent message(s), …]` → fetch via the row's `refetch`. Units over the role caps middle-truncate with explicit counts (JSON `text` is always full). A turn already quoted by the newest summary is flagged `(also in summary)` and demoted, never dropped.
- Slicing (hook injection, ≤10000-char cap): `--slices N --slice i --window W` = fixed-fleet chunks, whole turns; out-of-range ⇒ nothing, exit 0 (hook affordance). Text-only.

## agents — subagent lifecycle + topology

```
csift agents [target] [--agent ID] [--shape builtin-task|workflow|teammate]… [--agent-type T]…
  [--since W] [--until W] [--order-by trigger|start|completion] [--with-files] [--returned-message]
  [--sessions-from F] [--format json]
```
Text = a parent→child tree (nesting is logical, from spawn links; disk is flat). JSON = FLAT kind-tagged rows: per session a light `session` row (counts), each workflow run a `run` row, every agent its own `agent` row in tree pre-order — rebuild nesting from `parent_agent_id`/`depth`; `jq 'select(.kind=="agent")'` reaches every node.
- `shape` = transcript shape: `builtin-task` · `workflow` · `teammate` (built-in location + meta `taskKind:"in_process_teammate"`; name-embedded id; csift recovers the real `agent_type` + spawn via name-join).
- `--order-by` sets sort AND the `--since/--until` axis: `trigger` (default; the parent tool_use ts = true spawn) · `start` · `completion`. `--agent ID` = one node (implies returned-message; miss = error).
- Frozen lane: the newest record an unreturned tool_use ⇒ `status:"running"` + `pending_classification`: `escalation-blocked` (a dangerous-rm Bash CC hoists for approval — the one positively confirmable state) | `awaiting-execution` (slow OR wedged OR abandoned — jsonl can't tell them apart; at corpus scale a lane pending for hours/days is overwhelmingly "parent session ended", not in-flight — weigh `pending_since_utc` against now yourself).
- Fork provenance: a transcript created by `/fork` opens with a `fork-context-ref` record — its node prints `forked-at <uuid> (context N)` and JSON carries `fork_parent_last_uuid` + `fork_context_length`. `--agent-type T` (repeatable, EXACT match on `agent_type`) filters nodes — `--agent-type fork` lists fork children; it composes with `--shape` (shape = on-disk location, type = what the agent is).
- Teammate control (csift is read-only; this is a pointer): steer/terminate via `SendMessage` BY NAME (`message:{type:"shutdown_request"}`), never TaskStop (rejects every teammate id form) or pkill (in-process). Text footer + node `control_hint`.
- `returned_message` = the NEWEST message the child EVER returned — on a non-completed lane it predates the pending call, and the text render brands it inline (`history — predates the still-open lane, NOT the outcome`): a "work is complete"-sounding tail on a frozen lane is history, not the ending. It answers "what did the ORCHESTRATOR record", not "what did the agent conclude" — a `sync-tool-result` source can be the harness's truncated `Done. agentId: …` wrapper; the child's own final words are always `show @<agent-id> --turn -1..`. A `run` row's `status` is the workflow journal's verbatim last word (open set; observed `completed`/`killed`).

## image — pasted images

```
csift image [target] [--id N|L<line>i<n>]… [--out DIR|FILE.ext]
  [--since W] [--until W] [--turn N|A..B|N..|-k] [--uuid PREFIX] [--sessions-from F] [--no-subagents] [--format json]
```
Default list (content-deduped). `--id` input = bare digits (the `[Image #N]` number; display shows `#N`, input drops the `#`) or the always-unique locator `L<line>i<n>`; an ambiguous `#N` hard-errors with the occurrence list. `#N` is inherited from CC's paste-time `[Image #N]` numbering, NOT a dense 1..N index — handles can start past #1 and carry holes (a source gap: that number's image never landed in this transcript); a `--id` miss errors naming the handles that DO exist. `--out`: dir ⇒ source-format files; `file.ext` ⇒ converted by extension (png lossless · jpeg/webp q90 · gif dithered). search/verbatim cite ids inline (`[1 image: #265]`).

---

## status + wait — live truth (point-in-time, explicitly non-reproducible)

The one deliberate departure from the forensic contract: these two answer "NOW" and say so (everything else stays reproducible). `status TARGET` = one verdict with named evidence; `wait TARGET --until COND… --timeout S` = block until a condition fires or the bound elapses.

```
csift status TARGET [--background-since WHEN] [--ignore-background RE]… [--no-subagents] [--format json]
csift wait TARGET --until COND [--until COND…] --timeout SECS [--interval MS] [--background-since WHEN] [--ignore-background RE]… [--no-subagents] [--format json]
```
- Verdicts (closed set, seven since v0.10.0): `running` (a tool in flight: an unreturned tool call at the tail, or registry busy/shell) · `waiting-children` (main idle, subagent/workflow lanes live — incl. the workflow journal's started-minus-result imbalance) · `waiting-hitl` (a pending AUQ/ExitPlanMode/MCP elicitation via the sidecar) · `idle-background-open` (the turn ended, but N background task(s) the lens counts have not returned — neither running nor stopped; by design or not, csift cannot tell) · `idle-eot` (end_turn, nothing pending anywhere) · `stale-dead` (owner process gone — pid probe + a process-start-time guard against pid reuse; the tail then says HOW it died) · `unknown` (evidence insufficient or contradictory — stated, never guessed). Precedence: dead > hitl > running > children > background > eot > unknown.
- BACKGROUND TASKS (v0.10.0) — the section every long session needs. A `Bash` launched with `run_in_background` gets its tool_result within milliseconds, so the tail state machine pairs it at once; the harness writes NOTHING about a still-running shell at end of turn (the REPL's "1 shell still running" lives in process memory — the `turn_duration` record carries a duration and a message count, and its pending counts cover background AGENTS and workflows only). So `status` scans the whole main transcript (launches from every lane; completions land only in the main file, through three carriers: a user record when the session was idle, a `queue-operation` line + `queued_command` attachment when they arrived mid-turn) and lists every OPEN task as a `bg` row: kind `shell | agent | monitor`, id, launch instant and age, description or command, the output file's size and last write, and folds every closed one to counts (completed / failed / killed / stopped / timed out). A Monitor is armed as an immediately-paired tool call and shares the shell id namespace (both are `local_bash` tasks in the harness); event pulses never close it, its termination notice or timeout does; a PERSISTENT monitor never returns by design. NOT RETURNED IS NOT PROOF OF RUNNING: Claude Code's own orphan summary (written at the next session start, `shouldQuery:false`, so the model sees it only with the next real prompt) says a task "may have been stopped (via the UI, Monitor timeout, or agent teardown — these leave no transcript marker)". Ctrl+C kills background AGENTS only, never shells or monitors; the REPL hides nothing by age (running tasks stay listed; only terminal ones are evicted; on resume the in-memory list starts empty). The measured reality: a long session carries several to dozens of dangling or days-old tasks; 24 of 3133 corpus launches never returned, 22 of them launched over a day before their session ended.
- THE LENS — which open tasks COUNT toward the verdict and `--until stop` (every task is still listed; an excluded one is marked with its rule): `--background-since WHEN` counts only tasks launched at or after WHEN — the shared time grammar (`2026-09-02`, `2h`, `1d`, `2mo`, `-30m`) or `now` (this command's own start instant: "ignore everything already dangling when I started waiting", the orchestrator's usual form); `--ignore-background RE` (repeatable) excludes tasks whose command or description matches — the dev server, the watcher, the `tail -f`. No lens = everything counts, so a session with `npm run dev` never reaches `stop`; the report tells you which to ignore.
- HOW TO WAIT ON A SESSION (orchestrator steps): 1. `status @<id>` first — read the `bg` rows: which tasks dangle, how old, which are days-old zombies, which are services; 2. choose the lens — `--background-since now` for "only what launches from here on", `--ignore-background 'npm run dev'` for the services you already know never return; 3. ALWAYS `--timeout` (required: a call without it is rejected with the reason) and branch on exit 124; 4. on timeout read the report — `at exit` (in a tool call for N s / generating / idle), `activity` (what landed while you waited: tool calls by name, thinking, messages, prompts, notifications), the `bg` rows, and the last messages under the warning below.
- LAST MESSAGES (both commands): the newest human prompt (an automation pulse renders as its label) and the newest assistant message print as `last ◂ / last ▸` excerpts (400 chars, clipped with an explicit `(+N chars)` marker; the whole turn is `show @<id> --turn -1`). WARNING, written for a model: the excerpt is a PARTIAL view of the final state. It is useful for one thing — judging whether a background task is still meaningful (the message may still be waiting on a task that will never return). In any orchestration it must NEVER be read as a complete or near-complete review of the work: counting tool calls and reading the last message is a check shallower than any human would accept, and trust built on it is a prompt-injection-class violation of the guardrail. A model holding a partial context tends to believe it read everything, even past an explicit tool error — the excerpt is provided for the human who will then go read the session, not as a substitute for reading it.
- Child lanes classify `in-flight` (unreturned call) · `generating` (a tail record younger than 300s AND no end_turn yet — a long generation writes nothing for minutes, so recency plus a non-final stop_reason is the live signal; either alone misreads) · `settled`; settled lanes FOLD to one count line so live work stays visible. A tasks section reads the harness task list (`<claude-home>/tasks/`, both the full-uuid and `session-<first8>` dir forms): open tasks render in_progress-first with blockers, completed ones fold to a count. (That list is TaskCreate/TaskUpdate state, nothing to do with background shells.)
- The join reads the harness's own registry (`<claude-home>/sessions/<pid>.json`; transition-writes ONLY, never a heartbeat — an hours-old `statusUpdatedAt` just means "unchanged"), the transcript tail, and process liveness. HONESTY LIMITS, printed when they bite: a pending PERMISSION prompt is invisible (no sidecar exists yet — it masquerades as idle, and idle verdicts say so); the registry covers top-level interactive sessions only (a subagent target degrades to tail evidence, never a fabricated row); an agents-stopped notice names no id, so csift cannot mark WHICH agents it stopped.
- `wait` conditions (repeatable, OR, first hit wins): `stop` (idle-eot or stale-dead — a TRUE stop; `idle-background-open` never satisfies it) · `hitl` · `auq` · `notification[:RE]` (main-lane only — notifications never land in child transcripts) · `tool:NAME[:RE]` (RE over the serialized input) · `write:PATH_RE[:LINE_RE]` · `verdict:V` (any of the seven). Same RE2-class regex as search.
- BASELINE SEMANTICS — the monitor/query boundary: `wait` snapshots every watched file's byte length at startup and fires ONLY on events strictly after those offsets; a condition already satisfied by history never fires (history is `search`). After the snapshot a readiness line prints to stderr (`csift: watching N file(s)… timeout Ns[; lens: …]`) — a scripted caller orders its own trigger AFTER that line and the race is gone. Child lanes and the elicitation sidecar born AFTER the watch starts join it automatically with a zero baseline (their whole content is post-start).
- Exit codes: 0 = fired (the output names which condition, then the same report as a timeout) · **124** = timeout (JSON `fired:"timeout"`) · other non-zero = error (a missing `--timeout` is one).

```bash
csift status @<uuid>                                             # is it truly stopped? (with evidence + bg rows)
csift status @<uuid> --ignore-background 'npm run dev'           # the dev server never returns: count everything else
csift wait @<uuid> --until stop --timeout 300                    # block until truly stopped (or 5m -> exit 124 + report)
csift wait @<uuid> --until stop --timeout 900 --background-since now   # only what launches after I start waiting counts
csift wait @main --until auq --timeout 3600                      # fire when a question lands
csift wait @<uuid> --until tool:Read:handover --timeout 600      # ...until it reads that file
```

## JSON — envelope v2 + schema reference (transcribed from live output)

Every `--format json` stream is exactly: `{"kind":"header","command":…}` first (span commands add `sessions_in_scope`/`top_level_sessions`/`subagent_sessions`) → kind-tagged rows → `{"kind":"summary",…}` last. Universal idiom: `jq 'select(.kind=="<row>")'`; summary = `tail -1 | jq`.

Row kinds: list→`session` · search→`exchange` | `census` · show→`record` | `branch-point` · stats→`session` · files→`mutation|file|dir|bucket|boundary` · agents→`session|run|agent` · verbatim→`turn|compaction_boundary|collapsed_agents` · plan→`plan` | `binding` | `plan-edit` (--audit) · image→`image|extract` · whoami→`identity` · recover→`coverage|segment|snapshot|restore|boundary|backup` (--list-backups) · status→`verdict` · wait→one bare `{kind:"wait"}` object.

Shared row fields — the id trio on every spanning row: `session_id` (the transcript's OWN id: top-level uuid or subagent agent-id, both round-trip as `@…`) + `is_subagent` + `parent_session_id` (the owning uuid; = session_id on top-level rows). The two-rule id law: line-addressed fetches use `session_id`; scope-level re-targeting uses `parent_session_id`. Hits and collapsed rows carry `refetch` — a ready-to-run `csift show` command at the right id; prefer running it verbatim over assembling your own.

Field enums: `pairing` = `paired` | `pending` | `orphan` | null · census `axis` = `label|tool|turn|session|pairing|model|attachment|version|result` · `shape` = `builtin-task|workflow|teammate` · `source` = `elicitation-sidecar` | null · files `op` = `write|edit|multi_edit|notebook_edit|bash`. An agents RUN row's `status` is NOT one of these closed sets — it is the workflow journal's own last status verbatim (open set; observed: `completed`, `killed`), distinct from an agent row's csift-computed `status`.

Key fields per row (fixture-verified):
- search `exchange`: trio + `turn_index (null on a draft unit), superseded_draft, ts_utc/local, record_uuids, hits[]`; each hit: trio (v0.6.5 — bare `.hits[]` flattening keeps real ids) + `label, labels[], line (null=sidecar), uuid, ts_utc/local, tool_name, from, to, pairing, is_error (result hits: true|false; else null), tool_use_id, queue_operation, queue_reason (a `user.queued` hit's event + remove reason; null elsewhere), source, excerpt, image_ids[], refetch`. Summary: `matched, sessions, transcript_ids[≤100], transcript_ids_truncated, dropped_by_cap, skipped_lines, superseded_drafts, with_elicitation_sidecar, excerpts_truncated` (+ on zero matches `definitive_absence, active_filters, excluded_by_label, gated_leaves_unreached`).
- search `census`: `axis, key, records`. Summary: `axis, matched_records, distinct_keys, excluded_records, dropped_by_cap, skipped_lines`.
- show `record`: trio + `turn_index (null on a superseded draft), superseded_draft, line (null=sidecar), uuid, label, labels[], tool_name, from, to, pairing, is_error, tool_use_id, source, ts_utc/local, text (FULL), image_ids[]`. Summary: `records, dropped_by_cap, refetch_remainder, non_record_lines, skipped_lines, with_elicitation_sidecar`. `branch-point` (--branch-points): `uuid, line, children[{line, uuid, record_type, ts_utc/local}], widest_gap_seconds`; summary `{branch_points, conversation_records, skipped_lines}`.
- list `session`: trio + `path, cwd (first-seen), version, git_branch (both LAST-seen), version_first, version_last, git_branch_first, git_branch_last, first_user/last_user/last_agent ({excerpt, ts_utc, ts_local}|null), skipped_lines (WINDOW census — the head/tail lines list read, each booked once; whole-file census = stats), pending_elicitations[], sidecar_present, with_elicitation_sidecar, is_clone, clone_of, clone_boundary_uuid`. Summary: `sessions, dropped_by_cap, skipped_lines`.
- plan `plan`: trio + `line (the bind record's jsonl line), plan_file (the bound path — NOT `path`), plan_exists, slug, binding_source ("plan_mode"|"slug-only"), minted_at_compaction`. Summary: `plans`. (plan's header is the light `{command}` form — no scope split.) --audit: `binding` rows (same fields) + `plan-edit` rows `{owner_session_id, path, mutations, bound_by_owner, binder_session_id, binder_line}`; summary `{bindings, plan_files_touched, warnings, skipped_lines}`.
- recover rows by mode — `coverage`: trio + `file, fragments, hard_boundaries, soft_boundaries, events (incl. stale_hint, stale_recovered, bash_read_anchor, bash_write_anchor), boundaries, covered_ranges, recoverable_lines, seen_total_lines, opaque_commands, powershell_commands, suggested_search` · `segment` (--patches): trio + `segment_index, line, line_start/line_end, turn_start/turn_end, ts_utc/local, pre_state_known, anchor_source, unified_diff` · `snapshot` (--at/--salvage): trio + `file, lines, gaps, line, seen_total_lines, boundaries, opaque_commands, powershell_commands, suggested_search` · `restore`: `file, complete, lines, boundaries, bash_events, opaque_commands, powershell_commands, suggested_search` + `content` (or `path`+`wrote`) — the ERROR paths still emit `{kind:"restore", complete:false, reason:"partial"|"no-history"|"invalidated"}` + the summary before the non-zero exit, so the envelope always closes. `backup` (--list-backups): `session_id, version (the vN token), path (the store file), bytes, backup_utc/local`; its header adds `{mode:"list-backups", file, hash, store, store_present}` and the summary `{backups, sessions}`. A boundary object: `line` (the `--at @line:` cutoff coordinate) + `source_session_id`/`source_line` (the REAL transcript location — feed to `csift show`) + `turn_index, ts_utc/local, cause, confidence, detail`. Summary: `{file, mode, sessions, skipped_lines}`.
- image `image`: trio + `id, handle (#N|null), seq, img_index, line, record_uuid, media_type, source_kind, b64_len, est_bytes, url, ts_utc/local`. Summary: `images, transcripts, skipped_lines`.
- stats `session`: trio + `lines, line_types{type→count} (whole-file, never windowed), user_records, assistant_records, turns, compactions, first_utc/local, last_utc/local, tokens{model→{input,output,cache_read,cache_creation}} (deduped per API message.id), narration_blocks{model→count}, unknown_thinking_tags, tools{name→count}, skipped_lines`. Summary adds scope totals (`tokens`, `narration_blocks`, `unknown_thinking_tags`, `tools`, `turns`, `line_types`).
- agents `session`: `session_id, runs, agents` (counts). `run`: `session_id, run_id, task_id, workflow_name, status, agent_count, duration_ms, total_tokens, total_tool_calls, default_model, started_utc/local`. `agent`: `agent_id, shape, parent_session_id, parent_agent_id, depth, workflow_id, agent_type, name, team_name, description, fork_parent_last_uuid, fork_context_length, spawn_tool(_use_id), trigger/started/completed/last_activity_utc+local, duration, status, pending_tool_use_id/tool_name/classification/since_*, skipped_lines (head/tail window census, like list's) — completed_* and duration are non-null ONLY when status=completed; last_activity_* is the tail instant on every timestamped lane (== pending_since_* when frozen), control_hint?` (+ `returned_message(_source)`, `files_changed[]` when requested — `returned_message` is the NEWEST message the child EVER returned; on a frozen/running lane it predates the pending call, so read it beside `pending_*`, never as the outcome). Summary: `sessions, runs, agents`.
- verbatim `turn`: trio + `turn_index, line (null=sidecar), source, role, ts_utc/local, tool_calls, full_chars, rendered_chars, truncated, elided_*, also_in_summary, compactions_before, text (FULL), is_automation (+trigger_kind, task_id, status, event)`; `compaction_boundary`: `line, summary_chars`; `collapsed_agents`: `first_line, last_line, refetch`. Header adds the full budget accounting: `budget_chars, max_total_chars, round_trip_fraction, chars_used, boundaries_spanned (budget-window-relative), boundaries_total (scope's true total), selected_user, selected_assistant, automation_by_kind (the SELECTED triggers per class), automation_in_scope_by_kind (every in-scope pulse REGARDLESS of budget — the same window-vs-scope pairing as boundaries_*), automation_triggers (flat total of automation_by_kind's values), budget_is_per_session, sessions_rendered, with_elicitation_sidecar`.
- files rows carry the trio + `path, op, turn_index, line, is_create, heuristic, resolution, path_verbatim, command_errored, ts_utc/local` (timeline) or per-op counts + `first/last_utc/local` (grouped); `boundary`: `path, line, turn_index, cause, ts_utc/local`. Summary: `sessions, distinct_files, total_mutations, edit_before_read_boundaries, skipped_lines, detail_level` (no cap ⇒ no `dropped_by_cap`).
- status `verdict`: `{verdict, evidence:[{surface (registry|pid|tail|children|sidecar|background), value, age_secs}], children:[{session_id, state (in-flight|generating|settled), detail} — live lanes only], settled_children, tasks:[{id, subject, status, blocked_by}] (null = no tasks dir; [] = a dir with nothing), tasks_completed, pending:[…], background:{open, ignored, completed, failed, killed, stopped, timed_out, scanned_files, tasks:[{kind (shell|agent|monitor), id, tool_use_id, lane, state, description, command, launched_utc, launched_local, age_secs, output_file, output_bytes, output_age_secs, ignored_by} — open tasks only], notes:[…]}, last:{user:{ts_utc, ts_local, text, truncated}|null, agent:{…}|null}, tail_state, notes:[…]}`; summary `{verdict}`. wait exit object: `{kind:"wait", fired (condition|"timeout"), verdict, waited_secs, at_exit, activity:{records, lanes, tools:{name: count}, thinking, agent_messages, user_prompts, notifications}, evidence:[…], background:{…}, last:{…}, notes:[…]}`.
- whoami `identity`: `session_id, path` + lane fields `is_subagent`/`parent_session_id`/`depth` — REAL on the @trap chain, **null** on the env form (unknowable).

## jq canon — csift narrows, jq refines

Never jq the transcript FILE (you lose span resolution, the sidecar merge, and the malformed-line count). Always let csift emit the records, then jq freely — this is the intended pipeline, not a fallback:

```bash
csift search "" @U -t agent.message --raw | jq -r '.message.model' | sort | uniq -c     # any raw field
csift search P @U --format json | jq 'select(.kind=="exchange") | .hits[] | {label, line, excerpt}'
csift search P @U --format json | tail -1 | jq                                          # the summary
# flatten hits BARE — every hit carries the id trio itself (v0.6.5), no merge step needed:
csift search P @U --format json | jq -c 'select(.kind=="exchange") | .hits[] | {session_id, label, line}'
csift agents @U --format json | jq 'select(.kind=="agent") | {agent_id, shape, status}'
csift stats @main --no-subagents --format json | tail -1 | jq .tokens                    # token burn
csift files @U --by file --format json | jq -r 'select(.kind=="file" and (.heuristic|not)).path'
csift search "" @U -t agent.tool.use --raw | jq 'select(.message.content[]?.input.command? // "" | test("rm "))'
# RECORD-level pipeline (fetch a filtered subset of hits FULL): select in jq, then run the
# csift-generated refetch commands — each already addresses the hit's OWN transcript, so this
# composes across subagents where a line-number pipe could not (lines are per-FILE):
csift search P @U --format json | jq -r 'select(.kind=="exchange") | .hits[] | select(.label=="agent.tool.result") | .refetch' | sh
```

## What csift will NOT do (and the designated alternative)

- Semantic/BM25 search → regex is the tool; broaden the pattern, or census first (`--count-by label`).
- Arbitrary aggregation/group-by DSL → the closed `--count-by` axes, `stats`, `files --by`; anything else = `--raw | jq`.
- Field-predicate queries / joins ("tool_use where input.x AND result errored") → `search` narrows the scope, `--raw | jq` applies the predicate.
- Diffs between turns/files → `show` both, diff outside; file states = `recover --at`.
- Writing/terminating anything → csift is read-only; it prints control HINTS (teammates → SendMessage).
- Reading the live team/task coordination files under the config home → mutable, unversioned, mid-write state owned by the running harness; the transcript is the durable record — `agents` for topology, `search -t agent.communication` for the messages.

## Elicitation sidecar — pending AskUserQuestion / ExitPlanMode / MCP

While pending, these three leave NO trace in native jsonl (whole-turn buffered / in-memory) — a session blocked on a human looks stalled. A CC hook (recipe 3) appends markers to `<uuid>/elicitations.jsonl` (a sidecar, never the transcript). csift merges UNRESOLVED pendings automatically wherever it reads a session: they classify `agent.tool.use`, verbatim appends each as its own newest turn, list annotates. Once answered, CC writes the real record and the pending pairs off — no duplicates. GHOST GUARD: a REJECTED AUQ/plan fires no PostToolUse, so the hook can miss its `resolved` marker — csift therefore also drops any AUQ/ExitPlanMode pending whose tool id already appears on a native record (structural check, a quoted id in prose doesn't count): the native transcript outranks the sidecar, so a stale marker can never report a long-closed elicitation as pending. MCP markers have no native form — sidecar pairing stays their only signal. A merged record has no physical line: renders `(elicitation sidecar)`, JSON `source:"elicitation-sidecar"` + null `line`; surfaces print `with elicitation sidecar`. The sidecar cannot be targeted directly (error). Tri-state on list rows: `sidecar_present:false` = hook not installed — "nothing pending" is then NOT concludable. A sentinel-bearing marker the CURRENT schema cannot read (schema skew — a pre-release fossil under old field names) is counted into `skipped_lines`, never merged, never invisible.

## Conventions

- WHEN grammar (`--since/--until/--at`): relative `45s 90m 2h 3d 1w` (that long ago, system-local) or ISO8601 — bare date ⇒ local midnight · BARE datetime (`2026-06-01T05:00:00`, no `Z`/offset) ⇒ that LOCAL wall-clock time · `Z`/`+10:00` ⇒ explicit zone. Bounds inclusive; records without timestamps never match a bounded window.
- `--claude-home DIR` (global, any position — even before the subcommand) repoints `~/.claude`; precedence flag > `$CLAUDE_CONFIG_DIR` > the OS home's `.claude` (`$HOME` on Unix, `%USERPROFILE%` on Windows — the same resolution Claude Code uses; a stray Git-Bash `HOME` is ignored there).
- Path filters (`files --regex/--glob`) are case-exact (paths); search PATTERN is smart-case (text).
- Retention: CC deletes a transcript once its file MTIME (the session's last write — NOT its creation date; reading refreshes nothing) is older than `cleanupPeriodDays` (default 30!), and removes the session's whole sidecar tree (subagents, tool-results) with it. Check `jq '.cleanupPeriodDays // 30' ~/.claude/settings.json`; recommend 180/365 — csift can only read what survives.
- Exit codes: the contract is 0 vs non-zero, nothing finer. De facto a USAGE error (clap parse: bad flag/selector/conflict) exits 2 while a csift-level error (address miss, pinned id matching nothing) exits 1 — clap's convention, informational only; don't build on the split.

## Recipes

```bash
# which sessions mention X — then run ANY command over exactly those (the composition loop):
csift search "X" -l | csift files --sessions-from - --by file
# read what search found: run the hit's refetch verbatim (text prints the L<n> + the right id)
csift show @U --turn 270              # turn 270's whole exchange
csift show @U --turn -3..             # the last 3 turns (tail-peek "what's it doing")
# what record-types exist before you filter (so an empty -t is never a mystery):
csift search "" @U --count-by label
# pending tools / tool frequency / model census — one command each:
csift search "" @U --count-by pairing
csift stats @U --no-subagents          # tool CALL counts + tokens + turns
csift search "" @U --count-by model
# any unrendered field of matched records — never hand-parse the file:
csift search "" @U -t agent.message --raw | jq -r '.message.model' | sort | uniq -c
# only reach for verbatim when a COMPACTION clipped the turns (it tells you if not):
csift verbatim @U --turn -20..
```

### Hook 1 — SessionStart(compact): re-inject verbatim turns after compaction (#1 recipe)
N hooks run `verbatim --slices N --slice i` to supplement the summary with the recent verbatim turns (lands as an `attachment` record — csift ignores it, no feedback loop; safe to re-fire). Load-bearing race fix: CC runs same-event hooks CONCURRENTLY and concatenates in completion order — a `$PPID`-namespaced done-flag barrier forces slice order. ONE script registered N times:

```bash
#!/usr/bin/env bash
set -euo pipefail
slice="${1:?1-based slice index}"; N=4; WINDOW=9000 # N MUST equal the number of registered hooks
SEQ="/tmp/csift-turns-slice-$PPID"
release(){ mkdir -p "$SEQ"; touch "$SEQ/s$slice.done"; [ "$slice" = "$N" ] && rm -rf "$SEQ"; return 0; }
trap release EXIT
if [ "$slice" -le 1 ]; then rm -rf "$SEQ"; mkdir -p "$SEQ"
else u=$(($(date +%s)+5)); until [ -f "$SEQ/s$((slice-1)).done" ] || [ "$(date +%s)" -ge "$u" ]; do sleep 0.05; done; fi
command -v jq >/dev/null || exit 0
in=$(cat); [ "$(jq -r '.source//empty' <<<"$in")" = compact ] || exit 0
C=$(command -v csift||true); [ -x "$C" ] || C=$HOME/.cargo/bin/csift; [ -x "$C" ] || exit 0
sid=$(jq -r '.session_id//empty' <<<"$in"); [ -n "$sid" ] || exit 0
chunk=$("$C" verbatim "@$sid" --slices $N --window $WINDOW --slice "$slice" 2>/dev/null||true)
[ -n "$chunk" ] || exit 0
jq -n --arg c "Verbatim turns the compaction summary clipped (part $slice - a supplement; the summary still owns task state):
$chunk" '{hookSpecificOutput:{hookEventName:"SessionStart",additionalContext:$c}}'
```
Register N times: `{"matcher":"compact","hooks":[{"type":"command","command":"/ABS/csift-turns-slice.sh i"}]}`, i=1..N. Absolute path (global installs have no `$CLAUDE_PROJECT_DIR`); `--window 9000` stays under the 10K additionalContext cap.

### Hook 2 — PostToolUseFailure(TaskStop): redirect a failed teammate-kill
TaskStop can't stop a teammate (wrong tool, every id form rejected — a real session burned 30 min). On TaskStop FAILURE, confirm via csift that the id is a teammate, then inject the correct call. Fail-open.

```bash
#!/usr/bin/env bash
set -uo pipefail
in=$(cat)
command -v jq >/dev/null 2>&1 || exit 0
CSIFT=$(command -v csift 2>/dev/null||true); [ -x "$CSIFT" ]||CSIFT="$HOME/.cargo/bin/csift"; [ -x "$CSIFT" ]||exit 0
[ "$(jq -r '.tool_name//empty' <<<"$in" 2>/dev/null)" = TaskStop ] || exit 0
id=$(jq -r '.tool_input.task_id//.tool_input.shell_id//empty' <<<"$in" 2>/dev/null); [ -n "$id" ]||exit 0
sid=$(jq -r '.session_id//empty' <<<"$in" 2>/dev/null); [ -n "$sid" ]||exit 0
run(){ if command -v timeout >/dev/null 2>&1; then timeout 20 "$@"; elif command -v gtimeout >/dev/null 2>&1; then gtimeout 20 "$@"; else "$@"; fi; }
tm=$(run "$CSIFT" agents "@$sid" --shape teammate --format json 2>/dev/null)||exit 0; [ -n "$tm" ]||exit 0
m=$(printf '%s' "$tm" | jq -rs --arg id "$id" '[ .[]?|..|objects|select(.shape?=="teammate") ] as $t
  | ($id|split("@")[0]) as $b | ( $t[]|select(.name==$id or .agent_id==$id or .name==$b)|.name )' 2>/dev/null | head -n1)
[ -n "$m" ]||exit 0
ctx="TaskStop cannot terminate \"$id\" — csift confirms it is the teammate \"$m\" (in-process Agent subagent, no task_id / no separate PID). Use SendMessage: {\"to\":\"$m\",\"message\":{\"type\":\"shutdown_request\",\"reason\":\"<why>\"}}. A plain message only QUEUES until its current run ends; shutdown_request is the interrupt."
jq -n --arg c "$ctx" '{hookSpecificOutput:{hookEventName:"PostToolUseFailure",additionalContext:$c}}'
```
Register: `{"matcher":"TaskStop","hooks":[{"type":"command","command":"/ABS/taskstop-teammate-redirect.sh"}]}` under `PostToolUseFailure`.

### Hook 3 — Elicitation markers: backfill the sidecar csift merges
Fires when AUQ/ExitPlanMode/MCP elicitation OPENS and CLOSES; appends pending/resolved markers to the sidecar. MUST print nothing (observe only). Verified live: the pending marker lands the instant the picker appears. A REJECTION does NOT fire `PostToolUse` (verified on real data: every observed unpaired pending was a rejected plan/AUQ), so subscribe `PostToolUseFailure` too — belt-and-suspenders for whichever closure events CC emits; csift's ghost guard drops any still-unpaired stale pending against the native transcript regardless.

```bash
#!/usr/bin/env bash
set -uo pipefail
in=$(cat 2>/dev/null) || exit 0
command -v jq >/dev/null 2>&1 || exit 0
ev=$(jq -r '.hook_event_name//empty' <<<"$in" 2>/dev/null); tool=$(jq -r '.tool_name//empty' <<<"$in" 2>/dev/null)
kind=""; phase=""
case "$ev" in
  PreToolUse)  case "$tool" in AskUserQuestion|ExitPlanMode) kind="$tool"; phase="pending";; esac ;;
  PostToolUse|PostToolUseFailure) case "$tool" in AskUserQuestion|ExitPlanMode) kind="$tool"; phase="resolved";; esac ;;
  Elicitation)       kind="mcp-elicitation"; phase="pending" ;;
  ElicitationResult) kind="mcp-elicitation"; phase="resolved" ;;
esac
[ -n "$kind" ] || exit 0
tp=$(jq -r '.transcript_path//empty' <<<"$in" 2>/dev/null); sid=$(jq -r '.session_id//empty' <<<"$in" 2>/dev/null)
key=$(jq -r '.tool_use_id // .elicitation_id // .mcp_server_name // "unknown"' <<<"$in" 2>/dev/null)
srv=$(jq -r '.mcp_server_name//empty' <<<"$in" 2>/dev/null)
sidecar=""
if [ -n "$tp" ] && [ "${tp%.jsonl}" != "$tp" ]; then sidecar="${tp%.jsonl}/elicitations.jsonl"
elif [ -n "$sid" ]; then f=$(ls "${CLAUDE_CONFIG_DIR:-$HOME/.claude}"/projects/*/"$sid".jsonl 2>/dev/null|head -1); [ -n "$f" ] && sidecar="${f%.jsonl}/elicitations.jsonl"; fi
[ -n "$sidecar" ] || exit 0
mkdir -p "$(dirname "$sidecar")" 2>/dev/null || exit 0
ts=$(date -u +%Y-%m-%dT%H:%M:%S.000Z); uuid=$( (command -v uuidgen>/dev/null 2>&1 && uuidgen) || echo "csift-$$-$ts")
if [ "$phase" = resolved ]; then
  rec=$(jq -cn --arg k "$kind" --arg key "$key" --arg sid "$sid" --arg ts "$ts" --arg u "$uuid" \
    '{type:"csift-elicitation-resolved",uuid:$u,timestamp:$ts,sessionId:$sid,csift:"elicitation-marker-v1",csiftPhase:"resolved",csiftKind:$k,csiftKey:$key}' 2>/dev/null) || exit 0
elif [ "$kind" = mcp-elicitation ]; then
  msg=$(jq -r '.message//empty' <<<"$in" 2>/dev/null); mode=$(jq -r '.mode//"elicitation"' <<<"$in" 2>/dev/null)
  rec=$(jq -cn --arg key "$key" --arg sid "$sid" --arg ts "$ts" --arg u "$uuid" --arg srv "$srv" \
    --arg content "MCP elicitation [$srv] ($mode): $msg" --argjson hi "$in" \
    '{type:"system",subtype:"mcp_elicitation",uuid:$u,timestamp:$ts,sessionId:$sid,isSidechain:false,content:$content,csift:"elicitation-marker-v1",csiftPhase:"pending",csiftKind:"mcp-elicitation",csiftKey:$key,csiftMcpServer:$srv,hookInput:$hi}' 2>/dev/null) || exit 0
else
  rec=$(jq -cn --arg k "$kind" --arg key "$key" --arg sid "$sid" --arg ts "$ts" --arg u "$uuid" --argjson hi "$in" \
    '{type:"assistant",uuid:$u,timestamp:$ts,sessionId:$sid,isSidechain:false,message:{role:"assistant",stop_reason:"tool_use",content:[{type:"tool_use",id:$key,name:$k,input:($hi.tool_input//{})}]},csift:"elicitation-marker-v1",csiftPhase:"pending",csiftKind:$k,csiftKey:$key,csiftHookEvent:"PreToolUse",hookInput:$hi}' 2>/dev/null) || exit 0
fi
printf '%s\n' "$rec" >>"$sidecar" 2>/dev/null || exit 0
```
Register 5 events (one script, absolute path): `PreToolUse`+`PostToolUse`+`PostToolUseFailure` matcher `"AskUserQuestion|ExitPlanMode"`; `Elicitation`+`ElicitationResult` (no matcher).
