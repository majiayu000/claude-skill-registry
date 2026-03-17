---
name: pv-mapping
description: >
  Map permissible values in LinkML enums to ontology terms. Use this skill when:
  (1) Adding or updating ontology mappings (meaning: field) for enum permissible values,
  (2) Fixing validation errors from linkml-term-validator,
  (3) User asks to map enums to ontology terms or fix CURIE mappings.
  This skill covers OAK/runoak lookup, CURIE verification, and validation workflows.
---

# Permissible Value Ontology Mapping

## Core Rules

1. **Never change PERMISSIBLE_VALUE names** - Keep uppercase names like `NUCLEIC_ACID`
2. **Use `title:` for ontology label** - Match the ontology term's label
3. **Use `meaning:` for CURIE** - Always verify via runoak before adding
4. **Never guess CURIEs** - Wrong mappings are worse than no mappings

## Workflow

### 1. Look up term via runoak

```bash
# Search for terms
runoak -i sqlite:obo:ncit search "nucleic acid"

# Verify a CURIE exists and get its label
runoak -i sqlite:obo:ncit info NCIT:C706
```

### 2. Add mapping

```yaml
NUCLEIC_ACID:
  title: Nucleic Acids          # matches ontology term label
  description: DNA or RNA sample
  meaning: NCIT:C706            # verified CURIE
```

Note that either the permissible value key, the title, or one of the aliases
should be a (case insensitive) match to the ontology term.

If there is already a canonical `meaning` field, OR the concept is not a close map, then linkml close/narrow/broad/exact mappings can be used:

```yaml
NUCLEIC_ACID:
  title: Nucleic Acids          # matches ontology term label
  description: DNA or RNA sample
  meaning: NCIT:C706            # verified CURIE
  close_mappings:
    - SO:0000348.               # label is nucleic_acid
  aliases:
    - nucleic_acid              # to match SO
```

### 3. Validate

```bash
just validate
```

## Interpreting Validation Errors

| Error Type | Action |
|------------|--------|
| "resolves to [wrong concept]" | **Fix immediately** - CURIE points to wrong term |
| "label mismatch" | Usually OK - add `title:` to match label if needed, or use an aliases |
| "Could not retrieve" | Check CURIE format or remove if term doesn't exist |

## Ontology Selection

See [references/ontologies.md](references/ontologies.md) for:
- Domain-to-ontology mapping (which ontology for which concept type)
- CURIE format patterns for each ontology
- Additional runoak commands

## When to Remove Mappings

Remove `meaning:` when:
- No appropriate ontology term exists
- CURIE consistently fails validation
- Mapped term is semantically incorrect or not the same concept

