---
name: code-style-validator
description: Programmatic code style validation using AST analysis. Complements (not replaces) code-style rules by providing automated checking and instant feedback.
version: 1.0.0
model: haiku
invoked_by: both
user_invocable: true
tools: [Read, Grep, Bash, Glob]
best_practices:
  - Use AST analysis for accurate validation
  - Provide auto-fix suggestions
  - Integrate with pre-commit hooks
error_handling: graceful
streaming: supported
---

## Installation

No separate download: the skill runs the in-repo tool `.claude/tools/cli/security-lint.cjs`.

- Ensure **Node.js** (v18+) is installed: [nodejs.org](https://nodejs.org/) or `winget install OpenJS.NodeJS.LTS` (Windows), `brew install node` (macOS).
- From the project root, the script is invoked automatically; no extra install steps.

## Cheat Sheet & Best Practices

**AST-based validation:** Use ESLint (or equivalent) with selectors/patterns; rules listen for specific node types. Prefer existing community rules before writing custom ones; custom rules need `meta` (type, fixable, schema) and `create`.

**Process:** Check naming (camelCase/PascalCase/snake_case), indentation, import order, function/class structure, comment style. Run in pre-commit and CI; provide auto-fix where possible.

**Hacks:** Use `--fix` for auto-fixable rules; combine with security-lint for policy. Define rule metadata clearly for docs and tooling. Use AST selectors for precise pattern matching (node type, attributes, child/sibling).

## Certifications & Training

**ESLint:** [Use in project](https://eslint.org/docs/latest/use/), [custom rules](https://eslint.org/docs/latest/extend/custom-rules), [selectors](https://eslint.org/docs/latest/extend/selectors). No cert; skill data: AST-based validation, pre-commit/CI, auto-fix, naming/indent/imports.

## Hooks & Workflows

**Suggested hooks:** Pre-commit: run security-lint (skill script) or ESLint; block commit on failure. Use with **developer** (secondary), **code-reviewer** (secondary), **qa** (CI).

**Workflows:** Use with **code-reviewer** (secondary), **developer** (secondary). Flow: before commit or in CI → run validator → fix or block. See `code-review-workflow.md`, `validation` hooks.

<identity>
Code Style Validator - Programmatically validates code style using AST (Abstract Syntax Tree) analysis. Complements code-style rules by providing automated checking.
</identity>

<capabilities>
- Before committing code
- In pre-commit hooks
- During code review
- In CI/CD pipelines
- To enforce consistent code style
</capabilities>

<instructions>
<execution_process>

### Step 1: Identify Code Style Patterns

Analyze the codebase to identify style patterns:

- Naming conventions (camelCase, PascalCase, snake_case)
- Indentation style (spaces vs tabs, width)
- Import organization
- Function/class structure
- Comment style

### Step 2: AST-Based Validation

Use language-specific AST parsers:

**TypeScript/JavaScript**:
</execution_process>
</instructions>

<examples>
<code_example>
**TypeScript/JavaScript AST Validation**:

```javascript
const ts = require('typescript');
const fs = require('fs');

function validateTypeScriptFile(filePath) {
  const sourceCode = fs.readFileSync(filePath, 'utf8');
  const sourceFile = ts.createSourceFile(filePath, sourceCode, ts.ScriptTarget.Latest, true);

  const issues = [];

  // Validate naming conventions
  ts.forEachChild(sourceFile, node => {
    if (ts.isFunctionDeclaration(node) && node.name) {
      if (!/^[a-z][a-zA-Z0-9]*$/.test(node.name.text)) {
        issues.push({
          line: sourceFile.getLineAndCharacterOfPosition(node.name.getStart()).line + 1,
          message: `Function name "${node.name.text}" should be camelCase`,
        });
      }
    }
  });

  return issues;
}
```

</code_example>

<code_example>
**Python AST Validation**:

```python
import ast
import re

def validate_python_file(file_path):
    with open(file_path, 'r') as f:
        source_code = f.read()

    tree = ast.parse(source_code)
    issues = []

    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            if not re.match(r'^[a-z][a-z0-9_]*$', node.name):
                issues.append({
                    'line': node.lineno,
                    'message': f'Function name "{node.name}" should be snake_case'
                })

    return issues
```

</code_example>

<code_example>
**Style Checks**:

**Naming Conventions**:

- Variables: camelCase (JS/TS) or snake_case (Python)
- Functions: camelCase (JS/TS) or snake_case (Python)
- Classes: PascalCase
- Constants: UPPER_CASE
- Private: prefix with underscore

**Formatting**:

- Indentation: 2 spaces (JS/TS) or 4 spaces (Python)
- Line length: 88-100 characters
- Trailing commas: Yes (JS/TS)
- Semicolons: Consistent usage

**Structure**:

- Import order: external, internal, relative
- Function length: < 50 lines
- File organization: exports, helpers, types
  </code_example>

<code_example>
**Usage Examples** (Template - implement validator first):

**Validate Single File**:

```bash
# After implementing your validator:
node validate-code-style.js src/components/Button.tsx
```

**Validate Directory**:

```bash
# After implementing your validator:
node validate-code-style.js src/components/
```

**Output Format**:

```json
{
  "file": "src/components/Button.tsx",
  "valid": false,
  "issues": [
    {
      "line": 15,
      "column": 10,
      "rule": "naming-convention",
      "message": "Variable 'UserData' should be camelCase: 'userData'",
      "severity": "error"
    },
    {
      "line": 23,
      "column": 5,
      "rule": "indentation",
      "message": "Expected 2 spaces, found 4",
      "severity": "warning"
    }
  ],
  "summary": {
    "total": 2,
    "errors": 1,
    "warnings": 1
  }
}
```

</code_example>

<code_example>
**Pre-commit Hook** (Template - implement validator first):

```bash
#!/bin/bash
# .git/hooks/pre-commit
changed_files=$(git diff --cached --name-only --diff-filter=ACM | grep -E '\.(ts|tsx|js|jsx|py)$')

for file in $changed_files; do
  # Replace with your actual validator path
  if ! node validate-code-style.js "$file"; then
    echo "Code style validation failed for $file"
    exit 1
  fi
done
```

</code_example>

<code_example>
**CI/CD Integration** (Template - implement validator first):

```yaml
# .github/workflows/code-style.yml
- name: Validate code style
  run: |
    # Replace with your actual validator path
    node validate-code-style.js src/
    if [ $? -ne 0 ]; then
      echo "Code style validation failed"
      exit 1
    fi
```

</code_example>
</examples>

<instructions>
<best_practices>
1. **Complement, Don't Replace**: This tool complements code-style rules, doesn't replace them
2. **Configurable Rules**: Allow teams to customize validation rules
3. **Auto-fix When Possible**: Provide auto-fix suggestions for common issues
4. **Fast Feedback**: Provide instant feedback during development
5. **Clear Messages**: Show clear error messages with line numbers and suggestions
</best_practices>
</instructions>

## Memory Protocol (MANDATORY)

**Before starting:**
Read `.claude/context/memory/learnings.md`

**After completing:**

- New pattern -> `.claude/context/memory/learnings.md`
- Issue found -> `.claude/context/memory/issues.md`
- Decision made -> `.claude/context/memory/decisions.md`

> ASSUME INTERRUPTION: If it's not in memory, it didn't happen.
