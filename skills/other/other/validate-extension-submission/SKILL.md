---
name: validate-extension-submission
description: Validate that an extension meets all requirements for Extension Index submission
allowed-tools:
  - Bash
  - Read
context: auto
---

# Validate Extension Submission Skill

Validate that an extension meets all requirements for Slicer Extension Index submission.

## When to Use

- Before submitting to Extension Index
- After making changes to verify nothing is broken
- To check what's missing for submission

## How to Validate

Run the validation script:

```bash
./scripts/validate_extension.sh
```

This script checks:
- Repository structure (CMakeLists.txt, LICENSE, README.md)
- CMakeLists.txt metadata (HOMEPAGE, CONTRIBUTORS, DESCRIPTION, ICONURL, SCREENSHOTURLS)
- URL accessibility (homepage, icon, screenshots)
- Extension Index JSON file (if present)
- GitHub repository settings (3d-slicer-extension topic)
- License type

## Fixing Common Issues

### Missing 3d-slicer-extension topic

```bash
gh repo edit --add-topic 3d-slicer-extension
```

### Screenshot URL 404

Ensure screenshots are committed and pushed, then verify the URL path matches the actual file location:

```bash
# Check where screenshots are
ls Screenshots/

# URL should match: https://raw.githubusercontent.com/OWNER/REPO/BRANCH/Screenshots/filename.png
```

### Missing Extension JSON

Fetch the current schema version and create the JSON:

```bash
# Get current schema URL
curl -s "https://api.github.com/repos/Slicer/Slicer/contents/Schemas" | grep -o '"name": "slicer-extension-catalog-entry-schema-v[^"]*"' | head -1
```

Then create `ExtensionName.json` in the repository root using the current schema URL.

## Next Steps

After validation passes, use the `/submit-to-extension-index` skill in Claude Code to complete the submission.
