---
name: documentation-update
description: Reusable logic for updating repository documentation (README, indices, tables) with new content while preserving formatting and structure
---

# Documentation Update Skill

## When to Use This Skill

- Adding entries to README.md tables after integration
- Updating skill/command/agent indices
- Maintaining table of contents
- Cross-referencing new content
- Keeping documentation in sync with codebase

## What This Skill Does

Provides systematic approaches for:
- **Table Updates** - Adding rows while preserving format
- **Alphabetical Insertion** - Maintaining sorted order
- **Link Validation** - Ensuring references are correct
- **Format Preservation** - Matching existing markdown style
- **Duplicate Prevention** - Avoiding redundant entries

## Table Update Patterns

### Pattern 1: Adding to Markdown Tables

**Identify Table Structure**:
```markdown
| Column1 | Column2 | Column3 |
|---------|---------|---------|
| Value1  | Value2  | Value3  |
```

**Steps**:
1. **Locate table** - Search for table header
2. **Extract format** - Note column alignment (left/center/right)
3. **Create new row** - Match column count and format
4. **Insert position** - Alphabetical or by category
5. **Validate** - Ensure pipes align, no extra/missing columns

**Example - Adding Skill to README**:

Original:
```markdown
| Skill | Purpose | Use When |
|-------|---------|----------|
| **skill-creator** | Creates new skills | Building new automation |
| **skill-orchestrator** | Coordinates multiple skills | Complex workflows |
```

New Entry Data:
```
Name: using-git-worktrees
Purpose: Isolated workspace management
Use When: Feature work needing isolation
```

Updated (alphabetically inserted):
```markdown
| Skill | Purpose | Use When |
|-------|---------|----------|
| **skill-creator** | Creates new skills | Building new automation |
| **skill-orchestrator** | Coordinates multiple skills | Complex workflows |
| **using-git-worktrees** | Isolated workspace management | Feature work needing isolation |
```

### Pattern 2: Alphabetical Insertion

**Algorithm**:
```
function insertAlphabetically(table, newEntry):
  rows = table.split("\n")
  headerRow = rows[0]
  separatorRow = rows[1]
  dataRows = rows[2..]

  // Extract first column values for sorting
  existingEntries = dataRows.map(row => extractFirstColumn(row))

  // Find insertion point
  insertionIndex = 0
  for i, entry in existingEntries:
    if newEntry < entry:
      insertionIndex = i
      break
    else:
      insertionIndex = i + 1

  // Insert new row
  dataRows.insert(insertionIndex, formatRow(newEntry))

  // Rebuild table
  return [headerRow, separatorRow, ...dataRows].join("\n")
```

### Pattern 3: Category-Based Tables

For tables organized by category (not alphabetical):

**Example - Command Categories**:
```markdown
#### Core Workflow Commands
- **start-session.md** - Initialize development session
- **close-session.md** - End session with summary

#### Quality Assurance Commands
- **test-all.md** - Execute test suites
- **lint-fixes.md** - Auto-fix style issues
```

**Insertion Logic**:
1. Determine category from content/metadata
2. Locate correct category section
3. Add to end of that category (or alphabetically within)
4. Maintain bullet/numbering format

## Link Update Patterns

### Pattern 4: Updating Cross-References

**Find and Update Links**:
```markdown
Old: See [Document 07](docs/best-practices/07-Quick-Reference.md)
New: See [Document 07](docs/best-practices/07-Quick-Reference.md) and [Document 08](docs/best-practices/08-Skills-Guide.md)
```

**Validation**:
```bash
# Check link target exists
!test -f docs/best-practices/08-Skills-Guide.md && echo "✅ Valid"
```

### Pattern 5: Creating Index Files

**For skills/README.md**:

```markdown
# Skills Directory

## Available Skills

[Auto-generated table from skills/*/SKILL.md files]

| Skill | Description | Category |
|-------|-------------|----------|
[Rows auto-populated from frontmatter]

## Usage

[Standard usage instructions]

## Creating Skills

[Link to templates and guides]
```

**Generation Logic**:
```
function generateSkillsIndex():
  skills = findAll("skills/*/SKILL.md")

  table = createTable(["Skill", "Description", "Category"])

  for skill in skills:
    frontmatter = extractFrontmatter(skill)
    name = frontmatter.name
    description = frontmatter.description
    category = determineCategory(skill)

    table.addRow([name, description, category])

  table.sortAlphabetically()

  return table
```

## Format Preservation

### Matching Existing Style

**Detect Style**:
```
- Bold pattern: **text** or __text__
- Link pattern: [text](url) or [text][ref]
- List style: - item or * item or 1. item
- Code blocks: ```lang or ~~~lang
- Headers: # H1 or ## H2 (ATX style)
```

**Apply Consistently**:
```markdown
# If existing entries use:
| **bold-name** | Description |

# New entry must use:
| **new-entry** | Description |

# NOT:
| new-entry | Description |
```

### Column Alignment

Preserve alignment indicators:
```markdown
| Left | Center | Right |
|:-----|:------:|------:|
| L1   |   C1   |    R1 |
| L2   |   C2   |    R2 |
```

New row must match:
```markdown
| New  |  Data  |   123 |
```

## Duplicate Prevention

### Check Before Adding

```
function isDuplicate(table, newEntry):
  existingEntries = extractEntriesFromTable(table)

  for entry in existingEntries:
    if entry.name == newEntry.name:
      return true
    if entry.path == newEntry.path:
      return true

  return false
```

**Action on Duplicate**:
- **Exact match**: Skip, note in update report
- **Similar match**: Flag for review
- **Same name, different path**: Warning, possible conflict

## Example Usage

### Example 1: Add 6 Skills to README

**Input**:
```javascript
skills = [
  {name: "content-research-writer", purpose: "Writing assistance", useWhen: "Writing articles"},
  {name: "root-cause-tracing", purpose: "Systematic debugging", useWhen: "Tracing bugs"},
  {name: "sharing-skills", purpose: "Contribute skills upstream", useWhen: "Sharing patterns"},
  {name: "subagent-driven-development", purpose: "Execute plans with subagents", useWhen: "Plan execution"},
  {name: "using-git-worktrees", purpose: "Isolated workspace management", useWhen: "Feature isolation"},
  {name: "using-superpowers", purpose: "Meta-skill for skill discovery", useWhen: "Starting conversations"}
]
```

**Process**:
1. Read README.md
2. Locate "Pre-Built Skills" table
3. For each skill:
   - Check for duplicates
   - Format as table row
   - Insert alphabetically
4. Write updated README.md
5. Verify table structure intact

**Output Report**:
```markdown
### README.md Updates
- ✅ Added 6 skills to Pre-Built Skills table
- ✅ Alphabetical order maintained
- ✅ No duplicates created
- ✅ Table format preserved
- ✅ All links validated
```

### Example 2: Create skills/README.md Index

**Input**: List of all skills in `skills/*/SKILL.md`

**Process**:
1. Scan `skills/` directory
2. Read each SKILL.md file
3. Extract frontmatter (name, description)
4. Categorize by type (workflow/content/meta)
5. Generate organized tables
6. Add usage instructions
7. Write to skills/README.md

**Output**: Comprehensive index file with categorized skill tables

### Example 3: Update Command List

**Input**: New command `integration-process.md`

**Process**:
1. Determine category: "Integration & Maintenance Commands"
2. Extract description from frontmatter
3. Locate category section in README
4. Format as bullet item with link
5. Insert (alphabetically or at end)
6. Save README.md

## Validation Checks

### Pre-Update Validation

- [ ] Target file exists and is writable
- [ ] Table structure is valid
- [ ] New entry has all required fields
- [ ] No duplicate entries
- [ ] Links reference existing files

### Post-Update Validation

- [ ] Table structure still valid
- [ ] No broken pipes or misaligned columns
- [ ] All links still work
- [ ] Alphabetical order maintained (if applicable)
- [ ] No extra blank lines introduced

### Validation Commands

```bash
# Check table structure
!grep -A 5 "| Skill | Purpose |" README.md | head -10

# Verify link targets
!for link in $(grep -o "\](.*\.md)" README.md | tr -d ']()'); do
  test -f "$link" || echo "Broken: $link"
done

# Count table rows
!grep -c "|.*|.*|" README.md
```

## Error Handling

### Malformed Table

```
Error: Table has inconsistent column counts
Action: Report error, do not modify
Fix: Manually correct table structure first
```

### File Not Writable

```
Error: Permission denied writing to README.md
Action: Log error, skip update
Fallback: Create pending-updates.md with changes
```

### Duplicate Entry

```
Warning: Skill "using-git-worktrees" already in table
Action: Skip insertion, note in report
Info: Entry exists at line 156
```

## Integration with Commands

### Used By

- `/integration-update-docs` - Primary documentation updater
- `/maintenance-plan-update` - DEVELOPMENT_PLAN.md updates
- Custom documentation workflows

### Usage Pattern

```markdown
# In integration-update-docs command

After integration:
  1. Load integration report
  2. For each integrated file:
     - Use documentation-update skill
     - Update appropriate doc files
     - Validate changes
  3. Generate doc update report
```

## Best Practices

### DO
- ✅ Always backup before modifying
- ✅ Validate table structure before and after
- ✅ Preserve existing formatting
- ✅ Check for duplicates
- ✅ Verify all links
- ✅ Maintain alphabetical order
- ✅ Test with git diff before committing

### DON'T
- ❌ Assume table structure
- ❌ Mix formatting styles
- ❌ Skip duplicate checks
- ❌ Modify without validation
- ❌ Break existing links
- ❌ Introduce trailing whitespace

## Testing Recommendations

Test with:
1. **Simple table** - Add single entry to clean table
2. **Complex table** - Multi-column with formatting
3. **Edge cases** - Empty table, single row, malformed
4. **Bulk updates** - Add 10+ entries at once
5. **Recovery** - Test rollback on error

Expected behavior:
- **Clean tables**: 100% success
- **Malformed tables**: Detect and report, no corruption
- **Duplicates**: Detect and skip appropriately

## Version History

**1.0** (2025-11-23)
- Initial documentation update skill
- Table manipulation logic
- Link validation
- Format preservation
- Duplicate prevention

---

**Skill Status**: Production Ready
**Integration**: Used by /integration-update-docs
**Dependencies**: None (standalone logic)
