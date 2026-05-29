---
name: patient-variation
description: Generate patient demographics reflecting real-world population diversity including age distribution, gender, race, ethnicity, language, marital status, identifiers, contacts, and deceased status. Use for any request involving Patient resources.
keywords: [patient, demographic, age, gender, race, ethnicity, language, birth, name, address, identifier, contact, diversity, neonatal, pediatric, geriatric, elderly, deceased, twins]
resource_types: [Patient]
always: true
---

# Patient Variation

Generate data that reflects real-world population diversity:
- AGE DISTRIBUTION: Include neonates (0–28 days), infants (1m–1y), pediatric (1–17y),
  adults (18–64y), and geriatric (65+). Weight age groups roughly: 5% neonates/infants,
  15% pediatric, 55% adults, 25% geriatric. Adjust per clinical context.
- GENDER & SEX: Use FHIR administrative gender (male, female, other, unknown).
  Include transgender patients where clinically relevant — use extensions for
  birth sex (us-core-birthsex) and gender identity (us-core-genderIdentity).
- RACE & ETHNICITY (US Core): Populate US Core Race and Ethnicity extensions:
  * Race: http://hl7.org/fhir/us/core/StructureDefinition/us-core-race
    Codes from urn:oid:2.16.840.1.113883.6.238 (CDC Race & Ethnicity):
    2106-3 White, 2054-5 Black or African American, 2028-9 Asian,
    1002-5 American Indian or Alaska Native, 2076-8 Native Hawaiian or Other Pacific Islander,
    2131-1 Other Race. Include "detailed" sub-categories and "text" extension.
  * Ethnicity: http://hl7.org/fhir/us/core/StructureDefinition/us-core-ethnicity
    2135-2 Hispanic or Latino, 2186-5 Non Hispanic or Latino
- LANGUAGE & COMMUNICATION: Set Patient.communication with language codes (en, es, zh, vi, ko,
  tl, ar, fr, de, ru, pt, hi, etc.) and communication.preferred = True for primary language.
  Include patients with limited English proficiency (LEP).
- MARITAL STATUS: Vary using http://terminology.hl7.org/CodeSystem/v3-MaritalStatus
  (A=Annulled, D=Divorced, M=Married, S=Single/Never Married, W=Widowed, etc.)
- MULTIPLE IDENTIFIERS: Include MRN, SSN (fake), driver's license, insurance member ID.
  Use proper identifier systems:
  * MRN: http://hospital.example.org/mrn
  * SSN: http://hl7.org/fhir/sid/us-ssn
  * Driver License: urn:oid:2.16.840.1.113883.4.3.{state_fips}
- CONTACT/NOK: Include Patient.contact for emergency contacts / next of kin with relationship
  codes (C=Emergency Contact, N=Next of Kin, E=Employer, etc.)
- DECEASED PATIENTS: Some patients should have deceasedBoolean=True or deceasedDateTime set.
  Approximately 2–5% of a general patient cohort.
- MULTIPLE BIRTH: Use multipleBirthBoolean or multipleBirthInteger for twins/triplets.

