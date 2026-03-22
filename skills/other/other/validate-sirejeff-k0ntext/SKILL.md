---
description: Run complete validation suite on context engineering documentation
---

# Context Engineering: Validation

Run comprehensive validation on the context engineering setup.

## Validation Checks

### 1. Structure Validation
- All required directories exist in `.claude/`
- Required files are present
- Settings file is valid JSON

### 2. Schema Validation
- JSON files validate against their schemas
- Frontmatter in markdown files is valid

### 3. Link Validation
- All internal markdown links resolve
- No broken references to files or anchors

### 4. Placeholder Detection
- Find remaining `{{PLACEHOLDER}}` values
- Report files that need manual completion

### 5. Line Number Accuracy
- Sample referenced line numbers in documentation
- Verify they match actual code
- Target: ≥60% accuracy

## Output

```
Validation Results
==================
✓ Structure: PASS (12/12 directories)
✓ Schemas: PASS (5/5 files valid)
✓ Links: PASS (45/45 links resolve)
⚠ Placeholders: WARN (3 remaining in 2 files)
✓ Line Accuracy: PASS (78% accurate)

Overall: PASS with warnings
```

## Usage

Run validation:
- Full suite: `/context-eng:validate`
- Specific check: `/context-eng:validate --links`
- With fix: `/context-eng:validate --fix`

## Thresholds

| Check | Pass | Warn | Fail |
|-------|------|------|------|
| Structure | 100% | - | <100% |
| Schemas | 100% | - | <100% |
| Links | 100% | <100% | <90% |
| Placeholders | 0 | 1-5 | >5 |
| Line Accuracy | ≥60% | 50-60% | <50% |
