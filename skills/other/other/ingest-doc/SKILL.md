---
name: ingest-doc
description: >
  Single-command document ingestion pipeline. Chains extractor →
  cui-marker → doc2qra → taxonomy → memory for PDFs and documents.
  Handles compliance, research, and general documents end-to-end.
allowed-tools:
  - run_command
  - read_file
triggers:
  - ingest document
  - ingest compliance
  - ingest nist
  - ingest stig
  - ingest cmmc
  - compliance document
  - ingest itar document
  - compliance ingestion
  - convert document to qras
  - document to knowledge
metadata:
  short-description: End-to-end document ingestion pipeline
provides:
  - ingest-doc
composes:
  - extractor
  - doc2qra
  - cui-marker
  - taxonomy
  - memory
  - task-monitor
taxonomy:
  - security
  - compliance
---

# Ingest Document

Single command to ingest a PDF through the full pipeline:

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
- Apply appropriate markings

### Stage 3: QRA Extraction (doc2qra skill)
- Generate QRA triplets via LLM
- Persona-driven quality gating
- Grounding validation filters hallucinations

### Stage 4: Taxonomy (taxonomy skill)
- Extract federated taxonomy tags (bridges: Precision, Resilience, etc.)

### Stage 5: Memory Storage (memory skill)
- Store QRAs with taxonomy tags in ArangoDB
- Create graph edges between controls and requirements

## Supported Document Types

| Type | Detected By | Preset |
|------|------------|--------|
| NIST SP 800-171 | "NIST SP", control IDs (AC-*, SC-*) | nist_controls |
| NIST SP 800-53 | "NIST SP", control catalog format | nist_controls |
| DISA STIG | "STIG", V-number findings | requirements_spec |
| CMMC Assessment Guide | "CMMC", "Cybersecurity Maturity" | requirements_spec |
| ITAR/EAR Documents | Export control markers | requirements_spec |
| Engineering Specs | REQ-xxx, "Shall" language | requirements_spec |
| General PDF/markdown | Any document | auto |
