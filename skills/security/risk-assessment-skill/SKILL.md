---
skill: 'risk-assessment'
version: '2.0.0'
updated: '2025-12-31'
category: 'risk-compliance'
complexity: 'advanced'
prerequisite_skills: []
composable_with:
  - 'legal-compliance'
  - 'data-sovereignty'
  - 'production-readiness'
  - 'vendor-transition'
---

# Risk Assessment Skill

## Overview
Comprehensive expertise in identifying, analyzing, and mitigating risks associated with AI adoption for vendor replacement, covering security, compliance, business, and operational dimensions.

## Risk Assessment Frameworks

### Risk Identification Matrix

```markdown
## AI Adoption Risk Categories

| Category | Sub-Categories | Priority |
|----------|----------------|----------|
| **Security** | Data exposure, prompt injection, API vulnerabilities | 🔴 High |
| **Compliance** | GDPR, SOC2, HIPAA, industry regulations | 🔴 High |
| **Business** | Vendor lock-in, cost overruns, quality issues | 🟡 Medium |
| **Operational** | Availability, reliability, support | 🟡 Medium |
| **Reputational** | AI errors, bias, customer perception | 🟢 Low |
| **Legal** | IP ownership, liability, contracts | 🟡 Medium |
```

### Risk Scoring Methodology

**Likelihood Scale (1-5):**
- **1 - Rare:** <5% probability, unprecedented
- **2 - Unlikely:** 5-25% probability, has happened elsewhere
- **3 - Possible:** 25-50% probability, common in industry
- **4 - Likely:** 50-75% probability, expected to occur
- **5 - Almost Certain:** >75% probability, will definitely happen

**Impact Scale (1-5):**
- **1 - Negligible:** <$10K cost, no data exposure, minor inconvenience
- **2 - Minor:** $10-50K cost, limited data exposure, short disruption
- **3 - Moderate:** $50-250K cost, moderate exposure, multi-day disruption
- **4 - Major:** $250K-$1M cost, significant exposure, week+ disruption
- **5 - Catastrophic:** >$1M cost, severe breach, existential threat

**Risk Score = Likelihood × Impact**

**Risk Level Interpretation:**
- **1-5 (Low):** Accept and monitor
- **6-12 (Medium):** Mitigate or monitor closely
- **13-20 (High):** Must mitigate before proceeding
- **21-25 (Critical):** Immediate action required, may be show-stopper

### Risk Assessment Template

```markdown
## Risk Assessment: [AI Tool/Use Case]

### Risk #1: [Risk Name]

**Description:** [What could go wrong]

**Likelihood:** [1-5] - [Justification]
**Impact:** [1-5] - [Justification]
**Risk Score:** [L × I] - [Low/Medium/High/Critical]

**Triggers/Indicators:**
- [Early warning sign 1]
- [Early warning sign 2]

**Current Controls:**
- [Existing mitigation if any]

**Mitigation Strategy:**
1. [Action to reduce likelihood or impact]
2. [Action to reduce likelihood or impact]
3. [Monitoring/detection approach]

**Residual Risk:** [Score after mitigation]
**Owner:** [Person/team responsible]
**Status:** [Identified/Mitigated/Accepted/Monitoring]

**Review Date:** [Next assessment date]
```

## Security Risk Assessment

### Data Exposure Risks

**Risk: Confidential Code Sent to AI Services**
- **Likelihood:** 4 (Likely) - developers will paste code naturally
- **Impact:** 4 (Major) - trade secrets, competitive advantage lost
- **Risk Score:** 16 (High)

**Mitigation:**
1. **Technical Controls:**
   - Data loss prevention (DLP) rules
   - Code scanning for secrets before AI submission
   - Approved AI tools only (block consumer tools)
   - Local AI models for sensitive code

2. **Process Controls:**
   - Security training on AI data risks
   - Code review for AI-generated outputs
   - Classification of code (public/internal/confidential)
   - Policy: No confidential code to cloud AI

3. **Monitoring:**
   - API usage auditing
   - Anomaly detection (unusual volumes)
   - Regular access reviews
   - Incident response plan

**Residual Risk:** 8 (Medium) after mitigations

---

**Risk: PII in Prompts**
- **Likelihood:** 3 (Possible) - depends on use case
- **Impact:** 5 (Catastrophic) - regulatory fines, breach notification
- **Risk Score:** 15 (High)

**Mitigation:**
1. **Prevention:**
   - PII detection in prompts (automated scanning)
   - Data masking/anonymization before AI processing
   - Synthetic data for testing/training
   - Strict policy against PII in prompts

2. **Detection:**
   - Prompt logging and auditing
   - PII pattern matching
   - Regular compliance reviews
   - User training and awareness

3. **Response:**
   - Immediate prompt deletion if PII detected
   - Incident reporting procedures
   - Regulatory notification plan
   - Affected individual notification

**Residual Risk:** 6 (Medium) after mitigations

### Adversarial Attack Risks

**Prompt Injection Attack Matrix:**
```markdown
| Attack Type | Example | Likelihood | Impact | Mitigation |
|-------------|---------|------------|--------|------------|
| Direct injection | User adds "ignore previous instructions" | 3 | 3 | Input validation, prompt templates |
| Indirect injection | Malicious content in retrieved documents | 2 | 4 | Content sanitization, output filtering |
| Jailbreaking | Bypass safety guardrails | 2 | 3 | Use providers with strong guardrails |
| Data extraction | Trick AI into revealing training data | 1 | 4 | Use reputable providers, monitor outputs |
```

**Mitigation Strategies:**
- Use prompt templates with fixed structure
- Validate and sanitize all user inputs
- Implement output filtering
- Use role-based prompting
- Monitor for attack patterns
- Regular security testing

### API and Infrastructure Risks

**API Key Exposure:**
- **Prevention:** Use secrets management (Vault, AWS Secrets Manager)
- **Detection:** Scan code repos for hardcoded keys (git-secrets)
- **Response:** Immediate key rotation if exposed
- **Process:** Key rotation schedule (90 days)

**Rate Limiting and Quotas:**
- **Risk:** API limits exceeded during high usage
- **Mitigation:** Monitor usage, set alerts at 80% quota
- **Backup:** Multiple providers or fallback queuing
- **Cost control:** Budget alerts, usage caps

**Service Availability:**
- **Risk:** AI service outage impacts operations
- **Mitigation:** Multi-provider strategy, graceful degradation
- **Monitoring:** Uptime tracking, SLA enforcement
- **Fallback:** Manual process if AI unavailable

## Compliance Risk Assessment

### GDPR Compliance Checklist

```markdown
## GDPR Compliance for AI Tools

### Lawful Basis for Processing
- [ ] Documented lawful basis (consent, contract, legitimate interest)
- [ ] Data processing agreement (DPA) with AI vendor
- [ ] Purpose clearly defined and communicated
- [ ] Processing limited to stated purpose

### Data Subject Rights
- [ ] Right to access: Can retrieve data sent to AI?
- [ ] Right to erasure: Can delete data from AI provider?
- [ ] Right to portability: Can export data?
- [ ] Right to object: Can opt-out of AI processing?
- [ ] Automated decision-making: Humans in the loop?

### Data Protection Principles
- [ ] Data minimization: Only necessary data to AI
- [ ] Purpose limitation: Not using AI data for other purposes
- [ ] Storage limitation: Data retention policies defined
- [ ] Accuracy: Mechanisms to ensure data accuracy
- [ ] Integrity & confidentiality: Encryption, access controls

### Cross-Border Transfers
- [ ] AI vendor location documented (EU, US, other)
- [ ] Transfer mechanism in place (adequacy, SCCs, BCRs)
- [ ] Schrems II compliance for US vendors
- [ ] Data localization requirements met

### Accountability
- [ ] Privacy impact assessment (PIA) completed
- [ ] Records of processing activities maintained
- [ ] Data protection officer (DPO) consulted if required
- [ ] Training provided on GDPR and AI
- [ ] Breach notification procedures ready
```

**GDPR Risk Score:** [Calculate based on checklist completion]
- 100% complete: Low risk
- 80-99%: Medium risk
- <80%: High risk - do not proceed

### SOC2 Compliance Framework

**Trust Service Criteria Mapping:**

```markdown
## SOC2 Controls for AI Adoption

### Security (All AI implementations)
**CC6.1:** Logical and physical access controls
- [ ] API keys stored in secrets management
- [ ] MFA required for AI tool access
- [ ] Role-based access control (RBAC) implemented
- [ ] Access reviews performed quarterly

**CC6.6:** Encryption
- [ ] Data encrypted in transit (TLS 1.2+)
- [ ] Data encrypted at rest (AI provider confirms)
- [ ] Encryption key management documented

**CC7.2:** System monitoring
- [ ] AI usage logging enabled
- [ ] Anomaly detection configured
- [ ] Security event monitoring
- [ ] Incident response plan includes AI systems

### Availability
**A1.2:** System availability
- [ ] AI provider SLA documented (target: 99.9%)
- [ ] Monitoring and alerting configured
- [ ] Backup/fallback procedures defined
- [ ] Disaster recovery plan includes AI dependencies

### Processing Integrity
**PI1.4:** Processing completeness and accuracy
- [ ] AI output validation procedures
- [ ] Quality assurance checks
- [ ] Error handling and logging
- [ ] Human review for critical outputs

### Confidentiality
**C1.1:** Confidentiality controls
- [ ] Data classification applied to AI inputs
- [ ] Confidential data protection measures
- [ ] AI vendor confidentiality agreement signed
- [ ] Access to AI outputs restricted appropriately

### Privacy
**P4.3:** Data retention and disposal
- [ ] AI data retention policy defined
- [ ] Data deletion procedures with AI vendor
- [ ] Regular data disposal verification
- [ ] Compliance with privacy laws
```

### HIPAA Compliance (Healthcare)

**High-Risk Activities (Require BAA):**
- Sending PHI to AI for analysis or processing
- Using AI to generate patient communications
- AI-assisted diagnosis or treatment recommendations
- AI processing of patient records

**HIPAA-Safe AI Usage:**
- Use only HIPAA-compliant AI vendors with signed BAA
- De-identify PHI before AI processing (Safe Harbor or Expert Determination)
- Encrypt all PHI in transit and at rest
- Maintain audit logs of all PHI access
- Implement access controls and authentication
- Regular security risk assessments
- Breach notification procedures

**HIPAA Compliance Checklist:**
```markdown
- [ ] AI vendor is HIPAA-compliant (verify)
- [ ] Business Associate Agreement (BAA) signed
- [ ] Risk assessment completed and documented
- [ ] PHI de-identification process defined
- [ ] Encryption standards met (AES-256, TLS 1.2+)
- [ ] Audit logging configured and monitored
- [ ] Access controls implemented (RBAC, MFA)
- [ ] Breach notification plan includes AI systems
- [ ] Staff training on HIPAA and AI completed
- [ ] Regular compliance audits scheduled
```

## Business Risk Assessment

### Vendor Lock-in Risk Analysis

**Lock-in Risk Factors:**
```markdown
| Factor | Low Risk (1-2) | Medium Risk (3) | High Risk (4-5) | Score |
|--------|---------------|-----------------|-----------------|-------|
| **Data Portability** | Easy export | Some friction | Vendor-specific format | |
| **API Proprietary** | Standard APIs | Custom but documented | Fully proprietary | |
| **Training Data** | You own it | Shared ownership | Vendor owns it | |
| **Integration Depth** | Shallow, easily replaced | Moderate integration | Deep, hard to replace | |
| **Cost to Switch** | <$10K | $10-50K | >$50K | |
| **Feature Dependency** | Use basic features | Some unique features | Heavily dependent on unique | |
| **Contract Terms** | Month-to-month | Annual | Multi-year | |

**Total Lock-in Score:** [Sum / 35]
- 7-14: Low lock-in risk
- 15-24: Medium lock-in risk
- 25-35: High lock-in risk
```

**Mitigation Strategies:**
- **Multi-provider strategy:** Use multiple AI vendors for redundancy
- **Abstraction layer:** Build wrapper APIs to make switching easier
- **Data ownership:** Ensure contract grants you full data ownership
- **Exit planning:** Document migration path before full adoption
- **Avoid long contracts:** Prefer month-to-month or annual

### Quality and Reliability Risks

**AI Hallucination Risk:**
- **Use Cases Most at Risk:** Technical documentation, code generation, data analysis
- **Mitigation:**
  - Human review of all AI outputs
  - Validation against source truth
  - Confidence scoring where available
  - Testing and verification procedures
  - Clear labeling of AI-generated content

**Model Degradation:**
- **Risk:** AI provider updates model, quality drops
- **Mitigation:**
  - Pin to specific model versions where possible
  - Test new versions before switching
  - Monitor quality metrics continuously
  - Fallback to previous version if needed
  - Contract terms about version control

### Cost Overrun Risks

**Cost Risk Assessment:**
```markdown
## AI Cost Overrun Analysis

### Usage Uncertainty
**Risk:** Actual usage exceeds estimates
- Projected usage: [X] tokens/month
- Worst case usage: [Y] tokens/month (2-3x)
- Budget buffer: [Z]% recommended: 50-100%

### Pricing Changes
**Risk:** Vendor changes pricing model
- Current pricing: $[X] per [unit]
- Historical changes: [Track vendor pricing history]
- Contract protection: Price lock for [duration]?
- Multi-provider backup: Alternative pricing available

### Hidden Costs
- Integration and setup: $[X] (one-time)
- Training and adoption: $[Y] (one-time)
- Monitoring and management: $[Z]/month (ongoing)
- Quality assurance: $[W]/month (ongoing)
- Unexpected overage charges: $[V] (buffer)

### Cost Control Measures
- [ ] Usage monitoring and alerts
- [ ] Budget caps and quotas
- [ ] Approval for high-cost operations
- [ ] Regular cost reviews (monthly)
- [ ] Optimization opportunities identified
```

## Operational Risk Assessment

### Availability and Reliability

**Service Availability Risk Matrix:**
```markdown
| Scenario | Likelihood | Impact | Mitigation | RPO/RTO |
|----------|------------|--------|------------|---------|
| Planned maintenance | High (monthly) | Low | Schedule off-hours, notification | 2h / 4h |
| Unplanned outage | Medium (quarterly) | Medium | Fallback provider, queue | 1h / 8h |
| Regional outage | Low (annual) | High | Multi-region deployment | 15m / 4h |
| Vendor bankruptcy | Very Low | Critical | Data export, alternative ready | N/A / 2 weeks |
```

**Disaster Recovery Plan:**
1. **Detection:** Automated monitoring alerts within 5 minutes
2. **Assessment:** Determine scope and estimated duration (15 minutes)
3. **Communication:** Notify stakeholders of impact (30 minutes)
4. **Mitigation:** Activate fallback (manual process or alternate provider)
5. **Recovery:** Resume normal operations when service restored
6. **Post-mortem:** Document incident and improve resilience

### Support and Escalation Risks

**Support Tier Assessment:**
```markdown
| Vendor Support Level | Response Time | Suitable For | Risk Level |
|---------------------|---------------|--------------|------------|
| Community only | Days-weeks | Non-critical, learning | High |
| Email support | 24-48 hours | Low-priority use cases | Medium |
| Business support | 4-8 hours | Standard production use | Medium |
| Enterprise support | 1-4 hours | Critical production use | Low |
| Dedicated TAM | <1 hour | Mission-critical | Low |
```

**Recommendation:** Match support tier to use case criticality

## Risk Mitigation Strategies

### Defense in Depth Approach

**Layer 1: Prevention**
- Security controls (encryption, access control)
- Policy and training
- Tool selection and vetting
- Secure integration patterns

**Layer 2: Detection**
- Monitoring and logging
- Anomaly detection
- Regular audits
- Compliance scanning

**Layer 3: Response**
- Incident response procedures
- Escalation paths
- Containment actions
- Communication plans

**Layer 4: Recovery**
- Backup and fallback procedures
- Data restoration
- Service resumption
- Post-incident review

### Continuous Risk Monitoring

**Risk Dashboard Template:**
```markdown
## AI Risk Dashboard - [Month/Year]

### Overall Risk Status: 🟡 Medium

| Risk Category | Open Risks | Mitigated | Accepted | Trend |
|---------------|-----------|-----------|----------|-------|
| Security | 3 | 12 | 2 | ↓ Improving |
| Compliance | 1 | 8 | 0 | → Stable |
| Business | 4 | 6 | 3 | ↑ Increasing |
| Operational | 2 | 10 | 1 | → Stable |

### Top 5 Current Risks
1. [Risk name] - Score: [X] - Owner: [Y] - Due: [Date]
2. [Risk name] - Score: [X] - Owner: [Y] - Due: [Date]
3. [Risk name] - Score: [X] - Owner: [Y] - Due: [Date]
4. [Risk name] - Score: [X] - Owner: [Y] - Due: [Date]
5. [Risk name] - Score: [X] - Owner: [Y] - Due: [Date]

### Recent Changes
- New risk identified: [Description]
- Risk mitigated: [Description]
- Risk escalated: [Description]

### Action Items
- [ ] [Action for risk X]
- [ ] [Action for risk Y]
- [ ] [Action for risk Z]
```

**Review Cadence:**
- **Weekly:** Operational risks and incidents
- **Monthly:** All risk categories, dashboard update
- **Quarterly:** Risk assessment refresh, controls testing
- **Annually:** Comprehensive risk review, framework update

## Risk Assessment Best Practices

### Do's
✅ Assess risks before procurement decisions
✅ Involve security, legal, compliance early
✅ Document all risks and mitigation plans
✅ Monitor continuously, not just at start
✅ Update assessments as AI usage evolves
✅ Be realistic about likelihood and impact
✅ Have layered defenses (prevention + detection + response)
✅ Plan for worst-case scenarios

### Don'ts
❌ Skip risk assessment to move faster
❌ Downplay risks to get approval
❌ Ignore compliance requirements
❌ Assume vendor is secure without verification
❌ Use consumer AI tools for enterprise data
❌ Forget about insider threats
❌ Neglect incident response planning
❌ Set and forget - risks change over time

This skill ensures AI adoption proceeds with eyes wide open to risks, with appropriate mitigation strategies in place.
