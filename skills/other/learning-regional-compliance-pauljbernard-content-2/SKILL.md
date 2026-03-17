---
name: learning-regional-compliance
description: Validate compliance with regional data privacy laws (GDPR, CCPA, PIPEDA), accessibility requirements, age-appropriate content regulations, and copyright laws by jurisdiction. Use when ensuring legal compliance across regions. Activates on "GDPR", "data privacy", "regional compliance", or "legal requirements".
---

# Learning Regional Compliance

Validate educational content and systems comply with regional data privacy, accessibility, age-appropriateness, and copyright laws.

## When to Use

- Launching learning platforms in new regions
- Handling learner data across jurisdictions
- Age-restricted content verification
- International copyright compliance
- Accessibility law compliance

## Key Compliance Areas

### 1. Data Privacy Regulations

**GDPR (European Union)**:
- Consent requirements for learner data
- Right to access and erasure
- Data minimization principles
- Cross-border data transfer restrictions
- Data protection impact assessments (DPIA)
- Age of consent: 16 (13-16 with parental consent per member state)

**CCPA (California)**:
- Consumer rights to know, delete, opt-out
- Sale of personal information restrictions
- Age restrictions: Under 13, 13-16 consent rules
- Student data special protections

**PIPEDA (Canada)**:
- Consent for collection, use, disclosure
- Individual access rights
- Accountability principle
- Provincial variations (Quebec, BC, Alberta)

**LGPD (Brazil)**:
- Similar to GDPR
- Data controller and processor responsibilities
- Age of consent: 12 years

**Other Regional Laws**:
- POPIA (South Africa)
- PDPA (Singapore, Thailand)
- APPI (Japan)

### 2. Educational Data Protection

**US: FERPA (Family Educational Rights and Privacy Act)**:
- Student education records protection
- Parental access rights
- Directory information rules

**US: COPPA (Children's Online Privacy Protection Act)**:
- Under 13 years old protections
- Verifiable parental consent required
- Data collection limitations

**EU: Student Data Directive**:
- Special protections for minors
- School responsibility for data processors

### 3. Accessibility Regulations

**Regional Standards**:
- **US**: Section 508, ADA
- **EU**: EN 301 549, Web Accessibility Directive
- **UK**: Equality Act 2010
- **Canada**: AODA (Ontario), ACA (Canada)
- **Australia**: DDA (Disability Discrimination Act)

**Requirements**:
- WCAG 2.1 AA minimum (EU requires AA)
- Accessible purchasing (EU)
- Public sector requirements
- Educational institution obligations

### 4. Age-Appropriate Content

**Age Ratings by Region**:
- **US**: ESRB (games), TV-PG/TV-MA (video)
- **EU**: PEGI (games), FSK (Germany), BBFC (UK)
- **Australia**: ACB classifications
- **South Korea**: GRAC ratings

**Content Restrictions**:
- Violence depictions
- Sexual content
- Language/profanity
- Substance use
- Gambling references

### 5. Copyright and Fair Use

**Regional Differences**:
- **US**: Fair use (4-factor test)
- **UK/Commonwealth**: Fair dealing (more limited)
- **EU**: Copyright Directive, DSM Directive
- **Canada**: Fair dealing + education exemptions

**Educational Exceptions**:
- Classroom use provisions
- Distance learning considerations
- Copying limits by jurisdiction
- Attribution requirements

## Compliance Checklist

### Data Privacy Compliance

- [ ] Cookie consent mechanism
- [ ] Privacy policy localized
- [ ] Data processing agreements with vendors
- [ ] Right to access mechanism
- [ ] Right to erasure mechanism
- [ ] Age verification system
- [ ] Parental consent workflow
- [ ] Data breach notification procedure
- [ ] Cross-border transfer safeguards

### Accessibility Compliance

- [ ] WCAG 2.1 AA conformance
- [ ] Accessibility statement published
- [ ] Alternative formats available
- [ ] Keyboard navigation complete
- [ ] Screen reader testing completed
- [ ] Captions and transcripts for media
- [ ] Color contrast validated

### Content Compliance

- [ ] Age rating assigned
- [ ] Content warnings provided
- [ ] Regional sensitivities addressed
- [ ] Copyright clearances obtained
- [ ] Attributions provided
- [ ] Fair use justifications documented

## CLI Interface

```bash
# GDPR compliance check
/learning.regional-compliance --content "lms-platform/" --regulation "GDPR" --jurisdiction "EU"

# Multi-region validation
/learning.regional-compliance --platform "online-course/" --regions "EU,US-CA,Canada,Brazil"

# Age-appropriate content check
/learning.regional-compliance --content "video-course/" --age-rating --regions "US,UK,Australia"

# Copyright compliance
/learning.regional-compliance --materials "course-content/" --copyright-check --jurisdictions "US,UK,Canada"

# Generate compliance report
/learning.regional-compliance --full-audit --platform "learning-app/" --target-regions "EU,US,APAC"
```

## Output

- Compliance validation report
- Gap analysis with recommendations
- Required policy documents
- Implementation checklist
- Risk assessment
- Remediation roadmap

## Composition

**Input from**: `/curriculum.package-lms`, `/curriculum.package-web`, `/learning.global-accessibility`
**Works with**: `/learning.cultural-adaptation`, `/curriculum.review-accessibility`
**Output to**: Compliance documentation, legal requirements

## Exit Codes

- **0**: Compliance validated
- **1**: Critical compliance violations found
- **2**: Missing required documentation
- **3**: Unsupported jurisdiction
