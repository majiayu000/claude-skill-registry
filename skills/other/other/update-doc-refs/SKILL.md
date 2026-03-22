---
name: update-doc-refs
version: "1.0.0"
description: Update documentation references after structure migration - pure AI instruction implementation
last-updated: "2026-03-16"
---

# Update Doc Refs - Documentation Reference Updater

> Automatically update all documentation references after structure migration

## Overview

This skill updates documentation references throughout the project after `/migrate-docs` restructures the documentation.

**What it does:**
1. Detects documentation structure changes (compares docs.old/ vs docs/)
2. Scans project files for documentation references
3. Intelligently replaces references based on context (7 scenarios)
4. Validates updated links point to existing files
5. Generates detailed change report

**Why it's needed:**
After documentation migration, references scattered across Markdown files, source code, and configuration files become outdated. Manual updates are error-prone and time-consuming. This skill automates the process with intelligent context awareness.

**When to use:**
- After running `/migrate-docs` on a project
- When documentation structure has changed
- To fix broken documentation links project-wide

**Workflow integration:**
```bash
cd ~/dev/ai-dev
/migrate-docs ../buffer           # Step 1: Migrate docs structure
cd ../buffer
/update-doc-refs                  # Step 2: Update all references (this skill)
/check-docs --verbose             # Step 3: Validate result
```

## Arguments

```bash
/update-doc-refs [options]
```

**Common usage:**
```bash
/update-doc-refs                  # Basic usage
/update-doc-refs --dry-run        # Preview changes
/update-doc-refs --verbose        # Detailed output
```

**Options:**
- `--dry-run` - Preview changes without applying
- `--verbose` - Show detailed output for each replacement
- `--quiet` - Minimal output (only summary)

## TRIGGER Conditions

**Invoke this skill when user wants to:**
- "update doc refs after migration"
- "fix documentation references in buffer"
- "update all doc links after restructuring"
- "run update-doc-refs on ../buffer"

**DO NOT invoke when:**
- User wants to migrate docs (use `/migrate-docs`)
- User wants to check docs (use `/check-docs`)
- User wants to initialize docs (use `/init-docs`)

## Execution Steps

### Step 1: Detect Documentation Structure Changes

**Purpose**: Generate path mapping from old structure to new structure

```bash
# Check if docs.old/ exists (migration backup)
if [ ! -d "docs.old" ]; then
    echo "⚠️  No docs.old/ found - run /migrate-docs first"
    exit 1
fi

# Compare docs.old/ vs docs/ structure
echo "📋 Detecting documentation structure changes..."

# Generate path mapping
# AI analyzes both directories and creates mapping table
```

**Mapping detection strategy:**
```python
# Use AI tools to analyze structure
old_structure = scan_directory("docs.old/")
new_structure = scan_directory("docs/")

# AI intelligence creates mapping based on:
# 1. File name similarity
# 2. Directory reorganization patterns
# 3. Content similarity (if needed)
# 4. Known migration patterns (deployment→ops, workflow→dev, etc.)

mapping = {
    "docs/deployment/": "docs/ops/",
    "docs/workflow/": "docs/dev/",
    "docs/dev/ROADMAP.md": "docs/product/roadmap.md",
    "docs/Api-Guide.md": "docs/arch/API.md",
    # ... additional mappings
}
```

**Output example:**
```
Path Mapping Detected:

Old Path                          New Path
──────────────────────────────────────────────────────
docs/deployment/                  docs/ops/
docs/deployment/AWS.md            docs/ops/AWS.md
docs/deployment/MONITORING.md     docs/ops/MONITORING.md
docs/workflow/                    docs/dev/
docs/workflow/GIT_FLOW.md         docs/dev/WORKFLOW.md
docs/dev/ROADMAP.md               docs/product/roadmap.md
docs/Api-Guide.md                 docs/arch/API.md
docs/testing/TEST_PLAN.md         docs/qa/TEST_PLAN.md

Total: 15 path mappings detected
```

### Step 2: Scan Project Files

**Purpose**: Find all files containing documentation references

```bash
echo "🔍 Scanning project files for documentation references..."

# Use Grep tool to search for "docs/" pattern
# Scan multiple file types
```

**File types to scan:**
- Markdown files: `*.md`
- React components: `*.tsx`
- TypeScript files: `*.ts`
- JavaScript files: `*.js`
- JSON configuration: `*.json`
- YAML configuration: `*.yml`, `*.yaml`

**AI orchestration:**
```python
# Use Grep tool for efficient searching
files_with_refs = []

# Search Markdown files
markdown_matches = Grep(pattern="docs/", glob="*.md", output_mode="files_with_matches")
files_with_refs.extend(markdown_matches)

# Search React components
tsx_matches = Grep(pattern="docs/", glob="*.tsx", output_mode="files_with_matches")
files_with_refs.extend(tsx_matches)

# Search TypeScript files
ts_matches = Grep(pattern="docs/", glob="*.ts", output_mode="files_with_matches")
files_with_refs.extend(ts_matches)

# Search JSON files
json_matches = Grep(pattern="docs/", glob="*.json", output_mode="files_with_matches")
files_with_refs.extend(json_matches)

# Deduplicate
files_with_refs = list(set(files_with_refs))
```

**Output:**
```
Files with documentation references:

📄 Markdown (8 files):
  - README.md (12 references)
  - CLAUDE.md (8 references)
  - CONTRIBUTING.md (3 references)
  - docs/dev/SETUP.md (5 references)
  ...

📄 Source Code (3 files):
  - src/utils/docsLoader.ts (2 references)
  - src/components/DocLink.tsx (1 reference)
  ...

📄 Configuration (2 files):
  - package.json (1 reference)
  - .vscode/settings.json (1 reference)

Total: 13 files with 33 documentation references
```

### Step 3: Intelligent Replacement

**Purpose**: Replace references with context awareness (7 scenarios)

**Scenario 1: Markdown Links** ✅ Replace
```markdown
# Before
详见 [部署文档](docs/deployment/AWS.md)

# After
详见 [部署文档](docs/ops/AWS.md)
```

**Scenario 2: Relative Path References** ✅ Replace
```markdown
# Before
文件位于 `docs/dev/ROADMAP.md`

# After
文件位于 `docs/product/roadmap.md`
```

**Scenario 3: Code String Literals** ✅ Replace
```typescript
// Before
const docsPath = "docs/deployment/"

// After
const docsPath = "docs/ops/"
```

**Scenario 4: Example Code (Placeholders)** ❌ Do NOT Replace
```markdown
// Example: docs/your-category/your-file.md
→ Keep unchanged (this is a placeholder)
```

**Scenario 5: Historical Records (Changelog)** ❌ Do NOT Replace
```markdown
## Changelog
- 2024-01-01: Created docs/deployment/AWS.md
→ Keep unchanged (historical record)
```

**Scenario 6: Anchor Links** ✅ Replace + Validate
```markdown
# Before
[分支策略](docs/workflow/GIT_FLOW.md#branching-strategy)

# After
[分支策略](docs/dev/WORKFLOW.md#branching-strategy)

# AI must verify anchor exists in new file
```

**Scenario 7: JSON Configuration** ✅ Replace
```json
{
  "docsPath": "docs/deployment",
  "guides": {
    "workflow": "docs/workflow/GIT_FLOW.md"
  }
}
→
{
  "docsPath": "docs/ops",
  "guides": {
    "workflow": "docs/dev/WORKFLOW.md"
  }
}
```

**AI Context Understanding Instructions:**

```python
# For each file with references:
for file_path in files_with_refs:
    content = Read(file_path)

    # Apply intelligent replacement
    updated_content = content
    replacements = []

    for old_path, new_path in mapping.items():
        # Context-aware detection
        for match in find_all_matches(content, old_path):
            context = get_surrounding_context(content, match.position, lines=2)

            # Scenario detection
            if is_example_code(context):
                # Scenario 4: Skip placeholders
                continue
            elif is_historical_record(context):
                # Scenario 5: Skip changelog/history
                continue
            elif is_markdown_link(context):
                # Scenario 1: Markdown link
                updated_content = replace_markdown_link(updated_content, old_path, new_path)
                replacements.append({
                    "line": match.line_number,
                    "old": old_path,
                    "new": new_path,
                    "type": "markdown_link"
                })
            elif is_anchor_link(context):
                # Scenario 6: Anchor link - validate anchor exists
                if validate_anchor(new_path, match.anchor):
                    updated_content = replace_with_anchor(updated_content, old_path, new_path, match.anchor)
                    replacements.append({...})
                else:
                    warn(f"Anchor not found: {new_path}#{match.anchor}")
            elif is_json_config(file_path):
                # Scenario 7: JSON configuration
                updated_content = replace_json_value(updated_content, old_path, new_path)
                replacements.append({...})
            else:
                # Scenarios 2 & 3: Relative path or code string
                updated_content = replace_simple(updated_content, old_path, new_path)
                replacements.append({...})

    # Write updated content
    if replacements:
        Edit(file_path, old_string=content, new_string=updated_content)
        record_replacements(file_path, replacements)
```

### Step 4: Validate Link Validity

**Purpose**: Ensure all updated links point to existing files

```bash
echo "✅ Validating updated documentation links..."

# Extract all doc links from updated files
# Verify each link points to an existing file
```

**AI orchestration:**
```python
broken_links = []

for file_path in updated_files:
    content = Read(file_path)
    links = extract_doc_links(content)

    for link in links:
        target_file = resolve_link_path(link.path, relative_to=file_path)

        if not file_exists(target_file):
            broken_links.append({
                "source_file": file_path,
                "line": link.line_number,
                "broken_link": link.path,
                "suggestion": find_similar_file(target_file)
            })
```

**Output:**
```
Link Validation Results:

✅ 31/33 links valid
❌ 2 broken links found:

  📄 README.md:67
    Broken: docs/guides/tutorial.md
    Suggestion: Did you mean docs/dev/SETUP.md?

  📄 src/components/DocLink.tsx:23
    Broken: docs/api/endpoints.md
    Suggestion: File was removed in migration
```

### Step 5: Generate Change Report

**Purpose**: Provide detailed summary of all updates

```
📊 Update Doc Refs - Report

Scan Results:
  - Files scanned: 47
  - Files with doc refs: 13
  - Total references found: 33

Replacements Applied:

  📄 README.md (5 references updated)
    Line 15:  docs/deployment/AWS.md → docs/ops/AWS.md
    Line 23:  docs/dev/ROADMAP.md → docs/product/roadmap.md
    Line 45:  docs/workflow/ → docs/dev/WORKFLOW.md
    Line 67:  docs/Api-Guide.md → docs/arch/API.md
    Line 89:  docs/deployment/ → docs/ops/

  📄 CLAUDE.md (8 references updated)
    Line 34:  docs/deployment/ → docs/ops/ (3 occurrences)
    Line 67:  docs/workflow/ → docs/dev/ (5 occurrences)

  📄 src/utils/docsLoader.ts (2 references updated)
    Line 12:  "docs/deployment" → "docs/ops"
    Line 45:  "docs/workflow/GIT_FLOW.md" → "docs/dev/WORKFLOW.md"

  ...

Summary:
  ✅ 13 files updated
  ✅ 31 references fixed
  ❌ 2 broken links (manual review needed)
  ⏭️  6 references skipped (placeholders/history)

Manual Review Recommended:

  📄 CHANGELOG.md (Line 45)
    - Historical reference: "Added docs/deployment/AWS.md"
    - Recommendation: Keep unchanged (historical record)
    - Status: SKIPPED ✅

  📄 README.md (Line 67)
    - Broken link: docs/guides/tutorial.md
    - Recommendation: File removed - update or delete reference
    - Status: NEEDS ATTENTION ⚠️

Next Steps:
  1. Review changes: git diff
  2. Fix broken links manually (2 found)
  3. Test links: npm run check-links (if available)
  4. Commit: git add . && git commit -m "docs: update refs after migration"
```

## Error Handling & Rollback

**Common errors:**

**No docs.old/ directory:**
```
❌ No docs.old/ directory found

This skill requires docs.old/ from /migrate-docs.

Fix: Run /migrate-docs first
```

**No references found:**
```
ℹ️  No documentation references found

All files scanned, but no "docs/" references detected.

Possible reasons:
  1. Project doesn't reference documentation
  2. Documentation is in different location
  3. All references already updated
```

**Rollback mechanism:**
```bash
# If user wants to undo changes
rollback_updates() {
    echo "🔄 Rolling back documentation reference updates..."

    # Restore from git
    git checkout HEAD -- $(cat .update-doc-refs-modified-files.txt)

    echo "✅ Rollback complete"
}
```

## Integration with Other Skills

**Depends on:**
- `/migrate-docs` - Must run first to create docs.old/ and new structure

**Works with:**
- `/check-docs` - Run after to validate documentation quality
- `/init-docs` - Part of the documentation management workflow

**Complete workflow:**
```
1. /migrate-docs ../buffer       # Migrate documentation structure
2. /update-doc-refs              # Update all references (THIS SKILL)
3. /check-docs --verbose         # Validate result
4. git diff                      # Review changes
5. git commit                    # Commit updates
```

## Examples

### Example 1: Basic Update After Migration

```bash
# After running /migrate-docs on buffer project
cd ~/dev/buffer
/update-doc-refs

# Output:
# 📋 Detecting documentation structure changes...
# 🔍 Scanning project files...
# ✅ 13 files updated, 31 references fixed
# ✅ All links valid
```

### Example 2: Dry Run (Preview)

```bash
/update-doc-refs --dry-run

# Output:
# 🔍 DRY RUN - No changes will be applied
#
# Would update:
#   README.md: 5 references
#   CLAUDE.md: 8 references
#   src/utils/docsLoader.ts: 2 references
#
# Run without --dry-run to apply changes
```

### Example 3: Verbose Output

```bash
/update-doc-refs --verbose

# Output:
# 📋 Path mapping:
#   docs/deployment/ → docs/ops/
#   docs/workflow/ → docs/dev/
#   ...
#
# 🔍 Scanning files...
#   ✅ README.md (12 refs)
#   ✅ CLAUDE.md (8 refs)
#   ...
#
# 📝 Updating README.md...
#   Line 15: docs/deployment/AWS.md → docs/ops/AWS.md
#   Line 23: docs/dev/ROADMAP.md → docs/product/roadmap.md
#   ...
```

## Best Practices

1. **Always run after /migrate-docs** - This skill requires docs.old/ backup
2. **Use --dry-run first** - Preview changes before applying
3. **Review git diff** - Check all replacements make sense
4. **Fix broken links** - Address any broken links flagged in report
5. **Commit separately** - Keep ref updates in dedicated commit

## Performance

- **Detection**: <5 seconds
- **Scanning**: 10-30 seconds (depends on project size)
- **Replacement**: 5-20 seconds
- **Validation**: 5-10 seconds
- **Total**: ~30-60 seconds

Fast because:
- AI tools (Grep) are optimized for search
- Context-aware replacement is targeted
- Validation runs in parallel

## Related Skills

- **/migrate-docs** - Documentation structure migration (run before this)
- **/check-docs** - Documentation quality validation (run after this)
- **/init-docs** - Initialize documentation structure

## Related Documentation

- **[DOCUMENTATION_MIGRATION_GUIDE.md](../../docs/DOCUMENTATION_MIGRATION_GUIDE.md)** - Complete migration guide
- **[INTEGRATION.md](INTEGRATION.md)** - Integration with migrate-docs workflow

---

**Version:** 1.0.0
**Last Updated:** 2026-03-16
**Changelog:**
- v1.0.0 (2026-03-16): Initial release - update documentation cross-references

**Pattern:** Tool-Reference (pure AI instruction implementation)
**Compliance:** ADR-001 ✅
