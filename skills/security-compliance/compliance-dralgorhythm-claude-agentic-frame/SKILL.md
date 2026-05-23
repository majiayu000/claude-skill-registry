---
name: compliance
description: Ensure regulatory compliance. Use when implementing GDPR, HIPAA, PCI-DSS, or SOC2 requirements. Covers compliance frameworks and controls.
allowed-tools: Read, Write, Glob, Grep
---

# Compliance

## Common Frameworks

### GDPR (General Data Protection Regulation)
EU data protection regulation.

**Key Requirements**:
- Lawful basis for processing
- Data minimization
- Right to erasure
- Data portability
- Breach notification (72 hours)
- Privacy by design

### HIPAA (Health Insurance Portability and Accountability Act)
US healthcare data protection.

**Key Requirements**:
- Access controls
- Audit controls
- Integrity controls
- Transmission security
- Business Associate Agreements

### PCI-DSS (Payment Card Industry Data Security Standard)
Payment card data protection.

**Key Requirements**:
- Network segmentation
- Encryption of cardholder data
- Access restrictions
- Regular testing
- Security policies

### SOC 2 (Service Organization Control 2)
Trust service criteria.

**Principles**:
- Security
- Availability
- Processing Integrity
- Confidentiality
- Privacy

## Common Controls

### Access Control
```markdown
- [ ] Unique user IDs
- [ ] Strong authentication
- [ ] Role-based access
- [ ] Regular access reviews
- [ ] Termination procedures
```

### Data Protection
```markdown
- [ ] Encryption at rest
- [ ] Encryption in transit
- [ ] Key management
- [ ] Data classification
- [ ] Retention policies
```

### Audit & Monitoring
```markdown
- [ ] Audit logging enabled
- [ ] Log retention (1+ year)
- [ ] Regular log review
- [ ] Alerting on anomalies
- [ ] Incident response plan
```

### Documentation
```markdown
- [ ] Security policies
- [ ] Procedures documented
- [ ] Evidence collection
- [ ] Regular reviews
- [ ] Training records
```

## Compliance Checklist

| Control | GDPR | HIPAA | PCI | SOC2 |
|---------|------|-------|-----|------|
| Encryption | Yes | Yes | Yes | Yes |
| Access Control | Yes | Yes | Yes | Yes |
| Audit Logging | Yes | Yes | Yes | Yes |
| Breach Notification | Yes | Yes | Yes | Yes |
| Risk Assessment | Yes | Yes | Yes | Yes |
