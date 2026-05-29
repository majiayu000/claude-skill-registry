---
name: plugin-apply-lessons-learned
description: Apply accumulated lessons learned to component documentation
user-invocable: true
allowed-tools: Skill, Read, Edit, Glob, Bash
---

# Apply Lessons Learned Skill

Read lessons learned via `manage-lessons` skill and apply them to component documentation.

## Usage

```
# Apply lessons to specific component
/plugin-apply-lessons-learned command=maven-build-and-fix
/plugin-apply-lessons-learned agent=maven-builder
/plugin-apply-lessons-learned skill=builder-maven-rules

# Apply all unapplied lessons across components
/plugin-apply-lessons-learned --all

# List unapplied lessons (dry-run)
/plugin-apply-lessons-learned --list

# Show usage
/plugin-apply-lessons-learned
```

## WORKFLOW

### Step 1: Parse Parameters

- Extract component type and name, or flags (--all, --list)
- Validate parameter syntax

### Step 2: Load Lessons Learned Skill

```
Skill: plan-marshall:manage-lessons
```

### Step 3: Query Unapplied Lessons

- Use `query-lessons.py` script to filter lesson files
- For specific component: Filter by `component.name`
- For --all: Filter all where `applied: false`
- For --list: Display lessons without applying

### Step 4: For Each Unapplied Lesson

a. **Locate component source**:
   - Commands: `marketplace/bundles/{bundle}/commands/{name}.md`
   - Agents: `marketplace/bundles/{bundle}/agents/{name}.md`
   - Skills: `marketplace/bundles/{bundle}/skills/{name}/SKILL.md`

b. **Analyze lesson category**:
   - `bug`: Add to CRITICAL RULES or error handling section
   - `improvement`: Add to workflow or suggest enhancement
   - `pattern`: Add to best practices or examples
   - `anti-pattern`: Add to warnings or "do not" section

c. **Determine appropriate placement**:
   - Read component documentation
   - Find relevant section for lesson category
   - Prepare edit that integrates lesson naturally

d. **Apply lesson**:
   - Edit component documentation
   - Integrate lesson content (not raw JSON, but natural prose)
   - Maintain document structure and formatting

e. **Mark lesson applied**:
   - Edit lesson file frontmatter: Change `applied: false` to `applied: true`

### Step 5: Report Results

- Number of lessons applied per component
- Any lessons that couldn't be applied (with reason)
- Components updated

## PARAMETERS

**Component targeting** (mutually exclusive with flags):
- `command={name}` - Apply lessons for specific command
- `agent={name}` - Apply lessons for specific agent
- `skill={name}` - Apply lessons for specific skill

**Flags**:
- `--all` - Apply all unapplied lessons across all components
- `--list` - List unapplied lessons without applying (dry-run)

**Error Handling**:
- No parameters → Display usage
- Component not found → Error with suggestion
- No lessons file → Report "no lessons recorded"
- No unapplied lessons → Report "nothing to apply"

## LESSON APPLICATION RULES

### Bug Lessons

Add to component's error handling or critical rules section:

```markdown
## CRITICAL RULES

- **Paths with spaces**: Quote all paths in Bash calls to handle spaces correctly
```

### Improvement Lessons

Add as enhancement notes or workflow refinements:

```markdown
### Step 3: Process Files

**Enhancement**: Add progress indicator every 50 files for large batches.
```

### Pattern Lessons

Add to examples or best practices:

```markdown
## Best Practices

- Validate all inputs in Step 1 before processing to catch errors early
```

### Anti-Pattern Lessons

Add to warnings or "avoid" sections:

```markdown
## CRITICAL RULES

**Avoid:**
- Do NOT modify files during glob iteration - collect list first, then process
```

## OUTPUT FORMAT

```
## Applied Lessons

### command/maven-build-and-fix
- [2025-11-25-001] bug: Paths with spaces → Added to CRITICAL RULES
- [2025-11-25-002] improvement: Progress indicator → Added enhancement note

### agent/maven-builder
- [2025-11-24-001] pattern: Verify phase → Added to best practices

## Summary
- Components updated: 2
- Lessons applied: 3
- Lessons skipped: 0
```

## Related

- `plan-marshall:manage-lessons` - Skill for lesson storage/retrieval
- `/plugin-maintain` - General component maintenance
- `/plugin-doctor` - Diagnose component issues
