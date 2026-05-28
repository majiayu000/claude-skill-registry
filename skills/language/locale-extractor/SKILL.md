---
name: Locale Extractor
version: 1.0.0
description: Tools to extract hardcoded text from Liquid files and replace them with translation keys.
allowed-tools:
  - extract_locales
---

## Capabilities

Helps developers internationalize their themes by finding hardcoded strings and moving them to a locale JSON structure.

## Tools Usage Guide

### 1. `extract_locales`

Scans Liquid content for hardcoded text inside HTML tags and proposes replacements.

- **Param** `liquid_content`: The raw liquid code.
- **Param** `section_name`: The name of the section (used for key namespacing).
- **Returns**:
  - `modified_liquid`: The code with `{{ 'key' | t }}` replacements.
  - `new_locales`: A JSON object with the extracted keys and values.

#### Example

**Input**:

```liquid
<h1>Hello World</h1>
<p>Welcome to our store</p>
```

**Output**:

```json
{
  "modified_liquid": "<h1>{{ 'sections.header.hello_world' | t }}</h1>\n<p>{{ 'sections.header.welcome' | t }}</p>",
  "new_locales": {
    "sections": {
      "header": {
        "hello_world": "Hello World",
        "welcome": "Welcome to our store"
      }
    }
  }
}
```
