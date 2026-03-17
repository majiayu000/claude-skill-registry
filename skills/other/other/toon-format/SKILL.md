---
name: toon-format
description: "TOON (Token-Oriented Object Notation) encoding for LLM-efficient data representation. 30-60% token savings vs JSON for structured data."
---

# TOON Format Skill

TOON is a compact, human-readable encoding of JSON designed for LLM prompts.

## Variables

| Variable | Default | Description |
|----------|---------|-------------|
| VALIDATION_MODE | strict | `strict` (CLI validation required) or `lenient` (parser permissive) |
| AUTO_FIX | true | Run fix scripts automatically on validation failure |

## Instructions

**MANDATORY** - Follow the format rules in this skill and `reference/format-rules.md`.

- Always include explicit `[count]` for arrays
- Use 2-space indentation for tabular rows
- Add blank line after tabular arrays to terminate them
- Use semicolons for nested arrays in cells (NOT commas)

## Red Flags - STOP and Reconsider

If you're about to:
- Put commas inside quoted strings in tabular cells
- Omit the `[count]` from array declarations
- Forget the blank line after a tabular array
- Use YAML-style `- item` list syntax
- Add comments with `#`

**STOP** -> Check `reference/format-rules.md` -> Then proceed

## Workflow

1. [ ] Determine if TOON is appropriate (see "When to Use TOON" below)
2. [ ] Design data structure for tabular representation
3. [ ] **CHECKPOINT**: Verify format matches rules
4. [ ] Write TOON with proper indentation
5. [ ] Validate with `npx @toon-format/cli --decode`
6. [ ] If errors, run auto-fix scripts from `reference/validation-tools.md`

## Cookbook

### Format Rules
- IF: Writing or editing TOON files
- THEN: Read `reference/format-rules.md`
- COVERS: Syntax rules, constraints, correct patterns

### Validation & Fixing
- IF: TOON file fails validation
- THEN: Read `reference/validation-tools.md`
- COVERS: CLI validation, auto-fix scripts

## When to Use TOON

**Good candidates:**
- Uniform tabular data (lists of similar objects)
- Documentation indexes and manifests
- Repeated key-value structures
- Any structured data being fed to LLMs

**Use JSON instead for:**
- Deeply nested structures
- Non-uniform data (mixed schemas)
- Data requiring frequent programmatic manipulation
- Configuration files read by tools

## TOON Syntax

### Key-Value (YAML-like)
```toon
name: John
age: 30
active: true
```

### Arrays with Explicit Length
```toon
tags[3]: red, green, blue
```

### Tabular Data (Primary Use Case)
```toon
# Syntax: name[count]{col1,col2,col3}:
# Followed by 2-space indented CSV-like rows

users[3]{id,name,email}:
  1,John,john@example.com
  2,Jane,jane@example.com
  3,Bob,bob@example.com
```

**IMPORTANT**: Rows MUST be indented with 2 spaces. Always add a blank line after the last row.

### Nested Arrays in Cells
Use semicolons or quote values containing multiple items:
```toon
pages[2]{path,keywords,priority}:
/intro,"overview;basics;start",core
/api,"reference;methods;types",core
```

### Multi-line Strings
Use quoted strings with `\n` for line breaks:
```toon
description: "This is a multi-line\nstring value that preserves\nline breaks."
```

### Nested Objects
```toon
config:
  database:
    host: localhost
    port: 5432
  cache:
    enabled: true
```

## Encoding Patterns for Documentation

### Index Files
```toon
meta:
  category: libraries
  generated: 2025-01-15T10:30:00Z
  count: 5

items[5]{id,name,description,path,keywords}:
baml,BAML,Structured LLM outputs,ai-docs/libraries/baml/_index.toon,"llm;types;structured"
mcp,MCP,Tool integration protocol,ai-docs/libraries/mcp/_index.toon,"tools;context;servers"
prisma,Prisma,Type-safe database ORM,ai-docs/libraries/prisma/_index.toon,"database;orm;sql"
```

### Page Summaries
```toon
meta:
  library: baml
  page: error-handling
  source_url: https://docs.boundaryml.com/guide/error-handling
  content_hash: a3f2c1d4e5

summary:
  purpose: "Configure retry policies and fallback strategies for resilient LLM calls."

  key_concepts[4]: RetryPolicy,FallbackClient,timeout,exponential backoff

  gotchas[2]: Default timeout 60s may be too short,Retries count against rate limits

code_patterns[1]:
  - lang: baml
    desc: Retry policy configuration
    code: "retry_policy Resilient {\n  max_retries 3\n  strategy exponential\n}"
```

## Token Comparison

**JSON** (~280 tokens):
```json
{"pages":[{"path":"/intro","section":"guide","title":"Introduction","priority":"core"},{"path":"/setup","section":"guide","title":"Setup","priority":"core"}]}
```

**TOON** (~100 tokens):
```toon
pages[2]{path,section,title,priority}:
/intro,guide,Introduction,core
/setup,guide,Setup,core
```

**Savings: ~64%**

## Tools & Libraries

- **TypeScript/JS**: `@toon-format/toon` (npm)
- **Python**: `python-toon` (pip)
- **Online**: https://toontools.vercel.app/playground
- **Spec**: https://toonformat.dev/

## Best Practices

1. Design data structures for tabular representation when possible
2. Use explicit `[count]` for arrays - helps LLM parsing
3. Keep JSON as canonical source, TOON for LLM transport
4. Use semicolons for nested arrays (e.g., `"val1;val2;val3"`)
5. Truncate long strings (code snippets < 200 chars)
6. Always add a blank line after tabular arrays to terminate them

## Format Constraints

**Enforced by official `@toon-format/cli` (use `--decode` to validate):**

| Rule | ❌ Incorrect | ✅ Correct |
|------|-------------|-----------|
| No comments | `# comment` | (remove comments entirely) |
| No YAML-style lists | `- item` | `key[N]{col}:` + indented rows |
| Rows must be indented | `row,data` | `  row,data` (2 spaces) |
| Arrays need count+cols | `items{a,b}:` | `items[3]{a,b}:` |
| No multiline strings | `key: \|` | `key: "line1\nline2"` |
| No pipe delimiters | `val\|val` | `val,val` or `"val;val"` |
| No commas in tabular cells | `"a,b"` | `"a;b"` |
| Blank line AFTER arrays | missing terminator | blank line after last row |

**Validation tools:**
```bash
# Validate with official CLI (use --decode, not validate!)
npx @toon-format/cli --decode file.toon > /dev/null

# Auto-fix common issues (run in this order)
python3 .claude/ai-dev-kit/dev-tools/scripts/fix_toon_comments.py path/
python3 .claude/ai-dev-kit/dev-tools/scripts/fix_toon_yaml_lists.py path/
python3 .claude/ai-dev-kit/dev-tools/scripts/fix_toon_nested_lists.py path/
python3 .claude/ai-dev-kit/dev-tools/scripts/fix_toon_commas.py path/
python3 .claude/ai-dev-kit/dev-tools/scripts/fix_toon_pipes.py path/
python3 .claude/ai-dev-kit/dev-tools/scripts/fix_toon_multiline.py path/
python3 .claude/ai-dev-kit/dev-tools/scripts/fix_toon_blank_lines.py path/
```

