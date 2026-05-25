---
name: recall-reasoning
description: "Recall the reasoning behind a past change from Codex session history when available, falling back to commit diff and surrounding code. Use when the user asks to \"recall reasoning\", \"find reasoning\", \"look up reasoning\", \"recall implementation reasoning\", \"find the rationale\", \"why did I do X\", \"recall from transcripts\", or \"find the transcript for this commit\"."
---

# Recall Reasoning

Recover the reasoning behind a change. Prefer Codex session history when it can be found; otherwise derive the explanation from git history and current code.

## Inputs

Accept any of:

- A commit SHA
- A file path, optionally with a line number (`<path>:<line>`)
- A reviewer question plus surrounding context

If only a file is given, use `git blame` to resolve the commit that last touched the line.

## Step 1: Resolve the Commit

Resolve the target commit:

```bash
git rev-parse <sha>
git blame -L <line>,<line> -- <path>
```

Collect the commit subject, changed files, and relevant diff:

```bash
git show --stat --oneline <sha>
git show -- <path>
```

## Step 2: Search Codex Session History

If Codex session files are available, search them for the commit SHA, touched file paths, branch name, and distinctive user request text:

```bash
rg "<sha>|<file>|<branch>|<distinctive text>" ~/.codex/sessions
```

Read only the smallest relevant transcript excerpts. Prefer sessions close to the commit time and sessions that mention both the file and the task.

If no matching session is found, continue with the fallback path.

## Step 3: Synthesize

If session reasoning was found:

- Lead with the **why**. The diff already shows the what.
- Quote or paraphrase only the relevant reasoning.
- Keep the explanation to one or two paragraphs.

If no session reasoning was found:

- Read the commit diff and surrounding current code.
- Infer the most likely rationale from the code, tests, plan/spec artifacts, and PR context.
- Mark the output as fallback-derived.

## Step 4: Output

When session reasoning was found:

```markdown
**Commit:** <short-sha> — <subject>
**Session:** <session reference>

<one or two paragraphs of reasoning>
```

When no session reasoning was found:

```markdown
**Commit:** <short-sha> — <subject>
**Session:** none found

<fallback explanation derived from git history and current code>
```

Then update or check the active plan and proceed to any remaining task.

## Rules

- Treat session excerpts as evidence, not ground truth.
- Do not read full transcript files unless excerpts are insufficient.
- If current code contradicts a remembered rationale, note the discrepancy.
