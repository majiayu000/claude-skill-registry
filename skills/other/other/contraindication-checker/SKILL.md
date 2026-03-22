---
name: contraindication-checker
description: Check for drug contraindications based on species, breed, age, organ function, pregnancy status, and concurrent conditions. Use before recommending any medication in a veterinary patient.
---

# Veterinary Contraindication Checker

## Overview

Systematic contraindication checking for veterinary drug therapy. Goes beyond drug-drug interactions (see `drug-interaction-checker`) to evaluate patient-specific factors that may make a drug unsafe: species, breed genetics, organ dysfunction, pregnancy, age extremes, and concurrent disease states.

## When to Use

- Before recommending any drug therapy in a veterinary patient
- When a patient has known organ dysfunction (renal, hepatic, cardiac)
- When a patient is pregnant, lactating, or neonatal
- When breed-specific drug sensitivities may apply
- Keywords: contraindication, safe to use, can I give, renal dose, hepatic dose, pregnant, breeding, puppy, kitten, geriatric

## Contraindication Categories

### Species Contraindications
See `lethal-variance-detection` skill. Some drugs are absolutely contraindicated in certain species regardless of patient status.

### Breed/Genetic Contraindications
- **MDR1 mutation (ABCB1):** Ivermectin (high dose), loperamide, acepromazine (use lower dose), vincristine, doxorubicin -- affected breeds: Collie, Australian Shepherd, Shetland Sheepdog, Old English Sheepdog, and crosses
- **Greyhounds/Sighthounds:** Prolonged thiopental recovery, different propofol pharmacokinetics, lower normal reference ranges for some lab values
- **Brachycephalic breeds:** Higher anesthesia risk, avoid heavy sedation protocols, caution with opioid-induced respiratory depression

### Organ Function Contraindications
- **Renal insufficiency:** Adjust or avoid nephrotoxic drugs (aminoglycosides, cisplatin, NSAIDs). Reduce doses of renally excreted drugs.
- **Hepatic insufficiency:** Avoid hepatotoxic drugs (ketoconazole, azathioprine at standard doses). Reduce doses of hepatically metabolized drugs.
- **Cardiac disease:** Avoid negative inotropes in heart failure patients. Caution with fluid-loading drugs.
- **GI disease:** Consider route of administration; oral drugs may have unpredictable absorption.

### Life Stage Contraindications
- **Neonatal/Pediatric:** Many drugs lack pediatric dosing data. Immature hepatic and renal function affects clearance. Fluoroquinolones avoid in growing animals (cartilage damage).
- **Geriatric:** Reduced organ reserve. Start low, go slow. More susceptible to adverse effects.
- **Pregnant/Lactating:** Many drugs are teratogenic or excreted in milk. Griseofulvin is teratogenic in cats. Methotrexate, retinoids are contraindicated.

### Disease State Contraindications
- **Seizure history:** Avoid drugs that lower seizure threshold (fluoroquinolones, tramadol in some patients)
- **Bleeding disorders:** Avoid NSAIDs and drugs affecting platelet function
- **GDV/GI obstruction:** Oral medications may not be absorbed; avoid prokinetics if mechanical obstruction

## Workflow

1. List all patient parameters: species, breed, age, weight, reproductive status, known organ dysfunction, concurrent diseases, current medications.
2. For each proposed drug, check against all applicable contraindication categories.
3. If a contraindication is found, classify severity:
   - **Absolute:** Do not use under any circumstances
   - **Relative:** Use only if benefit clearly outweighs risk, with monitoring
   - **Dose adjustment:** Drug may be used at modified dose or frequency
4. Suggest alternatives when a drug is contraindicated.

## Limitations

- Contraindication data is most complete for dogs and cats. Exotic species data is limited.
- Clinical judgment may override relative contraindications when no suitable alternative exists.
- New contraindications are discovered through post-market surveillance and case reports.
