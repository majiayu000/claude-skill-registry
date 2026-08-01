---
name: export-oscal
description: Export NIST OSCAL (Open Security Controls Assessment Language) JSON from
  compliance
---

---
name: export-oscal
description: NIST OSCAL JSON export of compliance evidence from ArangoDB graph
triggers:
  - "export oscal"
  - "oscal export"
  - "compliance export"
allowed-tools:
  - Bash
provides:
  - export-oscal
composes: [, task-monitor]
---

# Export OSCAL

Export NIST OSCAL (Open Security Controls Assessment Language) JSON from compliance
evidence stored in the ArangoDB graph. Supports NIST 800-171 and CMMC Level 2
frameworks.

## Usage

### Export compliance evidence

```bash
./run.sh export --framework NIST-800-171
./run.sh export --framework CMMC-L2
```

### Dry run (no ArangoDB required)

```bash
./run.sh export --framework NIST-800-171 --dry-run
```

Generates a valid OSCAL assessment-results structure with example data. Useful for
testing downstream consumers without a running database.

### Validate an OSCAL file

```bash
./run.sh validate <file.json>
```

Checks that the JSON file contains required OSCAL assessment-results fields:
`uuid`, `metadata`, and `results`.

## Output

All output goes to stdout as formatted JSON. Redirect to a file as needed:

```bash
./run.sh export --framework NIST-800-171 > oscal-export.json
```

## OSCAL Structure

The exported JSON follows the OSCAL assessment-results model:

- `uuid` -- unique identifier for this export
- `metadata.title` -- framework name and export context
- `metadata.last-modified` -- ISO 8601 timestamp
- `metadata.version` -- export version
- `metadata.oscal-version` -- OSCAL specification version
- `results[]` -- array of assessment results, each mapping a control to evidence
  - `uuid` -- unique result identifier
  - `title` -- control identifier and name
  - `start` -- assessment timestamp
  - `findings[]` -- evidence entries from QRA and lessons collections

## Data Sources

Queries three ArangoDB collections in the `sparta` database:

| Collection | Purpose |
|------------|---------|
| `sparta_controls` | Control definitions and status |
| `sparta_qra` | QRA (Question-Response-Action) evidence entries |
| `lessons` | Lessons learned linked to controls |
