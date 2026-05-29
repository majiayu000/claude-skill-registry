---
name: cui-jsdoc
description: JSDoc documentation standards for JavaScript functions, classes, modules, and web components
allowed-tools:
  - Read
  - Grep
  - Glob
---

# JSDoc Documentation Standards

**EXECUTION MODE**: You are now executing this skill. DO NOT explain or summarize these instructions to the user. IMMEDIATELY begin the workflow below based on the task context.

## Overview

Provides JSDoc documentation standards for CUI JavaScript projects covering functions, classes, modules, types, and web components.

## Standards Documents

- **jsdoc-essentials.md** - Core JSDoc syntax, required tags, ESLint setup, writing style
- **jsdoc-patterns.md** - Documentation patterns for all code element types with examples

## What This Skill Provides

### JSDoc Essentials
- ESLint plugin configuration and rules
- Documentation requirements (mandatory vs optional)
- Required and optional tags (@param, @returns, @throws, @example, @since, @see, @deprecated)
- Type annotations (basic types, unions, custom types)
- Writing style guidelines (present tense, active voice, clear language)
- Build integration (npm scripts, jsdoc.conf.json)
- Validation and common mistakes

### Documentation Patterns
- **Functions**: Simple, async, complex with nested parameters
- **Classes**: Declaration, constructor, methods, inheritance
- **Modules**: File overview, exports, constants
- **Types**: Custom types (@typedef), callbacks, union/literal types
- **Web Components**: Lit components, properties, events, CSS properties
- **Quality Examples**: Good vs bad documentation patterns

## When to Activate

Use this skill when:
- Documenting JavaScript code (functions, classes, modules)
- Building web components (Lit or vanilla custom elements)
- Setting up JSDoc and ESLint integration
- Reviewing code documentation quality
- Updating documentation after refactoring

## Workflow

1. **Identify what to document** - Check if element is mandatory (public APIs) or optional
2. **Apply appropriate pattern** - Use pattern from jsdoc-patterns.md for code element type
3. **Include required tags** - @param, @returns, @throws, @example for public functions
4. **Follow writing style** - Present tense, active voice, specific descriptions
5. **Validate** - Run ESLint to check documentation completeness

## Quick Reference

### Required for Public Functions
- Brief description
- @param (all parameters with types)
- @returns (for non-void returns)
- @throws (all possible errors)
- @example (for complex functions)

### Required for Classes
- @class tag with description
- Constructor documentation
- Public method documentation

### Required for Modules
- @fileoverview
- @module tag
- Export documentation

## Best Practices

1. Document as you code - Don't defer documentation
2. Be specific - Avoid vague descriptions
3. Document all errors - Use @throws for all exceptions
4. Provide examples - Show realistic usage
5. Keep synchronized - Update docs when code changes
6. Validate with ESLint - Run linting before commit

## Common Mistakes

- Missing @param, @returns, or @throws
- Vague descriptions ("processes data")
- Parameter names not matching function signature
- No examples for complex functions
- Outdated documentation after refactoring

## Integration

Works with:
- **cui-javascript** skill - Core JavaScript development
- **cui-javascript-unit-testing** skill - Test documentation
- ESLint for automated validation
- JSDoc CLI for documentation generation

## Workflows

### Workflow: Analyze JSDoc Violations

Analyzes JavaScript files for JSDoc compliance violations and returns structured results for command orchestration.

**When to use**: To identify missing or incomplete JSDoc documentation across files or directories.

**Steps**:

1. **Run violation analysis script**

   Script: `pm-dev-frontend:cui-jsdoc` → `jsdoc.py`

   ```bash
   # Analyze entire directory
   python3 .plan/execute-script.py pm-dev-frontend:cui-jsdoc:jsdoc analyze --directory src/

   # Analyze single file
   python3 .plan/execute-script.py pm-dev-frontend:cui-jsdoc:jsdoc analyze --file src/utils/formatter.js

   # Analyze only for missing JSDoc (skip syntax checks)
   python3 .plan/execute-script.py pm-dev-frontend:cui-jsdoc:jsdoc analyze --directory src/ --scope missing

   # Analyze only JSDoc syntax issues
   python3 .plan/execute-script.py pm-dev-frontend:cui-jsdoc:jsdoc analyze --directory src/ --scope syntax
   ```

2. **Process violation results**
   - Review violations categorized by severity:
     - **CRITICAL**: Exported/public API without JSDoc
     - **WARNING**: Internal function without JSDoc, missing @param/@returns
     - **SUGGESTION**: Missing optional tags (@example, @fileoverview)
   - Note `fix_suggestion` for each violation

3. **Prioritize fixes**
   - Fix CRITICAL violations first (exported functions/classes)
   - Address WARNING violations next
   - SUGGESTION items are optional improvements

**JSON Output Contract**:
```json
{
  "status": "violations_found",
  "data": {
    "violations": [
      {
        "file": "src/utils/validator.js",
        "line": 45,
        "type": "missing_jsdoc",
        "severity": "CRITICAL",
        "target": "function validateEmail",
        "message": "Exported function missing JSDoc documentation",
        "fix_suggestion": "Add JSDoc block with @param and @returns tags"
      }
    ],
    "files_analyzed": ["src/utils/validator.js", "..."]
  },
  "metrics": {
    "total_files": 15,
    "files_with_violations": 6,
    "critical": 5,
    "warnings": 12,
    "suggestions": 3,
    "total_violations": 20
  }
}
```

**Violation types detected**:
- `missing_jsdoc` - Function/class entirely missing JSDoc
- `missing_class_doc` - Class without documentation
- `missing_constructor_doc` - Constructor with parameters undocumented
- `missing_param` - @param tag missing for parameter
- `missing_param_type` - Type annotation missing in @param
- `missing_returns` - @returns tag missing for return value
- `missing_fileoverview` - No @fileoverview at file level

**Scope options**:
- `all` - Check for missing JSDoc and syntax issues (default)
- `missing` - Only check for missing JSDoc documentation
- `syntax` - Only check JSDoc syntax and completeness
