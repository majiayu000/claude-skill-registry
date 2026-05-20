---
name: issue-creation
description: |
  Generate issues following repository templates for GitHub or GitLab.
  Use when creating bug reports, feature requests, or other issues.
  Triggers: "create issue", "bug report", "feature request", "new issue".
license: MIT
metadata:
  author: KemingHe
  version: "4.0.0"
---

# Issue Generation

Generate issues that communicate problems, feature requests, and enhancements following repository templates.

**Temporary persona**: Senior engineering manager with expertise in issue tracking and project communication.

## When to Use This Skill

- Creating a bug report for unexpected behavior
- Requesting a new feature or enhancement
- Documenting technical debt or improvements
- Creating issues that follow repository conventions

## Platform Detection

Determine whether the project uses GitHub or GitLab:

1. Check for `.github/` directory at project root - indicates GitHub
2. Check for `.gitlab/` directory at project root - indicates GitLab
3. If both directories exist, ask user which platform to target
4. If neither directory exists, ask user which platform to target

## Template Resolution

### GitHub

1. Search `.github/ISSUE_TEMPLATE/` for `bug-report.md`, `feature-request.md`, or other templates
2. Check `.github/ISSUE_TEMPLATE/config.yml` for template configuration
3. If not found, search `**/ISSUE_TEMPLATE/**` across repository
4. If still not found, ask user for template or use minimal structure

### GitLab

1. Search `.gitlab/issue_templates/` for `bug-report.md`, `feature-request.md`, or other templates
2. If not found, search `**/issue_templates/**` across repository
3. If still not found, ask user for template or use minimal structure

**Note**: GitHub issue templates use YAML frontmatter (`name`, `about`, `title`, `labels`); GitLab issue templates do not include frontmatter.

## Process

### Step 1: Gather Information

- Detect platform (GitHub or GitLab) using Platform Detection above
- Search for issue templates in repository using the platform-specific Template Resolution
- Classify issue type from user input (bug vs feature vs other)
- Use MCP tools for context:
  - Search existing issues, PRs (GitHub) / MRs (GitLab), discussions for related work
  - Search codebase for recent changes, error patterns
  - Identify dependencies or blockers from prior work
- Extract key information: symptoms, desired functionality, technical requirements

### Step 2: Classify and Consult User

Determine issue type and generate title:

| Type | Format | Example |
| :--- | :--- | :--- |
| Bug | `bug(scope): description` | bug(api): fix null pointer in auth |
| Feature | `feat(scope): description` | feat(ui): add dark mode toggle |

Present template selection and ask:

- Bug: Reproduction steps, expected/actual behavior, environment?
- Feature: Problem statement, proposed solution, alternatives?
- All: Related issues/PRs (GitHub) / MRs (GitLab), priority level?

### Step 3: Generate Issue

- Use template as minimum structure, enrich with critical details
- Include conventional title format
- Populate Related section with discovered issues/PRs (GitHub) / MRs (GitLab) (omit if none)
- Add context that helps maintainers: error logs, affected files, user impact
- Use dash bullets, each with specific actionable details
- Apply KISS and DRY: no fluff, but capture all information needed to act

**Enrichment guidance**:

- Bug: Include actual error messages, stack traces, affected code paths
- Feature: Clarify scope boundaries, success criteria, edge cases
- Both: Link related issues/PRs (GitHub) / MRs (GitLab), note blocking dependencies

## Output Format

Present final issue in markdown code block:

```markdown
bug(component): brief description
OR
feat(component): brief description

[complete issue content following template structure]
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

- **Title**: Max 50 characters, imperative mood, `bug(scope):` or `feat(scope):` format
- **Template as scaffold**: Use discovered templates as minimum structure, enrich appropriately
- **Completeness**: Capture all technical details, error messages, requirements
- **Platform awareness**: Use detected platform terminology consistently throughout the generated issue
