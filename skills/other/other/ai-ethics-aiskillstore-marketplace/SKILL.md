---
name: ai-ethics
description: Responsible AI development and ethical considerations. Use when evaluating
  AI bias, implementing fairness measures, conducting ethical assessments, or ensuring
  AI systems align with human values.
author: Joseph OBrien
status: unpublished
updated: '2025-12-23'
version: 1.0.1
tag: skill
type: skill
---

# AI Ethics

Comprehensive AI ethics skill covering bias detection, fairness assessment, responsible AI development, and regulatory compliance.

## When to Use This Skill

- Evaluating AI models for bias
- Implementing fairness measures
- Conducting ethical impact assessments
- Ensuring regulatory compliance (EU AI Act, etc.)
- Designing human-in-the-loop systems
- Creating AI transparency documentation
- Developing AI governance frameworks

## Ethical Principles

### Core AI Ethics Principles

| Principle | Description |
|-----------|-------------|
| **Fairness** | AI should not discriminate against individuals or groups |
| **Transparency** | AI decisions should be explainable |
| **Privacy** | Personal data must be protected |
| **Accountability** | Clear responsibility for AI outcomes |
| **Safety** | AI should not cause harm |
| **Human Agency** | Humans should maintain control |

### Stakeholder Considerations

- **Users**: How does this affect people using the system?
- **Subjects**: How does this affect people the AI makes decisions about?
- **Society**: What are broader societal implications?
- **Environment**: What is the environmental impact?

## Bias Detection & Mitigation

### Types of AI Bias

| Bias Type | Source | Example |
|-----------|--------|---------|
| Historical | Training data reflects past discrimination | Hiring models favoring male candidates |
| Representation | Underrepresented groups in training data | Face recognition failing on darker skin |
| Measurement | Proxy variables for protected attributes | ZIP code correlating with race |
| Aggregation | One model for diverse populations | Medical model trained only on one ethnicity |
| Evaluation | Biased evaluation metrics | Accuracy hiding disparate impact |

### Fairness Metrics

**Group Fairness:**

- Demographic Parity: Equal positive rates across groups
- Equalized Odds: Equal TPR and FPR across groups
- Predictive Parity: Equal precision across groups

**Individual Fairness:**

- Similar individuals should receive similar predictions
- Counterfactual fairness: Would outcome change if protected attribute differed?

### Bias Mitigation Strategies

**Pre-processing:**

- Resampling/reweighting training data
- Removing biased features
- Data augmentation for underrepresented groups

**In-processing:**

- Fairness constraints in loss function
- Adversarial debiasing
- Fair representation learning

**Post-processing:**

- Threshold adjustment per group
- Calibration
- Reject option classification

## Explainability & Transparency

### Explanation Types

| Type | Audience | Purpose |
|------|----------|---------|
| Global | Developers | Understand overall model behavior |
| Local | End users | Explain specific decisions |
| Counterfactual | Affected parties | What would need to change for different outcome |

### Explainability Techniques

- **SHAP**: Feature importance values
- **LIME**: Local interpretable explanations
- **Attention maps**: For neural networks
- **Decision trees**: Inherently interpretable
- **Feature importance**: Global model understanding

### Model Cards

Document for each model:

- Model purpose and intended use
- Training data description
- Performance metrics by subgroup
- Limitations and ethical considerations
- Version and update history

## AI Governance

### AI Risk Assessment

**Risk Categories (EU AI Act):**

| Risk Level | Examples | Requirements |
|------------|----------|--------------|
| Unacceptable | Social scoring, manipulation | Prohibited |
| High | Healthcare, employment, credit | Strict requirements |
| Limited | Chatbots | Transparency obligations |
| Minimal | Spam filters | No requirements |

### Governance Framework

1. **Policy**: Define ethical principles and boundaries
2. **Process**: Review and approval workflows
3. **People**: Roles and responsibilities (ethics board)
4. **Technology**: Tools for monitoring and enforcement

### Documentation Requirements

- Data provenance and lineage
- Model training documentation
- Testing and validation results
- Deployment and monitoring plans
- Incident response procedures

## Human Oversight

### Human-in-the-Loop Patterns

| Pattern | Use Case | Example |
|---------|----------|---------|
| Human-in-the-Loop | High-stakes decisions | Medical diagnosis confirmation |
| Human-on-the-Loop | Monitoring with intervention | Content moderation escalation |
| Human-out-of-Loop | Low-risk, high-volume | Spam filtering |

### Designing for Human Control

- Clear escalation paths
- Override capabilities
- Confidence thresholds for automation
- Audit trails
- Feedback mechanisms

## Privacy Considerations

### Data Minimization

- Collect only necessary data
- Anonymize when possible
- Aggregate rather than individual data
- Delete data when no longer needed

### Privacy-Preserving Techniques

- Differential privacy
- Federated learning
- Secure multi-party computation
- Homomorphic encryption

## Environmental Impact

### Considerations

- Training compute requirements
- Inference energy consumption
- Hardware lifecycle
- Data center energy sources

### Mitigation

- Efficient architectures
- Model distillation
- Transfer learning
- Green hosting providers

## Reference Files

- **`references/bias_assessment.md`** - Detailed bias evaluation methodology
- **`references/regulatory_compliance.md`** - AI regulation requirements

## Integration with Other Skills

- **machine-learning** - For model development
- **testing** - For bias testing
- **documentation** - For model cards
