---
name: clean
description: Intelligent code cleanup with mainline detection, stale artifact discovery, and safe execution. Supports targeted cleanup and confirmation.
argument-hint: "[--dry-run] [--focus=<area>]"
---

# Workflow Clean Command

## Overview

Evidence-based intelligent cleanup command. Systematically identifies stale artifacts through mainline analysis, discovers drift, and safely removes unused sessions, documents, and dead code.

**Core workflow**: Detect Mainline → Discover Drift → Confirm → Stage → Execute

## Target Cleanup

**Focus area**: $FOCUS (or entire project if not specified)
**Mode**: $ARGUMENTS

- `--dry-run`: Preview cleanup without executing
- `--focus`: Focus area (module or path)

## Execution Process

```
Phase 0: Initialization
   ├─ Parse arguments (--dry-run, FOCUS)
   ├─ Setup session folder
   └─ Initialize utility functions

Phase 1: Mainline Detection
   ├─ Analyze git history (30 days)
   ├─ Identify core modules (high commit frequency)
   ├─ Map active vs stale branches
   └─ Build mainline profile

Phase 2: Drift Discovery (Subagent)
   ├─ spawn_agent with cli-explore-agent role
   ├─ Scan workflow sessions for orphaned artifacts
   ├─ Identify documents drifted from mainline
   ├─ Detect dead code and unused exports
   └─ Generate cleanup manifest

Phase 3: Confirmation
   ├─ Validate manifest schema
   ├─ Display cleanup summary by category
   ├─ ASK_USER: Select categories and risk level
   └─ Dry-run exit if --dry-run

Phase 4: Execution
   ├─ Validate paths (security check)
   ├─ Stage deletion (move to .trash)
   ├─ Update manifests
   ├─ Permanent deletion
   └─ Report results
```

## Implementation

### Phase 0: Initialization

##### Step 0: Determine Project Root

检测项目根目录，确保 `.workflow/` 产物位置正确：

```bash
PROJECT_ROOT=$(git rev-parse --show-toplevel 2>/dev/null || pwd)
```

优先通过 git 获取仓库根目录；非 git 项目回退到 `pwd` 取当前绝对路径。
存储为 `{projectRoot}`，后续所有 `.workflow/` 路径必须以此为前缀。

```javascript
const getUtc8ISOString = () => new Date(Date.now() + 8 * 60 * 60 * 1000).toISOString()

// Parse arguments
const args = "$ARGUMENTS"
const isDryRun = args.includes('--dry-run')
const focusMatch = args.match(/FOCUS="([^"]+)"/)
const focusArea = focusMatch ? focusMatch[1] : "$FOCUS" !== "$" + "FOCUS" ? "$FOCUS" : null

// Session setup
const dateStr = getUtc8ISOString().substring(0, 10)
const sessionId = `clean-${dateStr}`
const sessionFolder = `${projectRoot}/.workflow/.clean/${sessionId}`
const trashFolder = `${sessionFolder}/.trash`
const projectRoot = bash('git rev-parse --show-toplevel 2>/dev/null || pwd').trim()

bash(`mkdir -p ${sessionFolder}`)
bash(`mkdir -p ${trashFolder}`)

// Utility functions
function fileExists(p) {
  try { return bash(`test -f "${p}" && echo "yes"`).includes('yes') } catch { return false }
}

function dirExists(p) {
  try { return bash(`test -d "${p}" && echo "yes"`).includes('yes') } catch { return false }
}

function validatePath(targetPath) {
  if (targetPath.includes('..')) return { valid: false, reason: 'Path traversal' }

  const allowed = ['.workflow/', '.claude/rules/tech/', 'src/']
  const dangerous = [/^\//, /^C:\\Windows/i, /node_modules/, /\.git$/]

  if (!allowed.some(p => targetPath.startsWith(p))) {
    return { valid: false, reason: 'Outside allowed directories' }
  }
  if (dangerous.some(p => p.test(targetPath))) {
    return { valid: false, reason: 'Dangerous pattern' }
  }
  return { valid: true }
}
```

---

### Phase 1: Mainline Detection

```javascript
// Check git repository
const isGitRepo = bash('git rev-parse --git-dir 2>/dev/null && echo "yes"').includes('yes')

let mainlineProfile = {
  coreModules: [],
  activeFiles: [],
  activeBranches: [],
  staleThreshold: { sessions: 7, branches: 30, documents: 14 },
  isGitRepo,
  timestamp: getUtc8ISOString()
}

if (isGitRepo) {
  // Commit frequency by directory (last 30 days)
  const freq = bash('git log --since="30 days ago" --name-only --pretty=format: | grep -v "^$" | cut -d/ -f1-2 | sort | uniq -c | sort -rn | head -20')

  // Parse core modules (>5 commits)
  mainlineProfile.coreModules = freq.trim().split('\n')
    .map(l => l.trim().match(/^(\d+)\s+(.+)$/))
    .filter(m => m && parseInt(m[1]) >= 5)
    .map(m => m[2])

  // Recent branches
  const branches = bash('git for-each-ref --sort=-committerdate refs/heads/ --format="%(refname:short)" | head -10')
  mainlineProfile.activeBranches = branches.trim().split('\n').filter(Boolean)
}

Write(`${sessionFolder}/mainline-profile.json`, JSON.stringify(mainlineProfile, null, 2))
```

---

### Phase 2: Drift Discovery

```javascript
let exploreAgent = null

try {
  // Launch cli-explore-agent
  exploreAgent = spawn_agent({
    message: `
## TASK ASSIGNMENT

### MANDATORY FIRST STEPS
1. Read: ~/.codex/agents/cli-explore-agent.md
2. Read: ${projectRoot}/.workflow/project-tech.json (if exists)

## Task Objective
Discover stale artifacts for cleanup.

## Context
- Session: ${sessionFolder}
- Focus: ${focusArea || 'entire project'}

## Discovery Categories

### 1. Stale Workflow Sessions
Scan: ${projectRoot}/.workflow/active/WFS-*, ${projectRoot}/.workflow/archives/WFS-*, ${projectRoot}/.workflow/.lite-plan/*, ${projectRoot}/.workflow/.debug/DBG-*
Criteria: No modification >7 days + no related git commits

### 2. Drifted Documents
Scan: .claude/rules/tech/*, ${projectRoot}/.workflow/.scratchpad/*
Criteria: >30% broken references to non-existent files

### 3. Dead Code
Scan: Unused exports, orphan files (not imported anywhere)
Criteria: No importers in import graph

## Output
Write to: ${sessionFolder}/cleanup-manifest.json

Format:
{
  "generated_at": "ISO",
  "discoveries": {
    "stale_sessions": [{ "path": "...", "age_days": N, "reason": "...", "risk": "low|medium|high" }],
    "drifted_documents": [{ "path": "...", "drift_percentage": N, "reason": "...", "risk": "..." }],
    "dead_code": [{ "path": "...", "type": "orphan_file", "reason": "...", "risk": "..." }]
  },
  "summary": { "total_items": N, "by_category": {...}, "by_risk": {...} }
}
`
  })

  // Wait with timeout handling
  let result = wait({ ids: [exploreAgent], timeout_ms: 600000 })

  if (result.timed_out) {
    send_input({ id: exploreAgent, message: 'Complete now and write cleanup-manifest.json.' })
    result = wait({ ids: [exploreAgent], timeout_ms: 300000 })
    if (result.timed_out) throw new Error('Agent timeout')
  }

  if (!fileExists(`${sessionFolder}/cleanup-manifest.json`)) {
    throw new Error('Manifest not generated')
  }

} finally {
  if (exploreAgent) close_agent({ id: exploreAgent })
}
```

---

### Phase 3: Confirmation

```javascript
// Load and validate manifest
const manifest = JSON.parse(Read(`${sessionFolder}/cleanup-manifest.json`))

// Display summary
console.log(`
## Cleanup Discovery Report

| Category | Count | Risk |
|----------|-------|------|
| Sessions | ${manifest.summary.by_category.stale_sessions} | ${getRiskSummary('sessions')} |
| Documents | ${manifest.summary.by_category.drifted_documents} | ${getRiskSummary('documents')} |
| Dead Code | ${manifest.summary.by_category.dead_code} | ${getRiskSummary('code')} |

**Total**: ${manifest.summary.total_items} items
`)

// Dry-run exit
if (isDryRun) {
  console.log(`
**Dry-run mode**: No changes made.
Manifest: ${sessionFolder}/cleanup-manifest.json
  `)
  return
}

// User confirmation
const selection = ASK_USER([
  {
    id: "categories", type: "multi-select",
    prompt: "Which categories to clean?",
    options: [
      { label: "Sessions", description: `${manifest.summary.by_category.stale_sessions} stale sessions` },
      { label: "Documents", description: `${manifest.summary.by_category.drifted_documents} drifted docs` },
      { label: "Dead Code", description: `${manifest.summary.by_category.dead_code} unused files` }
    ]
  },
  {
    id: "risk", type: "select",
    prompt: "Risk level?",
    options: [
      { label: "Low only", description: "Safest (Recommended)" },
      { label: "Low + Medium", description: "Includes likely unused" },
      { label: "All", description: "Aggressive" }
    ]
  }
])  // BLOCKS (wait for user response)
```

---

### Phase 4: Execution

```javascript
const riskFilter = {
  'Low only': ['low'],
  'Low + Medium': ['low', 'medium'],
  'All': ['low', 'medium', 'high']
}[selection.risk]

// Collect items to clean
const items = []
if (selection.categories.includes('Sessions')) {
  items.push(...manifest.discoveries.stale_sessions.filter(s => riskFilter.includes(s.risk)))
}
if (selection.categories.includes('Documents')) {
  items.push(...manifest.discoveries.drifted_documents.filter(d => riskFilter.includes(d.risk)))
}
if (selection.categories.includes('Dead Code')) {
  items.push(...manifest.discoveries.dead_code.filter(c => riskFilter.includes(c.risk)))
}

const results = { staged: [], deleted: [], failed: [], skipped: [] }

// Validate and stage
for (const item of items) {
  const validation = validatePath(item.path)
  if (!validation.valid) {
    results.skipped.push({ path: item.path, reason: validation.reason })
    continue
  }

  if (!fileExists(item.path) && !dirExists(item.path)) {
    results.skipped.push({ path: item.path, reason: 'Not found' })
    continue
  }

  try {
    const trashTarget = `${trashFolder}/${item.path.replace(/\//g, '_')}`
    bash(`mv "${item.path}" "${trashTarget}"`)
    results.staged.push({ path: item.path, trashPath: trashTarget })
  } catch (e) {
    results.failed.push({ path: item.path, error: e.message })
  }
}

// Permanent deletion
for (const staged of results.staged) {
  try {
    bash(`rm -rf "${staged.trashPath}"`)
    results.deleted.push(staged.path)
  } catch (e) {
    console.error(`Failed: ${staged.path}`)
  }
}

// Cleanup empty trash
bash(`rmdir "${trashFolder}" 2>/dev/null || true`)

// Report
console.log(`
## Cleanup Complete

**Deleted**: ${results.deleted.length}
**Failed**: ${results.failed.length}
**Skipped**: ${results.skipped.length}

### Deleted
${results.deleted.map(p => `- ${p}`).join('\n') || '(none)'}

${results.failed.length > 0 ? `### Failed\n${results.failed.map(f => `- ${f.path}: ${f.error}`).join('\n')}` : ''}

Report: ${sessionFolder}/cleanup-report.json
`)

Write(`${sessionFolder}/cleanup-report.json`, JSON.stringify({
  timestamp: getUtc8ISOString(),
  results,
  summary: {
    deleted: results.deleted.length,
    failed: results.failed.length,
    skipped: results.skipped.length
  }
}, null, 2))
```

---

## Session Folder

```
{projectRoot}/.workflow/.clean/clean-{YYYY-MM-DD}/
├── mainline-profile.json     # Git history analysis
├── cleanup-manifest.json     # Discovery results
├── cleanup-report.json       # Execution results
└── .trash/                   # Staging area (temporary)
```

## Risk Levels

| Risk | Description | Examples |
|------|-------------|----------|
| **Low** | Safe to delete | Empty sessions, scratchpad files |
| **Medium** | Likely unused | Orphan files, old archives |
| **High** | May have dependencies | Files with some imports |

## Security Features

| Feature | Protection |
|---------|------------|
| Path Validation | Whitelist directories, reject traversal |
| Staged Deletion | Move to .trash before permanent delete |
| Dangerous Patterns | Block system dirs, node_modules, .git |

## Iteration Flow

```
First Call (/prompts:clean):
   ├─ Detect mainline from git history
   ├─ Discover stale artifacts via subagent
   ├─ Display summary, await user selection
   └─ Execute cleanup with staging

Dry-Run (/prompts:clean --dry-run):
   ├─ All phases except execution
   └─ Manifest saved for review

Focused (/prompts:clean FOCUS="auth"):
   └─ Discovery limited to specified area
```

## Error Handling

| Situation | Action |
|-----------|--------|
| No git repo | Use file timestamps only |
| Agent timeout | Retry once with prompt, then abort |
| Path validation fail | Skip item, report reason |
| Manifest parse error | Abort with error |
| Empty discovery | Report "codebase is clean" |

---

**Now execute cleanup workflow** with focus: $FOCUS
