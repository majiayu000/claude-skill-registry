---
name: spec-issues-create
description: Generate GitHub issue drafts from spec directories, creating initiative/feature/task markdown files with gh CLI commands. Use when converting specs to GitHub issues or setting up issue tracking for features.
---

# Spec Issues Skill

Generate GitHub issue drafts from spec documents following the project's issue management framework.

---

## When to Use

Use when you need to create GitHub issues from:
- Spec documents (`./specs/`)
- Any structured work breakdown ready for issue tracking

---

## Workflow

### Step 1: Validate Input Path

Parse path from command argument and verify:

```bash
# User provides path like:
# ./specs/active/my-feature
# ./specs/archive/nested-view-refactor
```

Validate directory exists and contains appropriate files.

### Step 2: Detect Issue Type

**Spec indicators:**
- Has `spec.md`
- Has `tasks.md`
- Has `context.md`

**Issue type detection:**

1. Read spec.md frontmatter for `issue_type` field:
   ```yaml
   ---
   issue_type: [Initiative|Feature|Task]
   created: [Date]
   status: Active
   ---
   ```

2. If `issue_type` present in frontmatter:
   - Skip type selection question
   - Use frontmatter value directly for template selection

3. If `issue_type` absent:
   - Fall back to current detection logic (spec overview analysis)
   - Consider asking user to classify

**Template selection based on issue_type:**
- `Initiative` → `templates/initiative.md`
- `Feature` → `templates/feature.md`
- `Task` → `templates/task.md`

Read appropriate files based on detected type.

### Step 3: Create Issue Drafts Directory

```bash
mkdir -p "$SOURCE_DIR/drafts/issues"
```

**Structure created:**
```
./specs/archive/{spec-name}/drafts/issues/
├── initiative-{spec-name}.md
├── issue-001-{short-description}.md
├── issue-002-{short-description}.md
└── ...
```

### Step 4: Generate Issue Draft Files

Create issue markdown files using templates:

**Initiative file**: `initiative-{name}.md`
- Use [templates/initiative.md](templates/initiative.md)
- Map spec overview → initiative overview
- Map success criteria → acceptance criteria
- Include YAML frontmatter with metadata

**Feature/Task files**: `issue-{NNN}-{description}.md`
- Use [templates/feature.md](templates/feature.md) or [templates/task.md](templates/task.md)
- Extract from spec phases or tasks
- Sequential numbering: 001, 002, 003
- Include YAML frontmatter

**Key points:**
- YAML frontmatter contains: title, labels, milestone, assignees
- Frontmatter serves as reference metadata
- Content extracted from spec documents

### Step 5: Generate gh CLI Script

Create bash script using [scripts/create-issue.sh](scripts/create-issue.sh):

- Parse YAML frontmatter from draft files
- Generate `gh issue create` commands
- Capture issue numbers for sub-issue linking
- Use `gh sub-issue add` for hierarchy
- Include helper function to extract YAML fields

**Script structure:**
```bash
#!/bin/bash
# Extract YAML → gh issue create → capture numbers → link sub-issues
```

### Step 6: Provide Metadata Configuration Checklist

Include instructions for setting fields via GitHub web UI:
- Priority (Critical/High/Medium/Low)
- Status (Backlog/To Do/In Progress/etc.)
- Sprint/Iteration
- Complexity estimation
- Milestone/Release

---

## Content Transformation

See [mapping-guide.md](mapping-guide.md) for detailed rules on:
- Mapping spec content to issue hierarchy (Initiative → Feature → Task)
- Issue title patterns for each type
- Component label detection from file paths
- Priority and complexity mapping
- Cross-linking patterns

Quick summary:
- Specs: phases → Features, task breakdown → Tasks
- Titles follow verb-noun pattern, increasing specificity by level

---

## Templates

- [templates/initiative.md](templates/initiative.md) - Initiative issue template with YAML
- [templates/feature.md](templates/feature.md) - Feature issue template with YAML
- [templates/task.md](templates/task.md) - Task issue template with YAML

## Scripts

**generate-issues.py**: Automates draft generation from specs. Parses content, creates issue files with YAML frontmatter.
**create-issue.sh**: Creates actual GitHub issues from drafts using `gh` CLI.

**Requirement**: Install `gh sub-issue` extension: `gh extension install yahsan2/gh-sub-issue`

---

## Success Criteria

- Drafts directory created: `{source}/drafts/issues/`
- Initiative file with complete overview
- Feature/task files with proper templates
- gh CLI script with issue creation commands
- Metadata checklist provided

---

## Integration

**Workflow:**
1. Complete spec
2. Invoke this skill with source path
3. Review generated draft files
4. Run gh CLI script to create issues
5. Set metadata via GitHub web UI

**Related:**
- Command: `/spec.issues`
- Tools: `gh` CLI, `gh sub-issue` extension
