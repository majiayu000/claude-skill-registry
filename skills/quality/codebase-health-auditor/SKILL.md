---
name: codebase-health-auditor
description: Unified dead code detection, AST-based duplicate detection, and cleanup tool combining Legacy Tech Remover + Comprehensive Auditor + Architectural Cleanup with Knip, depcheck, TypeScript, Vue-specific analysis, file size/token limit detection, and AST-powered refactoring suggestions. Use for dead code, duplicates, oversized files, and architectural issues.
keywords: dead code, unused files, unused exports, unused dependencies, legacy removal, code cleanup, codebase audit, file size, token limit, large files, refactoring, duplicate code, AST analysis, architectural cleanup, pattern detection
category: code-maintenance
triggers: dead code detection, unused code removal, codebase cleanup, legacy tech audit, dependency cleanup, file too large, token limit exceeded, oversized files, refactoring suggestion, duplicate detection, AST analysis, architectural issues, code quality
---

# Codebase Health Auditor

Comprehensive dead code detection and safe cleanup for Vue 3 + TypeScript projects.

## Overview

A unified skill that merges the best of **Legacy Tech Remover** and **Comprehensive Auditor** while adding modern tooling:

- **File Size/Token Limit**: Detects oversized files that block AI editing (>25K tokens)
- **Knip**: Unused files, exports, dependencies
- **depcheck**: Unused npm packages
- **TypeScript**: noUnusedLocals, noUnusedParameters
- **Vue-specific**: Unused props, emits, computed, watchers
- **Legacy patterns**: Deprecated libraries, orphaned directories

## Quick Start

```bash
# Full audit (dry-run by default)
node .claude/skills/codebase-health-auditor/scripts/orchestrator.js audit

# Execute safe removals only
node .claude/skills/codebase-health-auditor/scripts/orchestrator.js execute --safe-only

# Single detector
node .claude/skills/codebase-health-auditor/scripts/orchestrator.js detect --detector vue

# CI mode
node .claude/skills/codebase-health-auditor/scripts/orchestrator.js audit --ci
```

## Detection Capabilities

### 1. Unused Files & Exports (via Knip)
- Files never imported anywhere
- Exported functions/classes never used
- Types/interfaces never referenced

### 2. Unused Dependencies (via depcheck)
- npm packages in package.json but never imported
- Missing dependencies (imported but not in package.json)
- devDependencies in wrong section

### 3. TypeScript Dead Code
- Unused local variables
- Unused function parameters
- Detects what TypeScript would flag if `noUnusedLocals`/`noUnusedParameters` were enabled

### 4. Vue-Specific Dead Code
- Unused props (defineProps not used in template/script)
- Unused emits (defineEmits never called)
- Unused computed properties
- Unused watchers
- Unused refs/reactive
- Unused imported components

### 5. Legacy Detection (ported from legacy-tech-remover)
- Deprecated libraries (moment, request, jQuery, etc.)
- Legacy config files (Grunt, Gulp, Travis CI)
- Orphaned directories (old/, legacy/, v1/, bak/)
- Files untouched for 2+ years

### 6. File Size & Token Limit Detection ⭐ NEW

Detects files that exceed token limits for AI editing tools like Claude Code.

**Why this matters**: Files over ~25,000 tokens become difficult or impossible for AI tools to edit effectively, causing truncation, context loss, and failed edits.

#### Token Thresholds

| Level | Tokens | ~Size | Meaning |
|-------|--------|-------|---------|
| WARNING | 15,000 | ~60KB | Getting large, monitor |
| CAUTION | 25,000 | ~100KB | Needs attention |
| CRITICAL | 35,000 | ~140KB | Urgent refactoring needed |
| BLOCKED | 50,000 | ~200KB | Blocks AI editing entirely |

#### Quick Usage

```bash
# Detect oversized files
node .claude/skills/codebase-health-auditor/scripts/orchestrator.js detect --detector file-size

# Custom threshold (e.g., only 20K+ tokens)
node .claude/skills/codebase-health-auditor/scripts/orchestrator.js detect --detector file-size --min-tokens 20000

# Save report to file
node .claude/skills/codebase-health-auditor/scripts/orchestrator.js detect --detector file-size --output ./audit-reports/file-size.json
```

#### Sample Output

```
📊 File Size Detection Results
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Files scanned: 156
Files over threshold: 3

By Risk Level:
  🔴 CRITICAL: 1 files
  🟡 CAUTION:  2 files

──────────────────────────────────────────────────
Detailed Findings:

🔴 src/views/CanvasView.vue
   Tokens: 38,500 | Lines: 2,847 | Size: 154.2KB
   Suggestions:
     • 🔴 CRITICAL - High priority refactoring needed
     • Extract script logic into composables (src/composables/)
     • Split into smaller child components
     • URGENT: Major component decomposition needed
     • Consider: extract state to Pinia store

🟡 src/stores/canvas.ts
   Tokens: 28,200 | Lines: 1,245 | Size: 112.8KB
   Suggestions:
     • Split store into feature-specific modules
     • Extract actions/getters into separate files
```

#### Refactoring Suggestions

The detector provides context-aware suggestions based on file type:

**Vue Components (.vue)**:
- Extract script logic into composables
- Split into smaller child components
- Consider state extraction to Pinia stores

**TypeScript/JavaScript (.ts/.js)**:
- Split store into feature-specific modules
- Break into smaller, focused composables
- Apply single responsibility principle
- Extract utility functions to separate files

## Risk Scoring

Each finding is categorized by risk level:

| Category | Score | Meaning | Action |
|----------|-------|---------|--------|
| SAFE | < 20 | Zero usage, high confidence | Auto-remove OK |
| CAUTION | 20-60 | Low/uncertain usage | Manual review |
| RISKY | > 60 | Possible indirect use | Migration needed |

### Risk Factors

| Factor | Weight | Description |
|--------|--------|-------------|
| Usage Count | 30% | How many imports reference this |
| Last Modified | 15% | Git history recency |
| Test Coverage | 20% | Is the code tested? |
| Import Depth | 15% | Transitive dependency depth |
| File Type | 10% | Config files riskier than components |
| Tool Agreement | 10% | Multiple tools agree = higher confidence |

## 4-Phase Workflow

```
┌─────────────────────────────────────────┐
│ PHASE 1: DETECTION                       │
│  - Run all detectors in parallel         │
│  - Deduplicate findings                  │
│  - Tag source (knip/depcheck/vue/etc)    │
└───────────────────┬─────────────────────┘
                    ▼
┌─────────────────────────────────────────┐
│ PHASE 2: ASSESSMENT                      │
│  - Calculate risk scores                 │
│  - Build dependency graph                │
│  - Categorize: SAFE / CAUTION / RISKY    │
└───────────────────┬─────────────────────┘
                    ▼
┌─────────────────────────────────────────┐
│ PHASE 3: ACTION (if --execute)           │
│  - Create backup branch                  │
│  - Remove SAFE items in batches          │
│  - Validate build after each batch       │
│  - Prompt for CAUTION items              │
└───────────────────┬─────────────────────┘
                    ▼
┌─────────────────────────────────────────┐
│ PHASE 4: REPORTING                       │
│  - Generate JSON report                  │
│  - Generate Markdown summary             │
│  - CI exit codes                         │
└─────────────────────────────────────────┘
```

## Configuration

Create `.claude/codebase-health-config.yml`:

```yaml
detection:
  knip:
    enabled: true
    ignore: ["**/*.test.ts", "**/*.stories.ts"]
  depcheck:
    enabled: true
    ignoreMatches: ["@types/*"]
  typescript:
    enabled: true
    noUnusedLocals: true
    noUnusedParameters: true
  vue:
    enabled: true
    detectUnusedProps: true
    detectUnusedEmits: true
    detectUnusedComputed: true
    detectUnusedWatchers: true
  legacy:
    enabled: true
    minYearsUntouched: 2

assessment:
  riskThresholds:
    safe: 20
    caution: 60
  protectedPaths:
    - "src/main.ts"
    - "src/App.vue"
    - "src/stores/**"
  protectedPackages:
    - "vue"
    - "pinia"
    - "vue-router"
    - "typescript"

actions:
  defaultMode: "dry-run"
  batchSize: 5
  validateAfterBatch: true
  gitIntegration:
    autoCommit: true
    commitPrefix: "[codebase-health]"
    createBackupBranch: true

reporting:
  formats: ["json", "markdown"]
  outputDir: "./audit-reports"
  includeBlindSpots: true
```

## Output Examples

### Console Summary
```
Codebase Health Audit Complete

Findings:
  SAFE (auto-remove OK):    23 items
  CAUTION (review needed):  18 items
  RISKY (migration needed):  6 items

By Category:
  Unused exports:     15
  Unused dependencies: 8
  Unused Vue props:   12
  Legacy patterns:     6
  Orphaned files:      6

Estimated Impact:
  Files to remove:    12
  Lines of code:   1,847
  Bundle savings: ~245KB

Run with --execute --safe-only to remove safe items.
```

### JSON Report
```json
{
  "metadata": {
    "timestamp": "2026-01-09T...",
    "version": "1.0.0",
    "executionTime": 45.2
  },
  "summary": {
    "totalFindings": 47,
    "byRisk": { "SAFE": 23, "CAUTION": 18, "RISKY": 6 },
    "byType": { "unused-export": 15, "unused-dependency": 8 }
  },
  "findings": [...]
}
```

## Safety Features

1. **Dry-run by default**: No changes without explicit `--execute`
2. **Backup branch**: Creates `backup/health-audit-YYYYMMDD` before changes
3. **Batch execution**: Removes 5 items at a time, validates between
4. **Build validation**: Runs `npm run build` after each batch
5. **Rollback commands**: Provides git revert commands in report
6. **Protected paths**: Never suggests removing core files

## False Positive Handling

### In Code
```typescript
// @codebase-health-ignore: Used dynamically
export const unusedButNeeded = ...;
```

### In Config
```yaml
detection:
  ignore:
    - "src/utils/polyfills.ts"  # Side-effect imports
    - "**/*.generated.ts"        # Generated code
```

## Known Blind Spots

- Dynamic imports: `import(variable)` cannot be statically analyzed
- Reflection/metaprogramming
- Runtime code generation
- Framework magic (e.g., Vue's `$attrs`, `$slots`)
- Side-effect-only imports

## Integration

This skill supersedes:
- `🧹 legacy-tech-remover` (patterns ported)
- `📊 comprehensive-auditor` (static analysis integrated)

Works alongside:
- `dev-lint-cleanup` - For ESLint-specific fixes
- `document-sync` - To update docs after removal

## CLI Options

| Option | Description |
|--------|-------------|
| `audit` | Run full audit (default: dry-run) |
| `execute` | Execute removal plan |
| `detect --detector <name>` | Run single detector |
| `list` | List available detectors |
| `--path <path>` | Project root directory |
| `--output <file>` | Save JSON report to file |
| `--min-tokens <number>` | Minimum tokens to report (file-size detector) |
| `--safe-only` | Only process SAFE items |
| `--ci` | CI mode with exit codes |
| `--config <path>` | Custom config file |
| `--output-dir <path>` | Report output directory |
| `--format json,markdown` | Report formats |

### Available Detectors

| Detector | Description |
|----------|-------------|
| `file-size` | Detects files exceeding token limits for AI editing |

*More detectors coming: `unused-exports`, `unused-deps`, `vue-dead-code`, `legacy-patterns`*

---

**Version**: 1.0.0
**Author**: Claude Code
**Category**: Code Maintenance
**Created**: January 9, 2026
