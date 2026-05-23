---
name: ingest-compliance-doc
description: >
  Single-command compliance document ingestion pipeline. Chains extractor →
  cui-marker → doc2qra → taxonomy → memory for defense/compliance PDFs.
  Handles NIST, CMMC, DISA STIG, and ITAR documents end-to-end.
allowed-tools:
  - run_command
  - read_file
triggers:
  - ingest compliance
  - ingest nist
  - ingest stig
  - ingest cmmc
  - compliance document
  - ingest itar document
  - compliance ingestion
metadata:
  short-description: End-to-end compliance document ingestion pipeline
provides:
  - ingest-compliance-doc
composes:
  - extractor
  - cui-marker
  - doc2qra
  - taxonomy
  - memory
  - task-monitor
taxonomy:
  - security
  - compliance
---

# Ingest Compliance Document

Single command to ingest a defense/compliance PDF through the full pipeline:

```
PDF → extractor → cui-marker → doc2qra → taxonomy → memory
```

## Commands

| Command | Description |
|---------|-------------|
| `./run.sh ingest <path>` | Full pipeline on a PDF/URL |
| `./run.sh ingest <path> --preset nist_controls` | Force NIST control preset |
| `./run.sh ingest <path> --dry-run` | Show what would happen without executing |
| `./run.sh ingest <path> --skip-cui` | Skip CUI marking (for public documents) |
| `./run.sh batch <dir>` | Process all PDFs in a directory |
| `./run.sh status` | Show pipeline health (all skills available?) |

## Pipeline Stages

### Stage 1: Extract (extractor skill)
- Profile document to detect preset (nist_controls, requirements_spec, etc.)
- Extract sections, tables, figures via deterministic pipeline
- Output: structured JSON + markdown

### Stage 2: CUI Check (cui-marker skill)
- Scan extracted text for CUI indicators
- Apply appropriate markings to ArangoDB document metadata
- Flag legacy markings (FOUO, SBU) for conversion

### Stage 3: QRA Extraction (doc2qra skill)
- Generate QRA triplets via LLM
- Grounding validation filters hallucinations

### Stage 4: Taxonomy (taxonomy skill)
- Extract federated taxonomy tags (bridges: Precision, Resilience, etc.)
- Map NIST control families to taxonomy domains

### Stage 5: Memory Storage (memory skill)
- Store QRAs with taxonomy tags in ArangoDB
- Create graph edges between controls and requirements
- Enable multi-hop recall for compliance queries

### Stage 6: Control Extraction (automatic via extractor s12)
- Extractor's s12_framework_mapper runs automatically during Stage 1
- Extracts NIST, CWE, ATT&CK, SPARTA, D3FEND, ISO control references from document chunks
- Creates `chunk_control_edges` (evidence: document references control)
- Creates `requirement_control_edges` for requirements (SHALL/MUST language, tables, specs)
- Queues `proof_jobs` for `/lean4-prove` formal verification of requirement→control claims
- 3-tier extraction: regex (wide net) → RapidFuzz (validate vs 7K control catalog) → classifier (future)
- Enables `/memory recall` to traverse from compliance documents directly to the controls they reference

## Supported Document Types

| Type | Detected By | Preset |
|------|------------|--------|
| NIST SP 800-171 | "NIST SP", control IDs (AC-*, SC-*) | nist_controls |
| NIST SP 800-53 | "NIST SP", control catalog format | nist_controls |
| DISA STIG | "STIG", V-number findings | requirements_spec |
| CMMC Assessment Guide | "CMMC", "Cybersecurity Maturity" | requirements_spec |
| ITAR/EAR Documents | Export control markers | requirements_spec |
| Engineering Specs | REQ-xxx, "Shall" language | requirements_spec |

## Example

```bash
# Ingest NIST SP 800-171
./run.sh ingest ~/Downloads/sp800-171r2.pdf

# Output:
# [1/5] Extracting... (detected preset: nist_controls, 113 pages)
# [2/5] CUI scanning... (detected: INFOSEC, marking applied)
# [3/5] Generating QRAs... (110 controls → 342 QRAs)
# [4/5] Extracting taxonomy... (14 families mapped)
# [5/5] Storing to memory... (342 QRAs stored, 156 edges created)
# Done. 342 QRAs ingested to scope: compliance
```
