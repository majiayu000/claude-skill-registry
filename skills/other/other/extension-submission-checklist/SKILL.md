---
name: extension-submission-checklist
description: Review and track progress against official 3D Slicer Extension Index requirements
allowed-tools:
  - WebFetch
  - Bash
  - Read
context: manual
---

# Extension Submission Checklist Skill

Review and track progress against the official 3D Slicer Extension Index submission requirements.

## When to Use

Use this skill when:
- Preparing to submit an extension to the Slicer Extension Index
- Reviewing submission readiness
- Creating a pull request for extension submission

## CRITICAL: Verify Latest Requirements First

**Before using this checklist, ALWAYS fetch the latest official requirements:**

```bash
# Fetch the current PR template (authoritative checklist)
curl -s "https://raw.githubusercontent.com/Slicer/ExtensionsIndex/main/.github/PULL_REQUEST_TEMPLATE.md"

# Fetch the current JSON schema
curl -s "https://raw.githubusercontent.com/Slicer/Slicer/main/Schemas/slicer-extension-catalog-entry-schema-v1.0.1.json"
```

Compare fetched content against this skill. If discrepancies exist, **the fetched content is authoritative**.

## Official Sources (Verified 2025-01-26)

- PR Template: https://github.com/Slicer/ExtensionsIndex/blob/main/.github/PULL_REQUEST_TEMPLATE.md
- JSON Schema: https://github.com/Slicer/Slicer/blob/main/Schemas/slicer-extension-catalog-entry-schema-v1.0.1.json
- Documentation: https://slicer.readthedocs.io/en/latest/developer_guide/extensions.html

## Extension Tiers

Extensions are classified by quality/maturity level:

| Tier | Description |
|------|-------------|
| 1 | Experimental extensions (minimum for listing) |
| 3 | Community-supported extensions |
| 5 | Critical extensions, supported by Slicer core developers |

Tiers 2 and 4 are reserved for future use.

---

## Tier 1 Requirements (Minimum for Listing)

### Naming and Repository

- [ ] **Extension name is reasonable** - Not too general, not too narrow, suggests what it's for
- [ ] **Extension name does NOT start with "Slicer"** - Unless it bridges Slicer to external tool/library
- [ ] **Repository name follows convention** - `Slicer` + ExtensionName (e.g., `SlicerMouseMaster`)
- [ ] **Repository has `3d-slicer-extension` GitHub topic** - For discoverability at https://github.com/topics/3d-slicer-extension

### Description and Documentation

- [ ] **Extension description summarizes functionality** - 1-2 sentences understandable by non-experts
- [ ] **Any related patents disclosed** - Must be mentioned in extension description if applicable

### Licensing

- [ ] **LICENSE.txt present in repository root**
- [ ] **License name mentioned on extension homepage**
- [ ] **Permissive license used** - MIT or Apache recommended
- [ ] **If restrictive license used** - Reason explained and license name in description

### URLs and References

- [ ] **scm_url correct** - Repository checkout URL (e.g., `https://github.com/user/repo.git`)
- [ ] **scm_revision appropriate** - Branch name (main, master) preferred over specific git hash
- [ ] **Icon URL correct** - Raw data URL, not webpage (e.g., `https://raw.githubusercontent.com/...`)
- [ ] **Screenshot URLs correct** - At least one screenshot, raw data URLs

### Metadata Consistency

- [ ] **JSON file consistent with CMakeLists.txt** - Dependencies, category, etc. must match

### Homepage Requirements

Homepage URL must point to valid webpage containing:

- [ ] Extension name
- [ ] Short description (1-2 sentences)
- [ ] At least one informative image/screenshot
- [ ] Description of each contained module (at least one sentence each)
- [ ] Publication link (if available) - Link to paper or PubMed reference

### GitHub Repository Settings

Hide unused features to reduce noise:

- [ ] **Settings > Features** - Uncheck Wiki, Projects, Discussions (if not used)
- [ ] **About section** - Uncheck Releases, Packages (if not used)

### Safety Requirements

- [ ] **No unreliable binaries** - Does not include/download binaries from untrusted sources
- [ ] **No data transmission without consent** - Explicit opt-in required for any data sending

---

## Tier 3 Requirements (Community-Supported)

All Tier 1 requirements PLUS:

### Documentation and Testing

- [ ] **Documentation provided for most modules**
- [ ] **Tutorial with step-by-step instructions** - At least for most typical use case
- [ ] **Tutorial includes screenshots**
- [ ] **Sample data registered with Sample Data module** - For easy user access

### Code Quality

- [ ] **Follows Slicer programming conventions** - GUI/logic separation, etc.
- [ ] **Follows Slicer UI conventions** - Minimal popups, no unnecessary custom styling

### Build and Platform Support

- [ ] **Builds successfully on Windows**
- [ ] **Builds successfully on macOS**
- [ ] **Builds successfully on Linux**

### Maintainer Responsiveness

- [ ] **Responds to issues on extension repository**
- [ ] **Responds to pull requests on extension repository**
- [ ] **Responds to @mentions on Slicer Forum** (discourse.slicer.org)

### Licensing (Additional)

- [ ] **Permissive license for main functions** - Apache or MIT recommended
- [ ] **Non-permissive optional components require user approval** - Pop-up explaining terms

---

## Tier 5 Requirements (Core Extensions)

All Tier 1 and Tier 3 requirements PLUS:

- [ ] **Slicer core developer has commit access** - For Slicer-related fixes
- [ ] **Automated tests for all critical features**
- [ ] **Maintainers respond to Forum questions** - About the extension

---

## Submission Process Steps

1. **Verify latest requirements** (see CRITICAL section above)
2. **Complete all Tier 1 requirements** (minimum)
3. **Run `/validate-extension-submission` skill** to check readiness
4. **Run `/prepare-extension-metadata` skill** to generate JSON file
5. **Fork https://github.com/Slicer/ExtensionsIndex**
6. **Add your JSON file** to the forked repository's main branch
7. **Create pull request** using the template
8. **Check all applicable boxes** in the PR template
9. **Respond to reviewer feedback**

## Files to Prepare

| File | Location | Purpose |
|------|----------|---------|
| `ExtensionName.json` | ExtensionsIndex repo | Catalog entry for Extension Index |
| `CMakeLists.txt` | Extension repo root | Extension metadata for Slicer build system |
| `LICENSE.txt` | Extension repo root | License file |
| `README.md` | Extension repo root | Homepage/documentation |
| Icon PNG | Extension repo | 128x128 recommended, raw URL needed |
| Screenshots | Extension repo | At least one, raw URLs needed |

## Example JSON File (Catalog Entry)

```json
{
  "$schema": "https://raw.githubusercontent.com/Slicer/Slicer/main/Schemas/slicer-extension-catalog-entry-schema-v1.0.1.json#",
  "build_dependencies": [],
  "build_subdirectory": ".",
  "category": "Utilities",
  "scm_revision": "main",
  "scm_url": "https://github.com/user/SlicerExtensionName.git",
  "tier": 1
}
```

## Validation Commands

```bash
# Validate JSON syntax
python -c "import json; json.load(open('ExtensionName.json'))"

# Check CMakeLists.txt metadata
grep -E "^set\(EXTENSION_" CMakeLists.txt

# Verify icon URL is accessible
curl -sI "https://raw.githubusercontent.com/..." | head -1

# Verify screenshot URLs are accessible
curl -sI "https://raw.githubusercontent.com/..." | head -1
```
