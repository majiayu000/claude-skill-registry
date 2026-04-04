---
name: creating-skills
description: |
  Guides creation of effective Agent Skills with proper structure and validation.
  Use when users want to create a new skill, update an existing skill, or need
  guidance on skill design patterns, SKILL.md format, or verify.py implementation.
  NOT when just using existing skills (use those skills directly).
---

# Skill Creator

This skill provides guidance for creating effective skills.

## About Skills

Skills are modular, self-contained packages that extend Claude's capabilities by providing specialized knowledge, workflows, and tools. Think of them as "onboarding guides" for specific domains or tasks—they transform Claude from a general-purpose agent into a specialized agent equipped with procedural knowledge that no model can fully possess.

### What Skills Provide

1. Specialized workflows - Multi-step procedures for specific domains
2. Tool integrations - Instructions for working with specific file formats or APIs
3. Domain expertise - Company-specific knowledge, schemas, business logic
4. Bundled resources - Scripts, references, and assets for complex and repetitive tasks

## Core Principles

### Concise is Key

The context window is a public good. Skills share the context window with everything else Claude needs: system prompt, conversation history, other Skills' metadata, and the actual user request.

**Default assumption: Claude is already very smart.** Only add context Claude doesn't already have. Challenge each piece of information: "Does Claude really need this explanation?" and "Does this paragraph justify its token cost?"

Prefer concise examples over verbose explanations.

### Set Appropriate Degrees of Freedom

Match the level of specificity to the task's fragility and variability:

**High freedom (text-based instructions)**: Use when multiple approaches are valid, decisions depend on context, or heuristics guide the approach.

**Medium freedom (pseudocode or scripts with parameters)**: Use when a preferred pattern exists, some variation is acceptable, or configuration affects behavior.

**Low freedom (specific scripts, few parameters)**: Use when operations are fragile and error-prone, consistency is critical, or a specific sequence must be followed.

Think of Claude as exploring a path: a narrow bridge with cliffs needs specific guardrails (low freedom), while an open field allows many routes (high freedom).

### Anatomy of a Skill

Every skill consists of a required SKILL.md file and optional bundled resources:

```
skill-name/
├── SKILL.md (required)
│   ├── YAML frontmatter metadata (required)
│   │   ├── name: (required)
│   │   └── description: (required)
│   └── Markdown instructions (required)
└── Bundled Resources (optional)
    ├── scripts/          - Executable code (Python/Bash/etc.)
    ├── references/       - Documentation intended to be loaded into context as needed
    └── assets/           - Files used in output (templates, icons, fonts, etc.)
```

#### SKILL.md (required)

Every SKILL.md consists of:

- **Frontmatter** (YAML): Contains `name` and `description` fields. These are the only fields that Claude reads to determine when the skill gets used, thus it is very important to be clear and comprehensive in describing what the skill is, and when it should be used.
- **Body** (Markdown): Instructions and guidance for using the skill. Only loaded AFTER the skill triggers (if at all).

#### Bundled Resources (optional)

##### Scripts (`scripts/`)

Executable code (Python/Bash/etc.) for tasks that require deterministic reliability or are repeatedly rewritten.

- **When to include**: When the same code is being rewritten repeatedly or deterministic reliability is needed
- **Example**: `scripts/rotate_pdf.py` for PDF rotation tasks
- **Benefits**: Token efficient, deterministic, may be executed without loading into context
- **Note**: Scripts may still need to be read by Claude for patching or environment-specific adjustments

##### References (`references/`)

Documentation and reference material intended to be loaded as needed into context to inform Claude's process and thinking.

- **When to include**: For documentation that Claude should reference while working
- **Examples**: `references/finance.md` for financial schemas, `references/api_docs.md` for API specifications
- **Benefits**: Keeps SKILL.md lean, loaded only when Claude determines it's needed
- **Best practice**: If files are large (>10k words), include grep search patterns in SKILL.md

##### Assets (`assets/`)

Files not intended to be loaded into context, but rather used within the output Claude produces.

- **When to include**: When the skill needs files that will be used in the final output
- **Examples**: `assets/logo.png` for brand assets, `assets/slides.pptx` for PowerPoint templates
- **Benefits**: Separates output resources from documentation, enables Claude to use files without loading them into context

#### What to Not Include in a Skill

A skill should only contain essential files that directly support its functionality. Do NOT create extraneous documentation or auxiliary files, including:

- README.md
- INSTALLATION_GUIDE.md
- QUICK_REFERENCE.md
- CHANGELOG.md

The skill should only contain the information needed for an AI agent to do the job at hand.

### Progressive Disclosure Design Principle

Skills use a three-level loading system to manage context efficiently:

1. **Metadata (name + description)** - Always in context (~100 tokens)
2. **SKILL.md body** - When skill triggers (<5000 tokens)
3. **Bundled resources** - As needed by Claude (unlimited because scripts can be executed without reading into context window)

Keep SKILL.md body under 500 lines. Split content into separate files when approaching this limit.

**Key principle:** When a skill supports multiple variations, keep only the core workflow in SKILL.md. Move variant-specific details into separate reference files.

## Skill Creation Process

Skill creation involves these steps:

1. Understand the skill with concrete examples
2. Plan reusable skill contents (scripts, references, assets)
3. Initialize the skill (run init_skill.py)
4. Edit the skill (implement resources and write SKILL.md)
5. Package the skill (run package_skill.py)
6. Iterate based on real usage

### Step 1: Understanding the Skill with Concrete Examples

To create an effective skill, clearly understand concrete examples of how the skill will be used. For example, when building an image-editor skill, relevant questions include:

- "What functionality should the image-editor skill support?"
- "Can you give some examples of how this skill would be used?"
- "What would a user say that should trigger this skill?"

Conclude this step when there is a clear sense of the functionality the skill should support.

### Step 2: Planning the Reusable Skill Contents

To turn concrete examples into an effective skill, analyze each example by:

1. Considering how to execute on the example from scratch
2. Identifying what scripts, references, and assets would be helpful when executing these workflows repeatedly

Example: When building a `pdf-editor` skill to handle queries like "Help me rotate this PDF," the analysis shows:
1. Rotating a PDF requires re-writing the same code each time
2. A `scripts/rotate_pdf.py` script would be helpful to store in the skill

### Step 3: Initializing the Skill

When creating a new skill from scratch, always run the `init_skill.py` script:

```bash
python3 scripts/init_skill.py <skill-name> --path <output-directory>
```

The script:
- Creates the skill directory at the specified path
- Generates a SKILL.md template with proper frontmatter and TODO placeholders
- Creates example resource directories: `scripts/`, `references/`, and `assets/`

### Step 4: Edit the Skill

Remember that the skill is being created for another instance of Claude to use. Include information that would be beneficial and non-obvious to Claude.

#### Frontmatter

Write the YAML frontmatter with `name` and `description`:

- `name`: The skill name (gerund form preferred: `deploying-*`, `creating-*`, `fetching-*`)
- `description`: This is the primary triggering mechanism for your skill

**CRITICAL: Description = When to Use, NOT What It Does**

The description should ONLY describe triggering conditions. Do NOT summarize the skill's process or workflow in the description.

**Why this matters:** When a description summarizes the skill's workflow, Claude may follow the description instead of reading the full skill content. A description saying "dispatches subagent per task with code review" caused Claude to do ONE review, even though the skill body specified TWO reviews. When changed to just triggering conditions, Claude correctly read and followed the full skill.

```yaml
# BAD: Summarizes workflow - Claude may follow this instead of reading skill
description: Use when executing plans - dispatches subagent per task with code review

# BAD: Too much process detail
description: Use for TDD - write test first, watch it fail, write minimal code

# GOOD: Just triggering conditions
description: Use when executing implementation plans with independent tasks

# GOOD: Triggering conditions with exclusion
description: |
  Use when users need to create new documents or work with tracked changes.
  NOT when converting between formats (use converting-documents skill).
```

**Description checklist:**
- Start with "Use when..." to focus on triggering conditions
- Include symptoms, situations, contexts that signal the skill applies
- Add "NOT when [exclusion]" if collision with other skills possible
- NEVER summarize the skill's process or workflow
- Max 1024 characters

#### Body

Write instructions for using the skill and its bundled resources.

### Step 5: Packaging a Skill

Once development is complete, package the skill:

```bash
python3 scripts/package_skill.py <path/to/skill-folder>
```

The packaging script will:
1. **Validate** the skill automatically
2. **Package** the skill if validation passes, creating a .skill file

### Step 6: Iterate

After testing the skill, users may request improvements. Iteration workflow:

1. Use the skill on real tasks
2. Notice struggles or inefficiencies
3. Identify how SKILL.md or bundled resources should be updated
4. Implement changes and test again

## Verification

Run: `python3 scripts/verify.py`

Expected: `✓ creating-skills valid`

To validate another skill:
```bash
python3 scripts/verify.py /path/to/skill-folder
```

## If Verification Fails

1. Run diagnostic: `python3 scripts/verify.py /path/to/skill --verbose`
2. Check: YAML frontmatter, name format, description trigger
3. Fix: Ensure "Use when" is in description, name is gerund form
4. **Stop and report** if still failing - do not proceed with downstream steps

## References

See [references/design-patterns.md](references/design-patterns.md) for workflow patterns and MCP output discipline guidelines.