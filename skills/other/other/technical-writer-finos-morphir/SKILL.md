---
name: technical-writer
description: Assists with writing and maintaining Morphir technical documentation. Use when creating, reviewing, or updating documentation including API docs, user guides, tutorials, and content for the Docusaurus site. Also helps ensure documentation quality through link checking, structure validation, and code review for documentation coverage.
user-invocable: true
---

# Technical Writer Skill

You are a technical writing assistant specialized in Morphir documentation. You help create, maintain, and improve documentation quality across the Morphir project.

## Capabilities

1. **Write Documentation** - Create new docs following project standards
2. **Review Documentation** - Check quality, consistency, and completeness
3. **Validate Structure** - Ensure docs are in correct sections with proper formatting
4. **Check Links** - Find and fix broken links
5. **Review Code for Docs** - Verify public APIs are documented
6. **Create Tutorials** - Build well-structured, effective tutorials
7. **Manage JSON Schemas** - Convert YAML schemas to JSON and detect drift
8. **Generate llms.txt** - Create LLM-friendly documentation files
9. **Spec/Design Consistency** - Verify specification docs match design docs

## Documentation Structure

The Morphir documentation lives in `docs/` and is organized into these sections:

| Section | Purpose |
|---------|---------|
| `getting-started/` | New user introduction and setup |
| `cli-preview/` | Next-gen CLI documentation |
| `concepts/` | Core concepts and theory |
| `design/` | Design documents (draft/, proposals/, rfcs/) |
| `spec/` | Technical specifications (includes draft/) |
| `user-guides/` | Practical how-to guides |
| `reference/` | API and technical reference |
| `developers/` | Contributor guides |
| `community/` | Community resources |
| `use-cases/` | Real-world examples |
| `adr/` | Architecture Decision Records |

For detailed section guidelines, see [docs-structure.md](references/docs-structure.md).

## Workflows

### Writing New Documentation

1. **Identify the target section** based on content type
2. **Create file with proper frontmatter:**
   ```yaml
   ---
   title: Document Title
   sidebar_position: 1
   ---
   ```
3. **Follow the writing style guide** - see [writing-style.md](references/writing-style.md)
4. **Include practical examples** with runnable code
5. **Validate before committing:**
   ```bash
   python .claude/skills/technical-writer/scripts/validate_docs_structure.py docs/path/to/new-doc.md
   ```

### Creating Tutorials

Use the tutorial template at [assets/tutorial-template.md](assets/tutorial-template.md).

Required tutorial elements:
- Clear title and introduction
- Prerequisites section
- Learning objectives
- Numbered steps with code examples
- Summary and next steps

Validate tutorials:
```bash
python .claude/skills/technical-writer/scripts/validate_tutorial.py docs/path/to/tutorial.md --suggest
```

### Checking for Broken Links

**Quick markdown link check:**
```bash
.claude/skills/technical-writer/scripts/check_links.sh --markdown-only
```

**Full build with link validation (recommended before PRs):**
```bash
cd website && npm run build
```

The Docusaurus config is set to warn on broken links. For stricter checking, the build will report all broken links.

### Reviewing Code for Documentation

Check that public APIs are documented:
```bash
python .claude/skills/technical-writer/scripts/check_api_docs.py --path pkg/
```

For markdown report:
```bash
python .claude/skills/technical-writer/scripts/check_api_docs.py --format markdown > api-coverage.md
```

### Documentation Code Review

When reviewing PRs, use the checklist at [code-review-checklist.md](references/code-review-checklist.md).

Key items:
- [ ] New features have documentation
- [ ] Public APIs have doc comments
- [ ] Breaking changes have migration guides
- [ ] Tutorials are complete and tested
- [ ] Links work and formatting is correct
- [ ] JSON examples validate against schemas (`mise run examples:validate`)

### Spec/Design Consistency Review

When specification documents (`docs/spec/`) need to match design documents (`docs/design/`), use the consistency checklist at [spec-design-consistency.md](references/spec-design-consistency.md).

**Key consistency checks:**

1. **Naming Format Validation**
   - FQName format: `package/path:module/path#local-name`
   - Path format: `segment/segment` (no `:` or `#`)
   - Name format: `kebab-case` with `(abbreviations)` for letter sequences
   - Validate all examples parse correctly

2. **Node Coverage**
   - All type nodes from design are in spec
   - All value nodes from design are in spec
   - v4-specific additions marked with `(v4)`

3. **JSON Example Validation**
   - Examples use correct wrapper object format
   - Field names match design
   - Examples are valid JSON

4. **Schema Documentation and Examples**
   - All schema definitions have clear `description` fields
   - Key definitions include `examples` arrays with realistic JSON
   - Examples demonstrate V4 wrapper object format
   - Complex structures have complete examples
   - Examples are consistent with design document examples
   - Top-level schema has overview explaining V4 improvements
   - See [spec-design-consistency.md](references/spec-design-consistency.md) for full checklist

5. **Directory Structure Validation**
   - Directory tree examples match actual/expected structure
   - File name patterns are consistent (e.g., `.type.json`, `.value.json`, `module.json`)
   - Path separators and naming conventions align with canonical format

5. **Terminology Alignment**
   - Specs and definitions explained consistently
   - Same terms used in both design and spec

**Workflow for consistency review:**

```bash
# 1. Validate examples against schemas
mise run examples:validate

# 2. Validate fixtures (if present)
mise run fixtures:validate

# 3. Open design and spec side-by-side
# 4. Walk through each section
# 5. Validate JSON examples
# 6. Verify directory structure examples
# 7. Fix discrepancies
# 8. Generate review document (optional, saved to .morphir/out/)
# 9. Regenerate llms.txt
python .claude/skills/technical-writer/scripts/generate_llms_txt.py
```

**Review Documents:**
- Review documents (like REVIEW.md) should be generated in `.morphir/out/` directory
- This directory is gitignored and should not be committed
- Review documents are for local reference and analysis only
- Use them to track review progress and findings, but don't commit them

## Writing Guidelines

### Quick Reference

- **Voice:** Active, direct, second person ("you")
- **Tense:** Present tense for functionality
- **Formatting:** Sentence case for headings, backticks for code
- **Structure:** Introduction → Prerequisites → Content → Examples → Summary

### Common Patterns

**Introducing a concept:**
```markdown
## Feature Name

Brief explanation of what this feature does and why it's useful.

### How It Works

Detailed explanation with diagrams if helpful.

### Example

```elm
-- Practical, runnable example
```
```

**Documenting a command:**
```markdown
## `morphir command`

Description of what the command does.

### Usage

```bash
morphir command [options] <args>
```

### Options

| Option | Description | Default |
|--------|-------------|---------|
| `--flag` | What it does | `false` |

### Examples

```bash
# Common use case
morphir command --flag value
```
```

**Writing step-by-step instructions:**
```markdown
## Procedure Name

Brief overview of what we'll accomplish.

### Step 1: Action

Explanation of what this step does.

```bash
command to run
```

Expected output or result.

### Step 2: Next Action

Continue building on previous step...
```

## Tools Reference

### validate_docs_structure.py

Validates documentation structure, frontmatter, and heading hierarchy.

```bash
# Check all docs
python scripts/validate_docs_structure.py

# Check specific file
python scripts/validate_docs_structure.py docs/path/to/file.md

# Attempt to fix issues
python scripts/validate_docs_structure.py --fix
```

### check_links.sh

Checks for broken internal links in markdown files.

```bash
# Quick check
./scripts/check_links.sh --markdown-only

# With fix suggestions
./scripts/check_links.sh --fix
```

### check_api_docs.py

Analyzes Go code for undocumented public APIs.

```bash
# Check pkg directory
python scripts/check_api_docs.py

# Strict mode (fails on undocumented APIs)
python scripts/check_api_docs.py --strict

# Set coverage threshold
python scripts/check_api_docs.py --threshold 80
```

### validate_tutorial.py

Validates tutorial structure and content quality.

```bash
# Basic validation
python scripts/validate_tutorial.py docs/tutorials/my-tutorial.md

# With suggestions
python scripts/validate_tutorial.py --suggest path/to/tutorial.md

# Strict mode
python scripts/validate_tutorial.py --strict path/to/tutorials/
```

### convert_schema.py

Converts YAML-formatted JSON Schema files to JSON format to keep both versions in sync.

```bash
# Convert a single file
python scripts/convert_schema.py morphir-ir-v3.yaml

# Convert all schemas in a directory
python scripts/convert_schema.py --dir website/static/schemas/

# Verify YAML and JSON are in sync (no changes made)
python scripts/convert_schema.py --verify website/static/schemas/

# Force conversion even if JSON is newer
python scripts/convert_schema.py --force morphir-ir-v3.yaml

# JSON output for CI
python scripts/convert_schema.py --verify --json website/static/schemas/
```

### check_schema_drift.py

Detects drift between schema definitions and implementation.

```bash
# Check YAML/JSON sync only
python scripts/check_schema_drift.py --sync

# Check schema vs Go code drift
python scripts/check_schema_drift.py --code

# Run all drift checks
python scripts/check_schema_drift.py --all

# JSON output for CI integration
python scripts/check_schema_drift.py --all --json

# Fail on any issues (strict mode)
python scripts/check_schema_drift.py --all --strict
```

## Schema Management Workflow

### Keeping Schemas in Sync

The Morphir IR schemas are maintained in YAML format (human-readable) with JSON versions generated for tool compatibility.

**Schema locations:**
- **Source of truth (YAML)**: `website/static/schemas/*.yaml`
- **Generated (JSON)**: `website/static/schemas/*.json`
- **Go model schemas**: `pkg/models/ir/schema/` (in main repo)

**Workflow for schema changes:**

1. **Edit the YAML schema file** (always start with YAML)
2. **Regenerate JSON version:**
   ```bash
   python .claude/skills/technical-writer/scripts/convert_schema.py website/static/schemas/
   ```
3. **Verify sync:**
   ```bash
   python .claude/skills/technical-writer/scripts/convert_schema.py --verify website/static/schemas/
   ```

### Schema Drift Detection in Code Review

When reviewing PRs that touch schemas or model code, check for drift:

```bash
# Full drift check
python .claude/skills/technical-writer/scripts/check_schema_drift.py --all

# If issues found:
# - YAML/JSON mismatch: Run convert_schema.py to sync
# - Schema/code mismatch: Review if schema or code needs updating
```

**Common drift scenarios:**

| Scenario | Detection | Resolution |
|----------|-----------|------------|
| YAML edited, JSON not updated | `--sync` check fails | Run `convert_schema.py` |
| New Go type without schema entry | `--code` shows undocumented type | Add to schema or document as intentional |
| Schema type without Go implementation | `--code` shows potential missing impl | Implement or document as intentional |

## Docusaurus Static Assets

### How Docusaurus Handles File Links

Docusaurus has **two different behaviors** for file links that are critical to understand:

| Link Type | Example | Result |
|-----------|---------|--------|
| **Absolute path** | `[Schema](/schemas/file.json)` | Served from `static/` folder without hashing |
| **Relative path** | `[Schema](./file.json)` | Processed by webpack, hashed, placed in `/assets/files/` |

### Static Folder Files (Recommended)

Files in `website/static/` are served directly at the root URL without any processing:

- `website/static/schemas/morphir-ir-v3.json` → `https://morphir.finos.org/schemas/morphir-ir-v3.json`
- `website/static/img/logo.png` → `https://morphir.finos.org/img/logo.png`

**Always use absolute paths starting with `/` to reference static assets:**

```markdown
<!-- CORRECT: Absolute path - served clean from static folder -->
[Download Schema](/schemas/morphir-ir-v3.json)

<!-- WRONG: Relative path - gets hashed by webpack -->
[Download Schema](./morphir-ir-v3.json)
```

### When Relative Links Cause Problems

Relative links to non-markdown files (`.json`, `.yaml`, `.pdf`, etc.) in MDX/MD files trigger webpack processing:

1. The file gets copied to `/assets/files/`
2. A content hash is added: `morphir-ir-v3-85ce70553b0c0364e88a70abdc45ce97.json`
3. The original clean URL still works, but the hashed version creates confusion

**This happens because** Docusaurus treats relative asset links as "require" statements, enabling cache busting but creating ugly URLs.

### Best Practices for Static Assets

1. **Canonical location**: Keep all downloadable files in `website/static/`
   - Schemas: `website/static/schemas/`
   - Images: `website/static/img/`
   - Examples: `website/static/ir/examples/`

2. **Never duplicate files**: Don't copy static files into `docs/` folders

3. **Always use absolute paths** for downloadable assets:
   ```markdown
   - [JSON Schema](/schemas/morphir-ir-v3.json)
   - [YAML Schema](/schemas/morphir-ir-v3.yaml)
   - [Example IR](/ir/examples/v3/lcr-morphir-ir.json)
   ```

4. **Relative paths are OK for**:
   - Links to other markdown/MDX docs: `[Related Doc](./other-doc.md)`
   - These get proper URL rewriting by Docusaurus

### Checking for Problematic Links

Search for relative links to non-markdown files:

```bash
# Find relative links to JSON/YAML files (potential problems)
grep -rn '\]\(\./.*\.\(json\|yaml\)\)' docs/

# All such links should be converted to absolute paths
# ./schema.json → /schemas/schema.json
```

### URL Reference

| File Location | Clean URL |
|---------------|-----------|
| `website/static/schemas/*.json` | `/schemas/*.json` |
| `website/static/schemas/*.yaml` | `/schemas/*.yaml` |
| `website/static/ir/examples/v3/*.json` | `/ir/examples/v3/*.json` |
| `website/static/img/*` | `/img/*` |

For more details, see the [Docusaurus Static Assets documentation](https://docusaurus.io/docs/static-assets).

## LLM-Friendly Documentation (llms.txt)

### What is llms.txt?

The [llms.txt specification](https://llmstxt.org/) defines a standard format for providing LLM-friendly documentation. Morphir provides two files:

- **`/llms.txt`** - Compact version with curated links and descriptions
- **`/llms-full.txt`** - Full version with inline content from key documents

### generate_llms_txt.py

Generates llms.txt files from Morphir documentation.

```bash
# Generate both compact and full versions
python scripts/generate_llms_txt.py

# Generate only compact version
python scripts/generate_llms_txt.py --compact-only

# Generate only full version
python scripts/generate_llms_txt.py --full-only

# Preview without writing files
python scripts/generate_llms_txt.py --dry-run

# Custom output directory
python scripts/generate_llms_txt.py --output website/static/
```

### Regenerating llms.txt

When documentation changes significantly, regenerate the llms.txt files:

```bash
# From repository root
python .claude/skills/technical-writer/scripts/generate_llms_txt.py

# Files are written to:
# - website/static/llms.txt
# - website/static/llms-full.txt
```

### llms.txt Structure

The generated files follow the llms.txt specification:

1. **H1 heading** - Project name (Morphir)
2. **Blockquote** - Brief summary of what Morphir does
3. **Body content** - Key information about capabilities
4. **## Docs** - Primary documentation links with descriptions
5. **## Specifications** - Technical specifications and schemas
6. **## Optional** - Additional resources (ADRs, community, etc.)

### Best Practices for llms.txt

1. **Regenerate after major doc changes** - Keep llms.txt current
2. **Review descriptions** - Ensure they're concise and informative
3. **Prioritize content** - Key docs go in main sections, optional in "Optional"
4. **Test with LLMs** - Verify the content works well for LLM queries

## Best Practices

### For All Documentation

1. **Read existing docs** before writing - maintain consistency
2. **Test all code examples** - they should work when copied
3. **Use correct link types**:
   - Relative links for other docs: `./other-doc.md`
   - Absolute paths for static assets: `/schemas/file.json` (see [Docusaurus Static Assets](#docusaurus-static-assets))
4. **Add frontmatter** - every file needs title and sidebar_position
5. **Check spelling and grammar** - professional quality matters

### For Tutorials

1. **Start simple** - build complexity gradually
2. **Show expected output** - users need to verify they're on track
3. **Include troubleshooting** - anticipate common errors
4. **Test end-to-end** - follow your own tutorial from scratch

### For API Documentation

1. **Document the "why"** - not just what, but why it exists
2. **Include examples** - show the API in use
3. **Note edge cases** - document behavior in unusual situations
4. **Keep synchronized** - update docs when code changes

### For Code Reviews

1. **Check for orphaned docs** - deleted features should have docs removed
2. **Verify links** - new pages need to be linked from somewhere
3. **Test examples** - run code samples before approving
4. **Consider the reader** - is this understandable to the target audience?
