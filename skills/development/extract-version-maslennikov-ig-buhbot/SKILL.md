---
name: extract-version
description: Parse and validate semantic version strings from various formats. Use for extracting versions from text, validating semver compliance, or comparing version numbers.
---

# Extract Version

Parse semantic version strings and validate semver compliance.

## When to Use

- Extract version from mixed text
- Validate version format
- Parse version components
- Compare version numbers
- Normalize version strings

## Instructions

### Step 1: Receive Version Input

Accept version string in various formats.

**Expected Input**:

- `versionString`: String (e.g., "v0.7.0", "0.7.0", "version: 0.7.0", "Ver. 1.2.3-beta.1")

### Step 2: Extract Version Pattern

Use regex to extract semver pattern.

**Patterns to Match**:

- `X.Y.Z`: Basic semver
- `vX.Y.Z`: With 'v' prefix
- `X.Y.Z-prerelease`: With prerelease tag
- `X.Y.Z+build`: With build metadata
- Full semver: `X.Y.Z-prerelease+build`

**Regex**:

```
(\d+)\.(\d+)\.(\d+)(?:-([a-zA-Z0-9.-]+))?(?:\+([a-zA-Z0-9.-]+))?
```

### Step 3: Parse Components

Extract major, minor, patch, and optional components.

**Components**:

- `major`: First number
- `minor`: Second number
- `patch`: Third number
- `prerelease`: Optional prerelease tag (after -)
- `build`: Optional build metadata (after +)

### Step 4: Validate Semver

Check if version follows semantic versioning 2.0.0 spec.

**Validation Rules**:

- Major, minor, patch must be non-negative integers
- Prerelease and build must match allowed characters
- No leading zeros in numeric identifiers (except 0 itself)

### Step 5: Return Parsed Data

Return structured version object.

**Expected Output**:

```json
{
  "major": 0,
  "minor": 7,
  "patch": 0,
  "prerelease": null,
  "build": null,
  "original": "v0.7.0",
  "normalized": "0.7.0",
  "valid": true,
  "semver": "0.7.0"
}
```

## Error Handling

- **No Version Found**: Return error indicating no version pattern matched
- **Invalid Format**: Return error with invalid version string
- **Invalid Component**: Describe which component is invalid

## Examples

### Example 1: Basic Version

**Input**:

```
versionString: "0.7.0"
```

**Output**:

```json
{
  "major": 0,
  "minor": 7,
  "patch": 0,
  "prerelease": null,
  "build": null,
  "original": "0.7.0",
  "normalized": "0.7.0",
  "valid": true,
  "semver": "0.7.0"
}
```

### Example 2: Version with Prefix

**Input**:

```
versionString: "v1.2.3"
```

**Output**:

```json
{
  "major": 1,
  "minor": 2,
  "patch": 3,
  "prerelease": null,
  "build": null,
  "original": "v1.2.3",
  "normalized": "1.2.3",
  "valid": true,
  "semver": "1.2.3"
}
```

### Example 3: Prerelease Version

**Input**:

```
versionString: "2.0.0-beta.1"
```

**Output**:

```json
{
  "major": 2,
  "minor": 0,
  "patch": 0,
  "prerelease": "beta.1",
  "build": null,
  "original": "2.0.0-beta.1",
  "normalized": "2.0.0-beta.1",
  "valid": true,
  "semver": "2.0.0-beta.1"
}
```

### Example 4: Full Semver with Build

**Input**:

```
versionString: "1.0.0-alpha.1+001"
```

**Output**:

```json
{
  "major": 1,
  "minor": 0,
  "patch": 0,
  "prerelease": "alpha.1",
  "build": "001",
  "original": "1.0.0-alpha.1+001",
  "normalized": "1.0.0-alpha.1+001",
  "valid": true,
  "semver": "1.0.0-alpha.1+001"
}
```

### Example 5: Extract from Text

**Input**:

```
versionString: "Version: 0.8.0 released on 2025-10-17"
```

**Output**:

```json
{
  "major": 0,
  "minor": 8,
  "patch": 0,
  "prerelease": null,
  "build": null,
  "original": "Version: 0.8.0 released on 2025-10-17",
  "normalized": "0.8.0",
  "valid": true,
  "semver": "0.8.0"
}
```

### Example 6: Invalid Version

**Input**:

```
versionString: "1.2.a"
```

**Output**:

```json
{
  "valid": false,
  "error": "Invalid version format: patch must be numeric",
  "original": "1.2.a"
}
```

## Validation

- [ ] Parses basic semver (X.Y.Z)
- [ ] Handles 'v' prefix correctly
- [ ] Extracts prerelease tags
- [ ] Extracts build metadata
- [ ] Validates semver compliance
- [ ] Extracts version from mixed text
- [ ] Returns normalized version

## Supporting Files

None required - pure parsing logic with regex.
