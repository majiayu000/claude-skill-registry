---
name: structured-output-fabric
description: This skill should be used when the user requests "get JSON with fields X, Y, Z", "need JSON output from this text", "create structured JSON from", or provides a JSON schema they want extracted from input data. Use this for converting ANY text into structured JSON format.
version: 0.1.0
---

# Text to Structured JSON Conversion

This skill enables Claude to automatically convert any text into clean, structured JSON output when the user specifies desired JSON fields or structure.

## Purpose

When users request structured data extraction (e.g., "I need JSON with name, tags, and summary from this text"), Claude executes an automated workflow to deliver clean JSON matching the requested schema.

## Scope

**What this skill does:**
- Converts ANY text input into structured JSON with specified fields
- Accepts text from any source: files, API responses, command output, user input, or other tools
- Generates prompts that enforce strict JSON-only output
- Validates and cleans the resulting JSON

**What this skill does NOT do:**
- Does NOT decide which analysis patterns to use (pattern selection is outside this skill's scope)
- Does NOT determine what fields to extract (user or calling skill specifies the schema)
- Does NOT interpret or analyze content meaning (only structures it as JSON)

## Core Workflow

Execute these steps automatically when the user requests structured JSON:

### 1. Parse JSON Requirements

Identify from the request:
- Desired JSON field names
- Field types (string, array, object)
- Any constraints (max length, format, etc.)
- The source text to structure

### 2. Generate Base Prompt

Create a prompt specifying the exact JSON structure:

```
Convert the provided text into JSON with this exact structure:

{
  "field1": "<description>",
  "field2": ["<items>"],
  "field3": {<nested>}
}

Requirements:
- field1: [constraints from request]
- field2: [constraints from request]
- field3: [constraints from request]

Return ONLY the JSON object. No explanations, no markdown code fences.
```

Write this to a temporary file.

### 3. Improve Prompt with Fabric

Execute:

```bash
cat base_prompt.txt | fabric -p improve_prompt -o improved_prompt.txt >/dev/null 2>&1
```

This enhances the prompt with:
- Clearer instructions
- Stronger "return ONLY JSON" emphasis
- Better field descriptions

### 4. Combine Prompt with Source Text

Create complete input by concatenating:
- Improved prompt
- Separator line
- Source text to be structured

### 5. Execute with Fabric raw_query

Run:

```bash
cat full_input.txt | fabric -p raw_query -m claude-3-5-haiku-latest -o output.txt >/dev/null 2>&1
```

Use `claude-3-5-haiku-latest` for speed and cost-efficiency. Use `claude-3-5-sonnet-latest` only if complex structuring is needed.

### 6. Extract and Validate Clean JSON

Execute the extraction script and validate:

```bash
bash scripts/extract_json_from_llm.sh output.txt > clean.json

if jq '.' clean.json >/dev/null 2>&1; then
  cat clean.json
else
  # Handle error - retry or inform user
fi
```

Return the validated JSON directly to the user.

## Example User Interactions

### Example 1: Converting Log Output to JSON

**User:** "Need JSON with timestamp, level, and message from this log text: [2024-03-15 10:30:45] ERROR Database connection failed"

**Claude does:**
1. Identifies fields: timestamp (string), level (string), message (string)
2. Creates prompt with that structure
3. Improves with fabric
4. Executes raw_query on log text
5. Extracts clean JSON
6. Returns:

```json
{
  "timestamp": "2024-03-15 10:30:45",
  "level": "ERROR",
  "message": "Database connection failed"
}
```

### Example 2: Nested Structure from API Response

**User:** "Extract JSON with: {name, contact: {email, phone}, tags: []} from this text"

**Claude does:**
1. Recognizes nested object structure
2. Generates appropriate prompt
3. Executes workflow
4. Returns:

```json
{
  "name": "John Doe",
  "contact": {
    "email": "john@example.com",
    "phone": "+1234567890"
  },
  "tags": ["customer", "premium", "active"]
}
```

### Example 3: With Constraints from File Content

**User:** "Get JSON with title (max 80 chars), priority (low/medium/high), items array from README.md"

**Claude does:**
1. Reads file content
2. Incorporates constraints into prompt
3. Executes workflow
4. Returns constrained JSON

## Using the Provided Scripts

### scripts/extract_json_from_llm.sh

Automatically extract JSON from fabric output:

```bash
bash scripts/extract_json_from_llm.sh fabric_output.txt > clean.json
```

Works with stdin:

```bash
cat fabric_output.txt | bash scripts/extract_json_from_llm.sh > clean.json
```

## Handling Edge Cases

### User Provides Schema Explicitly

When user shows exact JSON structure:

```
User: "Give me this JSON: {name: string, count: number}"
```

Use their structure directly in the prompt.

### Multiple Interpretations

If field requirements are ambiguous, choose the most reasonable interpretation:
- "tags" � array of strings
- "metadata" � object
- "count" � number
- "description" � string

### Invalid JSON Output

If extraction fails validation:
1. Check fabric output for errors
2. Retry with stronger "ONLY JSON" emphasis in prompt
3. If still failing, inform user of the issue

## Model Selection

Choose fabric model based on task:

- **haiku** (default): Simple extraction, clear structures
- **sonnet**: Complex analysis, nuanced requirements

Always use haiku unless user explicitly needs deeper analysis.

## Complete Automation Example

When user says: "Convert this text to JSON with name and email: John works at john@example.com"

Execute this workflow automatically:

```bash
# 1. Create base prompt
cat > /tmp/base.txt << 'EOF'
Convert the provided text into JSON with this exact structure:
{
  "name": "<person's name>",
  "email": "<email address>"
}
Return ONLY JSON.
EOF

# 2. Improve
fabric -p improve_prompt -o /tmp/improved.txt < /tmp/base.txt

# 3. Combine with input
(cat /tmp/improved.txt; echo ""; echo "Text: John works at john@example.com") > /tmp/full.txt

# 4. Execute
fabric -p raw_query -m claude-3-5-haiku-latest -o /tmp/out.txt < /tmp/full.txt

# 5. Extract and validate
bash scripts/extract_json_from_llm.sh /tmp/out.txt | jq '.'
```

Return result to user.

## Key Principles

1. **Source agnostic**: Accept text from ANY source (files, APIs, commands, user input)
2. **Schema driven**: User specifies the JSON structure, skill performs conversion
3. **Automate fully**: User gets JSON, not instructions
4. **Execute workflow**: Run all steps automatically
5. **Validate output**: Ensure clean, valid JSON before returning

## Assets Usage

### assets/prompt_template.txt

Reference this template when generating base prompts. Replace placeholders with user's requirements.

## Additional Resources

For implementation details:
- **`references/prompt_engineering.md`** - Prompt construction techniques
- **`references/json_extraction_methods.md`** - Extraction method details

For examples:
- **`examples/example_workflow.sh`** - Complete automation script
- **`examples/basic_prompt.txt`** - Simple prompt before improvement
- **`examples/improved_prompt.txt`** - After fabric enhancement

## Summary

When user requests structured JSON from any text source:

1. Parse their requirements (fields, types, constraints)
2. Generate base prompt with structure
3. Improve with `fabric -p improve_prompt`
4. Combine with source text
5. Execute `fabric -p raw_query`
6. Extract and validate JSON with `scripts/extract_json_from_llm.sh` and `jq`
7. Return clean JSON to user

The entire workflow executes automatically—user receives only the final JSON result.

This skill focuses solely on text-to-JSON conversion. Pattern selection and content analysis decisions are outside this skill's scope.
