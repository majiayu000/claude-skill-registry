---
name: audit-dependencies
description: Run npm audit and check for outdated/vulnerable dependencies. Returns structured output with vulnerability counts by severity, outdated packages, and recommended updates. Used for security validation and dependency health checks.
---

# Audit Dependencies

Executes npm audit and outdated checks to validate dependency security and freshness.

## Usage

This skill runs dependency audits and returns structured security/maintenance results.

## Checks Performed

1. **Security Audit** (`npm audit`)
   - Vulnerability scanning
   - Severity classification (critical/high/moderate/low)
   - Affected packages

2. **Outdated Packages** (`npm outdated`)
   - Packages behind latest versions
   - Semver distance (patch/minor/major)
   - Update recommendations

## Output Format

### Success (No Vulnerabilities)

```json
{
  "status": "success",
  "audit": {
    "vulnerabilities": {
      "critical": 0,
      "high": 0,
      "moderate": 0,
      "low": 0,
      "total": 0
    },
    "outdated": {
      "count": 5,
      "packages": [
        {"name": "react", "current": "18.2.0", "latest": "18.3.1", "type": "minor"}
      ]
    }
  },
  "canProceed": true
}
```

### Vulnerabilities Found

```json
{
  "status": "error",
  "audit": {
    "vulnerabilities": {
      "critical": 2,
      "high": 5,
      "moderate": 10,
      "low": 3,
      "total": 20
    },
    "packages": [
      {
        "name": "lodash",
        "severity": "high",
        "via": ["prototype pollution"],
        "fix": "npm install lodash@latest"
      }
    ],
    "outdated": {
      "count": 12,
      "packages": []
    }
  },
  "canProceed": false,
  "details": "2 critical and 5 high severity vulnerabilities must be fixed"
}
```

## When to Use

- Security validation (before deployment)
- Regular maintenance checks
- Conductor Phase 3 (Quality Assurance)
- Security audit agent workflows
- Dependency update planning

## Requirements

- npm or package manager installed
- package.json and package-lock.json present
- Internet connection for vulnerability database
