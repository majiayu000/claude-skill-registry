---
name: skill-creation
description: |
  Create or refactor Agent Skills following the agentskills.io specification.
  Use when creating new skills, converting prompts to skills, or validating skill structure.
  Triggers: "create skill", "new skill", "SKILL.md", "agent skill", "convert prompt".
license: MIT
metadata:
  author: KemingHe
  version: "1.2.0"
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
2. If not found, search `**/skill-template.md` in repository
3. If still not found, use the specification below to generate from scratch

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
- Keep under 500 lines; move supplementary detail to `references/`

### Step 4: Create Assets (if needed)

Place templates in `assets/` subdirectory:

- Use descriptive names: `{purpose}-template.md`
- Templates should be self-documenting with placeholders
- Include version footer in templates

### Step 5: Create README.md

Create human-readable documentation with: description, quick start, file listing, and related links. Follow the pattern of existing skill READMEs in the repository.

## Output Format

When creating a skill, produce three files:

1. **SKILL.md** - Complete with frontmatter and body
2. **README.md** - Human documentation
3. **assets/*.md** - Template files (if applicable)

Present each file in a markdown code block with the filename as header.

## Constraints

- **Frontmatter**: Must be valid YAML with `name` and `description`
- **Name matching**: Directory name must equal `name` field
- **Line limit**: Keep SKILL.md under 500 lines (move details to references/)
- **Token budget**: Body should be <5000 tokens for efficient loading
- **Progressive disclosure**: Only essential instructions in SKILL.md; details in assets/references
- **Asset resolution**: Always instruct to check local `./assets/` first, then search
- **Characters**: QWERTY keyboard typeable only - no em-dashes, smart quotes, emojis, or special Unicode. Exception: `↑` for ToC navigation

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

---

> Skill Creation Skill v1.2.0 - KemingHe/common-devx
