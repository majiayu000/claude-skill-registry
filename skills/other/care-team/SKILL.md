---
name: care-team
description: Generate Practitioner, PractitionerRole, Organization, and Location resources for the clinical care team including NPIs, specialties, taxonomies, and facility details. Use when user mentions practitioner, doctor, physician, nurse, provider, NPI, organization, hospital, clinic, facility, location, department, care team, or specialist.
keywords: [practitioner, doctor, physician, nurse, NPI, provider, organization, hospital, clinic, facility, location, department, care team, specialist, PractitionerRole, taxonomy, specialty, referring, attending, primary care, surgeon, cardiologist, bed, ward, ICU, operating room]
resource_types: [Practitioner, PractitionerRole, Organization, Location]
always: false
---

# Care Team Resources

Generate the foundational resources that other clinical resources reference.

## Practitioner

Individual healthcare providers:
- **Identifier**: NPI (system = http://hl7.org/fhir/sid/us-npi), 10-digit numeric.
  Generate realistic-looking NPIs (e.g., "1234567890"). Include DEA number for prescribers.
- **Name**: Use Faker for realistic names; include prefix (Dr., NP, PA).
- **Qualification**: Include code from http://terminology.hl7.org/CodeSystem/v2-0360
  (MD, DO, NP, PA, RN, PharmD, DDS, DPM).
- **Communication**: Include language codes matching patient population.
- **Gender**: male, female, other, unknown.
- **Active**: true (most), false for retired/inactive.

## PractitionerRole

Links Practitioner to Organization with specialty:
- **Specialty**: Use NUCC Health Care Provider Taxonomy
  (system = http://nucc.org/provider-taxonomy):
  * 207R00000X Internal Medicine
  * 207RC0000X Cardiovascular Disease
  * 207RG0100X Gastroenterology
  * 207RN0300X Nephrology
  * 207RP1001X Pulmonary Disease
  * 207Q00000X Family Medicine
  * 208D00000X General Practice
  * 207X00000X Orthopedic Surgery
  * 208600000X Surgery
  * 2084N0400X Neurology
  * 2084P0800X Psychiatry
  * 363L00000X Nurse Practitioner
  * 363A00000X Physician Assistant
  * 183500000X Pharmacist
- **Code** (role): doctor, nurse, pharmacist, researcher from
  http://terminology.hl7.org/CodeSystem/practitioner-role.
- **Location**: Reference Location where this practitioner practices.
- **AvailableTime**: Include schedule availability.

## Organization

Healthcare organizations (providers and payers):
- **Type**: Use http://terminology.hl7.org/CodeSystem/organization-type:
  prov (Healthcare Provider), pay (Payer), dept (Hospital Department),
  govt (Government), ins (Insurance Company), edu (Educational Institute).
- **Identifier**: NPI for provider orgs (system = http://hl7.org/fhir/sid/us-npi),
  TIN/EIN (system = urn:oid:2.16.840.1.113883.4.4).
- **Name**: Realistic hospital/clinic names (e.g., "Memorial Regional Medical Center",
  "Valley Health Partners", "Summit Cardiology Associates").
- **Address**: Use Faker for realistic US addresses.
- **Telecom**: Phone, fax, email, website.
- **PartOf**: Department → parent hospital Organization reference.
- **Active**: true.

### Common Organization Patterns
- **Hospital system**: Parent org + child departments (ED, ICU, Radiology, Lab).
- **Physician group**: Multi-provider practice with shared NPI.
- **Payer organizations**: BCBS, Aetna, UHC, Cigna, Humana, Medicare, Medicaid.
- **Pharmacy chains**: CVS, Walgreens, Rite Aid (for Rx claims).

## Location

Physical or virtual places of care:
- **Status**: active, suspended, inactive.
- **Mode**: instance (specific place), kind (class of locations).
- **Type**: Use http://terminology.hl7.org/CodeSystem/v3-RoleCode:
  HOSP (Hospital), ER (Emergency Room), ICU (Intensive Care Unit),
  OF (Outpatient Facility), PHARM (Pharmacy), LAB (Laboratory),
  HRAD (Radiology), OR (Operating Room), PACU (Recovery Room),
  NURS (Nursing Unit), PEDU (Pediatric Unit), BMTU (Bone Marrow Transplant),
  VR (Virtual / Telehealth).
- **PhysicalType**: bu (Building), wi (Wing), wa (Ward), ro (Room), bd (Bed),
  si (Site), area (Area).
- **Address**: Full US address with Faker.
- **Position**: Include latitude/longitude for mapping.
- **ManagingOrganization**: Reference to parent Organization.
- **PartOf**: Room → Ward → Wing → Building hierarchy.

## Creation Order

These resources are standalone and should be created FIRST:
1. **Organization** — no dependencies.
2. **Location** — references Organization (managingOrganization).
3. **Practitioner** — standalone.
4. **PractitionerRole** — references Practitioner + Organization + Location.

All other clinical resources (Patient, Encounter, etc.) then reference these.

