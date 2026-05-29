---
name: prepare-extension-metadata
description: Prepare and generate all required metadata files for Extension Index submission
allowed-tools:
  - WebFetch
  - Bash
  - Read
  - Write
  - Grep
context: manual
---

# Prepare Extension Metadata Skill

Prepare and generate all required metadata files for Extension Index submission.

## When to Use

Use this skill when:
- Ready to prepare extension for submission
- Need to update CMakeLists.txt metadata
- Need to generate the Extension Index JSON file
- Need to verify metadata consistency

## CRITICAL: Verify Latest Schema First

**Before generating files, ALWAYS fetch the latest JSON schema:**

```bash
# Fetch current schema to verify required/optional fields
curl -s "https://raw.githubusercontent.com/Slicer/Slicer/main/Schemas/slicer-extension-catalog-entry-schema-v1.0.1.json"
```

If schema version or fields have changed, **the fetched schema is authoritative**.

## Official Sources

- JSON Schema: https://github.com/Slicer/Slicer/blob/main/Schemas/slicer-extension-catalog-entry-schema-v1.0.1.json
- Example Extensions: https://github.com/Slicer/ExtensionsIndex (browse .json files)

---

## Step 1: Gather Required Information

Collect the following from the user or repository:

### For CMakeLists.txt

| Field | Description | Example |
|-------|-------------|---------|
| EXTENSION_HOMEPAGE | URL to documentation/README | `https://github.com/user/repo#readme` |
| EXTENSION_CONTRIBUTORS | Names with affiliations | `"Jane Doe (University), John Smith (Company)"` |
| EXTENSION_DESCRIPTION | 1-2 sentence summary | `"Mouse button remapping for 3D Slicer workflows"` |
| EXTENSION_ICONURL | Raw PNG URL (128x128 recommended) | `https://raw.githubusercontent.com/user/repo/main/Icon.png` |
| EXTENSION_SCREENSHOTURLS | Space-separated raw URLs | `"https://raw.githubusercontent.com/.../1.png https://...2.png"` |
| EXTENSION_DEPENDS | Other extensions required, or "NA" | `"NA"` or `"SlicerIGT SlicerOpenIGTLink"` |

### For Extension Index JSON

| Field | Required | Description |
|-------|----------|-------------|
| $schema | Yes | Schema URL (use current version) |
| category | Yes | Extension category (e.g., "Utilities", "Segmentation") |
| scm_url | Yes | Git clone URL ending in .git |
| scm_revision | No | Branch name (recommended) or commit hash |
| scm_type | No | Default: "git" |
| build_dependencies | No | Array of extension names required to build |
| build_subdirectory | No | Default: "." (use "inner-build" for superbuild) |
| enabled | No | Default: true |
| tier | No | Default: 1 (set based on checklist completion) |

---

## Step 2: Update CMakeLists.txt

Locate and update the extension metadata section:

```cmake
#-----------------------------------------------------------------------------
# Extension meta-information
set(EXTENSION_HOMEPAGE "https://github.com/USERNAME/REPONAME#readme")
set(EXTENSION_CONTRIBUTORS "Contributor Name (Affiliation)")
set(EXTENSION_DESCRIPTION "Brief 1-2 sentence description of extension functionality")
set(EXTENSION_ICONURL "https://raw.githubusercontent.com/USERNAME/REPONAME/main/ExtensionIcon.png")
set(EXTENSION_SCREENSHOTURLS "https://raw.githubusercontent.com/USERNAME/REPONAME/main/Screenshots/screenshot1.png")
set(EXTENSION_DEPENDS "NA") # Or list of extension names
```

### Validation Checks

1. **No placeholder URLs** - Replace all `example.com` references
2. **Raw GitHub URLs for images** - Must start with `https://raw.githubusercontent.com/`
3. **Description is concise** - 1-2 sentences, no line breaks
4. **Contributors include affiliations** - Format: `"Name (Affiliation)"`

---

## Step 3: Generate Extension Index JSON File

Create `ExtensionName.json` for the ExtensionsIndex repository:

```json
{
  "$schema": "https://raw.githubusercontent.com/Slicer/Slicer/main/Schemas/slicer-extension-catalog-entry-schema-v1.0.1.json#",
  "build_dependencies": [],
  "build_subdirectory": ".",
  "category": "CATEGORY_HERE",
  "scm_revision": "main",
  "scm_url": "https://github.com/USERNAME/REPONAME.git",
  "tier": 1
}
```

### Category Options (Common)

- `Diffusion` - Diffusion MRI processing
- `IGT` - Image-guided therapy
- `Informatics` - Data management, DICOM
- `Quantification` - Measurements, analysis
- `Registration` - Image registration
- `Segmentation` - Image segmentation
- `Utilities` - General utilities (use for MouseMaster)

### Build Subdirectory

- Use `.` for standard CMake extensions
- Use `inner-build` for Superbuild extensions (those with external dependencies)

---

## Step 4: Verify Metadata Consistency

Ensure CMakeLists.txt and JSON file are consistent:

```bash
# Extract dependencies from CMakeLists.txt
grep "EXTENSION_DEPENDS" CMakeLists.txt

# Compare with JSON build_dependencies
cat ExtensionName.json | jq '.build_dependencies'
```

### Consistency Rules

| CMakeLists.txt | JSON File |
|----------------|-----------|
| EXTENSION_DEPENDS "NA" | build_dependencies: [] |
| EXTENSION_DEPENDS "ExtA ExtB" | build_dependencies: ["ExtA", "ExtB"] |

---

## Step 5: Verify URLs Are Accessible

```bash
# Test icon URL
curl -sI "ICON_URL" | grep -E "^HTTP|^Content-Type"

# Test screenshot URLs
curl -sI "SCREENSHOT_URL" | grep -E "^HTTP|^Content-Type"

# Test homepage URL
curl -sI "HOMEPAGE_URL" | grep -E "^HTTP"
```

Expected results:
- `HTTP/2 200` or `HTTP/1.1 200 OK`
- `Content-Type: image/png` for images

---

## SlicerMouseMaster Specific Values

For this extension, use:

```cmake
set(EXTENSION_HOMEPAGE "https://github.com/benzwick/SlicerMouseMaster#readme")
set(EXTENSION_CONTRIBUTORS "Ben Zwick (contributor)")
set(EXTENSION_DESCRIPTION "Advanced mouse customization with button remapping, workflow presets, and context-sensitive bindings for multi-button mice.")
set(EXTENSION_ICONURL "https://raw.githubusercontent.com/benzwick/SlicerMouseMaster/main/SlicerMouseMaster/SlicerMouseMaster.png")
set(EXTENSION_SCREENSHOTURLS "https://raw.githubusercontent.com/benzwick/SlicerMouseMaster/main/Screenshots/main-ui.png")
set(EXTENSION_DEPENDS "NA")
```

```json
{
  "$schema": "https://raw.githubusercontent.com/Slicer/Slicer/main/Schemas/slicer-extension-catalog-entry-schema-v1.0.1.json#",
  "build_dependencies": [],
  "build_subdirectory": ".",
  "category": "Utilities",
  "scm_revision": "main",
  "scm_url": "https://github.com/benzwick/SlicerMouseMaster.git",
  "tier": 1
}
```

**Note**: Verify the GitHub username and URLs match the actual repository before using.

---

## Output Files

After running this skill, you should have:

1. **Updated `CMakeLists.txt`** - In extension repository with correct metadata
2. **`SlicerMouseMaster.json`** - Ready to submit to ExtensionsIndex repository
3. **Verification output** - Confirming all URLs are accessible

## Next Steps

After preparing metadata:
1. Commit CMakeLists.txt changes to extension repository
2. Push to GitHub
3. Run `/validate-extension-submission` to verify readiness
4. Run `/extension-submission-checklist` to review all requirements
5. Submit PR to ExtensionsIndex
