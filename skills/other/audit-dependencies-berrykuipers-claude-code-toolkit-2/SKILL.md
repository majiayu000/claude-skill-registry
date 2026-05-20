---
name: audit-dependencies
description: Run npm audit to scan for security vulnerabilities and check for outdated packages. Returns structured output with vulnerability counts by severity (critical/high/moderate/low), affected packages, and recommended updates. Used for security audits and maintenance.
---

# Audit Dependencies

## Purpose

Scan npm dependencies for known security vulnerabilities and identify outdated packages that need updates.

## When to Use

- Security audits before deployment
- Conductor Phase 6 (Final Report)
- Regular maintenance checks
- Before major releases
- As part of security validation workflows

## Supported Package Managers

- **npm**: npm audit + npm outdated
- **yarn**: yarn audit (detects automatically)
- **pnpm**: pnpm audit (detects automatically)

## Instructions

### Step 1: Run Security Audit

```bash
echo "→ Running security audit..."

# Run npm audit with JSON output
if npm audit --json > .claude/validation/audit-output.json 2>&1; then
  AUDIT_STATUS="clean"
  echo "✅ No vulnerabilities found"
else
  AUDIT_STATUS="vulnerabilities"
  echo "⚠️  Vulnerabilities detected"
fi
```

### Step 2: Parse Vulnerability Counts

```bash
# Extract vulnerability counts by severity
if [ -f .claude/validation/audit-output.json ]; then
  CRITICAL=$(jq '.metadata.vulnerabilities.critical // 0' .claude/validation/audit-output.json)
  HIGH=$(jq '.metadata.vulnerabilities.high // 0' .claude/validation/audit-output.json)
  MODERATE=$(jq '.metadata.vulnerabilities.moderate // 0' .claude/validation/audit-output.json)
  LOW=$(jq '.metadata.vulnerabilities.low // 0' .claude/validation/audit-output.json)
  TOTAL=$(jq '.metadata.vulnerabilities.total // 0' .claude/validation/audit-output.json)

  echo "Vulnerability Summary:"
  echo "  Critical: $CRITICAL"
  echo "  High: $HIGH"
  echo "  Moderate: $MODERATE"
  echo "  Low: $LOW"
  echo "  Total: $TOTAL"
fi
```

### Step 3: Extract Affected Packages

```bash
# Get list of vulnerable packages
if [ "$TOTAL" -gt 0 ]; then
  AFFECTED_PACKAGES=$(jq -r '.vulnerabilities | to_entries | map({
    name: .key,
    severity: .value.severity,
    via: (.value.via | if type == "array" then .[0].title else . end)
  }) | sort_by(.severity) | reverse' .claude/validation/audit-output.json)

  # Get top 10 most critical
  TOP_VULNS=$(echo "$AFFECTED_PACKAGES" | jq -c '.[:10]')
else
  AFFECTED_PACKAGES="[]"
  TOP_VULNS="[]"
fi
```

### Step 4: Check for Outdated Packages

```bash
echo ""
echo "→ Checking for outdated packages..."

# Run npm outdated
if npm outdated --json > .claude/validation/outdated-output.json 2>&1; then
  OUTDATED_STATUS="all-current"
  OUTDATED_COUNT=0
else
  # Parse outdated packages
  OUTDATED_COUNT=$(jq 'length' .claude/validation/outdated-output.json 2>/dev/null || echo "0")
  OUTDATED_STATUS="updates-available"

  echo "   $OUTDATED_COUNT packages have updates available"
fi

# Get packages with major version updates
MAJOR_UPDATES=$(jq -r 'to_entries | map(select(
  (.value.wanted != .value.latest) and
  ((.value.latest | split(".")[0] | tonumber?) > (.value.current | split(".")[0] | tonumber?))
)) | length' .claude/validation/outdated-output.json 2>/dev/null || echo "0")

echo "   $MAJOR_UPDATES packages have major version updates"
```

### Step 5: Determine Can Proceed

```bash
# Critical/High vulnerabilities block by default
if [ "$CRITICAL" -gt 0 ] || [ "$HIGH" -gt 0 ]; then
  CAN_PROCEED="false"
  STATUS="error"
  DETAILS="$CRITICAL critical and $HIGH high severity vulnerabilities must be addressed"
elif [ "$MODERATE" -gt 0 ] || [ "$LOW" -gt 0 ]; then
  CAN_PROCEED="true"
  STATUS="warning"
  DETAILS="$MODERATE moderate and $LOW low severity vulnerabilities - review recommended"
else
  CAN_PROCEED="true"
  STATUS="success"
  DETAILS="No security vulnerabilities found"
fi
```

### Step 6: Return Structured Output

```json
{
  "status": "$STATUS",
  "audit": {
    "status": "$AUDIT_STATUS",
    "vulnerabilities": {
      "critical": $CRITICAL,
      "high": $HIGH,
      "moderate": $MODERATE,
      "low": $LOW,
      "total": $TOTAL
    },
    "affectedPackages": $TOP_VULNS
  },
  "outdated": {
    "status": "$OUTDATED_STATUS",
    "count": $OUTDATED_COUNT,
    "majorUpdates": $MAJOR_UPDATES
  },
  "canProceed": $CAN_PROCEED,
  "details": "$DETAILS"
}
```

## Output Format

### No Vulnerabilities

```json
{
  "status": "success",
  "audit": {
    "status": "clean",
    "vulnerabilities": {
      "critical": 0,
      "high": 0,
      "moderate": 0,
      "low": 0,
      "total": 0
    },
    "affectedPackages": []
  },
  "outdated": {
    "status": "all-current",
    "count": 0,
    "majorUpdates": 0
  },
  "canProceed": true,
  "details": "No security vulnerabilities found"
}
```

### Critical Vulnerabilities Found

```json
{
  "status": "error",
  "audit": {
    "status": "vulnerabilities",
    "vulnerabilities": {
      "critical": 2,
      "high": 5,
      "moderate": 8,
      "low": 3,
      "total": 18
    },
    "affectedPackages": [
      {
        "name": "axios",
        "severity": "critical",
        "via": "Server-Side Request Forgery in axios"
      },
      {
        "name": "lodash",
        "severity": "high",
        "via": "Prototype Pollution in lodash"
      }
    ]
  },
  "outdated": {
    "status": "updates-available",
    "count": 12,
    "majorUpdates": 3
  },
  "canProceed": false,
  "details": "2 critical and 5 high severity vulnerabilities must be addressed"
}
```

## Integration with Conductor

Used in conductor Phase 6 (Final Report):

```markdown
### Final Security Check

Use `audit-dependencies` skill:

Expected result:
- No critical/high vulnerabilities
- Moderate/low acceptable (document)

If critical/high found:
  ⚠️  WARNING - Security issues detected
  → Document in PR description
  → Create security follow-up issue
  → May block merge (policy-dependent)

If clean or low-severity only:
  ✅ Security check passed
```

## Severity Levels

### Critical
- Immediate action required
- Known exploits in the wild
- Direct security impact

**Action**: Update immediately or find alternative

### High
- Serious security concern
- Potential for exploitation
- Should be addressed soon

**Action**: Schedule update within days

### Moderate
- Security concern
- Limited exploitation potential
- Should be addressed

**Action**: Schedule update within weeks

### Low
- Minor security issue
- Low exploitation risk
- Address when convenient

**Action**: Include in next maintenance cycle

## Fixing Vulnerabilities

### Auto-Fix (Safe)

```bash
# Let npm attempt auto-fix
npm audit fix

# For breaking changes
npm audit fix --force  # Use with caution!
```

### Manual Update

```bash
# Update specific package
npm update package-name

# Check what would change
npm outdated

# Update all (review changes)
npm update
```

## Related Skills

- `security-pentest` - Uses this for security validation
- `audit` - Comprehensive project audit including dependencies

## Error Handling

### npm Not Available

```json
{
  "status": "error",
  "error": "npm not available",
  "suggestion": "Ensure npm is installed and package.json exists"
}
```

### Network Errors

```bash
# Audit requires network access to vulnerability database
if grep -q 'ENOTFOUND\|ETIMEDOUT' .claude/validation/audit-output.json; then
  echo "⚠️  Network error - cannot reach npm registry"
fi
```

## Best Practices

1. **Run regularly** - Weekly or before each release
2. **Review all findings** - Don't auto-fix without review
3. **Check breaking changes** - Major updates may break code
4. **Document exceptions** - If vulnerability can't be fixed immediately
5. **Track trends** - Monitor vulnerability counts over time

## Notes

- Critical/High vulnerabilities block by default (configurable)
- Moderate/Low generate warnings but don't block
- Outdated packages don't block (informational)
- Output saved to `.claude/validation/audit-output.json`
- Requires internet connection to npm registry
