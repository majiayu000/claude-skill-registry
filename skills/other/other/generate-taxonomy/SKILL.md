---
name: generate-taxonomy
description: Develop hierarchical classification systems. Creates parent-child categorical structures for content organization.
required_roles:
  scribe: roles/scribe.editor
personas: [information-architect, taxonomist, knowledge-manager]
---

# Generate Taxonomy Skill

Develop a hierarchical classification system or taxonomy for a knowledge base or content repository. This skill creates parent-child categorical structures to organize content effectively.

## Inputs

- `PATH` - The content source to analyze (e.g., "/knowledge-base")
- `FACETED` - (Optional) Boolean, whether to create a faceted classification (multiple dimensions) (default: false)
- `BUSINESS_ALIGNMENT` - (Optional) Boolean, whether to align with specific business goals/terminology (default: true)
- `USER_TESTING` - (Optional) Boolean, whether to include user validation methodologies in the output (default: false)

## Workflow

### Step 1: Content Analysis & Term Extraction

Analyze the content at `PATH` to identify key topics, subjects, and categories.
- Cluster documents by similarity.
- Extract common tags and keywords.

### Step 2: Structure Design

Organize the extracted concepts into a hierarchy.
- **Hierarchical**: Define Broader Terms (Parent) and Narrower Terms (Child).
- **Faceted** (if enabled): Define dimensions (e.g., Topic, Format, Audience, Region).

### Step 3: Business & User Alignment

- Align terms with business vocabulary (if `BUSINESS_ALIGNMENT` is true).
- If `USER_TESTING` is true, generate a plan for card sorting or tree testing to validate the structure.

### Step 4: Taxonomy Definition

Output the defined taxonomy.

## Required Outputs

A `TAXONOMY_DEFINITION` document (e.g., in markdown or YAML format) containing:
- **Taxonomy Tree**: Visual or indented list of categories.
- **Facets** (if requested): Definitions of classification dimensions.
- **Rules**: Guidelines for applying the taxonomy.
- **Testing Plan** (if requested): Methodologies for validation.

## Quick Reference

- **Purpose**: Systematically classify content for retrieval optimization.
- **Types**: Hierarchical (Tree) vs. Faceted (Matrix).
