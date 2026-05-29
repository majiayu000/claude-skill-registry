---
name: source-unifier
description: Merge multiple documentation sources (docs, GitHub, PDF) with conflict detection. Use when combining docs + code for complete skill coverage.
tools: Read, Write, Bash, Glob, Grep
---

# Source Unifier Skill

## Purpose

Single responsibility: Intelligently merge documentation from multiple sources (websites, GitHub repos, PDFs) while detecting and transparently reporting conflicts between documented and implemented behavior. (BP-4)

## Grounding Checkpoint (Archetype 1 Mitigation)

Before executing, VERIFY:

- [ ] All source URLs/paths are accessible
- [ ] Each source type is correctly identified (docs, github, pdf)
- [ ] Output directory is writable
- [ ] Merge mode is specified (rule-based or AI-enhanced)
- [ ] Conflict resolution strategy is defined

**DO NOT merge without inspecting each source first.**

## Uncertainty Escalation (Archetype 2 Mitigation)

ASK USER instead of guessing when:

- Conflict severity unclear (is doc or code authoritative?)
- Multiple valid interpretations of API signature
- Source versions don't match (v2 docs vs v3 code)
- Merge strategy produces ambiguous results

**NEVER silently resolve conflicts. Always report discrepancies.**

## Context Scope (Archetype 3 Mitigation)

| Context Type | Included | Excluded |
|--------------|----------|----------|
| RELEVANT | All specified sources, merge config | Unrelated documentation |
| PERIPHERAL | Version history for context | Other projects |
| DISTRACTOR | Previous merge attempts | Unrelated codebases |

## Conflict Types

| Type | Severity | Description | Example |
|------|----------|-------------|---------|
| Missing in code | HIGH | Documented but not implemented | API endpoint in docs, not in code |
| Missing in docs | MEDIUM | Implemented but not documented | Hidden feature in code |
| Signature mismatch | MEDIUM | Different parameters/types | `func(a, b)` vs `func(a, b, c=None)` |
| Description mismatch | LOW | Different explanations | Wording differences |

## Workflow Steps

### Step 1: Verify Sources (Grounding)

```bash
# Test documentation URL
curl -I https://docs.example.com/

# Test GitHub repo
gh repo view owner/repo --json name,description

# Test PDF file
file manual.pdf && pdfinfo manual.pdf
```

### Step 2: Create Unified Configuration

```json
{
  "name": "myframework",
  "description": "Complete framework knowledge from docs + code",
  "merge_mode": "rule-based",
  "conflict_resolution": {
    "missing_in_code": "warn",
    "missing_in_docs": "include",
    "signature_mismatch": "show_both",
    "description_mismatch": "prefer_docs"
  },
  "sources": [
    {
      "type": "documentation",
      "base_url": "https://docs.example.com/",
      "extract_api": true,
      "max_pages": 200
    },
    {
      "type": "github",
      "repo": "owner/myframework",
      "include_code": true,
      "code_analysis_depth": "surface",
      "max_issues": 100
    },
    {
      "type": "pdf",
      "path": "docs/manual.pdf",
      "extract_tables": true
    }
  ]
}
```

### Step 3: Execute Unified Scraping

**Option A: With skill-seekers**

```bash
skill-seekers unified --config unified-config.json
```

**Option B: Manual merge workflow**

1. Scrape each source independently
2. Extract API signatures from each
3. Compare and detect conflicts
4. Generate merged output with conflict annotations

### Step 4: Review Conflict Report

The unifier generates a conflict report:

```markdown
# Conflict Report: myframework

## Summary
- Total APIs analyzed: 245
- Conflicts detected: 18
- Missing in code: 3 (HIGH)
- Missing in docs: 8 (MEDIUM)
- Signature mismatches: 5 (MEDIUM)
- Description mismatches: 2 (LOW)

## HIGH Severity Conflicts

### `deprecated_function()`
- **Status**: Documented but not found in code
- **Documentation**: "Use this function to..."
- **Code**: NOT FOUND
- **Recommendation**: Remove from docs or implement

## MEDIUM Severity Conflicts

### `process_data(input: str)`
- **Status**: Signature mismatch
- **Documentation**: `process_data(input: str)`
- **Code**: `process_data(input: str, validate: bool = True)`
- **Recommendation**: Update documentation to include `validate` parameter
```

### Step 5: Validate Merged Output

```bash
# Check merged skill structure
ls -la output/myframework/

# Verify conflict annotations
grep -r "⚠️\|Conflict\|WARNING" output/myframework/references/

# Count conflict markers
grep -c "Conflict" output/myframework/references/*.md
```

## Recovery Protocol (Archetype 4 Mitigation)

On error:

1. **PAUSE** - Preserve partial merge state
2. **DIAGNOSE** - Check error type:
   - `Source unavailable` → Skip source, note in report
   - `Parse error` → Check source format, retry with different parser
   - `Memory error` → Process sources sequentially
   - `Conflict overflow` → Increase conflict threshold or filter by severity
3. **ADAPT** - Adjust merge strategy
4. **RETRY** - Resume merge (max 3 attempts)
5. **ESCALATE** - Present partial results, ask user for conflict resolution

## Checkpoint Support

State saved to: `.aiwg/working/checkpoints/source-unifier/`

```
checkpoints/source-unifier/
├── source_1_docs.json      # Processed docs
├── source_2_github.json    # Processed GitHub
├── source_3_pdf.json       # Processed PDF
├── conflicts.json          # Detected conflicts
└── merge_progress.json     # Current merge state
```

Resume: `skill-seekers unified --config config.json --resume`

## Output Structure

```
output/myframework/
├── SKILL.md                    # Main skill with conflict summary
├── references/
│   ├── index.md                # Unified index
│   ├── api_reference.md        # Merged API docs (with conflict markers)
│   ├── guides.md               # Merged guides
│   └── conflicts.md            # Detailed conflict report
├── sources/
│   ├── documentation.md        # Original docs content
│   ├── github.md               # GitHub-extracted content
│   └── pdf.md                  # PDF-extracted content
└── metadata/
    ├── sources.json            # Source metadata
    └── conflict_summary.json   # Machine-readable conflicts
```

## Conflict Markers in Output

Merged content includes inline conflict markers:

```markdown
#### `process_data(input: str, validate: bool = True)`

⚠️ **Conflict**: Documentation signature differs from implementation

**Documentation says:**
```python
def process_data(input: str) -> dict:
    """Process input data and return results."""
```

**Code implementation:**
```python
def process_data(input: str, validate: bool = True) -> dict:
    """Process input data with optional validation."""
```

**Resolution**: Documentation should be updated to include the `validate` parameter added in v2.3.
```

## Merge Modes

| Mode | Description | Use Case |
|------|-------------|----------|
| `rule-based` | Apply predefined rules for conflict resolution | Fast, deterministic |
| `ai-enhanced` | Use AI to intelligently merge conflicting content | Better quality, slower |
| `manual` | Generate conflicts only, user resolves | Full control |

## Troubleshooting

| Issue | Diagnosis | Solution |
|-------|-----------|----------|
| Too many conflicts | Sources very different | Filter by severity, merge incrementally |
| False positives | Parser differences | Normalize API extraction |
| Missing content | Source incomplete | Add supplementary source |
| Merge too slow | Large sources | Use parallel processing |

## References

- Skill Seekers Unified Scraping: https://github.com/jmagly/Skill_Seekers/blob/main/docs/UNIFIED_SCRAPING.md
- REF-001: Production-Grade Agentic Workflows (BP-4, BP-6 model consortium parallel)
- REF-002: LLM Failure Modes (Archetype 1-4 mitigations)
