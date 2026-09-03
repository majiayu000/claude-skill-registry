---
name: session-stats
description: "Render a dashboard of the current Claude Code session — message counts, token usage, cache read/write, dollar cost, context %, lines changed, cost-per-turn sparkline, and a tool-call histogram — parsed from the session transcript JSONL by a bundled bash script. One bash call, zero analysis, zero confirmation. Optionally pass a session id to inspect a different session. Use when the user asks for session stats, usage, token or cost breakdown, or a session dashboard."
model: inherit
color: green
---

# Session-Stats

One bash call, then relay. The bundled script finds the transcript at
`~/.claude/projects/*/<session-id>.jsonl` (current id comes from
`CLAUDE_CODE_SESSION_ID` in the bash environment), aggregates it with `jq`,
and prints the dashboard. All numbers come from the script — compute nothing
yourself.

## Steps

1. Run — pass a session id only if the user named one, otherwise no args:

```bash
bash {base_directory}/dashboard.sh [session-id]
```

2. Print the script's stdout verbatim inside a ```text code fence. After the
   fence, add at most one sentence — or nothing.

3. Non-zero exit → print stderr verbatim and stop. No retries, no fallback
   parsing.

## Notes

- The transcript schema is internal to Claude Code; the script degrades to
  `—` for fields it can't find. Never "fill in" missing values by reading
  the JSONL yourself.
- For a colored render, the user can run the script directly:
  `! bash {base_directory}/dashboard.sh --color`

## You Must NOT

- Parse the JSONL or cost sidecar yourself, or run any git/jq command
- Summarize, interpret, reformat, or annotate the dashboard beyond one sentence
- Ask questions — this skill has no interactive path
