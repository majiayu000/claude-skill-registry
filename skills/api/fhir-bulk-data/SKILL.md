---
name: fhir-bulk-data
description: Expert guidance for implementing FHIR Bulk Data Access (Flat FHIR) following the HL7 specification. Use this skill when implementing bulk data export from FHIR servers, building bulk data clients, working with the $export operation, handling NDJSON output files, implementing asynchronous polling workflows, or integrating with SMART Backend Services authorisation. Trigger keywords include "bulk data", "bulk export", "$export", "NDJSON", "bulk FHIR", "async export", "flat FHIR", "Patient/$export", "Group/$export", "system export".
---

# FHIR Bulk Data Access

Expert guidance for implementing the FHIR Bulk Data Access (Flat FHIR) specification v3.0.0.

## Overview

Bulk Data Access enables efficient export of large FHIR datasets through an asynchronous request pattern. Instead of making thousands of individual API calls, clients initiate a single export operation and poll for completion.

**Specification:** <http://hl7.org/fhir/uv/bulkdata/>

## Export endpoints

Three endpoints support bulk export:

| Endpoint                    | Scope                                 |
| --------------------------- | ------------------------------------- |
| `[base]/Patient/$export`    | All data for all patients             |
| `[base]/Group/[id]/$export` | Data for patients in a specific group |
| `[base]/$export`            | System-level export (all resources)   |

## Asynchronous workflow

```
Client                                    Server
  │                                         │
  │─── POST [endpoint]/$export ───────────►│
  │    Accept: application/fhir+json        │
  │    Prefer: respond-async                │
  │                                         │
  │◄── 202 Accepted ──────────────────────│
  │    Content-Location: [status-url]       │
  │                                         │
  │─── GET [status-url] ──────────────────►│  ─┐
  │◄── 202 Accepted (X-Progress: 50%) ────│   │ Poll until
  │    Retry-After: 120                     │   │ complete
  │                                         │  ─┘
  │─── GET [status-url] ──────────────────►│
  │◄── 200 OK ────────────────────────────│
  │    [Complete manifest JSON]             │
  │                                         │
  │─── GET [file-url] ────────────────────►│  ─┐
  │◄── 200 OK (NDJSON content) ───────────│   │ Download
  │                                         │  ─┘ files
  │─── DELETE [status-url] ───────────────►│
  │◄── 202 Accepted ──────────────────────│
```

## Request parameters

| Parameter               | Type    | Description                                        |
| ----------------------- | ------- | -------------------------------------------------- |
| `_outputFormat`         | string  | Output format. Default: `application/fhir+ndjson`  |
| `_since`                | instant | Include resources modified after this timestamp    |
| `_until`                | instant | Include resources modified before this timestamp   |
| `_type`                 | string  | Comma-delimited resource types to include          |
| `_elements`             | string  | Comma-delimited elements to include (experimental) |
| `_typeFilter`           | string  | FHIR search queries to filter resources            |
| `includeAssociatedData` | code    | Include additional data sets (experimental)        |
| `organizeOutputBy`      | string  | Organise files by resource type instances          |
| `allowPartialManifests` | boolean | Enable paginated manifests                         |

### Example kick-off request

```http
GET [base]/Patient/$export?_type=Patient,Observation,Condition&_since=2024-01-01T00:00:00Z HTTP/1.1
Accept: application/fhir+json
Prefer: respond-async
Authorization: Bearer [token]
```

Or as POST with Parameters:

```http
POST [base]/Patient/$export HTTP/1.1
Content-Type: application/fhir+json
Accept: application/fhir+json
Prefer: respond-async
Authorization: Bearer [token]

{
  "resourceType": "Parameters",
  "parameter": [
    {"name": "_type", "valueString": "Patient,Observation,Condition"},
    {"name": "_since", "valueInstant": "2024-01-01T00:00:00Z"}
  ]
}
```

## Response handling

### Kick-off response

Success returns `202 Accepted` with `Content-Location` header pointing to the status endpoint.

### Status polling

Poll the status URL using exponential backoff. Respect `Retry-After` headers.

| Status         | Meaning                                         |
| -------------- | ----------------------------------------------- |
| `202 Accepted` | In progress. Check `X-Progress` for percentage. |
| `200 OK`       | Complete. Body contains the output manifest.    |
| `4XX/5XX`      | Error. Body contains `OperationOutcome`.        |

### Complete manifest

```json
{
    "transactionTime": "2024-06-15T10:30:00Z",
    "request": "[original request URL]",
    "requiresAccessToken": true,
    "output": [
        {
            "type": "Patient",
            "url": "https://example.org/bulk/file1.ndjson",
            "count": 1000
        },
        {
            "type": "Observation",
            "url": "https://example.org/bulk/file2.ndjson",
            "count": 50000
        }
    ],
    "deleted": [],
    "error": [],
    "link": [{ "relation": "next", "url": "[next manifest page]" }]
}
```

## NDJSON format

Output files use Newline Delimited JSON. Each line is a complete, valid JSON object representing one FHIR resource.

```
{"resourceType":"Patient","id":"p1","name":[{"family":"Smith"}]}
{"resourceType":"Patient","id":"p2","name":[{"family":"Jones"}]}
```

Rules:

- One JSON object per line
- UTF-8 encoding
- Lines terminated with `\n` (optionally preceded by `\r`)
- No newlines within JSON objects
- Media type: `application/x-ndjson` or `application/fhir+ndjson`

## Authorisation

Bulk Data servers should implement SMART Backend Services authorisation (OAuth 2.0 client credentials flow with JWT assertion).

See [references/authorization.md](references/authorization.md) for implementation details.

## Error handling

Servers return `OperationOutcome` resources for errors:

```json
{
    "resourceType": "OperationOutcome",
    "issue": [
        {
            "severity": "error",
            "code": "processing",
            "diagnostics": "Export failed: insufficient permissions"
        }
    ]
}
```

Common error scenarios:

- `429 Too Many Requests`: Rate limited. Respect `Retry-After`.
- `401 Unauthorized`: Token expired or invalid.
- `404 Not Found`: Export job deleted or never existed.

## Cleanup

After downloading all files, send `DELETE` to the status URL to signal completion and allow server cleanup.

## Conformance

Servers declare bulk data support in their CapabilityStatement:

```json
{
    "instantiates": [
        "http://hl7.org/fhir/uv/bulkdata/CapabilityStatement/bulk-data"
    ]
}
```

## References

- [references/authorization.md](references/authorization.md) - SMART Backend Services authorisation details
- [references/implementation-notes.md](references/implementation-notes.md) - Server and client implementation guidance
