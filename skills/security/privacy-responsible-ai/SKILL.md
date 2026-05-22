---
name: "Privacy & Responsible AI Skill"
description: "Privacy by design, data protection, and responsible AI principles."
applyTo: "**/*privacy*,**/*consent*,**/*data*,**/*PII*,**/*GDPR*,**/*responsible*,**/*ethical*,**/*bias*,**/*fairness*"
---

# Privacy & Responsible AI Skill

> Privacy by design, data protection, and responsible AI principles.

## ⚠️ Staleness Warning

Privacy regulations and AI ethics guidelines evolve continuously.

**Refresh triggers:**

- New privacy laws (state, country, region)
- AI regulation updates (EU AI Act, etc.)
- Industry standard changes
- Major incident learnings
- Annual transparency reports (Microsoft, Google)

**Last validated:** February 2026 (EU AI Act prohibitions active Aug 2025, GDPR/CCPA current)

**Check current state:** [Microsoft RAI](https://www.microsoft.com/en-us/ai/responsible-ai), [Google AI Principles](https://ai.google/responsibility/responsible-ai-practices/), [GDPR](https://gdpr.eu/), [CCPA](https://oag.ca.gov/privacy/ccpa), [EU AI Act](https://digital-strategy.ec.europa.eu/en/policies/regulatory-framework-ai)

---

## Privacy by Design Principles

| Principle | Implementation |
| --------- | -------------- |
| **Minimize** | Collect only what's needed |
| **Purpose** | Use data only for stated purpose |
| **Consent** | Get explicit permission |
| **Access** | Let users see their data |
| **Deletion** | Let users delete their data |
| **Security** | Protect data at rest and in transit |
| **Transparency** | Explain what you collect and why |

## Data Classification

| Level | Examples | Handling |
| ----- | -------- | -------- |
| **Public** | Marketing content | No restrictions |
| **Internal** | Employee directory | Internal only |
| **Confidential** | Customer data, PII | Encrypted, access-controlled |
| **Restricted** | Credentials, health data | Maximum protection |

## PII Checklist

Personal Identifiable Information includes:

- [ ] Names
- [ ] Email addresses
- [ ] Phone numbers
- [ ] Physical addresses
- [ ] IP addresses
- [ ] Device IDs
- [ ] Location data
- [ ] Financial data
- [ ] Health data
- [ ] Biometric data

---

## Responsible AI Principles

### Microsoft's 6 Principles (2025 RAI Transparency Report)

| Principle | Question to Ask | Implementation |
| --------- | --------------- | -------------- |
| **Fairness** | Does it treat all groups equitably? | Bias testing, diverse datasets, fairness metrics |
| **Reliability & Safety** | Does it work consistently and safely? | Testing, monitoring, failure modes, guardrails |
| **Privacy & Security** | Does it protect user data? | Data minimization, encryption, access controls |
| **Inclusiveness** | Does it work for everyone? | Accessibility, diverse user testing, edge cases |
| **Transparency** | Can users understand how it works? | Explainability, documentation, model cards |
| **Accountability** | Who is responsible for outcomes? | Human oversight, audit trails, governance |

### Google's 3 Pillars (2024 AI Responsibility Report)

| Pillar | Description |
| ------ | ----------- |
| **Bold Innovation** | Deploy AI where benefits substantially outweigh risks |
| **Responsible Development** | Human oversight, safety research, bias mitigation, privacy |
| **Collaborative Progress** | Enable ecosystem, share learnings, engage stakeholders |

### Key RAI Tools & Frameworks

| Tool | Purpose | Source |
| ---- | ------- | ------ |
| **HAX Workbook** | Human-AI interaction best practices | Microsoft |
| **Responsible AI Dashboard** | End-to-end RAI experience | Microsoft/Azure |
| **Model Cards** | Structured model documentation | Google |
| **People + AI Guidebook** | Design guidance for AI products | Google PAIR |
| **Frontier Safety Framework** | Advanced model risk management | Google |

---

## Bias Detection

```text
Ask:
1. What data was the model trained on?
2. Are there underrepresented groups?
3. What are the failure modes?
4. Who might be harmed by errors?
5. Have we tested with diverse inputs?
6. What demographic slices show performance gaps?
7. Are there proxy variables that encode bias?
```

### Bias Categories

| Type | Description | Example |
| ---- | ----------- | ------- |
| **Selection Bias** | Training data not representative | Hiring model trained only on past hires |
| **Measurement Bias** | Flawed data collection | Self-reported data with social desirability |
| **Algorithmic Bias** | Model amplifies patterns | Recommendation loops |
| **Presentation Bias** | UI choices influence perception | Image ordering in search results |

---

## AI Transparency & Documentation

### Model Card Template

```markdown
## Model Card: [Model Name]

### Model Details
- **Developer**: [Organization]
- **Version**: [Version number]
- **Type**: [Classification/Generation/etc.]
- **License**: [License terms]

### Intended Use
- **Primary use cases**: [Description]
- **Out-of-scope uses**: [What NOT to use it for]
- **Users**: [Target users]

### Training Data
- **Sources**: [Data sources]
- **Size**: [Dataset size]
- **Known limitations**: [Data gaps]

### Performance
- **Metrics**: [Evaluation metrics]
- **Sliced analysis**: [Performance by demographic groups]
- **Failure modes**: [Known failure patterns]

### Ethical Considerations
- **Risks**: [Potential harms]
- **Mitigations**: [Steps taken]
- **Human oversight**: [Review processes]
```

### AI Feature Transparency (User-Facing)

```markdown
## How This AI Works

**What it does**: [Clear description]
**What it doesn't do**: [Limitations]
**Data used**: [What inputs, how stored]
**Human oversight**: [When humans review]
**How to appeal**: [Process for disputes]
**Confidence indicators**: [How certainty is communicated]
```

---

## Human-AI Collaboration

### Appropriate Reliance Framework

| State | Description | Signal |
| ----- | ----------- | ------ |
| **Over-reliance** | Blind acceptance | User never questions AI |
| **Appropriate reliance** | Calibrated trust | User verifies when uncertain |
| **Under-reliance** | Excessive skepticism | User ignores useful AI output |

### Design for Appropriate Reliance

1. **Show confidence levels** — Don't present all outputs as equally certain
2. **Explain reasoning** — Help users evaluate AI logic
3. **Enable challenge** — Make it easy to question or override
4. **Provide alternatives** — Show multiple options when available
5. **Track calibration** — Monitor if users trust appropriately

## Code Patterns

### Don't Log PII

```typescript
// Bad
console.log(`User ${email} logged in`);

// Good
console.log(`User ${hashUserId(userId)} logged in`);
```

### Consent Before Collection

```typescript
// Get explicit consent
const consent = await showConsentDialog({
    purpose: 'Improve recommendations',
    data: ['usage patterns', 'preferences'],
    retention: '90 days',
    optOut: 'Settings > Privacy'
});

if (!consent.granted) {
    return fallbackBehavior();
}
```

### Data Minimization

```typescript
// Bad: Store everything
saveUser({ ...fullUserObject });

// Good: Store only what's needed
saveUser({
    id: user.id,
    preferences: user.preferences
    // Don't store: email, name, location
});
```

### Right to Deletion

```typescript
async function deleteUserData(userId: string) {
    await db.users.delete(userId);
    await db.userPreferences.delete(userId);
    await db.userHistory.delete(userId);
    await analytics.purge(userId);
    await logs.redact(userId);

    return { deleted: true, timestamp: new Date() };
}
```

## Regulatory Quick Reference

| Regulation | Region | Key Requirements |
| ---------- | ------ | ---------------- |
| GDPR | EU | Consent, access, deletion, breach notification |
| CCPA/CPRA | California | Disclosure, opt-out, deletion |
| LGPD | Brazil | Similar to GDPR |
| PIPL | China | Data localization, consent |
| HIPAA | US Healthcare | Health data protection |
| **EU AI Act** | EU | Risk-based classification; prohibited AI systems banned Aug 2025; GPAI (general-purpose AI) rules apply 2025+; full obligations for high-risk AI by Aug 2026 |

### EU AI Act Risk Tiers (Active 2025+)

| Tier | Examples | Status |
| ---- | -------- | ------ |
| **Unacceptable Risk** (prohibited) | Social scoring, real-time biometric surveillance | Banned since Aug 2, 2025 |
| **High Risk** | Employment AI, credit scoring, medical devices | Conformity assessment + registration required |
| **Limited Risk** | Chatbots, deepfakes | Transparency obligations (must disclose AI) |
| **Minimal Risk** | Spam filters, AI games | No mandatory requirements |

**For AI product builders**: Check if your AI system classifies as "high risk" — if yes, you need a risk management system, data governance plan, human oversight mechanisms, and EU registration before market launch (deadline: Aug 2026).

## AI Incident Response

When AI causes harm:

1. **Stop** — Disable the feature immediately
2. **Assess** — Who was affected, how severely
3. **Notify** — Inform affected users
4. **Fix** — Root cause + prevention
5. **Document** — Post-mortem for learning

## Synapses

See [synapses.json](synapses.json) for connections.
