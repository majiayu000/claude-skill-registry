---
name: provenance-data-quality
description: Generate Provenance resources for audit trails with agents, activities, entities, and security labels. Model realistic EHR data quality variation with missing fields, sparse records, data-absent reasons, duplicate records, and correction workflows. Use when user mentions provenance, audit, data quality, data origin, missing data, sparse records, data completeness, data lineage, correction, amendment, or data governance.
keywords: [provenance, audit, data quality, data origin, tracking, missing data, sparse, data absent, completeness, unconfirmed, cancelled, entered-in-error, amendment, correction, duplicate, lineage, security label, consent, redaction, data governance, source system, interface, HL7v2, migration]
resource_types: [Provenance]
always: true
---

# Provenance and Data Quality

## Provenance

Track data origin, authorship, and transformation for audit and compliance.

### Activity Codes

Use http://terminology.hl7.org/CodeSystem/v3-DataOperation:
- **CREATE** — resource first created (new patient registration, new order).
- **UPDATE** — resource modified (lab result amended, diagnosis updated).
- **DELETE** — resource removed (entered-in-error correction).
- **APPEND** — addendum to existing resource (addendum to clinical note).

Additional activity codes from http://terminology.hl7.org/CodeSystem/provenance-participant-type:
- **originator** — the entity that first created the content.
- **reviewer** — the entity that verified the content.
- **legal** — the entity that attested to the legal authenticity.

### Agent Types

Provenance.agent[].type from http://terminology.hl7.org/CodeSystem/provenance-participant-type:
- **author** — who wrote/created the resource.
  → Reference(Practitioner/{id}) or Reference(Patient/{id}).
- **performer** — who performed the activity described.
  → Reference(Practitioner/{id}).
- **verifier** — who verified/approved the resource.
  → Reference(Practitioner/{id}).
- **attester** — who attested to the accuracy.
  → Reference(Practitioner/{id}) or Reference(Organization/{id}).
- **informant** — who provided the information.
  → Reference(Patient/{id}) or Reference(RelatedPerson/{id}).
- **custodian** — who is responsible for ongoing maintenance.
  → Reference(Organization/{id}).
- **assembler** — device/system that assembled the resource.
  → Reference(Device/{id}).

### Agent.onBehalfOf

When a practitioner acts on behalf of an organization:
- Provenance.agent[].onBehalfOf → Reference(Organization/{id}).
- Common: resident documenting on behalf of attending, nurse on behalf of hospital.

### Entity (Source Tracking)

Provenance.entity[] tracks what the resource was derived from:
- **role**: derivation, revision, quotation, source, removal.
- **what**: Reference to the source resource or document.
- Use for:
  * Lab result derived from a Specimen.
  * Amended DiagnosticReport revision of a prior report.
  * Clinical note quoting a prior note.
  * Data migrated from a legacy system (source = Device or DocumentReference).

### Recorded Timestamp

- Provenance.recorded — MUST be an Instant (full datetime with timezone).
- Use `datetime.now(timezone.utc).isoformat()`.
- Should be at or after the resource's own lastUpdated timestamp.

### Common Provenance Patterns

**EHR data entry:**
```
target: Patient/{id}
activity: CREATE
agent: [{ type: author, who: Practitioner/{id} }]
recorded: 2025-03-15T10:30:00Z
```

**Lab result from analyzer:**
```
target: Observation/{id}
activity: CREATE
agent: [
  { type: author, who: Device/{id} },          ← lab instrument
  { type: verifier, who: Practitioner/{id} }    ← pathologist review
]
entity: [{ role: source, what: Specimen/{id} }]
```

**Amended report:**
```
target: DiagnosticReport/{id}  (status: amended)
activity: UPDATE
agent: [{ type: author, who: Practitioner/{id} }]
entity: [{ role: revision, what: DiagnosticReport/{original_id} }]
```

**Data received via HL7v2 interface:**
```
target: Observation/{id}
activity: CREATE
agent: [
  { type: assembler, who: Device/{id} },        ← integration engine
  { type: custodian, who: Organization/{id} }    ← receiving hospital
]
policy: ["http://hospital.example.org/policy/data-import"]
```

### Security and Policy

- Provenance.policy — list of policy URIs that apply (consent, data use agreements).
- Use for HIPAA, research consent, data sharing agreements.
- Example: `["http://hospital.example.org/policy/hipaa-minimum-necessary"]`.

## Data Quality Variation

Reflect real-world EHR messiness — not all data is clean, complete, or correct.

### Missing and Sparse Data

- **Vary completeness**: ~60% of patients fully documented, ~30% partially, ~10% sparse.
- **Sparse patients**: Only demographics + 1–2 encounters (newly registered, transferred in).
- **Missing optional fields**: Omit phone, email, address.line[1], maritalStatus randomly.
- **Missing clinical detail**: Some Conditions without onset, some Observations without interpretation.

### Data Absent Reasons

Use Observation.dataAbsentReason with http://terminology.hl7.org/CodeSystem/data-absent-reason:
- **unknown** — value is unknown (most common, ~40% of absent values).
- **asked-unknown** — patient was asked but doesn't know.
- **temp-unknown** — temporarily unavailable (pending lab result).
- **not-asked** — question was not asked (screening not performed).
- **asked-declined** — patient declined to answer.
- **masked** — value hidden due to security/privacy (restricted access).
- **not-applicable** — observation not applicable to this patient.
- **unsupported** — system doesn't support this measurement.
- **as-text** — value provided only as narrative text.
- **error** — measurement error occurred.
- **not-a-number** — result is NaN (e.g., division by zero in calculated field).
- **not-performed** — test/procedure was not performed.
- **negative-results-not-stored** — only positive results are stored (common for cultures).

### Status Variation

Reflect that not everything succeeds:
- **Conditions**: ~5% verificationStatus = "unconfirmed" or "provisional".
  ~2% = "refuted" (ruled out). ~1% = "entered-in-error".
- **Encounters**: ~3% status = "cancelled" (patient no-show). ~1% = "entered-in-error".
- **Observations**: ~2% status = "cancelled" (specimen lost). ~1% = "entered-in-error".
- **MedicationRequests**: ~5% status = "cancelled" or "stopped" (adverse reaction, patient refusal).
- **Procedures**: ~3% status = "not-done" with statusReason (contraindication, refusal).
- **Immunizations**: ~5% status = "not-done" with statusReason (patient objection, medical precaution).

### Corrections and Amendments

- **Amended observations**: Original status = "amended", new Observation with corrected value.
  Link via Provenance.entity[].role = "revision".
- **Corrected reports**: DiagnosticReport status = "corrected" with updated conclusion.
- **Entered-in-error**: Resources with status "entered-in-error" should have Provenance
  with activity = DELETE documenting who marked it and when.

### Duplicate and Conflicting Data

- **Duplicate patients**: ~2% of patients have slight name/DOB variations (data entry errors).
  Different MRNs but same person — realistic for EMPI scenarios.
- **Conflicting vitals**: Occasionally two BP readings for same encounter with different values
  (nurse station vs. physician re-check).
- **Stale data**: Some conditions remain "active" despite being clinically resolved
  (problem list not updated — very common in real EHRs).

### Temporal Data Quality

- **Backdated entries**: Some records entered days after the encounter (late documentation).
  Provenance.recorded > resource.period.end.
- **Future dates**: Occasionally a typo creates a future date (entered-in-error scenario).
- **Out-of-order events**: Discharge summary recorded before some inpatient notes.
- **Timezone inconsistencies**: Mix of UTC and local timezone offsets in DateTime fields
  (reflects real multi-site EHR data).

