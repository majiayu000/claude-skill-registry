---
context: fork
---

# /broken-links

Scan the vault for broken [[wiki-links]] and suggest fixes using parallel Sonnet sub-agents.

## Usage

```
/broken-links
/broken-links --auto-fix    # Interactive fixes with suggestions
```

## Instructions

This skill uses **3 parallel Sonnet sub-agents** to scan different vault areas concurrently for maximum performance.

### Phase 1: Launch Parallel Link Scanners

Create **3 Task agents** running in parallel with `model: "sonnet"`:

**Agent 1: Root Directory Scanner** (Sonnet)
```
Task: Scan root directory for broken wiki-links
- Use Glob to find all *.md files in root (exclude +Daily, +Meetings, +Templates)
- For each file, use Read tool to get content
- Extract all [[wiki-links]] using regex: \[\[([^\]|]+)(\|[^\]]+)?\]\]
- Also check frontmatter fields for wiki-links
- Build list of all referenced note names
- Compare against existing files using Glob
- Return: List of broken links with source files
Format:
{
  "source": "filename.md",
  "brokenLinks": ["Missing Note 1", "Missing Note 2"],
  "line": "content snippet with [[broken link]]"
}
```

**Agent 2: Meetings Directory Scanner** (Sonnet)
```
Task: Scan +Meetings/ directory for broken wiki-links
- Use Glob to find all *.md files in +Meetings/
- For each file, extract [[wiki-links]] from content and frontmatter
- Check attendees, project links, and inline person references
- Identify missing Person, Project, and Organisation notes
- Return: List of broken links in meeting notes
```

**Agent 3: Daily Notes Scanner** (Sonnet)
```
Task: Scan +Daily/ directory for broken wiki-links
- Use Glob to find all *.md files in +Daily/
- Extract [[wiki-links]] from daily notes
- Check task references, project links, person mentions
- Identify temporal references that may be broken
- Return: List of broken links in daily notes
```

### Phase 2: Consolidate Results

After all 3 agents complete:

1. **Merge Results**
   - Combine all broken links from 3 agents
   - Remove duplicates
   - Group by target note (show all sources linking to same missing note)

2. **Categorize by Severity**
   - **Critical**: Links in ADRs, Projects, important Pages (5+ backlinks)
   - **Warning**: Links in Tasks, Meetings (2-4 backlinks)
   - **Info**: Links in Daily Notes, single mentions (1 backlink)

3. **Fuzzy Match Suggestions**
   - For each broken link, find similar existing notes:
     - Case-insensitive matching
     - Levenshtein distance < 3
     - Partial word matches
   - Suggest: "Did you mean [[Actual Note]]?"

### Phase 3: Generate Report

```markdown
# Broken Wiki-Links Report

Generated: {{DATE}}
Total Broken Links: {{count}}

## Critical ({{critical_count}})

### [[Missing Note Name]] (referenced {{count}} times)

**Referenced in:**
- [[Source Note 1]] (line 42): "Context snippet with [[Missing Note Name]]"
- [[Source Note 2]] (line 15): "Another context [[Missing Note Name]]"

**Suggestions:**
- Did you mean [[Similar Note]]? (85% match)
- Did you mean [[Another Match]]? (72% match)

**Actions:**
- [ ] Create the note [[Missing Note Name]]
- [ ] Replace with [[Similar Note]] in all references
- [ ] Remove the broken links

---

## Warnings ({{warning_count}})

{{same format}}

## Info ({{info_count}})

{{same format}}

## Summary

| Severity | Count | % of Total |
|----------|-------|------------|
| Critical | {{n}}  | {{%}}     |
| Warning  | {{n}}  | {{%}}     |
| Info     | {{n}}  | {{%}}     |

## Next Steps

1. **Create Missing Critical Notes**: {{list top 5}}
2. **Fix Case Mismatches**: {{list}}
3. **Review and Clean Up Info-level**: {{list}}
```

### Phase 4: Interactive Fixes (Optional)

If `--auto-fix` flag is provided:

1. **Case Mismatch Fixes** (automatic)
   - Find: [[project - Cloud Migration]]
   - Should be: [[Project - Cloud Migration]]
   - Auto-fix these with Edit tool

2. **Fuzzy Match Replacements** (prompt user)
   - Show: "Replace [[Mising Note]] with [[Missing Note]]?"
   - If yes, use Edit tool to fix all occurrences

3. **Bulk Deletions** (prompt user)
   - Show: "Remove all references to [[Deleted Note]] (confirmed deleted)?"
   - If yes, remove links but keep context text

## Use Cases

**Vault Cleanup:**
- After bulk file operations (renames, deletions)
- After importing from other tools
- Regular maintenance (monthly checks)

**Link Hygiene:**
- Fix case mismatches
- Remove links to deleted notes
- Identify orphaned concepts

**Refactoring Support:**
- Pre-rename validation
- Post-migration verification
- Merge duplicate notes

**Quality Assurance:**
- Pre-commit validation
- CI/CD pipeline checks
- Vault health monitoring

## Performance

- **3 parallel agents** = 3x faster than sequential scan
- **~500 notes**: 15-30 seconds
- **~2000 notes**: 1-2 minutes
- **~5000 notes**: 3-5 minutes

## Notes

- Excludes checking links in +Templates/ (templates often reference non-existent placeholders)
- Handles both `[[Note Name]]` and `[[Note Name|Display Text]]` formats
- Checks frontmatter wiki-links (project, attendees, relatedTo, etc.)
- Ignores heading/block references: `[[Note#Heading]]` → checks `Note` exists
- Case-sensitive by default, but suggests case mismatches
- Works with all note types (Task, Project, Person, ADR, Meeting, Page, etc.)
