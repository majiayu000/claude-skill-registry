---
name: ai-ethics-compliance
description: Assessing Bias, Fairness, Transparency, and Legal (EU AI Act, GDPR).
role: prod-ethicist
triggers:
  - ethics check
  - bias review
  - eu ai act
  - gdpr
  - fairness
  - transparency
---

# ai-ethics-compliance Skill

This skill ensures the system respects human rights and legal frameworks.

## 1. Regulatory Checklist (EU AI Act / GDPR)
- **Transparency**: Does the user know they are interacting with AI? (Art 52).
- **Explanation**: Can we explain *why* the AI made a decision? (Right to Explanation).
- **Data Rights**: Can the user request their data be deleted? (Right to be Forgotten).
- **Risk Category**: Is this "High Risk" (CV recruitment, credit scoring)? If yes, Conformity Assessment required.

## 2. Bias Testing
- **Demographic Parity**: Does the model perform equally well for all groups?
- **Dataset Audit**: scan training/RAG data for stereotypes or under-representation.
- **Proxy Variables**: Are we using "Zip Code" as a proxy for race?

## 3. Dark Pattern Prevention
- **Addiction Loops**: Are we exploiting dopamine triggers?
- **Manipulation**: Are we tricking the user into consent?
- **Privacy Zuckering**: Making it hard to manage privacy settings.

## 4. The "Newspaper Test"
- If this feature's logic was published on the front page of the NYT, would we be ashamed?
