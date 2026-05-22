---
name: quality-checker
description: Validate skill quality, completeness, and adherence to standards. Use before packaging to ensure skill meets quality requirements.
tools: Read, Write, Bash, Glob, Grep
---

# Quality Checker Skill

## Purpose

Single responsibility: Validate Claude skill packages for quality, completeness, and standards compliance before upload. (BP-4)

## Grounding Checkpoint (Archetype 1 Mitigation)

Before executing, VERIFY:

- [ ] Skill directory exists
- [ ] SKILL.md is present
- [ ] Quality criteria are defined
- [ ] Validation scope is clear (quick/full/custom)

**DO NOT validate without defining quality criteria.**

## Uncertainty Escalation (Archetype 2 Mitigation)

ASK USER instead of guessing when:

- Quality threshold unclear (strict vs lenient)
- Custom validation rules needed
- Failures found - block or warn?
- Edge cases in validation logic

**NEVER auto-pass quality checks without proper validation.**

## Context Scope (Archetype 3 Mitigation)

| Context Type | Included | Excluded |
|--------------|----------|----------|
| RELEVANT | Skill directory, quality criteria | Other skills |
| PERIPHERAL | Quality examples for comparison | Source documentation |
| DISTRACTOR | Build process | Enhancement history |

## Quality Dimensions

| Dimension | Weight | Checks |
|-----------|--------|--------|
| Structure | 25% | Required files, directory layout |
| Content | 35% | SKILL.md completeness, references |
| Code Examples | 20% | Presence, syntax, relevance |
| Documentation | 20% | Clarity, navigation, completeness |

## Workflow Steps

### Step 1: Structure Validation (Grounding)

```bash
# Required files
SKILL_DIR="output/<skill-name>"

# Check SKILL.md
test -f "$SKILL_DIR/SKILL.md" && echo "✅ SKILL.md present" || echo "❌ SKILL.md missing"

# Check references directory
test -d "$SKILL_DIR/references" && echo "✅ references/ present" || echo "❌ references/ missing"

# Check at least one reference file
ls "$SKILL_DIR/references/"*.md >/dev/null 2>&1 && \
  echo "✅ Reference files present" || echo "❌ No reference files"

# Check for index
test -f "$SKILL_DIR/references/index.md" && \
  echo "✅ Index present" || echo "⚠️ No index.md (recommended)"
```

### Step 2: SKILL.md Content Validation

```bash
SKILL_MD="output/<skill-name>/SKILL.md"

# Required sections
echo "=== Section Check ==="
grep -q "^# " "$SKILL_MD" && echo "✅ Title present" || echo "❌ Missing title"
grep -q "^## Description\|^## Purpose" "$SKILL_MD" && echo "✅ Description present" || echo "❌ Missing description"

# Recommended sections
grep -q "^## Quick Reference\|^## Overview" "$SKILL_MD" && echo "✅ Quick reference" || echo "⚠️ No quick reference"
grep -q "^## Code Examples\|^## Examples" "$SKILL_MD" && echo "✅ Examples section" || echo "⚠️ No examples section"
grep -q "^## Navigation\|^## Contents" "$SKILL_MD" && echo "✅ Navigation" || echo "⚠️ No navigation"

# Content quality
echo ""
echo "=== Content Metrics ==="
echo "Lines: $(wc -l < "$SKILL_MD")"
echo "Code blocks: $(grep -c '```' "$SKILL_MD")"
echo "Sections: $(grep -c '^## ' "$SKILL_MD")"
echo "Links: $(grep -oE '\[.*\]\(.*\)' "$SKILL_MD" | wc -l)"
```

### Step 3: Code Example Validation

```bash
SKILL_MD="output/<skill-name>/SKILL.md"

# Extract code blocks
echo "=== Code Examples ==="
example_count=$(grep -c '```' "$SKILL_MD")
echo "Total code blocks: $((example_count / 2))"

# Check for language tags
tagged=$(grep -c '```[a-z]' "$SKILL_MD")
echo "Language-tagged blocks: $tagged"

# Check code isn't just placeholders
placeholder_count=$(grep -E '```\n(# placeholder|// TODO|pass)\n```' "$SKILL_MD" | wc -l)
echo "Placeholder blocks: $placeholder_count"

# Minimum requirement: 3 real code examples
real_examples=$((example_count / 2 - placeholder_count))
if [ "$real_examples" -ge 3 ]; then
  echo "✅ Sufficient code examples ($real_examples)"
else
  echo "⚠️ Few code examples ($real_examples, recommend 3+)"
fi
```

### Step 4: Reference Quality Validation

```bash
REF_DIR="output/<skill-name>/references"

echo "=== Reference Files ==="
for file in "$REF_DIR"/*.md; do
  if [ -f "$file" ]; then
    lines=$(wc -l < "$file")
    name=$(basename "$file")
    if [ "$lines" -lt 10 ]; then
      echo "⚠️ $name: $lines lines (sparse)"
    else
      echo "✅ $name: $lines lines"
    fi
  fi
done

# Total reference content
total_lines=$(cat "$REF_DIR"/*.md 2>/dev/null | wc -l)
echo ""
echo "Total reference content: $total_lines lines"
```

### Step 5: Generate Quality Report

```markdown
# Quality Report: <skill-name>

## Summary
- Overall Score: XX/100
- Status: PASS/WARN/FAIL

## Structure (25/25)
- [x] SKILL.md present
- [x] references/ directory
- [x] Reference files present
- [ ] Optional: scripts/, assets/

## Content (30/35)
- [x] Title present
- [x] Description clear
- [x] Quick reference
- [ ] FAQ section (missing)

## Code Examples (15/20)
- [x] 5 code examples
- [x] Language tags
- [ ] Example diversity (all Python)

## Documentation (18/20)
- [x] Navigation table
- [x] Links work
- [ ] Version info missing

## Recommendations
1. Add FAQ section based on common questions
2. Include examples in other languages
3. Add version/last updated info
```

## Recovery Protocol (Archetype 4 Mitigation)

On error:

1. **PAUSE** - Complete partial validation
2. **DIAGNOSE** - Check error type:
   - `File not found` → Check path
   - `Parse error` → Check file format
   - `Script error` → Simplify validation
3. **ADAPT** - Adjust validation scope
4. **RETRY** - With corrected parameters (max 3 attempts)
5. **ESCALATE** - Report partial results

## Checkpoint Support

State saved to: `.aiwg/working/checkpoints/quality-checker/`

```
checkpoints/quality-checker/
├── structure_results.json
├── content_results.json
├── code_results.json
├── docs_results.json
└── final_report.md
```

## Quality Thresholds

| Level | Score | Action |
|-------|-------|--------|
| PASS | 80-100 | Ready for packaging |
| WARN | 60-79 | Review recommendations |
| FAIL | <60 | Address issues before packaging |

## Configuration Options

```json
{
  "skill_dir": "output/myskill/",
  "validation_level": "full",
  "thresholds": {
    "pass": 80,
    "warn": 60
  },
  "requirements": {
    "min_skill_md_lines": 100,
    "min_code_examples": 3,
    "min_reference_files": 2,
    "require_navigation": true,
    "require_faq": false
  },
  "output": {
    "report_format": "markdown",
    "save_report": true
  }
}
```

## Validation Levels

| Level | Checks | Time |
|-------|--------|------|
| quick | Structure only | <5s |
| standard | Structure + content | <30s |
| full | All dimensions | <2m |
| strict | Full + extra rules | <5m |

## Custom Validation Rules

Add custom rules via configuration:

```json
{
  "custom_rules": [
    {
      "name": "api_coverage",
      "type": "grep",
      "pattern": "^### .*\\(\\)",
      "file": "references/api.md",
      "min_matches": 10,
      "message": "API reference should document at least 10 functions"
    }
  ]
}
```

## Troubleshooting

| Issue | Diagnosis | Solution |
|-------|-----------|----------|
| False positives | Rules too strict | Adjust thresholds |
| Missed issues | Rules too lenient | Use strict mode |
| Slow validation | Full mode on large skill | Use quick mode first |
| Parse errors | Malformed markdown | Fix source files |

## Integration with Workflow

```
doc-scraper → skill-builder → skill-enhancer → quality-checker → skill-packager
                                                     ↓
                                              [If FAIL: fix issues]
                                                     ↓
                                              [If WARN: review]
                                                     ↓
                                              [If PASS: package]
```

## References

- Claude Skills Quality Guidelines: https://docs.anthropic.com/skills
- AIWG Quality Standards: `agentic/code/addons/writing-quality/`
- REF-001: Production-Grade Agentic Workflows (BP-4, BP-9)
- REF-002: LLM Failure Modes (Archetype 1 grounding, Archetype 2 over-helpfulness)
