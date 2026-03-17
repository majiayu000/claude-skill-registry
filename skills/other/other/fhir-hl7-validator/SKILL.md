---
name: fhir-hl7-validator
description: This skill should be used when the user asks to "validate FHIR resources", "check HL7 messages", "validate healthcare data format", "parse FHIR", "HL7 v2 messages", "FHIR R5 validation", "CDA documents", "healthcare data interchange", "FHIR resource schema", "HL7 specifications", or mentions FHIR validation, HL7 message parsing, CDA validation, healthcare data format compliance, or Fast Healthcare Interoperability Resources standards.
license: MIT
metadata:
  author: 1mangesh1
  version: "1.0.0"
  tags:
    - fhir
    - hl7
    - cda
    - healthcare
    - validation
    - compliance
    - interoperability
    - ehr
    - healthcare-data
    - r5
---

# FHIR & HL7 Validator

Healthcare data format validation skill for AI agents. Validates FHIR R5 resources, HL7 v2 messages, and CDA clinical documents. Ensures healthcare data interchange compliance with HL7 standards and identifies schema violations, missing required fields, and interoperability issues.

## Capabilities

1. **FHIR Validation** - Validate FHIR R5 resources against official schemas
2. **HL7 Message Parsing** - Parse and validate HL7 v2.x messages (ADT, ORU, OBX, RXO)
3. **CDA Document Validation** - Validate Clinical Document Architecture (CDA) R2 documents
4. **Schema Compliance** - Check resources against FHIR specification and UK Core
5. **Data Type Validation** - Verify FHIR data types (Identifier, CodeableConcept, Reference, etc.)
6. **Reference Resolution** - Validate internal and external references
7. **Cardinality Checking** - Ensure required vs. optional field compliance
8. **Terminology Validation** - Check value sets and coding systems (SNOMED CT, LOINC, ICD-10)
9. **Interoperability Analysis** - Identify implementation guide adherence
10. **Error Reporting** - Generate detailed validation error reports with remediation

## Usage

```
/fhir-hl7-validator [command] [target] [options]
```

### Commands

- `validate-fhir <file>` - Validate FHIR JSON/XML resource
- `validate-hl7 <file>` - Validate HL7 v2 message
- `validate-cda <file>` - Validate CDA clinical document
- `parse-fhir <file>` - Parse and display FHIR resource structure
- `parse-hl7 <file>` - Parse and display HL7 segments
- `check-references <file>` - Validate all resource references
- `check-terminology <file>` - Validate coding systems and value sets
- `bulk-validate <directory>` - Validate multiple files
- `report <output-format>` - Generate validation report (JSON, markdown, HTML)

### Options

- `--version <ver>` - FHIR version (default: R5; also 4.0, 3.0)
- `--variant <name>` - Implementation guide (e.g., uk-core, us-core)
- `--strict` - Enforce must-support constraints
- `--terminology-check` - Validate coding systems (enables online lookup)
- `--output <file>` - Write report to file
- `--format <type>` - Output format: json, markdown, html, xml

## Workflow

Follow this workflow when invoked:

### Step 1: Identify Healthcare Data Type

Ask user to specify:
- Data format (FHIR, HL7 v2, CDA)
- FHIR version or HL7 dialect
- Implementation guide/profile (if applicable)
- Data source (EHR, lab system, imaging system)

### Step 2: Validate Structure

Check:
- JSON/XML well-formedness
- Required elements present
- Data type conformance
- Cardinality compliance (min/max occurrences)
- Pattern and regex validation

### Step 3: Semantic Validation

Verify:
- Code system membership (SNOMED CT, LOINC, ICD-10, etc.)
- Reference consistency (local vs. external)
- Identifier uniqueness and format
- Date/time format accuracy (ISO 8601)
- Quantity unit validity

### Step 4: Interoperability Check

Ensure compliance with:
- FHIR implementation guides
- US Core or UK Core profiles
- HL7 message specifications
- Clinical data interchange standards

### Step 5: Generate Report

Provide:
- List of validation errors with line numbers
- Severity level (error, warning, info)
- Remediation guidance
- Reference to relevant standards

## FHIR Resource Examples

### Patient Resource

```json
{
  "resourceType": "Patient",
  "id": "example",
  "identifier": [
    {
      "system": "http://example.org/medical-record",
      "value": "12345"
    }
  ],
  "name": [
    {
      "use": "official",
      "given": ["Jane"],
      "family": "Doe"
    }
  ],
  "birthDate": "1990-01-15",
  "address": [
    {
      "use": "home",
      "line": ["123 Main St"],
      "city": "Springfield",
      "state": "IL",
      "postalCode": "62701"
    }
  ]
}
```

### Observation Resource

```json
{
  "resourceType": "Observation",
  "id": "example",
  "status": "final",
  "code": {
    "coding": [
      {
        "system": "http://loinc.org",
        "code": "39156-5",
        "display": "BMI"
      }
    ]
  },
  "subject": {
    "reference": "Patient/example"
  },
  "valueQuantity": {
    "value": 24.5,
    "unit": "kg/m2",
    "system": "http://unitsofmeasure.org",
    "code": "kg/m2"
  }
}
```

## HL7 v2 Segment Examples

### ADT Message (Patient Admission)

```
MSH|^~\&|SendingApp|SendingFac|ReceivingApp|ReceivingFac|202502071350||ADT^A01|123456|P|2.5
PID^^^12345||JaneDoe||19900115|F|||123 Main St^^Springfield^IL^62701|||||||S
PV1||I|ICU^FL2^BED01|||||||||||||||||||||||||||
```

## Common Validation Errors

| Error | Cause | Solution |
|-------|-------|----------|
| Missing required element | Element marked `cardinality: 1..1` not present | Add the required element |
| Invalid data type | Value doesn't match specified type | Convert to correct type (e.g., date to YYYY-MM-DD) |
| Unknown code system | Code not in specified value set | Use code from official code system (SNOMED CT, LOINC) |
| Broken reference | Reference target doesn't exist | Verify reference path and ID |
| Invalid identifier format | ID format doesn't match pattern | Follow system-specific identifier format |

## Standards & Implementation Guides

- **FHIR R5** (http://hl7.org/fhir/R5/)
- **HL7 v2.5.1** (http://www.hl7.org/)
- **CDA R2** (https://www.hl7.org/implement/standards/cdar2/)
- **US Core** (http://www.hl7.org/fhir/us/core/)
- **UK Core** (https://digital.nhs.uk/developer/api-catalogue/fhir-uk-core)
- **SNOMED CT** (https://www.snomed.org/)
- **LOINC** (https://loinc.org/)
- **ICD-10** (https://www.cdc.gov/nchs/icd/icd10cm.htm)

## References

- **Fast Healthcare Interoperability Resources (FHIR)** - R5 Specification
- **HL7 Version 2.5.1** - Standard for Healthcare Data Exchange
- **Clinical Document Architecture R2** - CDA Specification
- **NIST SP 800-66 Rev. 2** - HIPAA Security Implementation Guidance
- **HL7 FHIR Implementation Guides**

