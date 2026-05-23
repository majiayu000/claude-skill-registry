---
name: pull-merge-request-creation
description: |
  Generate pull request (GitHub) or merge request (GitLab) descriptions following repository templates.
  Use when creating PRs/MRs to communicate changes, impact, and value.
  Triggers: "create pr", "create mr", "pull request", "merge request", "pr description", "mr description".
license: MIT
metadata:
  author: KemingHe
  version: "4.0.0"
---

# Pull/Merge Request Generation

Generate pull request (GitHub) or merge request (GitLab) descriptions that communicate changes, impact, and value following project templates.

**Temporary persona**: Senior engineering manager with expertise in code review and technical documentation.

## When to Use This Skill

- Creating a pull request (GitHub) or merge request (GitLab) description for branch changes
- Documenting changes for code review
- Communicating technical decisions and business value
- Following repository PR (GitHub) / MR (GitLab) conventions

## Platform Detection

Determine whether the project uses GitHub or GitLab:

1. Check for `.github/` directory at project root - indicates GitHub
2. Check for `.gitlab/` directory at project root - indicates GitLab
3. If both directories exist, ask user which platform to target
4. If neither directory exists, ask user which platform to target

## Template Resolution

### GitHub

1. Search `.github/pull_request_template.md` for PR template
2. If not found, search `**/pull_request_template.md` across repository
3. If still not found, ask user for template or use minimal structure

### GitLab

1. Search `.gitlab/merge_request_templates/merge_request_template.md` for MR template
2. If not found, search `**/merge_request_templates/**` across repository
3. If still not found, ask user for template or use minimal structure

**Note**: GitHub PR templates may include YAML frontmatter (`name`, `about`, `title`); GitLab MR templates do not include frontmatter.

## Git Operations (Read-Only)

This skill performs read-only reconnaissance. Never modify repository state.

**Setup**: Navigate to repository root. Pipe all git commands to `cat` to avoid interactive mode or pager.

**Safe commands**:

```shell
git status | cat                              # Current repository state
git log origin/main..HEAD --oneline | cat     # Commits on this branch
git diff origin/main...HEAD --stat | cat      # Summary of changes vs main
git diff origin/main...HEAD | cat             # Detailed changes vs main
git show --name-only HEAD | cat               # Files changed in latest commit
git branch -a | cat                           # All branches
```

**Forbidden operations**: Never use git commit, push, pull, merge, rebase, add, reset, clean, or stash.

**Prefer remote tools**: Use GitHub/GitLab MCP tools when available for related issues, PRs (GitHub) / MRs (GitLab), and branch history.

## Process

### Step 1: Analyze Branch

- Detect platform (GitHub or GitLab) using Platform Detection above
- Search for the appropriate template using platform-specific Template Resolution
- Run safe git operations (with `| cat`) to understand changes
- Use MCP tools for context:
  - Search related issues and PRs (GitHub) / MRs (GitLab)
  - Analyze affected functionality and dependencies
  - Identify architectural patterns impacted

### Step 2: Classify and Consult User

Determine PR (GitHub) / MR (GitLab) type and generate title:

| Type | When to Use |
| :--- | :--- |
| `feat` | New feature or capability |
| `fix` | Bug fix |
| `docs` | Documentation only |
| `refactor` | Code change, no feature/fix |
| `chore` | Maintenance, dependencies |

Generate title: `type(scope): brief description` - max 50 characters, imperative mood

Present change summary and ask:

- Confirm scope and key areas of change?
- Which issues does this resolve?
- Business motivation and testing approach?
- Breaking changes or review considerations?

### Step 3: Generate Description

- Use template as minimum structure, enrich with critical details
- Include conventional commit-style title
- Use dash bullets, each conveying unique information
- Apply KISS and DRY: no fluff, but capture all information reviewers need
- Group changes by feature area, impact level, or architectural component

**Enrichment guidance**:

- Changes: Describe what changed and why, not just file names
- Impact: Clarify user-facing effects, performance implications, breaking changes
- Notes: Include merge dependencies, testing considerations, rollback plan if relevant
- Connect technical changes to business value

## Change Categorization

Choose appropriate grouping for changes:

- Feature area: Specific modules, functionality, user-facing features
- Impact level: Critical fixes, performance, minor updates
- Architectural component: Database schemas, APIs, system integrations
- Combined: Mix categories for better clarity

## Output Format

Present final description in markdown code block:

```markdown
type(scope): brief description

[complete PR/MR description following template structure]
```

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

- **Title**: Max 50 characters, imperative mood, conventional commit format
- **Template as scaffold**: Use discovered templates as minimum structure, enrich appropriately
- **Comprehensive analysis**: Use git commands, MCP tools, codebase search
- **Business context**: Connect technical changes to business value
- **Issue linking**: Use separate "closes #X" for each resolved issue
- **Platform awareness**: Use detected platform terminology consistently throughout the generated description
