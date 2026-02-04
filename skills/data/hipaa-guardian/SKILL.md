---
name: hipaa-guardian
description: This skill should be used when the user asks to "scan for PHI", "detect PII", "HIPAA compliance check", "audit for protected health information", "find sensitive healthcare data", "generate HIPAA audit report", "check code for PHI leakage", "scan logs for PHI", "check authentication on PHI endpoints", or mentions PHI detection, HIPAA compliance, healthcare data privacy, medical record security, logging PHI violations, or authentication checks for health data.
license: MIT
metadata:
  author: 1mangesh1
  version: "1.1.0"
  tags:
    - hipaa
    - phi
    - pii
    - healthcare
    - compliance
    - security
    - authentication
    - logging
    - api-security
---

# HIPAA Guardian

A comprehensive PHI/PII detection and HIPAA compliance skill for AI agents, with a strong focus on developer code security patterns. Detects all 18 HIPAA Safe Harbor identifiers in data files and source code, provides risk scoring, maps findings to HIPAA regulations, and generates audit reports with remediation guidance.

## Capabilities

1. **PHI/PII Detection** - Scan data files for the 18 HIPAA Safe Harbor identifiers
2. **Code Scanning** - Detect PHI in source code, comments, test fixtures, configs
3. **Auth Gate Detection** - Find API endpoints exposing PHI without authentication
4. **Log Safety Audit** - Detect PHI leaking into log statements
5. **Classification** - Classify findings as PHI, PII, or sensitive_nonPHI
6. **Risk Scoring** - Score findings 0-100 based on sensitivity and exposure
7. **HIPAA Mapping** - Map each finding to specific HIPAA rules
8. **Audit Reports** - Generate findings.json, audit reports, and playbooks
9. **Remediation** - Provide step-by-step remediation with code examples
10. **Control Checks** - Validate security controls are in place

## Usage

```
/hipaa-guardian [command] [path] [options]
```

### Commands

- `scan <path>` - Scan files or directories for PHI/PII
- `scan-code <path>` - Scan source code for PHI leakage
- `scan-auth <path>` - Check API endpoints for missing authentication before PHI access
- `scan-logs <path>` - Detect PHI patterns in logging statements
- `scan-response <path>` - Check API responses for unmasked PHI exposure
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
- `references/auth-patterns.md` - Authentication gate patterns for PHI endpoints
- `references/logging-safety.md` - PHI-safe logging patterns and filters
- `references/api-security.md` - API response masking and field-level auth

## Examples

- `examples/sample-finding.json` - Example finding output format
- `examples/sample-audit-report.md` - Example audit report
- `examples/synthetic-phi-data.json` - Test data for validation

## Scripts

- `scripts/detect-phi.py` - PHI detection script
- `scripts/scan-code.py` - Code scanning script
- `scripts/generate-report.py` - Report generation script
- `scripts/validate-controls.sh` - Control validation script

---

## Developer-Focused Code Compliance

### Authentication Before PHI Access

**CRITICAL:** Any code that exposes PHI MUST check authentication first.

#### ❌ Non-Compliant: PHI Exposed Without Auth Check

```python
# BAD: No authentication check before returning PHI
@app.route('/api/patient/<patient_id>')
def get_patient(patient_id):
    patient = db.query(Patient).filter_by(id=patient_id).first()
    return jsonify({
        'name': patient.name,
        'ssn': patient.ssn,          # PHI exposed!
        'dob': patient.dob,          # PHI exposed!
        'diagnosis': patient.diagnosis
    })
```

#### ✅ Compliant: Auth Check + Audit Logging

```python
# GOOD: Authentication + authorization + audit logging
@app.route('/api/patient/<patient_id>')
@require_auth                        # Authentication required
@require_role(['doctor', 'nurse'])   # Role-based access
@audit_log('patient_access')         # Audit trail
def get_patient(patient_id):
    user = get_current_user()

    # Verify user has access to THIS patient
    if not user.can_access_patient(patient_id):
        audit.log_unauthorized_access(user.id, patient_id)
        abort(403)

    patient = db.query(Patient).filter_by(id=patient_id).first()

    # Log successful access
    audit.log_phi_access(
        user_id=user.id,
        patient_id=patient_id,
        action='view',
        fields_accessed=['name', 'dob', 'diagnosis']
    )

    return jsonify({
        'name': patient.name,
        'dob': mask_date(patient.dob),  # Mask when possible
        'diagnosis': patient.diagnosis
        # SSN excluded - minimum necessary
    })
```

### PHI in Logging - Detection Patterns

#### ❌ Non-Compliant: Logging PHI Directly

```python
# BAD: PHI in logs - HIPAA violation
logger.info(f"Processing patient: {patient.name}, SSN: {patient.ssn}")
logger.debug(f"Patient DOB: {patient.date_of_birth}")
logger.error(f"Failed to process: {patient_record}")  # Full record in logs!

# BAD: Exception with PHI in stack trace
try:
    process_patient(patient_data)
except Exception as e:
    logger.exception(f"Error processing {patient_data}")  # PHI leaked!
```

#### ✅ Compliant: Safe Logging Practices

```python
# GOOD: Use identifiers only, never PHI values
logger.info(f"Processing patient_id={patient.id}")
logger.debug(f"Patient record hash: {hash_patient_id(patient.id)}")

# GOOD: Mask/redact sensitive data before logging
logger.info(f"Processing patient: {mask_name(patient.name)}, SSN: ***-**-{patient.ssn[-4:]}")

# GOOD: Structured logging with PHI filter
class PHIFilter(logging.Filter):
    """Filter that redacts PHI patterns from log messages."""
    PHI_PATTERNS = [
        (r'\b\d{3}-\d{2}-\d{4}\b', '[SSN-REDACTED]'),
        (r'\b\d{2}/\d{2}/\d{4}\b', '[DOB-REDACTED]'),
        (r'\b[A-Z]{2}\d{6,}\b', '[MRN-REDACTED]'),
    ]

    def filter(self, record):
        for pattern, replacement in self.PHI_PATTERNS:
            record.msg = re.sub(pattern, replacement, str(record.msg))
        return True

# Apply filter to all handlers
logging.getLogger().addFilter(PHIFilter())
```

### Model/API Response PHI Checks

#### ❌ Non-Compliant: Unprotected API Response

```javascript
// BAD: Full patient object returned without filtering
app.get('/api/patients/:id', (req, res) => {
  const patient = await Patient.findById(req.params.id);
  res.json(patient);  // Exposes ALL fields including PHI!
});

// BAD: GraphQL without field-level auth
const PatientType = new GraphQLObjectType({
  name: 'Patient',
  fields: {
    id: { type: GraphQLID },
    ssn: { type: GraphQLString },      // No auth check!
    diagnosis: { type: GraphQLString }  // No auth check!
  }
});
```

#### ✅ Compliant: Protected API Response

```javascript
// GOOD: Explicit field selection with auth
app.get('/api/patients/:id', authenticate, authorize('view_patient'), async (req, res) => {
  const patient = await Patient.findById(req.params.id)
    .select('id name dateOfBirth')  // Only select needed fields
    .lean();

  // Apply field-level masking based on role
  const response = applyPHIMasking(patient, req.user.role);

  // Audit log the access
  await AuditLog.create({
    userId: req.user.id,
    action: 'patient_view',
    resourceId: patient.id,
    fieldsAccessed: Object.keys(response),
    timestamp: new Date(),
    ipAddress: req.ip
  });

  res.json(response);
});

// GOOD: GraphQL with field-level authorization
const PatientType = new GraphQLObjectType({
  name: 'Patient',
  fields: {
    id: { type: GraphQLID },
    ssn: {
      type: GraphQLString,
      resolve: (patient, args, context) => {
        // Field-level auth check
        if (!context.user.hasPermission('view_ssn')) {
          auditLog.unauthorized(context.user.id, 'ssn_access');
          return null;
        }
        auditLog.phiAccess(context.user.id, patient.id, 'ssn');
        return maskSSN(patient.ssn);  // Return masked
      }
    }
  }
});
```

### Database Query PHI Safety

#### ❌ Non-Compliant: Unsafe Database Practices

```python
# BAD: Raw SQL with PHI in query strings
cursor.execute(f"SELECT * FROM patients WHERE ssn = '{ssn}'")

# BAD: Full record fetch without need
patient = Patient.query.get(patient_id)  # Gets ALL columns

# BAD: PHI in error messages
try:
    patient = get_patient(ssn)
except PatientNotFound:
    raise ValueError(f"Patient with SSN {ssn} not found")  # PHI in error!
```

#### ✅ Compliant: Safe Database Practices

```python
# GOOD: Parameterized queries
cursor.execute("SELECT id, name FROM patients WHERE id = %s", (patient_id,))

# GOOD: Select only needed columns
patient = Patient.query.with_entities(
    Patient.id,
    Patient.name,
    Patient.appointment_date
).filter_by(id=patient_id).first()

# GOOD: Safe error handling
try:
    patient = get_patient(patient_id)
except PatientNotFound:
    logger.warning(f"Patient lookup failed for id={patient_id}")
    raise ValueError("Patient not found")  # No PHI in message
```

### Frontend PHI Protection

#### ❌ Non-Compliant: Frontend PHI Exposure

```jsx
// BAD: PHI in browser console/state
console.log('Patient data:', patientData);

// BAD: PHI in localStorage
localStorage.setItem('currentPatient', JSON.stringify(patient));

// BAD: PHI visible in React DevTools
const [patient, setPatient] = useState(fullPatientRecord);
```

#### ✅ Compliant: Frontend PHI Handling

```jsx
// GOOD: Never log PHI
if (process.env.NODE_ENV === 'development') {
  console.log('Patient loaded:', { id: patient.id });  // ID only
}

// GOOD: Session storage with encryption (if needed at all)
const encryptedData = encrypt(JSON.stringify(minimalData));
sessionStorage.setItem('session_data', encryptedData);

// GOOD: Minimal state, masked display
const [patient, setPatient] = useState({
  id: data.id,
  displayName: maskName(data.name),
  // No SSN, full DOB, or diagnosis in state
});

// GOOD: Mask PHI in UI
function PatientCard({ patient }) {
  return (
    <div>
      <p>Name: {patient.displayName}</p>
      <p>DOB: **/**/****</p>  {/* Masked by default */}
      <button onClick={() => revealWithAuth()}>Reveal DOB</button>
    </div>
  );
}
```

---

## Code Scanning Checklist for Developers

When reviewing code, check for these anti-patterns:

### 1. Missing Authentication Gates
```
SCAN FOR: API endpoints without @require_auth, authenticate, or auth middleware
RISK: Unauthenticated PHI access
SEVERITY: Critical
```

### 2. PHI in Log Statements
```
SCAN FOR: logger.*, console.log, print() containing patient.*, ssn, dob, mrn
RISK: PHI in log files, SIEM systems
SEVERITY: High
```

### 3. Unmasked API Responses
```
SCAN FOR: res.json(patient), return patient.*, jsonify(patient)
RISK: Full PHI objects exposed
SEVERITY: High
```

### 4. PHI in Error Messages
```
SCAN FOR: raise.*{patient, raise.*{ssn, throw.*patient
RISK: PHI in error logs and responses
SEVERITY: High
```

### 5. PHI in Test Data
```
SCAN FOR: Real SSN/DOB patterns in /test/, /spec/, fixtures/
RISK: Real PHI in source control
SEVERITY: Critical
```

### 6. Missing Audit Logging
```
SCAN FOR: PHI access without audit.log, AuditLog.create
RISK: No access trail for compliance
SEVERITY: Medium
```

### 7. Client-Side PHI Storage
```
SCAN FOR: localStorage.setItem.*patient, sessionStorage.*ssn
RISK: PHI persisted in browser
SEVERITY: High
```

---

## Quick Reference: PHI-Safe Code Patterns

### The Golden Rule
```
IF code_accesses_phi() THEN
    require_authentication()
    check_authorization()
    log_access_to_audit()
    mask_output()
    never_log_phi_values()
END
```

### Must-Have Checks Before PHI Access

| Check | Python Example | JavaScript Example |
|-------|----------------|-------------------|
| **Auth** | `@require_auth` | `authenticate()` middleware |
| **Authz** | `@require_role(['doctor'])` | `authorize('view_patient')` |
| **Audit** | `audit.log_access(user, patient_id)` | `AuditLog.create({...})` |
| **Mask** | `mask_ssn(patient.ssn)` | `maskPHI(data)` |

### What NOT to Do (Violations)

| ❌ Never | Why It's Bad | ✅ Instead |
|---------|-------------|-----------|
| `logger.info(f"Patient: {patient}")` | PHI in logs | `logger.info(f"patient_id={patient.id}")` |
| `return jsonify(patient)` | Full PHI exposed | `return jsonify(mask_phi(patient))` |
| `raise Error(f"SSN {ssn} invalid")` | PHI in errors | `raise Error("Invalid identifier")` |
| `localStorage.setItem(patient)` | PHI in browser | Use session-only + encrypt |
| `GET /patient/:id` without auth | Public PHI | Add `@require_auth` |

### Detection Patterns for Code Review

```python
# Anti-patterns to search for in code review:
DANGEROUS_PATTERNS = [
    # PHI in logs
    r'(log|print|console)\.(info|debug|error|warn).*patient',
    r'(log|print|console)\.(info|debug|error|warn).*(ssn|dob|mrn)',

    # Unprotected endpoints
    r'@(app|router)\.(get|post|put).*patient.*\n(?!.*@require_auth)',

    # PHI in error messages
    r'raise.*Exception.*\{.*patient',
    r'throw.*Error.*patient',

    # Client storage
    r'localStorage\.setItem.*patient',
    r'sessionStorage\.setItem.*ssn',

    # Full object returns
    r'return.*jsonify\(patient\)',
    r'res\.json\(patient\)',
]
```

### Compliant Code Template

```python
"""Template for PHI-safe endpoint."""
from auth import require_auth, require_role
from audit import audit_log
from masking import mask_phi

@app.route('/api/patient/<patient_id>')
@require_auth                           # 1. Authentication
@require_role(['doctor', 'nurse'])      # 2. Authorization
@audit_log('patient_access')            # 3. Audit logging
@rate_limit(100, per='hour')            # 4. Rate limiting
def get_patient(patient_id):
    user = get_current_user()

    # 5. Resource-level authorization
    if not user.can_access_patient(patient_id):
        audit.log_unauthorized(user.id, patient_id)
        abort(403)

    # 6. Minimum necessary - select only needed fields
    patient = Patient.query.with_entities(
        Patient.id,
        Patient.name,
        Patient.appointment_date
    ).filter_by(id=patient_id).first()

    # 7. Mask before return
    return jsonify({
        'id': patient.id,
        'name': mask_name(patient.name),
        'appointment': patient.appointment_date.isoformat()
    })
```
