# Discovery Rubric

Use this rubric to mine agent usage history for new skill candidates.

## 1. Evidence Sources

Scan only sources that exist and are relevant:

| Source | Typical Path | What To Extract |
| --- | --- | --- |
| Codex sessions | `~/.codex/sessions/**/*.jsonl` | User asks, tool patterns, repeated fixes, verification habits. |
| Codex archived sessions | `~/.codex/archived_sessions/*.jsonl` | Older user asks and tool patterns that are no longer in the active session tree. |
| Codex rollout summaries | `~/.codex/memories/rollout_summaries/` | Compressed memories, durable learnings, and older workflow names. |
| Claude Code sessions | `~/.claude/projects/**/*.jsonl` | Tool calls, skill usage, rejected workflows, recurring commands. |
| Claude Code sessions archive | `~/.claude/sessions/**/*.jsonl` | Additional Claude Code transcript stores when present. |
| Gemini / Antigravity | `~/.gemini/` | Task files, walkthroughs, implementation plans, exported chats. |
| Exported transcripts | User-provided `.json`, `.jsonl`, `.md`, `.txt` | Cursor, OpenCode, Gemini, or other agent history exports. |
| Shared memories | `~/.agents/memories/` or `~/.codex/memories/` | Stable preferences, repeated domains, prior run summaries. |
| Project notes | `AGENTS.md`, `CLAUDE.md`, docs, runbooks | Workflows already documented locally. |
| Scripts | repo `scripts/`, `bin/`, local utilities | Repeated operations that may need a skill wrapper. |

Prefer summaries and metadata first. Open raw transcripts only when needed to confirm recurrence or extract trigger examples.

For a first pass, run:

```bash
python3 scripts/scan_sessions.py --days 30 --limit 300 --min-count 3
```

For agents without a stable native history format, pass exported files:

```bash
python3 scripts/scan_sessions.py --export ~/Downloads/cursor-chat-export.json --export ./opencode-transcripts/
```

Workflow candidates are driven by `references/patterns.json`. For personal use, edit or replace that file with local workflow names and trigger regexes:

```bash
python3 scripts/scan_sessions.py --patterns ./my-patterns.json
```

The scanner emits sanitized clusters. Review the result manually before creating skills because command-only turns, automations, pasted logs, and multi-topic sessions can still create noisy clusters. Treat rollout summaries as compressed memory evidence, not raw transcript evidence; use them to discover candidates, then confirm with raw examples when possible.

Before accepting any workflow candidate, manually inspect at least five positive examples and three near-miss examples. If a pattern is catching broad words such as `build`, `host`, `微信`, `design`, or `service`, tighten it before drafting a skill.

## 2. Candidate Signals

Strong candidates usually have several of these:

- The user has asked for the same kind of work at least three times.
- The workflow requires non-obvious sequencing or local judgment.
- Agents often miss a step, ask unnecessary questions, or stop before verification.
- The task crosses tools, repos, remote hosts, browsers, or document formats.
- There is a repeated safety rule, privacy boundary, or deployment distinction.
- The user corrected an agent in a way future agents should remember.

Weak candidates:

- Generic coding concepts already handled by the base model.
- One-off project facts.
- Mechanical checks better implemented as scripts or tests.
- Secrets, private data extraction, or workflows that should not be automated.

## 3. Clustering Dimensions

Group similar turns by:

- Intent: review, debug, publish, deploy, summarize, install, sync, research.
- Natural trigger phrasing: the user's actual short phrases and shorthand.
- Artifacts: files, repos, URLs, hosts, documents, screenshots, PRs.
- Tool chain: shell, GitHub, browser, SSH, Lark, PDF, spreadsheets.
- Completion pattern: what "done" looked like in successful sessions.
- Failure pattern: where agents usually got stuck or drifted.

## 4. Candidate Score

Use a simple 1-5 score:

| Score | Meaning |
| --- | --- |
| 5 | Repeated, high-value, non-obvious, and future agents are likely to mishandle it without a skill. |
| 4 | Repeated and useful, with clear triggers and validation steps. |
| 3 | Plausible, but needs more evidence or narrower scope. |
| 2 | Mostly project-specific or better as documentation. |
| 1 | Do not create; generic, risky, or one-off. |

Recommend creating skills for scores 4-5. Put score-3 items in a backlog. Skip scores 1-2.

## 5. Candidate Output

For each candidate, provide:

- Proposed skill name.
- Personal or public direction.
- Evidence count and representative sanitized examples.
- Trigger description draft.
- Core workflow bullets.
- Bundled resources needed, if any.
- Validation prompts: direct trigger, natural shorthand, and neighbor task.
- Risks or privacy notes.

Do not create skills directly from broad intent clusters such as `debug`, `frontend`, or `publish`. Use those clusters as navigation hints, then create skills only from narrower workflow candidates or manually confirmed repeated workflows.

For each selected workflow candidate, simulate the next two lifecycle steps before writing files:

- Personalization: what local paths, commands, preferences, and validation habits would this skill need?
- Generalization: which of those details must be removed or parameterized before publication?

## 6. Creation Rules

When creating selected candidates:

- Start with one small `SKILL.md`.
- Keep frontmatter to `name` and `description`.
- Use the user's real phrasing in trigger conditions for personal skills.
- Move long examples, schemas, and scripts into bundled resources.
- Validate that the new skill would trigger on the evidence examples and stay silent on neighbor tasks.
- If the candidate needs deterministic counting, parsing, export conversion, or privacy redaction, create a script instead of relying on prose alone.
