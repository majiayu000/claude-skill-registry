---
name: skill-creator
description: Interactive assistant that scaffolds new Agent Skills. Use this when the user wants to create, write, or generate a new skill.
---

# Skill Creator

## About
Skills are modular, self-contained packages that extend an agent's capabilities by providing specialized knowledge, workflows, and tools. Think of them as onboarding guides for specific domains or tasks.

### What Skills Provide
1. Specialized workflows for specific domains
2. Tool integrations for file formats or APIs
3. Domain expertise like schemas, business logic, or policies
4. Bundled resources (scripts, references, assets) for complex or repetitive tasks

### Anatomy of a Skill
Every skill consists of a required SKILL.md file and optional bundled resources:

```
skill-name/
├── SKILL.md (required)
│   ├── YAML frontmatter (required)
│   │   ├── name: (required)
│   │   └── description: (required)
│   └── Markdown instructions (required)
└── Bundled Resources (optional)
	├── scripts/    - Executable code (Python/Bash/etc.)
	├── references/ - Documentation intended for in-context loading
	└── assets/     - Files used in output (templates, icons, fonts, etc.)
```

#### SKILL.md (required)
Metadata quality matters. The `name` and `description` in YAML frontmatter determine when the skill triggers. Be specific about what the skill does and when to use it. Use third-person in frontmatter (e.g., "This skill should be used when...").

Example frontmatter (VS Code compatible):

```yaml
---
name: pdf-rotator
description: This skill should be used when the user needs to rotate or reorient PDF pages.
---
```

#### Bundled Resources (optional)

##### Scripts (`scripts/`)
Executable code for tasks that need deterministic reliability or are repeatedly rewritten.

- When to include: When the same code is being rewritten repeatedly or deterministic reliability is needed
- Example: `scripts/rotate_pdf.py` for PDF rotation
- Benefits: Token efficient, deterministic, can be executed without loading into context
- Note: Scripts may still need to be read for patching or environment-specific adjustments

##### References (`references/`)
Documentation intended to be loaded as needed into context to inform the process.

- When to include: For documentation the skill should reference while working
- Examples: `references/schema.md`, `references/policies.md`, `references/api_docs.md`
- Use cases: Schemas, API docs, domain knowledge, policies, detailed workflow guides
- Benefits: Keeps SKILL.md lean; load only when needed
- Best practice: If files are large (over 10k words), include grep search patterns in SKILL.md
- Avoid duplication: Put details in either SKILL.md or references, not both

##### Assets (`assets/`)
Files not intended to be loaded into context, but used in the output.

- When to include: When the skill needs files for the final output
- Examples: `assets/logo.png`, `assets/slides.pptx`, `assets/frontend-template/`, `assets/font.ttf`
- Use cases: Templates, images, icons, boilerplate code, fonts, sample documents
- Benefits: Separates output resources from documentation and avoids context bloat

### Progressive Disclosure Design Principle
Skills use a three-level loading system to manage context:

1. Metadata (name + description) - Always in context (~100 words)
2. SKILL.md body - Loaded when the skill triggers (<5k words)
3. Bundled resources - Loaded as needed (scripts can execute without context load)

## Skill Creation Process
Follow the steps in order and skip only when clearly not applicable.

### Step 1: Understand the Skill with Concrete Examples
Clarify how the skill will be used and gather concrete examples. Ask only a few questions at a time and follow up as needed. Conclude when you have a clear sense of what should trigger the skill and what it should accomplish.

Trigger-example pairs (compact):
- Trigger: "Rotate this PDF 90 degrees." -> Expected: use a PDF rotation script and return updated file.
- Trigger: "Create a dashboard starter in React." -> Expected: copy boilerplate assets and explain how to run.
- Trigger: "Summarize this vendor contract." -> Expected: reference a policy doc and produce a structured summary.

### Step 2: Plan the Reusable Skill Contents
Analyze the examples to identify reusable resources:

1. Consider how to execute each example from scratch
2. Identify scripts, references, and assets that would help when repeating the workflows

Create a list of reusable resources to include.

### Step 3: Initialize the Skill
If creating a new skill, always run the initialization script:

```bash
scripts/init_skill.py <skill-name> --path <output-directory>
```

The script:
- Creates the skill directory at the specified path
- Generates a SKILL.md template with frontmatter and TODO placeholders
- Creates example resource directories and example files

Customize or remove the example files after initialization.

### Step 4: Edit the Skill
Remember the skill is for another agent to use. Include non-obvious, procedural knowledge and reusable assets that improve execution.

#### Start with Reusable Contents
Implement the reusable resources first: `scripts/`, `references/`, and `assets/`. Request user input for assets or documentation if needed. Delete any unused example files or directories.

#### Update SKILL.md
Writing style guidance:

- Frontmatter `name` and `description`: third-person phrasing
- Body: imperative/infinitive form (verb-first instructions) and objective language

To complete SKILL.md, answer:

1. What is the purpose of the skill?
2. When should the skill be used?
3. How should the skill be used in practice, including how to use reusable resources?

### Step 5: Package the Skill
Package the skill into a distributable zip after validation:

```bash
scripts/package_skill.py <path/to/skill-folder>
```

Optional output directory:

```bash
scripts/package_skill.py <path/to/skill-folder> ./dist
```

The packaging script:
1. Validates frontmatter format and required fields
2. Validates naming conventions and directory structure
3. Validates description completeness and quality
4. Validates file organization and resource references
5. Creates a zip named after the skill if validation passes

If validation fails, fix errors and re-run packaging.

Example output (happy path):
```
Validating skill at skills/my-new-skill...
Validation passed.
Packaging skill -> dist/my-new-skill.zip
Done.
```

Common validation errors (fix and retry):
- Description missing trigger keywords (add "use/when" phrasing)
- Name is not kebab-case or does not match folder name
- Frontmatter contains disallowed keys or invalid YAML
- SKILL.md exceeds 500 lines

### Step 6: Iterate
Iteration workflow:
1. Use the skill on real tasks
2. Notice struggles or inefficiencies
3. Identify how SKILL.md or resources should change
4. Implement changes and test again

## Validation Rules
- Name must be kebab-case, 1-80 characters, and match the folder name.
- Frontmatter must be valid YAML wrapped in --- lines.
- Required fields: name, description.
- VS Code uses only `name` and `description`. Keep names <= 64 characters for VS Code compatibility.
- Description must be specific (1-1024 chars), include trigger keywords (use/when), and avoid XML tags.
- Avoid reserved words in name/description (claude, anthropic).
- Keep SKILL.md under 500 lines.

## Template Usage
- Use templates/basic.md for instruction-only skills.
- Use templates/advanced.md for skills that require scripts.
- Customize placeholders and remove unused sections.

## Best Practices
- Progressive disclosure: only the description is always in context. Make it precise.
- Put usage triggers in the description; use the body for details and examples.
- Context efficiency: keep SKILL.md short; move details to references/.
- Determinism: if accuracy must be exact, include scripts and document how to run them.
- Avoid duplication: do not repeat large reference content in SKILL.md.
- Avoid time-sensitive instructions or timestamps.
- Keep references one level deep (references/ only; no nested folders).
- Do not create extra README files inside skill folders.
- If keeping skills outside `.github/skills/`, document the `chat.agentSkillsLocations` setting so VS Code can discover them.

## Additional Links
- Templates: templates/basic.md, templates/advanced.md
- Example skill: ../test-skill/SKILL.md
- Reference: https://github.com/ComposioHQ/awesome-claude-skills/tree/master/skill-creator

## Toolkit Scripts (Optional)
If this repository includes toolkit scripts at scripts/:
- Run scripts/init_skill.py to scaffold a skill quickly.
- Run scripts/validate_skill.py to check structure and frontmatter.
- Run scripts/package_skill.py to build a zip for distribution.
