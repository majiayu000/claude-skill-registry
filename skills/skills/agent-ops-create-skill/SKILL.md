---
name: agent-ops-create-skill
description: "Create new AgentOps skills via interactive interview. Supports from-scratch and clone modes with tiered complexity."
category: utility
invokes: [agent-ops-interview]
invoked_by: []
state_files:
  read: []
  write: []
---

# Create Skill Workflow

## Purpose

Guide users through creating new AgentOps skills with consistent structure and quality. Reduces friction for skill ecosystem growth while enforcing standards.

## Mode Selection

Present mode options at the start:

| Mode | Description | Use When |
|------|-------------|----------|
| **A) From scratch** | Start with blank template | Creating entirely new capability |
| **B) Clone existing** | Use existing skill as base | New skill similar to existing one |

### Clone Mode Procedure

1. List available skills from `.github/skills/`
2. User selects one to clone
3. Read that skill's SKILL.md as base
4. Interview focuses on what to change/customize

## Complexity Tiers

After mode selection, assess complexity:

| Tier | Questions | Criteria |
|------|-----------|----------|
| **Simple** | 5 | Single procedure, minimal dependencies, clear scope |
| **Complex** | 10+ | Multiple procedures, decision trees, error handling, many dependencies |

### Complexity Assessment Questions

Ask the user:
1. "Does this skill have a single main procedure, or multiple branching paths?"
2. "Does it need to invoke other skills or handle errors specially?"

**If answers suggest simple** → Simple tier (5 questions)
**If answers suggest complex** → Complex tier (10+ questions)

---

## Interview Questions

### Simple Tier (5 Questions)

Use `agent-ops-interview` skill for one-question-at-a-time flow.

| # | Question | Field | Validation |
|---|----------|-------|------------|
| 1 | "What should this skill be called? (use kebab-case, e.g., `my-custom-skill`)" | `name` | Kebab-case, unique in `.github/skills/`. **Must NOT start with `agent-ops-`** (reserved for bundled assets). |
| 2 | "Describe in one sentence what this skill does:" | `description` | Non-empty, < 200 chars |
| 3 | "What category does this fit? (core/utility/analysis/git/recovery)" | `category` | One of: core, utility, analysis, git, recovery |
| 4 | "What is the main procedure? Describe the step-by-step workflow:" | Procedure section | Non-empty |
| 5 | "What state files does it read and write? (e.g., focus.md, issues/*)" | `state_files` | Valid file paths or patterns |
| 6 | "Should this skill have an accompanying prompt file for slash command usage? (yes/no)" | `create_prompt` | Boolean - if yes, generate `.github/prompts/{name}.prompt.md` |

**IMPORTANT**: If user provides a name starting with `agent-ops-`, respond with:
> ❌ Cannot create skill with `agent-ops-` prefix. This prefix is reserved for bundled assets managed by `aoc bundle install`. Please choose a different name (e.g., `my-tags` instead of `agent-ops-tags`).

### Complex Tier Additional Questions (7-11+)

| # | Question | Field |
|---|----------|-------|
| 7 | "What other skills does this invoke? (comma-separated)" | `invokes` |
| 8 | "What skills might invoke this one? (comma-separated)" | `invoked_by` |
| 9 | "Are there multiple procedures or modes? If yes, describe each:" | Additional sections |
| 10 | "Are there decision points or branching logic? Describe:" | Decision tree |
| 11 | "How should errors be handled? Any recovery procedures?" | Error handling section |

**Follow-up questions** (as needed based on answers):
- "What are the preconditions before this skill can run?"
- "What completion criteria determine success?"
- "What are common anti-patterns to avoid?"
- "Can you provide an example invocation?"

---

## Skill Template

After interview completion, generate SKILL.md using this template:

```markdown
---
name: {name}
description: "{description}"
category: {category}
invokes: [{invokes}]
invoked_by: [{invoked_by}]
state_files:
  read: [{read_files}]
  write: [{write_files}]
---

# {Title} Workflow

## Purpose

{purpose_description}

## Procedure

{main_procedure}

## Completion Criteria

- [ ] {criterion_1}
- [ ] {criterion_2}

## Anti-patterns (avoid)

- ❌ {antipattern_1}
```

### Template Field Mapping

| Interview Answer | Template Field |
|------------------|----------------|
| Question 1 | `{name}`, directory name |
| Question 2 | `{description}`, `{purpose_description}` |
| Question 3 | `{category}` |
| Question 4 | `{main_procedure}` |
| Question 5 | `{read_files}`, `{write_files}` |
| Question 6 | `{invokes}` |
| Question 7 | `{invoked_by}` |
| Questions 8-10 | Additional sections as appropriate |

---

## Generation Procedure

1. **Validate answers**:
   - Name does NOT start with `agent-ops-` (reserved prefix)
   - Name is unique (check `.github/skills/` doesn't have directory)
   - Category is valid enum
   - Description is non-empty

2. **Create directory**:
   - Path: `.github/skills/{name}/`

3. **Generate SKILL.md**:
   - Populate template with interview answers
   - Add sections based on complexity tier

4. **Generate prompt file** (if requested):
   - Path: `.github/prompts/{name}.prompt.md`
   - Use prompt template (see below)

5. **Confirm with user**:
   - Show generated content
   - Ask "Does this look correct? (yes/edit/cancel)"

6. **Save file(s)**:
   - Write to `.github/skills/{name}/SKILL.md`
   - Write to `.github/prompts/{name}.prompt.md` (if requested)

---

## Prompt Template

When user requests a prompt file, generate using this template:

```markdown
Use the `{name}` skill for {short_description}.

## Quick Usage

{brief_usage_example}

## When to Use

- {use_case_1}
- {use_case_2}

## Options

{any_modes_or_options_from_skill}
```

**Mapping**:
- `{name}` → skill name from interview
- `{short_description}` → description from interview (lowercase, no period)
- `{brief_usage_example}` → derived from main procedure
- `{use_case_1/2}` → inferred from purpose

---

## Registration Procedure

After skill file is created, auto-register in SKILL-TIERS.md:

1. **Read** `.github/SKILL-TIERS.md`

2. **Determine tier** from category:
   | Category | Tier |
   |----------|------|
   | core | Tier 1 |
   | utility | Tier 3 |
   | analysis | Tier 5 |
   | git | Tier 4 |
   | recovery | Tier 4 |

3. **Find table** for target tier (pattern: `### Tier {N}:`)

4. **Insert row** at end of table:
   ```markdown
   | `{name}` | {description} | {invoked_by or "User request"} |
   ```

5. **Save file**

6. **Confirm**: "✅ Skill registered in SKILL-TIERS.md under Tier {N}"

---

## Post-Creation Validation

After generation, verify:

- [ ] File exists at `.github/skills/{name}/SKILL.md`
- [ ] Frontmatter is valid YAML
- [ ] Name in frontmatter matches directory name
- [ ] Name does NOT start with `agent-ops-` (reserved prefix)
- [ ] Description is non-empty
- [ ] At least one procedure section exists
- [ ] State files declared (read/write)
- [ ] Registered in SKILL-TIERS.md
- [ ] Prompt file exists at `.github/prompts/{name}.prompt.md` (if requested)

**If validation fails**: Report specific failure, offer to fix or regenerate.

---

## Examples

### Example 1: Simple Skill Creation

**User**: "Create a skill for managing project tags"

**Interview**:
```
Q1: "What should this skill be called?"
A1: "my-tags"

Q2: "Describe in one sentence what this skill does:"
A2: "Manage project-level tags for categorizing issues and documentation"

Q3: "What category does this fit?"
A3: "utility"

Q4: "What is the main procedure?"
A4: "1. List current tags from .agent/tags.md
     2. User selects action (add/remove/rename)
     3. Execute action and update file"

Q5: "What state files does it read and write?"
A5: "read: tags.md, focus.md; write: tags.md, focus.md"

Q6: "Should this skill have an accompanying prompt file for slash command usage?"
A6: "yes"
```

**Generated output**: 
- `.github/skills/my-tags/SKILL.md`
- `.github/prompts/my-tags.prompt.md`

### Example 2: Clone Mode

**User**: "Create a skill similar to agent-ops-docs but for API documentation"

**Interview**:
```
Mode: Clone agent-ops-docs

Q1: "What should this skill be called?"
A1: "my-api-docs"

Q2: "What's different from agent-ops-docs?"
A2: "Focuses on API endpoint documentation, generates OpenAPI specs"

... (remaining questions focus on differences)
```

**Generated output**: Based on agent-ops-docs structure with API-specific modifications

---

## Cancellation Handling

If user says "stop", "cancel", or "nevermind" at any point:

1. Acknowledge cancellation
2. Report progress: "Skill creation cancelled at question {N} of {total}"
3. No files created unless user explicitly confirmed

---

## Anti-patterns (avoid)

- ❌ Creating skill with reserved `agent-ops-` prefix
- ❌ Creating skill without interview (skipping validation)
- ❌ Registering skill in wrong tier based on category
- ❌ Creating duplicate skill name
- ❌ Generating SKILL.md without user confirmation
- ❌ Skipping validation checklist after creation
