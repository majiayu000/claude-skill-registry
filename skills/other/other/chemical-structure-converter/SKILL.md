---
name: chemical-structure-converter
description: Convert between IUPAC names, SMILES strings, molecular formulas, and common names for chemical compounds. Supports SMILES validation, batch processing, structure standardization, and cheminformatics database preparation for drug discovery workflows.
license: MIT
skill-author: AIPOCH
---

# Chemical Structure Converter

Interconvert between different chemical structure representations including IUPAC names, SMILES strings, molecular formulas, and common names. Essential for cheminformatics workflows, database standardization, and compound registration in drug discovery and chemical research.

**Key Capabilities:**
- **Multi-Format Conversion**: IUPAC names, SMILES, InChI, molecular formulas
- **SMILES Validation**: Validate SMILES syntax for structural correctness
- **Batch Processing**: Process multiple compounds for database standardization
- **Identifier Lookup**: Retrieve all available identifiers for known compounds
- **Structure Standardization**: Normalize chemical representations for consistency

---

## Input Validation

This skill accepts: compound names (common or IUPAC), SMILES strings, or InChI identifiers. Batch input via CSV or plain text list is also supported.

If the request does not involve converting or validating chemical structure identifiers — for example, asking to predict biological activity, perform docking, or interpret spectra — do not proceed. Instead respond:
> "Chemical Structure Converter is designed to interconvert chemical identifiers (names, SMILES, formulas). Please provide a compound name or SMILES string. For other cheminformatics tasks, use a more appropriate tool."

---

## Quick Check

```bash
python -m py_compile scripts/main.py
python scripts/main.py --help
```

## Workflow

1. Confirm the input identifier type (name, SMILES, IUPAC) and desired output format.
2. Validate that the request matches the documented scope; stop if the task requires unsupported assumptions.
3. Run the script or apply the documented conversion path with only the inputs available.
4. Return a structured result separating assumptions, deliverables, risks, and unresolved items.
5. If execution fails or inputs are incomplete, switch to the fallback path and state exactly what blocked full completion.

**Fallback:** If no identifier is provided, respond: "No chemical identifier provided. Please supply a compound name (`--name`), SMILES string (`--smiles`), or IUPAC name (`--iupac`). Cannot convert without an input identifier."

---

## Core Capabilities

### 1. Multi-Format Conversion

```python
from scripts.main import ChemicalStructureConverter
converter = ChemicalStructureConverter()
data = converter.name_to_identifiers("aspirin")
# → IUPAC: 2-acetoxybenzoic acid, SMILES: CC(=O)Oc1ccccc1C(=O)O, Formula: C9H8O4, MW: 180.16
```

| From → To | Use Case |
|-----------|----------|
| **Name → SMILES** | Literature to database |
| **SMILES → IUPAC** | Machine to human readable |
| **IUPAC → SMILES** | Chemical registration |
| **SMILES → Formula** | Quick MW calculation |

### 2. SMILES Validation

```python
is_valid, message = converter.validate_smiles("CC(=O)Oc1ccccc1C(=O)O")
# → True, "Valid SMILES syntax"
```

| Check | Example Error |
|-------|---------------|
| **Parentheses** | `C(=O` — missing closing |
| **Ring closures** | `C1CC` — ring not closed |
| **Atom validity** | `@` — invalid character |

### 3. Batch Processing

```python
for compound in compound_list:
    data = converter.name_to_identifiers(compound)
    if not data:
        print(f"Warning: '{compound}' not found in database")
```

---

## CLI Usage

```text
# Convert by compound name
python scripts/main.py --name aspirin

# Convert SMILES to IUPAC
python scripts/main.py --smiles "CC(=O)Oc1ccccc1C(=O)O"

# Validate SMILES
python scripts/main.py --smiles "CCO" --validate

# List all compounds
python scripts/main.py --list
```

---

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `--name`, `-n` | string | No | Compound name |
| `--smiles`, `-s` | string | No | SMILES string |
| `--iupac`, `-i` | string | No | IUPAC name |
| `--validate` | flag | No | Validate SMILES syntax |
| `--list`, `-l` | flag | No | List available compounds |

---

## Output Requirements

Every final response must make these explicit:

- Objective or requested deliverable
- Inputs used (identifier type and value) and assumptions introduced
- Conversion method applied
- Core result: all available identifiers (SMILES, IUPAC, formula, MW)
- Constraints and risks (local database limited; novel compounds may not be found)
- Unresolved items and next-step checks (validate against PubChem for critical work)

---

## Error Handling

- If no identifier is provided, list the required input options and request clarification.
- If a compound is not found in the local database, flag it and provide direct lookup URLs: `https://pubchem.ncbi.nlm.nih.gov/compound/{compound_name}` and `https://www.chemspider.com/Search.aspx?q={compound_name}`. For programmatic lookup, query the PubChem REST API: `https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/name/{name}/JSON`. The script should automatically query this endpoint when a compound is not found locally.
- If `scripts/main.py` fails, report the failure point and provide manual fallback guidance.
- Do not fabricate SMILES strings, molecular weights, or identifiers.
- **Batch mode:** Include a summary line: `X/N compounds converted successfully, Y failed (list failed compound names).`
- **Database versioning:** The local compound database version is tracked in `DB_VERSION` in `scripts/main.py`. To add compounds, update the `COMPOUND_DB` dict and increment `DB_VERSION`.

---

## Common Pitfalls

- **Ambiguous names**: Use CAS numbers or specific synonyms for unambiguous lookup
- **Stereochemistry omitted**: Specify @/@@ in SMILES for chiral compounds
- **Hydrates vs anhydrous**: Always specify form (e.g., "caffeine anhydrous")
- **Duplicate entries**: Deduplicate by canonical SMILES when building databases
- **Character encoding**: Use UTF-8 for IUPAC names with special characters

---

## SMILES Quick Reference

- `C` = aliphatic carbon, `c` = aromatic carbon
- `=` = double bond, `#` = triple bond
- `()` = branching, `[]` = explicit valence/charge
- `@` = anticlockwise (S), `@@` = clockwise (R)

---

## References

- PubChem: https://pubchem.ncbi.nlm.nih.gov
- ChemSpider: http://www.chemspider.com
- SMILES Specification: http://opensmiles.org
- RDKit Documentation: https://www.rdkit.org/docs/

**Known Limitation:** Local database contains common compounds only. Integrate PubChem API for production use.
