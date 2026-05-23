---
name: spitakolus-documentation-standards
description: Follow Spitakolus documentation rules. Update dates, avoid duplication, clean outdated files, and maintain consistent structure across all repos.
dependencies: []
---

# Spitakolus Documentation Standards

## Core Rules

### 1. Every Repo Must Have
- ✅ `README.md` with clear warning: "This is [PROJECT] repo"
- ✅ `DOCUMENTATION_MAP.md` with complete overview
- ✅ Links to spitakolus for shared documentation
- ✅ Links to other project repos

### 2. Where Does Documentation Go?

**In spitakolus (shared):**
- Applies to multiple projects
- Company-wide standards
- Shared infrastructure (GTM, BigQuery)

**In project repo (specific):**
- Project-specific setup
- Project-specific deployment
- Project-specific workflows

### 3. NEVER Duplicate
- ❌ Same information in multiple places
- ❌ Flocken docs in nastahem (or vice versa)
- ✅ Link instead of copying
- ✅ One source of truth

---

## When Creating Documentation

### Checklist
- [ ] Determined if shared or project-specific
- [ ] Chose correct repo and folder
- [ ] Followed naming conventions
- [ ] Added to relevant README.md
- [ ] Updated DOCUMENTATION_MAP.md if needed
- [ ] Added date and author
- [ ] Verified links work

### Naming Conventions

**Files:**
- Descriptive names (not "doc1.md")
- UPPERCASE for important files (README.md, DOCUMENTATION_MAP.md)
- Consistent across repos

**Folders:**
- Descriptive: `tracking/`, `meta-ads/`, `development/`
- Consistent structure across repos

---

## When Updating Documentation

1. **Update the document**
   - Keep structure and format
   - **ALWAYS update "Last updated" date**
   - Add changelog for major changes

2. **Update links**
   - Update DOCUMENTATION_MAP.md if needed
   - Check all links work

3. **Verify**
   - Read through for clarity
   - Test links

---

## Cleanup Rules

### DELETE Outdated Files

**Remove files that:**
- ❌ Are older than 3 months without updates
- ❌ Reference code/projects that no longer exist
- ❌ Have multiple versions (keep only latest)
- ❌ Are completed "cleanup plans" or "migration plans"
- ❌ Are temporary work documents

**Don't archive everything - DELETE what's not needed!**

### Monthly Maintenance

1. Review files older than 2 months
2. Delete outdated files
3. Update broken links
4. Verify structure matches DOCUMENTATION_MAP.md

---

## For AI Assistants

### Before Making Changes
1. Check which repo you're in
2. Read DOCUMENTATION_MAP.md
3. Understand existing structure

### When Creating New Docs
1. Determine shared vs project-specific
2. Follow existing patterns
3. Add to index files
4. Update dates

### Golden Rule
**Don't create documentation that contradicts existing docs without explicit agreement on a plan first.**

---

## Templates

Use templates from:
- `spitakolus/development/TEMPLATES/README_TEMPLATE.md`
- `spitakolus/development/TEMPLATES/DOCUMENTATION_MAP_TEMPLATE.md`
