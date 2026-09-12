---
name: summarize
description: |
  Summarize any block of text using the `summarize` CLI (chained-in from steipete/summarize — npm package `@steipete/summarize`). Use whenever the user pastes a long piece of content and asks for a TL;DR, a summary, a digest, a gist, a condensed version, or key points — even if they don't explicitly say "use summarize". Also chains into `mktg-transcribe --summarize` for audio/video TL;DRs and source-digestion workflows to condense long articles. Requires the `summarize` CLI to be installed (`mktg doctor` will tell you if it's missing). Do NOT trigger for structured data (JSON/CSV/code), for text already shorter than ~500 words, or when the user wants the full content preserved.
argument-hint: "[text-file-path OR stdin OR pasted text]"
allowed-tools:
  - Bash(summarize *)
  - Bash(npx @steipete/summarize *)
---

# /summarize — text → TL;DR via steipete/summarize

You are summarizing arbitrary text using the `summarize` CLI from github.com/steipete/summarize (npm: `@steipete/summarize`). This skill is a **chain-in wrapper** — mktg does not fork or vendor the tool; it orchestrates it when the user has it installed.

## On Activation

1. **Preflight:** Run `summarize --version` via the Bash tool.
   - If the command is not found, print the short install hint below and stop. Offer to walk the user through [rules/install.md](rules/install.md) if they want the long version.
     ```
     summarize CLI not installed. Quickest path:
       npm i -g @steipete/summarize   (requires Node 22+)
       brew install summarize         (macOS)
     Then rerun. Full install guide: skills/summarize/rules/install.md
     ```
   - If it prints a version, continue.
2. **Read `brand/voice-profile.md` if it exists.** At L1+ you should quietly align the TL;DR's *voice* to the brand (tone, energy, diction). At L0 (no brand memory), just produce a neutral summary — do not invent voice.
3. **Resolve the input.** Accept any of:
   - A **file path**: pass it directly to summarize (e.g. `summarize /tmp/article.md --length short --plain`)
   - **Stdin / pasted text**: pipe through `-` (e.g. `cat /tmp/article.md | summarize - --length short --plain`)
   - **Inline argument text**: write to a scratch file in `.summarize/` first, then pass the path — do not shell-interpolate large blobs of text
4. **Short-circuit check.** If the input is clearly under ~500 words (or under ~3,000 characters), do **not** run summarize. Return the content as-is and tell the user it was already short enough. Running summarize on tiny inputs wastes latency and the upstream CLI itself returns short content as-is by default unless `--force-summary` is set.
5. **Run summarize.** Prefer structured output for agent consumption:
   ```bash
   summarize <input> --length <preset> --plain --json
   ```
   - `--length short|medium|long|xl|xxl` — pick one based on the caller's ask (default: `medium`)
   - `--plain` — raw output, no ANSI/OSC markdown rendering (agents want plain text)
   - `--json` — machine-readable envelope with the summary, metrics, and prompt (only when the caller needs metadata; omit for simple TL;DRs)
   - `--no-color` — belt-and-suspenders if you're capturing stdout
   - `--timeout 2m` — keep the default unless you know the input is huge
6. **Capture and return structured output.** The skill's contract with callers:
   ```
   {
     "summary": "<the condensed text>",
     "input_chars": <int>,
     "output_chars": <int>,
     "compression_ratio": <float>,
     "length_preset": "<short|medium|long|xl|xxl>",
     "source": "<path or 'stdin'>"
   }
   ```
7. **Never dump huge outputs into context.** Write long outputs to `.summarize/<slug>.md` and return a path + head. Agents should treat the scratch dir like firecrawl's `.firecrawl/` — gitignored, isolated, cleaned on demand.

## How summarize works

`@steipete/summarize` is a Node-22+ CLI that takes a URL, file, or stdin and returns a condensed version rendered as streaming Markdown (or raw JSON when `--json` is set). Under the hood it routes text through an LLM backend — by default `auto` picks the best available provider (cloud key, local endpoint, or a chained coding CLI like Claude/Codex/Gemini/OpenCode). When only offline coding CLIs are available, it falls back to them automatically.

For Pillar 3 (this skill) mktg uses only the **text → summary** surface of the tool. The upstream CLI can also fetch URLs, transcribe YouTube videos, extract PDFs, and run OCR on video slides — but **those jobs belong to other pillars in mktg**:

- URL fetching → `firecrawl` skill
- YouTube / podcast / TikTok / audio transcription → `mktg-transcribe`
- X/Twitter reading → `mktg-x`

summarize's role inside mktg is narrower: **take text that another pillar already extracted, return a shorter version**. Keeping the role small keeps the chain-in surface predictable and prevents overlap with mktg's first-class capabilities.

Upstream repo: https://github.com/steipete/summarize
NPM package: `@steipete/summarize`
Author: Peter Steinberger (@steipete)
License: see upstream (chain-in, not vendored)

## Usage patterns

### Pattern A — summarize a local article/markdown file

```bash
summarize /path/to/article.md --length short --plain
```

Use when a source-digestion workflow has scraped a long blog post via firecrawl and the source extractor wants a TL;DR to attach to the grounding memo alongside the full extract.

### Pattern B — summarize stdin (pasted text, piped output)

```bash
cat /tmp/transcript.txt | summarize - --length medium --plain
pbpaste | summarize - --length short --plain
```

Use for ad-hoc "the user pasted a giant blob, condense it" requests. Remember: stdin has a 50MB cap upstream, and whitespace-only input is rejected.

### Pattern C — chain-in from mktg-transcribe

```bash
mktg transcribe "https://youtu.be/<id>" --json \
  | jq -r .data.transcript \
  | summarize - --length medium --plain \
  > .summarize/youtube-<id>-tldr.md
```

This is the `mktg-transcribe --summarize` flow. Transcribe pipes the transcript text, summarize compresses it, the result is a one-page TL;DR attached to the grounding memo.

### Pattern D — JSON envelope for agent consumption

```bash
summarize /tmp/long-article.md --length short --plain --json \
  > .summarize/article-summary.json
```

When a source-digestion workflow needs the summary plus metrics (input char count, model used, latency) for telemetry or caching, prefer `--json`. Parse `.summary`, `.metrics`, and `.prompt` fields downstream.

### Pattern E — preset selection cheat sheet

| Caller intent | `--length` | Why |
|---|---|---|
| "one-sentence gist" | `short` | ~900 char target, fast |
| "executive summary" | `medium` | ~1,800 char target, default |
| "detailed digest" | `long` | ~4,200 char target |
| "thorough condensation" | `xl` | ~9,000 char target |
| "near-full summary" | `xxl` | ~17,000 char target |
| "I need exactly N chars" | numeric (`--length 2500`) | character target, >= 50 |

## Chain-in role in the mktg multimedia digestion system

This skill is Pillar 3 of the four-pillar digestion system (see `docs/plans/2026-04-11-002-feat-mktg-multimedia-digestion-plan.md`). Its job is **text compression**, not source ingestion.

**Who calls summarize:**

- **`mktg-transcribe`** — optionally pipes its transcript output through summarize when `--summarize` is passed. This is how video source digestion produces both a full transcript and a TL;DR in a single agent hop.
- **Source extractors** — when a firecrawl-scraped article is long and the grounding memo would overflow, the source extractor summarizes the extract and attaches both.
- **Any skill producing long-form text** — `seo-content`, `newsletter`, `direct-response-copy` outputs can be summarized for preview cards, hooks, or social atomization.

**Who does NOT call summarize:**

- Anything dealing with structured data (JSON/CSV/code) — summarize is tuned for prose, not data schemas.
- Skills that need the full content preserved (brand memory, legal-critical docs, verbatim quotes).
- Short-input skills where the LLM round-trip isn't worth the latency.

**Default posture:** summarize is an *enhancement*, not a gate. If it's missing, the calling skill still ships the full content — just without a TL;DR. Progressive enhancement applies here the same way brand memory does.

## Anti-Patterns

1. **Running summarize on structured data.** JSON, CSV, code, SQL — don't. **Why:** the tool is tuned for prose. Structured data loses its schema semantics through an LLM condenser and the output is unreliable. If the user wants "the gist of this JSON", explain what the data represents in natural language yourself; don't route it through summarize.

2. **Summarizing already-short text.** If input is under ~500 words (~3,000 chars), skip the call entirely. **Why:** adds latency and cost with no value. Upstream summarize itself returns short content as-is by default. Be honest with the user: "this is already a short read, no TL;DR needed."

3. **Mandating summarization for every long text.** Never default-summarize a skill's output. Offer it as an option. **Why:** many skills want the full content — brand extraction, legal copy, launch memos. Silently truncating them via summarize corrupts the downstream pipeline. Let the caller explicitly ask for a TL;DR.

4. **Forgetting attribution.** summarize is a third-party tool maintained by @steipete. **Why:** mktg ships as a curation layer. When we chain in external tools we credit them so maintainers get recognition and users can upstream issues correctly. Every reference to summarize in generated content must link back to https://github.com/steipete/summarize.

5. **Dumping huge `--json` outputs directly into agent context.** Write to `.summarize/<slug>.json` and return head/tail slices. **Why:** a single summarize `--json` call can easily exceed 10KB of metrics + prompt + summary. Pouring that into an agent's context burns tokens and masks the actual TL;DR. Treat it like firecrawl output: file-based isolation, incremental reads.

6. **Using summarize as a URL fetcher even though it technically can.** Upstream summarize accepts URLs, YouTube, podcasts, and PDFs directly. **Why:** mktg reserves ingestion for its own pillars (firecrawl, mktg-transcribe, mktg-x) so the digestion matrix has exactly one owner per source type. Letting summarize also fetch URLs creates two sources of truth for "who scraped this blog" and breaks source-type routing. Scope this skill to text-in → text-out.

7. **Skipping the install preflight.** Always run `summarize --version` first. **Why:** the tool is an *optional* chain-in. Silent failures ("the summary never came back") are worse than a clear "not installed, here's how to install" message. `mktg doctor` will also flag it, but the skill itself should fail fast.

## References

- [rules/install.md](rules/install.md) — how to install `@steipete/summarize`, verify the binary, and handle install failures on macOS/Linux/WSL.
- [rules/usage.md](rules/usage.md) — idiomatic usage patterns, flag combinations, output shapes, and when to prefer summarize over direct LLM summarization.

## Attribution

**Source:** https://github.com/steipete/summarize
**NPM package:** `@steipete/summarize`
**Homepage:** https://summarize.sh
**Author:** Peter Steinberger ([@steipete](https://github.com/steipete))
**Type:** CLI tool (Node 22+)
**License:** see upstream (`repos/steipete/summarize` — "Other" per GitHub; check upstream LICENSE file)
**Relationship to mktg:** chained-in (upstream-only — mktg does not fork or vendor the code; users install `@steipete/summarize` separately and mktg orchestrates it)
**Date wrapped:** 2026-04-11
**Wrapped by:** mktg source-digestion workflows, Pillar 3 of the multimedia digestion plan
**Plan reference:** `docs/plans/2026-04-11-002-feat-mktg-multimedia-digestion-plan.md`
