---
name: skill-creator
description: Create, update, or validate SKILL.md files and skill packages. Use this skill when users ask to "create a skill", "make a new skill", "add a skill", "write a skill", "update a skill", "validate skill", "check skill quality", "review skill", "audit skills", or work with .claude/skills/ directory contents. Supports three operations: (1) CREATE - new skill from scratch, (2) UPDATE - modify existing skill, (3) VALIDATE - audit skill against SkillsBench best practices. NOT for UI/frontend design work - only for authoring skill definition files that extend Claude's capabilities.
---

# Skill Creator

Manage skills through three operations: **Create**, **Update**, and **Validate**.

## Operation Selection

Determine operation from user intent:

| User Intent                                                     | Operation | Section                                 |
| --------------------------------------------------------------- | --------- | --------------------------------------- |
| "create skill", "new skill", "add skill", "write skill"         | CREATE    | [Creating Skills](#creating-skills)     |
| "update skill", "modify skill", "change skill", "improve skill" | UPDATE    | [Updating Skills](#updating-skills)     |
| "validate skill", "check skill", "review skill", "audit skill"  | VALIDATE  | [Validating Skills](#validating-skills) |

---

## About Skills

Skills are modular, self-contained packages that extend Claude's capabilities by providing specialized knowledge, workflows, and tools. They transform Claude from a general-purpose agent into a specialized agent equipped with procedural knowledge.

### What Skills Provide

1. **Specialized workflows** - Multi-step procedures for specific domains
2. **Tool integrations** - Instructions for working with specific file formats or APIs
3. **Domain expertise** - Company-specific knowledge, schemas, business logic
4. **Bundled resources** - Scripts, references, and assets for complex and repetitive tasks

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

---

## Creating Skills

Skill creation involves these steps:

1. Understand the skill with concrete examples
2. Plan reusable skill contents (scripts, references, assets)
3. Initialize the skill directory
4. Edit the skill (implement resources and write SKILL.md)
5. Validate the skill (run validation checklist)
6. Iterate based on real usage

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
- **Examples**: `references/finance.md` for financial schemas, `references/mnda.md` for company NDA template, `references/policies.md` for company policies, `references/api_docs.md` for API specifications
- **Use cases**: Database schemas, API documentation, domain knowledge, company policies, detailed workflow guides
- **Benefits**: Keeps SKILL.md lean, loaded only when Claude determines it's needed
- **Best practice**: If files are large (>10k words), include grep search patterns in SKILL.md
- **Avoid duplication**: Information should live in either SKILL.md or references files, not both. Prefer references files for detailed information unless it's truly core to the skill—this keeps SKILL.md lean while making information discoverable without hogging the context window.

##### Assets (`assets/`)

Files not intended to be loaded into context, but rather used within the output Claude produces.

- **When to include**: When the skill needs files that will be used in the final output
- **Examples**: `assets/logo.png` for brand assets, `assets/slides.pptx` for PowerPoint templates, `assets/frontend-template/` for HTML/React boilerplate, `assets/font.ttf` for typography
- **Use cases**: Templates, images, icons, boilerplate code, fonts, sample documents that get copied or modified
- **Benefits**: Separates output resources from documentation, enables Claude to use files without loading them into context

#### What to Not Include in a Skill

A skill should only contain essential files that directly support its functionality. Do NOT create extraneous documentation or auxiliary files, including:

- README.md
- INSTALLATION_GUIDE.md
- QUICK_REFERENCE.md
- CHANGELOG.md
- etc.

The skill should only contain the information needed for an AI agent to do the job at hand.

### Progressive Disclosure Design Principle

Skills use a three-level loading system to manage context efficiently:

1. **Metadata (name + description)** - Always in context (~100 words)
2. **SKILL.md body** - When skill triggers (<5k words)
3. **Bundled resources** - As needed by Claude (Unlimited because scripts can be executed without reading into context window)

#### Progressive Disclosure Patterns

Keep SKILL.md body to the essentials and under 500 lines to minimize context bloat. Split content into separate files when approaching this limit.

**Key principle:** When a skill supports multiple variations, frameworks, or options, keep only the core workflow and selection guidance in SKILL.md. Move variant-specific details into separate reference files.

### Step 1: Understanding the Skill with Concrete Examples

Skip this step only when the skill's usage patterns are already clearly understood.

To create an effective skill, clearly understand concrete examples of how the skill will be used. This understanding can come from either direct user examples or generated examples that are validated with user feedback.

For example, when building an image-editor skill, relevant questions include:

- "What functionality should the image-editor skill support? Editing, rotating, anything else?"
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

Example: When building a `big-query` skill to handle queries like "How many users have logged in today?" the analysis shows:

1. Querying BigQuery requires re-discovering the table schemas and relationships each time
2. A `references/schema.md` file documenting the table schemas would be helpful

### Step 3: Initializing the Skill

When creating a new skill from scratch, always run the `init_skill.py` script:

```bash
scripts/init_skill.py <skill-name> --path <output-directory>
```

The script:

- Creates the skill directory at the specified path
- Generates a SKILL.md template with proper frontmatter and TODO placeholders
- Creates example resource directories: `scripts/`, `references/`, and `assets/`
- Adds example files in each directory that can be customized or deleted

### Step 4: Edit the Skill

When editing the skill, remember that the skill is being created for another instance of Claude to use. Include information that would be beneficial and non-obvious to Claude.

#### Learn Proven Design Patterns

Consult these helpful guides based on your skill's needs:

- **Multi-step processes**: See references/workflows.md for sequential workflows and conditional logic
- **Specific output formats or quality standards**: See references/output-patterns.md for template and example patterns

#### Start with Reusable Skill Contents

Begin implementation with the reusable resources identified: `scripts/`, `references/`, and `assets/` files.

Added scripts must be tested by actually running them to ensure there are no bugs and that the output matches what is expected.

Any example files and directories not needed for the skill should be deleted.

#### Update SKILL.md

**Writing Guidelines:** Always use imperative/infinitive form.

##### Frontmatter

Write the YAML frontmatter with `name` and `description`:

- `name`: The skill name
- `description`: This is the primary triggering mechanism for your skill, and helps Claude understand when to use the skill.
  - Include both what the Skill does and specific triggers/contexts for when to use it.
  - Include all "when to use" information here - Not in the body. The body is only loaded after triggering, so "When to Use This Skill" sections in the body are not helpful to Claude.

Do not include any other fields in YAML frontmatter.

##### Body

Write instructions for using the skill and its bundled resources.

### Step 5: Validate the Skill

Before finalizing, run the validation checklist from the [Validating Skills](#validating-skills) section.

Quick validation checks:

- [ ] SKILL.md exists with valid frontmatter
- [ ] `name` matches directory name
- [ ] `description` includes triggers and when-to-use
- [ ] Body has actionable instructions
- [ ] No orphaned files in skill directory
- [ ] All referenced resources exist

For comprehensive validation, use the full checklist in [Validating Skills](#validating-skills).

### Step 6: Iterate

After testing the skill, users may request improvements.

**Iteration workflow:**

1. Use the skill on real tasks
2. Notice struggles or inefficiencies
3. Identify how SKILL.md or bundled resources should be updated
4. Implement changes and test again

---

## Updating Skills

When updating an existing skill:

### Step 1: Analyze Current Skill

1. Read the current SKILL.md
2. Identify what needs to change
3. Check if change affects description (triggers) or body (instructions)

### Step 2: Determine Change Type

| Change Type     | Impact | Action                                    |
| --------------- | ------ | ----------------------------------------- |
| Trigger change  | High   | Update description in frontmatter         |
| Workflow change | Medium | Update body instructions                  |
| Add capability  | Medium | Add new section or reference file         |
| Bug fix         | Low    | Fix specific instructions                 |
| Clarification   | Low    | Improve wording without changing behavior |

### Step 3: Apply Changes

- Preserve existing structure
- Keep description comprehensive with all triggers
- Maintain progressive disclosure pattern
- Test changes against concrete examples

---

## Validating Skills

Audit skills against SkillsBench best practices and quality standards.

### Validation Workflow

1. **Scan skills** - List all skills in `.claude/skills/`
2. **Check each skill** - Apply validation checklist
3. **Generate report** - Summarize findings by severity
4. **Recommend fixes** - Prioritized action items

### Validation Checklist

#### Structure (Required)

| Check                       | Severity    | Criteria                              |
| --------------------------- | ----------- | ------------------------------------- |
| SKILL.md exists             | 🔴 CRITICAL | File must exist in skill directory    |
| YAML frontmatter            | 🔴 CRITICAL | Valid YAML between `---` markers      |
| `name` field                | 🔴 CRITICAL | Must match directory name             |
| `description` field         | 🔴 CRITICAL | Must be present and non-empty         |
| No extra frontmatter fields | 🟡 MEDIUM   | Only `name` and `description` allowed |

#### Description Quality (Triggers)

| Check                     | Severity    | Criteria                            |
| ------------------------- | ----------- | ----------------------------------- |
| Includes what skill does  | 🔴 CRITICAL | Clear statement of purpose          |
| Includes trigger keywords | 🔴 CRITICAL | Words/phrases that invoke the skill |
| Includes when to use      | 🟡 MEDIUM   | Context/scenarios for usage         |
| Under 200 words           | 🟡 MEDIUM   | Concise for context efficiency      |
| No "When to Use" in body  | 🟡 MEDIUM   | All triggers belong in description  |

#### Body Quality (Instructions)

| Check                       | Severity    | Criteria                           |
| --------------------------- | ----------- | ---------------------------------- |
| Has actionable instructions | 🔴 CRITICAL | Not just explanation, but workflow |
| Uses imperative form        | 🟡 MEDIUM   | "Do X" not "You should do X"       |
| Under 500 lines             | 🟡 MEDIUM   | Use references for overflow        |
| No duplicate content        | 🟡 MEDIUM   | Information in one place only      |
| Examples over explanations  | 🟢 LOW      | Prefer concrete over abstract      |

#### Resource Organization

| Check                  | Severity  | Criteria                      |
| ---------------------- | --------- | ----------------------------- |
| No README.md           | 🟡 MEDIUM | Not needed for skills         |
| No CHANGELOG.md        | 🟡 MEDIUM | Not needed for skills         |
| scripts/ tested        | 🟡 MEDIUM | Scripts should be runnable    |
| references/ referenced | 🟡 MEDIUM | Must be mentioned in SKILL.md |
| No orphaned files      | 🟢 LOW    | All files should be used      |

#### SkillsBench Best Practices

| Check                     | Severity  | Criteria                             |
| ------------------------- | --------- | ------------------------------------ |
| Composable design         | 🟡 MEDIUM | Can work with other skills           |
| Appropriate freedom level | 🟡 MEDIUM | Specificity matches task fragility   |
| Progressive disclosure    | 🟡 MEDIUM | Heavy content in references          |
| Context-efficient         | 🟢 LOW    | No verbose explanations              |
| Error-free content        | 🟢 LOW    | No factual errors or inconsistencies |

### Validation Report Format

```markdown
## Skill Validation Report

### Summary

| Severity    | Count |
| ----------- | ----- |
| 🔴 CRITICAL | X     |
| 🟡 MEDIUM   | X     |
| 🟢 LOW      | X     |

### Findings

| Skill      | Severity    | Issue               | Recommendation                |
| ---------- | ----------- | ------------------- | ----------------------------- |
| skill-name | 🔴 CRITICAL | Missing description | Add description with triggers |
| skill-name | 🟡 MEDIUM   | Body too long       | Move content to references/   |

### Action Items

1. [CRITICAL] Fix: skill-name - Add description
2. [MEDIUM] Improve: skill-name - Reduce body length
```

### Agent-Skill Alignment Check

When validating, also check agent-skill alignment:

1. **Scan agents** - List all agents in `.github/agents/`
2. **Extract skill references** - Find "Load and follow" patterns
3. **Cross-reference** - Verify all referenced skills exist
4. **Report orphans** - Skills not used by any agent
5. **Report missing** - Skills referenced but don't exist
