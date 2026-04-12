---
name: privacy-check
description: "Use to assess Privacy by Design compliance and GDPR/data protection alignment for a feature or system."
---

# Privacy Check Skill

Privacy by Design assessment.

## Workflow

### 7 Foundational Principles (Cavoukian)

1. **Proactive not Reactive**: Are privacy measures built in from the start?
   - [ ] Privacy considered in design phase, not bolted on
   - [ ] Risks identified before implementation

2. **Privacy as Default**: Is the most private option the default?
   - [ ] Data collection opt-in, not opt-out
   - [ ] Minimum data collected by default
   - [ ] Sharing disabled by default

3. **Privacy Embedded in Design**: Is privacy integral to the system?
   - [ ] Privacy controls are core features, not add-ons
   - [ ] Architecture supports data minimization

4. **Full Functionality**: Privacy without trade-offs?
   - [ ] Privacy features don't degrade user experience
   - [ ] Not a false choice between privacy and functionality

5. **End-to-End Security**: Data protected throughout its lifecycle?
   - [ ] Encryption at rest and in transit
   - [ ] Secure deletion when no longer needed
   - [ ] Access controls throughout the data lifecycle

6. **Visibility and Transparency**: Is data processing transparent?
   - [ ] Users know what data is collected and why
   - [ ] Processing purposes documented and communicated
   - [ ] Third-party sharing disclosed

7. **Respect for User Privacy**: Are user interests centered?
   - [ ] Users can access their data
   - [ ] Users can correct their data
   - [ ] Users can delete their data
   - [ ] Consent is informed, specific, and revocable

### Data Protection Assessment

- **What data is collected?** List all personal data fields.
- **Why?** Lawful basis for each data element.
- **How long?** Retention period for each data type.
- **Who accesses it?** List all parties with access.
- **Where is it stored?** Data residency and cross-border transfers.
- **How is it protected?** Encryption, access control, monitoring.
- **What if breached?** Incident response plan exists?

### Output

```
## Privacy Assessment: [Feature/System]

### PbD Principles
| Principle | Status | Notes |
|-----------|--------|-------|
| Proactive | Pass/Fail | ... |
| Default privacy | Pass/Fail | ... |
| Embedded | Pass/Fail | ... |
| Full functionality | Pass/Fail | ... |
| End-to-end security | Pass/Fail | ... |
| Transparency | Pass/Fail | ... |
| User respect | Pass/Fail | ... |

### Data Inventory
| Data | Purpose | Basis | Retention | Protection |
|------|---------|-------|-----------|-----------|
| ... | ... | ... | ... | ... |

### Risks and Recommendations
1. [risk and recommended action]
```

## Theory Citations
- Cavoukian: Privacy by Design (7 principles)
- GDPR: Data protection regulation
