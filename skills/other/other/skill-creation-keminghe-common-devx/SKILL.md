---
name: skill-creation
description: |
  Create or refactor Agent Skills following the agentskills.io specification.
  Use when creating new skills, converting prompts to skills, or validating skill structure.
  Triggers: "create skill", "new skill", "SKILL.md", "agent skill", "convert prompt".
license: MIT
metadata:
  author: KemingHe
  version: "2.0.0"
---

# Skill Creation

Create Agent Skills following the [agentskills.io](https://agentskills.io) specification for platform-agnostic AI capabilities.

## When to Use This Skill

- Creating a new skill from scratch
- Converting an existing prompt to skill format
- Refactoring or validating existing skills
- Understanding skill structure and best practices

## Asset Resolution

1. Check `./assets/skill-template.md` for the SKILL.md template
2. Check `./assets/general-doc-constraints.md` for the General Doc Constraints block (used conditionally for documentation-output skills)
3. If not found, search `**/skill-template.md` and `**/general-doc-constraints.md` in repository
4. If still not found, use the specification below to generate from scratch

## Process

### Step 1: Gather Context

Before creating a skill, understand:

- **Purpose**: What task does this skill accomplish?
- **Triggers**: What keywords or scenarios should activate this skill?
- **Inputs**: What information does the agent need from the user?
- **Outputs**: What should the agent produce?
- **Assets**: Are there templates or reference materials needed?

**When refactoring from existing prompt/content**:

Analyze the original for critical elements that must be preserved:

| Element | Look For | Why It Matters |
| :--- | :--- | :--- |
| **Safety mechanisms** | Read-only operations, forbidden actions, pipe to `cat` | Prevents destructive actions |
| **Setup instructions** | `cd` to directory, environment prep | Ensures correct execution context |
| **Role/persona** | "You are a..." statements | Sets expertise level and tone |
| **Tool guidance** | MCP tools, remote APIs, search patterns | Enables deeper analysis |
| **User consultation** | Questions to ask user | Ensures alignment with intent |
| **Edge cases** | Error handling, fallbacks | Improves robustness |

**Active user feedback**: Present your analysis of what to keep, improve, or remove. Ask:

- Are there critical behaviors to preserve?
- What should be improved or modernized?
- Any new requirements to add?

### Step 2: Create Directory Structure

```plaintext
skill-name/
├── SKILL.md              # Required: instructions + frontmatter
├── README.md             # Required: human documentation
├── assets/               # Optional: templates, static resources
├── references/           # Optional: detailed docs, acceptance criteria
└── scripts/              # Optional: executable code
```

**Naming rules** (from [agentskills.io](https://agentskills.io)):

- Lowercase letters, numbers, and hyphens only
- 1-64 characters
- No leading/trailing hyphens
- No consecutive hyphens (`--`)
- Directory name must match `name` field in frontmatter

### Step 3: Write SKILL.md

Read the skill template from Asset Resolution. Fill in all bracket placeholders with project-specific values.

**Frontmatter guidelines**:

- `description`: 1-1024 chars. First sentence: what the skill does. Second sentence: when to use it, including trigger keywords.
- `license`: Project license name or file reference
- See Specification Reference below for all available fields

**Body guidelines**:

- Adapt template sections to the skill's domain - remove unused optional sections, add domain-specific ones
- For skills interacting with external systems, uncomment and fill in the Safety section (the template provides the pattern)
- If the skill generates document or text output (READMEs, issues, PRs/MRs, commit messages, meeting docs, etc.), insert the General Doc Constraints block from `./assets/general-doc-constraints.md` at the placeholder position in the template (between Output Format and Skill Constraints)
- If the skill does not produce document output (e.g., coaching, interactive modes), omit the General Doc Constraints block entirely
- Keep under 500 lines; move supplementary detail to `references/`

### Step 4: Create Assets (if needed)

Place templates in `assets/` subdirectory:

- Use descriptive names: `{purpose}-template.md`
- Templates should be self-documenting with placeholders

### Step 5: Create README.md

Create human-readable documentation with: description, quick start, file listing, and related links. Follow the pattern of existing skill READMEs in the repository.

## Output Format

When creating a skill, produce three files:

1. **SKILL.md** - Complete with frontmatter and body
2. **README.md** - Human documentation
3. **assets/*.md** - Template files (if applicable)

Present each file in a markdown code block with the filename as header.

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

- **Frontmatter**: Must be valid YAML with `name` and `description`
- **Name matching**: Directory name must equal `name` field
- **Naming convention**: Prefer action-oriented names describing what the skill does (e.g., `readme-creation`, `commit-message-creation`, `contacts-management`) - this is a soft recommendation; exceptions like `senior-mentor` (persona/coaching mode) are acceptable when clarity requires it
- **Line limit**: Keep SKILL.md under 500 lines (move details to references/)
- **Token budget**: Body should be <5000 tokens for efficient loading
- **Progressive disclosure**: Only essential instructions in SKILL.md; details in assets/references
- **Asset resolution**: Always instruct to check local `./assets/` first, then search

## Specification Reference

Full specification: [agentskills.io/specification](https://agentskills.io/specification)

### Frontmatter Fields

| Field | Required | Constraints |
| :--- | :--- | :--- |
| `name` | Yes | 1-64 chars, lowercase, hyphens, must match directory |
| `description` | Yes | 1-1024 chars, what + when + triggers |
| `license` | No | License name or file reference |
| `compatibility` | No | Environment requirements (1-500 chars) |
| `metadata` | No | Key-value pairs (author, version, etc.) |
| `allowed-tools` | No | Space-delimited tool list (experimental) |

### Optional Directories

| Directory | Purpose | When to Use |
| :--- | :--- | :--- |
| `assets/` | Templates, images, data files, static resources | Skill produces output based on templates |
| `references/` | Detailed docs, acceptance criteria, domain-specific files | SKILL.md exceeds 500 lines or needs test criteria |
| `scripts/` | Executable code (Python, Bash, JavaScript) | Skill needs to run code for reliable execution |
