---
name: design-metadata-schema
description: Design comprehensive metadata frameworks. Develops structured metadata templates and tagging systems.
required_roles:
  scribe: roles/scribe.editor
personas: [information-architect, data-architect, content-strategist]
---

# Design Metadata Schema Skill

Develop a comprehensive metadata schema for content management. This skill defines structured fields, validation rules, and standards compliance to improve searchability and management.

## Inputs

- `PATH` - The content domain to apply the schema to (e.g., "/content")
- `OUTPUT_FORMAT` - (Optional) The output format for the schema, e.g., "json-schema", "xml", "markdown" (default: "json-schema")
- `DUBLIN_CORE` - (Optional) Boolean, whether to align with Dublin Core standards (default: true)
- `CUSTOM_FIELDS` - (Optional) List of custom business-specific fields to include
- `VALIDATION_RULES` - (Optional) Boolean, whether to define validation logic for fields (default: true)

## Workflow

### Step 1: Requirement Analysis

Analyze the content types at `PATH` to determine metadata needs.
- Identify common attributes (Title, Date, Author).
- Identify specific attributes (Product ID, Version, Region).

### Step 2: Schema Definition

Define the fields and their properties.
- **Standard Fields**: Map to Dublin Core (Title, Creator, Subject, etc.) if enabled.
- **Custom Fields**: Define fields specified in `CUSTOM_FIELDS` or discovered during analysis.

### Step 3: Constraints & Validation

If `VALIDATION_RULES` is true, define:
- **Data Types**: String, Date, Integer, Boolean, Enum.
- **Required/Optional**: Cardinality constraints.
- **Controlled Vocabularies**: Allowed values for specific fields.

### Step 4: Schema Output

Generate the schema definition in the requested `OUTPUT_FORMAT` (e.g., JSON Schema, XML Schema, or Markdown Table).

## Required Outputs

A `METADATA_SCHEMA` object in the specified `OUTPUT_FORMAT` containing:
- **Field Dictionary**: Name, Description, Type, Multiplicity.
- **Validation Logic**: Rules for data entry.
- **Mapping**: Correspondence to standards (like Dublin Core).

## Quick Reference

- **Purpose**: Standardize content tagging for consistency and interoperability.
- **Standards**: Dublin Core, Schema.org.
