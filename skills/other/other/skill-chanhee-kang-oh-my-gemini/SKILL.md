---
name: skill
description: Manage local skills - list, add, remove, search, edit
argument-hint: "<command> [args]"
---

# Skill Management CLI

Meta-skill for managing oh-my-gemini skills via CLI-like commands.

## Subcommands

### /skill list

Show all local skills organized by scope.

**Behavior:**
1. Scan user skills at `~/.gemini-cli/skills/omc-learned/`
2. Scan project skills at `.omc/skills/`
3. Parse YAML frontmatter for metadata
4. Display in organized table format:

```
USER SKILLS (~/.gemini-cli/skills/omc-learned/):
| Name              | Triggers           | Quality | Usage | Scope |
|-------------------|--------------------|---------|-------|-------|
| error-handler     | fix, error         | 95%     | 42    | user  |
| api-builder       | api, endpoint      | 88%     | 23    | user  |

PROJECT SKILLS (.omc/skills/):
| Name              | Triggers           | Quality | Usage | Scope   |
|-------------------|--------------------|---------|-------|---------|
| test-runner       | test, run          | 92%     | 15    | project |
```

**Fallback:** If quality/usage stats not available, show "N/A"

---

### /skill add [name]

Interactive wizard for creating a new skill.

**Behavior:**
1. **Ask for skill name** (if not provided in command)
   - Validate: lowercase, hyphens only, no spaces
2. **Ask for description**
   - Clear, concise one-liner
3. **Ask for triggers** (comma-separated keywords)
   - Example: "error, fix, debug"
4. **Ask for argument hint** (optional)
   - Example: "<file> [options]"
5. **Ask for scope:**
   - `user` → `~/.gemini-cli/skills/omc-learned/<name>/SKILL.md`
   - `project` → `.omc/skills/<name>/SKILL.md`
6. **Create skill file** with template:

```yaml
---
name: <name>
description: <description>
triggers:
  - <trigger1>
  - <trigger2>
argument-hint: "<args>"
---

# <Name> Skill

## Purpose

[Describe what this skill does]

## When to Activate

[Describe triggers and conditions]

## Workflow

1. [Step 1]
2. [Step 2]
3. [Step 3]

## Examples

```
/oh-my-gemini:<name> example-arg
```

## Notes

[Additional context, edge cases, gotchas]
```

7. **Report success** with file path
8. **Suggest:** "Edit `/skill edit <name>` to customize content"

**Example:**
```
User: /skill add custom-logger
Assistant: Creating new skill 'custom-logger'...

Description: Enhanced logging with structured output
Triggers (comma-separated): log, logger, logging
Argument hint (optional): <level> [message]
Scope (user/project): user

✓ Created skill at ~/.gemini-cli/skills/omc-learned/custom-logger/SKILL.md
→ Edit with: /skill edit custom-logger
```

---

### /skill remove <name>

Remove a skill by name.

**Behavior:**
1. **Search for skill** in both scopes:
   - `~/.gemini-cli/skills/omc-learned/<name>/SKILL.md`
   - `.omc/skills/<name>/SKILL.md`
2. **If found:**
   - Display skill info (name, description, scope)
   - **Ask for confirmation:** "Delete '<name>' skill from <scope>? (yes/no)"
3. **If confirmed:**
   - Delete entire skill directory (e.g., `~/.gemini-cli/skills/omc-learned/<name>/`)
   - Report: "✓ Removed skill '<name>' from <scope>"
4. **If not found:**
   - Report: "✗ Skill '<name>' not found in user or project scope"

**Safety:** Never delete without explicit user confirmation.

**Example:**
```
User: /skill remove old-logger
Assistant: Found skill 'old-logger' in user scope:
  Description: Legacy logging utility
  Scope: user (~/.gemini-cli/skills/omc-learned/)

Delete 'old-logger' skill? (yes/no)

User: yes
Assistant: ✓ Removed skill 'old-logger' from user scope
```

---

### /skill edit <name>

Edit an existing skill interactively.

**Behavior:**
1. **Find skill** by name (search both scopes)
2. **Read current content** via Read tool
3. **Display current values:**
   ```
   Current skill 'custom-logger':
   - Description: Enhanced logging with structured output
   - Triggers: log, logger, logging
   - Argument hint: <level> [message]
   - Scope: user
   ```
4. **Ask what to change:**
   - `description` - Update description
   - `triggers` - Update trigger keywords
   - `argument-hint` - Update argument hint
   - `content` - Edit full markdown content
   - `rename` - Rename skill (move file)
   - `cancel` - Exit without changes
5. **For selected field:**
   - Show current value
   - Ask for new value
   - Update YAML frontmatter or content
   - Write back to file
6. **Report success** with summary of changes

**Example:**
```
User: /skill edit custom-logger
Assistant: Current skill 'custom-logger':
  - Description: Enhanced logging with structured output
  - Triggers: log, logger, logging
  - Argument hint: <level> [message]

What would you like to edit? (description/triggers/argument-hint/content/rename/cancel)

User: triggers
Assistant: Current triggers: log, logger, logging
New triggers (comma-separated): log, logger, logging, trace

✓ Updated triggers for 'custom-logger'
```

---

### /skill search <query>

Search skills by content, triggers, name, or description.

**Behavior:**
1. **Scan all skills** in both scopes
2. **Match query** (case-insensitive) against:
   - Skill name
   - Description
   - Triggers
   - Full markdown content
3. **Display matches** with context:

```
Found 3 skills matching "typescript error":

1. typescript-fixer (user)
   Description: Fix common TypeScript errors
   Match: "typescript error handling patterns"

2. error-handler (user)
   Description: Generic error handling utilities
   Match: "Supports TypeScript and JavaScript errors"

3. lint-fix (project)
   Description: Auto-fix linting errors
   Match: "TypeScript ESLint error resolution"
```

**Ranking:** Prioritize matches in name/triggers over content matches

**Example:**
```
User: /skill search api endpoint
Assistant: Found 2 skills matching "api endpoint":

1. api-builder (user)
   Description: Generate REST API endpoints
   Triggers: api, endpoint, rest

2. backend-scaffold (project)
   Description: Scaffold backend services
   Match: "Creates API endpoint boilerplate"
```

---

### /skill info <name>

Show detailed information about a skill.

**Behavior:**
1. **Find skill** by name (search both scopes)
2. **Parse YAML frontmatter** and content
3. **Display complete details:**

```
Skill: custom-logger
Scope: user (~/.gemini-cli/skills/omc-learned/custom-logger/)
Description: Enhanced logging with structured output
Triggers: log, logger, logging
Argument Hint: <level> [message]
Quality: 95% (if available)
Usage Count: 42 times (if available)
File Path: /home/user/.gemini-cli/skills/omc-learned/custom-logger/SKILL.md

--- FULL CONTENT ---
[entire markdown content]
```

**If not found:** Report error with suggestion to use `/skill search`

**Example:**
```
User: /skill info custom-logger
Assistant: Skill: custom-logger
Scope: user
Description: Enhanced logging with structured output
Triggers: log, logger, logging
File: ~/.gemini-cli/skills/omc-learned/custom-logger/SKILL.md

--- CONTENT ---
# Custom Logger Skill

## Purpose
Enhanced logging with structured JSON output...
[rest of content]
```

---

### /skill sync

Sync skills between user and project scopes.

**Behavior:**
1. **Scan both scopes:**
   - User skills: `~/.gemini-cli/skills/omc-learned/`
   - Project skills: `.omc/skills/`
2. **Compare and categorize:**
   - User-only skills (not in project)
   - Project-only skills (not in user)
   - Common skills (in both)
3. **Display sync opportunities:**

```
SYNC REPORT:

User-only skills (5):
  - error-handler
  - api-builder
  - custom-logger
  - test-generator
  - deploy-helper

Project-only skills (2):
  - test-runner
  - backend-scaffold

Common skills (3):
  - frontend-ui-ux
  - git-master
  - planner

Options:
  [1] Copy user skill to project
  [2] Copy project skill to user
  [3] View differences
  [4] Cancel
```

4. **Handle user choice:**
   - Option 1: Select skill(s) to copy to project
   - Option 2: Select skill(s) to copy to user
   - Option 3: Show side-by-side diff for common skills
   - Option 4: Exit

**Safety:** Never overwrite without confirmation

**Example:**
```
User: /skill sync
Assistant: Found 5 user-only skills and 2 project-only skills.

Copy 'error-handler' from user to project? (yes/no/skip)
User: yes
Assistant: ✓ Copied 'error-handler' to .omc/skills/

Copy 'api-builder' from user to project? (yes/no/skip)
User: skip
...
```

---

## Error Handling

**All commands must handle:**
- File/directory doesn't exist
- Permission errors
- Invalid YAML frontmatter
- Duplicate skill names
- Invalid skill names (spaces, special chars)

**Error format:**
```
✗ Error: <clear message>
→ Suggestion: <helpful next step>
```

## Usage Examples

```bash
# List all skills
/skill list

# Create a new skill
/skill add my-custom-skill

# Remove a skill
/skill remove old-skill

# Edit existing skill
/skill edit error-handler

# Search for skills
/skill search typescript error

# Get detailed info
/skill info my-custom-skill

# Sync between scopes
/skill sync
```

## Implementation Notes

1. **YAML Parsing:** Use frontmatter extraction for metadata
2. **File Operations:** Use Read/Write tools, never Edit for new files
3. **User Confirmation:** Always confirm destructive operations
4. **Clear Feedback:** Use checkmarks (✓), crosses (✗), arrows (→) for clarity
5. **Scope Resolution:** Always check both user and project scopes
6. **Validation:** Enforce naming conventions (lowercase, hyphens only)

## Future Enhancements

- `/skill export <name>` - Export skill as shareable file
- `/skill import <file>` - Import skill from file
- `/skill stats` - Show usage statistics across all skills
- `/skill validate` - Check all skills for format errors
- `/skill template <type>` - Create from predefined templates
