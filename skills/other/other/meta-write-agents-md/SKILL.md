---
name: meta__write_agents_md
description: Creates or updates AGENTS.md files with proper structure, skill references, and best practices. Use when adding AI assistant guidance to a project or subdirectory.
---

Create effective AGENTS.md files that delegate work to existing skills.

**Key Principle**: Keep under 150 lines, link to details, defer workflows to skills.

1. **Identify Scope**
   - **Root**: Organization-wide standards, overall architecture
   - **Subdirectory**: Context-specific guidance (e.g., `src/ApiService/AGENTS.md`)
   - Use nested files when root exceeds 150 lines

2. **Use Template**
   - Copy [templates/AGENTS.md](templates/AGENTS.md) as starting point
   - Replace all `{placeholders}` with actual values
   - Follow [templates/BEST-PRACTICES.md](templates/BEST-PRACTICES.md) for guidance

3. **Reference Skills, Don't Explain**
   - ✅ "**Scaffold**: `/wolverine__create_operation`"
   - ❌ "To add a write operation: 1. Create command... 2. Create event... 3. Add Apply..."
   - Check `.claude/skills/` for available skills

4. **Follow Structure**
   - Quick Reference (stack, commands)
   - Key Rules (✅ good / ❌ bad)
   - Common Mistakes (→ solutions)
   - Project Layout (table)
   - Skills (categorized)
   - Quick Troubleshooting
   - Documentation Index

// turbo
5. **Verify Quality**
   - Use [templates/CHECKLIST.md](templates/CHECKLIST.md) for validation
   - Run: `wc -l AGENTS.md` (should be < 150)
   - Check all skill references exist
   - Ensure no sensitive information

## Related Skills

**Prerequisites**:
- None - This skill is standalone

**Next Steps**:
- Test the AGENTS.md by asking an AI agent to perform common tasks
- Update AGENTS.md in pull requests when processes change

**See Also**:
- `/meta__create_skill` - For creating new skills referenced in AGENTS.md

