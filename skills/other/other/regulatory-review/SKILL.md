---
name: regulatory-review
description: "Use to assess regulatory applicability for products that may fall under AI regulation (EU AI Act, Article 50 transparency)."
instruction_budget: 42
---

# Regulatory Review Skill

Assess whether the product falls under AI regulation and identify compliance requirements.

## When to Use

- At L3 Define->Develop and Develop->Deliver transitions (Regulatory Gate)
- At L4 Develop->Deliver when product_type is `ai_tool`
- At L5 Develop->Deliver for any product with user-facing AI features
- When guardrails G-S7 or G-S8 are triggered

## Workflow

1. **Determine AI presence**: Does this product contain AI/ML components?
   - If no: document "No AI components -- Regulatory Gate N/A" and stop
   - If yes: proceed to classification

2. **EU AI Act risk classification** (Regulation 2024/1689):
   - [ ] Check Annex III high-risk categories:
     - Biometric identification/categorization
     - Critical infrastructure management
     - Education and vocational training (access, assessment)
     - Employment (recruitment, screening, evaluation)
     - Essential services (credit scoring, insurance, social benefits)
     - Law enforcement
     - Migration and border control
     - Justice and democratic processes
   - [ ] Classify risk level: Minimal / Limited / High / Unacceptable

3. **Article 50 transparency check** (applies from 2 August 2026):
   - [ ] Does the system interact directly with people? -> Must disclose AI nature
   - [ ] Does it generate synthetic content? -> Must machine-mark outputs
   - [ ] Does it generate deepfakes? -> Must disclose artificial generation

4. **Product-type-specific checks**:
   - **ai_tool**: Full classification required. Check eval results for bias, safety review for harm potential.
   - **software**: Check if any feature uses AI/ML (recommendations, search, classification). If yes, assess that feature.
   - **content_***: Check if AI generates or curates content shown to users. If yes, transparency disclosure needed.
   - **service_offering**: Check if AI assists in service delivery decisions. If yes, explainability required.

5. **Document findings**:
   - Update `canvas/threat-model.yml` with regulatory classification
   - Update `canvas/privacy-assessment.yml` if data processing is involved
   - Log classification decision in `decision-log.md`

6. **Determine compliance path**:
   - Minimal risk: No action required beyond documentation
   - Limited risk: Transparency obligations (Article 50)
   - High risk: Conformity assessment path must be planned before L4 delivery
   - Unacceptable risk: Product cannot proceed in current form

## Output Format

```
## Regulatory Review: [Product Name]

AI Components: [Yes/No]
Risk Classification: [Minimal/Limited/High/Unacceptable]

### Annex III Assessment
| Category | Applicable? | Rationale |
|----------|------------|-----------|
| Biometric | No | ... |
| Critical infra | No | ... |
| ... | ... | ... |

### Transparency Requirements
- AI disclosure needed: [Yes/No]
- Synthetic content marking: [Yes/No]
- Deepfake disclosure: [Yes/No]

### Compliance Path
[What needs to happen before delivery]

### Decision
Regulatory Gate: [Pass/Fail/N-A]
```

## Important Disclaimer

Mycelium is not a legal compliance tool. This skill raises awareness and prompts assessment of regulatory applicability. For actual compliance decisions, consult qualified legal counsel specializing in AI regulation.

## Theory Citations
- EU AI Act (Regulation 2024/1689)
- Article 50 transparency obligations
- Annex III high-risk categories
