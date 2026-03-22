---
name: veterinary-drug-lookup
description: Species-specific veterinary drug information including dosing, contraindications, and safety warnings. Use when asked about animal medications, drug doses, or veterinary pharmacology.
---

# Veterinary Drug Lookup

## Overview

Retrieve species-specific drug information for veterinary clinical use. Unlike human pharmacology, veterinary drug safety varies dramatically across species. This skill enforces mandatory species identification before returning any drug information and flags known lethal variance situations.

## When to Use

- User asks about a drug dose for an animal
- User asks whether a drug is safe for a specific species
- User asks about veterinary drug formulations or routes of administration
- User mentions a brand name or generic drug in a veterinary context
- User asks about off-label drug use in animals
- Keywords: drug, dose, dosage, medication, prescribe, administer, mg/kg, PO, IV, IM, SC

## Key Capabilities

- Species-specific dosing (canine, feline, equine, bovine, avian, exotic)
- Route of administration guidance (PO, IV, IM, SC, topical, ophthalmic)
- Frequency and duration recommendations
- Contraindication identification
- Breed-specific warnings (e.g., MDR1 mutation in herding breeds)
- Food animal withdrawal times
- Pregnancy and pediatric safety categories

## Databases and Sources

- **FDA Green Book** (https://www.fda.gov/animal-veterinary/products/approved-animal-drug-products-green-book): Approved animal drug products
- **openFDA Animal & Veterinary** (https://open.fda.gov/apis/animalandveterinary/): Adverse event reports for animal drugs
- **Plumb's Veterinary Drug Handbook**: Industry-standard drug reference (cite edition)
- **FARAD** (Food Animal Residue Avoidance Databank): Withdrawal times for food animals

## Workflow

1. **Identify the drug.** Resolve brand names to generic names. Handle common misspellings. If ambiguous (e.g., "metronidazole" could be oral or topical), ask for clarification.

2. **Require species.** MANDATORY. Never return drug information without confirming the target species. If the user says "my patient" without specifying species, ask: "What species is the patient? Drug safety varies significantly between species."

3. **Check lethal variance.** Before returning any dosing information, check whether this drug has known lethal variance across species. Flag these explicitly:
   - Acetaminophen: Safe in dogs, LETHAL in cats (methemoglobinemia)
   - Permethrin: Safe in dogs, LETHAL in cats (neurotoxicity)
   - Ivermectin: Safe in most dogs, NEUROTOXIC in MDR1-mutant breeds (Collies, Australian Shepherds, Shelties)
   - NSAIDs (meloxicam, carprofen): Species-specific dosing; feline doses are fraction of canine
   - Xylazine: Dramatic species variation in sensitivity
   - 5-Fluorouracil: Safe in humans, LETHAL in dogs and cats

4. **Return structured drug information:**
   - Generic name and common brand names
   - Approved indication(s) vs. off-label use
   - Dose range (mg/kg), route, frequency
   - Duration if applicable
   - Key contraindications for this species
   - Breed-specific warnings if relevant
   - Monitoring recommendations
   - Food animal withdrawal time if applicable

5. **Cite sources.** Every dose and safety claim must reference a specific source (textbook + edition, FDA Green Book listing, or peer-reviewed publication).

## Output Format

```
## [Drug Name] - [Species]

**Status:** FDA-approved for this species / Off-label use
**Indication:** [What it treats]
**Dose:** [X-Y mg/kg] [route] [frequency]
**Duration:** [If applicable]
**Key Warnings:**
- [Species-specific warnings]
- [Breed-specific warnings if any]
**Contraindications:** [List]
**Monitoring:** [What to monitor]
**Source:** [Textbook/edition or FDA listing]
```

## Limitations

- This skill provides reference information, not clinical recommendations. All drug decisions require veterinary professional judgment.
- Compounding pharmacy formulations may differ from standard preparations.
- Regional availability varies (some drugs approved in US may not be available in UK/EU/Australia and vice versa).
- This skill does not replace checking current formulary references for the most up-to-date information.
- Exotic species (reptiles, birds, small mammals) have limited pharmacokinetic data for many drugs.
