---
name: AILANG Post-Release Tasks
description: Run automated post-release workflow (eval baselines, dashboard, docs) for AILANG releases. Executes 46-benchmark suite (medium/hard/stretch) + full standard eval with validation and progress reporting. Use when user says "post-release tasks for vX.X.X" or "update dashboard". Fully autonomous with pre-flight checks.
---

# AILANG Post-Release Tasks

Run post-release tasks for an AILANG release: evaluation baselines, dashboard updates, and documentation.

## Quick Start

**Most common usage:**
```bash
# User says: "Run post-release tasks for v0.3.14"
# This skill will:
# 1. Run eval baseline (ALL 6 PRODUCTION MODELS, both languages) - ALWAYS USE --full FOR RELEASES
# 2. Update website dashboard (JSON with history preservation)
# 3. Extract metrics and UPDATE CHANGELOG.md automatically
# 4. Move design docs from planned/ to implemented/
# 5. Run docs-sync to verify website accuracy (version constants, PLANNED banners, examples)
# 6. Commit all changes to git
```

**🚨 CRITICAL: For releases, ALWAYS use --full flag by default**
- Dev models (without --full) are only for quick testing/validation, NOT releases
- Users expect full benchmark results when they say "post-release" or "update dashboard"
- Never start with dev models and then try to add production models later

## When to Use This Skill

Invoke this skill when:
- User says "post-release tasks", "update dashboard", "run benchmarks"
- After successful release (once GitHub release is published)
- User asks about eval baselines or benchmark results
- User wants to update documentation after a release

## Available Scripts

### `scripts/run_eval_baseline.sh <version> [--full]`
Run evaluation baseline for a release version.

**🚨 CRITICAL: ALWAYS use --full for releases!**

**Usage:**
```bash
# ✅ CORRECT - For releases (ALL 6 production models)
.claude/skills/post-release/scripts/run_eval_baseline.sh 0.3.14 --full
.claude/skills/post-release/scripts/run_eval_baseline.sh v0.3.14 --full

# ❌ WRONG - Only use without --full for quick testing/validation
.claude/skills/post-release/scripts/run_eval_baseline.sh 0.3.14
```

**Output:**
```
Running eval baseline for 0.3.14...
Mode: FULL (all 6 production models)
Expected cost: ~$0.50-1.00
Expected time: ~15-20 minutes

[Running benchmarks...]

✓ Baseline complete
  Results: eval_results/baselines/0.3.14
  Files: 264 result files
```

**What it does:**
- **Step 1**: Runs `make eval-baseline` (standard 0-shot + repair evaluation)
  - Tests both AILANG and Python implementations
  - Uses all 6 production models (--full) or 3 dev models (default)
  - Tests all benchmarks in benchmarks/ directory
- **Step 2**: Runs agent eval on full benchmark suite
  - **Current suite** (v0.4.8+): 46 benchmarks (trimmed from 56)
    - Removed: trivial benchmarks (print tests), most easy benchmarks
    - Kept: fizzbuzz (1 easy for validation), all medium/hard/stretch benchmarks
    - **Stretch goals** (6 new): symbolic_diff, mini_interpreter, lambda_calc,
      graph_bfs, type_unify, red_black_tree
    - Expected: ~55-70% success rate with haiku, higher with sonnet/opus
  - Uses haiku+sonnet (--full) or haiku only (default)
  - Tests both AILANG and Python implementations
- Saves combined results to eval_results/baselines/X.X.X/
- Accepts version with or without 'v' prefix

### `scripts/update_dashboard.sh <version>`
Update website benchmark dashboard with new release data.

**Usage:**
```bash
.claude/skills/post-release/scripts/update_dashboard.sh 0.3.14
```

**Output:**
```
Updating dashboard for 0.3.14...

1/5 Generating Docusaurus markdown...
  ✓ Written to docs/docs/benchmarks/performance.md

2/5 Generating dashboard JSON with history...
  ✓ Written to docs/static/benchmarks/latest.json (history preserved)

3/5 Validating JSON...
  ✓ Version: 0.3.14
  ✓ Success rate: 0.627

4/5 Clearing Docusaurus cache...
  ✓ Cache cleared

5/5 Summary
  ✓ Dashboard updated for 0.3.14
  ✓ Markdown: docs/docs/benchmarks/performance.md
  ✓ JSON: docs/static/benchmarks/latest.json

Next steps:
  1. Test locally: cd docs && npm start
  2. Visit: http://localhost:3000/ailang/docs/benchmarks/performance
  3. Verify timeline shows 0.3.14
  4. Commit: git add docs/docs/benchmarks/performance.md docs/static/benchmarks/latest.json
  5. Commit: git commit -m 'Update benchmark dashboard for 0.3.14'
  6. Push: git push
```

**What it does:**
- Generates Docusaurus-formatted markdown
- Updates dashboard JSON with history preservation
- Validates JSON structure (version matches input exactly)
- Clears Docusaurus build cache
- Provides next steps for testing and committing
- Accepts version with or without 'v' prefix

### `scripts/extract_changelog_metrics.sh [json_file]`
Extract benchmark metrics from dashboard JSON for CHANGELOG.

**Usage:**
```bash
.claude/skills/post-release/scripts/extract_changelog_metrics.sh
# Or specify JSON file:
.claude/skills/post-release/scripts/extract_changelog_metrics.sh docs/static/benchmarks/latest.json
```

**Output:**
```
Extracting metrics from docs/static/benchmarks/latest.json...

=== CHANGELOG.md Template ===

### Benchmark Results (M-EVAL)

**Overall Performance**: 59.1% success rate (399 total runs)

**By Language:**
- **AILANG**: 33.0% - New language, learning curve
- **Python**: 87.0% - Baseline for comparison
- **Gap: 54.0 percentage points (expected for new language)

**Comparison**: -15.2% AILANG regression from 0.3.14 (48.2% → 33.0%)

=== End Template ===

Use this template in CHANGELOG.md for 0.3.15
```

**What it does:**
- Parses dashboard JSON for metrics
- Calculates percentages and gap between AILANG/Python
- **Auto-compares with previous version from history**
- **Formats comparison text automatically** (+X% improvement or -X% regression)
- Generates ready-to-paste CHANGELOG template with no manual work needed

### `scripts/cleanup_design_docs.sh <version> [--dry-run] [--force] [--check-only]`
Move design docs from planned/ to implemented/ after a release.

**Features:**
- Detects **duplicates** (docs already in implemented/)
- Detects **misplaced docs** (Target: field doesn't match folder version)
- Only moves docs with "Status: Implemented" in their frontmatter
- Docs with other statuses are flagged for review

**Usage:**
```bash
# Check-only: Report issues without making changes
.claude/skills/post-release/scripts/cleanup_design_docs.sh 0.5.9 --check-only

# Preview what would be moved/deleted/relocated
.claude/skills/post-release/scripts/cleanup_design_docs.sh 0.5.9 --dry-run

# Execute: Move implemented docs, delete duplicates, relocate misplaced
.claude/skills/post-release/scripts/cleanup_design_docs.sh 0.5.9

# Force move all docs regardless of status
.claude/skills/post-release/scripts/cleanup_design_docs.sh 0.5.9 --force
```

**Output:**
```
Design Doc Cleanup for v0.5.9
==================================

Checking 5 design doc(s) in design_docs/planned/v0_5_9/:

Phase 1: Detecting issues...

  [DUPLICATE] m-fix-if-else-let-block.md
              Already exists in design_docs/implemented/v0_5_9/
  [MISPLACED] m-codegen-value-types.md
              Target: v0.5.10 (folder: v0_5_9)
              Should be in: design_docs/planned/v0_5_10/

Issues found:
  - 1 duplicate(s) (can be deleted)
  - 1 misplaced doc(s) (wrong version folder)

Phase 2: Processing docs...

  [DELETED] m-fix-if-else-let-block.md (duplicate - already in implemented/)
  [RELOCATED] m-codegen-value-types.md → design_docs/planned/v0_5_10/
  [MOVED] m-dx11-cycles.md → design_docs/implemented/v0_5_9/
  [NEEDS REVIEW] m-unfinished-feature.md
                 Found: **Status**: Planned

Summary:
  ✓ Deleted 1 duplicate(s)
  ✓ Relocated 1 doc(s) to correct version folder
  ✓ Moved 1 doc(s) to design_docs/implemented/v0_5_9/
  ⚠ 1 doc(s) need review (not marked as Implemented)
```

**What it does:**
- **Phase 1 (Detection)**: Identifies duplicates and misplaced docs
- **Phase 2 (Processing)**:
  - Deletes duplicates (same file already exists in implemented/)
  - Relocates misplaced docs (Target: version doesn't match folder)
  - Moves docs with "Status: Implemented" to implemented/
  - Flags docs without Implemented status for review
- Creates target folders if needed
- Removes empty planned folder after cleanup
- Use `--check-only` to only report issues, `--dry-run` to preview actions, `--force` to move all

## Post-Release Workflow

### 1. Verify Release Exists

```bash
git tag -l vX.X.X
gh release view vX.X.X
```

If release doesn't exist, run `release-manager` skill first.

### 2. Run Eval Baseline

**🚨 CRITICAL: ALWAYS use --full for releases!**

**Correct workflow:**
```bash
# ✅ ALWAYS do this for releases - ONE command, let it complete
.claude/skills/post-release/scripts/run_eval_baseline.sh X.X.X --full
```

This runs all 6 production models with both AILANG and Python.

**Cost**: ~$0.50-1.00
**Time**: ~15-20 minutes

**❌ WRONG workflow (what happened with v0.3.22):**
```bash
# DON'T do this for releases!
.claude/skills/post-release/scripts/run_eval_baseline.sh X.X.X  # Missing --full!
# Then try to add production models later with --skip-existing
# Result: Confusion, multiple processes, incomplete baseline
```

**If baseline times out or is interrupted:**
```bash
# Resume with ALL 6 models (maintains --full semantics)
ailang eval-suite --full --langs python,ailang --parallel 5 \
  --output eval_results/baselines/X.X.X --skip-existing
```

The `--skip-existing` flag skips benchmarks that already have result files, allowing resumption of interrupted runs. But ONLY use this for recovery, not as a strategy to "add more models later".

### 3. Update Website Dashboard

**Use the automation script:**
```bash
.claude/skills/post-release/scripts/update_dashboard.sh X.X.X
```

**IMPORTANT**: This script automatically:
- Generates Docusaurus markdown (docs/docs/benchmarks/performance.md)
- Updates JSON with history preservation (docs/static/benchmarks/latest.json)
- Does NOT overwrite historical data - merges new version into existing history
- Validates JSON structure before writing
- Clears Docusaurus cache to prevent webpack errors

**Test locally (optional but recommended):**
```bash
cd docs && npm start
# Visit: http://localhost:3000/ailang/docs/benchmarks/performance
```

Verify:
- Timeline shows vX.X.X
- Success rate matches eval results
- No errors or warnings

**Commit dashboard updates:**
```bash
git add docs/docs/benchmarks/performance.md docs/static/benchmarks/latest.json
git commit -m "Update benchmark dashboard for vX.X.X"
git push
```

### 4. Extract Metrics for CHANGELOG

**Generate metrics template:**
```bash
.claude/skills/post-release/scripts/extract_changelog_metrics.sh X.X.X
```

This outputs a formatted template with:
- Overall success rate
- Standard eval metrics (0-shot, final with repair, repair effectiveness)
- Agent eval metrics by language
- **Automatic comparison with previous version** (no manual work!)

**Update CHANGELOG.md automatically:**
1. Run the script to generate the template
2. Insert the "Benchmark Results (M-EVAL)" section into CHANGELOG.md
3. Place it after the feature/fix sections and before the next version

For CHANGELOG template format, see [`resources/version_notes.md`](resources/version_notes.md).

### 4a. Analyze Agent Evaluation Results

```bash
# Get KPIs (turns, tokens, cost by language)
.claude/skills/eval-analyzer/scripts/agent_kpis.sh eval_results/baselines/X.X.X
```

Target metrics: Avg Turns ≤1.5x gap, Avg Tokens ≤2.0x gap vs Python.

For detailed agent analysis guide, see [`resources/version_notes.md`](resources/version_notes.md).

### 5. Move Design Docs to Implemented

**Step 1: Check for issues (duplicates, misplaced docs):**
```bash
.claude/skills/post-release/scripts/cleanup_design_docs.sh X.X.X --check-only
```

**Step 2: Preview all changes:**
```bash
.claude/skills/post-release/scripts/cleanup_design_docs.sh X.X.X --dry-run
```

**Step 3: Check any flagged docs:**
- `[DUPLICATE]` - These will be deleted (already in implemented/)
- `[MISPLACED]` - These will be relocated to correct version folder
- `[NEEDS REVIEW]` - Update `**Status**:` to `Implemented` if done, or leave for next version

**Step 4: Execute the cleanup:**
```bash
.claude/skills/post-release/scripts/cleanup_design_docs.sh X.X.X
```

**Step 5: Commit the changes:**
```bash
git add design_docs/
git commit -m "docs: cleanup design docs for vX_Y_Z"
```

The script automatically:
- Deletes duplicates (same file already in implemented/)
- Relocates misplaced docs (Target: version doesn't match folder)
- Moves docs with "Status: Implemented" to implemented/
- Flags remaining docs for manual review

### 6. Update Public Documentation

- Update `prompts/` with latest AILANG syntax
- Update website docs (`docs/`) with latest features
- Remove outdated examples or references
- Add new examples to website
- Update `docs/guides/evaluation/` if significant benchmark improvements
- **Update `docs/LIMITATIONS.md`**:
  - Remove limitations that were fixed in this release
  - Add new known limitations discovered during development/testing
  - Update workarounds if they changed
  - Update version numbers in "Since" and "Fixed in" fields
  - **Test examples**: Verify that limitations listed still exist and workarounds still work
    ```bash
    # Test examples from LIMITATIONS.md
    # Example: Test Y-combinator still fails (should fail)
    echo 'let Y = \f. (\x. f(x(x)))(\x. f(x(x))) in Y' | ailang repl

    # Example: Test named recursion works (should succeed)
    ailang run examples/factorial.ail

    # Example: Test polymorphic operator limitation (should panic with floats)
    # Create test file and verify behavior matches documentation
    ```
  - Commit changes: `git add docs/LIMITATIONS.md && git commit -m "Update LIMITATIONS.md for vX.X.X"`

### 7. Run Documentation Sync Check

**Run docs-sync to verify website accuracy:**
```bash
# Check version constants are correct
.claude/skills/docs-sync/scripts/check_versions.sh

# Audit design docs vs website claims
.claude/skills/docs-sync/scripts/audit_design_docs.sh

# Generate full sync report
.claude/skills/docs-sync/scripts/generate_report.sh
```

**What docs-sync checks:**
- Version constants in `docs/src/constants/version.js` match git tag
- Teaching prompt references point to latest version
- Architecture pages have PLANNED banners for unimplemented features
- Design docs status (planned vs implemented) matches website claims
- Examples referenced in website actually work

**If issues found:**
1. Update version.js if stale
2. Add PLANNED banners to theoretical feature pages
3. Move implemented features from roadmap to current sections
4. Fix broken example references

**Commit docs-sync fixes:**
```bash
git add docs/
git commit -m "docs: sync website with vX.X.X implementation"
```

See [docs-sync skill](../docs-sync/SKILL.md) for full documentation.

## Resources

### Post-Release Checklist
See [`resources/post_release_checklist.md`](resources/post_release_checklist.md) for complete step-by-step checklist.

## Prerequisites

- Release vX.X.X completed successfully
- Git tag vX.X.X exists
- GitHub release published with all binaries
- `ailang` binary installed (for eval baseline)
- Node.js/npm installed (for dashboard, optional)

## Common Issues

### Eval Baseline Times Out
**Solution**: Use `--skip-existing` flag to resume:
```bash
bin/ailang eval-suite --full --skip-existing --output eval_results/baselines/vX.X.X
```

### Dashboard Shows "null" for Aggregates
**Cause**: Wrong JSON file (performance matrix vs dashboard JSON)
**Solution**: Use `update_dashboard.sh` script, not manual file copying

### Webpack/Cache Errors in Docusaurus
**Cause**: Stale build cache
**Solution**: Run `cd docs && npm run clear && rm -rf .docusaurus build`

### Dashboard Shows Old Version
**Cause**: Didn't run update_dashboard.sh with correct version
**Solution**: Re-run `update_dashboard.sh X.X.X` with correct version

## Progressive Disclosure

This skill loads information progressively:

1. **Always loaded**: This SKILL.md file (YAML frontmatter + workflow overview)
2. **Execute as needed**: Scripts in `scripts/` directory (automation)
3. **Load on demand**: `resources/post_release_checklist.md` (detailed checklist)

Scripts execute without loading into context window, saving tokens while providing powerful automation.

## Version Notes

For historical improvements and lessons learned, see [`resources/version_notes.md`](resources/version_notes.md).

Key points:
- All scripts accept version with or without 'v' prefix
- Use `--validate` flag to check configuration before running
- Agent eval requires explicit `--benchmarks` list (defined in script)

## Notes

- This skill follows Anthropic's Agent Skills specification (Oct 2025)
- Scripts handle 100% of automation (eval baseline, dashboard, metrics extraction, design docs)
- Can be run hours or even days after release
- Dashboard JSON preserves history - never overwrites historical data
- Always use `--full` flag for release baselines (all production models)
- Design docs cleanup now handles duplicates, misplaced docs, and status-based moves
  - `--check-only` to report issues without changes
  - `--dry-run` to preview all actions
  - `--force` to move all regardless of status
