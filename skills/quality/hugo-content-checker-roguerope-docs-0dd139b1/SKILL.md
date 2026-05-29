---
name: hugo-content-checker
description: This skill should be used when checking Hugo content for consistency issues, validating internal references, detecting duplicate content, verifying frontmatter completeness, and ensuring proper naming conventions. Use this skill to audit content quality, fix broken links, and maintain consistency across a Hugo site.
---

# Hugo Content Checker

This skill provides tools and guidance for analyzing Hugo content for consistency issues, broken references, orphaned pages, and quality problems.

## Purpose

Maintaining a large Hugo documentation site requires consistent structure, proper linking, and high-quality metadata. This skill automates the detection of common issues that can degrade site quality and user experience:

- **Broken internal links** that lead to missing pages
- **Orphaned content** that exists but is never referenced
- **Inconsistent frontmatter** missing required metadata fields
- **Naming convention violations** that reduce maintainability
- **Duplicate content** that should be consolidated or cross-referenced

## When to Use This Skill

Use this skill when:
1. Auditing a Hugo site for consistency and quality issues
2. Finding and fixing broken internal links and references
3. Identifying content that may be orphaned or unused
4. Validating that frontmatter is complete across all content
5. Enforcing naming conventions across content sections
6. Detecting potentially duplicate or very similar content
7. Preparing for content refactoring or reorganization
8. Setting up quality gates before deployment

## How to Use This Skill

### Step 1: Run the Content Analysis Script

Execute the analysis script to scan the Hugo content folder:

```bash
python3 .claude/skills/hugo-content-checker/scripts/analyze_content.py content/
```

The script accepts one optional argument:
- **content-directory**: Path to the Hugo content folder (defaults to `content/`)

### Step 2: Review the Analysis Results

The script outputs both human-readable and JSON results showing:

#### Broken Links
Files that reference non-existent content pages. These are critical errors that break navigation.

Example output:
```
[ERROR] content/concept/something.md
        Broken link: 'concept/nonexistent'
```

**How to fix**: Verify the referenced page exists or update the link to the correct path.

#### Frontmatter Issues
Files missing required metadata fields or with empty values. These affect site functionality and search.

Example output:
```
[WARNING] content/wellbeing/page.md
          Missing or empty frontmatter field: description
```

**How to fix**: Add the missing field to the frontmatter with appropriate content.

#### Orphaned Content
Content files that exist but are never referenced from other pages. These may be:
- Legitimately standalone pages (homepage sections)
- Pages missing from navigation
- Content that should be deleted

Example output:
```
[INFO] content/practical/old-page.md
       Content file not referenced from any other file
```

**How to fix**: Either add references from other pages or verify the page should exist as standalone content.

#### Naming Issues
Filenames that violate conventions (uppercase, spaces, special characters).

Example output:
```
[WARNING] content/concept/My-Page.md
          Filename contains uppercase letters (convention: lowercase)
```

**How to fix**: Rename the file to lowercase with hyphens (e.g., `my-page.md`).

#### Duplicate Content
Files with very similar content (>80% similarity) that may need consolidation.

Example output:
```
[WARNING] content/concept/page1.md
          Similar to: content/concept/page2.md (85.3%)
```

**How to fix**: Review the files and either consolidate into one page with cross-references, or clarify the differences.

### Step 3: Fix Issues Based on Severity

**Priority order**:
1. **ERROR (Critical)**: Broken links - fix immediately as they break functionality
2. **WARNING (High)**: Missing frontmatter, naming issues, duplicates - fix before deployment
3. **INFO (Low)**: Orphaned content - review and decide if intentional

### Step 4: Validate Fixes

After making changes, run the script again to verify issues are resolved:

```bash
python3 .claude/skills/hugo-content-checker/scripts/analyze_content.py content/
```

## Implementation Details

### Analysis Script (scripts/analyze_content.py)

The Python script performs the following checks:

**Broken Links Check**
- Extracts all internal links from markdown content
- Matches against valid content paths in the content directory
- Ignores external links (http/https) and anchors (#)
- Supports Hugo ref/relref shortcodes and standard markdown links

**Frontmatter Consistency**
- Parses YAML frontmatter from each file
- Identifies required fields that are missing or empty
- Flags inconsistencies in field formats
- Respects special cases (e.g., index files may have different requirements)

**Orphaned Content Detection**
- Maps all content files to their URL paths
- Collects all referenced links from across the site
- Identifies content that is never referenced
- Excludes index files which may be accessed through navigation menus

**Naming Convention Validation**
- Checks for uppercase letters in filenames
- Identifies spaces or other problematic characters
- Flags violations of lowercase-with-hyphens convention

**Duplicate Content Detection**
- Extracts word sets from each page body
- Calculates Jaccard similarity between all pairs
- Flags pages with >80% similarity as potential duplicates
- Skips very short content (<50 words) to avoid false positives

### Hugo Best Practices Reference

See `references/hugo_best_practices.md` for:
- Hugo content organization structure
- Frontmatter field specifications and examples
- Naming conventions and URL structure
- Internal linking patterns
- Common consistency problems and solutions
- Recommended workflow for content auditing

## Integration with Your Workflow

### Pre-commit Hook
Add to your git pre-commit hook to catch issues before committing:

```bash
#!/bin/bash
python3 .claude/skills/hugo-content-checker/scripts/analyze_content.py content/ > /tmp/content-check.json
if grep -q '"error"' /tmp/content-check.json; then
  echo "Content consistency errors found. Fix before committing."
  exit 1
fi
```

### CI/CD Pipeline
Integrate into CI/CD to automatically check content on every push:

```bash
python3 .claude/skills/hugo-content-checker/scripts/analyze_content.py content/
```

### Regular Audits
Run periodically to maintain content quality:
- After major content additions
- Before releases to production
- When preparing for content restructuring
- When performance issues arise

## Limitations and Considerations

- The script performs basic similarity detection; high similarity doesn't always mean duplication
- Orphaned content detection is approximate; some pages may be accessed through menus rather than cross-links
- The script doesn't check for content quality, tone, or accuracy—only structural consistency
- External link checking is not included; use additional tools for that
- Performance scales linearly with content size; large sites may take a few seconds to analyze

## Next Steps After Analysis

1. **Create an action plan** based on issue severity and frequency
2. **Prioritize fixes** starting with broken links (highest impact)
3. **Establish guidelines** for future content to prevent similar issues
4. **Document decisions** about orphaned content (keep, link, or delete)
5. **Set up automation** to run checks regularly in your workflow
