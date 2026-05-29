---
name: drug-interaction-checker
description: Check for drug-drug interactions in veterinary patients with species-specific pharmacokinetic considerations. Use when a patient is on multiple medications or a new drug is being added.
---

# Veterinary Drug Interaction Checker

## Overview

Evaluate potential drug-drug interactions in veterinary patients. Drug interactions in animals differ from humans due to species-specific differences in hepatic metabolism (cytochrome P450 enzyme profiles), protein binding, renal clearance, and GI physiology. This skill checks for known interactions and flags combinations requiring dose adjustment or monitoring.

## When to Use

- User asks whether two or more drugs can be given together to an animal
- User is adding a new medication to an existing regimen
- User asks about drug interactions in a specific species
- Keywords: interaction, combine, together, concurrent, polypharmacy, concomitant, contraindicated combination

## Workflow

1. Identify all drugs in the patient's regimen (including supplements, nutraceuticals).
2. Confirm species (MANDATORY - metabolism pathways differ).
3. Check each drug pair for known interactions:
   - **Pharmacokinetic interactions:** Enzyme induction/inhibition, protein binding displacement, altered absorption
   - **Pharmacodynamic interactions:** Additive effects, synergism, antagonism
4. Classify severity:
   - **Contraindicated:** Must not be used together (e.g., MAOIs + serotonergic drugs)
   - **Major:** Significant risk requiring alternative therapy or intensive monitoring
   - **Moderate:** May require dose adjustment or monitoring
   - **Minor:** Minimal clinical significance but document
5. Provide management recommendation for each interaction found.

## Common Veterinary Drug Interactions

- **NSAIDs + corticosteroids:** Increased GI ulceration risk (especially in dogs)
- **ACE inhibitors + potassium-sparing diuretics:** Hyperkalemia risk
- **Phenobarbital + many drugs:** CYP450 enzyme inducer; decreases levels of concurrent drugs
- **Ketoconazole/itraconazole + many drugs:** CYP450 inhibitor; increases levels of concurrent drugs
- **Metoclopramide + opioids:** Antagonistic effects on GI motility
- **Fluoroquinolones + divalent cations (sucralfate, antacids):** Chelation reduces absorption
- **Cisapride + azole antifungals:** QT prolongation risk
- **Selegiline (Anipryl) + serotonergic drugs (tramadol, SSRIs, TCAs):** Serotonin syndrome risk. Selegiline is an MAO-B inhibitor used for canine cognitive dysfunction. Do not combine with tramadol, fluoxetine, clomipramine, or amitriptyline. Allow 2-week washout between discontinuation and starting a serotonergic drug.
- **Metronidazole + phenobarbital:** Phenobarbital induces metronidazole metabolism; may require dose adjustment
- **Cyclosporine + ketoconazole:** Ketoconazole intentionally used to reduce cyclosporine dose (cost-saving strategy in vet practice, but requires monitoring)

## Output Format

```
## Drug Interaction Check: [Species]

**Medications:** [List all drugs]

**Interactions found:**

1. [Drug A] + [Drug B]
   - **Severity:** [Contraindicated/Major/Moderate/Minor]
   - **Mechanism:** [How they interact]
   - **Clinical effect:** [What could happen]
   - **Management:** [What to do about it]

**No interactions found between:** [List non-interacting pairs]
```

## Limitations

- Veterinary drug interaction databases are less comprehensive than human databases. Many interactions are extrapolated from human data.
- Individual patient factors (hepatic/renal disease, age) affect interaction risk.
- Nutraceuticals and supplements may have undocumented interactions.
- This skill identifies known interactions; absence of a listed interaction does not guarantee safety.
