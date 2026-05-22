---
name: responsible-disclosure
version: "2.0.0"
description: Ethical vulnerability reporting, coordinated disclosure, and bug bounty participation for AI systems
sasmp_version: "1.3.0"
bonded_agent: 01-red-team-commander
bond_type: PRIMARY_BOND
# Schema Definitions
input_schema:
  type: object
  required: [disclosure_type]
  properties:
    disclosure_type:
      type: string
      enum: [coordinated, full, bug_bounty, private]
    vulnerability:
      type: object
      properties:
        severity:
          type: string
          enum: [critical, high, medium, low]
        category:
          type: string
        vendor:
          type: string
    timeline:
      type: object
      properties:
        discovery_date:
          type: string
        disclosure_deadline:
          type: integer
          default: 90
output_schema:
  type: object
  properties:
    disclosure_plan:
      type: object
    report_template:
      type: string
    timeline:
      type: object
    legal_considerations:
      type: array
# Framework Mappings
owasp_llm_2025: [LLM01, LLM02, LLM03, LLM04, LLM05, LLM06, LLM07, LLM08, LLM09, LLM10]
nist_ai_rmf: [Govern, Manage]
---

# Responsible Disclosure

Practice **ethical vulnerability reporting** through coordinated disclosure and bug bounty programs.

## Quick Reference

```yaml
Skill:       responsible-disclosure
Agent:       01-red-team-lead
OWASP:       Full LLM Top 10 Coverage
NIST:        Govern, Manage
Use Case:    Ethical vulnerability reporting
```

## Disclosure Framework

```
┌────────────────────────────────────────────────────────────────────┐
│                    RESPONSIBLE DISCLOSURE LIFECYCLE                 │
├────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  [Discovery] → [Verification] → [Documentation] → [Initial Contact]│
│       ↓              ↓               ↓                  ↓          │
│  Find issue     Reproduce       Full report      Contact vendor    │
│                 in isolation    with POC         security team     │
│                                                                     │
│  [Coordination] → [Remediation] → [Verification] → [Disclosure]    │
│       ↓              ↓               ↓                  ↓          │
│  Work with      Vendor         Confirm fix      Publish after      │
│  vendor         develops fix   is effective     patch available    │
│                                                                     │
└────────────────────────────────────────────────────────────────────┘
```

## Disclosure Types

### Coordinated Disclosure (Recommended)

```python
class CoordinatedDisclosure:
    """Standard coordinated disclosure process."""

    STANDARD_TIMELINE = 90  # days

    def __init__(self, vulnerability: Vulnerability):
        self.vulnerability = vulnerability
        self.timeline = self._calculate_timeline()
        self.communications = []

    def _calculate_timeline(self) -> DisclosureTimeline:
        """Calculate disclosure timeline based on severity."""
        base_days = self.STANDARD_TIMELINE

        # Adjust for severity
        if self.vulnerability.severity == "CRITICAL":
            # Faster timeline for critical issues
            return DisclosureTimeline(
                initial_report=0,
                vendor_response=7,
                fix_development=30,
                patch_release=45,
                public_disclosure=60
            )
        elif self.vulnerability.severity == "HIGH":
            return DisclosureTimeline(
                initial_report=0,
                vendor_response=7,
                fix_development=45,
                patch_release=75,
                public_disclosure=90
            )
        else:
            return DisclosureTimeline(
                initial_report=0,
                vendor_response=14,
                fix_development=60,
                patch_release=90,
                public_disclosure=120
            )

    def execute(self):
        """Execute coordinated disclosure process."""
        # Phase 1: Initial Contact
        self._send_initial_report()

        # Phase 2: Coordination
        self._coordinate_with_vendor()

        # Phase 3: Verification
        self._verify_patch()

        # Phase 4: Public Disclosure
        self._public_disclosure()
```

### Disclosure Timeline

```yaml
Standard Timeline (90 days):
  Day 0:
    action: "Send initial report to vendor"
    method: "Encrypted email to security@vendor.com"
    include:
      - Vulnerability summary
      - Impact assessment
      - Reproduction steps
      - Suggested timeline

  Day 7:
    action: "Expect acknowledgment"
    if_no_response:
      - Send follow-up email
      - Try alternative contacts
      - Consider CERT coordination

  Day 30:
    action: "Status check"
    expect:
      - Vulnerability confirmed
      - Fix in development
      - Estimated patch date

  Day 60:
    action: "Pre-disclosure coordination"
    tasks:
      - Agree on disclosure date
      - Coordinate CVE assignment
      - Prepare public advisory

  Day 90:
    action: "Public disclosure"
    publish:
      - Technical advisory
      - CVE details
      - Vendor credit
    channels:
      - Personal blog
      - Full disclosure lists
      - Security conferences
```

## Bug Bounty Programs

### Major AI Company Programs

```yaml
OpenAI:
  program_type: "Private (HackerOne)"
  scope:
    - ChatGPT vulnerabilities
    - API security issues
    - Model safety bypasses
    - Plugin security
  out_of_scope:
    - Jailbreaks (separate program)
    - Known limitations
    - Social engineering
  rewards:
    critical: "$10,000 - $20,000"
    high: "$5,000 - $10,000"
    medium: "$1,000 - $5,000"
    low: "$200 - $1,000"
  response_time: "< 5 business days"

Anthropic:
  program_type: "Private (Direct)"
  scope:
    - Claude security vulnerabilities
    - API misuse vectors
    - Safety system bypasses
  contact: "security@anthropic.com"
  rewards: "Case by case"
  note: "Focus on novel, impactful issues"

Google (Bard/Gemini):
  program_type: "Public (Google VRP)"
  scope:
    - Bard/Gemini vulnerabilities
    - AI Studio security
    - Model extraction risks
  rewards:
    critical: "$10,000 - $31,337"
    high: "$5,000 - $10,000"
    medium: "$1,000 - $5,000"
  url: "https://bughunters.google.com/"

Microsoft (Azure AI):
  program_type: "Public (MSRC)"
  scope:
    - Azure OpenAI Service
    - Cognitive Services
    - ML infrastructure
  rewards:
    critical: "$15,000 - $26,000"
    high: "$5,000 - $15,000"
    medium: "$1,000 - $5,000"
  url: "https://www.microsoft.com/msrc"

Meta (Llama):
  program_type: "Public (Meta Bug Bounty)"
  scope:
    - Llama model vulnerabilities
    - Meta AI products
    - API security
  rewards:
    minimum: "$500"
    maximum: "$100,000+"
  url: "https://www.facebook.com/whitehat"
```

### Bug Bounty Platforms

```python
class BugBountyPlatforms:
    """Major bug bounty platforms with AI programs."""

    PLATFORMS = {
        "HackerOne": {
            "url": "https://hackerone.com/",
            "ai_programs": [
                "OpenAI",
                "Anthropic",
                "Stability AI",
                "Character.ai"
            ],
            "features": [
                "Managed disclosure",
                "Reputation system",
                "Payment handling"
            ],
            "researcher_fee": "None"
        },
        "Bugcrowd": {
            "url": "https://bugcrowd.com/",
            "ai_programs": [
                "Various startups",
                "Enterprise AI"
            ],
            "features": [
                "Crowdsourced testing",
                "Skills-based matching",
                "Training resources"
            ],
            "researcher_fee": "None"
        },
        "Intigriti": {
            "url": "https://intigriti.com/",
            "ai_programs": [
                "European AI companies"
            ],
            "features": [
                "GDPR compliant",
                "European focus"
            ],
            "researcher_fee": "None"
        }
    }
```

## Vulnerability Report Template

```python
class VulnerabilityReport:
    """Professional vulnerability report template."""

    TEMPLATE = """
# AI Security Vulnerability Report

## Metadata
- **Report ID:** {report_id}
- **Date:** {date}
- **Researcher:** {researcher_name}
- **Contact:** {contact_info}

## Executive Summary
**Title:** {title}
**Severity:** {severity}
**CVSS Score:** {cvss_score}
**CVSS Vector:** {cvss_vector}
**Category:** {category}
**OWASP LLM:** {owasp_mapping}

## Vulnerability Details

### Description
{description}

### Affected Systems
- **Product:** {product}
- **Version:** {version}
- **Component:** {component}
- **Environment:** {environment}

### Impact Assessment

#### Confidentiality Impact
{confidentiality_impact}

#### Integrity Impact
{integrity_impact}

#### Availability Impact
{availability_impact}

#### Business Impact
{business_impact}

## Reproduction Steps

### Prerequisites
{prerequisites}

### Step-by-Step Instructions
{reproduction_steps}

### Proof of Concept
```
{poc_code}
```

### Expected vs Actual Behavior
- **Expected:** {expected_behavior}
- **Actual:** {actual_behavior}

## Evidence

### Screenshots
{screenshots}

### Logs
```
{logs}
```

### Video Demonstration
{video_link}

## Suggested Remediation

### Immediate Actions
{immediate_actions}

### Long-term Fix
{long_term_fix}

### Recommended Timeline
{remediation_timeline}

## Additional Information

### Related CVEs
{related_cves}

### References
{references}

### Disclosure Timeline
| Date | Action |
|------|--------|
{timeline_table}

---

**PGP Key:** {pgp_key}
**Encrypted Communication Preferred**
    """

    def generate(self, vulnerability_data: dict) -> str:
        """Generate formatted vulnerability report."""
        return self.TEMPLATE.format(**vulnerability_data)
```

## Ethical Guidelines

### Research Ethics

```yaml
DO:
  Authorization:
    - Get written permission when possible
    - Use official bug bounty programs
    - Respect scope limitations
    - Document authorization

  Minimization:
    - Access only necessary data
    - Don't exfiltrate real user data
    - Stop after proving the issue
    - Clean up test artifacts

  Reporting:
    - Report promptly after discovery
    - Provide complete reproduction steps
    - Suggest remediation
    - Maintain confidentiality

  Professionalism:
    - Communicate respectfully
    - Be patient with vendors
    - Credit collaborators
    - Follow disclosure timelines

DON'T:
  Exploitation:
    - Access data beyond POC needs
    - Pivot to other systems
    - Maintain persistent access
    - Use vulnerabilities for profit

  Disclosure:
    - Disclose before patch (usually)
    - Threaten or extort vendors
    - Sell vulnerabilities (usually)
    - Publish user data

  Testing:
    - Disrupt production services
    - Test without authorization
    - Social engineer employees
    - Physical intrusion
```

### Legal Framework

```python
class LegalConsiderations:
    """Legal framework for security research."""

    SAFE_HARBOR_POLICIES = {
        "US": {
            "primary_law": "Computer Fraud and Abuse Act (CFAA)",
            "safe_harbor": [
                "Bug bounty program terms",
                "DOJ Policy for Good Faith Research (2022)",
                "Authorized testing agreements"
            ],
            "risks": [
                "CFAA prosecution if unauthorized",
                "Civil liability possible"
            ],
            "recommendations": [
                "Stay within program scope",
                "Document authorization",
                "Consult lawyer if uncertain"
            ]
        },
        "EU": {
            "primary_law": "Various national laws",
            "safe_harbor": [
                "Coordinated disclosure frameworks",
                "NIS2 Directive provisions"
            ],
            "considerations": [
                "GDPR for any data accessed",
                "National cybercrime laws vary"
            ]
        },
        "UK": {
            "primary_law": "Computer Misuse Act 1990",
            "safe_harbor": [
                "CMA prosecution guidance",
                "Good faith research guidance"
            ],
            "recommendations": [
                "Follow NCSC guidance",
                "Use authorized programs"
            ]
        }
    }

    @staticmethod
    def assess_legal_risk(jurisdiction: str, research_type: str) -> LegalAssessment:
        """Assess legal risk for security research."""
        framework = LegalConsiderations.SAFE_HARBOR_POLICIES.get(jurisdiction)

        return LegalAssessment(
            jurisdiction=jurisdiction,
            safe_harbor_available=bool(framework.get("safe_harbor")),
            recommendations=framework.get("recommendations", []),
            risks=framework.get("risks", []),
            advice="Always seek legal counsel for novel research"
        )
```

## Communication Templates

### Initial Contact

```markdown
Subject: Security Vulnerability Report - [Product Name]

Dear Security Team,

I am a security researcher and I have discovered a vulnerability in
[Product Name] that I would like to report through coordinated disclosure.

**Summary:**
- Type: [Vulnerability Type]
- Severity: [Critical/High/Medium/Low]
- Impact: [Brief impact description]

I am committed to working with you to ensure this issue is resolved
before any public disclosure. My suggested timeline is [X] days,
but I am flexible based on the complexity of the fix.

I have attached a detailed report with reproduction steps. Please
confirm receipt and let me know the best way to proceed.

I am available via encrypted email (PGP key attached) or through
[HackerOne/Bugcrowd/Signal].

Best regards,
[Your Name]
[Contact Information]
[PGP Fingerprint]
```

### Follow-up (No Response)

```markdown
Subject: Follow-up: Security Vulnerability Report - [Product Name]

Dear Security Team,

I am following up on my vulnerability report sent on [Date].
I have not received acknowledgment and want to ensure the
report was received.

The vulnerability is [severity level] and affects [scope].
I remain committed to coordinated disclosure but need to
establish communication.

If you are not the correct contact, please forward this to
the appropriate team or provide an alternative contact.

Timeline: [X] days remaining before disclosure deadline.

Best regards,
[Your Name]
```

## Severity Assessment

```yaml
AI-Specific Severity Guidelines:
  CRITICAL:
    examples:
      - "Complete safety bypass enabling harmful content at scale"
      - "Training data extraction with PII"
      - "Remote code execution via model"
      - "Authentication bypass to model"
    cvss_range: "9.0-10.0"
    disclosure_timeline: "45-60 days"

  HIGH:
    examples:
      - "Consistent jailbreak bypass"
      - "System prompt extraction"
      - "Significant model theft risk"
      - "Privilege escalation in agents"
    cvss_range: "7.0-8.9"
    disclosure_timeline: "60-90 days"

  MEDIUM:
    examples:
      - "Partial information disclosure"
      - "Rate limiting bypass"
      - "Inconsistent safety bypass"
      - "Minor model manipulation"
    cvss_range: "4.0-6.9"
    disclosure_timeline: "90-120 days"

  LOW:
    examples:
      - "Verbose error messages"
      - "Minor configuration issues"
      - "Theoretical attacks only"
    cvss_range: "0.1-3.9"
    disclosure_timeline: "120+ days"
```

## Troubleshooting

```yaml
Issue: Vendor not responding
Solution: Try CERT/CC, alternative contacts, consider full disclosure timeline

Issue: Vendor disputes severity
Solution: Provide additional evidence, reference CVSS/OWASP, seek third-party opinion

Issue: Vendor requests extended timeline
Solution: Consider impact, negotiate reasonable extension, document agreement

Issue: Legal threats received
Solution: Consult lawyer, document good faith efforts, contact EFF if needed
```

## Integration Points

| Component | Purpose |
|-----------|---------|
| Agent 01 | Disclosure guidance |
| /report | Report generation |
| HackerOne | Bug bounty submission |
| Legal counsel | Risk assessment |

---

**Practice ethical AI security research through responsible disclosure.**
