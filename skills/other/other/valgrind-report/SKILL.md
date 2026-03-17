---
name: valgrind-summarizer
description: Summarize Valgrind Memcheck reports into concise Markdown. Use when the user uploads or references a Valgrind log file (.txt, .log, .valgrind) and wants a summary, analysis, or overview of memory leaks and errors. Triggers on mentions of "valgrind", "memcheck", "leak check", "memory leak report", or when the uploaded file contains Valgrind Memcheck output (identifiable by "==PID==" prefixed lines, "HEAP SUMMARY", "LEAK SUMMARY").
---

# Valgrind Report Summarizer

Produce a minimal-token Markdown summary of Valgrind Memcheck reports by running the bundled parser script.

## Workflow

1. Identify the valgrind log file (uploaded or at a given path).
   - If no log file exists yet and the user wants to run Valgrind, build with debug symbols first:
     ```bash
     cd python && MSCOMPRESS_DEBUG=1 uv sync --all-extras --reinstall
     ```
     Then run Valgrind:
     ```bash
     cd python && valgrind --tool=memcheck --leak-check=full --log-file=leak-check.txt $(uv run which python) -m pytest
     ```
2. Run the parser:
   ```bash
   python3 /path/to/this/skill/scripts/parse_valgrind.py <input_file> <output.md>
   ```
3. Deliver the resulting `.md` file to the user.

## What the Script Produces

- **Heap Overview** — exit usage, total allocated, alloc/free delta
- **Leak Summary** — table with definitely/indirectly/possibly lost, still reachable, suppressed (with severity icons)
- **Top 15 Leak Sources** — grouped & deduplicated by call stack, sorted by bytes, showing only user-code frames (runtime/valgrind internals stripped)

## Notes

- The parser strips `==PID==` / `--PID--` prefixes automatically.
- Stack frames from valgrind preload, libpython, CPython eval loop, pthread, and clone are filtered out to surface only the user's own code.
- Duplicate stacks (same top-4 frames) are merged with a `×N` count.
- Byte values are human-readable (KB/MB/GB).
- If the user wants deeper analysis or remediation advice beyond the summary, read the generated markdown and provide commentary.