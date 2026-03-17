---
name: deprecated-api-updater
description: "Identify and replace deprecated API usage in source code with modern alternatives. Use when: (1) Modernizing legacy codebases, (2) Upgrading framework versions (React, Django, Spring, etc.), (3) Fixing deprecation warnings in build output, (4) Preparing for major version upgrades, (5) Ensuring code uses current best practices. Supports Python, JavaScript/TypeScript, Java, and other major languages with both AST-based detection and pattern matching for accurate identification and automated replacement with validation."
---

# Deprecated API Updater

Identify and replace deprecated API usage with modern alternatives automatically.

## Quick Start

### Detect Deprecated APIs

Scan code to identify deprecated API usage:

```bash
# Scan a single file
python scripts/detect_deprecated_apis.py src/app.py

# Scan entire directory
python scripts/detect_deprecated_apis.py src/

# Specify language explicitly
python scripts/detect_deprecated_apis.py legacy/ --language python

# Output as JSON
python scripts/detect_deprecated_apis.py src/ --format json
```

### Replace Deprecated APIs

Automatically replace deprecated APIs:

```bash
# Dry run (preview changes)
python scripts/replace_deprecated_apis.py src/ --dry-run

# Apply replacements (creates .bak backups)
python scripts/replace_deprecated_apis.py src/

# Replace in specific language
python scripts/replace_deprecated_apis.py src/ --language javascript
```

## Supported Languages

### Python
- Standard library (collections, time, os, platform, imp)
- Django (URL routing, encoding, translation, models)
- Flask (JSON handling, send_file)
- SQLAlchemy, Pandas, NumPy, Requests

See **[python_deprecations.md](references/python_deprecations.md)** for complete reference.

### JavaScript/TypeScript
- Node.js core (Buffer, url, crypto, fs, util)
- React (lifecycle methods, createClass, PropTypes, Context)
- Express.js (body-parser)
- Webpack, Moment.js alternatives

See **[javascript_deprecations.md](references/javascript_deprecations.md)** for complete reference.

### Java
- Java core (Date/Calendar, Thread methods, finalize)
- Spring Framework (WebMvcConfigurerAdapter, RestTemplate)
- Hibernate (Criteria API)
- JUnit 4 → JUnit 5
- Android (AsyncTask, ProgressDialog, startActivityForResult)

See **[java_deprecations.md](references/java_deprecations.md)** for complete reference.

### Other Languages
- Ruby: URI.escape, Dir.exists?, File.exists?
- Go: ioutil package functions

## Detection Methods

### AST-Based Detection (Precise)

For Python and JavaScript, the skill uses Abstract Syntax Tree parsing for accurate detection:

- **Advantages**: Precise, understands code structure, fewer false positives
- **Limitations**: Requires parseable code, language-specific implementation

**Example**: Detects `os.popen()` by analyzing the AST node structure, not just string matching.

### Pattern Matching (Fast)

For all languages, regex-based pattern matching provides fast detection:

- **Advantages**: Works across all languages, fast, handles unparseable code
- **Limitations**: May have false positives, less precise

**Both methods are used together** for comprehensive detection.

## Workflow

### 1. Scan for Deprecations

Run detection to identify deprecated APIs:

```bash
python scripts/detect_deprecated_apis.py src/
```

**Output example**:
```
Found 3 deprecated API usage(s):

📍 src/utils.py:5:0
   Deprecated: collections.Mapping
   Replacement: collections.abc.Mapping
   Context: from collections import Mapping
   Detection: ast

📍 src/legacy.py:12:9
   Deprecated: os.popen()
   Replacement: subprocess.run() or subprocess.Popen()
   Context: result = os.popen('ls')
   Detection: ast
```

### 2. Review Suggestions

Examine the detected deprecations and suggested replacements. Check the reference documentation for detailed migration guides.

### 3. Test Replacements (Dry Run)

Preview changes before applying:

```bash
python scripts/replace_deprecated_apis.py src/ --dry-run
```

**Output shows**:
- What will be replaced
- Line-by-line changes
- Deprecated API → Replacement API mapping

### 4. Apply Replacements

Apply changes with automatic backups:

```bash
python scripts/replace_deprecated_apis.py src/
```

**Creates**:
- `.bak` backup files for all modified files
- Updated source files with modern APIs

### 5. Validate Changes

**Critical**: Always validate after replacement:

```bash
# Run tests
npm test  # JavaScript
pytest    # Python
mvn test  # Java

# Run linters
eslint src/     # JavaScript
flake8 src/     # Python
mvn checkstyle  # Java

# Manual testing
# Test critical functionality
```

### 6. Commit Changes

Once validated:

```bash
# Review changes
git diff

# Commit
git add .
git commit -m "Replace deprecated APIs with modern alternatives"

# Remove backup files
find . -name "*.bak" -delete
```

## Best Practices

### Before Replacement

1. **Create a branch**: `git checkout -b fix/deprecated-apis`
2. **Commit current state**: Ensure working directory is clean
3. **Run tests**: Verify tests pass before changes
4. **Review deprecation docs**: Check reference files for context

### During Replacement

1. **Start with dry run**: Always preview changes first
2. **Replace incrementally**: Process one module/directory at a time
3. **Keep backups**: Don't delete `.bak` files until validated
4. **Check imports**: Some replacements require new imports

### After Replacement

1. **Run full test suite**: Catch any breaking changes
2. **Check build output**: Look for new warnings
3. **Manual testing**: Test critical user flows
4. **Update dependencies**: Install any newly required packages
5. **Code review**: Have team members review changes

## Common Scenarios

### Scenario 1: Upgrading Django 2.x → 3.x

**Deprecations**:
- `django.conf.urls.url` → `django.urls.path`
- `force_text()` → `force_str()`
- `ugettext` → `gettext`

**Process**:
```bash
# Detect Django-specific deprecations
python scripts/detect_deprecated_apis.py myproject/ --language python

# Preview replacements
python scripts/replace_deprecated_apis.py myproject/ --dry-run

# Apply
python scripts/replace_deprecated_apis.py myproject/

# Test
python manage.py test
```

### Scenario 2: Upgrading React 17 → 18

**Deprecations**:
- `ReactDOM.render()` → `ReactDOM.createRoot()`
- Unsafe lifecycle methods → Modern alternatives

**Process**:
```bash
# Detect React deprecations
python scripts/detect_deprecated_apis.py src/ --language javascript

# Manual review needed for complex cases
# Some React upgrades require structural changes

# Apply simple replacements
python scripts/replace_deprecated_apis.py src/ --dry-run
python scripts/replace_deprecated_apis.py src/

# Test
npm test
npm start  # Manual testing
```

### Scenario 3: Modernizing Python Standard Library Usage

**Deprecations**:
- `collections.Mapping` → `collections.abc.Mapping`
- `time.clock()` → `time.perf_counter()`
- `os.popen()` → `subprocess.run()`

**Process**:
```bash
# Scan codebase
python scripts/detect_deprecated_apis.py . --language python --format json > deprecations.json

# Review JSON output
cat deprecations.json

# Apply replacements
python scripts/replace_deprecated_apis.py . --dry-run
python scripts/replace_deprecated_apis.py .

# Run tests
pytest
```

## Limitations and Caveats

### Automatic Replacement Limitations

1. **Context-dependent changes**: Some deprecations require understanding business logic
2. **Complex refactoring**: Major API redesigns may need manual intervention
3. **Imports**: New imports may need to be added manually
4. **Breaking changes**: Some replacements change behavior subtly

### Manual Review Required

**Always manually review** replacements for:
- Security-sensitive code (authentication, encryption)
- Performance-critical sections (may need optimization)
- Complex logic (ensure semantics unchanged)
- Public APIs (breaking changes for consumers)

### Known Edge Cases

1. **Dynamic imports**: May not detect `importlib.import_module('collections').Mapping`
2. **Aliased imports**: May not detect `import collections as c; c.Mapping`
3. **Conditional code**: Replacements in dead code paths
4. **Comments**: May replace deprecated API mentions in comments

## Troubleshooting

### Detection Issues

**Problem**: Deprecations not detected

**Solutions**:
- Check file extension matches language
- Use `--language` flag explicitly
- Verify file is parseable (no syntax errors)
- Check if pattern exists in deprecation database

**Problem**: False positives

**Solutions**:
- Review AST vs pattern detection method
- Check if it's actually deprecated in your version
- Report false positives for pattern refinement

### Replacement Issues

**Problem**: Replacement breaks code

**Solutions**:
- Restore from `.bak` files
- Review reference documentation for proper usage
- Check if imports need updating
- Manually refactor complex cases

**Problem**: Tests fail after replacement

**Solutions**:
- Check test expectations (mocking, assertions)
- Update test fixtures if API signatures changed
- Review behavior changes in reference docs
- Consider phased replacement approach

## Reference Documentation

### Language-Specific Guides

- **[python_deprecations.md](references/python_deprecations.md)**: Python standard library, Django, Flask, SQLAlchemy, Pandas, NumPy
- **[javascript_deprecations.md](references/javascript_deprecations.md)**: Node.js, React, Express, Webpack, Moment.js
- **[java_deprecations.md](references/java_deprecations.md)**: Java core, Spring, Hibernate, JUnit, Android

Each guide includes:
- Deprecated API examples
- Modern replacement examples
- Migration rationale
- Code samples (before/after)

## Advanced Usage

### Custom Detection Patterns

To add custom deprecation patterns, edit the scripts:

**`scripts/detect_deprecated_apis.py`**:
```python
DEPRECATION_PATTERNS = {
    'python': [
        # Add your patterns
        (r'your\.deprecated\.api\(', 'your.deprecated.api()', 'modern.api()'),
    ]
}
```

**`scripts/replace_deprecated_apis.py`**:
```python
REPLACEMENT_RULES = {
    'python': [
        # Add your replacements
        (r'your\.deprecated\.api\(', r'modern.api(', 'deprecated', 'modern'),
    ]
}
```

### Integration with CI/CD

**Detect deprecations in CI**:
```yaml
# .github/workflows/deprecation-check.yml
name: Check Deprecations
on: [push, pull_request]

jobs:
  check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Check for deprecated APIs
        run: |
          python scripts/detect_deprecated_apis.py src/ --format json > deprecations.json
          if [ -s deprecations.json ]; then
            echo "Deprecated APIs found!"
            cat deprecations.json
            exit 1
          fi
```

### Batch Processing

Process multiple projects:
```bash
#!/bin/bash
for project in project1 project2 project3; do
    echo "Processing $project..."
    python scripts/detect_deprecated_apis.py "$project/src" > "$project-report.txt"
    python scripts/replace_deprecated_apis.py "$project/src" --dry-run
done
```
