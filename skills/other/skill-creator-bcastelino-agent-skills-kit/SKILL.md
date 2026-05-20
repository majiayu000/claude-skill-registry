---
name: skill-creator
description: Interactive guide for creating, scaffolding, and iterating on Agent Skills. Use when the user wants to build a skill, write a SKILL.md, generate frontmatter, define trigger phrases, validate, package, or distribute a skill.
license: MIT
metadata: {version: "1.0.0", tags: [skill-authoring]}
---

# Skill Creator

## About
A skill is a folder containing `SKILL.md` (required instructions with YAML frontmatter) and optional bundled resources. Skills teach Claude how to handle specific tasks or workflows, eliminating the need to re-explain preferences, processes, and domain expertise in every conversation.

Skills are powerful when you have repeatable workflows — generating consistent documents, conducting research with a standard methodology, orchestrating multi-step processes, or providing workflow guidance on top of MCP integrations.

### Use Case Categories
Skills fall into three common categories:

**Category 1: Document & Asset Creation** — creating consistent, high-quality output (documents, presentations, code, designs).
- Key techniques: embedded style guides, template structures, quality checklists
- No external tools required; uses Claude's built-in capabilities

**Category 2: Workflow Automation** — multi-step processes that benefit from consistent methodology.
- Key techniques: step-by-step workflow with validation gates, iterative refinement loops
- This skill (skill-creator) is a Category 2 example

**Category 3: MCP Enhancement** — workflow guidance layered on top of an MCP server's tool access.
- Key techniques: multi-MCP call coordination, embedded domain expertise, error handling for MCP failures

### Anatomy of a Skill

```
skill-name/
├── SKILL.md         # Required — instructions + YAML frontmatter
├── scripts/         # Optional — executable code (Python, Bash, etc.)
├── references/      # Optional — documentation loaded into context as needed
└── assets/          # Optional — templates, fonts, icons used in output
```

#### SKILL.md (required)
The YAML frontmatter is how Claude decides whether to load your skill. Get it right.

**Minimal required format:**
```yaml
---
name: your-skill-name
description: What it does. Use when user asks to [specific phrases].
---
```

**Full example with optional fields:**
```yaml
---
name: pdf-rotator
description: Rotates and reorients PDF pages. Use when the user says "rotate PDF", uploads a .pdf and asks to fix page orientation, or needs portrait/landscape conversion.
license: MIT
compatibility: Requires Python 3.9+ and pypdf
metadata: {version: "1.0.0", author: YourName, tags: [pdf-processing, file-manipulation]}
---
```

**Description field structure:** `[What it does] + [When to use it] + [Key capabilities]`

Good descriptions — specific, trigger-focused:
```yaml
# Good — includes trigger phrases users would actually say
description: Manages Linear project workflows including sprint planning and task creation. Use when user mentions "sprint", "Linear tasks", "project planning", or asks to "create tickets".

# Good — mentions relevant file types
description: Analyzes Figma design files and generates developer handoff docs. Use when user uploads .fig files or asks for "design specs" or "design-to-code handoff".
```

Bad descriptions — vague or missing triggers:
```yaml
# Bad — too vague
description: Helps with projects.

# Bad — missing triggers
description: Creates sophisticated multi-page documentation systems.
```

**Security restrictions:**
- Never include XML angle brackets (`<` `>`) — YAML is injected into Claude's system prompt; malicious content can hijack instructions
- Never use `claude` or `anthropic` in the `name` field (reserved words)
- Do not embed executable code or dynamic expressions in YAML values

#### Bundled Resources (optional)

##### `scripts/`
Executable code for tasks requiring deterministic reliability or repeated execution.

- Include when the same logic is rewritten across conversations or exact accuracy is required
- Code is deterministic; language instructions are not — prefer scripts for critical validations
- Reference with exact commands: `python scripts/validate.py --input {filename}`

##### `references/`
Documentation loaded into context as needed.

- Include schemas, API docs, domain knowledge, policies, workflow guides
- For files exceeding 10k words, add grep/search patterns in SKILL.md to guide context loading
- Keep references one level deep — no nested subdirectories
- Avoid duplicating content between SKILL.md and reference files

##### `assets/`
Files used in output, not loaded into context.

- Include templates, images, icons, boilerplate code, fonts, sample documents
- Example: `assets/report-template.md`, `assets/logo.png`, `assets/frontend-template/`

### Core Design Principles

**Progressive Disclosure** — Three loading levels minimize token usage:
1. YAML frontmatter — always loaded; enables Claude to decide when to trigger the skill
2. SKILL.md body — loaded when skill is relevant; contains full instructions (`< 5k words`)
3. Bundled resources — loaded only as needed; scripts can execute without being loaded

**Composability** — Claude can load multiple skills simultaneously. Design skills to work alongside others rather than assuming exclusive context.

**Portability** — Skills work identically across Claude.ai, Claude Code, and the API without modification. Document required dependencies in the `compatibility` field.

---

## Skill Creation Process
Follow the steps in order; skip only when clearly not applicable.

### Step 1: Define Use Cases
Identify 2–3 concrete use cases before writing any instructions. For each use case, answer:
- What does the user want to accomplish?
- What multi-step workflow does this require?
- Which tools are needed (built-in, scripts, or MCP)?
- What domain knowledge or best practices should be embedded?

**Trigger-example pairs:**
- Trigger: "Rotate this PDF 90 degrees." → Expected: run `scripts/rotate_pdf.py`, return updated file.
- Trigger: "Create a dashboard starter in React." → Expected: copy boilerplate from `assets/`, explain how to run.
- Trigger: "Summarize this vendor contract." → Expected: load `references/policies.md`, produce structured summary.

**Define success criteria before building:**
- Quantitative: skill triggers on 90%+ of relevant queries; workflow completes in target tool calls; 0 failed API calls per workflow
- Qualitative: users don't need to redirect Claude; consistent results across sessions; new users succeed on first try

### Step 2: Plan Skill Contents
Identify the skill's category (Document & Asset Creation, Workflow Automation, or MCP Enhancement) and list reusable resources:

1. Walk through each use case and identify what scripts, references, or assets it needs
2. Flag steps requiring deterministic accuracy → bundle as scripts
3. Flag knowledge reusable across conversations → bundle as references

### Step 3: Initialize the Skill
Run the initialization script for new skills:

```bash
python scripts/init_skill.py <skill-name> --path <output-directory>
```

The script creates the skill directory with a SKILL.md template and example resource directories. Remove unused example files after initialization.

### Step 4: Write the Skill

#### Implement Resources First
Build `scripts/`, `references/`, and `assets/` before finalizing SKILL.md. Request user-provided assets or documentation explicitly before proceeding.

#### Write SKILL.md Body
Answer these questions to complete SKILL.md:
1. What is the purpose of the skill?
2. When exactly should it trigger? (Include specific phrases users would say.)
3. What are the step-by-step instructions?
4. How should bundled resources be invoked?

**Writing style:**
- Frontmatter: third-person ("This skill should be used when...")
- Body: imperative, verb-first ("Fetch", "Validate", "Create" — not "You should" or "Remember to")
- Put critical instructions at the top; mark must-follow steps with `CRITICAL:`
- Reference scripts with exact commands: `python scripts/validate.py --input {filename}`
- Reference documentation explicitly: "Consult `references/api-patterns.md` for rate limiting guidance before writing queries."
- Move detailed docs to `references/`; keep SKILL.md focused on core workflow

**Include error handling:**
```markdown
## Common Issues

### [Error Message]
Cause: [Why it happens]
Solution: [How to fix]
```

### Step 5: Test

#### Triggering Tests
Run 10–20 queries to verify when the skill loads:

| Test type | Goal |
|-----------|------|
| Should trigger | Obvious phrasings, paraphrased requests, file-type mentions |
| Should NOT trigger | Unrelated queries, overlapping skill domains |

Debug under-triggering: ask Claude "When would you use the [skill name] skill?" — it quotes the description back. Adjust based on missing keywords.

Debug over-triggering: add negative triggers to the description:
```yaml
description: Advanced data analysis for CSV files. Use for statistical modeling. Do NOT use for simple data exploration (use the data-viz skill instead).
```

#### Functional Tests
Verify the skill produces correct outputs:
- Confirm valid outputs are generated for the defined use cases
- Confirm tool/MCP calls succeed without errors
- Confirm error handling works for defined edge cases

### Step 6: Validate and Package
Run the validator before packaging:

```bash
python scripts/validate_skill.py <path/to/skill>
```

Then package into a distributable zip:

```bash
python scripts/package_skill.py <path/to/skill-folder>

# Optional output directory:
python scripts/package_skill.py <path/to/skill-folder> ./dist
```

The packaging script runs validation then creates `dist/<skill-name>.zip`.

**Common validation errors:**
- Description missing trigger keywords → add "use/when" phrasing
- Name not kebab-case or doesn't match folder name → rename both
- Unsupported frontmatter keys → only `name`, `description`, `license`, `compatibility`, `allowed-tools`, `metadata` are allowed
- SKILL.md exceeds 500 lines → move content to `references/`

### Step 7: Distribute
Host the skill on GitHub with a public repo and a clear README at the repo level. **Do not put a README.md inside the skill folder** — all documentation goes in SKILL.md or `references/`.

For MCP-enhanced skills, add a section to your MCP documentation that:
- Links to the skill
- Explains the value of using MCP + skill together
- Provides a quick-start example prompt

### Step 8: Iterate
Skills are living documents. Iterate based on real usage signals:

| Signal | Likely Cause | Fix |
|--------|-------------|-----|
| Skill doesn't trigger | Description too generic | Add specific trigger phrases, include keywords users actually say |
| Skill triggers too often | Description too broad | Add negative triggers; be more specific about scope |
| Instructions not followed | Instructions verbose or buried | Move details to `references/`; put critical steps first; use `CRITICAL:` headers |
| Inconsistent results | Relying on language for exact steps | Bundle a script; code is deterministic, language isn't |

Iterate on a single challenging task until Claude succeeds, then extract the winning approach into the skill. This gives faster signal than broad testing.

---

## Validation Rules

| Rule | Requirement |
|------|-------------|
| Name | kebab-case, 1–64 chars, matches folder name exactly |
| Name | No reserved words (`claude`, `anthropic`) |
| Description | 1–1024 chars, includes `use` or `when`, no XML tags |
| Frontmatter | Valid YAML wrapped in `---` lines |
| Frontmatter keys | Only `name`, `description`, `license`, `compatibility`, `allowed-tools`, `metadata` |
| `metadata.version` | Semantic versioning (`X.Y.Z`) if provided |
| `metadata.tags` | List of kebab-case strings if provided |
| SKILL.md | 500 lines or fewer; exactly named `SKILL.md` (case-sensitive) |
| Folder name | kebab-case only — no spaces, underscores, or capitals |

Run `python scripts/validate_skill.py <path/to/skill>` to check all rules before packaging.

---

## Best Practices
- **Triggers in description**: the description is the only content always in context — make it precise with specific phrases users would say
- **Progressive disclosure**: keep SKILL.md focused on core workflow; move detailed docs to `references/`
- **Specificity**: avoid vague descriptions — include actions, file types, and concrete trigger phrases
- **Determinism**: for steps where exact accuracy matters, bundle scripts rather than relying on language instructions
- **No duplication**: put content in SKILL.md or `references/`, not both
- **No time-sensitive content**: avoid timestamps or "as of [date]" phrasing
- **Flat references**: keep `references/` one level deep — no nested subdirectories
- **No README inside skill folder**: all documentation goes in SKILL.md or `references/`
- **Negative triggers**: if the skill over-triggers, add "Do NOT use for..." to the description
- **Composability**: assume other skills may be active simultaneously — don't write instructions that conflict with general Claude behavior

## Template Usage
- Use `templates/basic.md` for instruction-only skills (no scripts needed)
- Use `templates/advanced.md` for skills that bundle scripts or MCP workflows
- Customize placeholders and remove unused sections after initializing

## Additional Links
- Templates: `templates/basic.md`, `templates/advanced.md`
- Example skill: `../test-skill/SKILL.md`
- Skill creator skill: https://github.com/ComposioHQ/awesome-claude-skills/tree/master/skill-creator
- Public skills repository: https://github.com/anthropics/skills
