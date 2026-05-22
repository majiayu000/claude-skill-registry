---
name: code-style-validator
description: Programmatic code style validation using AST analysis. Complements (not replaces) code-style rules by providing automated checking and instant feedback.
model: haiku
allowed-tools: read, grep, bash, glob
---

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
**Usage Examples**:

**Validate Single File**:

```bash
node .claude/tools/validate-code-style.js src/components/Button.tsx
```

**Validate Directory**:

```bash
node .claude/tools/validate-code-style.js src/components/
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
**Pre-commit Hook**:

```bash
#!/bin/bash
# .git/hooks/pre-commit
changed_files=$(git diff --cached --name-only --diff-filter=ACM | grep -E '\.(ts|tsx|js|jsx|py)$')

for file in $changed_files; do
  if ! node .claude/tools/validate-code-style.js "$file"; then
    echo "Code style validation failed for $file"
    exit 1
  fi
done
```

</code_example>

<code_example>
**CI/CD Integration**:

```yaml
# .github/workflows/code-style.yml
- name: Validate code style
  run: |
    node .claude/tools/validate-code-style.js src/
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
