---
name: capture-lessons
description: Summarize the current conversation and implementation into a durable lessons note saved under the project's lessons directory. Use when the user asks to capture lessons learned, save takeaways, record gotchas, write a retrospective, preserve decisions or fixes from the current session, or update a lessons log. Resolve the destination by reading AGENTS.md or CLAUDE.md for an explicit lessons path; if none is declared, prefer `.agents/lessons/`, then `.claude/lessons/`.
---

# Capture Lessons

Turn the current session into a concise markdown note that future agents can reuse. Capture only the parts that would save time later: constraints, root causes, decisions, commands, and file-level evidence.

## Workflow

1. Review the current conversation and the files that matter.
- Prefer concrete evidence from code, configs, and command results.
- Ignore routine back-and-forth unless it explains a non-obvious decision.

2. Decide what is worth keeping.
- Keep root causes, fixes, decision rationale, reusable commands, and repo-specific constraints.
- Skip raw transcript content, generic advice, and dead ends that add no future value.

3. Draft a short note before writing anything.
- Use a specific title tied to the problem or decision.
- Keep the note scannable and reuse-oriented.
- Prefer this structure:

```markdown
# <title>

## Context

## Lessons
- <lesson>

## Evidence

## Affected Files
- [path](/absolute/path)

## Open Questions
```

4. Resolve the output directory and save the note.
- Run `python3 scripts/save_lesson.py --workspace <repo> --title "<title>" --content-file <tmp-markdown-file>`.
- The script searches upward from `--workspace`.
- In each directory, it checks `AGENTS.md` before `CLAUDE.md`.
- It accepts explicit declarations such as `LESSONS_DIR: Lessons`, `lessons folder: docs/lessons`, `save lessons to: .agents/lessons/`, or `save lessons to: .claude/lessons/`.
- If no declaration is found, it reuses `.agents/lessons/` when present, otherwise `.claude/lessons/` when present, otherwise creates `.agents/lessons/` under the workspace root.

5. Re-open the written file and verify quality.
- Every lesson should be actionable or explanatory.
- The note should be shorter and cleaner than the original conversation.
- Keep filenames stable and descriptive; let the script append a numeric suffix if the slug already exists.

## Destination Rules

- Support absolute or relative paths declared in `AGENTS.md` or `CLAUDE.md`.
- Resolve relative paths from the directory containing the declaration file.
- Prefer the nearest declaration to the current workspace.
- Fall back in this order when no declaration exists: `.agents/lessons/`, then `.claude/lessons/` if it already exists.

## Supported Declarations

The bundled script recognizes these common forms:

```markdown
LESSONS_DIR: Lessons
LESSONS_PATH = docs/lessons
- lessons folder: .agents/lessons/
- lessons folder: .claude/lessons/
- lessons directory: docs/lessons
- save lessons to: docs/retros
```

Keep declarations simple: one path per line. The helper also tolerates legacy values joined with `or`, but new declarations should stay single-path.

## Content Bar

Good lesson notes usually include:
- Why something failed or succeeded.
- Constraints that are easy to miss on a fresh read.
- Commands, paths, or patterns worth reusing.
- Evidence pointing to the changed files or configs.

Weak lesson notes usually include:
- Generic best practices.
- Raw transcript snippets.
- Status updates with no reusable insight.
- Exhaustive implementation detail with no future decision value.

## Script Reference

Use the bundled helper from this skill directory:

```bash
python3 scripts/save_lesson.py --workspace "$PWD" --print-dir
python3 scripts/save_lesson.py --workspace "$PWD" --title "fix data loader race" --content-file /tmp/lesson.md
```

Arguments:
- `--workspace`: repository or working directory to resolve against.
- `--title`: optional note title; if omitted, the first markdown H1 is used.
- `--content-file`: read the lesson body from a markdown file. If omitted, read from stdin.
- `--print-dir`: print the resolved lessons directory without writing a note.
- `--dry-run`: print the resolved output path without writing the file.
