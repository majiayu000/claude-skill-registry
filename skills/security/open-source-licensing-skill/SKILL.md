---
skill: 'open-source-licensing'
version: '2.0.0'
updated: '2025-12-31'
category: 'risk-compliance'
complexity: 'intermediate'
prerequisite_skills: []
composable_with:
  - 'legal-compliance'
  - 'tool-evaluation'
  - 'risk-assessment'
  - 'local-ai-deployment'
---

# Open Source Licensing Skill

## Overview
Expertise in navigating open-source licenses for AI models and tools, ensuring commercial compliance, managing license obligations, and mitigating intellectual property risks in enterprise AI deployments.

## Key Capabilities
- License identification and classification
- Commercial use eligibility assessment
- License obligation management
- IP risk evaluation for AI models
- License compliance documentation
- Open source governance frameworks

## License Classification

### Permissive Licenses (Low Restriction)

| License | Commercial Use | Modify | Distribute | Patent Grant | Attribution | Share-Alike |
|---------|---------------|--------|------------|--------------|-------------|-------------|
| **MIT** | Yes | Yes | Yes | No | Required | No |
| **Apache 2.0** | Yes | Yes | Yes | Yes | Required | No |
| **BSD 2-Clause** | Yes | Yes | Yes | No | Required | No |
| **BSD 3-Clause** | Yes | Yes | Yes | No | Required | No |
| **ISC** | Yes | Yes | Yes | No | Required | No |

**Best for enterprise:** Apache 2.0 (includes patent grant)

### AI-Specific Licenses

| License | Commercial Use | Training Use | Key Restrictions | Examples |
|---------|---------------|--------------|------------------|----------|
| **Provider Open-Weights License** | Varies | Varies | Variant-specific terms | Qwen-Next, GLM-4.6, MiniMax-M2 |
| **RAIL-style (Responsible AI)** | Often | Often | Use restrictions / behavioral constraints | Some open-weights releases |
| **Commercial EULA** | Yes | Limited | Redistribution + usage limits | Enterprise-only models |

### Copyleft Licenses (Higher Restriction)

| License | Commercial Use | Derivative Work Rules | Typical Impact |
|---------|---------------|----------------------|----------------|
| **GPL v3** | Yes | Must open source derivatives | Rarely used for models |
| **LGPL v3** | Yes | Link exception | Libraries only |
| **AGPL v3** | Yes | Network use triggers | Avoid for production |

## License Deep Dives

### Apache 2.0 (Recommended)

```markdown
## Apache 2.0 License Summary

### What You Can Do
- Use commercially without restrictions
- Modify and create derivative works
- Distribute modified or unmodified versions
- Use in proprietary software
- Sublicense

### What You Must Do
- Include copyright notice
- Include copy of Apache 2.0 license
- Document significant changes made
- Include NOTICE file if provided

### Patent Grant
"Subject to the terms and conditions of this License, each Contributor
hereby grants to You a perpetual, worldwide, non-exclusive, no-charge,
royalty-free, irrevocable... patent license"

### Termination
License terminates automatically if you initiate patent litigation
claiming the software infringes a patent.

### Models Using Apache 2.0
- Some current-generation model/tool releases may be Apache 2.0 (variant dependent)
- Falcon family
- MPT family
```

### MIT License

```markdown
## MIT License Summary

### What You Can Do
- Everything Apache 2.0 allows
- Even simpler attribution requirements

### What You Must Do
- Include copyright notice and license text

### What's Missing (vs Apache 2.0)
- No explicit patent grant
- No explicit contribution terms

### Models Using MIT
- Some current-generation model/tool releases may be MIT (variant dependent)
- Some StableLM variants

### Risk Consideration
For enterprise use, MIT is slightly higher risk than Apache 2.0
due to lack of explicit patent grant. Generally acceptable for
inference use but consider patent landscape.
```

### Provider Open-Weights License (Most Common in 2025)

```markdown
## Provider Open-Weights License Summary

### Commercial Use Rules
Commercial use, redistribution, and fine-tuning rights vary by provider and by variant.

### Common Restrictions to Look For
1. **Redistribution limits:** whether you can mirror weights internally / ship to air-gapped networks
2. **Usage restrictions:** regulated domains, disallowed content, safety constraints
3. **Attribution/notice:** requirements in documentation or UI
4. **Fine-tuning/training constraints:** whether LoRA/QLoRA is allowed; whether re-training is restricted

### Derivative Works
Often allowed, but obligations differ (model card usually defines it).

### Practical Implications
| Use Case | Allowed | Notes |
|----------|---------|-------|
| Internal code assistant | Usually | Verify internal redistribution + logging constraints |
| Customer-facing product | Sometimes | Check any usage restrictions and attribution requirements |
| Fine-tuned model | Often | Confirm fine-tune + redistribution terms |
| Training new model | Varies | Many licenses restrict training new foundation models |
| Enterprise deployment | Usually | Ensure legal sign-off and archiving of terms |

### Compliance Checklist
- [ ] Archive the model card + license text alongside deployment artifacts
- [ ] Confirm commercial use + internal redistribution rights
- [ ] Confirm any usage restrictions fit your intended use
- [ ] Implement any required attribution/notice
- [ ] Legal review sign-off (recommended)
```

### RAIL-Style Licenses (Use Restrictions)

```markdown
## RAIL-Style License Summary

### Permissive Base
- Commercial use allowed
- Modification allowed
- Distribution allowed

### Use Restrictions (Behavioral)
The license includes specific "Use Restrictions" prohibiting:

1. **Harmful Content Generation**
   - Violence, harassment, discrimination
   - Illegal activities

2. **Deceptive Uses**
   - Impersonation
   - Disinformation

3. **High-Risk Automated Decisions Without Human Review**
   - Legal advice
   - Medical diagnosis
   - Financial advice
   - Employment decisions

4. **Surveillance**
   - Unauthorized surveillance
   - Biometric processing without consent

### Practical Compliance
For typical code assistant use:
- [ ] Don't use for illegal purposes
- [ ] Include human review for critical decisions
- [ ] Don't use for surveillance
- [ ] Pass through use restrictions to end users

### Enterprise Consideration
The use restrictions are reasonable for code assistant use cases.
Primary concern: Ensure end users understand restrictions if
building customer-facing products.
```

## License Compliance Workflow

### Pre-Deployment Assessment

```markdown
## License Assessment Checklist

### Step 1: Identify All Components
| Component | License | Source | Commercial OK |
|-----------|---------|--------|---------------|
| Base model | [e.g., Apache 2.0] | Hugging Face | Yes |
| Fine-tune data | [source license] | Internal | Yes |
| Tokenizer | [license] | Model repo | Yes |
| Serving framework | [e.g., Apache 2.0] | vLLM | Yes |
| Dependencies | [various] | pip | Check each |

### Step 2: Commercial Use Verification
For each component:
- [ ] License explicitly allows commercial use
- [ ] No use restrictions that conflict with intended use
- [ ] No threshold triggers (MAU, revenue, etc.)

### Step 3: Obligation Mapping
| Obligation | Components | How to Comply |
|------------|------------|---------------|
| Attribution | Model, framework | Include in docs |
| License inclusion | All | Bundle licenses |
| Source disclosure | None (permissive) | N/A |
| Patent notice | Apache 2.0 | Include PATENTS |

### Step 4: Risk Assessment
| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| License change | Low | Medium | Version lock, alternatives |
| Patent claim | Very Low | High | Use Apache 2.0 where possible |
| Compliance audit | Medium | Medium | Document everything |
```

### Ongoing Compliance

```markdown
## License Compliance Maintenance

### Quarterly Review
- [ ] Check for license changes in dependencies
- [ ] Review new model versions for license changes
- [ ] Update compliance documentation
- [ ] Audit distribution for proper attribution

### When Updating Models
- [ ] Verify new version has same/compatible license
- [ ] Update attribution if required
- [ ] Document license in change log
- [ ] Re-assess use restrictions

### Documentation Requirements
1. **License Inventory:** List of all components and licenses
2. **Attribution Notices:** Consolidated attribution file
3. **Distribution Package:** Include all required license texts
4. **Compliance Decisions:** Document any interpretations made
```

## Model-Specific Guidance

### Recommended Models by License Risk

```markdown
## License Risk Tiers for Enterprise

### Tier 1: Minimal Risk (Apache 2.0 / MIT)
**Use freely with standard attribution**

| Model | License | Notes |
|-------|---------|-------|
| Any license-approved variant of Qwen-Next / GLM-4.6 / MiniMax-M2 | Apache 2.0 / MIT / BSD | Verify the specific model card and include required notices |

### Tier 2: Low Risk (Clear Commercial, Some Obligations)
**Commercial use clear, follow specific terms**

| Model | License | Key Obligation |
|-------|---------|----------------|
| Qwen-Next / GLM-4.6 / MiniMax-M2 (provider terms) | Provider Open-Weights License | Archive terms; follow attribution/redistribution rules |
| Any RAIL-style release | RAIL-style | Enforce usage restrictions and pass-through obligations |

### Tier 3: Medium Risk (Review Required)
**Need legal review for specific use case**

| Model | License | Concern |
|-------|---------|---------|
| Large/enterprise variants | Provider-specific | Redistribution and commercial terms may differ by variant |
| Some fine-tuned models | Varies | May inherit restrictions |
| Datasets (for fine-tuning) | Varies | Often unclear terms |

### Tier 4: Avoid for Commercial Use
**Significant restrictions or unclear commercial terms**

| Model | License | Issue |
|-------|---------|-------|
| Models with NC (Non-Commercial) | Various | No commercial use |
| Research-only models | Varies | Explicit restriction |
| Models from unclear sources | Unknown | Provenance risk |
```

## IP Considerations

### Training Data Concerns

```markdown
## Training Data IP Issues

### Known Concerns
- **Copyrighted code:** Many models trained on GitHub code
- **Licensed content:** Training data may include licensed works
- **Opt-out requests:** Some publishers opted out

### Mitigation Strategies
1. **Use models with transparent training:**
   - Prefer models with published data documentation and clear licensing provenance

2. **Implement output filtering:**
   - Detect verbatim code reproduction
   - License header detection

3. **Document model selection rationale:**
   - Why this model was chosen
   - Training data considerations
   - Risk acceptance if applicable

### Indemnification
- Some commercial providers offer indemnification
- Open source models typically have no indemnification
- Consider insurance for IP claims
```

### Output Ownership

```markdown
## Who Owns AI-Generated Code?

### Current Legal Landscape (2024-2025)
- **Unclear:** Copyright law still evolving
- **Generally:** Human authorship required for copyright
- **Practical:** Treat AI output as work product

### Enterprise Best Practices
1. **Treat as if company owns:**
   - Add standard company copyright
   - Include in version control
   - Apply normal IP policies

2. **Document AI involvement:**
   - Code review for AI-generated content
   - Note AI assistance in commit messages (optional)
   - Maintain records for potential future requirements

3. **Avoid problematic outputs:**
   - Don't commit verbatim model regurgitation
   - Review for license headers from training data
   - Treat as starting point, not final code
```

## Compliance Documentation Templates

### License Inventory

```markdown
## AI System License Inventory

**System:** Local Code Assistant
**Last Updated:** [Date]
**Maintained By:** [Name]

### Core Components

| Component | Version | License | Source | Commercial | Notes |
|-----------|---------|---------|--------|------------|-------|
| <MODEL_NAME> (e.g., Qwen-Next / GLM-4.6 / MiniMax-M2) | <MODEL_VERSION> | <MODEL_LICENSE> | <MODEL_SOURCE> | <YES/NO> | Archive model card + terms |
| vLLM | 0.5.0 | Apache 2.0 | GitHub | Yes | |
| NGINX | 1.24 | BSD 2-clause | nginx.org | Yes | |
| Python | 3.11 | PSF License | python.org | Yes | |

### Dependencies (Notable)

| Package | License | Risk | Notes |
|---------|---------|------|-------|
| transformers | Apache 2.0 | Low | |
| torch | BSD | Low | |
| numpy | BSD | Low | |

### License Files Location
- `/opt/llm/licenses/` - All third-party licenses
- `/opt/llm/NOTICE` - Attribution notices
- `/opt/llm/THIRD_PARTY` - Complete inventory
```

### Attribution Notice

```markdown
## Third-Party Attribution Notice

This software includes the following third-party components:

### Model Attribution (Fill In)
<MODEL_ATTRIBUTION>
<MODEL_LICENSE_URL>
<REQUIRED_NOTICE_TEXT>

### vLLM
Copyright (c) 2023 vLLM Team
Licensed under the Apache License, Version 2.0.
https://github.com/vllm-project/vllm/blob/main/LICENSE

### [Additional components...]

---

For complete license texts, see the /licenses directory.
```

## Best Practices

### License Selection
1. **Prefer Apache 2.0** for patent protection
2. **MIT is acceptable** for inference use
3. **Review AI-specific licenses** carefully
4. **Avoid GPL/AGPL** unless specifically needed
5. **Document all license decisions**

### Compliance
1. **Maintain license inventory** for all components
2. **Include all required notices** in distributions
3. **Review quarterly** for license changes
4. **Train team** on license obligations
5. **Establish escalation path** for license questions

### Risk Management
1. **Have alternatives** for critical components
2. **Version lock** to avoid surprise license changes
3. **Consider legal review** for Tier 3+ licenses
4. **Document risk acceptance** for any gray areas
5. **Monitor legal developments** in AI/copyright

This skill ensures organizations navigate open-source licensing effectively, minimizing legal risk while maximizing the benefits of open-source AI.
