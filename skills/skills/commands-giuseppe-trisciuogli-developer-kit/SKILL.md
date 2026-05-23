---
description: Validates a skill against DevKit standards (requirements, template, dependencies). Use when you need to verify a skill before publishing or after modifications.
argument-hint: "[skill-name]"
allowed-tools: Read, Grep, Glob
---

# Verify Skill: $1

## Overview

You are a skill validation specialist for the Claude Code Developer Kit. Your task is to perform a comprehensive
validation of the skill "$1" against all DevKit standards.

## Usage

```
/devkit.verify-skill $ARGUMENTS
```

## Arguments

| Argument     | Description                              |
|--------------|------------------------------------------|
| `$ARGUMENTS` | Combined arguments passed to the command |

## Execution Instructions

**Agent Selection**: To execute this task, use the following approach:

- Primary: Use `general-purpose` agent with appropriate domain expertise
- Or use specialized agent if available for the specific task type

## Validation Process

Execute the following checks in sequence:

### 1. Skill Existence Check

- Search for the skill directory in the following locations (in this order):
    - `.claude/skills/$1/` (project-level)
    - `~/.claude/skills/$1/` (user-level)
    - `./skills/**/$1/` (any category subfolder under the repo `skills/` directory — recursive search)
    - Any other project-local plugin directories that the repository documents for skills (if present)
- Verify that a `SKILL.md` file exists inside the found skill directory
- Important: many development workflows (for example when authoring a Claude plugin or a shared skills repo) keep skills
  under top-level `skills/` categories (e.g. `skills/langchain4j/<skill-name>`). This is an acceptable and supported
  location for the purposes of validation and MUST NOT be treated as a false-positive or as a failure just because
  `.claude/skills/` or `~/.claude/skills/` do not contain the skill.
- If the skill cannot be found in any of the locations above, report failure (Existence).

### 2. Requirements Conformance (@.docs/skills.md)

Check that the skill complies with all requirements from the official Skills documentation:

**SKILL.md Frontmatter:**

- `name` field: lowercase letters, numbers, hyphens only (max 64 characters)
- `description` field: present and descriptive (max 1024 characters). Description includes BOTH what the skill does AND
  when to use it
- `allowed-tools` field: uses valid tool names only
- `category`: field, valid category
- `tags`: field, relevant, and descriptive (no generic tags like "skill" or "devkit")
- `version` field: uses semantic versioning (e.g., 1.0.0)
  **Important:** Other frontmatter fields are not allowed.

**File Structure:**

- `SKILL.md` uses valid YAML frontmatter (opening and closing `---`)
- No YAML syntax errors (tabs, incorrect indentation)
- All referenced files in SKILL.md exist in the skill directory
- File paths use forward slashes (Unix style), not backslashes

**Content Quality:**

- Description is specific with trigger keywords (not vague/generic)
- Skill has a clear "When to Use" or "Instructions" section
- Examples are present and demonstrate the skill
- Examples (examples.md) file exists if multiple examples are provided
- Supporting files (if any) are properly referenced with Markdown links
- References (reference.md) file exists if the skill is complex

### 3. Template Adherence (@.docs/skill_template.md)

Verify the skill structure matches the template:

**Required Sections:**

- Skill name as H1 heading
- "When to Use This Skill" section with clear use cases
- "Core Concepts" or "Instructions" section
- "Examples" or practical demonstrations
- "Best Practices" or "Summary" section

**Metadata Alignment:**

- Frontmatter includes recommended fields (name, description, category, tags, version)
- Version number is present and follows semantic versioning (if included)
- Tags are relevant and descriptive (if included)
- Category is specified (if included)

**Content Organization:**

- Logical section hierarchy
- Progressive complexity in examples
- Clear cross-references to related content
- Proper code formatting and syntax highlighting

### 4. Dependency Validation (Context7 or u2m)

**IMPORTANT:** Only perform this check if the skill references specific libraries or frameworks.

For each library/framework mentioned in the skill:

- Identify the library name and version (if specified)
- Use mcp Context7 to check if the library is current
- Verify trust score is adequate (≥ 7.0 for enterprise skills)
- Check if there are newer stable versions available
- Note if documentation indicates breaking changes
  If context7 is not accessible, use this bash tool `u2m`.
- Verify with bash tool `u2m -v <link-reference>` to get the latest version and trust score
- Clean every output from `u2m` to extract only relevant data
  IF `u2m` fails, note this but do not fail validation
  Finally, compare the current version with the latest stable version found.

**Skip this check if:**

- The skill is language-agnostic or doesn't reference specific libraries
- The skill only uses built-in language features
- No version numbers are specified

## Output Format

### Success Case

If ALL checks pass, output:

```
✅ Validation completed: The skill '$1' complies with all standards.

Details:
- ✅ SKILL.md file present and valid
- ✅ Frontmatter correct (name, description)
- ✅ Structure conforms to the template
- ✅ All referenced files exist
- ✅ [Dependencies validated / No dependencies to validate]
```

### Failure Case

If ANY check fails, output:

```
❌ Validation failed for the skill '$1'.

Required actions:

* **[Category]:** [Specific description of the issue]
* **[Category]:** [Specific description of the issue]
...
```

**Categories for errors:**

- **Existence:** Skill or SKILL.md not found
- **Requirements:** YAML frontmatter errors, invalid field values, missing required fields
- **Template:** Missing sections, incorrect structure, poor organization
- **File:** Referenced files not found, incorrect path format
- **Dependencies:** Outdated libraries, low trust scores, breaking changes
- **Content:** Vague descriptions, missing examples, poor documentation

## Examples of Specific Feedback

**Good specific feedback:**

- ❌ **Requirements:** The `name` field contains uppercase characters. It must use only lowercase letters, numbers, and
  hyphens.
- ❌ **Template:** The "When to Use This Skill" section required by the template is missing.
- ❌ **File:** The `reference.md` file is referenced in SKILL.md but does not exist in the skill directory.
- ❌ **Dependencies:** The 'spring-boot' library uses version 2.7.x. Recommended version: 3.2.x (Context7 Trust Score:
  9.2).
- ❌ **Content:** The description does not specify WHEN to use the skill; it only describes what it does.

**Bad vague feedback (avoid):**

- ❌ The file is not valid
- ❌ There are issues with the template
- ❌ The dependencies might be outdated

## Validation Rules

1. **Be thorough:** Check every requirement systematically
2. **Be specific:** Each error must include the exact issue and how to fix it
3. **Be actionable:** Suggest concrete solutions, not just identify problems
4. **Be accurate:** Only report actual issues found, don't assume
5. **Prioritize:** List critical issues (existence, syntax errors) before style issues

## Additional Notes

- If the skill directory exists but is empty, report as missing SKILL.md
- If YAML frontmatter is malformed, report the specific YAML error
- If Context7 lookup fails, note this but don't fail validation
- Check both `.claude/skills/$1/` (project) and `~/.claude/skills/$1/` (personal)
- For multi-file skills, validate that supporting files add value

Begin validation now for skill: $1

---

## Examples

```bash
/devkit.verify-skill skill-name
```
