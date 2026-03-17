---
name: standards-compliance-training
description: Align training to regulatory compliance requirements including OSHA, FDA, HIPAA, SOX, GDPR, and industry-specific regulations. Verify compliance coverage and identify gaps. Use for mandated compliance training. Activates on "OSHA", "compliance training", "regulatory requirements", or "mandated training".
---

# Standards: Compliance Training

Align corporate training to regulatory compliance requirements and industry standards.

## When to Use

- Creating compliance training programs
- Regulatory requirement verification
- Industry certification training
- Audit preparation
- Legal compliance documentation

## Major Regulatory Areas

### Workplace Safety

**OSHA (Occupational Safety and Health Administration)**:
- General Industry (29 CFR 1910)
- Construction (29 CFR 1926)
- Maritime (29 CFR 1915-1918)

**Required Training Topics**:
- Hazard Communication (HazCom/GHS)
- Personal Protective Equipment (PPE)
- Lockout/Tagout (LOTO)
- Confined Spaces
- Fall Protection
- Electrical Safety
- Bloodborne Pathogens
- Emergency Action Plans

**Documentation Requirements**:
- Training records (name, date, trainer, topic)
- Certificates of completion
- Competency verification

### Healthcare Compliance

**HIPAA (Health Insurance Portability and Accountability Act)**:
- Privacy Rule training
- Security Rule requirements
- Breach notification
- Annual training required

**OSHA Healthcare Standards**:
- Bloodborne Pathogens Standard
- TB exposure control
- Workplace violence prevention

**FDA Regulations** (pharmaceutical/medical device):
- GMP (Good Manufacturing Practices)
- GCP (Good Clinical Practices)
- 21 CFR Part 11 (electronic records)

### Financial Services

**SOX (Sarbanes-Oxley Act)**:
- Internal controls
- Financial reporting
- Auditor independence

**FINRA Regulations**:
- Securities training requirements
- Continuing education (Regulatory Element, Firm Element)
- AML (Anti-Money Laundering)

**Dodd-Frank Act**:
- Whistleblower protection
- Risk management

### Data Privacy

**GDPR (General Data Protection Regulation)**:
- Data protection principles
- Individual rights
- Data breach procedures
- DPO responsibilities

**CCPA/CPRA (California Privacy)**:
- Consumer rights
- Data handling procedures
- Privacy notices

**HIPAA** (covered above)

**PCI-DSS** (Payment Card Industry):
- Data security training
- Secure handling procedures

### Environmental

**EPA Regulations**:
- Hazardous waste management
- Air quality compliance
- Water discharge
- Spill prevention

**ISO 14001** (Environmental Management):
- Environmental aspects training
- EMS awareness

### Quality Management

**ISO 9001** (Quality Management):
- Quality awareness training
- Process documentation
- Corrective actions

**AS9100** (Aerospace):
- Configuration management
- First article inspection

### Food Safety

**FDA Food Safety**:
- HACCP (Hazard Analysis Critical Control Points)
- Food defense
- Allergen management
- FSMA (Food Safety Modernization Act)

### Information Security

**ISO 27001**:
- Information security awareness
- Access control
- Incident response

**NIST Cybersecurity Framework**:
- Identify, Protect, Detect, Respond, Recover

**Industry-Specific**:
- NERC CIP (power grid)
- CMMC (defense contractors)

## Compliance Mapping Process

### 1. Identify Applicable Regulations

**By Industry**:
- Manufacturing: OSHA, EPA, ISO
- Healthcare: HIPAA, OSHA Bloodborne Pathogens, FDA
- Finance: SOX, FINRA, AML
- Technology: ISO 27001, GDPR, SOC 2

### 2. Extract Training Requirements

**Regulatory Text Analysis**:
- Identify "shall," "must," "required"
- Extract frequency requirements (annual, biennial, ongoing)
- Note documentation requirements
- Identify competency validation needs

### 3. Map Training to Requirements

**Coverage Matrix**:
- Regulation citation
- Training requirement
- Course module
- Assessment method
- Frequency
- Record keeping

### 4. Validate Sufficiency

**Ensure**:
- All requirements covered
- Appropriate depth
- Competency demonstration
- Documentation adequate for audit

## CLI Interface

```bash
# OSHA compliance check
/standards.compliance-training --training "safety-program/" --regulation "OSHA-1910" --industry "manufacturing"

# Healthcare compliance
/standards.compliance-training --program "hospital-orientation/" --regulations "HIPAA,OSHA-Bloodborne" --validate

# Financial services
/standards.compliance-training --content "finra-training/" --regulations "FINRA-CE,AML,SOX" --gap-analysis

# Multi-regulation audit
/standards.compliance-training --full-audit --company-training "/" --industry "healthcare" --regulations "all-applicable"

# Generate compliance documentation
/standards.compliance-training --training "programs/" --regulation "OSHA" --generate-audit-report
```

## Output

- Compliance requirements checklist
- Training coverage map
- Gap analysis with recommendations
- Audit-ready documentation
- Training record templates
- Compliance certificate templates

## Composition

**Input from**: `/learning.training-needs`, `/curriculum.develop-content`
**Works with**: `/standards.coverage-validator`, `/standards.compliance-documentation`
**Output to**: Compliance-verified training programs

## Exit Codes

- **0**: Compliance validated
- **1**: Critical requirements not met
- **2**: Documentation insufficient
- **3**: Regulation not supported
