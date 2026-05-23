---
name: skill-master
description: "Agent Skills authoring. Covers SKILL.md format, frontmatter, folders, docs ingestion. Keywords: agentskills.io, SKILL.md."
version: "1.2.4"
release_date: "2026-01-27"
metadata:
  author: itechmeat
---

# Skill Master

This skill is the entry point for creating and maintaining Agent Skills.

**Language requirement:** all skills MUST be authored in English.

## Quick Navigation

- New to skills? Read: `references/specification.md`
- SKILL.md templates? See: `assets/skill-templates.md`
- Advanced features (context, agents, hooks)? Read: `references/advanced-features.md`
- Creating from docs? Read: `references/docs-ingestion.md`
- Validation & packaging? See `scripts/`

## When to Use

- Creating a new skill from scratch
- Updating an existing skill
- Creating a skill by ingesting external documentation
- Validating or packaging a skill for distribution

## Skill Structure (Required)

```
my-skill/
├── SKILL.md          # Required: instructions + metadata
├── README.md         # Optional: human-readable description
├── metadata.json     # Optional: extended metadata for publishing
├── references/       # Optional: documentation, guides, API references
├── examples/         # Optional: sample outputs, usage examples
├── scripts/          # Optional: executable code
└── assets/           # Optional: templates, images, data files
```

### Folder Purposes (CRITICAL)

| Folder        | Purpose                                    | Examples                                                |
| ------------- | ------------------------------------------ | ------------------------------------------------------- |
| `references/` | **Documentation** for agents to read       | Guides, API docs, concept explanations, troubleshooting |
| `examples/`   | **Sample outputs** showing expected format | Output examples, usage demonstrations                   |
| `assets/`     | **Static resources** to copy/use           | Document templates, config templates, images, schemas   |
| `scripts/`    | **Executable code** to run                 | Python scripts, shell scripts, validators               |

### When to Use Each

**Use `references/` for:**

- Detailed documentation about concepts
- API references and usage guides
- Troubleshooting and FAQ
- Anything the agent needs to **read and understand**

**Use `examples/` for:**

- Sample outputs showing expected format
- Usage demonstrations
- Before/after comparisons
- Anything showing **what the result should look like**

**Use `assets/` for:**

- Document templates (markdown files to copy as starting point)
- Configuration file templates
- Schema files, lookup tables
- Images and diagrams
- Anything the agent needs to **copy or reference verbatim**

**IMPORTANT**: Templates belong in `assets/`, examples in `examples/`, documentation in `references/`.

## Frontmatter Schema

Every `SKILL.md` MUST start with YAML frontmatter:

```yaml
---
name: skill-name
description: "What it does. Keywords: term1, term2."
metadata:
  author: your-name
  version: "1.0.0"
---
```

**Field order:** `name` → `description` → `license` → `compatibility` → `metadata` → other fields

### Required Fields

| Field       | Constraints                                                                                 |
| ----------- | ------------------------------------------------------------------------------------------- |
| name        | 1-64 chars, lowercase `a-z0-9-`, no `--`, no leading/trailing `-`, must match folder name   |
| description | 1-1024 chars (target: 80-150), describes what skill does + when to use it, include keywords |

### Optional Fields (Top Level)

| Field         | Purpose                                           |
| ------------- | ------------------------------------------------- |
| license       | License name or reference to bundled LICENSE file |
| compatibility | Environment requirements (max 500 chars)          |
| metadata      | Object for arbitrary key-value pairs (see below)  |

### metadata Object (Common Fields)

| Field         | Purpose                                          |
| ------------- | ------------------------------------------------ |
| author        | Author name or organization                      |
| version       | **Skill version** (semver format, e.g., "1.0.0") |
| argument-hint | Hint for autocomplete, e.g., `[issue-number]`    |

**IMPORTANT**: `version` in `metadata` is the **skill version**. If you reference external product docs, track that version separately (e.g., in README.md or metadata.json).

### Optional Fields (Claude Code / Advanced)

| Field                    | Purpose                                                                    |
| ------------------------ | -------------------------------------------------------------------------- |
| disable-model-invocation | `true` = only user can invoke (via `/name`). Default: `false`              |
| user-invocable           | `false` = hidden from `/` menu, only agent can load. Default: `true`       |
| allowed-tools            | Space-delimited tools agent can use without asking, e.g., `Read Grep Glob` |
| model                    | Specific model to use when skill is active                                 |
| context                  | Set to `fork` to run in a forked subagent context                          |
| agent                    | Subagent type when `context: fork`, e.g., `Explore`, `Plan`                |
| hooks                    | Hooks scoped to skill's lifecycle (see agent documentation)                |

### Invocation Control Matrix

| Frontmatter                      | User can invoke | Agent can invoke | Notes                                   |
| -------------------------------- | --------------- | ---------------- | --------------------------------------- |
| (default)                        | ✅ Yes          | ✅ Yes           | Description in context, loads when used |
| `disable-model-invocation: true` | ✅ Yes          | ❌ No            | For manual workflows with side effects  |
| `user-invocable: false`          | ❌ No           | ✅ Yes           | Background knowledge, not a command     |

### Variable Substitutions

Available placeholders in skill content:

| Variable               | Description                                              |
| ---------------------- | -------------------------------------------------------- |
| `$ARGUMENTS`           | All arguments passed when invoking the skill             |
| `${CLAUDE_SESSION_ID}` | Current session ID for logging or session-specific files |

If `$ARGUMENTS` is not in content, arguments are appended as `ARGUMENTS: <value>`.

Example:

```yaml
---
name: fix-issue
description: Fix a GitHub issue
disable-model-invocation: true
---
Fix GitHub issue $ARGUMENTS following our coding standards.
```

### Dynamic Context Injection

Use `!`command`` syntax to run shell commands before skill content is sent to the agent:

```markdown
## Pull request context

- PR diff: !`gh pr diff`
- Changed files: !`gh pr diff --name-only`

## Your task

Review this pull request...
```

The command output replaces the placeholder, so the agent receives actual data.

## metadata.json (Optional)

For publishing or extended metadata, create `metadata.json`:

```json
{
  "version": "1.0.0",
  "organization": "Your Org",
  "date": "January 2026",
  "abstract": "Brief description of what this skill provides...",
  "references": ["https://docs.example.com", "https://github.com/org/repo"]
}
```

**Fields:**

- `version` — Skill version (semver)
- `organization` — Author or organization
- `date` — Publication date
- `abstract` — Extended description (can be longer than frontmatter)
- `references` — List of source documentation URLs

### Name Validation Examples

```yaml
# Valid
name: pdf-processing
name: data-analysis
name: code-review

# Invalid
name: PDF-Processing  # uppercase not allowed
name: -pdf            # cannot start with hyphen
name: pdf--processing # consecutive hyphens not allowed
```

### Description Rules

**Purpose:** Tell the LLM what the skill does and when to activate it. Minimize tokens — just enough for activation decision.

**Formula:**

```
[Product] [core function]. Covers [2-3 key topics]. Keywords: [terms].
```

**Constraints:**

- Target: 80-150 chars
- Max: 300 chars
- No marketing ("powerful", "comprehensive", "modern")
- No filler ("this skill", "use this for", "helps with")
- No redundant context (skip "for apps", "for developers")

**Good examples:**

```yaml
description: "Turso SQLite database. Covers encryption, sync, agent patterns. Keywords: Turso, libSQL, SQLite."

description: "Base UI unstyled React components. Covers forms, menus, overlays. Keywords: @base-ui/react, render props."

description: "Inworld TTS API. Covers voice cloning, audio markups, timestamps. Keywords: Inworld, TTS, visemes."
```

**Poor examples:**

```yaml
# Too vague
description: "Helps with PDFs."

# Too verbose
description: "Turso embedded SQLite database for modern apps and AI agents. Covers encryption, authorization, sync, partial sync, and agent database patterns."

# Marketing
description: "A powerful solution for all your database needs."
```

**Keywords:** product name, package name, 3-5 terms max.

## How Skills Work (Progressive Disclosure)

1. **Discovery**: Agent loads only `name` + `description` of each skill (~50-100 tokens)
2. **Activation**: When task matches, agent reads full `SKILL.md` into context
3. **Execution**: Agent follows instructions, loads referenced files as needed

**Key rule:** Keep `SKILL.md` under 500 lines. Move details to `references/`.

## Creating a New Skill

### Step 1: Scaffold

```bash
python scripts/init_skill.py <skill-name>
# Or specify custom directory:
python scripts/init_skill.py <skill-name> --skills-dir skills
```

Or manually create:

```
<skills-folder>/<skill-name>/
├── SKILL.md
├── references/   # For documentation, guides
└── assets/       # For templates, static files
```

### Step 2: Write Frontmatter

```yaml
---
name: <skill-name>
description: "[Purpose] + [Triggers/Keywords]"
---
```

### Step 3: Write Body

Recommended sections:

- When to use (triggers, situations)
- Quick navigation (router to references and assets)
- Steps / Recipes / Checklists
- Critical prohibitions
- Links

### Step 4: Add References (documentation)

For each major topic, create `references/<topic>.md` with:

- Actionable takeaways (5-15 bullets)
- Gotchas / prohibitions
- Practical examples

### Step 5: Add Assets (if needed)

For templates or static resources, create `assets/<resource>`:

- Document templates
- Configuration templates
- Schema files

### Step 6: Validate

```bash
python scripts/quick_validate_skill.py <skill-path>
```

## Creating a Skill from Documentation

When building a skill from external docs, use the autonomous ingestion workflow:

### Phase 1: Scaffold

1. Create skill folder with `SKILL.md` skeleton
2. Create `plan.md` for progress tracking
3. Create `references/` directory

### Phase 2: Build Queue

For each doc link:

- Fetch the page
- Extract internal doc links (avoid nav duplicates)
- Prioritize: concepts → API → operations → troubleshooting

### Phase 3: Ingest Loop

For each page:

1. Fetch **one** page
2. Create `references/<topic>.md` with actionable summary
3. Update `plan.md` checkbox
4. Update `SKILL.md` if it adds a useful recipe/rule

**Do not ask user after each page** — continue autonomously.

### Phase 4: Finalize

- Review `SKILL.md` for completeness
- Ensure practical recipes, not docs mirror
- `plan.md` may be deleted manually after ingestion

## Critical Prohibitions

- Do NOT copy large verbatim chunks from vendor docs (summarize in own words)
- Do NOT write skills in languages other than English
- Do NOT include project-specific secrets, paths, or assumptions
- Do NOT keep `SKILL.md` over 500 lines
- Do NOT skip `name` validation (must match folder name)
- Do NOT use poor descriptions that lack trigger keywords
- Do NOT omit product version when creating skills from documentation

## Version Tracking

When creating or updating a skill from external documentation:

1. Add `version` field in frontmatter for product version:

   ```yaml
   ---
   name: my-skill
   description: "..."
   version: "1.2.3"
   ---
   ```

2. Optionally add `release_date` if known:

   ```yaml
   ---
   name: my-skill
   description: "..."
   version: "1.2.3"
   release_date: "2025-01-21"
   ---
   ```

3. Create `README.md` with:
   - Skill overview (1-2 sentences)
   - Usage section (when to use)
   - Links section (standardized format)

**README.md Links section format:**

```markdown
## Links

- [Documentation](https://example.com/docs)
- [Changelog](https://example.com/changelog)
- [GitHub](https://github.com/org/repo)
- [npm](https://www.npmjs.com/package/name)
```

Include only applicable links. Order: Documentation → Changelog/Releases → GitHub → Package registry.

Example frontmatter:

```yaml
---
name: turso
description: "Turso embedded SQLite database..."
version: "0.4.0"
release_date: "2025-01-05"
---
```

This helps track when the skill was last updated and against which product version.

## Validation Checklist

- [ ] `name` matches folder name
- [ ] `name` is 1-64 chars, lowercase, no `--`
- [ ] `description` is 1-1024 chars, includes keywords
- [ ] `SKILL.md` under 500 lines
- [ ] Documentation in `references/`, templates in `assets/`
- [ ] All text in English

## Scripts

| Script                    | Purpose                                                 |
| ------------------------- | ------------------------------------------------------- |
| `init_skill.py`           | Scaffold new Agent Skill (agentskills.io)               |
| `init_copilot_asset.py`   | Scaffold Copilot-specific assets (instructions, agents) |
| `quick_validate_skill.py` | Validate skill structure                                |
| `package_skill.py`        | Package skill into distributable zip                    |

## Links

- Specification: `references/specification.md`
- Advanced Features: `references/advanced-features.md`
- SKILL.md Templates: `assets/skill-templates.md`
- Docs Ingestion: `references/docs-ingestion.md`
- Official spec: https://agentskills.io/specification
- Claude Code skills: https://code.claude.com/docs/en/skills
