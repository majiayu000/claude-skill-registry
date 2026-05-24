---
skill: 'data-sovereignty'
version: '2.0.0'
updated: '2025-12-31'
category: 'risk-compliance'
complexity: 'advanced'
prerequisite_skills:
  - 'risk-assessment'
  - 'legal-compliance'
composable_with:
  - 'local-ai-deployment'
  - 'mlops-operations'
  - 'production-readiness'
---

# Data Sovereignty Skill

## Overview
Expertise in maintaining complete control over enterprise data in AI systems, ensuring data residency compliance, implementing privacy protections, and achieving regulatory compliance across jurisdictions.

## Key Capabilities
- Data residency and localization requirements
- Privacy regulation compliance (GDPR, CCPA, HIPAA)
- Data classification and handling policies
- Cross-border data transfer restrictions
- Audit trail and access control design
- Privacy-enhancing technologies

## Data Sovereignty Fundamentals

### Core Principles

```markdown
## Data Sovereignty Principles for AI

### 1. Data Residency
Data must remain within specified geographic boundaries
- Physical storage location
- Processing location
- Backup and disaster recovery locations

### 2. Data Control
Organization maintains complete authority over data
- Who can access
- How it's processed
- When it's deleted

### 3. Data Portability
Ability to move data between systems
- Export in standard formats
- No vendor lock-in
- Complete data retrieval on demand

### 4. Legal Jurisdiction
Data subject to laws of specific jurisdiction
- Which laws apply
- Which courts have authority
- Regulatory oversight
```

### Why Data Sovereignty Matters for AI

| Concern | Without Sovereignty | With Sovereignty |
|---------|--------------------|--------------------|
| Data exposure | Code/prompts sent to external APIs | All processing local |
| Regulatory risk | Complex compliance across jurisdictions | Single jurisdiction |
| IP protection | Potential training data contribution | No external exposure |
| Audit capability | Limited visibility | Complete audit trail |
| Vendor dependency | Subject to vendor changes | Full control |

## Regulatory Framework

### GDPR Requirements

```markdown
## GDPR Data Sovereignty Requirements

### Data Localization
- **Default:** Data can be processed in EU/EEA
- **Adequacy decisions:** Certain countries approved (limited)
- **Standard Contractual Clauses:** Required for most transfers
- **Post-Schrems II:** Enhanced due diligence required

### Key Articles for AI

**Article 5 - Principles**
- Purpose limitation: Only process for specified purposes
- Data minimization: Only collect what's necessary
- Storage limitation: Delete when no longer needed
- Integrity and confidentiality: Secure processing

**Article 25 - Data Protection by Design**
- Privacy built into systems from the start
- Default settings favor privacy
- Technical and organizational measures

**Article 28 - Processors**
- If using any third party: DPA required
- Processor must meet GDPR requirements
- Controller remains responsible

**Article 44-49 - International Transfers**
- Transfers outside EU restricted
- Need legal basis for any transfer
- Adequacy, SCCs, or BCRs required

### Compliance Strategy: Keep Data Local
Local AI eliminates most GDPR transfer concerns:
- No Article 44-49 analysis needed
- Simplified compliance
- Reduced documentation burden
- Lower regulatory risk
```

### HIPAA Requirements

```markdown
## HIPAA Data Sovereignty Requirements

### Protected Health Information (PHI)
Any information that:
- Relates to health condition, treatment, or payment
- Identifies or could identify an individual
- Created or received by covered entity

### Data Residency Rules
- **No specific localization:** US law, applies to covered entities
- **Business Associates:** Any processor must sign BAA
- **Cloud services:** Must have BAA, may have location requirements
- **Local AI advantage:** No BAA needed, complete control

### Technical Safeguards (45 CFR 164.312)
- Access controls (unique user ID, emergency access)
- Audit controls (record and examine activity)
- Integrity controls (authenticate PHI)
- Transmission security (encryption)

### Local AI Compliance
| Requirement | Local AI Implementation |
|-------------|------------------------|
| Access controls | RBAC with authentication |
| Audit controls | Comprehensive logging |
| Integrity | No external modification possible |
| Transmission | Internal network only, encrypted |
| BAA requirement | Not needed (no third party) |
```

### Industry-Specific Requirements

```markdown
## Industry Data Sovereignty Requirements

### Financial Services
- **Regulations:** GLBA, SOX, DORA (EU), MAS (Singapore)
- **Key requirements:**
  - Customer financial data protection
  - Audit trail retention (7+ years)
  - Operational resilience
  - Third-party risk management
- **Local AI benefit:** No third-party data sharing

### Healthcare
- **Regulations:** HIPAA (US), GDPR (EU), PIPEDA (Canada)
- **Key requirements:**
  - PHI protection
  - Patient consent
  - Breach notification
  - Minimum necessary
- **Local AI benefit:** No BAAs, complete PHI control

### Government/Defense
- **Regulations:** FedRAMP, ITAR, EAR
- **Key requirements:**
  - Data classification levels
  - Citizenship requirements for access
  - Air-gapped networks
- **Local AI benefit:** Air-gapped deployment possible

### Legal
- **Regulations:** Attorney-client privilege, professional rules
- **Key requirements:**
  - Confidentiality
  - Client data protection
  - Ethical obligations
- **Local AI benefit:** No third-party access to privileged info
```

## Data Classification Framework

### Classification Levels

```markdown
## Enterprise Data Classification for AI Systems

### Level 1: PUBLIC
**Description:** Information intended for public release
**Examples:**
- Open source code
- Public documentation
- Marketing materials
**AI Processing:** Unrestricted
**Controls:** None required

### Level 2: INTERNAL
**Description:** General business information not for public release
**Examples:**
- Internal documentation
- General communications
- Non-sensitive code
**AI Processing:** Local AI only
**Controls:**
- Authentication required
- Access logging

### Level 3: CONFIDENTIAL
**Description:** Sensitive business information
**Examples:**
- Proprietary source code
- Business strategies
- Customer lists (non-PII)
- Internal designs
**AI Processing:** Local AI with enhanced controls
**Controls:**
- RBAC
- Audit logging
- Encryption at rest
- Need-to-know access

### Level 4: RESTRICTED
**Description:** Highly sensitive with regulatory implications
**Examples:**
- PII (names, emails, SSN)
- PHI (health records)
- Financial records
- Credentials
**AI Processing:** Local AI with strict controls + approval
**Controls:**
- Explicit authorization
- DLP scanning
- Full audit trail
- Automatic redaction
- Encryption everywhere

### Level 5: PROHIBITED
**Description:** Must never be processed by AI
**Examples:**
- Passwords and secrets
- Private keys
- Classified information
- Raw biometrics
**AI Processing:** BLOCKED
**Controls:**
- Technical prevention (DLP)
- Blocked at input
```

### Classification Implementation

```markdown
## Data Classification Workflow

### Input Classification
```
User Input → DLP Scan → Classify → Process/Block
                ↓
         [Level Determination]
                ↓
    ┌───────────────────────────┐
    │ Level 1-3: Process       │
    │ Level 4: Process + Log   │
    │ Level 5: Block + Alert   │
    └───────────────────────────┘
```

### Classification Signals
| Signal Type | Detection Method | Action |
|-------------|------------------|--------|
| PII patterns | Regex matching | Tag Level 4 |
| Code markers | File extension, content | Tag Level 3 |
| Secret patterns | Entropy, patterns | Block Level 5 |
| Healthcare terms | Keyword matching | Tag Level 4 |
| File source | Path analysis | Inherit classification |
```

## Privacy-Preserving Techniques

### Technical Controls

```markdown
## Privacy-Enhancing Technologies for AI

### 1. Data Minimization
**Principle:** Only include necessary data in prompts
**Implementation:**
- Truncate context to relevant sections
- Remove comments containing names/identifiers
- Use summaries instead of full documents
- Strip file metadata

### 2. Anonymization
**Principle:** Remove identifying information
**Implementation:**
- Replace names with placeholders
- Generalize dates (year only)
- Remove unique identifiers
- Aggregate data where possible

### 3. Pseudonymization
**Principle:** Replace identifiers with consistent tokens
**Implementation:**
- Map real names to consistent pseudonyms
- Maintain referential integrity
- Store mapping separately (if reversal needed)
- Token rotation for long-running tasks

### 4. Differential Privacy
**Principle:** Add noise to prevent individual identification
**Use case:** Analytics and aggregate queries
**Note:** Complex to implement for generative AI

### 5. Secure Enclaves
**Principle:** Process sensitive data in isolated environment
**Implementation:**
- Confidential computing (SGX, SEV)
- Limited applicability for large LLMs
- Emerging technology
```

### PII Detection Patterns

```python
# PII Detection Reference Patterns

PII_PATTERNS = {
    # Direct identifiers
    'email': r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}',
    'phone_us': r'\b\d{3}[-.\s]?\d{3}[-.\s]?\d{4}\b',
    'phone_intl': r'\+\d{1,3}[-.\s]?\d{1,14}',
    'ssn': r'\b\d{3}-\d{2}-\d{4}\b',
    'credit_card': r'\b\d{4}[-\s]?\d{4}[-\s]?\d{4}[-\s]?\d{4}\b',

    # Credentials (should block)
    'api_key_generic': r'[a-zA-Z0-9]{32,}',
    'aws_access_key': r'AKIA[0-9A-Z]{16}',
    'github_token': r'ghp_[a-zA-Z0-9]{36}',
    'private_key': r'-----BEGIN.*PRIVATE KEY-----',

    # Network identifiers
    'ipv4': r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b',
    'ipv6': r'([0-9a-fA-F]{1,4}:){7}[0-9a-fA-F]{1,4}',
}

# Detection thresholds
BLOCK_ON_DETECTION = ['ssn', 'credit_card', 'api_key_generic',
                       'aws_access_key', 'github_token', 'private_key']
WARN_ON_DETECTION = ['email', 'phone_us', 'phone_intl', 'ipv4']
```

## Data Residency Implementation

### Architecture Patterns

```markdown
## Data Residency Architecture

### Pattern 1: Single-Region Deployment
```
┌─────────────────────────────────────────┐
│           Single Data Center            │
│  ┌─────────┐ ┌─────────┐ ┌─────────┐   │
│  │   LLM   │ │ Storage │ │  Logs   │   │
│  │ Server  │ │ (models)│ │ (audit) │   │
│  └─────────┘ └─────────┘ └─────────┘   │
│         All data stays here             │
└─────────────────────────────────────────┘
```
**Best for:** Strictest data residency, single jurisdiction

### Pattern 2: Regional Deployment with Local Processing
```
┌──────────────┐     ┌──────────────┐
│   Region A   │     │   Region B   │
│ ┌──────────┐ │     │ ┌──────────┐ │
│ │   LLM    │ │     │ │   LLM    │ │
│ │ Instance │ │     │ │ Instance │ │
│ └──────────┘ │     │ └──────────┘ │
│ Data stays   │     │ Data stays   │
│ in Region A  │     │ in Region B  │
└──────────────┘     └──────────────┘
```
**Best for:** Multi-region teams, different regulatory zones

### Pattern 3: Air-Gapped Deployment
```
┌─────────────────────────────────────────┐
│            AIR GAP BOUNDARY             │
│  ┌─────────────────────────────────┐   │
│  │     Isolated Network            │   │
│  │  ┌─────────┐ ┌─────────────┐   │   │
│  │  │   LLM   │ │  Offline    │   │   │
│  │  │ Server  │ │  Storage    │   │   │
│  │  └─────────┘ └─────────────┘   │   │
│  │  NO EXTERNAL CONNECTIVITY       │   │
│  └─────────────────────────────────┘   │
└─────────────────────────────────────────┘
```
**Best for:** Highest security, classified environments
```

### Data Flow Controls

```markdown
## Preventing Data Leakage

### Network Controls
```yaml
# Firewall rules for AI server
firewall_rules:
  inbound:
    - source: 10.0.0.0/8  # Internal only
      port: 8000
      action: allow
    - source: any
      port: any
      action: deny

  outbound:
    - destination: any
      port: any
      action: deny  # No external access
```

### Application Controls
```yaml
# vLLM configuration for data sovereignty
vllm_config:
  # Disable telemetry
  disable_telemetry: true

  # No external API calls
  trust_remote_code: false

  # Offline mode
  offline: true

  # Logging controls
  log_requests: false  # Don't log prompts by default
  log_responses: false
```

### Monitoring for Data Exfiltration
- Network traffic analysis (should be zero external)
- DNS query monitoring (block external resolution)
- Process monitoring (no unexpected outbound connections)
- File system monitoring (no writes to removable media)
```

## Audit and Compliance

### Audit Trail Requirements

```markdown
## Data Sovereignty Audit Trail

### What to Log
| Event | Data Captured | Retention | Purpose |
|-------|---------------|-----------|---------|
| Access | User, timestamp, IP | 1 year | Who accessed |
| Query | User, classification level | 90 days | What was processed |
| Admin | User, action, target | 7 years | Configuration changes |
| Security | Event type, severity | 1 year | Incident response |

### Log Integrity
- Write-once storage (WORM where required)
- Cryptographic hashing for tamper detection
- Centralized log aggregation
- Backup to separate system

### Compliance Reporting
```json
{
  "report_type": "data_sovereignty_compliance",
  "period": "2025-Q1",
  "data_residency": {
    "processing_locations": ["us-east-dc1"],
    "storage_locations": ["us-east-dc1"],
    "no_external_transfers": true
  },
  "access_summary": {
    "total_users": 45,
    "total_requests": 150000,
    "pii_incidents": 0,
    "blocked_requests": 12
  },
  "compliance_status": "COMPLIANT"
}
```
```

### Compliance Checklist

```markdown
## Data Sovereignty Compliance Checklist

### Infrastructure
- [ ] All processing occurs in approved locations
- [ ] No external API calls from AI systems
- [ ] Network isolation implemented
- [ ] Encryption at rest and in transit
- [ ] Air-gap option available if required

### Data Handling
- [ ] Data classification policy implemented
- [ ] PII detection active
- [ ] Prohibited data blocked
- [ ] Data minimization enforced
- [ ] Retention limits enforced

### Access Control
- [ ] Authentication required
- [ ] RBAC implemented
- [ ] Admin access audited
- [ ] Access reviews conducted

### Audit & Logging
- [ ] Comprehensive audit trail
- [ ] Log integrity protected
- [ ] Retention meets requirements
- [ ] Regular compliance reports

### Documentation
- [ ] Data flow diagrams current
- [ ] Processing activities documented
- [ ] Policies documented
- [ ] Risk assessments completed
```

## Cross-Border Considerations

### Data Transfer Restrictions

```markdown
## When Data Stays Local, Transfers Are Avoided

### Traditional Cloud AI (Transfer Required)
User Prompt → [CROSSES BORDER] → Cloud API → [CROSSES BORDER] → Response
- Requires SCCs, adequacy, or other legal basis
- Complex compliance analysis
- Ongoing monitoring for legal changes
- Risk of regulatory action

### Local AI (No Transfer)
User Prompt → Local LLM → Response
- All processing in single jurisdiction
- No transfer analysis needed
- Simplified compliance
- Regulatory certainty
```

### Multi-Jurisdiction Teams

```markdown
## Supporting Global Teams with Local AI

### Option 1: Regional Instances
Each region has its own deployment:
- EU team uses EU instance
- US team uses US instance
- APAC team uses APAC instance
- Data never leaves region

### Option 2: Nearest Processing
Route users to geographically closest instance:
- Latency optimization
- Data residency compliance
- Load balancing benefits

### Option 3: Single Global Instance
If single jurisdiction acceptable:
- Simplest architecture
- May require legal analysis for international users
- Consider user location disclosure
```

## Best Practices

### Design Principles
1. **Local by default:** Process data locally unless absolutely necessary
2. **Minimize data:** Only include necessary data in prompts
3. **Classify everything:** Know what data you're processing
4. **Log appropriately:** Audit trail without exposing sensitive data
5. **Defense in depth:** Multiple layers of protection

### Implementation
1. **Air-gap capability:** Design for offline operation
2. **Encryption everywhere:** At rest, in transit, in use if possible
3. **Network isolation:** No external connectivity for AI systems
4. **DLP integration:** Detect and block sensitive data
5. **Regular audits:** Verify controls are working

### Governance
1. **Policy documentation:** Clear data handling policies
2. **Training:** Ensure users understand data classification
3. **Incident response:** Plan for data exposure scenarios
4. **Continuous improvement:** Regular review and updates

This skill ensures organizations maintain complete control over their data while leveraging AI capabilities, achieving true data sovereignty without compromise.
