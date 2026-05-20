---
name: converting-commands-to-skills
description: Use this skill when converting Claude Code slash commands to Skills format. Handles transformation from ./commands/*.md to ./skills/*/SKILL.md, including YAML frontmatter conversion, name transformation to gerund form, description enhancement for invocation triggers, and batch processing. Invoke when user asks to convert commands to skills, migrate slash commands, or transform command files.
hooks:
  PostToolUse:
    - matcher: Write
      hooks:
        - type: command
          command: python3 ~/.claude/skills/converting-commands-to-skills/scripts/validate-frontmatter.py
---

# Converting Slash Commands to Skills

This skill automates the conversion of Claude Code slash commands (in `./commands/` or `~/.claude/commands/`) to the Skills format (in `./skills/` or `~/.claude/skills/`).

## Conversion Process

### 1. Choose Conversion Type

**CRITICAL:** Before starting, use AskUserQuestion to ask the user which conversion type they want:

**Basic Conversion:**
- Transforms YAML frontmatter (name to gerund form, remove command-specific fields, enhance description)
- Transforms directory structure (./commands → ./skills)
- **Does NOT change any content below the YAML frontmatter** (keeps @path, !commands, all content as-is)

**Full Conversion:**
- Everything in basic conversion
- PLUS transforms content below frontmatter (progressive disclosure, @path → ./path, !command → Bash tool instructions, supporting files)

Ask the user: "Do you want a basic conversion (frontmatter + directory only) or full conversion (frontmatter + directory + content transformation)?"

### 2. Analyze Source Command and Check for Existing Skill

First, read the command file to understand its structure:

```bash
# Example command file structure
cat ./commands/gsd/add-phase.md
```

Command files typically have:
- YAML frontmatter with fields like `description`, `allowed-tools`, `argument-hint`, `model`, `context`, `agent`
- Markdown content with instructions
- Bash execution blocks prefixed with exclamation mark (!)
- File references using @ symbol syntax (@file.md)

**Check if target skill already exists:**
```bash
# Check if skill directory and SKILL.md exist
ls ./skills/skill-name/SKILL.md
```

**If skill already exists:**
- **Preserve the existing frontmatter** (do NOT overwrite it)
- **Only update the content below the frontmatter** according to conversion type
- Ask user: "This skill already exists. Should I update only the content below the frontmatter while preserving the existing frontmatter?"

### 2. Transform to Skill Format

Apply these transformations (see `./transformation-rules.md` for details):

**Name Transformation:**
- Command: `add-phase.md` → Skill: `adding-phases` (gerund form)
- Command: `review.md` → Skill: `reviewing-code`
- Pattern: Use verb + -ing form, lowercase, hyphens

**Directory Structure:**
- Source: `./commands/category/command-name.md`
- Target: `./skills/category-command-name/SKILL.md`
- **The category/namespace becomes a prefix in the skill directory name**
- Examples:
  - `./commands/kata/add-phase.md` → `./skills/kata-adding-phases/SKILL.md`
  - `./commands/gsd/new-project.md` → `./skills/gsd-starting-new-projects/SKILL.md`
  - `./commands/review.md` (no category) → `./skills/reviewing-code/SKILL.md`

**YAML Frontmatter:**
- Keep: `name` (transformed), `description` (enhanced)
- Remove: `allowed-tools`, `argument-hint`, `model`, `context`, `agent`
- Skills inherit all Claude Code capabilities automatically

**Description Enhancement:**
- Original (task-focused): "Add a new phase to the roadmap"
- Enhanced (invocation-focused): "Use this skill when adding planned phases to the roadmap, appending sequential work to milestones, or creating new phase entries. Triggers include 'add phase', 'append phase', 'new phase', and 'create phase'."
- Include: trigger keywords, use cases, when to invoke

**Content Transformation (FULL CONVERSION ONLY):**
- Convert bash execution (exclamation mark prefix like !command) to explicit instructions with Bash tool
- Transform file references (@ prefix like @file.md) to relative paths (./file.md)
- Move detailed content to supporting files with intention-revealing names
- Keep SKILL.md under 500 lines using progressive disclosure
- **For BASIC conversion: Skip all content transformation - copy content as-is**

### 3. Batch Conversion Workflow

When converting multiple commands:

```bash
# 1. List all commands to convert
find ./commands -name "*.md" -type f

# 2. For each command file, perform conversion
# (Claude will iterate through files)
```

For each file:
1. Read the source command file
2. Determine target skill name and directory
3. Check if target skill already exists
4. **If skill exists:**
   - Read existing SKILL.md
   - Extract and preserve existing frontmatter
   - Only update content below frontmatter
5. **If skill does not exist:**
   - Create skill directory structure
   - Transform YAML frontmatter according to rules
6. **If BASIC conversion:** Copy content below frontmatter as-is
7. **If FULL conversion:** Transform content according to rules
8. Write SKILL.md (preserving frontmatter if skill existed)
9. **If FULL conversion:** Extract supporting content to separate files if needed
10. Validate the conversion (hook runs automatically)

### 4. Validate Conversion

**Automatic Validation:**
After each skill file is written, a PostToolUse hook automatically runs `validate-frontmatter.py` to check:
- Name follows gerund form convention (verb + -ing)
- Name is max 64 characters
- Description is present and under 1024 characters
- Description is in third person
- No invalid frontmatter fields (allowed-tools, argument-hint, etc.)

The hook will output validation results. If validation fails, review and fix the issues.

**Manual Validation Checklist:**

**All conversions (basic and full):**
- ✓ Name uses gerund form (verb + -ing)
- ✓ Name is max 64 characters
- ✓ Description includes trigger keywords and use cases
- ✓ Description is in third person
- ✓ YAML frontmatter has no invalid fields
- ✓ Directory structure is correct (./skills/)

**Full conversion only:**
- ✓ Supporting files have intention-revealing names
- ✓ Relative path references use `./` prefix
- ✓ SKILL.md is concise (under 500 lines preferred)
- ✓ Bash executions converted to explicit instructions

### 5. Prompt for User Review

After automatic transformation:
1. Show the user what was converted
2. Highlight the enhanced description
3. Ask if description improvements are needed
4. Suggest any supporting files that could be extracted

## Usage Examples

**Single File Conversion:**
User: "Convert ./commands/gsd/add-phase.md to a skill"

**Batch Conversion:**
User: "Convert all commands in ./commands/gsd/ to skills"

**Project Migration:**
User: "Migrate all my slash commands to the skills format"

## Acceptance Criteria

**All conversions (basic and full):**
- [ ] User asked about conversion type (basic vs full)
- [ ] If skill exists, user asked about updating content only
- [ ] Existing frontmatter preserved if skill already exists
- [ ] Skill directory created in correct location (./skills/)
- [ ] SKILL.md has proper YAML frontmatter
- [ ] Name follows gerund form convention
- [ ] Description is invocation-focused with triggers
- [ ] All slash-command-specific fields removed
- [ ] Automatic validation hook ran successfully
- [ ] User prompted to review description enhancements

**Full conversion only:**
- [ ] Bash executions converted to explicit instructions
- [ ] File references use relative paths
- [ ] Supporting files have intention-revealing names
- [ ] Content transformed with progressive disclosure

**Basic conversion only:**
- [ ] Content below frontmatter copied as-is with NO changes

## Supporting Files

See `./transformation-rules.md` for detailed transformation patterns and `./conversion-examples.md` for before/after examples.
