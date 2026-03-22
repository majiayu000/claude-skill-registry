---
name: lethal-variance-detection
description: Detect drugs and substances with extreme safety variance across species where a safe dose in one species is lethal in another. CRITICAL SAFETY SKILL. Use before returning any drug information.
---

# Lethal Variance Detection

## Overview

Identify drugs and substances where the safety profile varies so dramatically across species that what is routine therapy in one species is lethal in another. This is a CRITICAL SAFETY skill. These are not edge cases or theoretical risks. These are well-documented causes of iatrogenic animal death.

## When to Use

- ALWAYS check before returning any drug dosing information
- When a drug is being prescribed or recommended for a species
- When a multi-species household is involved (e.g., dog and cat in same home)
- When a drug approved for one species is being considered for off-label use in another
- This skill should be checked automatically by the agent before any drug skill returns results

## Critical Lethal Variance List

### Acetaminophen (Tylenol/Paracetamol)
- **Dogs:** Therapeutic at 10-15 mg/kg PO q8-12h (with caution)
- **Cats:** LETHAL. Causes fatal methemoglobinemia and hepatic necrosis. No safe dose.
- **Action:** If the patient is a cat, DO NOT provide dosing. State clearly: "Acetaminophen is contraindicated in cats. It causes fatal methemoglobinemia. There is no safe dose."

### Permethrin
- **Dogs:** Safe and commonly used in flea/tick products
- **Cats:** LETHAL. Causes tremors, seizures, death. Even environmental exposure from treated dogs can kill cats.
- **Action:** If the patient is a cat or lives with cats, flag permethrin products as dangerous.

### Ivermectin (at elevated doses)
- **Most dogs:** Safe at standard heartworm prevention doses (6-12 mcg/kg)
- **MDR1-mutant breeds (Collies, Australian Shepherds, Shelties, and crosses):** NEUROTOXIC at doses above ~120 mcg/kg. Microfilaricide (50 mcg/kg) and mange treatment doses (200-400 mcg/kg) can be lethal.
- **Action:** If a herding breed or cross, flag MDR1 risk and recommend genetic testing before elevated ivermectin doses.

### 5-Fluorouracil (5-FU)
- **Humans:** Common chemotherapy and topical dermatologic agent
- **Dogs and Cats:** LETHAL even at small exposures. Topical human products (Efudex) have killed dogs who licked treated skin.
- **Action:** Flag any mention of 5-FU in a veterinary context as extremely dangerous.

### Xylazine
- **Horses:** Standard sedation at 0.5-1.0 mg/kg IV
- **Dogs:** 1-2 mg/kg IV (much more sensitive; same mg/kg causes profound sedation)
- **Cats:** 1-2 mg/kg IM (emetic use at lower doses; sedation at higher)
- **Cattle:** Most sensitive, ~0.05-0.1 mg/kg IV
- **Action:** Verify species before any xylazine dosing. Dose ranges differ by 10-20x across species.

### Lily Plants (Lilium and Hemerocallis)
- **Cats:** ALL parts are nephrotoxic. Even pollen or vase water can cause fatal acute kidney injury.
- **Dogs:** Not nephrotoxic (may cause mild GI upset only)
- **Action:** If a cat, treat any lily exposure as a medical emergency.

### Onions/Garlic (Allium species)
- **Dogs and Cats:** Toxic. Causes oxidative damage to red blood cells (Heinz body anemia). Cats are more sensitive than dogs.
- **Horses, Cattle:** Also susceptible
- **Action:** Flag any Allium ingestion, especially in cats.

### Grapefruit/Naringin interaction drugs
- **Note:** CYP3A4 inhibition by grapefruit is primarily a human concern. Veterinary relevance is limited but may affect cyclosporine levels in dogs.

## Workflow

1. When any drug information is requested, cross-reference the drug name against the lethal variance list.
2. If a match is found, determine the patient species.
3. If the species is one where the drug is dangerous, INTERRUPT the normal response flow and present the safety warning FIRST.
4. Use explicit, unambiguous language: "CONTRAINDICATED," "LETHAL," "DO NOT USE."
5. Provide the species where the drug IS safe for contrast, so the user understands this is species-specific, not a universally dangerous drug.

## Output Format (when triggered)

```
!! SPECIES SAFETY ALERT !!

[Drug] has LETHAL variance across species:
- [Species A]: [Safe/Therapeutic -- brief note]
- [Species B]: CONTRAINDICATED -- [mechanism of toxicity]

Your patient is a [species]. [SAFE TO USE WITH CAUTION / DO NOT USE -- clear directive]

[If contraindicated: suggest species-appropriate alternatives]
```

## Limitations

- This list covers the most critical and well-documented lethal variance situations. It is not exhaustive.
- New cases of species-specific toxicity are discovered regularly.
- Individual patient factors (age, organ function, concurrent medications) affect toxicity risk beyond species.
