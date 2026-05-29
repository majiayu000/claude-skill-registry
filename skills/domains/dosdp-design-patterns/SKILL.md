---
name: dosdp-design-patterns
description: Skills for understanding and applying DOSDP (Dead Simple Ontology Design Patterns) to ensure consistent ontology term creation and maintenance. This skill is about recognizing patterns and ensuring consistency, not using dosdp-tools directly.
---

# DOSDP Design Patterns Guide

This skill helps you understand, identify, and apply Dead Simple Ontology Design Patterns (DOSDP) when creating or editing ontology terms.

## What are DOSDP Patterns?

DOSDP patterns are templates that ensure consistent naming, definitions, and logical axioms across similar types of ontology terms. They encode best practices for term construction and help maintain consistency in:

- **Term naming conventions** - How terms should be named
- **Text definitions** - Standard definition templates
- **Logical definitions** - OWL equivalence axioms (intersection_of in OBO)
- **Synonyms** - Standard synonym patterns
- **Relationships** - Which relationships to use

## Why Design Patterns Matter

1. **Consistency**: All terms following the same pattern have the same structure
2. **Quality**: Patterns encode domain expertise and best practices
3. **Automation**: Pattern-based terms can be generated or validated automatically
4. **Reasoning**: Logical definitions enable automated classification
5. **Maintenance**: Updates to patterns can be applied systematically

## Pattern File Structure

DOSDP patterns are defined in YAML files with this structure:

```yaml
pattern_name: pattern_name_here

description: 'Human-readable description with examples'

classes:
  # Upper-level classes used in the pattern
  disease: MONDO:0000001

relations:
  # Relations used in logical definitions
  disease has location: RO:0004026

vars:
  # Variables that will be filled in
  disease: "'disease'"
  location: "'anatomical entity'"

name:
  # Template for term name
  text: '%s of %s'
  vars: [disease, location]

def:
  # Template for definition
  text: 'A %s that involves the %s.'
  vars: [disease, location]

equivalentTo:
  # Logical definition template (OWL equivalence)
  text: "%s and 'disease has location' some %s"
  vars: [disease, location]
```

## Common Pattern Types

### Location-Based Patterns

**Pattern**: `location.yaml`

Used when a disease/phenotype affects a specific anatomical location.

**Structure**:
- Name: `{disease} of {location}` or `{location} {disease}`
- Definition: `A {disease} that involves the {location}.`
- Logic: `{disease} and 'disease has location' some {location}`

**Examples**:
- lymph node adenoid cystic carcinoma
- articular cartilage disease
- urethral disease

**When to use**: Creating terms for diseases in specific anatomical locations

### Gene-Based Disease Patterns

**Pattern**: `disease_series_by_gene.yaml`

Used for diseases caused by mutations in a specific gene.

**Structure**:
- Name: `{disease} caused by variation in {gene}` or `{gene}-related {disease}`
- Definition: `Any {disease} in which the cause of the disease is a variation in the {gene} gene.`
- Logic: `{disease} and 'has material basis in germline mutation in' some {gene}`
- Relationship: `has_material_basis_in_germline_mutation_in {gene_id}`

**Examples**:
- MED12-related intellectual disability syndrome
- TTN-related myopathy
- MYCBP2-related developmental delay with corpus callosum defects

**When to use**: Creating terms for monogenic diseases with gene-based names

**Important notes**:
- Always verify gene identifiers (HGNC for human, NCBI Gene for non-human)
- Use the pattern's naming convention even if users request different formats
- Include proper source attribution in relationships

### Age of Onset Patterns

**Patterns**: `childhood.yaml`, `adult.yaml`, `infantile.yaml`

Used for diseases characterized by onset at specific life stages.

**Structure**:
- Name: `{age_stage} {disease}`
- Definition: `A {disease} that occurs during {age_stage}.`
- Logic: `{disease} and 'has characteristic' some {age_characteristic}`

**Examples**:
- childhood astrocytic tumor
- adult neuronal ceroid lipofuscinosis
- infantile epilepsy

**When to use**: Creating age-specific variants of diseases

### Inheritance Pattern Terms

**Patterns**: `autosomal_dominant.yaml`, `autosomal_recessive.yaml`, `x_linked.yaml`, `y_linked.yaml`

Used for diseases with specific inheritance patterns.

**Examples**:
- autosomal dominant polycystic kidney disease
- autosomal recessive intellectual disability

**When to use**: Creating terms that emphasize inheritance mode

### Neoplasm/Cancer Patterns

**Patterns**: `cancer.yaml`, `carcinoma.yaml`, `benign.yaml`, `malignant.yaml`, `sarcoma.yaml`

Used for various types of neoplastic diseases.

**Examples**:
- lung cancer
- squamous cell carcinoma of skin
- benign neoplasm of breast

**When to use**: Creating cancer/tumor-related terms

### Process-Based Patterns

**Pattern**: `basis_in_disruption_of_process.yaml`

Used for diseases characterized by disruption of a biological process.

**Structure**:
- Logic includes: `'has basis in disruption of' some {process}`

**When to use**: Diseases with clear mechanistic etiology

### Other Common Patterns

- **Inflammatory diseases**: `inflammatory_disease_by_site.yaml`
- **Infectious diseases**: `infectious_disease_by_agent.yaml`
- **Allergies**: `allergy.yaml`, `allergic_form_of_disease.yaml`
- **Rare diseases**: `rare.yaml`, `rare_genetic.yaml`
- **Clinical forms**: `isolated.yaml`, `syndromic.yaml`, `acute.yaml`, `chronic.yaml`

## Applying Patterns: Step-by-Step Process

### Step 1: Identify the Applicable Pattern

Before creating a new term, ask:

1. What is the primary distinguishing characteristic?
   - Location? → Use location pattern
   - Gene? → Use disease_series_by_gene pattern
   - Age of onset? → Use childhood/adult/infantile pattern
   - Cell/tissue type? → Use neoplasm_by_origin or similar
   - Process disrupted? → Use basis_in_disruption_of_process

2. Check pattern directory:
   - Look in `src/patterns/dosdp-patterns/*.yaml`
   - Read pattern descriptions
   - Review examples in the pattern file

3. Examine similar existing terms:
   - Use obo-grep or search to find similar terms
   - Check their structure for consistency

### Step 2: Verify Pattern Components

Once you've identified a pattern, gather the required information:

1. **Variable values**: What will fill the pattern slots?
   - For gene patterns: Verify gene identifier (HGNC/NCBI Gene)
   - For location patterns: Find UBERON/CL term
   - For agent patterns: Find NCBITaxon or other appropriate ID

2. **Parent class**: What is the upper-level class?
   - Should match the pattern's requirement
   - Verify it's the most specific appropriate parent

3. **References**: What sources support this term?
   - PMIDs for definitions
   - Sources for relationships
   - Attribution for synonyms

### Step 3: Apply the Pattern Structure

Create the term following the pattern's template:

**Name**: Follow the pattern's naming convention exactly
- Don't deviate even if user requests different format
- Pattern ensures consistency across the ontology

**Definition**: Use the pattern's definition template
- Fill in variables appropriately
- Add clinical details if needed
- Include proper citations

**Logical definition**: Create intersection_of axioms
```
intersection_of: {parent_class}
intersection_of: {relation} {filler}
```

**Relationships**: Add appropriate relationship statements
```
relationship: {relation} {target} {source="PMID:xxxxx"}
```

**Synonyms**: Follow pattern's synonym templates
- Add with proper scope (EXACT, RELATED, etc.)
- Include citations

### Step 4: Verify Pattern Compliance

Check that your term follows the pattern:

1. **Name matches template**: Does it follow the `name:` section?
2. **Definition matches template**: Does it follow the `def:` section?
3. **Logic is complete**: Are all `intersection_of` axioms present?
4. **Relationships included**: Are redundant relationships present with attribution?
5. **Synonyms follow patterns**: Do they match `annotations:` section?

## Pattern Compliance Examples

### Good Example: Gene-Based Disease Pattern

```
[Term]
id: MONDO:1060117
name: MYCBP2-related developmental delay with corpus callosum defects
def: "Any neurodevelopmental disorder in which the cause of the disease is a mutation in the MYCBP2 gene." [PMID:36200388]
synonym: "MDCD" EXACT ABBREVIATION [PMID:36200388]
synonym: "MYCBP2 neurodevelopmental disorder" EXACT []
is_a: MONDO:0700092 {source="PMID:36200388"} ! neurodevelopmental disorder
intersection_of: MONDO:0700092 ! neurodevelopmental disorder
intersection_of: has_material_basis_in_germline_mutation_in http://identifiers.org/hgnc/23386
relationship: has_material_basis_in_germline_mutation_in http://identifiers.org/hgnc/23386 {source="PMID:36200388"} ! MYCBP2
```

This follows the disease_series_by_gene pattern:
- ✓ Name uses "{gene}-related {disease}" format
- ✓ Definition uses pattern template
- ✓ Has intersection_of axioms
- ✓ Has redundant relationship with source
- ✓ Synonyms follow pattern

### Good Example: Location Pattern

```
[Term]
id: MONDO:0000715
name: lymph node adenoid cystic carcinoma
def: "An adenoid cystic carcinoma that involves the lymph node." [PMID:12345678]
is_a: MONDO:0001082 ! lymph node cancer
is_a: MONDO:0004971 ! adenoid cystic carcinoma
intersection_of: MONDO:0004971 ! adenoid cystic carcinoma
intersection_of: disease_has_location UBERON:0000029 ! lymph node
```

This follows the location pattern:
- ✓ Name uses "{location} {disease}" format
- ✓ Definition uses "A {disease} that involves the {location}" template
- ✓ Has proper intersection_of axioms
- ✓ Both parent classes are present (can be inferred by reasoner)

## Common Pitfalls and How to Avoid Them

### Pitfall 1: Wrong Parent Class

**Problem**: Choosing too specific or too general a parent

**Solution**:
- Use the parent specified in the pattern's `classes:` section
- For gene-based diseases, use the broadest disease category that fits
- Don't default to overly specific parents like "inherited disease"

### Pitfall 2: Incomplete Logical Definitions

**Problem**: Missing intersection_of axioms or relationships

**Solution**: Every pattern requires:
1. All `intersection_of` axioms from the `equivalentTo:` template
2. Redundant relationships (these carry source attribution)

### Pitfall 3: Non-Standard Naming

**Problem**: Deviating from pattern naming conventions

**Solution**:
- Always use pattern's `name:` template
- Add alternative names as synonyms instead
- If user requests different format, create as synonym

### Pitfall 4: Missing Source Attribution

**Problem**: Relationships without source tags

**Solution**: Add source attribution to all asserted axioms:
```
is_a: PARENT:123 {source="PMID:xxxxx"}
relationship: has_basis_in ENTITY:456 {source="PMID:yyyyy"}
```

### Pitfall 5: Unverified Identifiers

**Problem**: Using wrong or guessed gene/anatomy identifiers

**Solution**: Always verify:
- Gene identifiers: Check HGNC (human) or NCBI Gene (other species)
- Anatomy: Search UBERON or species-specific anatomy ontology
- Other entities: Use appropriate source ontology

## Working with Multiple Patterns

Sometimes a term could fit multiple patterns. Guidelines:

1. **Primary characteristic wins**: Choose the pattern that captures the most important distinguishing feature
   - Gene-based name requested? Use disease_series_by_gene
   - Location is key feature? Use location

2. **Combine patterns when appropriate**: Some terms can use multiple patterns
   - Example: "childhood leukemia" uses both childhood and cancer patterns

3. **Avoid pattern conflicts**: Don't mix incompatible patterns
   - Check if patterns are designed to be used together

4. **Consult existing terms**: Look for similar multi-pattern terms in the ontology

## Finding and Reading Pattern Files

### Locating Patterns

Patterns are typically stored in:
- `src/patterns/dosdp-patterns/*.yaml`

### Reading a Pattern File

Key sections to understand:

1. **description**: Explains when to use the pattern, with examples
2. **classes**: Upper-level classes that can fill this slot
3. **relations**: Which relationships the pattern uses
4. **vars**: What variables need to be filled in
5. **name**: How the term should be named
6. **def**: Definition template
7. **equivalentTo**: Logical definition (becomes intersection_of in OBO)
8. **annotations**: Synonym templates

### Pattern Documentation

Many pattern files include:
- Examples of existing terms using the pattern
- Links to related patterns
- Notes about when (and when not) to use the pattern

## Tools and Validation

While this skill focuses on understanding patterns rather than using tools, be aware:

1. **dosdp-tools**: Can generate terms from patterns and TSV data
2. **Pattern validation**: Some ontologies have QC checks for pattern compliance
3. **Pattern files**: Are the source of truth for term structure

## Important Reminders

1. **Always check for applicable patterns** before creating new terms
2. **Follow pattern templates exactly** - consistency is crucial
3. **Verify all identifiers** - never guess gene IDs, anatomy IDs, etc.
4. **Include proper citations** - in definitions, relationships, and synonyms
5. **Check existing similar terms** - ensure your term follows the same pattern
6. **When in doubt, ask** - better to clarify than create inconsistent terms

## Pattern Philosophy

The overall philosophy is to:
- **Split rather than lump**: Have distinct patterns for similar but different cases
  - Example: Separate patterns for "carcinoma" vs "cancer"
- **Capture domain knowledge**: Patterns encode expert knowledge
- **Enable automation**: Well-defined patterns can be processed by tools
- **Maintain consistency**: All terms of a type should look the same
- **Support reasoning**: Logical definitions enable automated classification
