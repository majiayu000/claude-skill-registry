---
name: remember
description: This skill should be used when the user says "remember", "note this", "add to CLAUDE.md", "don't forget", "keep in mind", or asks to store a preference, convention, or project-specific instruction. Stores memories in the project's CLAUDE.md file.
version: 1.0.0
---

# Remember Skill

Stores user preferences, conventions, and project-specific instructions in the appropriate CLAUDE.md file with proper wording and placement.

---

## When This Skill Applies

Use this skill when the user:
- Says "remember that...", "remember to...", "note that..."
- Asks to "add this to CLAUDE.md"
- Says "don't forget..." or "keep in mind..."
- Wants to store a preference, convention, or instruction
- Mentions something should be remembered for future sessions

---

## Execution Steps

### 1. Parse the Memory

Extract the core information to remember:
- **What**: The specific fact, preference, or convention
- **Context**: Why it matters or when it applies
- **Scope**: Project-specific or general preference

### 2. Locate the CLAUDE.md File

Check for CLAUDE.md in this order:
1. Project root: `./CLAUDE.md`
2. Project .claude dir: `./.claude/CLAUDE.md`
3. If neither exists, create `./.claude/CLAUDE.md`

**Important**: Do NOT modify the global `~/.claude/CLAUDE.md` unless the user explicitly says the memory is global/applies to all projects.

### 3. Read Existing Content

Read the current CLAUDE.md to understand:
- Existing sections and structure
- Writing style and tone
- Where the new memory fits best

### 4. Determine Placement

Place the memory in the most appropriate section:

| Memory Type | Suggested Section |
|-------------|-------------------|
| Code style preference | `## Code Style` or `## Conventions` |
| Naming convention | `## Naming Conventions` |
| Architecture decision | `## Architecture` or `## Patterns` |
| Tool/dependency preference | `## Tooling` or `## Dependencies` |
| Testing approach | `## Testing` |
| Workflow preference | `## Workflow` |
| Personal preference | `## Preferences` |
| Project-specific fact | `## Project Notes` or `## Context` |
| Don't do X | `## Avoid` or `## Anti-patterns` |

If no matching section exists:
- Add to an existing related section, OR
- Create a new appropriate section

### 5. Word Appropriately

Transform the user's casual statement into a clear instruction:

**User says**: "remember I hate semicolons"
**Store as**: "Omit semicolons in JavaScript/TypeScript (Prettier handles this)"

**User says**: "remember the API uses snake_case"
**Store as**: "API responses use snake_case - convert to camelCase in frontend code"

**User says**: "don't forget to run tests before committing"
**Store as**: "Run `npm test` before committing changes"

**Guidelines**:
- Use imperative mood for instructions
- Be specific and actionable
- Include the "why" if the user provided it
- Keep it concise but complete
- Match the existing document's tone

### 6. Apply the Edit

Use the Edit tool to add the memory to CLAUDE.md:
- Add under the appropriate section heading
- Use consistent formatting (bullets, etc.)
- Preserve existing content

### 7. Confirm to User

After adding, confirm what was stored and where:
```
Added to .claude/CLAUDE.md under "## Code Style":
- Omit semicolons in JavaScript/TypeScript
```

---

## Examples

### Example 1: Code Preference

**User**: "remember that I prefer functional components over class components"

**Action**: Add to `## Code Style` or `## React` section:
```markdown
- Prefer functional components with hooks over class components
```

### Example 2: Project Convention

**User**: "remember the database uses soft deletes"

**Action**: Add to `## Database` or `## Architecture` section:
```markdown
- Database uses soft deletes (`deleted_at` timestamp) - never use hard DELETE
```

### Example 3: Workflow Note

**User**: "don't forget that PR reviews require two approvals"

**Action**: Add to `## Workflow` or `## Process` section:
```markdown
- Pull requests require two approvals before merging
```

### Example 4: Avoid Pattern

**User**: "remember never to use any type"

**Action**: Add to `## TypeScript` or `## Avoid` section:
```markdown
- Never use `any` type - use `unknown` if type is genuinely uncertain
```

---

## Edge Cases

### Empty or Missing CLAUDE.md

If no CLAUDE.md exists:
1. Create `./.claude/CLAUDE.md`
2. Add a minimal header:
```markdown
# Project Instructions

## Notes
- [the memory]
```

### Duplicate Information

If similar information already exists:
- Update the existing entry rather than adding a duplicate
- Merge information if the new memory adds detail

### Ambiguous Scope

If unclear whether memory is project-specific or global:
- Default to project-specific (safer)
- Ask user to clarify if it seems important

### User Says "Always" or "Never"

Treat strong preferences seriously:
- "Always" → Add as a clear instruction
- "Never" → Add to an `## Avoid` section or phrase as "Do not..."

---

## Success Criteria

Memory storage is successful when:
- Memory is placed in a logical section
- Wording is clear and actionable
- Existing content is preserved
- User is informed of what was stored and where
- Future Claude sessions will see and follow the instruction
