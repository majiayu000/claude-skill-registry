---
name: moai-workflow-docs
description: Enhanced documentation unified validation (2 UV scripts migrated to builder-skill-uvscript, 3 workflow scripts retained)
version: 2.0.0
modularized: true
scripts_enabled: true
scripts_migration:
  date: 2025-11-30
  migrated_count: 2
  migrated_location: builder-skill-uvscript
  reason: UV script consolidation with unified builder-skill_ prefix
  remaining_scripts: 3
last_updated: 2025-11-30
compliance_score: 61
auto_trigger_keywords:
  - docs
  - workflow
scripts:
  - name: extract_mermaid_details.py
    purpose: Mermaid diagram detail extraction and rendering test guide generation
    type: python
    command: uv run .claude/skills/moai-workflow-docs/scripts/extract_mermaid_details.py
    zero_context: false
    version: 1.0.0
    last_updated: 2025-11-30
  - name: generate_final_comprehensive_report.py
    purpose: "Phase 4: Generate final comprehensive validation report"
    type: python
    command: uv run .claude/skills/moai-workflow-docs/scripts/generate_final_comprehensive_report.py
    zero_context: false
    version: 1.0.0
    last_updated: 2025-11-30
# MIGRATED to builder-skill-uvscript:
  # - lint_korean_docs.py → builder-skill_lint_docs.py
  # - validate_mermaid_diagrams.py → builder-skill_validate_diagrams.py
  - name: validate_korean_typography.py
    purpose: "Korean-specific validation script (Phase 3)"
    type: python
    command: uv run .claude/skills/moai-workflow-docs/scripts/validate_korean_typography.py
    zero_context: false
    version: 1.0.0
    last_updated: 2025-11-30
color: red
---

> **⚠️ Partial UV Script Migration Notice**
>
> 2 of 5 UV CLI scripts have been consolidated into the **`builder-skill-uvscript`** skill on 2025-11-30.
>
> **Migrated scripts**:
> - `builder-skill_lint_docs.py` (previously lint_korean_docs.py)
> - `builder-skill_validate_diagrams.py` (previously validate_mermaid_diagrams.py)
> - Find migrated scripts in: `.claude/skills/builder-skill-uvscript/scripts/`
>
> **Remaining scripts** (3 workflow-specific scripts retained in this skill):
> - `extract_mermaid_details.py`
> - `generate_final_comprehensive_report.py`
> - `validate_korean_typography.py`
>
> **Usage**:
> - Migrated: `uv run .claude/skills/builder-skill-uvscript/scripts/builder-skill_lint_docs.py`
> - Retained: `uv run .claude/skills/moai-workflow-docs/scripts/extract_mermaid_details.py`

## Quick Reference (30 seconds)

**Purpose**: Comprehensive documentation validation framework with 5 specialized phases.

**Core Phases**:
1. **Markdown Linting** - Syntax, structure, links validation
2. **Mermaid Diagrams** - Diagram syntax and type checking
3. **Mermaid Details** - Code extraction and rendering guide
4. **Korean Typography** - UTF-8, spacing, encoding validation
5. **Report Generation** - Aggregated quality report

**Key Benefits**:
- Catch errors before publication
- Multi-language support (Korean, English, Japanese, Chinese)
- Diagram syntax validation
- Typography consistency
- Actionable recommendations

**Available Scripts**: 5 validation and reporting scripts

**Usage Pattern**:
1. Load skill: `Skill("moai-workflow-docs")`
2. Check SKILL.md for "When to use"
3. Execute script with `--help` flag
4. Run script with options
5. **Only read source if --help insufficient**

**Important**: Don't read script source code unless necessary. All scripts are self-documenting via `--help` flag.

---


## Implementation Guide (5 minutes)

### Features

- Unified documentation generation for technical projects
- README, API docs, architecture guides, and deployment docs
- CommonMark compliance with proper formatting standards
- Automated cross-referencing and navigation
- Multi-language documentation support

### When to Use

- Generating project documentation from code and specifications
- Creating API reference documentation automatically
- Building architecture decision records (ADRs)
- Producing deployment guides and runbooks
- Synchronizing documentation with code changes

### Core Patterns

**Pattern 1: Documentation Structure**
```
docs/
├── README.md (project overview)
├── API.md (API reference)
├── ARCHITECTURE.md (system design)
├── DEPLOYMENT.md (deployment guide)
└── CONTRIBUTING.md (contribution guide)
```

**Pattern 2: Auto-generated API Docs**
```python
# Extract from code comments and type hints
def generate_api_docs(source_files):
    1. Parse docstrings and annotations
    2. Generate markdown tables for parameters/returns
    3. Include code examples from tests
    4. Cross-reference related endpoints
    5. Validate all links and references
```

**Pattern 3: Documentation Sync**
1. Detect code changes via git diff
2. Identify affected documentation sections
3. Update docs automatically or prompt for review
4. Validate documentation completeness
5. Generate changelog entries

## Available Scripts

### `scripts/lint_korean_docs.py`
**When to use:** Validate Korean markdown documentation before committing
**Quick start:** `uv run .claude/skills/moai-workflow-docs/scripts/lint_korean_docs.py --help`

**Features**:
- Validate Korean markdown syntax (UTF-8 encoding)
- Check heading structure (H1-H6 hierarchy)
- Verify code block formatting
- Detect broken internal links
- Check list indentation
- Dual output (human + --json)

**Exit codes**: 0 (pass), 1 (warnings), 2 (errors), 3 (fatal)

### `scripts/validate_mermaid_diagrams.py`
**When to use:** Check Mermaid diagram syntax before committing documentation
**Quick start:** `uv run .claude/skills/moai-workflow-docs/scripts/validate_mermaid_diagrams.py --help`

**Features**:
- Validate Mermaid diagram types (flowchart, sequence, class, state, ER, gantt, pie)
- Check syntax errors (missing nodes, edges, participants)
- Verify required elements per diagram type
- Detect unclosed diagram blocks
- Dual output (human + --json)

**Exit codes**: 0 (all valid), 1 (warnings), 2 (invalid diagrams), 3 (fatal)

### `scripts/validate_korean_typography.py`
**When to use:** Validate Korean typography rules and encoding
**Quick start:** `uv run .claude/skills/moai-workflow-docs/scripts/validate_korean_typography.py --help`

### `scripts/extract_mermaid_details.py`
**When to use:** Extract Mermaid diagrams for detailed review
**Quick start:** `uv run .claude/skills/moai-workflow-docs/scripts/extract_mermaid_details.py --help`

### `scripts/generate_final_comprehensive_report.py`
**When to use:** Generate aggregated validation report
**Quick start:** `uv run .claude/skills/moai-workflow-docs/scripts/generate_final_comprehensive_report.py --help`

---

## 📚 Core Patterns (5-10 minutes)

### Pattern 1: Documentation Validation Pipeline

**Key Concept**: Run validation scripts in sequence to catch multiple error types

**Pipeline Flow**:
1. Run markdown linting on documentation files
2. Validate all Mermaid diagrams for syntax
3. Extract Mermaid diagrams for review
4. Check Korean typography (if applicable)
5. Generate comprehensive report

**Basic Execution**:
```bash
# Run complete validation
uv run .claude/skills/moai-workflow-docs/scripts/lint_korean_docs.py --help
uv run .claude/skills/moai-workflow-docs/scripts/lint_korean_docs.py --input docs/
uv run .claude/skills/moai-workflow-docs/scripts/lint_korean_docs.py --input docs/ --json
```

### Pattern 2: Markdown Structure Validation

**Key Concept**: Ensure consistent markdown structure and formatting

**Common Validations**:
- **Headers**: H1 unique, proper nesting (H1→H2→H3)
- **Code blocks**: Language declared, matching delimiters
- **Links**: Relative paths valid, files exist, HTTPS protocol
- **Lists**: Consistent markers (-, *, +), proper indentation
- **Tables**: Column count consistent, alignment markers

**Example Issues**:
```
❌ Missing language in code block: ```
✅ Correct syntax: ```python

❌ Invalid link: [text](../docs/file)
✅ Correct syntax: [text](../docs/file.md)

❌ Inconsistent list markers: - item1, * item2
✅ Consistent: - item1, - item2
```

### Pattern 3: Mermaid Diagram Validation

**Key Concept**: Validate diagram syntax and type compatibility

**Supported Types**:
- `graph TD/BT/LR/RL` - Flowcharts (top-down, bottom-up, left-right, right-left)
- `stateDiagram-v2` - State machines
- `sequenceDiagram` - Sequence diagrams
- `classDiagram` - Class structures
- `erDiagram` - Entity relationship diagrams
- `gantt` - Gantt charts (timelines)

**Validation Checks**:
- Diagram type recognized
- Configuration block valid
- Node/edge relationships valid
- Syntax errors detected
- Complexity metrics

### Pattern 4: Korean Typography Rules

**Key Concept**: Maintain Korean language best practices

**Validation Rules**:
- No full-width ASCII characters (ａ-ｚ should be a-z)
- Proper spacing around parentheses: `（한글）` vs `(한글)`
- UTF-8 encoding (no broken characters)
- Consistent punctuation (，vs, 、vs..)
- Proper use of Hangul vs Hanja (한글 vs 한漢字)

### Pattern 5: Quality Report Generation

**Key Concept**: Aggregate validation results with actionable recommendations

**Report Contents**:
- Summary statistics (files, issues, severity)
- Issue categorization (errors vs warnings)
- Priority ranking (critical, high, medium, low)
- Specific file locations and line numbers
- Recommended fixes

---

## Advanced Documentation

This Skill uses Progressive Disclosure. For detailed implementation:

- **[modules/validation-scripts.md](modules/validation-scripts.md)** - Complete script specifications
- **[modules/execution-guide.md](modules/execution-guide.md)** - How to run validations
- **[modules/troubleshooting.md](modules/troubleshooting.md)** - Common issues and fixes
- **[modules/reference.md](modules/reference.md)** - API reference and configuration
- **[modules/scripts-reference.md](modules/scripts-reference.md)** - Script API reference
- **[modules/integration-patterns.md](modules/integration-patterns.md)** - Integration patterns and examples

---

## 🔧 Common Use Cases

### Use Case 1: CI/CD Integration

Run validation on every commit:

```yaml
# .github/workflows/docs-validation.yml
on: [push, pull_request]
jobs:
  validate-docs:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Validate documentation
        run: |
          uv run .claude/skills/moai-workflow-docs/scripts/lint_korean_docs.py
          uv run .claude/skills/moai-workflow-docs/scripts/validate_mermaid_diagrams.py
```

### Use Case 2: Pre-Commit Hook

Validate docs before committing:

```bash
#!/bin/bash
# .git/hooks/pre-commit
uv run .claude/skills/moai-workflow-docs/scripts/lint_korean_docs.py
if [ $? -ne 0 ]; then
  echo "Documentation validation failed"
  exit 1
fi
```

### Use Case 3: Documentation Review

Generate report for review team:

```bash
uv run .claude/skills/moai-workflow-docs/scripts/generate_quality_report.py \
  --path docs/src \
  --output .moai/reports/review_report.txt \
  --format detailed
```

---

## 🔗 Integration with Other Skills

**Complementary Skills**:
- Skill("moai-docs-generation") - Generate documentation automatically
- Skill("moai-docs-toolkit") - Document manipulation and conversion
- Skill("moai-cc-claude-md") - Markdown formatting standards

**Typical Workflow**:
1. Use moai-docs-generation to create documentation
2. Use this Skill (moai-workflow-docs) to validate output
3. Use moai-docs-toolkit for additional processing

---

## 📈 Version History

**1.0.1** (2025-11-23)
- 🔄 Refactored with Progressive Disclosure pattern
- 📚 Scripts moved to modules/ for clarity
- ✨ Core patterns highlighted in SKILL.md
- ✨ Added CI/CD and hook integration examples

**1.0.0** (2025-11-12)
- ✨ Markdown linting with 8 validation categories
- ✨ Mermaid diagram validation
- ✨ Korean typography validation
- ✨ Comprehensive quality reporting

---

## Works Well With

**Agents**:
- **workflow-docs** - Documentation generation workflow
- **core-quality** - Quality assurance and validation
- **workflow-spec** - Specification documentation

**Skills**:
- **moai-docs-generation** - Generate documentation automatically
- **moai-docs-toolkit** - Document manipulation and conversion
- **moai-cc-claude-md** - Markdown formatting standards
- **moai-library-mermaid** - Advanced diagram validation
- **moai-library-nextra** - Nextra-based documentation architecture

**Commands**:
- `/moai:3-sync` - Documentation synchronization
- `/moai:9-feedback` - Documentation improvement feedback

---

**Maintained by**: alfred
**Domain**: Documentation & Quality Assurance
**Generated with**: MoAI-ADK Skill Factory