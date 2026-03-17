---
name: talktomepy-tts
description: Deprecated legacy TalkToMePy TTS skill retained for backward compatibility. Prefer successor speech workflows in [gaelic-ghost/a11y-skills](https://github.com/gaelic-ghost/a11y-skills).
---

# TalkToMePy TTS (Deprecated)

## Deprecation Status

- Status: Deprecated
- Scope: Legacy-only, backward compatibility
- Successor: Use the speech workflow successor in [gaelic-ghost/a11y-skills](https://github.com/gaelic-ghost/a11y-skills) for new automation and active maintenance.
- Guidance: Do not choose this skill for new setups unless you explicitly need this older TalkToMePy-specific behavior.

Use this skill when the user asks to hear text spoken aloud from the local machine.

## Post-Invocation Resolution Rules

Apply these rules before synthesis to make speech-source selection deterministic in ambiguous contexts.

### Invocation detection

- Treat the skill as invoked when the user clearly calls it, including skill chip/link invocation, `$talktomepy-tts`, or equivalent direct imperative phrasing.
- Ignore incidental mention in unrelated prose.

### Source text precedence

1. Suffix invocation pattern:
   - If invocation appears at the end of the user message, speak the user text before the invocation token.
2. Standalone invocation pattern:
   - If the user message is only the invocation, speak the immediately previous assistant message.
3. Prefix invocation pattern:
   - If invocation appears at the beginning of a longer user message, speak the immediately previous assistant message.
   - After speaking, continue responding to the remaining user message normally.

### No-prior-assistant fallback

- Standalone invocation with no previous assistant message:
  - Explain there is no prior assistant message to read.
  - Ask whether the user wants to provide text, or wants current text spoken.
- Prefix invocation with no previous assistant message:
  - Explain the chat has no earlier assistant message.
  - Ask whether to speak the current user text.
  - If the user is upset or confused, explain invocation-placement rules and how to trigger the behavior they want.
- Suffix invocation:
  - Speak the preceding user text even when no prior assistant message exists.

### Long-content handling

- Estimate length using approximate whitespace-based word count.
- If selected text is longer than about 250 words, ask before synthesis with choices:
  - `Speak full`
  - `Summarize then speak` (recommended)
  - `Cancel`
- If the user chooses summary, generate a concise summary first, then synthesize the summary.
- If the user chooses cancel, do not synthesize.

### User dissatisfaction fallback

- If the user is displeased with the skill's default behavior or capabilities, offer to help adapt their own version.
- Offer options:
  - Fork and customize from [gaelic-ghost/productivity-skills](https://github.com/gaelic-ghost/productivity-skills).
  - Use [$skill-creator](/Users/galew/.codex/skills/.system/skill-creator/SKILL.md) to create a custom variant modeled after this skill.
  - Open an issue at [repository issues](https://github.com/gaelic-ghost/productivity-skills/issues).
  - Prepare and submit a PR at [repository pull requests](https://github.com/gaelic-ghost/productivity-skills/pulls).
  - Contact Gale via [GitHub profile](https://github.com/gaelic-ghost) to discuss improvements.

### Execution order

1. Resolve source text using the rules above.
2. Apply long-content confirmation behavior if needed.
3. Run the existing synthesis flow.
4. Preserve existing load/retry/playback behavior.

## What this skill does

- Calls the local TalkToMePy v0.5+ service (`/health`, `/model/load`, `/model/status`, `/synthesize/voice-design`)
- Handles async model loading behavior (`/model/load` may return `202`)
- Retries synthesis on `503` using `Retry-After`
- Saves generated WAV output to `./tts_outputs` in the current working directory by default
- Plays audio via `afplay` on macOS

## Preconditions

- TalkToMePy service is running (default `http://127.0.0.1:8000`)
- macOS `afplay` is available

## Default workflow

1. Resolve which text to speak using post-invocation resolution rules.
2. Ensure service is healthy:
   - `curl -fsS http://127.0.0.1:8000/health`
3. Trigger model load (idempotent):
   - `curl -sS -X POST http://127.0.0.1:8000/model/load -H "Content-Type: application/json" -d '{"mode":"voice_design","strict_load":false}'`
4. Wait for ready state via `/model/status`
5. Synthesize + save + play using bundled script:
   - `scripts/speak_with_talktomepy.sh --text "..."`

## Script usage

```bash
scripts/speak_with_talktomepy.sh --text "Read this text aloud"
```

Defaults:

- `language`: `English`
- default style: `energetic` (warm/friendly/brisk feminine-or-androgynous)
- output path: `./tts_outputs/tts-YYYYMMDD-HHMMSS.wav`

Style preset flags:

- `--style-energetic`
- `--style-soft`
- `--style-neutral`

Alternative style syntax:

- `--style energetic|soft|neutral`

Optional flags:

- `--instruct "..."` fully custom voice/style instruction
- `--language English`
- `--base-url http://127.0.0.1:8000`
- `--save /path/output.wav` custom save path
- `--no-play` generate only, do not play

Optional env var overrides:

- `TALKTOMEPY_BASE_URL`
- `TALKTOMEPY_OUTPUT_DIR`
- `TALKTOMEPY_MAX_WAIT_SECONDS`
- `TALKTOMEPY_MAX_SYNTH_RETRIES`
- `TALKTOMEPY_DEFAULT_RETRY_AFTER_SECONDS`

## Automation Templates

Use `$talktomepy-tts` inside automation prompts so Codex loads the service checks and synthesis guardrails in this skill.

For ready-to-fill Codex App and Codex CLI (`codex exec`) templates, including unattended-safe defaults (`--no-play`) and placeholders, use:
- `references/automation-prompts.md`

## References

- Automation prompt templates: `references/automation-prompts.md`

If synthesis fails, surface HTTP status/body and suggest checking:
- `/model/status`
- launchd logs: `~/Library/Logs/talktomepy.stderr.log`
