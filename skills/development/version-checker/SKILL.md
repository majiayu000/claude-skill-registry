---
name: version-checker
description: Check version compatibility, breaking changes, and security vulnerabilities
  for dependencies
allowed-tools: Read, Bash
---

# Version Checker Skill

## Purpose

The Version Checker skill provides version compatibility analysis, breaking change detection, and security vulnerability scanning for Python dependencies. It validates version specifiers, checks for breaking changes between versions, and identifies security vulnerabilities in dependency versions.

**Key Functions:**
- Parse and validate version specifiers (>=, ~=, ^, ==, etc.)
- Check compatibility across Python versions
- Detect breaking changes between package versions
- Scan for security vulnerabilities
- Recommend upgrade paths
- Generate version compatibility reports

## When to Use

Use this skill when you need to:
- Validate version specifiers in dependency declarations
- Check if new dependency versions are compatible with Python 3.11+
- Detect breaking changes when upgrading dependencies
- Scan dependencies for security vulnerabilities
- Plan dependency upgrade strategies
- Resolve version conflicts

**Typical Scenarios:**
- Phase 2 design (version compatibility for PRP)
- Dependency upgrade planning
- Security vulnerability assessment
- Version conflict resolution
- Compatibility verification before installation

## Workflow

### 1. Parse Version Specifiers

**Action**: Extract and validate version specifiers from dependency declarations

**Version Specifier Types**:
- `==1.2.3` - Exact version match
- `>=1.0.0` - Minimum version (inclusive)
- `>1.0.0` - Minimum version (exclusive)
- `<=2.0.0` - Maximum version (inclusive)
- `<2.0.0` - Maximum version (exclusive)
- `~=1.2.0` - Compatible release (>=1.2.0, <2.0.0)
- `>=1.0,<2.0` - Range specifier
- `!=1.3.0` - Exclude specific version

**Example**:
```bash
# Validate version specifiers
echo "httpx>=0.27.0" | grep -E '^[a-zA-Z0-9_-]+[><=~!].*'
```

**Output**: Valid/invalid version specifier

### 2. Check Python Version Compatibility

**Action**: Verify dependency compatibility with target Python version (3.11+)

**Process**:
1. Read package metadata from PyPI
2. Check `python_requires` field
3. Verify compatibility with Python 3.11+
4. Report incompatibilities

**Example**:
```bash
# Check Python compatibility via pip
pip index versions httpx | grep -A 5 "Available versions"
```

**Output**: Python version compatibility status

### 3. Detect Breaking Changes

**Action**: Identify breaking changes between versions

**Breaking Change Indicators**:
- Major version bump (1.x.x → 2.x.x)
- Deprecated API removal
- Changed function signatures
- Removed features
- Configuration format changes

**Process**:
1. Compare current version to target version
2. Parse CHANGELOG or release notes
3. Identify major version changes
4. List breaking changes
5. Suggest migration strategies

**Example**:
```markdown
### Breaking Changes: pydantic 1.10 → 2.0

**Major Changes**:
- BaseModel API changes (validation rewrite)
- Field() signature changes
- Config class → ConfigDict
- parse_obj() → model_validate()
- dict() → model_dump()

**Migration Strategy**:
- Use pydantic.v1 compatibility shim during migration
- Update validators and serializers
- Migrate incrementally
```

**Output**: Breaking change report

### 4. Scan Security Vulnerabilities

**Action**: Check for known security vulnerabilities in dependency versions

**Tools**:
- pip-audit (Python dependency scanner)
- safety (Python vulnerability database)
- GitHub Security Advisories

**Process**:
```bash
# Scan with pip-audit (if available)
which pip-audit && pip-audit --desc

# Scan with safety (if available)
which safety && safety check --json

# Manual check against security-advisory-db.md
grep "package-name" .claude/skills/version-checker/security-advisory-db.md
```

**Output**: Security vulnerability report

### 5. Recommend Upgrade Paths

**Action**: Suggest safe upgrade paths for dependencies

**Upgrade Strategies**:

**Strategy 1: Minor Version Upgrade** (low risk)
```
Current: package==1.2.3
Upgrade: package==1.2.5
Risk: Low (patch/bugfix updates)
```

**Strategy 2: Major Version Upgrade** (high risk)
```
Current: package==1.10.0
Upgrade: package==2.0.0
Risk: High (breaking changes)
Recommendation: Review migration guide, test thoroughly
```

**Strategy 3: Security Patch** (urgent)
```
Current: package==1.2.3 (CVE-2023-12345)
Upgrade: package==1.2.4 (security fix)
Risk: Low (security patch)
Priority: URGENT
```

**Output**: Recommended upgrade path with risk assessment

## Output Format

### Version Compatibility Report

```markdown
## Version Compatibility Analysis

### Package: httpx

**Current Version**: 0.25.0
**Target Version**: >=0.27.0
**Latest Stable**: 0.27.2

### Python Compatibility
✅ Python 3.11+ supported
- httpx 0.27.0: Python >=3.8
- httpx 0.27.2: Python >=3.8

### Breaking Changes
**0.25.0 → 0.27.0**:
- No breaking changes (minor version)
- New features added
- Bug fixes included

**Recommendation**: ✅ Safe to upgrade

### Security Status
✅ No known vulnerabilities
- Last security audit: 2024-10-15
- Active maintenance
- Regular security updates

### Upgrade Path
```bash
# Recommended upgrade
pip install httpx==0.27.2

# Verification
python -c "import httpx; print(httpx.__version__)"
```

### Installation Command
```bash
# Add to requirements.txt
httpx>=0.27.0

# Or pin to specific version
httpx==0.27.2
```
```

## Best Practices

### Version Selection

**Development Environment**:
- Use version ranges for flexibility: `package>=1.0,<2.0`
- Allow minor/patch updates: `package~=1.2.0`
- Keep dependencies up-to-date

**Production Environment**:
- Pin exact versions for stability: `package==1.2.3`
- Test upgrades in staging first
- Document version selection reasoning

**Library Development**:
- Specify minimum versions: `package>=1.0`
- Avoid overly restrictive bounds: `package>=1.0,<2.0` better than `package==1.0`
- Test against multiple versions

### Breaking Change Management

**Before Upgrading**:
1. Read CHANGELOG/release notes
2. Check for migration guides
3. Test in isolated environment
4. Update tests first
5. Gradual rollout

**During Migration**:
1. Use compatibility shims if available (e.g., pydantic.v1)
2. Update incrementally (module by module)
3. Run comprehensive test suite
4. Monitor for runtime errors

**After Migration**:
1. Remove compatibility shims
2. Update documentation
3. Verify all tests pass
4. Monitor production for issues

### Security Vulnerability Response

**Critical Vulnerabilities** (CVSS ≥ 7.0):
1. Upgrade immediately
2. Test thoroughly but quickly
3. Deploy urgently
4. Monitor for exploitation attempts

**Medium Vulnerabilities** (CVSS 4.0-6.9):
1. Plan upgrade within 1 week
2. Test in staging
3. Deploy during maintenance window

**Low Vulnerabilities** (CVSS < 4.0):
1. Include in next regular update cycle
2. Standard testing process

## Supporting Resources

### version-matrix.md

**Location**: `.claude/skills/version-checker/version-matrix.md`

**Contents**:
- Python version compatibility matrix
- Common library version ranges
- Breaking change references by package
- Upgrade path recommendations
- Platform-specific version notes

**Usage**:
```bash
# Check compatibility for specific package
grep -A 10 "package-name" version-matrix.md
```

### security-advisory-db.md

**Location**: `.claude/skills/version-checker/security-advisory-db.md`

**Contents**:
- Known security vulnerabilities
- CVE references
- Affected version ranges
- Fixed versions
- Severity ratings (CVSS scores)
- Mitigation strategies

**Usage**:
```bash
# Check for security advisories
grep -B 5 -A 10 "package-name" security-advisory-db.md
```

## Example Usage

### Scenario 1: Check New Dependency Compatibility

**Input**: Feature requires httpx>=0.27.0

**Process**:
1. Check Python compatibility → httpx 0.27.0 supports Python 3.8+
2. Verify with Python 3.11+ → ✅ Compatible
3. Check for breaking changes → None (from 0.25.0 to 0.27.0)
4. Scan for vulnerabilities → None found
5. Recommend version → httpx==0.27.2 (latest stable)

**Output**:
```markdown
### httpx Compatibility

✅ **Python 3.11+ Compatible**
✅ **No Breaking Changes**
✅ **No Security Vulnerabilities**

**Recommended Version**: httpx==0.27.2

**Installation**:
```bash
pip install httpx==0.27.2
```
```

### Scenario 2: Detect Breaking Changes

**Input**: Upgrade pydantic from 1.10.0 to 2.5.0

**Process**:
1. Identify major version change → 1.x to 2.x
2. Parse release notes → List breaking changes
3. Check migration guide → Found at pydantic docs
4. Assess impact → High (API changes)
5. Recommend strategy → Use pydantic.v1 shim, migrate incrementally

**Output**:
```markdown
### pydantic 1.10.0 → 2.5.0 Upgrade

⚠️  **Major Version Change - Breaking Changes Expected**

**Breaking Changes**:
- BaseModel validation rewritten
- parse_obj() → model_validate()
- dict() → model_dump()
- Config class → ConfigDict
- Field() signature changes

**Migration Strategy**:
1. Install pydantic 2.5.0
2. Use compatibility shim during migration:
   ```python
   from pydantic.v1 import BaseModel  # Legacy code
   from pydantic import BaseModel     # New code
   ```
3. Migrate modules incrementally
4. Update tests alongside code
5. Remove shim when migration complete

**Resources**:
- [pydantic Migration Guide](https://docs.pydantic.dev/latest/migration/)

**Recommendation**: ⚠️  Plan 2-3 days for migration and testing
```

### Scenario 3: Security Vulnerability Scan

**Input**: Check requests library for vulnerabilities

**Process**:
1. Check current version → requests==2.28.0
2. Query security database → Found CVE-2023-32681
3. Check fixed version → 2.31.0+
4. Assess severity → Medium (CVSS 6.5)
5. Recommend upgrade → requests==2.32.0

**Output**:
```markdown
### requests Security Scan

⚠️  **Vulnerability Detected**

**CVE**: CVE-2023-32681
**Severity**: Medium (CVSS 6.5)
**Affected**: requests <2.31.0
**Current Version**: 2.28.0
**Fixed Version**: 2.31.0+

**Vulnerability**:
Improper handling of proxy headers could allow HTTP request smuggling

**Recommendation**: ⬆️  Upgrade to requests==2.32.0 (latest stable)

**Upgrade Command**:
```bash
pip install requests==2.32.0
```

**Priority**: Medium - Upgrade within 1 week
```

## Integration with Feature Implementation Flow

**Input**: New dependency requirements from analysis document

**Process**:
1. Dependency Manager agent activates this skill
2. Skill validates version specifiers
3. Skill checks Python 3.11+ compatibility
4. Skill detects breaking changes
5. Skill scans for security vulnerabilities
6. Skill recommends versions with rationale

**Output**: Version compatibility section for PRP

**Next Step**: Dependency Manager synthesizes version analysis into dependency section

## Advanced Features

### Automated Version Checking

```bash
#!/bin/bash
# Auto-check versions for all dependencies

# Parse requirements.txt
while IFS= read -r line; do
    # Skip comments and empty lines
    [[ "$line" =~ ^#.*$ ]] && continue
    [[ -z "$line" ]] && continue

    # Extract package name
    pkg=$(echo "$line" | sed 's/[><=~!].*$//')

    # Check latest version
    latest=$(pip index versions "$pkg" 2>/dev/null | grep -oP 'Available versions: \K[^,]+' | head -1)

    echo "$pkg: $line (latest: $latest)"
done < requirements.txt
```

### Breaking Change Detection

```python
#!/usr/bin/env python3
"""Detect breaking changes between versions."""

import re
from typing import Tuple

def parse_version(version: str) -> Tuple[int, int, int]:
    """Parse semantic version."""
    match = re.match(r'(\d+)\.(\d+)\.(\d+)', version)
    if match:
        return tuple(int(g) for g in match.groups())
    return (0, 0, 0)

def is_breaking_change(old: str, new: str) -> bool:
    """Check if version change is breaking (major version bump)."""
    old_ver = parse_version(old)
    new_ver = parse_version(new)
    return new_ver[0] > old_ver[0]

# Example usage
if is_breaking_change("1.10.0", "2.0.0"):
    print("⚠️  Breaking changes expected - major version bump")
```

---

**Version**: 2.0.0
**Agent**: @dependency-manager
**Phase**: 2 (Design & Planning)
**Created**: 2025-10-29