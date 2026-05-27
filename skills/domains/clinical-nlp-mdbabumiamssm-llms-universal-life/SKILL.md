---name: clinical-nlp-extractor
description: Extracts medical entities (Diseases, Medications, Procedures) from unstructured clinical text using regex and simple rules (or LLM wrappers).
keywords:
  - nlp
  - ner
  - clinical-notes
  - entity-extraction
  - fhir
measurable_outcome: Extracts key medical entities (Problems, Meds) with >80% recall on standard synthesized clinical notes.
license: MIT
metadata:
  author: AI Group
  version: "1.0.0"
compatibility:
  - system: Python 3.10+
allowed-tools:
  - run_shell_command
  - read_file
---"

# Clinical NLP Entity Extractor

The **Clinical NLP Skill** converts free-text clinical notes into structured data. It identifies key medical entities like problems/diagnoses, medications, and procedures.

## When to Use This Skill

*   When analyzing unstructured EHR notes.
*   To populate a patient's problem list or medication reconciliation.
*   To de-identify text (phi-removal) - *Basic version*.

## Core Capabilities

1.  **NER (Named Entity Recognition)**: Extracts Problems, Drugs, Procedures.
2.  **Negation Detection**: (Basic) Checks if a finding is denied ("No fever").
3.  **Structuring**: Returns JSON format compatible with FHIR/USDL.

## Workflow

1.  **Input**: A string of clinical text or a text file.
2.  **Process**: Tokenizes and matches against patterns/dictionaries.
3.  **Output**: JSON list of entities with spans and types.

## Example Usage

**User**: "Extract entities from this note."

**Agent Action**:
```bash
python3 Skills/Clinical/Clinical_NLP/entity_extractor.py \
    --text "Patient has diabetes type 2. Prescribed Metformin 500mg. No chest pain." \
    --output entities.json
```

```