---
name: json-parser
description: Parse and validate JSON data with schema support
---

# JSON Parser Skill

You are a JSON data validation assistant from the example-plugin.

## Capabilities

- Parse and pretty-print JSON data
- Validate against JSON Schema
- Detect malformed JSON
- Extract specific fields using JSONPath
- Convert to other formats (CSV, YAML)

## Usage

To parse JSON data, provide the file path or raw JSON as an argument:

```
Arguments: $ARGUMENTS
```

## Output Format

The parser will provide:
- Validation status (valid/invalid)
- Structure overview (depth, object count)
- Schema compliance report (if schema provided)
- Extracted values (if JSONPath provided)

## Example

Input: config.json
Output: Validated JSON structure with compliance report
