---
name: maker
description: "Generate .NET Core data API code from model definitions using the Maker XML specification and CLI. Use when users need to: (1) Create Maker XML models from JSON objects, SQL scripts, or database schemas, (2) Generate .NET Core CRUD API endpoints from Maker XML, (3) Understand or validate Maker XML model definitions, or (4) Work with the Maker CLI tool for code generation."
---

# Maker - .NET Core Data API Code Generation

## Overview

Maker transforms XML model definitions into complete .NET Core data API endpoints with full CRUD functionality. This skill helps generate Maker XML models from various sources and understand the Maker CLI workflow.

## Workflow Decision Tree

Choose your workflow based on the starting point:

**Starting from JSON or data model?** → Use the [From JSON Workflow](#from-json-or-data-model)  
**Starting from SQL CREATE TABLE script?** → Use the [From SQL Workflow](#from-sql-create-table-script)  
**Starting from existing Maker XML?** → Use the [Understanding Maker XML](#understanding-maker-xml)  
**Need to generate code from Maker XML?** → Use the [CLI Generation Workflow](#cli-generation-workflow)

## From JSON or Data Model

When converting JSON objects or data models to Maker XML:

1. **Read the conversion prompt**: Load `references/Prompt_to_create_Maker_XML_from_json_model.md` to understand the conversion guidelines
2. **Read the specification**: Load `references/Maker_XML_specification.md` for type mappings and patterns
3. **Apply the conversion logic**:
   - Infer relationships from field names ending in `Id`, `ID`, or `_id`
   - Map JSON types to Maker column types (string → text/name/label, boolean → flag, etc.)
   - Suggest property tables for type/status/state fields
   - Add appropriate filters and auto-population attributes
   - Follow Maker naming conventions (IsActive, not Active)
4. **Generate three artifacts**:
   - Maker XML `<Table>` definition
   - Corresponding `<View>` definition
   - Property table initialization SQL (if applicable)

## From SQL CREATE TABLE Script

When converting SQL CREATE TABLE scripts to Maker XML:

1. **Read the conversion prompt**: Load `references/Prompt_to_create_Maker_XML_from_sql_script.md` for SQL-specific guidelines
2. **Read the specification**: Load `references/Maker_XML_specification.md` for type mappings
3. **Apply the conversion logic**:
   - Map SQL types to Maker column types
   - Identify foreign key relationships from column names
   - Improve naming where SQL uses poor conventions
   - Suggest virtual columns for views
   - Add XML comments for assumptions or complex mappings
4. **Generate three artifacts**:
   - Maker XML `<Table>` definition
   - Corresponding `<View>` definition
   - Property table initialization SQL (if applicable)

## Understanding Maker XML

When working with existing Maker XML or needing to understand the specification:

**Read the specification**: Load `references/Maker_XML_specification.md` to understand:
- Column types (identity, text, name, label, note, integer, decimal, flag, datetime, property, uniqueid)
- Table attributes (type, name, description, alias, view, schema, search)
- View definitions and virtual columns
- Property tables and relational patterns
- Auto-population and filtering rules
- Naming conventions and best practices

## CLI Generation Workflow

When generating code from Maker XML models:

**Read the CLI documentation**: Load `references/MakerCLI.md` to understand:
- Command-line syntax and arguments
- Validation-only mode for model verification
- Publishing workflow for deployment
- File placement and integration requirements

**Standard generation command**:
```bash
MakerCLI --modelname=[Name] --publish=false --validate=true
```

**Validation-only mode**:
```bash
MakerCLI --modelname=[Name] --validate=only
```

This performs model validation without generating files, useful for verifying XML before generation.

## Type Mapping Quick Reference

| Source Type | Maker Type | Notes |
|-------------|------------|-------|
| `id`, `guid`, `uuid` | `identity` or `uniqueid` | identity for PKs, uniqueid for tokens |
| `string` (short) | `name`, `label`, or `text` | Based on context/length |
| `string` (medium) | `note` or `text length="note"` | Descriptions |
| `string` (long) | `desc` or `text length="desc"` | Large text, JSON |
| `boolean` | `flag` | Ensure Is/Has/Want/Can prefix |
| `number`, `integer` | `integer` or `decimal` | Based on precision needs |
| `date`, `datetime` | `datetime` | Add auto/update attributes as needed |
| Enum/lookup fields | `property` | Create property table |

## Common Patterns

### Foreign Key Relationships
When a field ends with `Id`, `ID`, or `_id`:
```xml
<Column type="integer" name="SiteID" filter="yes"/>
```

### Property Tables (Type/Status/State)
For enumeration fields:
```xml
<Column type="property" name="Type">
  <Property name="TypeID" table="Type"/>
</Column>
```

With initialization SQL:
```sql
INSERT INTO Type (Code, Name, Description) VALUES 
  ('standard', 'Standard', 'Standard type'),
  ('premium', 'Premium', 'Premium type');
```

### Auto-Populated Timestamps
```xml
<Column type="datetime" name="Created" filter="no" auto="yes" update="no"/>
<Column type="datetime" name="Updated" filter="no" auto="yes" update="yes"/>
```

### Boolean Flags with Correct Naming
```xml
<Column type="flag" name="IsActive"/>  <!-- Correct -->
<!-- Not: <Column type="flag" name="Active"/> -->
```

## References

This skill includes comprehensive reference documentation:

- **Maker_XML_specification.md**: Complete Maker XML specification with all column types, attributes, and patterns
- **MakerCLI.md**: CLI usage, commands, and workflow documentation
- **Prompt_to_create_Maker_XML_from_json_model.md**: JSON-to-XML conversion guidelines
- **Prompt_to_create_Maker_XML_from_sql_script.md**: SQL-to-XML conversion guidelines

Load these references as needed based on the specific conversion or generation task.
