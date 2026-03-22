---
name: fda-green-book
description: Query the FDA Green Book database of approved animal drug products. Use when checking whether a veterinary drug is FDA-approved, finding approved indications, or looking up NADA/ANADA numbers.
---

# FDA Green Book

## Overview

Access the FDA Center for Veterinary Medicine (CVM) Green Book, the official database of FDA-approved animal drug products. This is the veterinary equivalent of the FDA Orange Book for human drugs. Use it to verify approval status, find approved species and indications, identify generic equivalents, and look up regulatory details.

## When to Use

- User asks whether a drug is FDA-approved for use in animals
- User asks about approved indications for an animal drug
- User asks about generic equivalents of a veterinary drug
- User needs NADA (New Animal Drug Application) or ANADA numbers
- User asks about drug withdrawal times for food animals
- Keywords: FDA approved, Green Book, NADA, ANADA, animal drug approval, CVM, veterinary drug label

## Key Resources

- **FDA Green Book** (https://www.fda.gov/animal-veterinary/products/approved-animal-drug-products-green-book): Searchable database
- **Animal Drugs@FDA** (https://animaldrugsatfda.fda.gov): Complete product information
- **FDA CVM FOIA** resources for supplemental approvals

## Workflow

1. Search the Green Book by drug name (generic or brand), active ingredient, or NADA number.
2. Identify the approved species and indications.
3. Note whether the product is approved for food animals (withdrawal times apply) or companion animals.
4. Distinguish between pioneer (NADA) and generic (ANADA) products.
5. Check for any recent FDA safety communications or label changes via CVM updates.

## Important Context

- Many drugs used in veterinary medicine are used off-label (not FDA-approved for that species or indication). Off-label use is legal under the Animal Medicinal Drug Use Clarification Act (AMDUCA) when prescribed by a veterinarian within a valid VCPR.
- Food animal drugs have mandatory withdrawal times. Using a drug not approved for food animals requires FARAD consultation and extended withdrawal periods.
- FDA CVM regulates animal drugs under a different regulatory framework than FDA CDER (human drugs).

## Output Format

```
## FDA Green Book: [Drug Name]

**Brand Name(s):** [List]
**Active Ingredient:** [Generic name]
**NADA/ANADA:** [Number]
**Sponsor:** [Company]
**Approved Species:** [List]
**Approved Indication(s):** [List]
**Dosage Form/Route:** [Details]
**Food Animal Withdrawal:** [Time if applicable, or "Not approved for food animals"]
**Status:** [Approved / Withdrawn / Conditional approval]
```

## Limitations

- The Green Book covers FDA-approved products only. Many veterinary drugs are used off-label.
- Compounded medications are not in the Green Book.
- International approvals (EMA, APVMA) are separate regulatory systems.
- The Green Book does not include dosing recommendations beyond what is on the approved label.
