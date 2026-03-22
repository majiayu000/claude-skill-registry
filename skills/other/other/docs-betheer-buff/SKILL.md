---
name: buff-docs
description: This skill should be used when the user asks to "generate documentation", "write docs", "create a README", "document the project", "run /buff:docs", "write API docs", "create a getting started guide", "update the README", or any request for project documentation creation or update.
version: 0.2.0
argument-hint: "[--readme-only] [--full] [--changelog]"
allowed-tools: Read, Glob, Bash, Write, Edit, Agent
---

# buff-docs

The docs skill generates modern, minimal, GitHub-standard documentation. Smart by default — scales scope to project size. Infers style from existing docs. Produces docs that are clean for humans and token-efficient for AI consumers.

## Scope detection (smart default)

Determine output scope before writing anything:

| Condition | Output |
|---|---|
| Source files ≤ 10 | `README.md` only |
| Source files > 10 | `README.md` + `docs/` folder |
| `api/` or `lib/` directory exists | Include API reference |
| Git history available | Include changelog (if `--changelog` flag) |
| `docs/` folder already exists | Update existing docs, match existing style |

Count source files:
```bash
find . -type f \( -name "*.ts" -o -name "*.js" -o -name "*.py" -o -name "*.rs" -o -name "*.go" \) | grep -v node_modules | grep -v dist | wc -l
```

## Style inference

Before writing, check for existing docs:

1. Read existing `README.md` — match heading hierarchy, tone, section order
2. Read `docs/` folder structure — match naming conventions
3. Check `package.json` `"description"` and `"homepage"` fields — use for project summary
4. Read `.buff/plan.md` — use architecture section for technical overview

If nothing exists, apply the buff minimal template (see below).

## README structure (buff default)

```markdown
# [project name]

> [one-line tagline from package.json description or plan summary]

## What it does

[2-4 sentences. What problem does it solve? Who is it for?]

## Installation

\`\`\`bash
[install command — npm install / pip install / cargo add / etc.]
\`\`\`

## Quick start

\`\`\`[language]
[minimal working example — the smallest possible complete usage]
\`\`\`

## Usage

[Core usage patterns — not exhaustive, just the 80% cases]

## API

[Only if the project exports a public API — otherwise omit]

## Configuration

[Only if there are config options — list with defaults]

## Contributing

[1-3 sentences max. Link to CONTRIBUTING.md if it exists.]

## License

[License type and link]
```

Rules:
- No empty sections — omit a section if there's nothing real to put in it
- No boilerplate filler ("this project uses best practices") — every sentence earns its place
- Code examples run on copy-paste — test them mentally before writing
- Use backtick fences with language tags — always
- Headings: H1 for project name only, H2 for sections, H3 for subsections

## Full docs folder structure (`docs/`)

```
docs/
├── README.md          → same as project README (or link to it)
├── getting-started.md → installation + first real task walkthrough
├── api-reference.md   → all public exports, signatures, parameters
└── changelog.md       → version history (only if --changelog flag)
```

### getting-started.md

Walk through the smallest complete task from zero:
1. Install
2. Configure (if needed)
3. First real usage (not "hello world" — something that demonstrates actual value)

### api-reference.md

For each exported function, class, or type:
```markdown
### functionName(param: Type): ReturnType

[One sentence description]

**Parameters**
- `param` — [description, valid values if constrained]

**Returns** — [what it returns, and when it returns different things]

**Example**
\`\`\`typescript
[minimal working example]
\`\`\`
```

Generate from source by reading exported symbols. Do not invent API docs — read the actual signatures.

### changelog.md

Generate from git log if `--changelog` is set:
```bash
git log --oneline --no-merges --pretty=format:"- %s (%h)" v[last-tag]..HEAD
```

Group by type (feat, fix, refactor, docs) from conventional commit prefixes.

## Flags

| Flag | Behavior |
|---|---|
| `/buff:docs` | Smart scope based on project size |
| `/buff:docs --readme-only` | Generate/update README.md only |
| `/buff:docs --full` | Generate full docs/ folder regardless of project size |
| `/buff:docs --changelog` | Include changelog generation from git history |

## Doc quality standards

A good buff doc:
- Can be understood in a single read without prior context
- Has a working code example in the first 30 lines
- Contains zero marketing language ("powerful", "seamless", "robust")
- Uses active voice ("Run the server" not "The server can be run")
- Is scannable — headings and code blocks visible on scroll
- Renders correctly on GitHub (test Mermaid, tables, fenced code)

## AI readability

Docs are written for both humans and AI consumers (LLMs reading the project):
- Keep section headings descriptive and consistent — they become semantic anchors
- Put the most important information first in each section
- Use tables for structured data — they parse cleanly
- Avoid nested bullet lists > 2 levels — they're ambiguous to parse

## Counterfeit integration

Read from `.buff/memory/preferences.json`:
- `communication.verbosity` → controls detail level in docs
- `communication.language` → target language for docs content

## Additional Resources

- **`references/templates.md`** — Full buff docs templates for README, API reference, getting-started
