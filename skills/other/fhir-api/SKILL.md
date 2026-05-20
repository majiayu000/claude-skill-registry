---
name: fhir-api
description: Expert guidance for implementing FHIR RESTful API servers and clients following the HL7 FHIR specification. Use this skill when implementing a FHIR server with REST endpoints, building a FHIR client, designing FHIR API routes and handlers, implementing FHIR operations (read, create, update, delete, search, history), working with FHIR bundles, batch requests, or transactions, handling FHIR content negotiation, headers, and versioning, or implementing conditional operations. Trigger keywords include "FHIR REST", "FHIR API", "FHIR server", "FHIR client", "FHIR endpoint", "FHIR operations", "RESTful FHIR", "implement FHIR".
---

# FHIR REST API implementation

This skill provides guidance for implementing FHIR RESTful APIs according to the HL7 FHIR specification (R4/R5).

## URL structure

All FHIR REST URLs follow the pattern:

```
[base]/[type]/[id]
```

- `[base]`: Service base URL (e.g., `https://fhir.example.org/r4`)
- `[type]`: Resource type (e.g., `Patient`, `Observation`)
- `[id]`: Logical resource ID

URLs are case-sensitive and use UTF-8 encoding.

## Core operations

| Operation         | HTTP     | URL Pattern                         | Success |
| ----------------- | -------- | ----------------------------------- | ------- |
| Read              | GET      | `[base]/[type]/[id]`                | 200     |
| VRead             | GET      | `[base]/[type]/[id]/_history/[vid]` | 200     |
| Create            | POST     | `[base]/[type]`                     | 201     |
| Update            | PUT      | `[base]/[type]/[id]`                | 200/201 |
| Patch             | PATCH    | `[base]/[type]/[id]`                | 200     |
| Delete            | DELETE   | `[base]/[type]/[id]`                | 200/204 |
| Search            | GET/POST | `[base]/[type]?params`              | 200     |
| History           | GET      | `[base]/[type]/[id]/_history`       | 200     |
| Capabilities      | GET      | `[base]/metadata`                   | 200     |
| Batch/Transaction | POST     | `[base]`                            | 200     |

For detailed specifications of each operation, see [references/operations.md](references/operations.md).

## Content negotiation

### MIME types

| Format | MIME Type                 |
| ------ | ------------------------- |
| JSON   | `application/fhir+json`   |
| XML    | `application/fhir+xml`    |
| RDF    | `application/fhir+turtle` |

Use the `Accept` header for response format and `Content-Type` for request body format.

The `_format` query parameter overrides `Accept` when clients cannot set headers.

### FHIR version

Specify version via MIME type parameter:

```
Accept: application/fhir+json; fhirVersion=4.0
```

Version mappings: 1.0 (R2), 3.0 (R3), 4.0 (R4), 4.3 (R4B), 5.0 (R5).

## Required headers

### Request headers

| Header        | Purpose             | Example                 |
| ------------- | ------------------- | ----------------------- |
| Accept        | Response format     | `application/fhir+json` |
| Content-Type  | Request body format | `application/fhir+json` |
| If-Match      | Optimistic locking  | `W/"123"`               |
| If-None-Exist | Conditional create  | `identifier=123`        |
| Prefer        | Return preference   | `return=representation` |

### Response headers

| Header        | Purpose            | Example                         |
| ------------- | ------------------ | ------------------------------- |
| ETag          | Version identifier | `W/"123"`                       |
| Location      | New resource URL   | `[base]/Patient/123/_history/1` |
| Last-Modified | Modification time  | RFC 7231 date                   |

## Versioning and optimistic locking

FHIR uses weak ETags for version tracking:

1. Server returns `ETag: W/"[versionId]"` with responses
2. Client sends `If-Match: W/"[versionId]"` with updates
3. Server returns `412 Precondition Failed` if version mismatch

Implement version-aware updates when `CapabilityStatement.rest.resource.versioning` is `versioned-update`.

## Error handling

Return `OperationOutcome` resources for all errors:

```json
{
    "resourceType": "OperationOutcome",
    "issue": [
        {
            "severity": "error",
            "code": "invalid",
            "diagnostics": "Patient.birthDate: Invalid date format"
        }
    ]
}
```

### Status codes

| Code | Meaning                                |
| ---- | -------------------------------------- |
| 400  | Invalid syntax or validation failure   |
| 404  | Resource not found                     |
| 409  | Version conflict                       |
| 410  | Resource deleted                       |
| 412  | Precondition failed (version mismatch) |
| 422  | Business rule violation                |

## Prefer header

Control response content with `Prefer`:

| Value                     | Response body        |
| ------------------------- | -------------------- |
| `return=minimal`          | Empty (headers only) |
| `return=representation`   | Full resource        |
| `return=OperationOutcome` | Validation outcome   |

For async operations, use `Prefer: respond-async` to get `202 Accepted` with status polling URL.

## Implementation checklist

Server implementations should:

1. Implement CapabilityStatement at `/metadata`
2. Support content negotiation (JSON at minimum)
3. Return proper ETags for versioned resources
4. Include `Location` header on create/update
5. Return `OperationOutcome` for all errors
6. Support `_format` parameter fallback
7. Honour `Prefer` header for response content

## References

- [operations.md](references/operations.md): Detailed operation specifications
- [search.md](references/search.md): Search parameter and result handling
- [batch-transaction.md](references/batch-transaction.md): Batch and transaction processing
