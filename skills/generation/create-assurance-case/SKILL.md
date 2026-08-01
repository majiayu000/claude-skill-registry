---
name: create-assurance-case
description: Generate Goal Structuring Notation (GSN) assurance case diagrams from
  the
---

---
name: create-assurance-case
description: GSN (Goal Structuring Notation) assurance case diagrams from compliance graph
triggers:
  - "assurance case"
  - "gsn diagram"
  - "safety case"
allowed-tools:
  - Bash
provides:
  - create-assurance-case
composes: [, task-monitor]
---

# create-assurance-case

Generate Goal Structuring Notation (GSN) assurance case diagrams from the
SPARTA compliance graph stored in ArangoDB.  GSN is the standard notation
for structured safety and security arguments (ISO/IEC 15026, OMG SACM).

## Usage

Render a single control as an SVG assurance case:

```bash
./run.sh render --control AC-1
```

Render every control under a framework:

```bash
./run.sh render --framework NIST-800-171
```

Export raw DOT notation (pipe to `dot` yourself or inspect):

```bash
./run.sh export-dot --control AC-1
```

### Options

| Flag            | Description                                         |
|-----------------|-----------------------------------------------------|
| `--control`     | NIST/CMMC control ID (e.g. `AC-1`, `SC-7`)         |
| `--framework`   | Framework name; renders all controls under it        |
| `--output`      | Output file path (`.svg` default, `.png` supported) |
| `--dry-run`     | Generate sample GSN without querying ArangoDB        |

`--dry-run` with `export-dot` requires no external dependencies at all
(no ArangoDB, no graphviz system package).  `--dry-run` with `render`
requires the graphviz system package but not ArangoDB.
