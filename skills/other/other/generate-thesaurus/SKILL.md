---
name: generate-thesaurus
description: Generate controlled vocabulary thesaurus for content domains. Creates comprehensive thesauri with preferred terms, broader/narrower/related terms.
required_roles:
  scribe: roles/scribe.editor
personas: [information-architect, technical-writer, content-strategist]
---

# Generate Thesaurus Skill

Generate a controlled vocabulary thesaurus for a specified content domain or directory. This skill analyzes content to identify key terms and structures them into a thesaurus with relationships (broader, narrower, related terms).

## Inputs

- `PATH` - The directory or file path to analyze (e.g., "/docs/security")
- `RECURSIVE` - (Optional) Boolean, whether to include subdirectories (default: true)
- `OUTPUT_FORMAT` - (Optional) Format of the output: "markdown", "yaml", "json", "csv" (default: "markdown")

## Workflow

### Step 1: Content Analysis

Analyze the content at `PATH` to identify frequently used terms, concepts, and entities. This involves scanning documentation files (Markdown, Text, etc.) to extract potential vocabulary candidates.

### Step 2: Term Extraction & Relationship Mapping

Identify relationships between terms based on context and standard taxonomies:
- **Preferred Terms**: The standard term to be used (e.g., "Multi-Factor Authentication" instead of "MFA").
- **Broader Terms**: More general concepts (e.g., "Access Control" is broader than "Authentication").
- **Narrower Terms**: More specific sub-concepts (e.g., "Biometrics" is narrower than "Authentication").
- **Related Terms**: Associative relationships (e.g., "Identity Management" is related to "Authentication").

### Step 3: Thesaurus Generation

Format the collected terms and relationships into the requested `OUTPUT_FORMAT`.

**Example Output (Markdown):**
```markdown
# Security Thesaurus

## Authentication
*   **Scope Note**: verification of the identity of a user, process, or device
*   **Broader Term**: Access Control
*   **Narrower Terms**: Multi-Factor Authentication, Single Sign-On
*   **Related Terms**: Authorization, Identity Management
```

## Required Outputs

A `THESAURUS_DOCUMENT` in the specified `OUTPUT_FORMAT` containing:
- List of terms
- Relationships (BT, NT, RT)
- Scope notes (definitions)
- Synonyms or "Use For" entries

## Quick Reference

- **Purpose**: Ensure consistent terminology and improve content findability.
- **Best Practice**: Include scope notes for ambiguous terms.
- **Standards**: Follows ISO 25964 standards for thesaurus construction where applicable.
