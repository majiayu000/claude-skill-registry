---
name: hipaa-guardian
description: HIPAA compliance skill for PHI/PII detection, code scanning, audit reports, and remediation. This skill should be used when the user asks to "scan for PHI", "detect PII", "HIPAA compliance check", "audit for protected health information", "find sensitive healthcare data", "generate HIPAA audit report", or mentions PHI detection, HIPAA compliance, healthcare data privacy, or medical record security.
license: MIT
metadata:
  author: 1mangesh1
  version: "1.0.0"
  tags:
    - hipaa
    - phi
    - pii
    - healthcare
    - compliance
    - security
---

# HIPAA Guardian

Comprehensive HIPAA compliance skill for AI agents. Detects all 18 HIPAA Safe Harbor identifiers in data files and source code, provides risk scoring, maps findings to HIPAA regulations, and generates audit reports with remediation guidance.

## Capabilities

1. **PHI/PII Detection** - Scan data files for the 18 HIPAA Safe Harbor identifiers
2. **Code Scanning** - Detect PHI in source code, comments, test fixtures, configs
3. **Classification** - Classify findings as PHI, PII, or sensitive_nonPHI
4. **Risk Scoring** - Score findings 0-100 based on sensitivity and exposure
5. **HIPAA Mapping** - Map each finding to specific HIPAA rules
6. **Audit Reports** - Generate findings.json, audit reports, and playbooks
7. **Remediation** - Provide step-by-step remediation guidance
8. **Control Checks** - Validate security controls are in place

## Usage

```
/hipaa-guardian [command] [path] [options]
```

### Commands

- `scan <path>` - Scan files or directories for PHI/PII
- `scan-code <path>` - Scan source code for PHI leakage
- `audit <path>` - Generate full HIPAA compliance audit report
- `controls <path>` - Check security controls in a project
- `report` - Generate report from existing findings

### Options

- `--format <type>` - Output format: json, markdown, csv (default: markdown)
- `--output <file>` - Write results to file
- `--severity <level>` - Minimum severity: low, medium, high, critical
- `--include <patterns>` - File patterns to include
- `--exclude <patterns>` - File patterns to exclude
- `--synthetic` - Treat all data as synthetic (default for safety)

## Workflow

When invoked, follow this workflow:

### Step 1: Determine Scan Scope

Ask the user to specify:
- Target path (file, directory, or glob pattern)
- Scan type (data files, source code, or both)
- Whether data is synthetic/test data or potentially real PHI

### Step 2: File Discovery

Use Glob to find relevant files:

```
# For data files
Glob: **/*.{json,csv,txt,log,xml,hl7,fhir}

# For source code
Glob: **/*.{py,js,ts,tsx,java,cs,go,rb,sql,sh}

# For config files
Glob: **/*.{env,yaml,yml,json,xml,ini,conf}
```

### Step 3: PHI Detection

For each file, scan for the 18 HIPAA identifiers using patterns from `references/detection-patterns.md`:

1. **Names** - Patient, provider, relative names
2. **Geographic** - Addresses, cities, ZIP codes
3. **Dates** - DOB, admission, discharge, death dates
4. **Phone Numbers** - All formats
5. **Fax Numbers** - All formats
6. **Email Addresses** - All formats
7. **SSN** - Social Security Numbers
8. **MRN** - Medical Record Numbers
9. **Health Plan IDs** - Insurance identifiers
10. **Account Numbers** - Financial accounts
11. **License Numbers** - Driver's license, professional
12. **Vehicle IDs** - VIN, license plates
13. **Device IDs** - Serial numbers, UDI
14. **URLs** - Web addresses
15. **IP Addresses** - Network identifiers
16. **Biometric** - Fingerprints, retinal, voice
17. **Photos** - Full-face images
18. **Other Unique IDs** - Any other identifying numbers

### Step 4: Classification

Classify each finding:
- **PHI** - Health information linkable to individual
- **PII** - Personally identifiable but not health-related
- **sensitive_nonPHI** - Sensitive but not individually identifiable

### Step 5: Risk Scoring

Calculate risk score (0-100) using methodology from `references/risk-scoring.md`:

```
Risk Score = (Sensitivity × 0.35) + (Exposure × 0.25) +
             (Volume × 0.20) + (Identifiability × 0.20)
```

### Step 6: HIPAA Mapping

Map findings to HIPAA rules from references:
- `references/privacy-rule.md` - 45 CFR 164.500-534
- `references/security-rule.md` - 45 CFR 164.302-318
- `references/breach-rule.md` - 45 CFR 164.400-414

### Step 7: Generate Output

Create structured output following `examples/sample-finding.json` format:

```json
{
  "id": "F-YYYYMMDD-NNNN",
  "timestamp": "ISO-8601",
  "file": "path/to/file",
  "line": 123,
  "field": "field.path",
  "value_hash": "sha256:...",
  "classification": "PHI|PII|sensitive_nonPHI",
  "identifier_type": "ssn|mrn|dob|...",
  "confidence": 0.95,
  "risk_score": 85,
  "hipaa_rules": [...],
  "remediation": [...],
  "status": "open"
}
```

## Code Scanning

When scanning source code, look for:

### 1. Hardcoded PHI in Source
- String literals containing SSN, MRN, names, dates
- Variable assignments with sensitive values
- Database seed/fixture data

### 2. PHI in Comments
- Example data in code comments
- TODO comments with patient info
- Documentation strings with real data

### 3. Test Data Leakage
- Test fixtures with real PHI
- Mock data files with actual patient info
- Integration test data

### 4. Configuration Files
- `.env` files with PHI
- Connection strings with embedded credentials
- API responses cached with PHI

### 5. SQL Files
- INSERT statements with PHI
- Sample queries with real patient data
- Database dumps

See `references/code-scanning.md` for detailed patterns.

## Security Control Checks

Verify these controls are in place:

### Access Controls
- [ ] Role-based access control (RBAC) implemented
- [ ] Minimum necessary access principle applied
- [ ] Access logging enabled

### Encryption
- [ ] Data encrypted at rest (AES-256)
- [ ] Data encrypted in transit (TLS 1.2+)
- [ ] Encryption keys properly managed

### Audit Controls
- [ ] Audit logging implemented
- [ ] Log integrity protected
- [ ] Retention policies defined

### Code Security
- [ ] `.gitignore` excludes sensitive files
- [ ] Pre-commit hooks scan for PHI
- [ ] Secrets management in place
- [ ] Data masking in logs

## Output Formats

### findings.json
Structured array of all findings with full metadata.

### audit_report.md
Human-readable report with:
- Executive summary
- Findings by severity
- HIPAA compliance status
- Risk assessment
- Recommendations

### playbook.md
Step-by-step remediation guide:
- Prioritized actions
- Code examples
- Verification steps

## Security Guardrails

1. **Default Synthetic Mode** - Assumes data is synthetic unless confirmed otherwise
2. **No PHI Storage** - Never stores detected PHI values, only hashes
3. **Redaction** - All example outputs redact actual values
4. **Warning Prompts** - Warns before processing potentially real PHI
5. **Audit Trail** - Logs all scans (without PHI values)

## References

- `references/hipaa-identifiers.md` - All 18 HIPAA Safe Harbor identifiers
- `references/detection-patterns.md` - Regex patterns for PHI detection
- `references/code-scanning.md` - Code scanning patterns and rules
- `references/privacy-rule.md` - HIPAA Privacy Rule (45 CFR 164.500-534)
- `references/security-rule.md` - HIPAA Security Rule (45 CFR 164.302-318)
- `references/breach-rule.md` - Breach Notification Rule (45 CFR 164.400-414)
- `references/risk-scoring.md` - Risk scoring methodology

## Examples

- `examples/sample-finding.json` - Example finding output format
- `examples/sample-audit-report.md` - Example audit report
- `examples/synthetic-phi-data.json` - Test data for validation

## Scripts

- `scripts/detect-phi.py` - PHI detection script
- `scripts/scan-code.py` - Code scanning script
- `scripts/generate-report.py` - Report generation script
- `scripts/validate-controls.sh` - Control validation script
