---
name: breed-predisposition
description: Breed-specific disease predispositions and genetic risk factors for veterinary differential diagnosis. Use when breed information is available and may affect diagnostic priorities.
---

# Breed Predisposition

## Overview

Incorporate breed-specific disease predispositions into clinical reasoning. Different breeds have dramatically different risk profiles for hundreds of conditions. A Cavalier King Charles Spaniel presenting with a murmur should have mitral valve disease at the top of the differential list. A Doberman with syncope should be evaluated for dilated cardiomyopathy. This skill encodes these breed-disease associations to improve differential diagnosis ranking.

## When to Use

- User provides a breed along with clinical signs
- User asks "what diseases is [breed] predisposed to?"
- User is building a differential diagnosis list and breed is known
- User asks about genetic testing for a specific breed
- User asks about breed-specific screening recommendations
- Keywords: breed, predisposed, genetic, hereditary, screening, risk

## Key Databases

- **OMIA** (Online Mendelian Inheritance in Animals, https://omia.org): Curated catalog of inherited disorders and traits in animals. Maintained by University of Sydney.
- **VBO** (Vertebrate Breed Ontology): 19,500+ breed concepts across 49 species with standardized nomenclature.
- **OFA** (Orthopedic Foundation for Animals): Breed-specific health data and screening statistics.
- **Breed-specific health surveys** from national kennel clubs (AKC, KC UK, FCI affiliates).

## Workflow

1. **Standardize the breed name.** Map common names, abbreviations, and regional variants to a canonical breed identifier. Examples:
   - "GSD" / "German Shepherd" / "Alsatian" -> German Shepherd Dog
   - "Doodle" -> Clarify: Labradoodle, Goldendoodle, or other cross
   - "Pit Bull" -> Clarify: American Pit Bull Terrier, American Staffordshire Terrier, or Staffordshire Bull Terrier
   - Mixed breeds: Note that predisposition data is breed-specific; mixed breeds may carry any combination

2. **Retrieve known predispositions.** For the identified breed, list conditions with documented increased risk. Organize by body system:
   - Cardiovascular (e.g., CKCS: mitral valve disease; Doberman: DCM; Boxer: ARVC)
   - Orthopedic (e.g., Labrador: hip/elbow dysplasia, CCL rupture)
   - Neurologic (e.g., IVDD in Dachshunds, syringomyelia in CKCS)
   - Dermatologic (e.g., atopic dermatitis in West Highland White Terriers)
   - Endocrine (e.g., hypothyroidism in Golden Retrievers)
   - Oncologic (e.g., hemangiosarcoma in Golden Retrievers, osteosarcoma in large breeds)
   - Ophthalmic (e.g., PRA in many breeds, entropion in Shar-Peis)
   - Other genetic conditions

3. **Rank by prevalence and clinical relevance.** Not all predispositions are equally important. Prioritize conditions that are:
   - Common in the breed (high prevalence)
   - Clinically significant (not cosmetic variants)
   - Relevant to the presenting complaint (if one is given)
   - Screenable or testable (actionable information)

4. **Note available genetic tests.** For conditions with known genetic basis, indicate whether a DNA test is commercially available and from which lab.

5. **Include screening recommendations.** For breeds with established screening protocols (e.g., cardiac screening for Dobermans, hip scoring for Labradors), note the recommended screening age and method.

## Output Format

When breed is provided with clinical signs:
```
## Breed Considerations: [Breed] presenting with [signs]

**Elevated differentials based on breed predisposition:**
1. [Condition] -- [Breed] has [X-fold] increased risk; [prevalence if known]
2. [Condition] -- [Reason for elevation]

**Recommended breed-specific diagnostics:**
- [Test] to evaluate for [condition]

**Genetic testing available:**
- [Test name] from [Lab] for [condition]
```

When asking about breed predispositions generally:
```
## Known Predispositions: [Breed]

**High-priority conditions:**
- [System]: [Condition] -- [Brief note on prevalence/severity]

**Recommended screening:**
- [Age]: [Screening test] for [condition]

**Available genetic tests:**
- [Gene/mutation]: [Test] -- [Lab]

**Source:** OMIA, OFA breed statistics, [relevant breed health survey]
```

## Limitations

- Predisposition data is strongest for popular purebred dogs. Data for mixed breeds, cats, horses, and exotic species is more limited.
- "Predisposed" means increased risk, not certainty. A breed predisposition does not confirm a diagnosis.
- Prevalence data varies by geographic population. UK breed data may not perfectly match US or Australian populations.
- New genetic discoveries are ongoing. This skill should be supplemented with current literature.
- For mixed breeds and designer crosses, predispositions from contributing breeds may or may not apply depending on actual genetic inheritance.
