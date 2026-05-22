---
name: code-fix-assistant
description: Automated code quality assistant that formats code, fixes syntax/type errors, detects bugs, and validates fixes across Python, JavaScript, TypeScript, Java, Go, and Rust
---

# Code Fix Assistant

Automated code quality assistant providing a complete fix pipeline: formatting → syntax/type fixing → bug detection → validation, supporting multiple programming languages.

## Capabilities

- **Code Formatting**: Automatically apply standard code style and formatting rules
  - Python: Black, autopep8, isort
  - JavaScript/TypeScript: Prettier, ESLint
  - Java: Google Java Format
  - Go: gofmt, goimports
  - Rust: rustfmt

- **Syntax/Type Error Fixing**: Detect and fix common syntax and type issues
  - Missing semicolons, unmatched brackets
  - Import/dependency issues
  - Type errors (TypeScript, Java, Rust)
  - Unused variables and imports

- **Bug Detection & Fixing**: Static analysis and intelligent fixes
  - Null pointer/null reference issues
  - Array out of bounds
  - Resource leaks (files, connections)
  - Logic errors (incorrect conditions)
  - Dead code detection

- **Fix Validation**: Automatically validate fix effectiveness
  - Run linter checks
  - Syntax validation
  - Generate fix reports
  - Compare before/after differences

## Input Requirements

**Required Inputs**:
- `file_path`: Path to code file to fix
- `language`: Programming language (python, javascript, typescript, java, go, rust)
- `fix_types`: List of fix types (optional, defaults to all)
  - `format`: Code formatting
  - `syntax`: Syntax/type fixing
  - `bugs`: Bug detection and fixing
  - `validate`: Fix validation

**Optional Inputs**:
- `config`: Custom configuration (e.g., ESLint rules, Black options)
- `severity_threshold`: Severity threshold (error, warning, info)
- `auto_apply`: Whether to auto-apply fixes (default false, report only)

**Input Format**:
```json
{
  "file_path": "src/main.py",
  "language": "python",
  "fix_types": ["format", "syntax", "bugs", "validate"],
  "auto_apply": true,
  "severity_threshold": "warning"
}
```

## Output Formats

**Fix Report** (JSON format):
```json
{
  "file": "src/main.py",
  "language": "python",
  "fixes_applied": {
    "format": { "changes": 15, "status": "success" },
    "syntax": { "issues_found": 3, "issues_fixed": 3 },
    "bugs": { "issues_found": 2, "issues_fixed": 1, "unfixable": 1 },
    "validation": { "linter_passed": true, "syntax_valid": true }
  },
  "issues": [
    {
      "type": "syntax",
      "severity": "error",
      "line": 42,
      "message": "Undefined variable 'results'",
      "fix": "Added variable initialization",
      "status": "fixed"
    },
    {
      "type": "bug",
      "severity": "warning",
      "line": 58,
      "message": "Potential null pointer dereference",
      "fix": "Added null check",
      "status": "fixed"
    }
  ],
  "diff": "--- original\n+++ fixed\n@@ -42,3 +42,4 @@\n+results = []\n",
  "summary": "Applied 15 formatting changes, fixed 3 syntax errors, fixed 1/2 bugs, validation passed"
}
```

**Fixed Code File** (if `auto_apply: true`)

## How to Use

**Basic Usage**:
```
@code-fix-assistant

Fix formatting and syntax issues in this Python file: src/main.py
```

**Complete Fix Pipeline**:
```
@code-fix-assistant

Run complete fix pipeline on src/app.ts:
1. Format code
2. Fix TypeScript type errors
3. Detect and fix potential bugs
4. Validate fix results
```

**Batch Fixing**:
```
@code-fix-assistant

Fix code quality issues in all Python files under src/ directory
```

**Check Only (No Auto-Fix)**:
```
@code-fix-assistant

Check code issues in main.go and generate report, but don't auto-fix
```

## Scripts

- `code_fixer.py`: Main fix engine coordinating all fix steps
- `formatters.py`: Code formatting module (multi-language support)
- `syntax_checker.py`: Syntax and type error detection & fixing
- `bug_detector.py`: Static analysis and bug detection
- `validator.py`: Fix validation and report generation
- `language_config.py`: Language-specific config and tool mapping

## Best Practices

1. **Incremental Fixing**: Recommended order: format → syntax → bugs
2. **Version Control**: Commit code before fixing for easy rollback
3. **Test Validation**: Run test suites after fixing to ensure no functionality breakage
4. **Review Fixes**: For critical code, generate report and manually review before applying
5. **Config Files**: Use project-level configs (.prettierrc, .black.toml) for consistency
6. **Batch Fixing**: For large projects, fix incrementally to avoid massive changesets

## Limitations

**Tool Dependencies**:
- Requires language-specific linter/formatter tools installed
- Python: `black`, `flake8`, `mypy`
- JavaScript/TypeScript: `prettier`, `eslint`
- Java: `google-java-format`, `checkstyle`
- Go: `gofmt`, `golangci-lint`
- Rust: `rustfmt`, `clippy`

**Fix Capabilities**:
- Can only fix automatable issues (formatting, common syntax errors, simple bugs)
- Complex logic errors require human intervention
- Cannot guarantee 100% fix rate for all issues
- Some bugs require contextual understanding and may be misdiagnosed

**Performance Considerations**:
- Large files (>10,000 lines) may be slow to process
- Batch fixing many files takes time
- Static analysis depth is limited (not full program analysis)

**Security**:
- Will not modify .git/ or config files
- Will not execute code (static analysis only)
- Recommended to test in isolated environment
- Critical production code should be manually reviewed

## Language-Specific Notes

### Python
- Default uses Black format (88-character line width)
- Supports type hint checking (mypy)
- Auto-sorts imports (isort)

### JavaScript/TypeScript
- Follows Prettier default rules
- ESLint rules customizable
- TypeScript type errors auto-fixed (simple types only)

### Java
- Google Java Format style
- Supports null checking and resource leak detection
- Unused imports auto-cleaned

### Go
- Strictly follows gofmt standard
- goimports auto-manages imports
- Supports go vet static checks

### Rust
- rustfmt standard formatting
- Clippy lint suggestion fixes
- Ownership and lifetime errors reported (not auto-fixable)

## Error Handling

**Tools Not Installed**:
- Prompts to install missing tools
- Provides installation commands
- Skips step and continues with other fixes

**Fix Failures**:
- Logs failure reason
- Preserves original file unchanged
- Provides manual fix suggestions

**File Permission Issues**:
- Checks read/write permissions
- Prompts permission errors
- Suggests solutions

## Examples

### Example 1: Python Formatting and Syntax Fixing

**Input**:
```python
# bad_code.py
import os,sys
import json

def process_data(data):
  results=[]
  for item in data:
      if item['value']>0:
        results.append(item)
  return results

def main( ):
    data=[{'value':1},{'value':-1}]
    result=process_data(data)
    print(result)
```

**After Fix**:
```python
# bad_code.py
import json
import os
import sys


def process_data(data):
    results = []
    for item in data:
        if item["value"] > 0:
            results.append(item)
    return results


def main():
    data = [{"value": 1}, {"value": -1}]
    result = process_data(data)
    print(result)
```

### Example 2: TypeScript Type Error Fixing

**Input**:
```typescript
// app.ts
function greet(name) {
  return "Hello, " + name;
}

let user = { name: "Alice", age: 30 };
console.log(greet(user.name));
console.log(user.address); // Error: Property 'address' does not exist
```

**After Fix**:
```typescript
// app.ts
function greet(name: string): string {
  return "Hello, " + name;
}

interface User {
  name: string;
  age: number;
}

let user: User = { name: "Alice", age: 30 };
console.log(greet(user.name));
// Removed: console.log(user.address); - Property does not exist
```

### Example 3: Go Code Formatting and Lint Fixing

**Input**:
```go
// main.go
package main
import "fmt"
func main(){
var x int=10
if x>5{
fmt.Println("x is greater than 5")
}
}
```

**After Fix**:
```go
// main.go
package main

import "fmt"

func main() {
	var x int = 10
	if x > 5 {
		fmt.Println("x is greater than 5")
	}
}
```
