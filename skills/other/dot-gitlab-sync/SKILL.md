---
name: dot-gitlab-sync
description: |
  Sync .github/ and .gitlab/ template directories, applying platform-specific transformations.
  Use when keeping GitHub and GitLab templates in sync after edits to either directory.
  Triggers: "sync templates", "sync gitlab", "sync github gitlab", "dot-gitlab-sync".
license: MIT
metadata:
  author: KemingHe
  version: "1.0.0"
---

# GitHub-GitLab Template Sync

Synchronize `.github/` and `.gitlab/` template directories, applying all necessary platform-specific transformations so both directories stay consistent.

**Temporary persona**: Senior DevOps engineer with expertise in cross-platform template management and CI/CD conventions.

## When to Use This Skill

- After editing issue or PR templates in `.github/` and needing `.gitlab/` updated
- After editing issue or MR templates in `.gitlab/` and needing `.github/` updated
- Auditing both directories for consistency after any template change
- Setting up `.gitlab/` templates for the first time from existing `.github/` templates

## Asset Resolution

1. Check `./assets/transformation-rules.md` for the platform transformation reference
2. If not found, search `**/transformation-rules.md` in repository
3. If still not found, use the rules documented in this skill's Process section

## Process

### Step 1: Determine Sync Direction

Ask the user:

- **Source**: Which directory was just edited? (`.github/` or `.gitlab/`)
- **Target**: Which directory needs updating?
- If unclear, compare file modification timestamps to suggest a direction

### Step 2: Inventory Templates

List templates in both directories:

- `.github/ISSUE_TEMPLATE/` vs `.gitlab/issue_templates/`
- `.github/pull_request_template.md` vs `.gitlab/merge_request_templates/merge_request_template.md`
- `.github/ISSUE_TEMPLATE/config.yml` (GitHub-only, no GitLab equivalent)

Report any templates that exist in source but not in target (new templates to create) or vice versa (orphaned templates to flag).

### Step 3: Apply Transformations

For each template, apply the platform-specific transformations from the asset reference:

**GitHub to GitLab**:

- Remove YAML frontmatter (`name`, `about`, `title`, `labels` fields)
- Replace "PR" with "MR" and "pull request" with "merge request" in template body
- Replace "issue/PR number" with "issue/MR number" in Related sections
- Copy to GitLab directory structure (lowercase `issue_templates/`, `merge_request_templates/`)
- Skip `config.yml` (no GitLab equivalent)

**GitLab to GitHub**:

- Add YAML frontmatter with appropriate `name`, `about`, `title`, `labels` fields
- Replace "MR" with "PR" and "merge request" with "pull request" in template body
- Replace "issue/MR number" with "issue/PR number" in Related sections
- Copy to GitHub directory structure (uppercase `ISSUE_TEMPLATE/`, root-level PR template)

### Step 4: Validate

After sync, verify consistency:

- Every issue template in source has a corresponding template in target
- Template body content matches (modulo platform transformations)
- No stale terminology remains (e.g., "PR" in GitLab templates)
- Frontmatter is present in GitHub templates and absent in GitLab templates

Report clean status or list remaining discrepancies.

## General Doc Constraints

Apply to all generated output. If a discovered template deviates from any rule (e.g., uses emojis semantically, uses a different bullet convention), note the deviation explicitly and confirm with the user before treating it as a permitted exception.

- **Characters**: QWERTY keyboard typeable only - no smart quotes, emojis, or special Unicode anywhere. In prose, do not use em-dashes or em-dash substitutes (`--`, ` -- `); use ` - ` (space-dash-space) for clause separation instead. Exception: `↑` for ToC navigation.
- **Inline formatting**: Use `_underscore_` for italics, not `*single-star*`. Place colons after bold inline labels outside the markers: `**Topic**:` not `**Topic:**`.
- **Bullets**: Use `-` for all unordered lists; one bullet per complete thought; never wrap a bullet's content mid-sentence onto a continuation line - split into separate bullets if too long or multi-thought. Nested sub-bullets for component grouping are permitted. End with a period only when the item is a full sentence; omit the period for concise fragment items (preferred).
- **Prose**: Never break a sentence across lines with a hard newline; multi-sentence paragraphs belong on one continuous line since editors and viewers handle visual wrapping. Exception: commit message bodies use one sentence per line for `git log` readability.
- **Template hygiene**: Delete `(optional)` and any parenthetical conditional label (e.g., `(if operational)`) from a section header the moment the section is populated - treat it as a `.gitkeep`-style placeholder that exists only until first use, then is removed. Omit the entire section (header and body) when unused. Populate all bracketed placeholders with actual content; never leave `[TODO]`, `[TBD]`, or any `[placeholder]` in generated output.
- **Consistency**: Use the same term for the same concept throughout; match the voice and tense of the template; do not mix header levels for parallel sections.
- **KISS and DRY**: Each section and bullet conveys unique information - no redundancy or overlap.

> General Doc Constraints v1.1.0 - KemingHe/common-devx

## Skill Constraints

- **Templates only**: Sync issue and PR/MR templates; do not touch CI/CD configs, workflows, or other dot-dir contents
- **User confirmation**: Always confirm sync direction before applying changes
- **Preserve intent**: Transformations must preserve the template's purpose and structure; only platform-specific elements change
- **config.yml**: GitHub-only; never create a GitLab equivalent, never delete from GitHub during GitLab-to-GitHub sync
