---
name: differential-diagnosis
description: Generate ranked differential diagnosis lists for veterinary cases incorporating species, breed, age, and clinical signs. Use when a veterinarian presents a case with clinical findings.
---

# Veterinary Differential Diagnosis

## Overview

Generate ranked differential diagnosis lists that account for species, breed, age, signalment, and presenting clinical signs. Veterinary differential diagnosis differs fundamentally from human medicine because the same clinical sign in different species often indicates completely different disease processes.

## When to Use

- User presents clinical signs and asks "what could this be?"
- User asks for a differential diagnosis list
- User describes a case with signalment (species, breed, age, sex) and findings
- User asks what diagnostics to run based on clinical presentation
- Keywords: differential, DDx, diagnosis, what could cause, rule out, presenting with

## Workflow

1. **Gather signalment.** Species (MANDATORY), breed, age, sex, reproductive status, weight. Each of these influences differential ranking.

2. **Categorize clinical signs** by body system. Identify the primary problem list.

3. **Generate differentials** ranked by:
   - **Prevalence** in this species/breed/age combination
   - **Breed predisposition** (if breed is known)
   - **Age-related likelihood** (e.g., neoplasia more likely in older patients, congenital in young)
   - **Geographic considerations** if location is provided (e.g., Valley Fever in Southwest US, heartworm in endemic areas)
   - **Acuity** (acute vs. chronic presentation changes ranking)

4. **Organize by likelihood tier:**
   - **Most likely (rule these out first):** Common conditions matching this signalment
   - **Consider:** Less common but clinically important
   - **Less likely but do not miss:** Rare conditions with serious consequences if missed

5. **Suggest minimum diagnostic database** to differentiate between top differentials.

## Output Format

```
## Differential Diagnosis: [Species/Breed/Age] with [Primary Signs]

**Most likely:**
1. [Condition] -- [Why it ranks here for this patient]
2. [Condition] -- [Supporting reasoning]

**Consider:**
3. [Condition] -- [Reasoning]
4. [Condition] -- [Reasoning]

**Do not miss:**
- [Condition] -- [Why this is dangerous to overlook]

**Recommended diagnostics to differentiate:**
- [Test] -- rules in/out [conditions]
- [Test] -- rules in/out [conditions]
```

## Limitations

- Differential diagnosis is a clinical reasoning tool, not a definitive diagnosis. Physical examination and diagnostics are required.
- This skill cannot examine the patient. The quality of the differential list depends entirely on the quality of clinical information provided.
- Rare and emerging diseases may not be represented.
- Geographic and seasonal disease patterns are important but may not be fully captured.
