---
name: living-docs
description: Launch or resume Living Docs Builder independently. Generates comprehensive enterprise documentation from codebase analysis with AI-powered insights. LSP-enhanced by default for accurate API extraction.
argument-hint: [--resume jobId] [--depth level] [--full-scan]
---

# Living Docs Builder (Standalone)

**Usage**: `/sw:living-docs [options]`

---

## Purpose

Launch the Living Docs Builder independently of `specweave init`. This is essential for:
- **Resuming after crash** - Claude Code crashed after init, need to restart living docs
- **On-demand analysis** - Re-analyze codebase after major changes
- **Large brownfield projects** - Run targeted analysis on specific modules
- **CI/CD integration** - Automate documentation generation
- **Enterprise knowledge base** - Generate comprehensive "wikipedia-style" documentation of your entire organization

---

## LSP-Enhanced Analysis (DEFAULT)

**LSP is ENABLED BY DEFAULT** for all living docs operations. This dramatically improves documentation accuracy:

| Without LSP (--no-lsp) | With LSP (DEFAULT) |
|------------------------|-------------------|
| Grep-based symbol search (~45s) | Semantic symbol resolution (~50ms) |
| Text-based import parsing | Accurate dependency graphs |
| Limited type inference | Full type hierarchy |
| May miss indirect references | Complete reference tracking |

**LSP runs automatically** - just ensure language servers are installed:
```bash
# Full scan (LSP enabled by default)
/sw:living-docs --full-scan

# Install language servers for your stack:
npm install -g typescript-language-server typescript  # TypeScript/JS
pip install python-lsp-server                          # Python
go install golang.org/x/tools/gopls@latest            # Go
rustup component add rust-analyzer                     # Rust

# Disable LSP only if needed (not recommended):
/sw:living-docs --full-scan --no-lsp
```

**LSP provides** (automatically):
- **Accurate API surface extraction** - All exports, types, signatures with full type info
- **Semantic dependency graphs** - Based on actual symbol resolution, not text patterns
- **Dead code detection** - Identifies unreferenced symbols across codebase
- **Type hierarchy maps** - Interface implementations, class inheritance
- **Cross-module relationships** - Precise "used by" and "depends on" mappings

---

## Command Options

| Option | Description |
|--------|-------------|
| (none) | Interactive mode - prompts for configuration |
| `--resume <jobId>` | Resume orphaned/paused living-docs job |
| `--depth <level>` | Analysis depth: `quick`, `standard`, `deep-native`, `deep-interactive` |
| `--priority <modules>` | Priority modules (comma-separated): `auth,payments,api` |
| `--sources <folders>` | Additional doc folders (comma-separated): `docs/,wiki/` |
| `--depends-on <jobIds>` | Wait for jobs before starting (comma-separated) |
| `--foreground` | Run in current session instead of background |
| `--force` | Force run even for greenfield projects |
| `--full-scan` | **Force full enterprise scan** - All 8 phases including enterprise KB, delivery/ops docs, diagrams |
| `--no-lsp` | **Disable LSP analysis** - Falls back to grep-based symbol search (not recommended, use only if language servers unavailable) |

---

## Quick Start

### Launch New Analysis (Interactive)

```bash
/sw:living-docs

# Prompts for:
# 1. Analysis depth (quick/standard/deep-native/deep-interactive)
# 2. Priority modules to focus on
# 3. Additional documentation sources
# 4. Confirmation to launch
```

### Resume After Crash

```bash
# Check for orphaned jobs first
/sw:jobs

# If you see an orphaned living-docs-builder job:
/sw:living-docs --resume abc12345

# Or let it auto-detect:
/sw:living-docs
# → "Found orphaned job abc12345. Resume? [Y/n]"
```

### Quick Analysis (Non-Interactive)

```bash
# Quick scan - basic structure + imports + tech detection + inconsistencies
/sw:living-docs --depth quick

# Standard analysis - modules + dependencies + relationships + diagrams
/sw:living-docs --depth standard --priority auth,payments

# AI-powered deep analysis (FREE with MAX subscription)
/sw:living-docs --depth deep-native --priority core,api

# FULL ENTERPRISE SCAN - All 8 phases (A through H)
# Generates complete knowledge base: company history, team structure, delivery docs, diagrams
/sw:living-docs --full-scan
```

---

## Analysis Depths

| Depth | Scope | What It Does | Cost |
|-------|-------|--------------|------|
| `quick` | Core analysis | Structure scan + tech detection + imports map + inconsistency detection + basic diagrams | Free |
| `standard` | Full module analysis | Module deep-dive + exports + dependencies + relationships + team detection + Mermaid diagrams | Free |
| `deep-native` | Intelligent analysis | ⭐ AI-powered understanding: purpose extraction, pattern recognition, organization synthesis | FREE (MAX) |
| `deep-interactive` | Enterprise knowledge | AI analysis in current session with full enterprise KB generation (checkpoint/resume) | FREE (MAX) |

### Quick Depth Features (Expanded)

Quick mode now includes:
- File structure discovery across all repos
- Technology stack detection (frameworks, languages, tools)
- Import/export dependency mapping
- **Basic inconsistency detection** (duplicates, naming issues)
- **Basic Mermaid diagrams** (module structure, imports)
- External specification loading (GitHub/JIRA/ADO imports)

### Standard Depth Features (Expanded)

Standard mode adds:
- Deep module analysis with exports/APIs
- Cross-module dependency graphs
- **Team structure inference** from code ownership
- **Relationship mapping** (feature-to-code, team-to-features)
- **Full Mermaid diagram suite** (org charts, dependencies, timelines)
- Basic architecture detection (patterns, ADR candidates)
- Spec-code gap detection

### Full Scan Mode (--full-scan) - Enterprise Knowledge Base

**What it does**: Forces a comprehensive deep analysis through **ALL 8 PHASES (A-H)**, generating a complete enterprise knowledge base that serves as a "living wikipedia" for your organization.

**When to use**:
- Initial setup - want complete documentation structure
- After major refactoring - need fresh analysis of everything
- Imported external repos - want full org structure, inconsistencies, strategy docs
- Enterprise documentation - need company history, team directory, delivery docs
- Complete living docs - all folders populated with cross-referenced documentation

**Duration**: Variable based on project size and complexity. For large enterprise projects (50+ repos, 247+ microservices), **expect this to run over multiple sessions spanning days or weeks**. The checkpoint/resume system ensures no work is lost.

**What you get** (complete enterprise knowledge base):
```
.specweave/docs/internal/
├── repos/                      # Per-repo analysis (Phase B)
│   └── {repo-name}/
│       ├── overview.md         # Purpose, key concepts, patterns
│       └── api-surface.md      # All public APIs documented
│
├── organization/               # Team structure (Phase C)
│   ├── teams/
│   │   └── {team-name}.md      # Responsibilities, expertise, tech stack
│   ├── microservices/          # Service boundaries
│   ├── domains/                # Domain groupings
│   └── org-synthesis.md        # Organization overview
│
├── architecture/               # System architecture (Phase D)
│   ├── adr/                    # Auto-detected ADRs with evidence
│   │   └── 0001-pattern-name.md
│   ├── system-architecture.md  # High-level architecture
│   └── c4-diagrams/            # C4 model diagrams
│
├── review-needed/              # Categorized issues (Phase E) ✨
│   ├── index.md                # Overview with priority summary
│   ├── CRITICAL-ISSUES.md      # P0: Must fix immediately
│   ├── BROKEN-LINKS.md         # All broken references
│   ├── SPEC-CODE-GAPS.md       # Ghost completions, missing impl
│   ├── ORPHANED-DOCS.md        # Docs without owners
│   └── tech-debt-catalog.md    # Categorized tech debt
│
├── strategy/                   # Strategic recommendations (Phase F) ✨
│   ├── recommendations.md      # Prioritized action items
│   ├── modernization.md        # Migration/upgrade candidates
│   └── risk-assessment.md      # Security and compliance risks
│
├── enterprise/                 # Enterprise KB (Phase G) ✨✨ NEW
│   ├── COMPANY-HISTORY.md      # Timeline of project evolution
│   ├── FEATURE-CATALOG.md      # All features with status/ownership
│   ├── TEAM-DIRECTORY.md       # Team roster with expertise areas
│   └── PROJECT-METRICS.md      # Stats: features, completions, velocity
│
├── delivery/                   # Delivery documentation (Phase G) ✨✨ NEW
│   ├── RELEASE-HISTORY.md      # All releases with changelogs
│   ├── CI-CD-PIPELINE.md       # Pipeline documentation
│   ├── DEPLOYMENT-GUIDE.md     # How to deploy
│   └── ENVIRONMENTS.md         # Environment configurations
│
├── operations/                 # Ops documentation (Phase G) ✨✨ NEW
│   ├── RUNBOOKS.md             # Operational procedures
│   ├── MONITORING.md           # What to monitor
│   ├── INCIDENT-HISTORY.md     # Past incidents (if any)
│   └── SLA-TRACKING.md         # Service level targets
│
├── relationships/              # Cross-references (Phase G) ✨✨ NEW
│   ├── FEATURE-TO-CODE.md      # Feature → file mappings
│   ├── TEAM-TO-FEATURES.md     # Team → owned features
│   ├── MODULE-DEPENDENCIES.md  # Module → module deps
│   └── EXTERNAL-REFS.md        # External tool linkages
│
└── diagrams/                   # Mermaid diagrams (Phase H) ✨✨ NEW
    ├── feature-hierarchy.md    # Feature tree visualization
    ├── team-org-chart.md       # Team structure
    ├── module-dependencies.md  # Dependency graph
    ├── project-timeline.md     # Gantt chart of evolution
    ├── system-architecture.md  # C4 context diagram
    └── feature-status.md       # Pie chart of completion
```

**Command**:
```bash
/sw:living-docs --full-scan

# Uses deep-native (Claude MAX) for AI-powered analysis
# Runs ALL 8 phases: A → B → C → D → E → F → G → H
# Checkpoint/resume: Can stop and continue from any phase
# Enterprise projects: May take multiple sessions (days/weeks)
```

**Resume after interruption**:
```bash
# Check progress
/sw:jobs

# Resume from checkpoint (all previous work preserved)
/sw:living-docs --resume <jobId>
```

### Deep-Native (Recommended for MAX Users)

Uses your Claude MAX subscription via `claude --print`:
- **No extra cost** - included in MAX
- Runs in **background** - survives terminal close
- **Checkpoint/resume** - can resume from any phase
- Uses **Opus 4.5** for best quality

```bash
/sw:living-docs --depth deep-native

# Monitor progress:
/sw:jobs --follow <jobId>
```

---

## The 8 Phases of Enterprise Analysis

Full scan (`--full-scan`) executes all 8 phases sequentially with checkpoint/resume support:

| Phase | Name | What It Does | Output |
|-------|------|--------------|--------|
| **A** | Discovery | Scan file structure, detect repos, identify entry points | Internal state |
| **B** | Deep Analysis | AI-powered per-repo understanding: purpose, concepts, APIs, patterns | `repos/{name}/overview.md`, `api-surface.md` |
| **C** | Org Synthesis | Infer team structure, microservices, domains from code patterns | `organization/teams/`, `microservices/`, `domains/` |
| **D** | Architecture | Detect architectural decisions, generate ADRs, system diagrams | `architecture/adr/`, `system-architecture.md` |
| **E** | Inconsistencies | Find issues: broken links, spec-code gaps, orphaned docs, duplicates | `review-needed/CRITICAL-ISSUES.md`, `BROKEN-LINKS.md`, etc. |
| **F** | Strategy | Generate recommendations, tech debt catalog, modernization roadmap | `strategy/recommendations.md`, `tech-debt-catalog.md` |
| **G** | Enterprise | Build knowledge base: history, feature catalog, delivery docs, runbooks | `enterprise/`, `delivery/`, `operations/`, `relationships/` |
| **H** | Diagrams | Generate Mermaid visualizations: org charts, dependencies, timelines | `diagrams/*.md` |

**Checkpoint/Resume**: Each phase completion is checkpointed. If interrupted, resume continues from the last completed phase - no work is lost.

**Enterprise Scale**: For large organizations (50+ repos), phases B-G may each take significant time. The system is designed for long-running analysis that spans multiple sessions.

---

## Implementation Steps

When this command is invoked:

### Step 1: Check for Orphaned Jobs

```typescript
import { getOrphanedJobs, getJobManager } from '../../../src/core/background/job-launcher.js';

const orphaned = getOrphanedJobs(projectPath).filter(j => j.type === 'living-docs-builder');
if (orphaned.length > 0) {
  // Prompt: "Found orphaned job {id}. Resume? [Y/n]"
  // If yes: resume job
  // If no: ask if they want to start fresh
}
```

### Step 2: Collect Configuration (if not --resume)

If no `--resume` flag and no auto-resume:

```typescript
import { collectLivingDocsInputs } from '../../../src/cli/helpers/init/living-docs-preflight.js';

const result = await collectLivingDocsInputs({
  projectPath,
  language: 'en',
  isCi: hasFlags, // Skip prompts if flags provided
});
```

Override with flags:
- `--depth` → `result.userInputs.analysisDepth`
- `--priority` → `result.userInputs.priorityAreas`
- `--sources` → `result.userInputs.additionalSources`

### Step 3: Launch Job

```typescript
import { launchLivingDocsJob } from '../../../src/core/background/job-launcher.js';

const { job, pid, isBackground } = await launchLivingDocsJob({
  projectPath,
  userInputs: result.userInputs,
  dependsOn: dependsOnJobIds,
  foreground: hasForegroundFlag,
});
```

### Step 4: Display Status

```
✅ Living Docs Builder launched!

   Job ID: ldb-abc12345
   Depth: deep-native (Claude Code Opus 4.5)
   Priority: auth, payments, api
   PID: 45678

   Monitor: /sw:jobs --follow ldb-abc12345
   Logs: /sw:jobs --logs ldb-abc12345

💡 This job runs in background and survives terminal close.
   Output will be saved to:
   - .specweave/docs/SUGGESTIONS.md
   - .specweave/docs/ENTERPRISE-HEALTH.md
```

---

## Resume Behavior

When resuming a job:

1. **Load checkpoint** from `.specweave/state/jobs/<jobId>/checkpoints/`
2. **Skip completed phases**:
   - `waiting` → dependency waiting
   - `discovery` → codebase scanning
   - `foundation` → high-level docs
   - `integration` → work item matching
   - `deep-dive` → module analysis (per-module checkpoints)
   - `suggestions` → recommendations
   - `enterprise` → health report
3. **Continue from resume point**

```bash
# Example: Job crashed during deep-dive phase
/sw:living-docs --resume abc12345

# Output:
# Resuming from checkpoint: phase=deep-dive, module=auth (5/18)
# ✓ Skipping completed phases: waiting, discovery, foundation, integration
# → Continuing deep-dive from module: payments
```

---

## Waiting for Dependencies

For umbrella projects with clone/import jobs:

```bash
# Launch after clone completes
/sw:living-docs --depends-on clone-xyz123 --depth standard

# Launch after both clone and import complete
/sw:living-docs --depends-on clone-xyz123,import-abc456
```

The job will:
1. Enter `waiting` phase
2. Poll dependency status every 30 seconds
3. Start analysis once all dependencies complete
4. Warn if any dependency failed (proceeds with available data)

---

## Update Summary

After completion, you'll see a detailed summary showing:

```
✅ LIVING DOCS UPDATE COMPLETE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📊 SUMMARY:

  Discovery: Discovered 3 repos (2,845 files)
    Duration: 5s

  Analysis: Analyzed 3 repos
    Duration: 127s

  Synthesis: Generated 12 ADRs, 4 teams
    Duration: 43s

  Files Created: 47
    • .specweave/docs/internal/repos/main/overview.md
    • .specweave/docs/internal/repos/main/api-surface.md
    • .specweave/docs/internal/architecture/system-architecture.md
    • .specweave/docs/internal/architecture/adr/0001-typescript-migration.md
    • .specweave/docs/internal/architecture/adr/0002-plugin-system.md
    ... and 42 more

  Files Updated: 8
    • .specweave/docs/internal/modules/auth.md
    • .specweave/docs/internal/modules/payments.md
    ... and 6 more

  Total Duration: 175s
  Mode: INCREMENTAL (cache used)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

## Output Files

After completion (varies by depth):

### Core Output (All Depths)

| File | Description |
|------|-------------|
| `.specweave/docs/SUGGESTIONS.md` | Documentation recommendations by priority |
| `.specweave/docs/ENTERPRISE-HEALTH.md` | Health score, coverage, accuracy metrics |
| `.specweave/docs/overview/PROJECT-OVERVIEW.md` | Auto-generated project overview |
| `.specweave/docs/overview/TECH-STACK.md` | Detected technologies and frameworks |
| `.specweave/docs/modules/*.md` | Per-module documentation |

### Standard+ Output

| Folder | Description |
|--------|-------------|
| `.specweave/docs/internal/organization/` | Team structure, microservices, domains |
| `.specweave/docs/internal/relationships/` | Feature-to-code, team-to-features mappings |
| `.specweave/docs/internal/diagrams/` | Mermaid diagrams for visual navigation |

### Full Scan Output (Enterprise KB)

| Folder | Description |
|--------|-------------|
| `.specweave/docs/internal/repos/` | Per-repo deep analysis with APIs |
| `.specweave/docs/internal/architecture/` | ADRs, system architecture, C4 diagrams |
| `.specweave/docs/internal/review-needed/` | Categorized issues (P0-P3) with remediation |
| `.specweave/docs/internal/strategy/` | Recommendations, modernization, risk assessment |
| `.specweave/docs/internal/enterprise/` | Company history, feature catalog, team directory |
| `.specweave/docs/internal/delivery/` | CI/CD, releases, deployment guides |
| `.specweave/docs/internal/operations/` | Runbooks, monitoring, SLAs |

---

## Examples

### Example 1: Post-Crash Resume

```bash
# Claude crashed after init, living docs job orphaned

# Step 1: Check what's there
/sw:jobs
# Shows: [ldb-abc123] living-docs-builder - ORPHANED (worker died)

# Step 2: Resume
/sw:living-docs --resume ldb-abc123

# Output:
# ✅ Resuming Living Docs Builder (ldb-abc123)
#    Last checkpoint: deep-dive phase, module 12/45
#    Continuing from: payments-service
```

### Example 2: Large Enterprise (247 repos)

```bash
# Full enterprise scan - generates complete knowledge base
# For large projects, this runs across multiple sessions
/sw:living-docs --full-scan --depends-on clone-main123

# Monitor progress (runs in background, survives terminal close)
/sw:jobs --follow ldb-xyz789

# Resume after interruption (all progress preserved)
/sw:living-docs --resume ldb-xyz789

# Alternatively: Focus on critical modules first (faster initial pass)
/sw:living-docs --depth standard \
  --priority auth,payments,billing,core
```

### Example 3: CI/CD Integration

```bash
# In CI pipeline (non-interactive)
specweave living-docs --depth quick --foreground

# Or background with polling
specweave living-docs --depth standard
specweave jobs --wait ldb-latest  # Wait for completion
```

---

## Error Handling

### Worker Crashed
```
/sw:jobs
# Shows: ORPHANED status

/sw:living-docs --resume <jobId>
# Resumes from last checkpoint
```

### Dependency Failed
```
⚠️  Dependency clone-xyz123 failed
    Reason: Network timeout

Proceeding with available data...
Some repositories may be missing from analysis.
```

### No Brownfield Detected
```
ℹ️  No existing code detected (greenfield project)
    Living docs will sync automatically as you create increments.

    To force analysis anyway: /sw:living-docs --force
```

---

## See Also

- `/sw:jobs` - Monitor all background jobs
- `/sw:import-docs` - Import existing documentation
- `specweave:brownfield-analyzer` skill - Analyze doc gaps
- `specweave:brownfield-onboarder` skill - Merge existing docs

---

**Implementation**: `src/cli/commands/living-docs.ts`
