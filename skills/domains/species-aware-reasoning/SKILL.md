---
name: species-aware-reasoning
description: Enforce species-specific clinical reasoning across all veterinary queries. Prevents dangerous cross-species assumptions. Use as a meta-skill that modifies how other veterinary skills operate.
---

# Species-Aware Reasoning

## Overview

This is a foundational reasoning skill that enforces species-specific thinking across all veterinary clinical queries. The most dangerous errors in veterinary AI come from applying knowledge about one species to another without adjustment. This skill defines the rules for species disambiguation, cross-species safety checking, and species-specific clinical reasoning patterns.

## When to Use

- ALWAYS active when any veterinary clinical question is being answered
- Specifically triggered when species is ambiguous or unspecified
- When a user says "my patient" without species context
- When applying clinical knowledge that may vary by species
- This is a meta-skill: it modifies the behavior of other skills rather than standing alone

## Core Rules

### Rule 1: Never Assume Species

If a user asks a clinical question without specifying the species, ask before answering. "What species is your patient?" is always the correct first response to an ambiguous clinical query.

**Exception:** If context makes species unambiguous (e.g., "my dog ate chocolate"), proceed without asking.

### Rule 2: Physiology Differs

Do not assume physiological processes are the same across species:
- **Cats are obligate carnivores.** Dietary and metabolic recommendations differ fundamentally from dogs.
- **Cats lack significant glucuronidation capacity.** Many drugs safe in dogs are toxic in cats (acetaminophen, aspirin at dog doses, permethrin, essential oils).
- **Horses are hindgut fermenters.** GI disease presentations and treatments differ from small animals.
- **Ruminants have a four-compartment stomach.** Drug pharmacokinetics and GI disease are species-unique.
- **Avian and reptile patients** have nucleated RBCs, different thermoregulation, unique respiratory anatomy (air sacs in birds), and renal portal systems.

### Rule 3: Disease Presentation Differs

The same disease process can present differently across species:
- Heart failure: Dogs show cough (left-sided) or ascites (right-sided). Cats show dyspnea/tachypnea with minimal cough. Horses show ventral edema and exercise intolerance.
- Diabetes: Dogs are typically Type 1 (insulin-dependent). Cats are typically Type 2 (may be transient/reversible).
- Pain: Cats mask pain differently than dogs. Reptiles show minimal pain behavior. Pain assessment scales are species-specific.

### Rule 4: Drug Safety Requires Species Verification

Before returning any drug dose or safety information, verify the species and check for known species-specific toxicity or dosing differences. See `lethal-variance-detection` and `veterinary-drug-lookup` skills.

### Rule 5: Breed Matters Within Species

Within a species, breed significantly affects disease risk, drug sensitivity, and normal parameters. See `breed-predisposition` skill. Key examples:
- MDR1 mutation (herding breeds): Ivermectin, loperamide sensitivity
- Brachycephalic breeds: Anesthesia risk, upper airway disease
- Sighthounds (Greyhounds, Whippets): Altered drug metabolism, different hematologic normals
- Scottish Fold cats: Osteochondrodysplasia (cartilage defect is the same gene as the ear fold)

## Workflow

1. Identify species from context or ask explicitly.
2. Before answering any clinical question, verify that the knowledge being applied is appropriate for this species.
3. Flag any species-specific caveats explicitly in the response.
4. If extrapolating from data in another species, state this explicitly: "This recommendation is based on canine data; feline-specific evidence is limited."

## Limitations

- This skill defines reasoning rules, not a database. It works in conjunction with other VetClaw skills.
- Exotic species (reptiles, amphibians, fish, invertebrates) have the least clinical data available.
- Wildlife medicine often requires extrapolation from domestic species data.
