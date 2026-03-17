---
name: {skill-slug}
description: {What this skill does} and {when to use it}. Use when {specific trigger or context}. Example: "Processes Excel files and generates reports. Use when working with spreadsheets or .xlsx files."
---

{Brief opening statement - assume Claude is smart, only provide context Claude doesn't have.}

1. **{First Step}**
   - {Actionable instruction}
   - **Template**: `templates/{FileName}.cs` (if generating code)
   - **Reference**: See [{reference-file}.md]({reference-file}.md) (if details are large)

2. **{Second Step}**
   - {Another instruction}
   - {Sub-bullet if needed}

// turbo
3. **{Automated Step (Optional)}**
   - Run: `{command to execute automatically}`
   - This step runs without user confirmation

## Related Skills

**Prerequisites**:
- `/{prerequisite-skill}` - What must exist or run before this skill

**Next Steps**:
- `/{next-skill}` - What to run after completing this skill
- `/{verify-feature}` - Verification step (if applicable)

**Related**:
- `/{related-skill}` - When to use instead or in addition

**See Also**:
- Relevant AGENTS.md files
- Other skills in `.claude/skills/` for examples
