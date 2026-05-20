---
name: obsidian-base-create
description: |
  Generates Obsidian .base files from natural language descriptions. Translates
  requests like "show me all active project notes sorted by date" into valid
  .base YAML with filters, formulas, views, and summaries. Activates on
  "create base", "make a view", "show me all notes where", "dashboard", or when
  user wants structured views of their vault.
allowed-tools: |
  bash: ls, find, cat
  file: read, write
---

# Obsidian Base Create

<purpose>
Bases bring database-style views to Obsidian — tables, cards, lists, maps —
all powered by note frontmatter. The .base format is YAML but the syntax is
non-obvious: nested filter logic, formula functions, property references, view
configurations. This skill translates what you want to see into working .base
files.
</purpose>

## When To Activate

<triggers>
- User says "create base", "make a base", "new base"
- User says "show me all notes where...", "filter my notes", "dashboard"
- User says "I want a table of...", "list all my...", "view of..."
- User wants to track tasks, projects, readings, meetings across notes
- After vault init when creating starter views
</triggers>

Do NOT trigger for:
- Editing existing .base files (edit directly)
- Simple search queries (use obsidian-vault-search)
- Views that don't depend on frontmatter properties

## Instructions

### Step 1: Understand What the User Wants to See

<clarify>
Map the request to a base configuration:

| Request | View Type | Key Filter | Sort |
|---------|-----------|------------|------|
| "All my meetings" | table | type == meeting | date desc |
| "Active projects" | cards | type == project AND status == active | name asc |
| "Tasks this week" | table | type == task AND date >= week start | date asc |
| "Recent notes" | table | (none or date-based) | file.mtime desc |
| "Reading list" | cards | type == reference AND status == draft | created desc |

Ask if not obvious:
- What properties should show as columns?
- How should it be sorted?
- Table, cards, or list view?
</clarify>

### Step 2: Check Available Properties

<properties>
Before building filters, check what properties actually exist in the vault:

```bash
# Find all frontmatter properties used in the vault
grep -rh "^[a-z].*:" "$VAULT_PATH" --include="*.md" | \
  grep -v "^#\|^-\|^ " | sort | uniq -c | sort -rn | head -20
```

Common properties from the vault schema (check CLAUDE.md):
- `type`: note, meeting, project, daily, reference, task
- `status`: draft, active, completed, archived
- `date`: YYYY-MM-DD
- `created`: YYYY-MM-DD
- `project`: project name
- `tags`: array of tags
- `attendees`: list (meetings)

Don't create filters on properties that don't exist in the vault.
</properties>

### Step 3: Build the Base YAML

<build>
Base file structure:

```yaml
# Global filter (applies to all views)
filter:
  - property: <name>
    operator: "<op>"
    value: "<value>"

# Computed properties
formulas:
  formula-name: '<expression>'

# View configurations
views:
  - name: "View Name"
    type: table  # table, cards, list, map
    properties:
      - file.name
      - property-name
    sort:
      - property: <name>
        order: asc  # or desc
    filter:  # view-specific filter (in addition to global)
      - property: <name>
        operator: "<op>"
        value: "<value>"
```

**Filter operators:**
| Operator | Meaning |
|----------|---------|
| `==` | equals |
| `!=` | not equals |
| `>` | greater than |
| `<` | less than |
| `>=` | greater or equal |
| `<=` | less or equal |

**Compound filters (AND/OR/NOT):**
```yaml
filter:
  # AND (default — sequential conditions)
  - property: type
    operator: "=="
    value: meeting
  - property: status
    operator: "=="
    value: active

  # OR (explicit)
  - operator: OR
    conditions:
      - property: type
        operator: "=="
        value: meeting
      - property: type
        operator: "=="
        value: project

  # NOT
  - operator: NOT
    conditions:
      - property: status
        operator: "=="
        value: archived
```

**File metadata properties:**
```
file.name     — Note filename without extension
file.path     — Full path from vault root
file.mtime    — Last modified time
file.ctime    — Creation time
file.size     — File size in bytes
file.folder   — Parent folder path
file.ext      — File extension
```
</build>

### Step 4: Add Formulas (if needed)

<formulas>
Formulas are computed properties that derive values from existing data:

```yaml
formulas:
  # Days since creation
  age: '(now() - this.created).days'

  # Status badge
  badge: 'if(this.status == "active", "🟢", if(this.status == "draft", "🟡", "⚪"))'

  # Overdue check
  overdue: 'if(this.date < today(), "⚠️ Overdue", "On track")'

  # Tag count
  tag-count: 'this.tags.length'

  # Full name from path
  display: 'this.file.name'
```

**Useful formula functions:**
- Date: `now()`, `today()`, `date("YYYY-MM-DD")`, `format(date, "MMM DD")`, `relative(date)`
- String: `contains(str, substr)`, `replace(str, old, new)`, `lower(str)`, `trim(str)`
- Number: `abs()`, `ceil()`, `floor()`, `round()`
- List: `filter()`, `map()`, `join()`, `sort()`, `.length`
- File: `hasTag(tag)`, `hasProperty(prop)`, `inFolder(path)`, `asLink()`
- Logic: `if(condition, then, else)`

**The `this` keyword** refers to the current row's note.
</formulas>

### Step 5: Configure View

<views>
**Table view** (best for data-heavy views):
```yaml
views:
  - name: "All Meetings"
    type: table
    properties:
      - file.name
      - date
      - attendees
      - project
      - status
    sort:
      - property: date
        order: desc
```

**Cards view** (best for visual browsing):
```yaml
views:
  - name: "Active Projects"
    type: cards
    properties:
      - file.name
      - status
      - tags
    sort:
      - property: file.name
        order: asc
```

**List view** (best for simple lists):
```yaml
views:
  - name: "Quick List"
    type: list
    properties:
      - file.name
    sort:
      - property: file.mtime
        order: desc
```

**Multiple views** (same base, different perspectives):
```yaml
views:
  - name: "Table"
    type: table
    properties: [file.name, status, date]
    sort: [{property: date, order: desc}]

  - name: "Cards"
    type: cards
    properties: [file.name, status]
    sort: [{property: status, order: asc}]
```

**Summaries** (aggregate values shown at column bottom):
```yaml
views:
  - name: "Project Budget"
    type: table
    properties:
      - file.name
      - budget
      - spent
    summaries:
      budget: sum
      spent: sum
```

Summary types: `average`, `min`, `max`, `sum`, `range`, `median`, `count`,
`earliest`, `latest`, `checked`, `unchecked`, `empty`, `filled`, `unique`
</views>

### Step 6: Write and Verify

<write>
```bash
# Name the base file descriptively
BASE_PATH="$VAULT_PATH/base-name.base"
```

Write the YAML. Then verify by checking the YAML is valid:

```bash
python3 -c "import yaml; yaml.safe_load(open('$BASE_PATH'))" && echo "Valid YAML"
```

Confirm:
```markdown
Base created: base-name.base

View: [table / cards / list]
Filter: [what's filtered]
Columns: [listed properties]
Sort: [sort order]

Open in Obsidian to see your data.
```
</write>

## Output Format

```markdown
## Base Created

**File:** base-name.base
**View:** [table / cards / list / map]
**Filter:** [description of filter logic]
**Columns:** [list of shown properties]
**Sort:** [property, direction]
**Formulas:** [any computed properties]

Open in Obsidian to interact with the view.
```

## NEVER

- Create filters on properties that don't exist in the vault
- Write invalid YAML (always validate)
- Skip checking what properties exist first
- Use complex formulas without explaining what they compute
- Create a base without at least one view configured
- Assume property names — check CLAUDE.md or scan existing notes

## ALWAYS

- Check what frontmatter properties exist in the vault first
- Validate the YAML output
- Include at least `file.name` in every view's properties
- Use descriptive view names
- Explain the filter logic in plain English
- Suggest additional views or formulas that might be useful

## Example

**User:** "Make me a dashboard showing all active projects with their status and last modified date"

```yaml
filter:
  - property: type
    operator: "=="
    value: project
  - property: status
    operator: "!="
    value: archived

formulas:
  last-active: 'relative(this.file.mtime)'

views:
  - name: "Active Projects"
    type: table
    properties:
      - file.name
      - status
      - project
      - tags
      - last-active
    sort:
      - property: file.mtime
        order: desc

  - name: "Project Cards"
    type: cards
    properties:
      - file.name
      - status
      - last-active
    sort:
      - property: status
        order: asc
```

```
Base created: project-dashboard.base

View 1: "Active Projects" (table)
  Filter: type == project AND status != archived
  Columns: name, status, project, tags, last active (relative time)
  Sort: last modified (newest first)

View 2: "Project Cards" (cards)
  Same filter, card layout for visual browsing

Open in Obsidian to see your projects.
```

<failed-attempts>
What DOESN'T work:
- Filtering on `content` or note body — Bases only filters on frontmatter properties and file metadata
- Using Dataview syntax (`FROM`, `WHERE`) — Bases has its own YAML syntax, not Dataview
- Assuming properties exist — if notes don't have `status` in frontmatter, the filter returns nothing
- Complex nested formulas without testing — start simple, iterate
</failed-attempts>
