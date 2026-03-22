---
name: claims-eob
description: Generate Claim, ClaimResponse, and ExplanationOfBenefit (EOB) resources for healthcare billing including professional, institutional, pharmacy (Rx), dental, and vision claims. Use when user mentions claims, EOB, explanation of benefit, billing, reimbursement, adjudication, pharmacy claims, Rx claims, denied claims, copay, deductible, or allowed amount.
keywords: [claim, claims, EOB, explanation of benefit, billing, reimbursement, adjudication, pharmacy claim, Rx claim, professional claim, institutional claim, dental claim, vision claim, denied, copay, deductible, coinsurance, allowed amount, paid, CMS-1500, UB-04, NCPDP, DRG, CPT, HCPCS, NDC, revenue code]
resource_types: [Claim, ClaimResponse, ExplanationOfBenefit]
always: false
---

# Claims and Explanation of Benefit (EOB)

Generate realistic healthcare billing resources reflecting the US claims lifecycle.

## Claim

Professional, institutional, pharmacy, dental, and vision claims:

- **Use** codes from http://terminology.hl7.org/CodeSystem/claim-type:
  `professional`, `institutional`, `oral`, `vision`, `pharmacy`.
- **Status**: active, cancelled, draft, entered-in-error.
- **Priority**: normal, stat, deferred (http://terminology.hl7.org/CodeSystem/processpriority).
- **Patient / Provider / Insurer**: Reference Patient, Practitioner/Organization, Organization.
- **Insurance**: Reference the Coverage resource; set `focal = true` for the primary payer.
- **Diagnosis**: Include Claim.diagnosis[] with ICD-10 codes, sequence, and type
  (admitting, clinical, principal, secondary) from
  http://terminology.hl7.org/CodeSystem/ex-diagnosistype.
- **Procedure**: Include Claim.procedure[] with CPT/HCPCS codes and date.
- **Item-level detail**:
  * `Claim.item[].productOrService` — CPT (professional), revenue code + HCPCS (institutional),
    NDC (pharmacy), CDT (dental).
  * `Claim.item[].quantity` — units of service.
  * `Claim.item[].unitPrice` — Money with currency USD.
  * `Claim.item[].net` — quantity × unitPrice.
  * `Claim.item[].servicedDate` or `servicedPeriod`.
- **SupportingInfo**: Attach relevant clinical info (onset date, discharge status, etc.).
- **Total**: Claim.total = sum of item.net values.

### Professional Claims (CMS-1500)

- productOrService: CPT codes (99213 office visit, 99214 detailed visit, 99232 hospital care,
  99283 ER visit moderate, 36415 venipuncture, 71046 chest X-ray 2 views).
- Place of service: office (11), hospital inpatient (21), ER (23), telehealth (02).
- Include Practitioner NPI in Claim.provider.

### Institutional Claims (UB-04)

- Revenue codes in Claim.item[].revenue:
  0120 (room & board semi-private), 0250 (pharmacy), 0260 (IV therapy),
  0300 (laboratory), 0320 (radiology diagnostic), 0450 (ER),
  0710 (operating room).
- Include admit/discharge dates in Claim.billablePeriod.
- DRG in Claim.diagnosis with type "drg" when applicable.

### Pharmacy / Rx Claims

- productOrService: NDC codes (National Drug Codes).
  * Metformin 500mg: NDC 00093-7214-01
  * Lisinopril 10mg: NDC 00093-7339-01
  * Atorvastatin 20mg: NDC 00093-5057-01
  * Omeprazole 20mg: NDC 65862-0525-01
  * Albuterol inhaler: NDC 00173-0682-20
- Quantity: dispense quantity (e.g., 30 tablets, 1 inhaler).
- Days supply in supportingInfo.
- Include prescribing Practitioner reference.
- Pharmacy Organization as Claim.facility.

## ClaimResponse

Adjudication result from the payer:

- **Status**: active, cancelled, draft, entered-in-error.
- **Outcome**: complete, error, partial, queued
  (http://hl7.org/fhir/remittance-outcome).
- **Disposition**: "Claim settled as per contract" or denial reason text.
- **Item adjudication**: Each item gets adjudication[] with categories:
  * `submitted` — billed amount.
  * `eligible` — allowed/contracted amount.
  * `deductible` — patient deductible portion.
  * `copay` — patient copay amount.
  * `benefit` — payer payment amount.
  Use http://terminology.hl7.org/CodeSystem/adjudication.
- **Payment**: ClaimResponse.payment with amount, date, and type
  (complete, partial) from http://terminology.hl7.org/CodeSystem/ex-paymenttype.
- **Total**: adjudication totals mirroring the item-level categories.
- Include realistic denial scenarios:
  * Authorization not obtained → outcome partial, disposition "Prior auth required".
  * Non-covered service → adjudication benefit = $0.
  * Duplicate claim → outcome error.

## ExplanationOfBenefit (EOB)

Combines Claim + ClaimResponse into a patient-facing benefits explanation:

- **Status**: active, cancelled, draft, entered-in-error.
- **Use**: claim, preauthorization, predetermination.
- **Type**: Same as Claim type (professional, institutional, pharmacy, oral, vision).
- **Outcome**: complete, error, partial, queued.
- **Patient / Provider / Insurer**: Same references as the Claim.
- **Insurance**: Reference Coverage, set focal.
- **Item + Adjudication**: Mirror the Claim items with full adjudication breakdown
  (submitted, eligible, deductible, copay, benefit).
- **Total**: EOB.total[] with category and amount for each adjudication type.
- **Payment**: EOB.payment with amount and date.
- **BenefitBalance**: Include benefit category
  (http://terminology.hl7.org/CodeSystem/benefit-type) with financial limits:
  * allowed money/quantity, used money/quantity for the benefit period.
- **Realistic dollar amounts** (approximate US ranges):
  * Office visit: billed $150–$350, allowed $80–$200, copay $20–$50.
  * ER visit: billed $500–$5,000, allowed $300–$2,500.
  * Inpatient day: billed $2,000–$10,000, allowed $1,200–$5,000.
  * Rx (generic): billed $15–$100, copay $5–$25.
  * Rx (brand): billed $100–$1,000, copay $30–$75.

## Creation Order

Claims resources depend on other resources in this order:

1. Organization (payer + provider org) — standalone
2. Practitioner — standalone
3. Patient — may reference Organization
4. Coverage — references Patient + Organization (payer)
5. Encounter, Condition, Procedure, MedicationRequest — clinical resources
6. **Claim** — references Patient, Coverage, Practitioner, Encounter, diagnoses
7. **ClaimResponse** — references Claim
8. **ExplanationOfBenefit** — references Patient, Coverage, Claim, Practitioner

