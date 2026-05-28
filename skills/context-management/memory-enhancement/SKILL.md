---
name: memory-enhancement
version: 1.0.0
description: >
  Manage memory citations, verify code references, and track confidence scores. Use when adding citations to memories, checking memory health, or verifying code references are still valid.
license: MIT
model: claude-sonnet-4-5
metadata:
  domains: [memory, citations, verification]
  type: utility
  adr: ADR-007, ADR-037
---

# Memory Enhancement

Manage citations, verify code references, and track confidence scores for Serena memories. Ensures memories stay accurate by linking them to specific code locations and detecting when those locations change.

## Triggers

- "add citation to memory" - Link memory to specific code location
- "verify memory citations" - Check if code references are still valid
- "check memory health" - Generate staleness report across all memories
- "update memory confidence" - Recalculate trust score based on verification

## Quick Reference

| Input | Output | Duration |
|-------|--------|----------|
| Memory ID + code reference | Citation added with validation | < 5 seconds |
| Memory directory | Health report with stale memories | < 30 seconds |
| Verification results | Updated confidence scores | < 10 seconds |

## Decision Tree

```text
Need memory enhancement?
│
├─ Add citation to memory → add-citation command
├─ Verify citations → verify or verify-all command
├─ Check memory health → health command
├─ Traverse memory graph → graph command
└─ Update confidence → update-confidence command
```

## Process

### Phase 1: Identify Target Memory

Locate memory file by ID or path:

1. **Check default directory** - Look in `.serena/memories/` for `<memory-id>.md`
2. **Try direct path** - If full path provided, use it directly
3. **Validate existence** - Error if memory file not found (exit code 2)

**Verification:** Memory file exists and is readable

### Phase 2: Add/Verify Citations

Use CLI commands with structured output:

#### Add Citation

```bash
python -m memory_enhancement add-citation <memory-id> --file <path> --line <num> --snippet <text>
```

**Parameters:**

- `memory-id` - Memory identifier or file path
- `--file` - Relative file path from repository root (required)
- `--line` - Line number (1-indexed, optional for file-level citations)
- `--snippet` - Code snippet for fuzzy matching (optional)
- `--dry-run` - Preview changes without writing (optional)

**Exit Codes** (ADR-035):

- 0: Success
- 1: Validation failed (stale citation)
- 2: Invalid arguments or file not found
- 3: File I/O error

#### Verify Citations

```bash
# Single memory
python -m memory_enhancement verify <memory-id> [--json]

# All memories
python -m memory_enhancement verify-all [--dir .serena/memories] [--json]
```

**Output Indicators:**

- ✅ VALID - All citations point to valid locations
- ❌ STALE - Some citations are invalid
- Confidence score (0.0-1.0)
- Detailed mismatch reasons

**Verification:** Citations validated against current codebase state

### Phase 3: Update Confidence

Recalculate based on verification results:

```bash
python -m memory_enhancement update-confidence <memory-id>
```

**Confidence Calculation:**

```text
confidence = valid_citations / total_citations
```

**Interpretation:**

| Score Range | Meaning | Action |
|-------------|---------|--------|
| 0.9 - 1.0 | High confidence | Trust memory, use in decisions |
| 0.7 - 0.9 | Medium confidence | Review stale citations |
| 0.5 - 0.7 | Low confidence | Update memory or mark obsolete |
| 0.0 - 0.5 | Very low confidence | Memory likely outdated |
| No citations | Default (0.5) | Add citations to improve confidence |

**Verification:** Confidence score updated in YAML frontmatter

### Phase 4: Report Results

Display summary with actionable recommendations:

#### List Citations

```bash
python -m memory_enhancement list-citations <memory-id> [--json]
```

Human-readable output:

```text
Citations for memory-001:
Total: 3

✅ src/api.py:42
   Snippet: handleError

❌ src/client.ts:100
   Reason: Line 100 exceeds file length (95 lines)

✅ scripts/test.py
```

JSON output for programmatic usage:

```json
{
  "citations": [
    {
      "path": "src/api.py",
      "line": 42,
      "snippet": "handleError",
      "valid": true,
      "mismatch_reason": null,
      "verified": "2026-01-24T14:30:00"
    }
  ]
}
```

#### Health Report

```bash
python -m memory_enhancement health [--format markdown|json] [--include-graph]
```

Generates comprehensive report with:

- Total memories with citations
- Stale memory count and percentage
- Memories ranked by staleness (worst first)
- Optional: Orphaned memories (disconnected from graph)

**Verification:** Report generated successfully

## Script Reference

| Operation | CLI Command | Key Parameters |
|-----------|-------------|----------------|
| Add citation | `python -m memory_enhancement add-citation` | `<memory-id>`, `--file`, `--line`, `--snippet` |
| Verify memory | `python -m memory_enhancement verify` | `<memory-id>`, `--json` |
| Verify all | `python -m memory_enhancement verify-all` | `--dir`, `--json` |
| Health report | `python -m memory_enhancement health` | `--format` (markdown/json) |
| Update confidence | `python -m memory_enhancement update-confidence` | `<memory-id>` |
| List citations | `python -m memory_enhancement list-citations` | `<memory-id>`, `--json` |
| Graph traversal | `python -m memory_enhancement graph` | `<root-id>`, `--strategy`, `--max-depth` |

## Anti-Patterns

| Avoid | Why | Instead |
|-------|-----|---------|
| Adding citations without verifying file exists | Adds invalid citations immediately | Let CLI validate on add |
| Skipping confidence updates after verification | Confidence becomes stale | Run `update-confidence` after big code changes |
| Using absolute paths | Breaks on different machines | Use repo-relative paths |
| Adding duplicate citations | Clutters frontmatter | CLI automatically updates existing citations |
| Forgetting to verify after refactoring | Citations go stale silently | Run `verify-all` regularly or in CI |

## Integration with Existing Skills

- **reflect** - Auto-capture citations from learnings that reference code
- **memory** - Verify citations during memory search
- **curating-memories** - Update citations when memories change
- **qa** - Run verification as part of test strategy

## CI Integration (Optional)

Create `.github/workflows/memory-validation.yml`:

```yaml
name: Memory Citation Validation

on:
  pull_request:
    paths:
      - '.serena/memories/**'
      - 'src/**'
      - 'scripts/**'

jobs:
  verify:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@11bd71901bbe5b1630ceea73d27597364c9af683 # v4.2.2
      - uses: actions/setup-python@40c6b50cc6aa807e2d020b243100c016221d604c # v5.3.0
        with:
          python-version: '3.12'
      - run: pip install -e .
      - run: python -m memory_enhancement verify-all --json > results.json
        continue-on-error: true
      - run: cat results.json
      - name: Comment on PR
        if: failure()
        uses: actions/github-script@60a0d83039c74a4aee543508d2ffcb1c3799cdea # v7.0.1
        with:
          script: |
            const results = require('./results.json');
            const stale = results.filter(r => !r.valid);
            if (stale.length > 0) {
              await github.rest.issues.createComment({
                issue_number: context.issue.number,
                owner: context.repo.owner,
                repo: context.repo.name,
                body: `⚠️ ${stale.length} stale memory citation(s) detected. Run \`python -m memory_enhancement verify-all\` locally for details.`
              });
            }
```

Initially set `continue-on-error: true` (warning only). After adoption, make blocking.

## Verification

After using this skill:

- [ ] Citations validated against current codebase
- [ ] Confidence scores updated in memory frontmatter
- [ ] Stale memories identified and reported
- [ ] Health report generated (if requested)
- [ ] Exit codes follow ADR-035 standard

## References

- [examples.md](references/examples.md) - Usage examples and workflows
- [confidence-scoring.md](references/confidence-scoring.md) - How confidence is calculated
- [ADR-007](../../.agents/architecture/ADR-007-memory-first-architecture.md) - Memory-first architecture
- [ADR-037](../../.agents/architecture/ADR-037-reflexion-schema.md) - Reflexion memory schema (if exists)
