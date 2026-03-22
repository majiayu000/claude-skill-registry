---
name: workspace-cleanup
description: Intelligent workspace cleanup using multi-signal detection (similarity, timestamps, references) to identify and archive clutter with two-stage safety review
---

# Workspace Cleanup

## Overview

Automatically clean workspace directories by detecting and archiving clutter using intelligent multi-signal analysis. Reduces AI context pollution from temp files, sync conflicts, and superseded code versions while maintaining safety through archive-based two-stage deletion.

**Core principle:** Safe, intelligent cleanup that understands file drift from AI code generation and protects important files through multi-signal confidence scoring.

## When to Use

- Workspace has accumulated clutter (temp files, old versions, sync conflicts)
- AI context windows are polluted with noise during file scanning
- User mentions cleanup needs ("this is a mess", "clean up experiments", etc.)
- Regular maintenance to prevent drift accumulation

## Problem This Solves

AI assistants (Claude, Codex, Gemini) often create new files instead of updating existing ones:
- `auth.ts` → `auth-new.ts` → `auth-fixed.ts`
- Over time: multiple versions, unclear which is current
- Clutter from system files, temp files, and abandoned experiments
- Context window pollution during code analysis

## Detection System

### Three Core Signals

**1. Similarity Detection**
- Content hash comparison between files
- Filename similarity (Levenshtein distance)
- Flags files with >80% content match + similar names

**2. Timestamp Analysis**
- Last modified time (default: 90 days untouched)
- Last accessed time
- Configurable thresholds

**3. Import/Reference Analysis**
- Grep for imports/requires across codebase
- Search for file references in code/docs
- Flag files with zero references as "unused"

### Tiered Confidence Scoring

**Tier 1 (auto-archive)**: 100% safe to remove
```
System files: .DS_Store, .sync-conflict-*
Build artifacts: __pycache__/, *.pyc, .pytest_cache/
Empty directories (except with .gitkeep)
Version patterns: -old, -backup, -fixed, -new, -updated, .bak
Status files: *.log, *.tmp, temp-*, tmp-*
Exact duplicates: Files with identical SHA256 (archive all but newest)
```

**Tier 2 (archive)**: High confidence (2+ signals)
```
Similar files (80%+ content match) + old timestamp → archive older
Unused + old timestamp
Similarity + unused
```

**Tier 3 (suggest only)**: Low confidence (1 signal)
```
Just old, just unused, or just similar
Large files (>100MB) even with multiple signals
Recently modified similar files (<7 days)
Report for manual review, don't auto-archive
```

## Archive Management

### Central Archive Structure
```
/Users/braydon/projects/archive/cleanup/
├── 2025-11-21-143022/
│   ├── metadata.json
│   └── [preserved directory structure]
└── 2025-10-15-091234/
    ├── metadata.json
    └── [files...]
```

### Two-Stage Safety

**Stage 1: Archive**
- Move files to central archive (never immediate deletion)
- Preserve original directory structure
- Store metadata explaining why each file was archived

**Stage 2: Review (30+ days)**
- Auto-prompt for archives >30 days old
- Show summary of archived contents
- Options: Keep archive, Delete permanently, Restore files, Skip
- Mark reviewed in metadata

### Metadata Format
```json
{
  "timestamp": "2025-11-21T14:30:22Z",
  "scope": "/Users/braydon/projects",
  "recursive": true,
  "files": [
    {
      "original_path": "/Users/braydon/projects/foo.txt",
      "tier": 1,
      "signals": ["pattern_match"],
      "score": 100
    },
    {
      "original_path": "/Users/braydon/projects/experiments/old-auth.ts",
      "tier": 2,
      "signals": ["similarity", "unused", "old_timestamp"],
      "score": 85,
      "similar_to": "experiments/auth.ts"
    }
  ],
  "reviewed": false,
  "review_date": null
}
```

## Protected Patterns

### Three-Layer Protection

**Layer 1: Respect .gitignore**
- If git ignores it, cleanup should too
- Check with: `git check-ignore -q "$file"`
- Prevents cleaning build artifacts, dependencies, etc.

**Layer 2: .cleanupignore**
Optional file for cleanup-specific exclusions:
```
# .cleanupignore
archive/          # Don't clean the archive itself
important-*.md    # Keep files matching pattern
legacy-project/   # Preserve specific directories
```

**Layer 3: Hard-coded System Patterns**
Always protected regardless of ignore files:
```
Directories: .git, .claude, node_modules, .venv, venv, dist, build
Files: package.json, requirements.txt, *.lock, CLAUDE.md, README.md, .env*
```

### Efficient Scanning with Prune

Use find's `-prune` to skip entire protected directory trees:
```bash
find . \( -name node_modules -o -name .git -o -name dist \) -prune \
  -o -type f -name "*.tmp" -print
```

This never even traverses into protected directories, making scans much faster.

## Usage

### Context-Aware Invocation

**From conversation:**
```
User: "This directory is a mess, let's clean it up"
→ Runs recursive cleanup from CWD

User: "Let's clean up the experiments directory"
→ Runs cleanup scoped to /experiments
```

**Explicit commands:**
```bash
/cleanup                          # Current directory
/cleanup --recursive              # Current + subdirs
/cleanup /path/to/dir             # Specific directory
/cleanup --review-archives        # Review old archives
```

## Execution Workflow

When invoked, follow these steps:

### 1. Parse Scope
- Determine target directory from user request or CWD
- Check if recursive or targeted cleanup
- Validate directory exists and is accessible

### 2. Scan & Analyze
```bash
# Build file hash map for duplicate detection
declare -A file_hashes

# Scan with protection (prune protected dirs early)
find . \( -name node_modules -o -name .git -o -name dist -o -name build \) -prune \
  -o -type f -print | while read file; do

  # Layer 1: Check .gitignore
  if git check-ignore -q "$file" 2>/dev/null; then
    continue
  fi

  # Layer 2: Check .cleanupignore (if exists)
  if [[ -f .cleanupignore ]] && grep -q "$(basename "$file")" .cleanupignore; then
    continue
  fi

  # Layer 3: Hard-coded protections
  if [[ "$file" =~ (package\.json|CLAUDE\.md|README\.md|\.env) ]]; then
    continue
  fi

  # === TIER 1 CHECKS (auto-archive) ===

  # Check obvious patterns
  if [[ "$file" =~ (\.DS_Store|\.sync-conflict-|\.tmp$|\.log$) ]]; then
    archive "$file" tier:1 signal:pattern_match
    continue
  fi

  # Check exact duplicates
  hash=$(sha256sum "$file" | cut -d' ' -f1)
  if [[ -n "${file_hashes[$hash]}" ]]; then
    # Found duplicate - archive older file
    original="${file_hashes[$hash]}"
    if [[ "$file" -nt "$original" ]]; then
      archive "$original" tier:1 signal:exact_duplicate duplicate_of:"$file"
      file_hashes[$hash]="$file"
    else
      archive "$file" tier:1 signal:exact_duplicate duplicate_of:"$original"
    fi
    continue
  fi
  file_hashes[$hash]="$file"

  # Check version patterns
  if [[ "$file" =~ (-old|-backup|-fixed|-new|-updated|\.bak)$ ]]; then
    archive "$file" tier:1 signal:version_pattern
    continue
  fi

  # === TIER 2/3 CHECKS (multi-signal) ===
  signals=()

  # Run similarity detection (expensive, do after Tier 1)
  if hasSimilarFile "$file"; then
    signals+=("similarity")
  fi

  # Check timestamps
  if [[ $(find "$file" -mtime +90) ]]; then
    signals+=("old_timestamp")
  fi

  # Check references
  if ! grep -rq "$(basename "$file")" --exclude-dir=node_modules .; then
    signals+=("unused")
  fi

  # Score and tier
  if [[ ${#signals[@]} -ge 2 ]]; then
    archive "$file" tier:2 signals:"${signals[*]}"
  elif [[ ${#signals[@]} -eq 1 ]]; then
    suggest "$file" tier:3 signals:"${signals[*]}"
  fi
done
```

### 3. Archive Files
- Create timestamped archive directory
- Move Tier 1 + Tier 2 files preserving structure
- Generate metadata.json with analysis results
- Skip Tier 3 (just report)

### 4. Report Results
```
🧹 Workspace Cleanup - /Users/braydon/projects
Scope: Recursive | Protected dirs: 8 | Scanning...

📊 Analysis Results:
  • 156 files scanned (78 skipped via protection layers)
  • 23 Tier 1 (auto-archive):
    - System files: .DS_Store (8), sync conflicts (3)
    - Exact duplicates: (6 files, kept newest)
    - Version patterns: -old, -backup files (6)
  • 12 Tier 2 (archive): similar + old or unused
  • 8 Tier 3 (suggestions): review manually

📦 Archiving to: /Users/braydon/projects/archive/cleanup/2025-11-21-143022/
  ✓ Archived 35 files (2.3 MB saved)

💡 Tier 3 Suggestions (not archived):
  • experiments/test-model.py (unused, 45 days old)
  • personal/notes.txt (old, 120 days)
  • work/large-dataset.csv (>100MB, unused - verify before archiving)

⏰ Archives ready for review: 2 archives >30 days old
   Run '/cleanup --review-archives' to review
```

### 5. Check Archives
- Find archives >30 days old
- If found, prompt for review
- Show summary and offer actions

## Archive Review Workflow

```
📋 Archive Review - 2 archives ready

Archive: 2025-10-15-091234 (37 days old)
  • Scope: /Users/braydon/projects (recursive)
  • 18 files archived (1.2 MB)
  • Breakdown:
    - Tier 1: .DS_Store (8), sync conflicts (10)
    - Tier 2: unused code (0)

Actions:
  K - Keep archive (don't prompt again for 30 days)
  D - Delete permanently (CANNOT BE UNDONE)
  R - Restore files to original locations
  S - Skip this review

Your choice [K/D/R/S]:
```

## Configuration

Users can override defaults in `.claude/workspace-cleanup-config.json`:

```json
{
  "timestamp_threshold_days": 90,
  "similarity_threshold": 0.80,
  "archive_review_days": 30,
  "custom_protected_patterns": [
    "important-*.md",
    "do-not-delete/*"
  ],
  "custom_tier1_patterns": [
    "*.tmp",
    "temp-*",
    ".scratch"
  ],
  "excluded_dirs": [
    "special-project"
  ]
}
```

## Implementation Notes

### Exact Duplicate Detection
```bash
# Build hash map of all files
declare -A file_hashes

while read file; do
  # Generate SHA256 hash
  hash=$(sha256sum "$file" | cut -d' ' -f1)

  # Check if we've seen this hash before
  if [[ -n "${file_hashes[$hash]}" ]]; then
    original="${file_hashes[$hash]}"

    # Archive older file, keep newer
    if [[ "$file" -nt "$original" ]]; then
      echo "Duplicate found: $file is newer than $original"
      archive "$original" tier:1 signal:exact_duplicate
      file_hashes[$hash]="$file"  # Update to keep newer
    else
      echo "Duplicate found: $original is newer than $file"
      archive "$file" tier:1 signal:exact_duplicate
    fi
  else
    # First time seeing this content
    file_hashes[$hash]="$file"
  fi
done
```

**Why SHA256:** Strong collision resistance, fast computation, standard tool (sha256sum).

**Edge case:** If duplicates have same mtime, keep first found, archive rest.

### Similarity Detection (for non-exact matches)
```typescript
// Generate content hash for quick comparison
const hash = crypto.createHash('sha256')
  .update(fs.readFileSync(file))
  .digest('hex');

// Compare filenames (Levenshtein distance)
const nameDistance = levenshtein(file1, file2);
const similarity = 1 - (nameDistance / Math.max(file1.length, file2.length));

// Flag if both content and name are similar (but not identical)
if (contentMatch > 0.80 && contentMatch < 1.0 && similarity > 0.70) {
  // Tier 2: Archive older file if also old/unused
}
```

### Reference Detection
```bash
# Use grep to find references
grep -r "import.*${filename}" ${scope}
grep -r "require.*${filename}" ${scope}
grep -r "${filename}" ${scope}

# If no results: unused
```

### Version Pattern Detection
```typescript
const VERSION_PATTERNS = [
  /-old$/, /-backup$/, /-fixed$/, /-new$/,
  /-updated$/, /-v\d+$/, /-copy$/,
  /^old-/, /^backup-/, /^new-/, /^temp-/,
  /\.bak$/, /\.backup$/
];

// When detected + similarity match:
// Keep file without pattern, archive file with pattern
```

## Common Mistakes

**Cleaning without scanning first**
- ❌ Don't skip analysis phase
- ✅ Always scan → analyze → report → archive

**Ignoring Tier 3 suggestions**
- ❌ Tier 3 files might become Tier 2 over time
- ✅ Review suggestions periodically

**Deleting archives too quickly**
- ❌ Don't delete archives <30 days old
- ✅ Wait for review prompt, verify you don't need files

**Not checking protected patterns**
- ❌ Assuming default patterns cover everything
- ✅ Review protected patterns for your workspace

**Running on untracked important work**
- ❌ Don't clean directory with active untracked experiments
- ✅ Commit or stash important work first

## Edge Cases

**Similar files, both recent**
- If both files modified within last 7 days: Tier 3 (suggest only)
- Let user decide which to keep

**Empty directories with .gitkeep**
- Don't archive empty dirs containing .gitkeep
- These are intentionally empty

**Large files (>100MB)**
- Always Tier 3 (suggest only)
- User should explicitly confirm before archiving

**Files in git staging area**
- Skip files with uncommitted changes
- Report as "skipped: uncommitted changes"

## Benefits

1. **AI Context Reduction** - Less noise in context windows
2. **Safety First** - Two-stage archive prevents accidental deletion
3. **Intelligent Detection** - Finds actual clutter, not just patterns
4. **Context Aware** - Adapts to user intent and scope
5. **Low Maintenance** - Mostly automated with sensible defaults
6. **Recoverable** - Everything archived, nothing immediately deleted

## Related Skills

- **learning-from-outcomes** - Learn from cleanup patterns over time
- **coordinating-sub-agents** - Delegate cleanup to specialized agent

## Future Enhancements

- Machine learning on user archive/restore decisions
- Cross-project similarity detection
- Automatic .gitignore updates based on archived patterns
- Integration with project task management
