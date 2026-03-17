---
name: editing-obo-ontologies
description: Skills and tools for editing OBO format ontologies, including querying terms, checking out/checking in individual terms, and following OBO format conventions. Do not use this if the source for the ontology you are editing is not in obo format (e.g. ofn)
---

# OBO Ontology Editing Guide

This skill provides guidance and tools for editing ontologies in OBO format.

## Project Layout Conventions

Most OBO ontologies follow a similar structure:
- Main development file is typically `src/ontology/{ontology}-edit.obo`
- Individual terms can be checked out to `terms/` directory for editing
- Some projects may have different layouts - check the project's documentation

## Querying Ontology Terms

Use the `obo-grep.pl` script for searching OBO files:

- Look at a specific term by ID:
    - `obo-grep.pl --noheader -r 'id: ONTO:0004177' src/ontology/{ontology}-edit.obo`
- All mentions of an ID:
    - `obo-grep.pl --noheader -r 'ONTO:0004177' src/ontology/{ontology}-edit.obo`
- Search by regex (e.g., all mentions of hand or foot):
    - `obo-grep.pl --noheader -r '(hand|foot)' src/ontology/{ontology}-edit.obo`
- Search is much faster than full file reads
- ONLY search the main edit file (usually `src/ontology/{ontology}-edit.obo`)
- DO NOT do manual greps or read entire files unless necessary

## Before Making Edits

- Read the request carefully and make a plan, especially if there is nuance
- If a PMID is mentioned, try to read it using: `aurelian fulltext PMID:NNNNNN`
- This also works for DOIs and URLs for scientific papers (if accessible)
- ALWAYS check proposed parent terms for consistency
- Check project-specific guidelines if available

## Editing Workflow

### IMPORTANT: Use Checkout/Checkin for Large Files

- Do not edit large ontology files directly
- Use the checkout/checkin workflow for individual terms
- Check out a term: `obo-checkout.pl src/ontology/{ontology}-edit.obo ONTO:1234567 [OTHER_IDS]`
- This creates a single stanza file: `terms/{ontology}_1234567.obo` (note: colon replaced with underscore)
- Edit the small file in the `terms/` folder
- Check back in: `obo-checkin.pl src/ontology/{ontology}-edit.obo ONTO:1234567 [OTHER_IDS]`
- Checking in updates the edit file and removes the file from `terms/`
- You can edit multiple terms in one batch file if needed

### Scripts Available

This skill includes three essential scripts:
1. `obo-grep.pl` - Fast searching of OBO files
2. `obo-checkout.pl` - Extract terms to individual files for editing
3. `obo-checkin.pl` - Merge edited terms back into main file

All scripts are available in your PATH when this skill is loaded.

## OBO Format Guidelines

### Basic Structure

- Term ID format: `ONTO:NNNNNNN` (check project conventions for number of digits)
- Each term requires:
  - `id:` - unique identifier
  - `name:` - human-readable label
  - `namespace:` - ontology namespace
  - `def:` - definition with references in square brackets
- Use standard relationship types: `is_a`, `part_of`, `has_part`, etc.
- Follow existing term patterns for consistency

### Handling New Term Requests (NTRs)

- Check project conventions for temporary ID ranges
- Example: Some projects use ranges like `ONTO:777xxxx` for new terms
- Always check for ID clashes: `grep 'id: ONTO:777' src/ontology/{ontology}-edit.obo`
- NEVER guess ontology IDs - use search tools to find actual terms
- NEVER guess PMIDs for references - do web searches if needed

### Citations and References

- Cite publications appropriately: `def: "..." [PMID:nnnn, doi:mmmm]`
- Fetch full text when needed: `aurelian fulltext <PMID:nnn>` (also works with DOIs and URLs)
- All synonyms should include proper citations
- Never use empty brackets `[]` without a source

### Synonyms

Synonyms should include proper attribution:

**Correct:**
```
synonym: "alternative name" EXACT [PMID:12345678]
synonym: "abbrev" EXACT ABBREVIATION [PMID:12345678]
```

### Relationships and Logical Definitions

- All terms should have at least one `is_a` parent
- Logical definitions follow genus-differentia form
- Text definitions should mirror logical definitions
- Include source attribution for relationships when based on literature:

### Logical Definitions (intersection_of)

Example of proper intersection_of usage:

```
[Term]
id: ONTO:0000715
name: specific disease
def: "A general disease that involves specific location." [PMID:12345678]
is_a: ONTO:0001082 ! general disease
intersection_of: ONTO:0004971 ! general disease
intersection_of: disease_has_location UBERON:0000029 ! specific location
```

Note that in OWL this corresponds to: `'specific disease' EquivalentTo 'general disease' and 'disease has location' some 'specific location'`

## Obsoleting Terms

- Obsolete terms should have NO logical axioms (`is_a`, `relationship`, `intersection_of`)
- Obsolete terms may have one `replaced_by` tag (exact replacement)
- Or multiple `consider` tags (suggested alternatives)
- Always include obsolescence reason and tracker reference

Example of simple obsolescence:

```
[Term]
id: ONTO:0100334
name: obsolete term name
property_value: IAO:0000231 OMO:0001000
property_value: IAO:0000233 "https://github.com/{project}/issues/XXXX" xsd:anyURI
is_obsolete: true
replaced_by: ONTO:0100321
```

Example with considerations instead of replacement:

```
[Term]
id: ONTO:0100229
name: obsolete term name
def: "OBSOLETE. Original definition here." [original references]
property_value: IAO:0000231 OMO:0001000
property_value: IAO:0000233 "https://github.com/{project}/issues/XXXX" xsd:anyURI
is_obsolete: true
consider: ONTO:0100259
consider: ONTO:0100260
```

### Important Notes on Obsolescence

- Synonyms and xrefs can be migrated to replacement terms judiciously
- Never do complete merges with `alt_id` - use obsolescence with replacement instead
- No relationships should point to an obsolete term
- When obsoleting, you may need to rewire other terms to "skip" the obsoleted term

## Metadata Best Practices

- Link to issue trackers: `property_value: IAO:0000233 "https://github.com/{project}/issues/XXXX" xsd:anyURI`
- Sign new terms (don't tag pre-existing terms):
  ```
  property_value: http://purl.org/dc/terms/creator https://orcid.org/0000-0001-2345-6789
  ```
- All terms should have definitions with at least one reference (preferably PMID)
- Dates are typically auto-generated by build processes

## Syntax Checking

Validate OBO syntax using ROBOT:

```bash
robot convert --catalog src/ontology/catalog-v001.xml \
  -i src/ontology/{ontology}-edit.obo \
  -f obo \
  -o {ontology}-edit.TMP.obo
```

Use `-vvv` flag for full stack trace if there are errors.

## Design Patterns

Many OBO ontologies use DOSDP (Dead Simple Ontology Design Patterns):
- Check `src/patterns/dosdp-patterns/*.yaml` for project-specific patterns
- Follow existing patterns when creating similar terms
- Common patterns include:
  - Location-based disease patterns
  - Gene-related disease patterns
  - Part-of hierarchies
  - Abnormality patterns


## Important Reminders

- NEVER guess identifiers of any kind
- If you include an identifier not provided by the user, you MUST verify it
- PMIDs can be checked with `aurelian` or web search
- Always follow project-specific conventions and check existing examples
- When in doubt, ask for clarification rather than making assumptions
