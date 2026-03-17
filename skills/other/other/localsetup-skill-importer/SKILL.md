---
name: localsetup-skill-importer
description: Import external skills from a URL (GitHub or other) or local path; discover, validate, security-screen, and summarize each skill so the user can choose which to import. Use when the user wants to add skills from a repo/URL or local folder, or when screening and selecting skills to add to the framework.
metadata:
  version: "1.3"
---

# Skill importer (framework)

**Purpose:** Let the user point at a **URL** (e.g. GitHub repo) or **local path** containing skills; discover and validate them; run a heuristic security screen (no execution); produce a **per-skill brief** (what it does, what it has, what kind of code); then let the user **choose which to import** and complete registration.

## When to use this skill

- User wants to "import skills from this URL" or "add skills from GitHub/anthropics/skills."
- User has a local folder or markdown and wants to screen/import skills.
- User asks to "parse a repo and add the skills" or "validate and import skills."

## Workflow (agent steps)

0. **Ensure skill validation pattern file**  - The scan tool uses `_localsetup/docs/SKILL_VALIDATION_PATTERNS.yaml` (or fetches it if missing). If the tool reports that the file is stale (7+ days old), prompt the user: "(1) Pull latest from repo, (2) Do nothing, (3) Use existing file." Act on their choice; if they choose pull latest, fetch the canonical URL (see SKILL_VALIDATION_PATTERNS.md) and overwrite the local file, then re-run the scan.
1. **Get source**  - URL or local path. If URL: clone or download to a temp dir (e.g. `git clone --depth 1 <url> /tmp/skills-src`); then use that path as scan root. If local path: use as scan root.
2. **Scan**  - Run `_localsetup/tools/skill_importer_scan <path>` (or `.ps1` on Windows). It discovers skill dirs (containing SKILL.md with valid frontmatter), validates format, lists contents and code types, runs heuristic security checks, and content-safety checks (pattern file + English-only on body). Output: per-skill summary including "Security" and "Content safety" sections.
3. **Summarize for user**  - For each skill present a brief:
   - **What it does**  - From description (and body if needed).
   - **What it has**  - Scripts, references, assets; file types and languages.
   - **Code**  - Kinds of code (Python, Bash, etc.); any deps or compatibility notes.
   - **Security**  - Screening result: no concerns, or "Review: …" with file/line (heuristic flags in scripts/assets). Do not auto-block; let the user decide.
   - **Content safety**  - If the scan shows "Content safety: REVIEW", present the trigger keyword(s) and **file, line, and column** for each hit, plus the short description from the pattern index (plain language). Do **not** read or display the actual content at those positions. State: "For safety reasons we are not reading or displaying that content here. Please open the file at the indicated position(s) and review it yourself." Then offer: (1) Do not import / skip this skill, (2) I have reviewed the file; proceed with import, (3) I will ignore and continue anyway.
4. **User selects**  - Ask which skills to import (by name or "all"). Use AskQuestion or a clear list with instructions (e.g. "Reply with names or 'all'").
4b. **Public skill discovery (optional)**  - For each selected candidate, optionally load **localsetup-skill-discovery**: check PUBLIC_SKILL_INDEX.yaml for similar public skills; if relevant matches exist, suggest "Similar public skills are available; would you like in-depth summaries or to pull one instead?" and offer the same four options (in-depth summary, use public skill, continue, adapt).
5. **Duplicate, overlap, and namespace check**  - Before importing each selected skill, compare to existing framework skills. List existing skills from `_localsetup/skills/` (each dir name and SKILL.md `name` + `description`). For each candidate: (a) **Namespace collision**  - same `name` or directory as an existing skill: warn and offer **Ignore new**, **Replace existing**, **Merge** (combine best of both), or **Create as new** (different name). (b) **High overlap**  - no name match but description/purpose/triggers very similar to an existing skill: warn and offer the same four options. Do not auto-replace or auto-merge; get explicit user choice. For **Merge**, combine content from both into one skill and replace the existing; do not add the candidate as a second copy.
5b. **Offer normalize before copy**  - For each selected skill, offer: "Normalize this skill for spec compliance and platform-neutral wording before copy?" Use _localsetup/docs/SKILL_NORMALIZATION.md as the single source of truth. If **yes:** apply the checklist and platform-neutralization rules to the skill's SKILL.md (in memory or temp); produce a **summary** (e.g. "Frontmatter: add compatibility, remove platform metadata; replace 'Integration with X' with generic section") and a **concrete list of key edits** (e.g. "Remove metadata.openclaw"; "Replace lines 427–453 with generic snippet"); present both to the user and get explicit approval; then copy the **normalized** skill dir to `_localsetup/skills/<name>/`. If **no:** copy the skill as-is to `_localsetup/skills/<name>/`, then warn once: "Imported without normalization. This skill may contain platform-specific content; you can normalize later using the rules in _localsetup/docs/SKILL_NORMALIZATION.md." Normalization applies to SKILL.md only; other files (references, scripts, playbooks) are copied unchanged.
6. **Import**  - For each selected, after user choice (and any merge/rename) and after normalize step if applied: copy dir to `_localsetup/skills/<name>/` (normalized content if user approved normalize, else as-is); set `name` in frontmatter to match directory (e.g. `localsetup-<name>`); add `metadata.version: "1.0"` if missing; register in every file in _localsetup/docs/PLATFORM_REGISTRY.md § Skill registration (new skills); optionally run deploy.
7. **Confirm**  - Tell the user what was imported and that they can run deploy.

## Security and content safety screening (heuristic only)

- Tool does **not** execute any skill code. It only scans file contents.
- **Security:** Flags patterns in scripts/assets (e.g. `eval(`, `curl | sh`, `Invoke-Expression`). Output is "Security: Review …" for the user; do not block import automatically.
- **Content safety:** Scans SKILL.md body and scripts/assets using the pattern file (see [SKILL_VALIDATION_PATTERNS.md](../../docs/SKILL_VALIDATION_PATTERNS.md)). Also flags non-English body content. For pattern hits, only **references** are shown (file, line, column, pattern id, and description from the index); the actual content at those positions is not read or displayed so the user can open the file and review themselves. Present the three options (skip / proceed after review / ignore and continue); do not auto-block.

## Sources

- **URL**  - GitHub repo, archive link, or any fetchable URL. Agent fetches; then runs scan on the resulting path.
- **Local path**  - Directory on disk with skill subdirs.
- **Single markdown**  - Use the skill-creator workflow to create a new skill from a doc; that skill is then framework-compatible and can be used with this importer flow for batch consistency.
- **Pasted content or URL to a single document**  - Follow the canonical flow in _localsetup/docs/SKILL_IMPORTING.md § "Adding a skill from paste or URL": write content to a temporary directory first, run the validation script on that path, present results and user choices, and only then copy to `_localsetup/skills/` if the user approves. Validation is always path-based; never pass skill content through the shell.

## Compatibility

- Only directories that contain a valid SKILL.md (Agent Skills spec: `name`, `description`) are considered skills. Imported skills remain spec-compliant and interchangeable (see [SKILL_INTEROPERABILITY.md](../../docs/SKILL_INTEROPERABILITY.md)).

## Duplicate and overlap (user options)

- Check each candidate against existing `_localsetup/skills/` (names and descriptions). On **namespace collision** (same name/dir) or **high overlap** (very similar purpose), warn and offer: **Ignore new**, **Replace existing**, **Merge** (best of both into one), **Create as new** (e.g. different name). User choice is final.

## Reference

- _localsetup/docs/SKILL_IMPORTING.md  - Full workflow, duplicate/overlap checks, normalize step, tool usage, security notes.
- _localsetup/docs/SKILL_NORMALIZATION.md  - Spec-compliance checklist, frontmatter examples, platform-neutralization rules and generic snippets; used when user accepts "Normalize before copy?"
- _localsetup/docs/SKILL_VALIDATION_PATTERNS.md  - Pattern file location, fetch URL, 7-day refresh, content safety and user options.
- _localsetup/docs/SKILL_DISCOVERY.md  - Public registries; use localsetup-skill-discovery to recommend similar public skills when importing.
- _localsetup/docs/PLATFORM_REGISTRY.md  - Registration file list after import.
- _localsetup/docs/SKILL_INTEROPERABILITY.md  - Import/export and spec.
