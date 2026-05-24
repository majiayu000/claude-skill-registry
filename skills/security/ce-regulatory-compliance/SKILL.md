---
name: ce-regulatory-compliance
description: >
  Map calibrated_explanations capabilities to EU AI Act, GDPR, AI Liability
  Directive, and Product Liability Directive obligations for compliance documentation
  and presentation materials.
---

# CE Regulatory Compliance

You are mapping calibrated_explanations capabilities to EU regulatory obligations.
This skill covers the EU AI Act, GDPR, AI Liability Directive (AILD), and the
revised Product Liability Directive (PLD) as they apply to ML prediction systems.

**This is NOT legal advice.** This skill provides capability-to-article mappings
based on the library's technical features. Legal interpretation requires qualified
counsel.

Load `references/regulation_capability_map.md` for the full article-to-CE mapping
across all four regulations.

## Required references

- `docs/practitioner/playbooks/eu-ai-act-compliance.md` — canonical compliance guide
- `CITATION.cff` — paper references for mathematical guarantees

## Use this skill when

- Writing or reviewing compliance documentation for a CE-powered system.
- Preparing presentations on CE and regulatory compliance.
- Answering "how does CE satisfy Article X?" questions.
- Identifying gaps where CE alone is insufficient and additional controls are needed.

---

## Quick reference: CE capabilities and their regulatory relevance

| CE capability | Method(s) | Regulatory relevance |
|---|---|---|
| Per-instance factual rules | `explain_factual()`, `print_rules()` | Transparency (AI Act Art. 13), Right to explanation (GDPR Art. 22) |
| Counterfactual alternatives | `explore_alternatives()` | Right to explanation (AI Act Art. 50, GDPR Recital 71) |
| Calibrated probabilities | `predict_proba(uq_interval=True)` | Accuracy declaration (AI Act Art. 15), Risk quantification (Art. 9) |
| Uncertainty intervals | Coverage-guarantee bounds from Venn-Abers/CPS | Robustness documentation (AI Act Art. 15), Burden of proof (AILD Art. 4) |
| Reject/escalation policy | `RejectPolicy.FLAG`, straddle/width gates | Human oversight (AI Act Art. 14) |
| Mondrian calibration | `bins=` parameter on explain/predict | Bias examination (AI Act Art. 10), Non-discrimination (GDPR Art. 22(3)) |
| JSON audit payload | `to_json()`, `to_json_stream()` | Record-keeping (AI Act Art. 12), Technical docs (Art. 11 + Annex IV) |
| Narrative output | `to_narrative(expertise_level=...)` | Plain-language explanation (AI Act Art. 50, GDPR Recital 71) |
| Schema validation | `validate_payload()` | Audit evidence integrity (AI Act Art. 11) |
| Guarded explanations | `explain_guarded_factual()` | OOD detection for production (AI Act Art. 9) |

---

## Regulation-by-regulation overview

### EU AI Act (Regulation (EU) 2024/1689)

The primary regulation. CE maps to 8 articles: Art. 9, 10, 11+Annex IV, 12, 13,
14, 15, and 50. Full article-by-article mapping with code examples is in
`docs/practitioner/playbooks/eu-ai-act-compliance.md`.

**Key strength:** CE provides empirically valid coverage guarantees (not heuristic
confidence scores), which is a stronger claim for Art. 15 accuracy documentation.

### GDPR (Regulation (EU) 2016/679)

Relevant when ML predictions constitute automated individual decision-making:

- **Art. 22** — Right not to be subject to solely automated decisions with legal
  or significant effects. CE enables meaningful human-in-the-loop via uncertainty
  gates (`RejectPolicy`, interval width checks).
- **Art. 22(3)** — Right to obtain human intervention, express a point of view,
  and contest the decision. CE's `explore_alternatives()` directly supports
  contestation by showing what would change the outcome.
- **Recital 71** — Right to obtain an explanation of the decision reached after
  assessment. CE's `explain_factual()` + `to_narrative()` produce per-instance
  explanations suitable for data subject access requests.
- **Art. 35** — Data Protection Impact Assessment (DPIA). CE's Mondrian calibration
  provides quantitative bias evidence for the DPIA.

### AI Liability Directive (AILD — Directive proposal COM/2022/496)

- **Art. 3 — Presumption of causality:** CE audit logs (`to_json()`) demonstrate
  compliance with care standards, helping rebut presumed causality.
- **Art. 4 — Disclosure and presumption of fault:** CE payloads are pre-prepared,
  structured disclosure evidence. Failure to disclose = presumed fault.
- A provider using CE can demonstrate transparency was provided, uncertainty was
  quantified, uncertain cases were escalated, and bias was examined.

### Product Liability Directive (PLD — Directive (EU) 2024/2853)

- **Art. 4(4)** — AI systems are "products." CE outputs are product safety artefacts.
- **Art. 7** — Defectiveness considers safety expectations. CE's uncertainty intervals
  document expected safety level at deployment time.
- **Art. 9(4)** — Disclosure: CE audit payloads serve as pre-prepared evidence.

---

## What CE does NOT cover

| Gap | Regulation | Required additional control |
|---|---|---|
| Data quality certification | AI Act Art. 10(2)(a-e) | Data validation framework (Great Expectations, Soda) |
| Cybersecurity/adversarial robustness | AI Act Art. 15(3-5) | Adversarial testing (ART library), access controls |
| Conformity assessment | AI Act Art. 43-49 | Notified body or internal assessment process |
| Post-market monitoring | AI Act Art. 72 | Drift detection system (Evidently, WhyLabs) |
| Human reviewer training | AI Act Art. 14(4)(a) | Documented training programme |
| DPIA process | GDPR Art. 35 | Legal/DPO-led impact assessment |
| Insurance/liability coverage | AILD | Organisational risk management |
| CE marking declaration | PLD Art. 4 | Regulatory affairs process |

---

## Constraints

- This skill provides capability mappings, not legal advice.
- Always cite specific article numbers when making compliance claims.
- Always cite concrete CE method names when claiming coverage.
- Flag gaps honestly — partial coverage must be stated as such.
- The AILD references are based on the proposed text and may change.
- Refer to `docs/practitioner/playbooks/eu-ai-act-compliance.md` as the canonical
  detailed guide for AI Act compliance.

## Evaluation Checklist

- [ ] Correct regulation(s) identified for the deployment context.
- [ ] CE capabilities mapped to specific articles with method names cited.
- [ ] Gaps identified and documented with required additional controls.
- [ ] Code examples reference actual CE API methods (not hypothetical).
- [ ] Mathematical guarantees (coverage, calibration) cited where relevant to Art. 15.
- [ ] Limitations section included — CE is a technical tool, not a compliance certificate.
