---
name: healthcare-audit-logger
description: This skill should be used when the user asks to "generate audit logs", "create HIPAA audit trail", "log healthcare events", "configure audit logging", "track PHI access", "maintain compliance logs", "audit log format", "healthcare event logging", "access control logging", "authentication logging", "HIPAA logging requirements", or mentions HIPAA audit trails, healthcare event logging, compliance logging, PHI access tracking, authentication auditing, or §164.312(b) logging requirements.
license: MIT
metadata:
  author: 1mangesh1
  version: "1.0.0"
  tags:
    - hipaa
    - audit-logging
    - compliance
    - healthcare
    - security
    - logging
    - phi-tracking
    - access-control
    - authentication
    - §164.312(b)
---

# Healthcare Audit Logger

Comprehensive HIPAA audit logging and event tracking skill for AI agents. Generates immutable audit trails for healthcare systems, tracks PHI access, monitors authentication events, and ensures compliance with 45 CFR §164.312(b) audit control requirements.

## Capabilities

1. **Audit Log Generation** - Create HIPAA-compliant audit logs with immutable records
2. **Event Classification** - Categorize healthcare events (access, modification, deletion, export)
3. **PHI Access Tracking** - Log all access to Protected Health Information
4. **Authentication Logging** - Record login, logout, and privilege escalation events
5. **Modification Auditing** - Track who changed what, when, and why for PHI records
6. **User Activity Monitoring** - Follow user workflows and data interactions
7. **Timestamp Management** - Synchronized UTC timestamps with tamper detection
8. **Retention Policies** - Manage audit log retention per HIPAA requirements (6+ years)
9. **Log Export** - Generate compliance reports and audit summaries
10. **Integrity Verification** - Validate audit log authenticity and non-repudiation

## Usage

```
/healthcare-audit-logger [command] [options]
```

### Commands

- `init <config-file>` - Initialize audit logging for a healthcare system
- `log <event-type> <details>` - Log a healthcare event
- `log-access <user> <resource> <action>` - Log PHI access
- `log-auth <user> <event> <result>` - Log authentication event
- `log-modification <user> <resource> <change>` - Log data modification
- `policy <retention-years>` - Set audit log retention policy
- `report [date-range]` - Generate audit report
- `verify <log-file>` - Verify audit log integrity
- `export <format> <output>` - Export audit logs (JSON, CSV, XML)

### Options

- `--user <id>` - User identifier
- `--resource <path>` - Resource being accessed (patient ID, record ID)
- `--action <type>` - Action type (read, write, delete, export)
- `--reason <text>` - Clinical reason for access
- `--outcome <status>` - Success or failure status
- `--timestamp <iso8601>` - Event timestamp (default: now)
- `--retention <years>` - Log retention period (default: 6 years per HIPAA)

## Workflow

Follow this workflow when invoked:

### Step 1: Configure Audit System

Ask user to specify:
- Healthcare system type (EHR, medical records, data warehouse)
- Sensitive resources (patient records, medical images, test results)
- User roles and access levels
- Audit log storage location and format

### Step 2: Design Audit Schema

Create logging schema including:
- Event types to track
- User role classifications
- Resource categories
- Access justification requirements
- Timestamp precision (milliseconds for audit accuracy)
- Log entry format (structured JSON recommended)

### Step 3: Implement Audit Logging

Instrument key points:
- Authentication/authorization gates
- PHI access checkpoints
- Data modification operations
- Export/external sharing events
- System configuration changes
- Access permission changes

### Step 4: Validate Compliance

Ensure audit logs capture:
- **User ID** - Who accessed the information (45 CFR §164.312(b)(2)(i))
- **Workstation ID** - Which computer was used
- **Date & Time** - When access occurred (UTC with timezone)
- **Action Performed** - Read, write, delete, export, etc.
- **Resource Accessed** - Patient ID, record type, data elements
- **Outcome** - Success or failure of operation
- **Reason/Justification** - Clinical or operational purpose
- **Result** - Changes made or information retrieved

## HIPAA Compliance Mapping

| Control | Requirement | Implementation |
|---------|-------------|-----------------|
| §164.312(b) | Audit Controls | Implement comprehensive logging |
| §164.312(b)(2)(i) | User Identification | Log all user access with unique IDs |
| §164.312(b)(2)(ii) | Emergency Access Log | Separate tracking for emergency access |
| §164.308(a)(3)(ii)(B) | Workforce Security | Track privilege changes and role assignments |
| §164.308(a)(5)(ii)(C) | Log-in Monitoring | Log authentication attempts and outcomes |
| §164.312(a)(2)(i) | Access Controls | Audit access permissions and changes |
| §164.312(c)(2) | Encryption | Log encryption key operations |
| §164.314(a)(2)(i) | Partner Agreements | Log external system access |

## Example Audit Log Entry

```json
{
  "event_id": "evt_20250207143556_abc123",
  "timestamp": "2025-02-07T14:35:56.123Z",
  "user_id": "dr_jane_smith",
  "user_role": "physician",
  "workstation_id": "ws_04_floor2",
  "action": "read",
  "resource_type": "patient_record",
  "resource_id": "pat_98765", // Encrypted in production
  "data_accessed": ["demographics", "lab_results", "vitals"],
  "clinical_reason": "Patient follow-up appointment",
  "access_result": "success",
  "duration_ms": 45,
  "ip_address": "10.24.5.12", // Masked in logs
  "hipaa_rule": "§164.312(b)(2)(i)"
}
```

## References

- **45 CFR §164.312(b)** Audit Controls
- **45 CFR §164.308(a)(5)(ii)(C)** Log-in Monitoring
- **NIST SP 800-66 Rev. 2** - HIPAA Security Implementation Guidance
- **NIST SP 800-92** - Guide to Computer Security Log Management
- **HHS Office for Civil Rights Audit Protocols**

