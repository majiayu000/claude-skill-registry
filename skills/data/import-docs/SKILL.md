---
name: import-docs
description: Import brownfield documentation from Notion exports, Confluence, GitHub Wiki, or any markdown folder. Automatically classifies files as specs, modules, team docs, or legacy.
---

# Import Brownfield Documentation

Import existing documentation from Notion exports, Confluence, GitHub Wiki, or any markdown folder.

## What This Does

1. **Analyzes markdown files** in source directory (recursively)
2. **Classifies files** based on content:
   - **Specs** - Contains "user story", "acceptance criteria", "feature"
   - **Modules** - Contains "module", "component", "architecture"
   - **Team** - Contains "onboarding", "convention", "workflow"
   - **Legacy** - Everything else (no strong match)
3. **Copies files** to appropriate destinations
4. **Creates migration report** with classification details
5. **Updates config** with import history

## Usage

```bash
/sw:import-docs <source-path> [options]
```

### Options

- `--source=<type>` - Source type: `notion`, `confluence`, `wiki`, `custom` (required)
- `--project=<id>` - Target project ID (default: active project)
- `--preserve-structure` - Preserve original folder structure
- `--dry-run` - Preview classification without importing

## Examples

### Example 1: Notion Export

```bash
# Export Notion workspace to /tmp/notion-export/
# Then import:

/sw:import-docs /tmp/notion-export/ --source=notion

# Result:
# 📊 Analysis Results:
#    Total files: 47
#    - Specs: 12 files → specs/
#    - Modules: 18 files → modules/
#    - Team docs: 5 files → team/
#    - Legacy: 12 files → legacy/notion/
# ✅ Import complete!
```

### Example 2: Confluence Export

```bash
/sw:import-docs /path/to/confluence/ --source=confluence --project=web-app

# Imports to: projects/web-app/specs/, modules/, team/, legacy/confluence/
```

### Example 3: Dry Run (Preview)

```bash
/sw:import-docs /tmp/docs/ --source=custom --dry-run

# Shows classification without importing files
# Use this to preview results before actual import
```

### Example 4: Preserve Structure

```bash
/sw:import-docs /path/to/wiki/ --source=wiki --preserve-structure

# Preserves original folder structure:
# legacy/wiki/engineering/backend/auth.md
# legacy/wiki/engineering/frontend/components.md
```

## Supported Sources

### Notion
- **Export Format**: Markdown & CSV
- **Steps**:
  1. In Notion: Settings → Export → Export all workspace content
  2. Choose "Markdown & CSV" format
  3. Download ZIP file
  4. Extract to folder (e.g., `/tmp/notion-export/`)
  5. Run import command

### Confluence
- **Export Format**: HTML or Markdown
- **Steps**:
  1. Space tools → Content Tools → Export
  2. Choose HTML or Markdown
  3. Extract exported files
  4. Run import command

### GitHub Wiki
- **Export Format**: Git repository
- **Steps**:
  1. Clone wiki: `git clone https://github.com/user/repo.wiki.git`
  2. Run import command on cloned directory

### Custom (Any Markdown)
- Any folder containing `.md` or `.markdown` files
- Recursive search through subdirectories

## Classification Algorithm

Files are classified using keyword analysis:

### Specs (70%+ confidence)
- Keywords: "user story", "acceptance criteria", "feature", "requirement"
- Patterns: "As a [user], I want [goal]", "Given-When-Then"
- Example: Feature specs, PRDs, user stories

### Modules (70%+ confidence)
- Keywords: "module", "component", "service", "architecture"
- Patterns: API docs, technical design, integration points
- Example: Auth module, payment processing, ML pipeline

### Team (70%+ confidence)
- Keywords: "onboarding", "convention", "workflow", "pr process"
- Patterns: Team processes, coding standards, deployment guides
- Example: Onboarding guide, code review checklist

### Legacy (<70% confidence)
- No strong match to above categories
- Uncertain classification
- Requires manual review

## Destination Folders

Files are imported to:

```
.specweave/docs/internal/projects/{project}/
├── specs/              ← Specs (spec keywords)
├── modules/            ← Modules (module keywords)
├── team/               ← Team docs (team keywords)
└── legacy/{source}/    ← Legacy (uncertain classification)
    ├── notion/
    ├── confluence/
    ├── wiki/
    └── custom/
```

## Migration Report

After import, a detailed report is generated:

**Location**: `.specweave/docs/internal/projects/{project}/legacy/README.md`

**Contents**:
- Import summary (counts per category)
- Classification analysis (with confidence scores)
- List of imported files
- Next steps and recommendations

## Configuration Updates

Import history is tracked in `.specweave/config.json`:

```json
{
  "brownfield": {
    "importHistory": [{
      "source": "notion",
      "workspace": "acme-corp",
      "importedAt": "2025-11-06T10:30:00Z",
      "project": "web-app",
      "filesImported": 47,
      "destination": ".specweave/docs/internal/projects/web-app/legacy/notion/"
    }]
  }
}
```

## After Import

1. **Review classification** - Check migration report
2. **Move misclassified files** - Use file manager or git
3. **Update spec numbers** - Rename to `spec-NNN-name.md`
4. **Clean up legacy** - Delete obsolete content
5. **Update references** - Fix broken links

## When to Use

- **Migrating from Notion** to SpecWeave
- **Consolidating wikis** from GitHub, Confluence, etc.
- **Onboarding brownfield projects** with existing documentation
- **Merging multiple doc sources** into single SpecWeave instance

## Limitations

- Only markdown files (.md, .markdown) supported
- No direct API integration (use exports)
- Classification is heuristic (80%+ accuracy target)
- Manual review recommended for low-confidence files

## See Also

- `/sw:init-multiproject` - Set up multi-project mode first
- [Brownfield Import Guide](https://docs.spec-weave.com/guides/brownfield-import)
- [Migration Best Practices](https://docs.spec-weave.com/guides/migration-best-practices)

---

**Implementation**: `src/cli/commands/import-docs.ts`
