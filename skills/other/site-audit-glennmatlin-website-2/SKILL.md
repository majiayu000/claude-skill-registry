---
name: site-audit
description: Audit the website for broken links, SEO issues, accessibility problems, and content quality. Use before deployment or for periodic maintenance.
allowed-tools: Bash(grep:*), Bash(find:*), Grep, Glob, Read
---

# Website Audit

## Instructions

Perform a comprehensive audit of the website covering:

### 1. Broken Links Check

Search for internal links and verify targets exist:
```bash
# Find all internal links in .qmd files
grep -rh '\[.*\](' --include="*.qmd" | grep -oP '\]\(\K[^)]+' | grep -v '^http' | sort -u
```

Check that referenced files exist:
- Images in content
- PDF downloads
- Internal page links

### 2. Frontmatter Validation

Verify all content files have required frontmatter:

**Blog posts** (`posts/*/index.qmd`):
- [ ] title
- [ ] author
- [ ] date
- [ ] categories
- [ ] description

**Publications** (`publications/*/index.qmd`):
- [ ] title
- [ ] author
- [ ] date
- [ ] venue or categories

**Projects** (`projects/*/index.qmd`):
- [ ] title
- [ ] description
- [ ] date
- [ ] categories

### 3. SEO Checks

- [ ] All pages have `description` in frontmatter
- [ ] Descriptions are under 160 characters
- [ ] Images have alt text
- [ ] `_quarto.yml` has site-url configured
- [ ] Open Graph metadata is present

### 4. Accessibility Review

- [ ] Images have descriptive alt text
- [ ] Heading hierarchy is correct (no skipped levels)
- [ ] Links have descriptive text (not "click here")
- [ ] Color contrast is sufficient
- [ ] Forms have labels (if any)

### 5. Content Quality

- [ ] No draft posts published (`draft: false` or missing)
- [ ] No placeholder/Lorem ipsum text
- [ ] Dates are not in the future
- [ ] External links are valid (spot check)

### 6. Technical Checks

- [ ] `quarto render` completes without errors
- [ ] No files in `_site/` committed to git
- [ ] CNAME file exists for custom domain
- [ ] `.gitignore` excludes build artifacts

## Audit Commands

```bash
# Check for missing descriptions
grep -rL "description:" posts/*/index.qmd

# Find images without alt text
grep -rn '!\[' --include="*.qmd" | grep '!\[\]'

# Check for draft posts
grep -rn "draft: true" --include="*.qmd"

# List all external links
grep -rhoP 'https?://[^\s)>"]+' --include="*.qmd" | sort -u

# Find large images
find . -type f \( -name "*.png" -o -name "*.jpg" \) -size +500k
```

## Report Format

After audit, provide a summary:

```
## Audit Summary

### Critical Issues
- Issue 1...
- Issue 2...

### Warnings
- Warning 1...
- Warning 2...

### Recommendations
- Suggestion 1...
- Suggestion 2...

### Stats
- Total pages: X
- Blog posts: X
- Publications: X
- Projects: X
- Images: X
```
