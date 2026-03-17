---
name: ride
description: Analyze codebase to extract reality into Loa artifacts
context: fork
agent: Explore
allowed-tools: Read, Grep, Glob, Bash(git *)
---

# Riding Through the Codebase

You are analyzing an existing codebase to generate evidence-grounded Loa artifacts following the v0.6.0 Enterprise-Grade Managed Scaffolding model.

> *"The Loa rides through the code, channeling truth into the grimoire."*

## Core Principles

```
CODE IS TRUTH → Loa channels CODE → Grimoire reflects REALITY
```

1. **Never trust documentation** - Verify everything against code
2. **Flag, don't fix** - Dead code/issues flagged for human decision
3. **Evidence required** - Every claim needs `file:line` citation
4. **Target repo awareness** - Grimoire lives WITH the code it documents

---

## Phase 0: Preflight & Mount Verification

### 0.1 Verify Loa is Mounted

```bash
if [[ ! -f ".loa-version.json" ]]; then
  echo "❌ Loa not mounted on this repository"
  echo ""
  echo "The Loa must mount before it can ride."
  echo "Run '/mount' first, or:"
  echo "  curl -fsSL https://raw.githubusercontent.com/0xHoneyJar/loa/main/.claude/scripts/mount-loa.sh | bash"
  exit 1
fi

VERSION=$(jq -r '.framework_version' .loa-version.json)
echo "✓ Loa mounted (v$VERSION)"
```

### 0.2 System Zone Integrity Check (BLOCKING)

Before the Loa can ride, verify the System Zone hasn't been tampered with:

```bash
CHECKSUMS_FILE=".claude/checksums.json"
FORCE_RESTORE="${1:-false}"

if [[ ! -f "$CHECKSUMS_FILE" ]]; then
  echo "⚠️ No checksums found - skipping integrity check (first ride?)"
else
  echo "🔐 Verifying System Zone integrity..."

  DRIFT_DETECTED=false
  DRIFTED_FILES=()

  while IFS= read -r file; do
    expected=$(jq -r --arg f "$file" '.files[$f] // empty' "$CHECKSUMS_FILE")
    [[ -z "$expected" ]] && continue

    if [[ -f "$file" ]]; then
      actual=$(sha256sum "$file" | cut -d' ' -f1)
      if [[ "$expected" != "$actual" ]]; then
        DRIFT_DETECTED=true
        DRIFTED_FILES+=("$file")
      fi
    else
      DRIFT_DETECTED=true
      DRIFTED_FILES+=("$file (MISSING)")
    fi
  done < <(jq -r '.files | keys[]' "$CHECKSUMS_FILE")

  if [[ "$DRIFT_DETECTED" == "true" ]]; then
    echo ""
    echo "╔═════════════════════════════════════════════════════════════════╗"
    echo "║  ⛔ SYSTEM ZONE INTEGRITY VIOLATION                             ║"
    echo "╚═════════════════════════════════════════════════════════════════╝"
    echo ""
    echo "The following framework files have been modified:"
    for f in "${DRIFTED_FILES[@]}"; do
      echo "  ✗ $f"
    done
    echo ""
    echo "The Loa cannot ride with a corrupted saddle."
    echo ""
    echo "Options:"
    echo "  1. Move customizations to .claude/overrides/ (recommended)"
    echo "  2. Run '/ride --force-restore' to reset System Zone"
    echo "  3. Run '/update-loa --force-restore' to sync from upstream"
    echo ""

    if [[ "$FORCE_RESTORE" == "--force-restore" ]]; then
      echo "Force-restoring System Zone from upstream..."
      git checkout loa-upstream/main -- .claude 2>/dev/null || {
        echo "❌ Failed to restore - run '/mount' to reinstall"
        exit 1
      }
      echo "✓ System Zone restored"
    else
      echo "❌ BLOCKED: Use --force-restore to override"
      exit 1
    fi
  else
    echo "✓ System Zone integrity verified"
  fi
fi
```

### 0.3 Detect Execution Context

```bash
CURRENT_DIR=$(pwd)
CURRENT_REPO=$(basename "$CURRENT_DIR")

# Check if we're in the Loa framework repo
if [[ -f ".claude/commands/ride.md" ]] && [[ -d ".claude/skills/riding-codebase" ]]; then
  IS_FRAMEWORK_REPO=true
  echo "📍 Detected: Running from Loa framework repository"
else
  IS_FRAMEWORK_REPO=false
  TARGET_REPO="$CURRENT_DIR"
  echo "📍 Detected: Running from project repository"
fi
```

### 0.4 Target Resolution (Framework Repo Only)

If `IS_FRAMEWORK_REPO=true`, use `AskUserQuestion` to select target:

```markdown
## Target Repository Required

You're running /ride from the Loa framework repo.

**Which codebase should the Loa ride?**

Options:
1. Specify path: `/ride --target ../thj-envio`
2. Select sibling repo: [list siblings]

⚠️ The Loa rides codebases, not itself.
```

### 0.5 Initialize Ride Trajectory

```bash
RIDE_DATE=$(date -u +%Y-%m-%dT%H:%M:%SZ)
TRAJECTORY_FILE="grimoires/loa/a2a/trajectory/riding-$(date +%Y%m%d).jsonl"
mkdir -p grimoires/loa/a2a/trajectory

echo '{"timestamp":"'$RIDE_DATE'","agent":"riding-codebase","phase":0,"action":"preflight","status":"complete"}' >> "$TRAJECTORY_FILE"
```

---

<attention_budget>
## Attention Budget

This skill follows the **Tool Result Clearing Protocol** (`.claude/protocols/tool-result-clearing.md`).

### Token Thresholds

| Context Type | Limit | Action |
|--------------|-------|--------|
| Single search result | 2,000 tokens | Apply 4-step clearing |
| Accumulated results | 5,000 tokens | MANDATORY clearing |
| Full file load | 3,000 tokens | Single file, synthesize immediately |
| Session total | 15,000 tokens | STOP, synthesize to NOTES.md |

### Clearing Triggers for Codebase Riding

- [ ] `grep`/`ripgrep` returning >20 matches
- [ ] `find`/`glob` returning >30 files
- [ ] File reads >100 lines
- [ ] Any output exceeding 2K tokens

### 4-Step Clearing

1. **Extract**: Max 10 files, 20 words per finding, with `file:line` refs
2. **Synthesize**: Write to `grimoires/loa/reality/` or NOTES.md
3. **Clear**: Remove raw output from context
4. **Summary**: `"Probe: N files → M relevant → reality/"`

### RLM Pattern Alignment

The Retrieve-Load-Modify (RLM) pattern naturally enforces attention budget:
- **Retrieve**: Probe first, don't load eagerly
- **Load**: JIT retrieval of relevant sections only
- **Modify**: Synthesize to grimoire, clear working memory

### Semantic Decay Stages

| Stage | Age | Format | Cost |
|-------|-----|--------|------|
| Active | 0-5 min | Full synthesis + snippets | ~200 tokens |
| Decayed | 5-30 min | Paths only | ~12 tokens/file |
| Archived | 30+ min | Single-line in trajectory | ~20 tokens |
</attention_budget>

---

## Phase 0.5: Codebase Probing (RLM Pattern)

Before loading any files, probe the codebase to determine optimal loading strategy.
This reduces token usage by avoiding eager loading of large, low-relevance files.

### 0.5.1 Run Codebase Probe

```bash
# Probe the target repository
PROBE_RESULT=$(.claude/scripts/context-manager.sh probe "$TARGET_REPO" --json 2>/dev/null)

if [[ -z "$PROBE_RESULT" ]] || ! echo "$PROBE_RESULT" | jq -e '.' >/dev/null 2>&1; then
  echo "⚠️ Probe unavailable - falling back to eager loading"
  LOADING_STRATEGY="eager"
  TOTAL_LINES=0
  TOTAL_FILES=0
  ESTIMATED_TOKENS=0
else
  TOTAL_LINES=$(echo "$PROBE_RESULT" | jq -r '.total_lines // 0')
  TOTAL_FILES=$(echo "$PROBE_RESULT" | jq -r '.total_files // 0')
  ESTIMATED_TOKENS=$(echo "$PROBE_RESULT" | jq -r '.estimated_tokens // 0')
  CODEBASE_SIZE=$(echo "$PROBE_RESULT" | jq -r '.codebase_size // "unknown"')

  echo "📊 Codebase Probe Results:"
  echo "   Files: $TOTAL_FILES"
  echo "   Lines: $TOTAL_LINES"
  echo "   Estimated tokens: $ESTIMATED_TOKENS"
  echo "   Size category: $CODEBASE_SIZE"
fi
```

### 0.5.2 Determine Loading Strategy

```bash
# Loading strategy based on codebase size (from .loa.config.yaml token_budget)
# Small (<10K lines): Load all files - fits comfortably in context
# Medium (10K-50K): Prioritized loading - load high-relevance first
# Large (>50K): Probe + excerpts only - too large for full loading

if [[ "$TOTAL_LINES" -lt 10000 ]]; then
  LOADING_STRATEGY="full"
  echo "📁 Strategy: FULL LOAD (small codebase)"
elif [[ "$TOTAL_LINES" -lt 50000 ]]; then
  LOADING_STRATEGY="prioritized"
  echo "📁 Strategy: PRIORITIZED LOAD (medium codebase)"
else
  LOADING_STRATEGY="excerpts"
  echo "📁 Strategy: EXCERPTS ONLY (large codebase)"
fi
```

### 0.5.3 Generate Loading Plan

Based on probe results, categorize files for Phase 2:

```bash
LOADING_PLAN_FILE="grimoires/loa/reality/loading-plan.md"
mkdir -p grimoires/loa/reality

cat > "$LOADING_PLAN_FILE" << EOF
# Loading Plan

Generated: $(date -u +%Y-%m-%dT%H:%M:%SZ)
Strategy: $LOADING_STRATEGY
Codebase: $TOTAL_FILES files, $TOTAL_LINES lines (~$ESTIMATED_TOKENS tokens)

## File Categories

EOF

if [[ "$LOADING_STRATEGY" == "full" ]]; then
  echo "All files will be loaded (small codebase)." >> "$LOADING_PLAN_FILE"
elif [[ "$LOADING_STRATEGY" == "prioritized" || "$LOADING_STRATEGY" == "excerpts" ]]; then
  # Categorize files by should-load decision with relevance-based prioritization
  # High relevance (7+): Load first
  # Medium relevance (4-6): Load if budget allows
  # Low relevance (0-3): Skip or excerpt

  echo "### Priority Loading Order (by relevance)" >> "$LOADING_PLAN_FILE"
  echo "" >> "$LOADING_PLAN_FILE"
  echo "Files are sorted by relevance score (highest first) within each category." >> "$LOADING_PLAN_FILE"
  echo "" >> "$LOADING_PLAN_FILE"

  # Temporary files for sorting
  LOAD_TMP=$(mktemp)
  EXCERPT_TMP=$(mktemp)
  SKIP_TMP=$(mktemp)

  # Get file list from probe result
  FILES=$(echo "$PROBE_RESULT" | jq -r '.files[]?.file // empty' 2>/dev/null)

  if [[ -n "$FILES" ]]; then
    while IFS= read -r file; do
      [[ -z "$file" ]] && continue
      DECISION_JSON=$(.claude/scripts/context-manager.sh should-load "$file" --json 2>/dev/null) || continue
      DECISION=$(echo "$DECISION_JSON" | jq -r '.decision // "skip"')
      RELEVANCE=$(echo "$DECISION_JSON" | jq -r '.relevance // 0')

      # Store as "score|file" for sorting
      case "$DECISION" in
        load)
          echo "$RELEVANCE|$file" >> "$LOAD_TMP"
          ;;
        excerpt)
          echo "$RELEVANCE|$file" >> "$EXCERPT_TMP"
          ;;
        *)
          echo "$RELEVANCE|$file" >> "$SKIP_TMP"
          ;;
      esac
    done <<< "$FILES"
  fi

  # Write sorted categories (highest relevance first)
  echo "### Will Load Fully (sorted by relevance)" >> "$LOADING_PLAN_FILE"
  echo "" >> "$LOADING_PLAN_FILE"
  if [[ -s "$LOAD_TMP" ]]; then
    sort -t'|' -k1 -rn "$LOAD_TMP" | while IFS='|' read -r score file; do
      echo "- $file (relevance: $score)" >> "$LOADING_PLAN_FILE"
    done
  else
    echo "_No files in this category_" >> "$LOADING_PLAN_FILE"
  fi

  echo "" >> "$LOADING_PLAN_FILE"
  echo "### Will Use Excerpts (sorted by relevance)" >> "$LOADING_PLAN_FILE"
  echo "" >> "$LOADING_PLAN_FILE"
  if [[ -s "$EXCERPT_TMP" ]]; then
    sort -t'|' -k1 -rn "$EXCERPT_TMP" | while IFS='|' read -r score file; do
      echo "- $file (relevance: $score)" >> "$LOADING_PLAN_FILE"
    done
  else
    echo "_No files in this category_" >> "$LOADING_PLAN_FILE"
  fi

  echo "" >> "$LOADING_PLAN_FILE"
  echo "### Will Skip (sorted by relevance)" >> "$LOADING_PLAN_FILE"
  echo "" >> "$LOADING_PLAN_FILE"
  if [[ -s "$SKIP_TMP" ]]; then
    sort -t'|' -k1 -rn "$SKIP_TMP" | while IFS='|' read -r score file; do
      echo "- $file (relevance: $score)" >> "$LOADING_PLAN_FILE"
    done
  else
    echo "_No files in this category_" >> "$LOADING_PLAN_FILE"
  fi

  # Cleanup temp files
  rm -f "$LOAD_TMP" "$EXCERPT_TMP" "$SKIP_TMP"
fi

echo ""
echo "✓ Loading plan generated: $LOADING_PLAN_FILE"
```

### 0.5.4 Log Probe to Trajectory

```bash
echo '{"timestamp":"'$(date -u +%Y-%m-%dT%H:%M:%SZ)'","agent":"riding-codebase","phase":"0.5","action":"codebase_probe","strategy":"'$LOADING_STRATEGY'","total_files":'$TOTAL_FILES',"total_lines":'$TOTAL_LINES',"estimated_tokens":'$ESTIMATED_TOKENS'}' >> "$TRAJECTORY_FILE"
```

---

## Phase 1: Interactive Context Discovery

### 1.1 Check for Existing Context

```bash
if [[ -d "grimoires/loa/context" ]] && [[ "$(ls -A grimoires/loa/context 2>/dev/null)" ]]; then
  echo "📚 Found existing context in grimoires/loa/context/"
  find grimoires/loa/context -type f \( -name "*.md" -o -name "*.txt" \) | while read f; do
    echo "  - $f ($(wc -l < "$f") lines)"
  done
  CONTEXT_EXISTS=true
else
  CONTEXT_EXISTS=false
fi
```

### 1.2 Context File Prompt

Inform the user about context files using `AskUserQuestion`:

```markdown
## 📚 Context Files

Before we begin the interview, you can add any existing documentation to:

    grimoires/loa/context/

Supported formats:
- Architecture docs, diagrams, decision records
- Stakeholder interviews, requirements docs
- Tribal knowledge, onboarding notes
- Roadmaps, sprint plans, tech debt lists
- Any .md, .txt, or .pdf files

**Why this matters**: I'll analyze these files first and skip questions
you've already answered. This saves time and focuses the interview on
gaps in my understanding.

Would you like to add context files now, or proceed with the interview?
```

### 1.3 Analyze Existing Context (Pre-Interview)

If context files exist, analyze them BEFORE the interview to generate `context-coverage.md`:

```markdown
# Context Coverage Analysis

> Pre-interview analysis of user-provided context

## Files Analyzed
| File | Type | Key Topics Covered |
|------|------|-------------------|
| architecture-notes.md | Architecture | Tech stack, module boundaries, data flow |
| tribal-knowledge.md | Tribal | Gotchas, unwritten rules |

## Topics Already Covered (will skip in interview)
- ✅ Tech stack (from architecture-notes.md)
- ✅ Known gotchas (from tribal-knowledge.md)

## Gaps to Explore in Interview
- ❓ Business priorities and critical features
- ❓ User types and permissions model
- ❓ Planned vs abandoned WIP code

## Claims Extracted (to verify against code)
| Claim | Source | Verification Strategy |
|-------|--------|----------------------|
| "Uses PostgreSQL with pgvector" | architecture-notes.md | Check DATABASE_URL, imports |
```

### 1.4 Interactive Discovery (Gap-Focused Interview)

Use `AskUserQuestion` tool for each topic, focusing on gaps. Skip questions already answered by context files.

**Interview Topics:**

1. **Architecture Understanding**
   - What is this project? (one sentence)
   - What's the primary tech stack?
   - How is the codebase organized?
   - What are the main entry points?

2. **Domain Knowledge**
   - What are the core domain entities?
   - What external services does this integrate with?
   - Are there feature flags or environment-specific behaviors?

3. **Tribal Knowledge (Critical)**
   - What's surprising or counterintuitive about this codebase?
   - What would break if someone didn't know the unwritten rules?
   - Are there areas that "just work" and shouldn't be touched?
   - What's the scariest part of the codebase?

4. **Work in Progress**
   - Is there intentionally incomplete code?
   - What's planned but not implemented yet?

5. **History**
   - How old is this codebase?
   - Has the architecture changed significantly over time?

### 1.5 Generate Claims to Verify (MANDATORY OUTPUT)

**YOU MUST CREATE THIS FILE** - `grimoires/loa/context/claims-to-verify.md`:

```bash
mkdir -p grimoires/loa/context
```

```markdown
# Claims to Verify Against Code

> Generated from context discovery interview on [DATE]
> These are HYPOTHESES, not facts. Code is truth.

## Architecture Claims

| Claim | Source | Verification Strategy |
|-------|--------|----------------------|
| "[Claim from interview]" | Interview | [How to verify] |

## Domain Claims

| Claim | Source | Verification Strategy |
|-------|--------|----------------------|
| "[Entity/feature claim]" | Interview | Grep for entity definitions |

## Tribal Knowledge (Handle Carefully)

| Claim | Source | Verification Strategy |
|-------|--------|----------------------|
| "[Gotcha or unwritten rule]" | Interview | Check for warnings in code |

## WIP Status

| Area | Status | Verification Strategy |
|------|--------|----------------------|
| "[Area mentioned as WIP]" | Unknown | Check for TODO/incomplete code |
```

**IMPORTANT**: Even if the interview is skipped or minimal, you MUST still create this file with whatever claims were gathered. If no interview occurred, note "No interview conducted - claims extracted from existing context files only."

Log to trajectory:
```json
{"timestamp": "...", "agent": "riding-codebase", "phase": 1, "action": "claims_generated", "output": "grimoires/loa/context/claims-to-verify.md", "claim_count": N}
```

### 1.6 Tool Result Clearing Checkpoint

After context discovery, clear raw interview data and summarize:

```markdown
## Context Discovery Summary (for active context)

Captured [N] claims to verify from user interview.
Full details written to: grimoires/loa/context/claims-to-verify.md

Key areas to investigate:
- [Top 3 architectural claims]
- [Top 3 tribal knowledge items]

Raw interview responses cleared from context.
```

---

## Phase 2: Code Reality Extraction

### 2.1 Setup

```bash
mkdir -p grimoires/loa/reality
cd "$TARGET_REPO"
```

### 2.1.5 Apply Loading Strategy (from Phase 0.5)

The loading strategy from Phase 0.5 controls file processing:

```bash
# Track token savings for reporting
TOKENS_SAVED=0
FILES_SKIPPED=0
FILES_EXCERPTED=0
FILES_LOADED=0

# Helper function: Check if file should be fully loaded
should_load_file() {
  local file="$1"

  # Always load in "full" strategy (small codebase)
  if [[ "$LOADING_STRATEGY" == "full" || "$LOADING_STRATEGY" == "eager" ]]; then
    return 0
  fi

  # Check loading plan or run should-load
  local decision
  decision=$(.claude/scripts/context-manager.sh should-load "$file" --json 2>/dev/null | jq -r '.decision // "load"')

  case "$decision" in
    load) return 0 ;;
    excerpt)
      ((FILES_EXCERPTED++))
      return 1
      ;;
    skip)
      local tokens
      tokens=$(.claude/scripts/context-manager.sh probe "$file" --json 2>/dev/null | jq -r '.estimated_tokens // 0')
      ((TOKENS_SAVED += tokens))
      ((FILES_SKIPPED++))
      return 2
      ;;
  esac
}

# Helper function: Get excerpt of file (high-relevance sections only)
get_file_excerpt() {
  local file="$1"
  local keywords=("export" "class" "interface" "function" "async" "api" "route" "handler")

  echo "# Excerpt: $file"
  echo ""

  # Extract lines containing keywords with 2 lines context
  for kw in "${keywords[@]}"; do
    grep -n -B1 -A2 "$kw" "$file" 2>/dev/null | head -20
  done | sort -t: -k1 -n -u | head -50
}

echo "📁 Loading strategy: $LOADING_STRATEGY"
```

### 2.2 Directory Structure Analysis

```bash
echo "## Directory Structure" > grimoires/loa/reality/structure.md
echo '```' >> grimoires/loa/reality/structure.md
find . -type d -maxdepth 4 \
  -not -path "*/node_modules/*" \
  -not -path "*/.git/*" \
  -not -path "*/dist/*" \
  -not -path "*/build/*" \
  -not -path "*/__pycache__/*" \
  2>/dev/null >> grimoires/loa/reality/structure.md
echo '```' >> grimoires/loa/reality/structure.md
```

### 2.3 Entry Points & Routes

```bash
.claude/scripts/search-orchestrator.sh hybrid \
  "@Get @Post @Put @Delete @Patch router app.get app.post app.put app.delete app.patch @route @api route handler endpoint" \
  "${TARGET_REPO}/src" 50 0.4 \
  > grimoires/loa/reality/api-routes.txt 2>/dev/null || \
grep -rn "@Get\|@Post\|@Put\|@Delete\|@Patch\|router\.\|app\.\(get\|post\|put\|delete\|patch\)\|@route\|@api" \
  --include="*.ts" --include="*.js" --include="*.py" --include="*.go" "${TARGET_REPO}" 2>/dev/null \
  > grimoires/loa/reality/api-routes.txt

ROUTE_COUNT=$(wc -l < grimoires/loa/reality/api-routes.txt 2>/dev/null || echo 0)
echo "Found $ROUTE_COUNT route definitions"
```

### 2.4 Data Models & Entities

```bash
.claude/scripts/search-orchestrator.sh hybrid \
  "model @Entity class Entity CREATE TABLE type struct interface schema definition" \
  "${TARGET_REPO}/src" 50 0.4 \
  > grimoires/loa/reality/data-models.txt 2>/dev/null || \
grep -rn "model \|@Entity\|class.*Entity\|CREATE TABLE\|type.*struct\|interface.*{\|type.*=" \
  --include="*.prisma" --include="*.ts" --include="*.sql" --include="*.go" --include="*.graphql" "${TARGET_REPO}" 2>/dev/null \
  > grimoires/loa/reality/data-models.txt
```

### 2.5 Environment Dependencies

```bash
.claude/scripts/search-orchestrator.sh regex \
  "process\\.env\\.[A-Z_]+|os\\.environ\\[|os\\.Getenv\\(|env\\.[A-Z_]+|import\\.meta\\.env\\." \
  "${TARGET_REPO}/src" 100 0.0 2>/dev/null | sort -u > grimoires/loa/reality/env-vars.txt || \
grep -roh 'process\.env\.\w\+\|os\.environ\[.\+\]\|os\.Getenv\(.\+\)\|env\.\w\+\|import\.meta\.env\.\w\+' \
  --include="*.ts" --include="*.js" --include="*.py" --include="*.go" "${TARGET_REPO}" 2>/dev/null \
  | sort -u > grimoires/loa/reality/env-vars.txt
```

### 2.6 Tech Debt Markers

```bash
.claude/scripts/search-orchestrator.sh regex \
  "TODO|FIXME|HACK|XXX|BUG|@deprecated|eslint-disable|@ts-ignore|type:\\s*any" \
  "${TARGET_REPO}/src" 100 0.0 \
  > grimoires/loa/reality/tech-debt.txt 2>/dev/null || \
grep -rn "TODO\|FIXME\|HACK\|XXX\|BUG\|@deprecated\|eslint-disable\|@ts-ignore\|type: any" \
  --include="*.ts" --include="*.js" --include="*.py" --include="*.go" "${TARGET_REPO}" 2>/dev/null \
  > grimoires/loa/reality/tech-debt.txt
```

### 2.7 Test Coverage Detection

```bash
find . -type f \( -name "*.test.ts" -o -name "*.spec.ts" -o -name "*_test.go" -o -name "test_*.py" \) \
  -not -path "*/node_modules/*" 2>/dev/null > grimoires/loa/reality/test-files.txt

TEST_COUNT=$(wc -l < grimoires/loa/reality/test-files.txt 2>/dev/null || echo 0)

if [[ "$TEST_COUNT" -eq 0 ]]; then
  echo "⚠️ NO TESTS FOUND - This is a significant gap"
fi
```

### 2.8 Tool Result Clearing Checkpoint (MANDATORY)

After all extractions complete, **clear raw tool outputs** from active context:

```markdown
## Phase 2 Extraction Summary (for active context)

Reality extraction complete. Results synthesized to grimoires/loa/reality/:
- Routes: [N] definitions → reality/api-routes.txt
- Entities: [N] models → reality/data-models.txt
- Env vars: [N] dependencies → reality/env-vars.txt
- Tech debt: [N] markers → reality/tech-debt.txt
- Tests: [N] files → reality/test-files.txt

### Loading Strategy Results (RLM Pattern)

| Metric | Value |
|--------|-------|
| Strategy | $LOADING_STRATEGY |
| Files loaded | $FILES_LOADED |
| Files excerpted | $FILES_EXCERPTED |
| Files skipped | $FILES_SKIPPED |
| Tokens saved | ~$TOKENS_SAVED |

⚠️ RAW TOOL OUTPUTS CLEARED FROM CONTEXT
Refer to reality/ files for specific file:line details.
```

---

## Phase 2b: Code Hygiene Audit

### Purpose

Flag potential issues for HUMAN DECISION - do not assume intent or prescribe fixes.

### 2b.1 Files Outside Standard Directories

Generate `grimoires/loa/reality/hygiene-report.md`:

```markdown
# Code Hygiene Audit

## Files Outside Standard Directories
| Location | Type | Question for Human |
|----------|------|-------------------|
| `script.js` (root) | Script | Move to `scripts/` or intentional? |

## Potential Temporary/WIP Folders
| Folder | Files | Question |
|--------|-------|----------|
| `.temp_wip/` | 15 files | WIP for future, or abandoned? |

## Commented-Out Import/Code Blocks
| Location | Question |
|----------|----------|
| src/handlers/badge.ts:45 | Remove or waiting on fix? |

## Potential Dependency Conflicts
⚠️ Both `ethers` and `viem` present - potential conflict or migration in progress?
```

### 2b.2 Dead Code Philosophy

```markdown
## ⚠️ Important: Dead Code Philosophy

Items flagged above are for **HUMAN DECISION**, not automatic fixing.

When you see potential dead code:
✅ Ask: "What's the status of this?"
❌ Don't assume: "This needs to be fixed and integrated"

Possible dispositions:
- **Keep (WIP)**: Intentionally incomplete, will be finished
- **Keep (Reference)**: Useful for copy-paste or learning
- **Archive**: Move to `_archive/` folder
- **Delete**: Confirmed abandoned

Add disposition decisions to `grimoires/loa/NOTES.md` Decision Log.
```

---

## Phase 3: Legacy Documentation Inventory

### 3.1 Find All Documentation

```bash
mkdir -p grimoires/loa/legacy

find . -type f \( -name "*.md" -o -name "*.rst" -o -name "*.txt" -o -name "*.adoc" \) \
  -not -path "*/node_modules/*" \
  -not -path "*/.git/*" \
  -not -path "*/grimoires/loa/*" \
  2>/dev/null > grimoires/loa/legacy/doc-files.txt
```

### 3.2 Assess AI Guidance Quality (CLAUDE.md)

```bash
if [[ -f "CLAUDE.md" ]]; then
  LINES=$(wc -l < CLAUDE.md)
  HAS_TECH_STACK=$(grep -ci "stack\|framework\|language\|database" CLAUDE.md || echo 0)
  HAS_PATTERNS=$(grep -ci "pattern\|convention\|style" CLAUDE.md || echo 0)
  HAS_WARNINGS=$(grep -ci "warning\|caution\|don't\|avoid" CLAUDE.md || echo 0)

  SCORE=0
  [[ $LINES -gt 50 ]] && ((SCORE+=2))
  [[ $HAS_TECH_STACK -gt 0 ]] && ((SCORE+=2))
  [[ $HAS_PATTERNS -gt 0 ]] && ((SCORE+=2))
  [[ $HAS_WARNINGS -gt 0 ]] && ((SCORE+=1))

  # Score out of 7 - below 5 is insufficient
fi
```

### 3.3 Create Inventory

Create `grimoires/loa/legacy/INVENTORY.md` listing all docs with type and key claims.

---

## Phase 4: Three-Way Drift Analysis (ENHANCED)

### 4.1 Drift Categories

| Category | Definition | Impact |
|----------|------------|--------|
| **Missing** | Code exists, no documentation | Shadow feature risk |
| **Stale** | Docs exist, code changed significantly | Misleading information |
| **Hallucinated** | Docs claim things code doesn't support | False promises |
| **Ghost** | Documented feature not in code at all | Phantom asset |
| **Shadow** | Exists in code, completely undocumented | Hidden liability |
| **Aligned** | Documentation accurately reflects code | Healthy state |

### 4.2 Legacy Documentation Claim Verification (MANDATORY)

**YOU MUST VERIFY** each claim found in legacy documentation against code:

```bash
# Extract claims from legacy docs
echo "Extracting claims from legacy documentation..."

for doc in $(cat grimoires/loa/legacy/doc-files.txt); do
  echo "## Claims from: $doc" >> grimoires/loa/legacy/extracted-claims.md

  # Extract feature/entity names mentioned
  grep -oE "[A-Z][a-zA-Z]+(?:Service|Manager|Handler|Controller|Module|Feature)" "$doc" 2>/dev/null | sort -u >> grimoires/loa/legacy/extracted-claims.md

  # Extract API endpoint claims
  grep -oE "(GET|POST|PUT|DELETE|PATCH)\s+/[a-zA-Z0-9/_-]+" "$doc" 2>/dev/null >> grimoires/loa/legacy/extracted-claims.md

  # Extract entity/model names
  grep -oE "model [A-Z][a-zA-Z]+|entity [A-Z][a-zA-Z]+|table [a-z_]+" "$doc" 2>/dev/null >> grimoires/loa/legacy/extracted-claims.md
done
```

### 4.3 Cross-Reference Claims Against Code

For EACH extracted claim, verify against code reality:

```markdown
## Claim Verification Process

For each claim in legacy docs:
1. Search for exact match in code
2. Search for similar/renamed versions
3. Check if behavior exists under different name
4. Determine claim status: VERIFIED | STALE | HALLUCINATED | MISSING
```

### 4.4 Generate Enhanced Drift Report

Create `grimoires/loa/drift-report.md`:

```markdown
# Three-Way Drift Report

> Generated: [timestamp]
> Target: [repo path]

## Truth Hierarchy Reminder

```
CODE wins every conflict. Always.
```

## Summary

| Category | Code Reality | Legacy Docs | User Context | Aligned |
|----------|--------------|-------------|--------------|---------|
| API Endpoints | X | Y | Z | W% |
| Data Models | X | Y | Z | W% |
| Features | X | Y | Z | W% |

## Drift Score: X% (lower is better)

## Drift Breakdown by Type

| Type | Count | Impact Level |
|------|-------|--------------|
| Missing (code exists, no docs) | N | Medium |
| Stale (docs outdated) | N | High |
| Hallucinated (docs claim non-existent) | N | Critical |
| Ghost (feature never existed) | N | Critical |
| Shadow (undocumented code) | N | Medium |

## Critical Drift Items

### 🔴 Hallucinated Documentation (CRITICAL)

**These claims in legacy docs are NOT supported by code:**

| Claim | Source Doc | Verification Attempt | Verdict |
|-------|------------|---------------------|---------|
| "OAuth2 authentication" | legacy/auth.md:L15 | `grep -r "oauth\|OAuth" --include="*.ts"` = 0 results | ❌ HALLUCINATED |
| "Batch rebate processing" | legacy/rebates.md:L23 | Code shows individual processing only | ❌ HALLUCINATED |
| "CubQuest badge tiers" | legacy/rebates.md:L45 | Badge logic differs from documentation | ❌ STALE (partially wrong) |

### 🟠 Stale Documentation (HIGH)

**These docs exist but code has changed:**

| Doc Claim | Source | Code Reality | Drift Type |
|-----------|--------|--------------|------------|
| "Uses Redis for caching" | legacy/arch.md:L30 | Now uses in-memory Map | STALE |
| "Rate limit: 100 req/min" | legacy/api.md:L12 | Rate limit is 60 req/min | STALE |

### 🟡 Missing Documentation (MEDIUM)

**Code features without documentation:**

| Feature | Location | Needs Docs |
|---------|----------|------------|
| RateLimiter middleware | src/middleware/rate.ts:45 | Yes - critical |
| BatchProcessor | src/services/batch.ts:1-200 | Yes - core business logic |

### Ghosts (Documented/Claimed but Missing in Code)
| Item | Claimed By | Evidence Searched | Verdict |
|------|------------|-------------------|---------|
| "Feature X" | legacy/api.md | `grep -r "FeatureX"` found nothing | ❌ GHOST |

### Shadows (In Code but Undocumented)
| Item | Location | Needs Documentation |
|------|----------|---------------------|
| RateLimiter | src/middleware/rate.ts:45 | Yes - critical infrastructure |

### Conflicts (Context + Docs disagree with Code)
| Claim | Sources | Code Reality | Confidence |
|-------|---------|--------------|------------|
| "Uses PostgreSQL" | context + legacy | MySQL in DATABASE_URL | HIGH |

## Verification Evidence

### Search Commands Executed

| Claim Searched | Command | Result |
|----------------|---------|--------|
| OAuth | `grep -ri "oauth" --include="*.ts" --include="*.js"` | 0 matches |
| BadgeTier | `grep -ri "badgetier\|badge.*tier" --include="*.sol"` | 3 matches (different implementation) |

## Recommendations

### Immediate Actions (Hallucinated/Stale)
1. **Remove** hallucinated claims from legacy docs
2. **Update** stale documentation OR deprecate entirely
3. **Flag** for product team: Features promised but not delivered

### Documentation Actions (Missing/Shadow)
1. Document critical middleware: RateLimiter
2. Add architecture docs for undocumented services
```

Log to trajectory:
```json
{"timestamp": "...", "agent": "riding-codebase", "phase": 4, "action": "drift_analysis", "details": {"drift_score": X, "missing": N, "stale": N, "hallucinated": N, "ghosts": N, "shadows": N}}
```

---

## Phase 5: Consistency Analysis (MANDATORY OUTPUT)

**YOU MUST CREATE THIS FILE** - `grimoires/loa/consistency-report.md`:

### 5.1 Analyze Naming Patterns

```bash
# Extract all exported names, class names, function names
.claude/scripts/search-orchestrator.sh regex \
  "export\\s+(const|function|class|interface|type)" \
  "${TARGET_REPO}/src" 100 0.0 2>/dev/null | head -100 || \
grep -rh "export \(const\|function\|class\|interface\|type\)" --include="*.ts" --include="*.js" "${TARGET_REPO}" 2>/dev/null | head -100

# For Solidity
.claude/scripts/search-orchestrator.sh regex \
  "contract |interface |struct |event |function " \
  "${TARGET_REPO}" 100 0.0 2>/dev/null | head -100 || \
grep -rh "contract \|interface \|struct \|event \|function " --include="*.sol" "${TARGET_REPO}" 2>/dev/null | head -100
```

### 5.2 Generate Consistency Report

```markdown
# Consistency Analysis

> Generated: [DATE]
> Target: [repo]

## Naming Patterns Detected

### Entity/Contract Naming
| Pattern | Count | Examples | Consistency |
|---------|-------|----------|-------------|
| `{Domain}{Type}` | N | `SFPosition`, `SFVaultStats` | Consistent |
| `{Type}` only | N | `Transfer`, `Mint` | Mixed |
| `I{Name}` interfaces | N | `IVault`, `IStrategy` | Consistent |

### Function Naming
| Pattern | Count | Examples |
|---------|-------|----------|
| `camelCase` | N | `getBalance`, `setOwner` |
| `snake_case` | N | `get_balance` |

### File Naming
| Pattern | Count | Examples |
|---------|-------|----------|
| `PascalCase.sol` | N | `SFVault.sol` |
| `kebab-case.ts` | N | `vault-manager.ts` |

## Consistency Score: X/10

**Scoring Criteria:**
- 10: Single consistent pattern throughout
- 7-9: Minor deviations, clear dominant pattern
- 4-6: Mixed patterns, no clear standard
- 1-3: Inconsistent, multiple competing patterns

## Pattern Conflicts Detected

| Conflict | Examples | Impact |
|----------|----------|--------|
| Mixed naming | `UserProfile` vs `user_data` | Cognitive overhead |

## Improvement Opportunities (Non-Breaking)
| Change | Type | Impact |
|--------|------|--------|
| [Specific suggestion] | Additive | [Impact description] |

## Breaking Changes (Flag Only - DO NOT IMPLEMENT)
| Change | Why Breaking | Impact |
|--------|--------------|--------|
| [Specific change] | [Reason] | [Downstream impact] |
```

**IMPORTANT**: You MUST create this file even if the codebase is small. If patterns are unclear, document that finding.

Log to trajectory:
```json
{"timestamp": "...", "agent": "riding-codebase", "phase": 5, "action": "consistency_analysis", "output": "grimoires/loa/consistency-report.md", "score": N}
```

---

## Phase 6: Loa Artifact Generation (WITH GROUNDING MARKERS)

**MANDATORY**: Every claim in PRD and SDD MUST use grounding markers.

### 6.0 Grounding Marker Reference

| Marker | When to Use | Example |
|--------|-------------|---------|
| `[GROUNDED]` | Direct code evidence | `[GROUNDED] Uses PostgreSQL (prisma/schema.prisma:L3)` |
| `[INFERRED]` | Logical deduction from multiple sources | `[INFERRED] Likely handles bulk operations based on batch naming` |
| `[ASSUMPTION]` | No direct evidence - needs validation | `[ASSUMPTION] OAuth was planned but descoped - verify with team` |

### 6.1 Generate PRD

Create `grimoires/loa/prd.md` with evidence-grounded content:

```markdown
# Product Requirements Document

> ⚠️ **Source of Truth Notice**
> Generated from code analysis on [date].
> All claims use grounding markers: [GROUNDED], [INFERRED], [ASSUMPTION]

## Document Metadata
| Field | Value |
|-------|-------|
| Generated | [timestamp] |
| Source | Code reality extraction |
| Drift Score | X% |
| Grounding | X% GROUNDED, Y% INFERRED, Z% ASSUMPTION |

## User Types
[From actual role/permission code with evidence]

### User Type: [Name]
- **[GROUNDED]** Role exists in `src/auth/roles.ts:23`
- **[GROUNDED]** Permissions: [list from code with citations]

## Features (Code-Verified)

### Feature: [Name]
- **[GROUNDED]** Status: Active in code (`src/features/x/index.ts:1-50`)
- **[GROUNDED]** Endpoints: [from api-routes.txt with file:line]
- **[INFERRED]** Purpose: [deduced from function names and structure]

### Feature: [Documented but Uncertain]
- **[ASSUMPTION]** This feature was mentioned in docs but implementation unclear
- **Requires validation by**: Engineering Lead
```

### 6.2 Generate SDD

Create `grimoires/loa/sdd.md` with architecture evidence:

```markdown
# System Design Document

> ⚠️ **Source of Truth Notice**
> Generated from code analysis on [date].
> All claims use grounding markers: [GROUNDED], [INFERRED], [ASSUMPTION]

## Architecture (As-Built)

### Tech Stack (Verified)
| Component | Technology | Grounding | Evidence |
|-----------|------------|-----------|----------|
| Runtime | Node.js | [GROUNDED] | `package.json:engines` |
| Database | PostgreSQL | [GROUNDED] | `DATABASE_URL` pattern in `.env.example:L5` |
| Cache | Redis | [INFERRED] | Redis imports found, config unclear |

### Module Structure
[From directory analysis with actual paths]
- **[GROUNDED]** `src/api/` - API handlers (47 files)
- **[GROUNDED]** `src/services/` - Business logic (23 files)
- **[INFERRED]** `src/utils/` - Shared utilities (likely internal)

### Data Model
[From data-models.txt with schema quotes]

#### Entity: [Name]
- **[GROUNDED]** Schema definition: `prisma/schema.prisma:L45-60`
- **[GROUNDED]** Fields: [list with evidence]
- **[ASSUMPTION]** Relationship to [OtherEntity] - schema suggests but unclear

### API Surface
| Method | Endpoint | Handler | Grounding |
|--------|----------|---------|-----------|
| GET | /api/users | UserController.list | [GROUNDED] `src/controllers/user.ts:L23` |
| POST | /api/auth | AuthController.login | [GROUNDED] `src/controllers/auth.ts:L45` |
```

### 6.3 Grounding Summary Block

At the end of BOTH PRD and SDD, include:

```markdown
---

## Grounding Summary

| Category | Count | Percentage |
|----------|-------|------------|
| [GROUNDED] (direct evidence) | N | X% |
| [INFERRED] (logical deduction) | N | Y% |
| [ASSUMPTION] (needs validation) | N | Z% |
| **Total Claims** | N | 100% |

### Assumptions Requiring Validation

| # | Claim | Location | Validator Needed |
|---|-------|----------|------------------|
| 1 | [Assumption text] | prd.md:L[N] | [Role] |
| 2 | [Assumption text] | sdd.md:L[N] | [Role] |

> **Quality Target**: >80% GROUNDED, <10% ASSUMPTION
```

Log to trajectory:
```json
{"timestamp": "...", "agent": "riding-codebase", "phase": 6, "action": "artifact_generation", "details": {"prd_claims": N, "sdd_claims": N, "grounded_pct": X, "inferred_pct": Y, "assumption_pct": Z}}
```

---

## Phase 6.5: Reality File Generation (Token-Optimized Codebase Interface)

**Purpose**: Generate token-optimized reality files for the `/reality` command, enabling efficient cross-repo agent integration without dumping entire codebases into context windows.

### 6.5.0 Reality Directory Setup

```bash
mkdir -p grimoires/loa/reality
REALITY_DIR="grimoires/loa/reality"
TIMESTAMP=$(date -u +%Y-%m-%dT%H:%M:%SZ)
COMMIT_HASH=$(git rev-parse --short HEAD 2>/dev/null || echo "unknown")
```

### 6.5.1 Generate index.md (Hub File)

The index.md is the routing hub - MUST be < 500 tokens.

```markdown
# Reality Index

> Generated by /ride on [TIMESTAMP]
> Source commit: [COMMIT_HASH]

## Codebase Overview

| Property | Value |
|----------|-------|
| Language | [Primary language from package.json/go.mod/etc] |
| Framework | [Main framework if detected] |
| Entry Point | [Main entry file path] |
| Total Files | [Count from Phase 2] |
| Lines of Code | [Approximate from probe] |

## Navigation

| I want to... | Read | Tokens |
|--------------|------|--------|
| See public API functions | [api-surface.md](api-surface.md) | ~[N] |
| Understand data types | [types.md](types.md) | ~[N] |
| Learn integration patterns | [interfaces.md](interfaces.md) | ~[N] |
| Find entry points | [entry-points.md](entry-points.md) | ~[N] |
| See directory structure | [structure.md](structure.md) | ~[N] |

## Quick Reference

**Main entry**: `[path]:1`
**API routes**: `[routes file path]`
**Auth handler**: `[auth file if exists]`
```

### 6.5.2 Generate api-surface.md (Public Functions)

Extract public function signatures - target < 2000 tokens.

```bash
# Extract exported functions and their signatures
echo "# API Surface" > "$REALITY_DIR/api-surface.md"
echo "" >> "$REALITY_DIR/api-surface.md"
echo "> Generated by /ride on $TIMESTAMP" >> "$REALITY_DIR/api-surface.md"
echo "" >> "$REALITY_DIR/api-surface.md"
```

For each major service/module:

```markdown
## Public Functions

### [ServiceName] (`[file path]`)

| Function | Signature | Line |
|----------|-----------|------|
| [name] | `[params] => [return type]` | [line number] |
```

Also extract API endpoints:

```markdown
## API Endpoints

| Method | Route | Handler | Line |
|--------|-------|---------|------|
| POST | /api/v1/users | UserController.create | [file:line] |
```

### 6.5.3 Generate types.md (Type Definitions)

Extract type/interface definitions - target < 2000 tokens.

```markdown
# Type Definitions

> Generated by /ride on [TIMESTAMP]

## Core Types

### [TypeName] (`[file path]:[line]`)

\`\`\`typescript
[Type definition code]
\`\`\`
```

Group by domain (User types, Payment types, etc.) for better organization.

### 6.5.4 Generate interfaces.md (Integration Patterns)

Document how external systems connect - target < 1000 tokens.

```markdown
# Integration Interfaces

> Generated by /ride on [TIMESTAMP]

## External Integrations

### [Integration Name]

**Location**: `[file path]:[line]`

\`\`\`typescript
[Interface code]
\`\`\`

**Required env vars**: `[VAR1]`, `[VAR2]`

## Webhooks

### [Webhook Name] (`[file path]:[line]`)

**Endpoint**: [METHOD] [path]
**Payload**:
\`\`\`typescript
[Payload type definition]
\`\`\`
```

### 6.5.5 Generate structure.md (Directory Tree)

Already exists from Phase 2, but enhance with annotations - target < 1000 tokens.

```markdown
# Codebase Structure

> Generated by /ride on [TIMESTAMP]

## Directory Tree

\`\`\`
src/
├── index.ts              # Application entry point
├── config/
│   ├── database.ts       # Database configuration
│   └── env.ts            # Environment validation
├── routes/
│   └── ...               # HTTP routing
├── services/
│   └── ...               # Business logic
└── types/
    └── ...               # Type definitions
\`\`\`

## Module Responsibilities

| Module | Purpose | Dependencies |
|--------|---------|--------------|
| routes/ | HTTP routing | services/, middleware/ |
| services/ | Business logic | types/, utils/ |
```

### 6.5.6 Generate entry-points.md (Starting Points)

Document main files, CLI commands, routes - target < 500 tokens.

```markdown
# Entry Points

> Generated by /ride on [TIMESTAMP]

## Application Entry

| Type | File | Line | Command |
|------|------|------|---------|
| Main | [main file] | 1 | `npm start` / `go run` |
| Dev | [same or different] | 1 | `npm run dev` |
| Test | [test setup] | 1 | `npm test` |

## API Routes

| Route Prefix | File | Description |
|--------------|------|-------------|
| /api/v1/users | [file] | User management |

## CLI Commands

| Command | File | Description |
|---------|------|-------------|
| [command] | [file] | [purpose] |

## Environment Requirements

| Variable | Required | Default |
|----------|----------|---------|
| [VAR] | Yes/No | [value or -] |
```

### 6.5.7 Generate .reality-meta.json (Metadata)

```bash
# Count tokens (using word count as proxy)
INDEX_TOKENS=$(wc -w < "$REALITY_DIR/index.md" 2>/dev/null || echo 0)
API_TOKENS=$(wc -w < "$REALITY_DIR/api-surface.md" 2>/dev/null || echo 0)
TYPES_TOKENS=$(wc -w < "$REALITY_DIR/types.md" 2>/dev/null || echo 0)
INTERFACES_TOKENS=$(wc -w < "$REALITY_DIR/interfaces.md" 2>/dev/null || echo 0)
STRUCTURE_TOKENS=$(wc -w < "$REALITY_DIR/structure.md" 2>/dev/null || echo 0)
ENTRY_TOKENS=$(wc -w < "$REALITY_DIR/entry-points.md" 2>/dev/null || echo 0)
TOTAL_TOKENS=$((INDEX_TOKENS + API_TOKENS + TYPES_TOKENS + INTERFACES_TOKENS + STRUCTURE_TOKENS + ENTRY_TOKENS))

cat > "$REALITY_DIR/.reality-meta.json" << EOF
{
  "generated_at": "$TIMESTAMP",
  "source_commit": "$COMMIT_HASH",
  "generator_version": "1.0.0",
  "token_counts": {
    "index": $INDEX_TOKENS,
    "api-surface": $API_TOKENS,
    "types": $TYPES_TOKENS,
    "interfaces": $INTERFACES_TOKENS,
    "structure": $STRUCTURE_TOKENS,
    "entry-points": $ENTRY_TOKENS,
    "total": $TOTAL_TOKENS
  },
  "staleness_threshold_days": 7
}
EOF
```

### 6.5.8 Token Budget Verification

```bash
# Verify token budgets
if [[ $INDEX_TOKENS -gt 500 ]]; then
  echo "⚠️ WARNING: index.md exceeds 500 token budget ($INDEX_TOKENS tokens)"
fi
if [[ $TOTAL_TOKENS -gt 7000 ]]; then
  echo "⚠️ WARNING: Total reality files exceed 7000 token budget ($TOTAL_TOKENS tokens)"
fi

echo "✓ Reality files generated in $REALITY_DIR"
echo "  Total tokens: $TOTAL_TOKENS (budget: 7000)"
```

### 6.5.9 Log to Trajectory

```json
{"timestamp": "...", "agent": "riding-codebase", "phase": "6.5", "action": "reality_generation", "details": {"files": 6, "total_tokens": N, "within_budget": true}}
```

---

## Phase 7: Governance Audit

Generate `grimoires/loa/governance-report.md`:

```markdown
# Governance & Release Audit

| Artifact | Status | Impact |
|----------|--------|--------|
| CHANGELOG.md | ❌ Missing | No version history |
| CONTRIBUTING.md | ❌ Missing | Unclear contribution process |
| SECURITY.md | ❌ Missing | No security disclosure policy |
| CODEOWNERS | ❌ Missing | No required reviewers |
| Semver tags | ❌ None | No release versioning |
```

---

## Phase 8: Legacy Deprecation

For each file in legacy/doc-files.txt, prepend deprecation notice:

```html
<!--
╔════════════════════════════════════════════════════════════════════╗
║  ⚠️  DEPRECATED - DO NOT UPDATE                                    ║
╠════════════════════════════════════════════════════════════════════╣
║  This document has been superseded by Loa-managed documentation.   ║
║                                                                    ║
║  Source of Truth:                                                  ║
║  • Product Requirements: grimoires/loa/prd.md                       ║
║  • System Design: grimoires/loa/sdd.md                              ║
║                                                                    ║
║  Drift Report: grimoires/loa/drift-report.md                        ║
╚════════════════════════════════════════════════════════════════════╝
-->
```

---

## Phase 9: Trajectory Self-Audit (MANDATORY OUTPUT)

**YOU MUST CREATE THIS FILE** - `grimoires/loa/trajectory-audit.md`:

### 9.1 Review Generated Artifacts

Before creating the audit, review all generated artifacts for grounding:

```bash
# Count grounding markers in PRD
grep -c "(.*:L[0-9]" grimoires/loa/prd.md 2>/dev/null || echo 0
grep -c "\[ASSUMPTION\]" grimoires/loa/prd.md 2>/dev/null || echo 0
grep -c "\[INFERRED\]" grimoires/loa/prd.md 2>/dev/null || echo 0

# Count grounding markers in SDD
grep -c "(.*:L[0-9]" grimoires/loa/sdd.md 2>/dev/null || echo 0
```

### 9.2 Generate Trajectory Audit

```markdown
# Trajectory Self-Audit

> Generated: [DATE]
> Agent: riding-codebase
> Target: [repo]

## Execution Summary

| Phase | Status | Output File | Key Findings |
|-------|--------|-------------|--------------|
| 0 - Preflight | Complete | - | Loa v[X] mounted |
| 1 - Context Discovery | Complete | claims-to-verify.md | [N] claims captured |
| 2 - Code Extraction | Complete | reality/*.txt | [N] routes, [N] entities |
| 2b - Hygiene Audit | Complete | reality/hygiene-report.md | [N] items flagged |
| 3 - Legacy Inventory | Complete | legacy/INVENTORY.md | [N] docs found |
| 4 - Drift Analysis | Complete | drift-report.md | [X]% drift |
| 5 - Consistency | Complete | consistency-report.md | Score: [N]/10 |
| 6 - PRD/SDD Generation | Complete | prd.md, sdd.md | Evidence-grounded |
| 7 - Governance Audit | Complete | governance-report.md | [N] gaps |
| 8 - Legacy Deprecation | Complete | [N] files marked | - |
| 9 - Self-Audit | Complete | trajectory-audit.md | This file |

## Grounding Analysis

### PRD Grounding
| Metric | Count | Percentage |
|--------|-------|------------|
| **[GROUNDED]** claims (file:line citations) | N | X% |
| **[INFERRED]** claims (logical deduction) | N | X% |
| **[ASSUMPTION]** claims (needs validation) | N | X% |
| Total claims | N | 100% |

### SDD Grounding
| Metric | Count | Percentage |
|--------|-------|------------|
| **[GROUNDED]** claims (file:line citations) | N | X% |
| **[INFERRED]** claims (logical deduction) | N | X% |
| **[ASSUMPTION]** claims (needs validation) | N | X% |
| Total claims | N | 100% |

## Claims Requiring Validation

| # | Claim | Location | Type | Validator Needed |
|---|-------|----------|------|------------------|
| 1 | [Claim text] | prd.md:L[N] | ASSUMPTION | [Role] |
| 2 | [Claim text] | sdd.md:L[N] | INFERRED | [Role] |

## Potential Hallucination Check

Review these areas for accuracy:
- [ ] Entity names match actual code (grep verified)
- [ ] Feature descriptions match implementations
- [ ] API endpoints exist as documented
- [ ] Dependencies listed are actually imported

## Reasoning Quality Score: X/10

**Scoring Criteria:**
- 10: 100% grounded, zero assumptions
- 8-9: >90% grounded, assumptions flagged
- 6-7: >75% grounded, some gaps
- 4-5: >50% grounded, significant gaps
- 1-3: <50% grounded, needs re-ride

## Trajectory Log Reference

Full trajectory logged to: `grimoires/loa/a2a/trajectory/riding-[DATE].jsonl`

## Self-Certification

- [ ] All phases completed and outputs generated
- [ ] All claims in PRD/SDD have grounding markers
- [ ] Assumptions explicitly flagged with [ASSUMPTION]
- [ ] Drift report reflects actual code state
- [ ] No hallucinated features or entities
```

**IMPORTANT**: You MUST create this file as the final phase. It serves as a quality gate for the entire /ride workflow.

Log to trajectory:
```json
{"timestamp": "...", "agent": "riding-codebase", "phase": 9, "action": "self_audit", "output": "grimoires/loa/trajectory-audit.md", "quality_score": N}
```

### Grounding Categories

| Category | Marker | Requirement |
|----------|--------|-------------|
| **Grounded** | `(file.ts:L45)` | Direct code citation |
| **Inferred** | `[INFERRED: ...]` | Logical deduction from multiple sources |
| **Assumption** | `[ASSUMPTION: ...]` | No direct evidence - requires validation |

---

## Phase 10: Maintenance Handoff

### 10.1 Update NOTES.md

```markdown
## Session Continuity
| Timestamp | Agent | Summary |
|-----------|-------|---------|
| [now] | riding-codebase | Completed /ride workflow |

## Ride Results
- Routes documented: X
- Entities documented: Y
- Tech debt imported: Z
- Drift score: W%
- Governance gaps: N items
```

### 10.2 Completion Summary

```markdown
╔═════════════════════════════════════════════════════════════════╗
║  ✓ The Loa Has Ridden                                           ║
╚═════════════════════════════════════════════════════════════════╝

### Grimoire Artifacts Created
- grimoires/loa/prd.md (Product truth)
- grimoires/loa/sdd.md (System truth)
- grimoires/loa/drift-report.md (Three-way analysis)
- grimoires/loa/consistency-report.md (Pattern analysis)
- grimoires/loa/governance-report.md (Process gaps)
- grimoires/loa/reality/* (Raw extractions)

### Next Steps
1. Review drift-report.md for critical issues
2. Address governance gaps
3. Schedule stakeholder PRD review
4. Run `/implement` for high-priority drift

The code truth has been channeled. The grimoire reflects reality.
```

---

## Uncertainty Protocol

If code behavior is ambiguous:

1. State: "I'm uncertain about [specific aspect]"
2. Quote the ambiguous code with `file:line`
3. List possible interpretations
4. Ask for clarification via `AskUserQuestion`
5. Log uncertainty in `NOTES.md`

**Never assume. Always ground in evidence.**

---

## Trajectory Logging (MANDATORY)

**YOU MUST LOG EACH PHASE** to `grimoires/loa/a2a/trajectory/riding-{date}.jsonl`:

### Setup Trajectory File

```bash
TRAJECTORY_DATE=$(date +%Y%m%d)
TRAJECTORY_FILE="grimoires/loa/a2a/trajectory/riding-${TRAJECTORY_DATE}.jsonl"
mkdir -p grimoires/loa/a2a/trajectory
```

### Log Format

Each phase MUST append a JSON line:

```json
{"timestamp": "2024-01-15T10:30:00Z", "agent": "riding-codebase", "phase": 0, "action": "preflight", "status": "complete", "details": {"loa_version": "0.7.0"}}
{"timestamp": "2024-01-15T10:31:00Z", "agent": "riding-codebase", "phase": 1, "action": "context_discovery", "status": "complete", "details": {"claims_count": 12, "output": "claims-to-verify.md"}}
{"timestamp": "2024-01-15T10:35:00Z", "agent": "riding-codebase", "phase": 2, "action": "code_extraction", "status": "complete", "details": {"routes": 47, "entities": 60, "env_vars": 15}}
{"timestamp": "2024-01-15T10:36:00Z", "agent": "riding-codebase", "phase": "2b", "action": "hygiene_audit", "status": "complete", "details": {"items_flagged": 8}}
{"timestamp": "2024-01-15T10:40:00Z", "agent": "riding-codebase", "phase": 3, "action": "legacy_inventory", "status": "complete", "details": {"docs_found": 5}}
{"timestamp": "2024-01-15T10:45:00Z", "agent": "riding-codebase", "phase": 4, "action": "drift_analysis", "status": "complete", "details": {"drift_score": 34, "ghosts": 3, "shadows": 5, "stale": 2}}
{"timestamp": "2024-01-15T10:50:00Z", "agent": "riding-codebase", "phase": 5, "action": "consistency_analysis", "status": "complete", "details": {"score": 7, "output": "consistency-report.md"}}
{"timestamp": "2024-01-15T10:55:00Z", "agent": "riding-codebase", "phase": 6, "action": "artifact_generation", "status": "complete", "details": {"prd_claims": 25, "sdd_claims": 30, "grounded_pct": 85}}
{"timestamp": "2024-01-15T11:00:00Z", "agent": "riding-codebase", "phase": 7, "action": "governance_audit", "status": "complete", "details": {"gaps": 4}}
{"timestamp": "2024-01-15T11:05:00Z", "agent": "riding-codebase", "phase": 8, "action": "legacy_deprecation", "status": "complete", "details": {"files_marked": 3}}
{"timestamp": "2024-01-15T11:10:00Z", "agent": "riding-codebase", "phase": 9, "action": "self_audit", "status": "complete", "details": {"quality_score": 8, "assumptions": 3, "output": "trajectory-audit.md"}}
{"timestamp": "2024-01-15T11:15:00Z", "agent": "riding-codebase", "phase": 10, "action": "handoff", "status": "complete", "details": {"total_duration_minutes": 45}}
```

### Logging Implementation

After EACH phase completes, append to the trajectory file:

```bash
echo '{"timestamp":"'$(date -u +%Y-%m-%dT%H:%M:%SZ)'","agent":"riding-codebase","phase":'$PHASE',"action":"'$ACTION'","status":"complete","details":'$DETAILS'}' >> "$TRAJECTORY_FILE"
```

### Why This Matters

1. **Audit Trail**: Proves what the agent actually did
2. **Debugging**: Identify where issues occurred
3. **Quality Gate**: Phase 9 uses this to verify all phases ran
4. **Reproducibility**: Can re-run specific phases if needed

**IMPORTANT**: If the trajectory file is empty at Phase 9, the self-audit MUST flag this as a failure.
