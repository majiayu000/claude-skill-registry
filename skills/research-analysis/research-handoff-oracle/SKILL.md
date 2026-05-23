---
name: research-handoff-oracle
description: "Use when asked to create a deep-research handoff bundle: do web research, codebase analysis, Gemini Oracle critique, and produce a prompt + context folder on Desktop for another AI agent (include a zipped archive of the bundle)."
metadata:
  short-description: Deep research handoff prompt + context bundle
---

# Research Handoff (Oracle)

Create a reusable, high-quality research handoff for a "super researcher" AI agent. The deliverable is a **Desktop folder** containing:
- `PROMPT.md` (the final research prompt)
- `context/` (copies of relevant files)
- `MANIFEST.md` (list of copied files + why they matter)
- `SEARCH_LOG.md` (search queries, sources, dates, filters, and result counts)
and a **zip archive** of the entire folder for easy handoff.

This skill is **generic** and should work for any question or project.

## When to use
- The user wants a **comprehensive prompt** for a separate research agent.
- The user asks for **web research + codebase research + Oracle critique**.
- The user wants a **Desktop bundle** with the prompt + context files.

## Workflow

### 1) Scope & Assumptions
- Restate the goal in 1-2 sentences.
- Identify **repositories** and **roots** involved. If ambiguous, ask a short clarification or default to `cwd`.
- Capture key constraints (e.g., must use existing logic, preserve tests, auth requirements).
- Note any **dates** or recency constraints.

### 2) Context Inventory (local files)
- Read **AGENTS.md**, README, CLAUDE/GEMINI files, and core docs/specs.
- Use `rg` to find important modules, configs, and specs.
- Create a shortlist of **must-copy** files: specs, architecture docs, security, auth, schema, API docs, key configs.
- Record these in `MANIFEST.md` with one-line reasons.

### 3) Codebase Recon
- Identify key folders (e.g., `internal/`, `src/`, `prisma/`, `docs/`).
- Note important entrypoints, build systems, and tests.
- Extract **exact file paths** for core logic or APIs.

### 4) Web Research
- Use `web.run` when available; otherwise use `curl`/`wget`/browser.
- Search for best practices, pitfalls, and security considerations **relevant to the prompt**.
- Capture citations (links + publisher) for inclusion in `PROMPT.md`.
- Maintain a `SEARCH_LOG.md` with: date, source/database, full query, filters/limits, and result counts.

### 5) Gemini Oracle Critique
- Run `gemini-oracle` (on PATH). If unknown usage, run `gemini-oracle --help` first.
- Provide a concise summary of the planned prompt and key findings.
- Incorporate the oracle’s critiques into the prompt.

### 6) Build the Prompt
Include these sections in `PROMPT.md`:
1. **Executive summary** of the task.
2. **Current state** + codebase constraints.
3. **Target output** (what the researcher must produce).
4. **Required research steps** (web + code + Oracle critique).
5. **Context files** (explicit list + paths).
6. **Open questions / decisions needed**.
7. **Format requirements** (headers, deliverables, citations).
8. **Search strategy expectations** (databases/sources, date bounds, and documentation requirements).
9. **Out-of-scope** items.

Keep the prompt clear, explicit, and actionable.

### 7) Build the Desktop Bundle
- Create a folder on Desktop: `~/Desktop/<project>-research-handoff-YYYY-MM-DD/`
- Save `PROMPT.md` at the root.
- Copy files into `context/` mirroring repo structure.
- Add `MANIFEST.md` listing:
  - file path
  - reason included
- Add `SEARCH_LOG.md` with search strategy details.

### 8) Zip the Bundle (required)
- Create a zip file alongside the folder:
  - `~/Desktop/<project>-research-handoff-YYYY-MM-DD.zip`
- Use a recursive zip command (e.g., `zip -r <zip> <folder>`).
- If a zip already exists, overwrite it.

### 9) Final Response
- Provide the bundle path.
- Provide the zip path.
- List which files were copied.
- State that the prompt is ready for handoff.

## Output Template (minimal)

```text
<Desktop>/<bundle>/
  PROMPT.md
  MANIFEST.md
  SEARCH_LOG.md
  context/
    <repo>/...
<Desktop>/<bundle>.zip
```

## Quality Checklist
- Prompt includes: goals, constraints, required research, deliverable, context list, and output format.
- Web research done and sources cited.
- Search log includes queries, sources, dates, and filters.
- Oracle critique applied.
- Desktop bundle created with prompt + context.
- Zip archive created and matches the bundle.
- Manifest lists files with reasons.
