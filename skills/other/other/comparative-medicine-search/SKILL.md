---
name: comparative-medicine-search
description: Search for relevant human medical research that may inform veterinary clinical decisions when veterinary-specific evidence is lacking. Use when no species-specific evidence exists and cross-species extrapolation is considered.
---

# Comparative Medicine Search

## Overview

When veterinary-specific evidence is insufficient, human medical research may provide useful clinical insights. This skill structures the process of finding relevant human evidence, assessing its applicability to veterinary patients, and clearly communicating the limitations of cross-species extrapolation.

## When to Use

- No veterinary-specific RCTs or guidelines exist for the clinical question
- User explicitly asks "what do we know from human medicine about [condition]?"
- A novel treatment being considered in animals has an evidence base in human medicine
- One Health topics where human and animal medicine intersect
- Keywords: comparative, translational, human medicine, extrapolate, One Health, cross-species

## Workflow

1. First search for species-specific veterinary evidence (see `veterinary-pubmed-search`).
2. If insufficient, search human PubMed for the clinical topic.
3. Assess biological plausibility of cross-species application:
   - Is the pathophysiology similar between species?
   - Are the drug targets conserved?
   - Are pharmacokinetic parameters known in the target species?
4. Grade the comparative evidence as Level IV (see `evidence-grading` skill).
5. Clearly label all cross-species extrapolations in the output.

## Successful Comparative Medicine Examples

- **Cardiac disease:** Many canine cardiac drugs (pimobendan, enalapril, atenolol) were developed from human cardiology research.
- **Oncology:** Cancer biology is highly conserved. Chemotherapy protocols in veterinary oncology derive from human oncology.
- **Pain management:** Opioid, NSAID, and gabapentin use in animals draws heavily on human pain research.
- **Diabetes:** Insulin therapy principles translate, though disease pathophysiology differs (Type 1 in dogs, Type 2 in cats, both in humans).

## When Comparative Medicine Fails

- **Drug metabolism:** Species-specific differences in cytochrome P450 enzymes, glucuronidation (cats lack this), and acetylation make direct dose extrapolation dangerous.
- **Disease pathophysiology:** "Heart failure" in a horse is a fundamentally different clinical entity than in a human or a dog.
- **Behavioral medicine:** Cognitive and behavioral processes are not directly comparable across species.

## Output Format

When using comparative evidence, always include this framing:

```
**Note: Veterinary-specific evidence is limited for this question.**

The following information is drawn from human medical research and should be considered Level IV evidence (cross-species extrapolation) for veterinary application:

[Information with citation]

**Species-specific considerations:**
- [Known differences in pathophysiology, pharmacokinetics, or clinical presentation]
- [Whether veterinary validation studies exist]
```

## Limitations

- Cross-species extrapolation is inherently uncertain.
- Human dosing is never directly applicable to animals without species-specific pharmacokinetic data.
- Regulatory approval for human drugs does not extend to animal use.
