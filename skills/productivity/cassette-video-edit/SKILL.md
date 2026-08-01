---
name: cassette-video-edit
description: Orchestrate gateway media and natural-language editing instructions into complete Cassette editing jobs through the plugin's API transport, with timeline grounding, plan relay, and live editor links.
version: 3.0.0
metadata:
  hermes:
    tags: [cassette, video, gateway, qqbot, telegram, media]
    category: automation
    requires_toolsets: [cassette]
---
# Cassette Video Edit Workflow

## When to Use

Use this skill when a gateway user, including QQ or Telegram, asks Hermes to edit, cut, caption, reframe, remix, subtitle, combine, polish, export, or otherwise transform video/image/audio media through Cassette. Weixin/WeChat remains a legacy compatible path; QQ and Telegram are the primary supported gateway targets.

Also use it when the user sends media first and later gives an editing instruction, or gives an instruction first and then uploads required assets. The goal is to make Cassette continue working with a complete prompt rather than stopping for routine clarification.

Use Cassette as the only editing engine. Do not fall back to local FFmpeg, terminal scripts, or any other non-Cassette editing path unless the user explicitly cancels Cassette and asks for a different tool.

Hermes is not the creative video-analysis engine. For editing requests, Hermes must not inspect, describe, understand, extract frames from, probe, or analyze the source media itself. Do not use `terminal`, `ffprobe`, `ffmpeg`, `vision_analyze`, Python scripts, or other non-Cassette tools to decide filters, poems, captions, music, timing, or visual treatment. Relay the user's intent to Cassette and let Cassette analyze the uploaded media.

## Working surface

The plugin talks to the Cassette server APIs directly (media upload, agent run, project reads, export) — there is no browser to supervise. The sources of truth, in order:

1. **Structured job state** — `cassette_run_job` / `cassette_job_status` results: `status`, `questions`, `report`, `timeline_delta`, `plan_progress`, `quality`.
2. **The timeline digest** — `cassette_timeline` returns the live project as bounded text (CTL) with a version number. Every user-visible statement about project state comes from this tool, never from memory. Name the version when reporting: "v42 → v43: trimmed the intro to 4.0s."
3. **The live editor link** — jobs carry `editor_url`, a tap-to-open live view of the real editor (timeline, scrubbing preview, plan card; zero render). The plugin notifier includes it in gateway messages automatically; when you compose your own reply at job start or at a question, include it once as "Watch live". Do not repeat it in every message.

## Procedure

1. Ingest incoming media immediately with `cassette_ingest_media`. If the turn contains only media or a gateway placeholder such as `[Attachment: ...]` / `[Voice] ...`, save the assets and wait for a later editing instruction instead of starting Cassette.
2. Inspect the manifest with `cassette_list_assets` when needed.
3. Interpret editing intent semantically (edit vs ordinary chat). That is your ONLY routing decision — there are no upfront questions about model, thinking level, prompt optimization, or BGM.
4. For an edit instruction, call `cassette_run_job` with `message` set to the user's words EXACTLY as written — never rewrite, optimize, summarize, translate, or expand them — plus the gateway session_id and the session language (QQ defaults to `cassette_language="zh"`, Telegram to `"en"`, `/cassette language zh|en` overrides). Do not call `cassette_make_prompt`. For QQ, Telegram, or Weixin gateway sessions use `wait=false` so `/cut` stays responsive; the plugin notifier sends progress and final notifications itself.
5. One gateway session is ONE continuous conversation with the Cassette agent on one persistent thread: follow-ups like "把那个标题改大一点" need no context restating, and the "Watch live" link stays the same for the whole session.
6. A turn ends with the edit committed and NOTHING rendered. The plugin notification carries the timeline delta, a contact-sheet preview image, and the live link — that is the per-turn preview. When the user expresses finish/export intent, pass `export=true` on that turn; it then routes through completion review before rendering.
7. Explicit opt-ins the user can invoke: `/refine <instruction>` optimizes the instruction into a professional brief (policy in `prompts/hermes-edit-brief-optimizer.md`) and asks for confirmation before running; `/music <BGM requirement>` recommends exactly 3 concrete real songs (plus option 4 "换一批" and option 5 "随机匹配") and only registers a BGM asset; `/cassette_model` changes the saved model/thinking preference via a numbered picker over the static product list.
8. Handle Cassette follow-up questions with `cassette_answer_question` (see "Questions and plan review" below).
9. For local/manual non-gateway runs, report progress by summarizing `report.current_stage`, `plan_progress`, and `timeline_delta`. For gateway background jobs, stop after the start acknowledgement and let the plugin notifier send progress and final notifications. Keep updates short and never expose local paths, prompt text, or raw identifiers.
10. On an export turn with completion review pending, judge the result from the structured review context (see "Completion review"), then call `cassette_review_completion` with `decision="export"`, `"continue"`, `"failed"`, or `"needs_user"`.
11. If the user sends `/cut` or `/cassette cut`, let the plugin handle it as a gateway command: it cancels the active Cassette job and preserves session state for the next instruction.

## Model and thinking level

- The session model preference is set via `/cassette_model` (numbered picker) or `cassette_config`; it persists for the gateway session and applies from the next turn. Defaults (DeepSeek V4 Flash, low thinking) match the web editor.
- Never ask about the model upfront and never override it from ordinary editing text.

## Lane routing

- **Brief lane (default)** — anything that needs watching footage, music sync, creative judgment, or a multi-step plan goes through `cassette_run_job`. This is the Cassette agent's job, not yours.
- **Direct lane (when enabled)** — when `CASSETTE_DIRECT_EDIT=1` and the ask names specific clips or values needing at most a handful of operations ("trim the intro to 4 seconds", "delete the whoosh sound", "undo that"), read `cassette_timeline` first, then call `cassette_edit` with the matching tool and `expected_version` from the read. A `stale_timeline` error means the project moved: re-read and retry. A `job_active` error means a run holds the session: wait or cancel first. Report direct edits with their version step and the returned delta.
- Never mix lanes blindly: while a job is running or waiting on a question, the direct lane refuses; relay the job flow instead.

## Questions and plan review

`cassette_run_job` / `cassette_job_status` return `needs_user` with typed questions:

- `reason: "edit_plan_review"` — the question text IS the edit plan (with the current timeline summary; storyboard beats appear as readable cells, and the gateway push includes a storyboard-sheet image of one source frame per planned beat). Relay it to the user verbatim with the live link, and map their reply onto `cassette_answer_question`: `approve`, `revise <their feedback>`, or `reject`. Free-text change requests count as revise feedback. Note: gateway sessions default to `CASSETTE_PLAN_REVIEW=auto` (plans auto-approve to keep unattended jobs moving); this flow applies when the operator enabled `user` mode.
- `reason: "explicit_user_choice_required"` or `"missing_required_asset"` — genuine questions: relay the question and its numbered choices, send the user's answer back via `cassette_answer_question`.
- A `resume_not_waiting_for_user` error on answering means the user already decided in the open editor tab — first answer wins. Call `cassette_job_status` once and continue from the returned state.
- Routine ambiguities are auto-answered by the plugin with safe defaults; their audit entries appear in `questions` with `requires_user: false`. Do not re-ask them.

## Completion review

When `cassette_run_job` returns `needs_user` with `completion_requires_hermes_review`, Hermes is the supervisor deciding export. Judge from the structured review context the plugin attaches:

- `quality.timeline_ctl` — the timeline digest of what would be exported.
- `quality.contact_sheet` — a tiled poster image (source frames, not composed output); for gateway users the notifier pushes it as a chat image automatically.
- `quality.progress_summary` — the agent's own completion summary.
- The `editor_url` live view, for the user's own judgment.

Export only when the evidence says the edit is complete enough to export. Do not treat a single keyword in the agent's summary as proof either way. If the timeline is empty or obviously wrong, use `decision="continue"` with feedback or `"needs_user"`.

## Hard Rules

- Cassette is the only allowed editing engine. Never use local FFmpeg, terminal media commands, Python media processing, or other workarounds to create the edited video.
- Send only the user-facing editing request to Cassette. Never send the Hermes/internal prompt template, tool instructions, manifest details, policy text, local paths, or automation notes.
- Every user-visible statement about project state comes from `cassette_timeline` or the structured job fields, never from memory or guesswork.
- Do not say "I will look at/watch/analyze the video" for a Cassette edit. The correct response is to start the Cassette tool flow and report Cassette progress.
- Do not start a Cassette job from a media-only gateway turn. Save all media first; start the job only after a later user message provides an actual editing instruction.
- Do not alter explicit user requirements when optimizing the editing brief. If the user states a product name, price, duration, aspect ratio, caption text, layout constraint, style, order, or exclusion, preserve it. Improve only unspecified details.
- Never rewrite the user's editing message. `message` on `cassette_run_job` is the user's words verbatim; `/refine <instruction>` is the only path that optimizes an instruction, and `/music <BGM requirement>` only adds a smart-matched BGM asset without starting Cassette.
- `/check_assets` is the only gateway command for reporting how many assets have been saved in the current session. Do not treat natural-language receive/status complaints as asset-check requests.
- `/cassette_model` changes the saved Cassette model/thinking preference for the current gateway session via numbered choices over the static product list; do not route those number replies through BGM selection or editing.
- `/cut` and `/cassette cut` are pause commands, not new editing instructions. Do not route them through prompt optimization, smart BGM, `cassette_make_prompt`, or a fresh `cassette_run_job`.
- `/cassette language zh|en` sets the Cassette UI/reply language for the current gateway session. Do not treat it as an editing instruction, prompt-optimization reply, BGM reply, or confirmation.
- Smart BGM runs only from `/music`. When it runs, first recommend exactly 3 concrete real songs with title plus artist/singer, followed by option 4 "换一批" and option 5 "随机匹配"; tell the user they can reply 1-5 or send text to add BGM requirements and receive a new batch. Do not call any BGM tool before the user chooses. If the user selects 1-3, call `cassette_match_exact_bgm` with the selected title and artist. If the user selects 4, provide a new batch and avoid repeating previous recommendations. If the user sends non-number text, treat it as additional BGM requirements and recommend a new batch. If the user selects 5, follow the plugin-selected random provider order. If exact song search fails, fall back without asking again: use `jamendo_music_matcher` when configured, then Free To Use `cassette_match_bgm`. Never generate or print raw Jamendo SearchPlan JSON in assistant content.
- Keep using the gateway-provided cassette `session_id` from the user/system context when calling `cassette_list_assets`, `cassette_run_job`, `cassette_timeline`, `cassette_edit`, and `cassette_config`. Do not replace it with `manifest.session_id`, `manifest.session_hash`, or `manifest_path` from a tool result.
- Scrubbed tool results intentionally hide `local_path`; exported files live under `${CASSETTE_ASSET_ROOT}/exports/<job_id>/`, and gateway delivery is handled by the plugin notification path. Do not invent a local export path from a filename.
- Do not emit `MEDIA:` for exported Cassette videos in gateway replies, including guessed paths. The plugin notification sends the exported artifact when a supported delivery target is available; if `notification.status` is `partial` or `failed`, tell the user the plugin could not deliver the attachment instead of retrying the same mp4 path through gateway media routing.
- Telegram Bot API uploads are limited to 50 MB for videos/files. Do not manually compress and resend Cassette exports from Hermes; the plugin notifier converts oversize exports into a compressed preview automatically and states where the original is saved.
- Do not expose local paths, raw wxids/openids, tokens, or the full prompt in user-facing replies.
- Do not over-ask the user for stylistic choices.

## Diagnostics

When `cassette_run_job` returns `timed_out` or an unclear state, diagnose from the structured record — there is no browser to inspect:

1. Read the scrubbed job result: `status`, error codes, `report.current_stage`, `report.stage_timings`, latest `progress_events`, `timeline_delta`, and `final_screenshot`/export thumbnail if present.
2. Call `cassette_timeline` for the session: a populated timeline with a recent version means Cassette created an edit but completion/export was not confirmed — report it as such ("timeline has N clips at v42; export not confirmed"), not as total failure.
3. If a follow-up question is pending, classify and answer it via `cassette_answer_question` when safe.
4. Give the user the `editor_url` link so they can see the live state themselves.
5. Do not inspect or manipulate media locally to "finish" the edit. Local filesystem checks are only for validating job metadata and exported artifacts produced by Cassette.

## Progress Updates

For gateway users, let the plugin notifier own progress and final summaries instead of keeping Hermes in a polling loop:

- After job creation: tell the user the Cassette job has started, include the "Watch live" link once, and say progress/final notifications will arrive automatically.
- During work: do not call `cassette_job_status` repeatedly in the same Hermes turn. The plugin folds live commit events into `timeline_delta` and pushes progress through the stored delivery target.
- Explicit status requests: if the user asks for status, call `cassette_job_status` once and summarize `report.current_stage`, `plan_progress`, and `timeline_delta`; then end the turn.
- On timeout: summarize what Cassette visibly accomplished (via `cassette_timeline`) and what is still pending.
- On completion: summarize changes and mention the plugin notification result. Do not add an extra `MEDIA:` tag; detached jobs may also send this final summary directly using the stored delivery target.
