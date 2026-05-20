---
name: rlm
description: Run a Recursive Language Model-style loop for long-context tasks. Uses a persistent local Python REPL and an rlm-subcall subagent as the sub-LLM (llm_query).
allowed-tools:
  - Read
  - Write
  - Edit
  - Grep
  - Glob
  - Bash
---

# rlm (Recursive Language Model workflow)

Use this Skill when:
- The user provides (or references) a very large context file (docs, logs, transcripts, scraped webpages) that won't fit comfortably in chat context.
- You need to iteratively inspect, search, chunk, and extract information from that context.
- You can delegate chunk-level analysis to a subagent.

## Mental model

- Main Claude Code conversation = the root LM.
- Persistent Python REPL (`rlm_repl.py`) = the external environment.
- Subagent `rlm-subcall` = the sub-LM used like `llm_query`.

## How to run

### Inputs

This Skill reads `$ARGUMENTS`. Accept these patterns:
- `context=<path>` (required): path to the file containing the large context.
- `query=<question>` (required): what the user wants.
- Optional: `chunk_chars=<int>` (default ~200000) and `overlap_chars=<int>` (default 0).

If the user didn't supply arguments, ask for:
1) the context file path, and
2) the query.

### Step-by-step procedure

1. Initialise the REPL state
   ```bash
   python3 .claude/skills/rlm/scripts/rlm_repl.py init <context_path>
   python3 .claude/skills/rlm/scripts/rlm_repl.py status
   ```

2. Scout the context quickly
   ```bash
   python3 .claude/skills/rlm/scripts/rlm_repl.py exec -c "print(peek(0, 3000))"
   python3 .claude/skills/rlm/scripts/rlm_repl.py exec -c "print(peek(len(content)-3000, len(content)))"
   ```

3. Choose a chunking strategy
   - Prefer semantic chunking if the format is clear (markdown headings, JSON objects, log timestamps).
   - Otherwise, chunk by characters (size around chunk_chars, optional overlap).

4. Materialise chunks as files (so subagents can read them)
   ```bash
   python3 .claude/skills/rlm/scripts/rlm_repl.py exec <<'PY'
   paths = write_chunks('.claude/rlm_state/chunks', size=200000, overlap=0)
   print(len(paths))
   print(paths[:5])
   PY
   ```

5. Subcall loop (delegate to rlm-subcall)
   - For each chunk file, invoke the rlm-subcall subagent with:
     - the user query,
     - the chunk file path,
     - and any specific extraction instructions.
   - Keep subagent outputs compact and structured (JSON preferred).
   - Append each subagent result to buffers (either manually in chat, or by pasting into a REPL add_buffer(...) call).

6. Synthesis
   - Once enough evidence is collected, synthesise the final answer in the main conversation.
   - Optionally ask rlm-subcall once more to merge the collected buffers into a coherent draft.

## Guardrails

- Do not paste large raw chunks into the main chat context.
- Use the REPL to locate exact excerpts; quote only what you need.
- Subagents cannot spawn other subagents. Any orchestration stays in the main conversation.
- Keep scratch/state files under .claude/rlm_state/.
