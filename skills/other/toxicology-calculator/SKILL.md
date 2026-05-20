---
name: toxicology-calculator
description: Calculate toxicity risk for common animal poisonings including chocolate, xylitol, grapes, lilies, rodenticides. Use when a pet has ingested a potentially toxic substance.
---

# Veterinary Toxicology Calculator

## Overview

Calculate dose-dependent toxicity risk when an animal has ingested a potentially toxic substance. Provides species-specific toxic and lethal dose thresholds, expected clinical signs by dose range, and initial decontamination guidance with time-sensitivity assessment.

## When to Use

- An animal has eaten or been exposed to a potentially toxic substance
- User asks "is [substance] toxic to [species]?"
- User asks about chocolate, xylitol, grapes/raisins, lilies, antifreeze, rodenticide, marijuana/THC, or other common toxicants
- User needs to calculate whether the amount ingested is dangerous
- User asks about decontamination timing (emesis, activated charcoal)
- Keywords: ate, ingested, poisoning, toxic, toxicity, exposure, swallowed, chewed

## Key Capabilities

- Dose-per-kilogram calculation from amount ingested and patient weight
- Risk stratification (no concern / monitor / treat / critical)
- Species-specific thresholds (a substance toxic to cats may be safe for dogs)
- Time-since-ingestion assessment for decontamination decisions
- Common toxicant database with dose-response data

## Common Toxicant Reference

**Chocolate (dogs):**
- Theobromine content varies by type: white (~0.25 mg/g), milk (~2.4 mg/g), dark (~5.5 mg/g), baking (~16 mg/g), cocoa powder (~28.5 mg/g)
- Mild signs (GI): 20 mg/kg theobromine
- Cardiac signs: 40-50 mg/kg
- Seizures: 60+ mg/kg
- Lethal dose (LD50): ~100-200 mg/kg
- Theobromine half-life in dogs: ~17.5 hours

**Xylitol (dogs):**
- Hypoglycemia threshold: 0.1 g/kg (100 mg/kg); some reports suggest sensitivity at doses as low as 0.05 g/kg. Treat any significant xylitol ingestion as an emergency.
- Hepatotoxicity threshold: 0.5 g/kg (500 mg/kg)
- Onset of hypoglycemia: 30-60 minutes (can be delayed with some xylitol-containing products)
- Note: Cats appear less susceptible but data is limited; increasing prevalence in sugar-free foods, dental products, and peanut butters

**Grapes/Raisins (dogs):**
- No established safe dose. Any ingestion in dogs should be treated as potentially toxic.
- Toxic dose is idiosyncratic and unpredictable
- Raisins are more concentrated than grapes by weight
- Can cause acute kidney injury

**Lilies (cats):**
- ALL parts of true lilies (Lilium and Hemerocallis species) are nephrotoxic to cats
- No safe dose. Even pollen exposure or water from a lily vase can be fatal.
- Causes acute kidney injury within 24-72 hours
- Dogs are NOT affected by lily nephrotoxicity

**Ethylene glycol (all species):**
- Lethal dose dogs: ~6.6 mL/kg
- Lethal dose cats: ~1.5 mL/kg (cats are 4x more sensitive)
- Treatment window: 8-12 hours (dogs), 3 hours (cats) for antidote efficacy

**THC / Marijuana (dogs primarily):**
- Dogs are significantly more sensitive than humans; toxicity reported at 0.5-3 g/kg of marijuana plant material
- Edibles (brownies, gummies, butter) are the most common exposure route and may contain additional toxicants (chocolate, xylitol)
- Clinical signs: Ataxia, urinary incontinence, mydriasis, bradycardia, hypothermia, stupor. Onset 30-90 minutes (edibles may be delayed).
- Severe cases: Seizures, coma, death (rare but reported, especially with concentrated products)
- Treatment: Supportive care, IV fluids, anti-emetics (if early), lipid emulsion therapy for severe cases

**Macadamia nuts (dogs):**
- Toxic dose: 2.4-62.4 g/kg (wide range; individual sensitivity varies)
- Clinical signs: Weakness (especially hindlimb), vomiting, tremors, hyperthermia. Onset 6-12 hours.
- Duration: Self-limiting, typically resolves within 24-48 hours
- Treatment: Supportive; rarely fatal but causes significant distress. Combined macadamia + chocolate ingestion increases severity.

## Workflow

1. **Identify the toxicant.** What did the animal ingest? Resolve brand names to active ingredients where possible.

2. **Identify the species.** MANDATORY. Toxicity is species-dependent.

3. **Gather quantitative data:**
   - Patient body weight (kg)
   - Amount ingested (grams, mL, number of items, or "unknown")
   - Time since ingestion
   - If chocolate: type of chocolate (milk, dark, baking, cocoa powder)

4. **Calculate dose per kilogram.** Convert the amount ingested to mg/kg or g/kg of the toxic compound.

5. **Stratify risk:**
   - **No concern:** Dose below any toxic threshold for this species
   - **Monitor:** Dose in range where mild signs possible; home monitoring may be appropriate
   - **Treat:** Dose in range where clinical signs expected; veterinary care recommended
   - **Critical:** Dose at or above potentially lethal range; emergency veterinary care immediately

6. **Assess decontamination window:**
   - Emesis generally effective within 1-2 hours of ingestion (contraindicated in some situations)
   - Activated charcoal may help within 1-4 hours depending on substance
   - Note contraindications to emesis: corrosives, hydrocarbons, sharp objects, seizuring patient, brachycephalic breeds (higher aspiration risk)

7. **Provide initial guidance** and recommend contacting a veterinarian or the ASPCA Animal Poison Control Center (888-426-4435) or Pet Poison Helpline (855-764-7661).

## Output Format

```
## Toxicity Assessment: [Substance] in [Species]

**Patient:** [Weight] kg [Species/Breed]
**Ingested:** [Amount] of [Substance]
**Calculated dose:** [X mg/kg] of [toxic compound]
**Time since ingestion:** [X hours]

**Risk Level:** [NO CONCERN / MONITOR / TREAT / CRITICAL]

**Toxic thresholds for [species]:**
- Mild signs at: [X mg/kg]
- Serious signs at: [X mg/kg]
- Potentially lethal at: [X mg/kg]
- Patient's dose: [X mg/kg] -- [above/below] [threshold]

**Expected clinical signs at this dose:**
- [List expected signs]
- [Expected onset timing]

**Decontamination:**
- Emesis: [Recommended/Not recommended] -- [reason]
- Activated charcoal: [Recommended/Not recommended]

**Action:** [Specific recommendation]

**Contact:** ASPCA Animal Poison Control: 888-426-4435 | Pet Poison Helpline: 855-764-7661
```

## Limitations

- Calculations are based on published toxic dose ranges. Individual animals may be more or less sensitive.
- "Amount ingested" is often estimated. When uncertain, assume worst-case.
- This skill provides initial risk assessment, not treatment protocols. Treatment decisions require veterinary professional judgment.
- Some toxicants (grapes/raisins) have idiosyncratic toxicity with no reliable dose-response relationship.
- Exotic species toxicology data is extremely limited for most substances.
