---
name: smart-doc-manager
description: Universal documentation consolidation skill that verifies system reality before making ANY organizational decisions. Analyzes codebase, detects redundancies, and safely consolidates documentation with preservation of git history and rollback capabilities. Includes specialized MASTER_PLAN.md management with intelligent updates, backup, validation, task creation (/task), and idea/issue processing. Triggers on "master-plan", "plan update", "documentation", "consolidate docs", "audit docs", "add task", "new task", "process ideas", "check inbox".
---

# Smart Documentation Manager (SDM)

**Universal documentation consolidation skill that verifies system reality before making ANY organizational decisions.**

## Skill Boundary (IMPORTANT)

| This Skill Manages | NOT This Skill (Use Instead) |
|-------------------|------------------------------|
| `docs/` directory | `.claude/skills/` → Use `Skill(skill-creator-doctor)` |
| `MASTER_PLAN.md` | Skill frontmatter/description → Use `Skill(skill-creator-doctor)` |
| SOPs in `docs/sop/` | Skill telemetry/stats → See `skills.json` |
| README files in docs/ | Skills consolidation → Use `Skill(skill-creator-doctor)` |
| Architecture docs | - |

**Clear division**: This skill manages `docs/` and project documentation. For anything in `.claude/skills/`, use `skill-creator-doctor` instead.

---

## Core Safety Principle

**NEVER ASSUME - ALWAYS VERIFY**

This skill MUST analyze actual codebase, dependencies, and implementation to understand current technology before evaluating documentation. No deletions, merges, or reorganization without explicit verification against running code.

---

## When to Use This Skill

Use this skill when you need to:

- **Audit documentation accuracy** - Verify docs match actual code implementation
- **Consolidate duplicate content** - Merge redundant documentation safely
- **Reorganize documentation structure** - Create logical organization with validation
- **Archive obsolete documentation** - Safely remove outdated docs with rollback
- **Find undocumented features** - Identify code that lacks documentation
- **Add tasks to MASTER_PLAN.md** - Create new tasks with auto-generated IDs (see `references/add-task-workflow.md`)
- **Process ideas inbox** - Transform bullet points into prioritized items (see `references/idea-processing-workflow.md`)
- **Clean up documentation mess** - Transform scattered docs into organized structure

**Critical:** This skill prioritizes safety over automation. It will never delete or move files without verification and user confirmation.

---

## Parallel Subagent Architecture (MANDATORY)

**This skill MUST use parallel subagents for efficient analysis.** Never run sequential searches when parallel execution is possible.

### When to Spawn Subagents

| Task Type | Subagent Strategy |
|-----------|-------------------|
| **Tech stack detection** | Spawn 3-4 Explore agents in parallel (dependencies, imports, configs) |
| **Doc vs Code verification** | Spawn 1 agent per technology/feature being verified |
| **Duplicate detection** | Spawn 1 agent per docs subdirectory |
| **Link validation** | Spawn 1 agent for internal links, 1 for external links |
| **Coverage gap analysis** | Spawn agents per codebase area (src/, api/, components/) |

### Subagent Spawning Pattern

**ALWAYS use this pattern for parallel analysis:**

```
// Example: Verifying documentation for 3 technologies
Task(subagent_type="Explore", prompt="Search for Tauri usage: check src-tauri/, package.json for @tauri-apps, and any invoke() calls in src/")
Task(subagent_type="Explore", prompt="Search for Supabase usage: check imports of @supabase/supabase-js, connection configs, and RLS policies")
Task(subagent_type="Explore", prompt="Search for Vue Flow usage: check imports of @vue-flow/core, canvas components, and node/edge definitions")
// All 3 run IN PARALLEL in a single message
```

### Subagent Types for SDM

| Agent Type | Use For |
|------------|---------|
| `Explore` | Code searches, dependency checks, import analysis |
| `general-purpose` | Complex multi-step verification requiring reasoning |
| `Bash` | Git history checks, file operations |

### Critical Rules

1. **NEVER run searches sequentially** - Always batch into parallel Task calls
2. **One specific task per agent** - Each agent gets ONE clear question to answer
3. **Combine results after** - Wait for all agents, then synthesize findings
4. **Max 5 agents per batch** - Don't overwhelm; batch in groups of 5

### Example: Full Documentation Audit with Subagents

```
Step 1: Spawn 4 parallel Explore agents
  - Agent 1: "List all technologies in package.json dependencies"
  - Agent 2: "Find all .md files in docs/ and list their topics"
  - Agent 3: "Search for database-related code (supabase, postgres, sql)"
  - Agent 4: "Search for auth-related code (jwt, token, session, login)"

Step 2: Wait for results, then spawn verification agents
  - Agent 5: "Verify docs/database.md accuracy against actual Supabase code"
  - Agent 6: "Verify docs/auth.md accuracy against actual auth implementation"
  - Agent 7: "Check for undocumented features in src/composables/"

Step 3: Synthesize all findings into single report
```

---

## Phase 1: System Reality Verification (MANDATORY FIRST STEP)

### 1.1 Technology Stack Detection

**Objective:** Build accurate map of ACTUAL technologies in use.

**Process:**

#### Step 1: Identify dependency files
```bash
find . -name "package.json" -o -name "requirements.txt" -o -name "Cargo.toml" \
  -o -name "go.mod" -o -name "pom.xml" -o -name "composer.json" \
  -o -name "Gemfile" -o -name "build.gradle"
```

#### Step 2: Parse each dependency file
```bash
# For package.json:
cat package.json | jq -r '.dependencies, .devDependencies | keys[]'

# For requirements.txt:
grep -v "^#" requirements.txt | cut -d'=' -f1 | cut -d'>' -f1 | cut -d'<' -f1

# For Cargo.toml:
grep "^[a-zA-Z]" Cargo.toml | cut -d'=' -f1 | tr -d ' '
```

**Output Format:**
```json
{
  "detected_stack": {
    "languages": ["TypeScript", "Python", "Rust"],
    "frameworks": ["React", "FastAPI", "Actix"],
    "databases": ["PostgreSQL", "Redis"],
    "storage": ["S3", "LocalFileSystem"],
    "deployment": ["Docker", "Kubernetes"],
    "testing": ["Jest", "Pytest"]
  },
  "confidence": {
    "PostgreSQL": 100,
    "PouchDB": 15
  },
  "detection_method": {
    "PostgreSQL": "Found in package.json + psycopg2 in requirements.txt + import statements in 12 files",
    "Redis": "Found in docker-compose.yml + redis-py in requirements.txt + 5 cache.py files"
  }
}
```

### 1.2 Implementation Reality Check

**Objective:** Verify what's ACTUALLY implemented vs what's documented.

**Safety Rules:**
1. ✅ ONLY confirm technology exists if found in BOTH dependencies AND code
2. ✅ Mark as "uncertain" if found in docs but not in code
3. ✅ Flag as "documentation-only" if no code evidence exists
4. ❌ NEVER assume documentation is correct without code verification

**Verification Commands:**

```bash
# Database verification example
echo "Checking PostgreSQL claims..."
rg "import.*psycopg2|from.*psycopg2|import.*pg|Pool.*postgresql" --type py
rg "import.*pg|from.*pg|Pool" --type ts
grep -r "postgresql://" config/ .env.example

# API framework verification
rg "@app.route|@router.get|@router.post" --type py  # FastAPI/Flask
rg "app.get\(|app.post\(|router.get\(" --type ts   # Express
rg "#\[get\(|#\[post\(" --type rust                # Actix

# Storage verification
rg "S3Client|boto3|aws-sdk" --type-all
rg "PouchDB|new PouchDB|pouchdb" --type-all
rg "fs.writeFile|fs.readFile" --type-all
```

**Output Format:**
```json
{
  "verified_features": {
    "user_authentication": {
      "status": "ACTIVE",
      "evidence": [
        "src/auth/login.ts:15 - JWT token generation",
        "src/middleware/auth.ts:8 - Token verification",
        "package.json:23 - jsonwebtoken@9.0.0"
      ],
      "last_modified": "2025-11-15",
      "documentation": ["docs/auth.md", "docs/api/authentication.md"]
    },
    "pouchdb_sync": {
      "status": "DOCUMENTATION_ONLY",
      "evidence": [],
      "code_search_results": 0,
      "documentation": ["docs/offline-sync.md"],
      "warning": "⚠️ Documented but NO code implementation found"
    }
  }
}
```

### 1.3 Active vs Obsolete Detection

**Objective:** Distinguish between current features and legacy documentation.

**Decision Matrix:**

| Code Exists | Docs Exist | Classification | Action |
|-------------|------------|----------------|--------|
| ✅ Yes | ✅ Yes | ACTIVE | Verify accuracy |
| ✅ Yes | ❌ No | UNDOCUMENTED | Create docs |
| ❌ No | ✅ Yes | OBSOLETE (maybe) | **VERIFY BEFORE DELETION** |
| ❌ No | ❌ No | N/A | No action |

**Safety Protocol for "Maybe Obsolete":**

BEFORE marking as obsolete:
1. Check git history: Was feature recently removed?
   ```bash
   git log --all --oneline --grep="remove.*pouchdb"
   ```

2. Check branches: Does feature exist in other branches?
   ```bash
   git branch -r --contains <feature-commit>
   ```

3. Check issues/PRs: Is feature planned but not implemented?
   ```bash
   gh issue list --search "pouchdb"
   ```

4. ASK USER: "Found docs for PouchDB but no code. Should I:
   a) Archive (feature was removed)
   b) Keep (feature is planned)
   c) Investigate further"

5. NEVER auto-delete without explicit user confirmation

---

## Phase 2: Comprehensive Document Analysis

### 2.1 Content Inventory & Classification

**For EVERY documentation file, generate:**
```json
{
  "file": "docs/authentication.md",
  "metadata": {
    "word_count": 1247,
    "last_modified": "2025-10-12T14:23:00Z",
    "last_author": "Alice Developer",
    "size_kb": 8.4
  },
  "content_analysis": {
    "main_topics": ["JWT", "OAuth2", "Session Management"],
    "code_examples": 5,
    "code_examples_verified": 4,
    "code_examples_broken": 1,
    "external_links": 3,
    "external_links_alive": 2,
    "external_links_dead": 1,
    "cross_references": ["docs/api/login.md", "docs/security.md"]
  },
  "technical_accuracy": {
    "score": 85,
    "verification": {
      "mentions_jwt": true,
      "jwt_in_code": true,
      "mentions_oauth2": true,
      "oauth2_in_code": false,
      "mentions_sessions": true,
      "sessions_in_code": true
    },
    "discrepancies": [
      "Documents OAuth2 integration but no oauth2 imports found in codebase"
    ]
  },
  "classification": "MOSTLY_ACCURATE",
  "recommendation": "UPDATE - Remove OAuth2 section or implement OAuth2 feature"
}
```

### 2.2 Redundancy Detection

**Safety Rule:** Mark as duplicate ONLY if >90% content similarity AND same accuracy level.

**Detection Commands:**
```bash
# Find potential duplicates by content similarity
for file in docs/**/*.md; do
  echo "=== $file ==="
  head -20 "$file" | tr '[:upper:]' '[:lower:]' | sed 's/[^a-z0-9 ]//g'
done

# Check for exact duplicates
find docs/ -name "*.md" -exec md5sum {} \; | sort | uniq -d -w32

# Find near-duplicates by first paragraph
find docs/ -name "*.md" -exec sh -c '
  file="$1"
  first_para=$(sed -n "/^$/q;p" "$file" | tr -d "\n" | tr "[:upper:]" "[:lower:]")
  echo "$first_para|${file##*/}"
' _ {} \; | sort | cut -d"|" -f1 | uniq -c | sort -nr | head -10
```

**Redundancy Classification:**

- **Exact Duplicates (100%)**: Safe to delete after confirming newer version
- **Near Duplicates (90-99%)**: Review differences before merging
- **Overlapping Scope (70-89%)**: May serve different purposes - investigate
- **Complementary (<70%)**: Different perspectives OK to keep separate

### 2.3 Link Validation & Cross-Reference Analysis

**Safety Rule:** Before deleting/moving ANY file, verify no broken links will result.

```bash
# Find all internal links
rg '\[.*\]\([^h].*\.md.*\)' docs/ --only-matching

# Build dependency graph
echo "Building link dependency graph..."
for file in docs/**/*.md; do
  links=$(rg '\[.*\]\(([^h)]*\.md)\)' "$file" -o -r '$1' || true)
  for link in $links; do
    echo "$file -> $link"
  done
done

# Safety check before deletion:
target_file="docs/api/old-endpoint.md"
if [ -n "$(rg -l "$target_file" docs/)" ]; then
  echo "⚠️ CANNOT DELETE: Still referenced by:"
  rg -l "$target_file" docs/
  echo "Update references first or archive instead of delete"
fi
```

---

## Phase 3: Strategic Consolidation Planning

### 3.1 Consolidation Decision Framework

**Decision Tree with Safety Checks:**

**MERGE:**
- Conditions: similarity >= 90%, both_verified_accurate: true, no_unique_critical_info: true
- Safety Checks: User confirms merge preview, all cross-references will be updated, git history preserved
- Risk Level: LOW

**ARCHIVE:**
- Conditions: documented_feature_removed_from_code: true, last_modified > 180_days, historical value: true
- Safety Checks: Git log confirms feature removal, no active cross-references, user confirms not planned feature
- Risk Level: MEDIUM

**DELETE:**
- Conditions: exact_duplicate: true, zero_unique_information: true, newer_version_exists: true
- Safety Checks: User explicitly confirms deletion, no external links to this file, archived copy created first
- Risk Level: HIGH

**REWRITE:**
- Conditions: accuracy_score < 60, code_verification_failed: true, still_relevant_topic: true
- Safety Checks: Identify all inaccuracies first, verify current implementation, user reviews rewrite before replacing
- Risk Level: MEDIUM

**CREATE:**
- Conditions: feature_exists_in_code: true, no_documentation_found: true, critical_user_facing: true
- Safety Checks: Verify feature is stable (not experimental), extract examples from actual code, user confirms scope before writing
- Risk Level: LOW

### 3.2 Proposed New Structure

**Adaptive Structure Based on Project Size:**

```bash
# Small projects (<20 docs): Flat structure
docs/
  README.md           # Overview + navigation
  quickstart.md       # Getting started
  api.md              # API reference
  development.md      # Contributing guide
  changelog.md        # Version history

# Medium projects (20-100 docs): 2-level hierarchy
docs/
  /getting-started/
    installation.md
    quickstart.md
    configuration.md
  /guides/
    authentication.md
    deployment.md
    troubleshooting.md
  /api/
    rest-api.md
    graphql-api.md
    webhooks.md
  /architecture/
    overview.md
    database-schema.md
    tech-stack.md
  /contributing/
    development-setup.md
    code-standards.md
    testing.md
  README.md           # Main navigation hub

# Large projects (100+ docs): 3-level hierarchy with role separation
docs/
  /users/             # End-user documentation
  /developers/        # Developer documentation
  /operations/        # DevOps/SRE documentation
  /archive/           # Historical docs
  README.md
```

### 3.3 Migration Plan Generation

**Git-Safe Migration with History Preservation:**

```bash
#!/bin/bash
# Generated migration script with safety checks

set -e  # Exit on any error

# Pre-flight checks
echo "=== Pre-Flight Safety Checks ==="
if [ -n "$(git status --porcelain)" ]; then
  echo "❌ Working directory not clean. Commit or stash changes first."
  exit 1
fi

# Create working branch
BRANCH="docs/consolidation-$(date +%Y%m%d-%H%M%S)"
git checkout -b "$BRANCH"
echo "✅ Working on branch: $BRANCH"

# Create backup
BACKUP_DIR=".backup-docs-$(date +%Y%m%d)"
if [ ! -d "$BACKUP_DIR" ]; then
  echo "📦 Creating backup..."
  cp -r docs/ "$BACKUP_DIR/"
fi
```

---

## Phase 4: Safe Execution with Continuous Verification

### 4.1 Pre-Execution Checklist

**DO NOT PROCEED** unless ALL checkboxes verified:

- [ ] Git working directory is clean
- [ ] On dedicated branch (not main/master)
- [ ] Backup created at `.backup-docs-YYYYMMDD/`
- [ ] User has reviewed consolidation plan
- [ ] All tests passing before changes
- [ ] Code analysis completed (Phase 1)
- [ ] Documentation inventory completed (Phase 2)
- [ ] Consolidation plan generated (Phase 3)
- [ ] User explicitly confirmed plan

### 4.2 Execution with Rollback Points

```bash
CHECKPOINT_FILE=".sdm-checkpoints.log"

function create_checkpoint() {
  local checkpoint_name=$1
  local commit_hash=$(git rev-parse HEAD)
  echo "$(date +%Y-%m-%d_%H:%M:%S) | $checkpoint_name | $commit_hash" >> $CHECKPOINT_FILE
  echo "📍 Checkpoint: $checkpoint_name ($commit_hash)"
}

function rollback_to_checkpoint() {
  local checkpoint_name=$1
  local commit_hash=$(grep "$checkpoint_name" $CHECKPOINT_FILE | tail -1 | cut -d'|' -f3 | tr -d ' ')

  if [ -z "$commit_hash" ]; then
    echo "❌ Checkpoint '$checkpoint_name' not found"
    return 1
  fi

  echo "⏪ Rolling back to checkpoint: $checkpoint_name"
  git reset --hard "$commit_hash"
  echo "✅ Rollback complete"
}

# Initialize
create_checkpoint "pre-consolidation"

# Execute in batches with validation after each
```

### 4.3 Continuous Validation

**After EACH batch:**

```bash
function validate_documentation_state() {
  echo "=== Running Validation Suite ==="

  # Check 1: No broken internal links
  echo "1. Checking internal links..."
  broken_links=$(rg '\[.*\]\((?!http).*\.md\)' docs/ -o | \
    while read link; do
      file=$(echo "$link" | sed -E 's/.*\]\(([^)]+)\).*/\1/')
      if [ ! -f "docs/$file" ]; then
        echo "$file"
      fi
    done)

  if [ -n "$broken_links" ]; then
    echo "❌ Broken links found:"
    echo "$broken_links"
    return 1
  fi
  echo "✅ All internal links valid"

  # Check 2: No orphaned files
  echo "2. Checking for orphaned files..."
  # Implementation for detecting unreferenced docs

  # Check 3: Code examples still valid
  echo "3. Validating code examples..."
  # Extract and test code blocks

  return 0
}
```

---

## Phase 5: Reporting and Quality Metrics

### 5.1 Execution Report Template

```markdown
# Documentation Consolidation Report
**Generated:** 2025-11-23 10:24 IST
**Branch:** docs/sdm-20251123-102400
**Duration:** 8 minutes 34 seconds

---

## Summary

- **Files Analyzed:** 73
- **Actions Taken:** 18
- **Files Deleted:** 5
- **Files Merged:** 8 → 4
- **Files Archived:** 3
- **Files Moved:** 12
- **Links Updated:** 47
- **Space Saved:** 184 KB

---

## System Verification

### Technology Stack (Verified)
✅ React 18.2.0 (package.json + 234 imports)
✅ TypeScript 5.0.0 (tsconfig.json + .ts files)
✅ PostgreSQL 15 (docker-compose.yml + 45 queries)
✅ Redis 7.0 (docker-compose.yml + 12 cache files)

### Discrepancies Found
❌ **PouchDB** mentioned in docs/offline-sync.md but NOT in code
   - No imports found
   - No npm dependency
   - Recommendation: Archived to docs/archive/offline-sync.md
```

### 5.2 Success Metrics

After consolidation:

- ✅ Duplicate content: <5%
- ✅ Documentation accuracy: >90%
- ✅ Broken links: 0
- ✅ Orphaned files: 0
- ✅ Outdated docs (>180 days): <10%
- ✅ Missing docs for critical features: 0
- ✅ Code example validity: 100%

---

## Natural Language Commands

**Audit Commands:**
- "Audit the documentation for accuracy"
- "Check if docs match the actual codebase"
- "Find outdated or obsolete documentation"

**Consolidation Commands:**
- "Clean up duplicate documentation"
- "Organize the docs folder structure"
- "Merge similar documentation files"

**Analysis Commands:**
- "Find undocumented features in the code"
- "Which parts of the system lack documentation?"
- "Show me documentation coverage gaps"

**Safety Commands:**
- "Verify documentation accuracy before making changes"
- "Create a safe consolidation plan"
- "Check what would be affected by deleting old docs"

---

## Safety Guarantee

**This skill will NEVER:**
- ❌ Delete files without verification against code
- ❌ Assume documentation is obsolete without git history check
- ❌ Make changes without user confirmation (except trivial fixes)
- ❌ Break cross-references or external links
- ❌ Lose git history during restructuring
- ❌ Execute without creating rollback points
- ❌ Skip validation after changes

**This skill will ALWAYS:**
- ✅ Verify actual code implementation first
- ✅ Create backups before destructive operations
- ✅ Preserve git history with `git mv`
- ✅ Show previews before execution
- ✅ Execute in incremental batches
- ✅ Validate after each batch
- ✅ Provide detailed audit trail
- ✅ Generate rollback commands

---

## Usage Examples

### Example 1: Full Documentation Audit

```
User: "Audit the documentation and clean up any issues"

SDM Execution:
1. Phase 1: System Reality Check
   ✅ Detected: React + TypeScript + PostgreSQL + Redis
   ✅ Verified: 47 features in code
   ⚠️ Found: 3 documented features not in code

2. Phase 2: Document Analysis
   📊 Total docs: 73
   ✅ Accurate: 58 (79%)
   ⚠️ Needs update: 12 (16%)
   ❌ Obsolete: 3 (5%)

3. Phase 3: Consolidation Plan
   📋 Generated plan with 23 actions
   User approved selective execution

4. Safe Execution
   ✅ Executed approved batches with validation
   ✅ Created rollback checkpoints
   ✅ Generated detailed report
```

### Example 2: Targeted Accuracy Verification

```
User: "Check if the API documentation matches the actual implementation"

SDM Execution:
1. Run Phase 1 (System Reality) only
2. Compare docs against code
3. Generate accuracy report:

   Inaccurate Documentation Found:

   ❌ docs/offline-sync.md
      Claims: "Built with PouchDB for offline-first architecture"
      Reality: No PouchDB in dependencies or code
      Confidence: 100%
      Suggestion: Remove or mark as planned feature

   ✅ docs/authentication.md
      Verified: JWT implementation matches documentation
      Code references: 23 files
      Confidence: 100%

4. No execution - report only mode
```

### Example 3: Parallel Subagent Verification (Tauri)

```
User: "Check what the documentation says about Tauri vs actual code"

SDM Execution with Subagents:

Step 1: Spawn 5 parallel Explore agents in ONE message:
  Task(subagent_type="Explore", prompt="Find all Tauri mentions in docs/ folder")
  Task(subagent_type="Explore", prompt="Check package.json for @tauri-apps dependencies")
  Task(subagent_type="Explore", prompt="Find src-tauri/ directory and list its contents")
  Task(subagent_type="Explore", prompt="Search for @tauri-apps/api imports in src/")
  Task(subagent_type="Explore", prompt="Check CLAUDE.md for Tauri documentation")

Step 2: Wait for ALL agents to complete (parallel execution)

Step 3: Synthesize findings into comparison table:
  | Aspect              | Docs Say           | Code Reality        | Status    |
  |---------------------|-------------------|---------------------|-----------|
  | Basic Tauri app     | "runs on Linux"   | ✅ Valid v2.9.5     | ACCURATE  |
  | System Tray         | TODO (planned)    | ❌ No code          | ACCURATE  |
  | Frontend API usage  | Not documented    | ❌ No imports       | GAP       |
  | CLAUDE.md mention   | Expected          | ❌ Missing          | GAP       |

Step 4: Generate recommendations:
  - ACCURATE items: No action needed
  - GAP items: Flag for user decision (add docs or implement feature?)
```

### Example 4: Full Codebase Documentation Audit with Subagents

```
User: "Audit all documentation for accuracy"

SDM Parallel Execution Strategy:

Batch 1 - Tech Stack Detection (4 agents):
  Task(Explore, "Parse package.json dependencies and devDependencies")
  Task(Explore, "Find all import statements in src/ and categorize by library")
  Task(Explore, "List all config files (*.config.*, .env.*, docker-compose.*)")
  Task(Explore, "Find all database/API connection code")

Batch 2 - Documentation Inventory (3 agents):
  Task(Explore, "List all .md files in docs/ with their H1/H2 headings")
  Task(Explore, "Find all code examples in docs/*.md files")
  Task(Explore, "Check for broken internal links between docs")

Batch 3 - Cross-Verification (per technology found):
  Task(Explore, "Verify Supabase docs match src/composables/useSupabase*.ts")
  Task(Explore, "Verify Canvas docs match src/composables/canvas/*.ts")
  Task(Explore, "Verify Timer docs match src/stores/timer.ts")

Total: 10 agents across 3 batches = ~30 seconds vs ~5 minutes sequential
```

---

## Resources

This skill includes scripts for automated analysis and references for detailed guidance:

### scripts/
Automated analysis tools for documentation auditing and consolidation:

- **analyze_tech_stack.py** - Detect actual technologies from codebase
- **verify_docs_accuracy.py** - Compare documentation against code implementation
- **detect_duplicates.py** - Find duplicate and near-duplicate documentation
- **validate_links.py** - Check for broken internal and external links
- **generate_consolidation_plan.py** - Create safe, step-by-step consolidation plan
- **execute_migration.sh** - Safe execution script with rollback capabilities

### references/
Detailed guides and reference materials:

- **link_validation_guide.md** - Comprehensive link checking strategies
- **redundancy_detection_guide.md** - Advanced techniques for finding duplicate content
- **git_safe_operations.md** - Best practices for preserving history during reorganization
- **documentation_metrics.md** - Standards for measuring documentation quality
- **rollback_procedures.md** - Emergency recovery procedures

These resources provide the technical implementation details for the workflows described above, enabling systematic and safe documentation management.

---

## MASTER_PLAN.md Management

**Specialized workflows for intelligent master-plan file management.**

This section provides dedicated capabilities for managing `docs/MASTER_PLAN.md` and related planning documents, including safe updates, progress tracking, and chief-architect integration.

### Activation Triggers
- **Keywords**: master-plan, plan update, document maintenance, progress update, ADR update
- **Files**: `/docs/MASTER_PLAN.md` and related planning documents
- **Contexts**: Chief-architect delegation, post-implementation updates, architectural decisions

### Core Capabilities

#### 1. Intelligent Document Analysis
- **Complete File Reading**: Parse entire master-plan before any operations
- **Content Structure Analysis**: Understand existing sections and format
- **Change Detection**: Identify outdated, missing, or redundant content
- **Currency Assessment**: Determine what needs updating vs. what's current
- **Redundancy Prevention**: Avoid adding duplicate or unnecessary content

#### 2. Safe Update Operations
- **Read-First Approach**: Never write without comprehensive analysis
- **Incremental Updates**: Apply changes section by section
- **Content Merging**: Integrate new information with existing content
- **Format Preservation**: Maintain existing structure and emoji usage
- **Backup Location**: All backups stored with timestamps in `/docs/master-plan/backups/`

### Master-Plan Management Domains

#### Domain 1: Executive Summary Management
- **Current State Assessment**: Analyze project health and status indicators
- **Brutal Honesty Updates**: Update honest assessments with current data
- **Success Criteria Refresh**: Update measurable success criteria
- **Immediate Actions**: Maintain current prioritized action items

#### Domain 2: Phase Progress Tracking
- **Phase Completion Status**: Track and update phase progress with metrics
- **Deliverable Documentation**: Update created deliverables and evidence
- **Validation Results**: Document testing and validation outcomes
- **Readiness Assessment**: Update phase-to-phase readiness status

#### Domain 3: Architecture Decision Records (ADRs)
- **Decision Documentation**: Add new architectural decisions with full rationale
- **Alternative Analysis**: Document considered alternatives and trade-offs
- **Impact Assessment**: Track decision impact on user experience and system
- **Status Updates**: Update ADR status based on implementation outcomes

#### Domain 4: Skills Execution Tracking
- **Skills Inventory**: Update skills executed with actual outcomes
- **Performance Metrics**: Document quantified results and improvements
- **Learning Capture**: Update insights and patterns discovered
- **Integration Status**: Track how skills work together

#### Domain 5: Success Criteria Management
- **Criteria Tracking**: Monitor progress toward measurable success criteria
- **Completion Evidence**: Document proof of criteria fulfillment
- **Metrics Updates**: Update quantified metrics with current data
- **Status Validation**: Verify and document completion status

### Integration with Chief-Architect

The smart-doc-manager skill accepts delegation from chief-architect through standardized interfaces:

#### Update with Implementation Results
```typescript
interface ImplementationUpdateRequest {
  action: 'update-with-implementation-results';
  decision: PersonalAppDecision;
  results: PersonalImplementationResult;
  context: PersonalAppContext;
  safetyLevel: 'comprehensive' | 'standard' | 'quick';
}
```

#### Update with Architecture Decision
```typescript
interface ArchitectureDecisionUpdateRequest {
  action: 'update-with-architecture-decision';
  decision: PersonalAppDecision;
  alternatives: AlternativeAnalysis[];
  rationale: DecisionRationale;
  impact: ImpactAssessment;
}
```

#### Update Progress Status
```typescript
interface ProgressUpdateRequest {
  action: 'update-progress-status';
  phase: number;
  completion: CompletionStatus;
  deliverables: DeliverableRecord[];
  validation: ValidationResults;
}
```

### Master-Plan Update Workflow

```typescript
async analyzeMasterPlan(): Promise<PlanAnalysis> {
  // 1. Read complete current document
  const currentContent = await this.readEntireFile(this.planPath);

  // 2. Parse and understand structure
  const parsedStructure = this.parseMarkdownStructure(currentContent);

  // 3. Analyze content currency and completeness
  const contentAnalysis = {
    currentSections: parsedStructure.sections,
    outdatedContent: this.detectOutdatedContent(parsedStructure),
    missingContent: this.identifyMissingContent(parsedStructure),
    redundantAreas: this.identifyRedundantContent(parsedStructure)
  };

  // 4. Create safety backup
  await this.createTimestampedBackup(currentContent);

  return contentAnalysis;
}
```

### Master-Plan Manager Principles

1. **Document Safety First**: Never compromise document integrity or existing content
2. **Read Before Writing**: Never make changes without comprehensive analysis of current state
3. **Meaningful Updates Only**: Only update when changes represent genuine improvements
4. **Backup and Recovery**: Always maintain reliable backup and rollback capabilities
5. **Format Preservation**: Maintain existing document structure, formatting, and style
6. **Content Intelligence**: Understand context and meaning, not just text patterns
7. **Integration Excellence**: Work seamlessly with chief-architect and other skills

---

## MANDATORY USER VERIFICATION REQUIREMENT

### Policy: No Fix Claims Without User Confirmation

**CRITICAL**: Before claiming ANY issue, bug, or problem is "fixed", "resolved", "working", or "complete", the following verification protocol is MANDATORY:

#### Step 1: Technical Verification
- Run all relevant tests (build, type-check, unit tests)
- Verify no console errors
- Take screenshots/evidence of the fix

#### Step 2: User Verification Request
**REQUIRED**: Use the `AskUserQuestion` tool to explicitly ask the user to verify the fix:

```
"I've implemented [description of fix]. Before I mark this as complete, please verify:
1. [Specific thing to check #1]
2. [Specific thing to check #2]
3. Does this fix the issue you were experiencing?

Please confirm the fix works as expected, or let me know what's still not working."
```

#### Step 3: Wait for User Confirmation
- **DO NOT** proceed with claims of success until user responds
- **DO NOT** mark tasks as "completed" without user confirmation
- **DO NOT** use phrases like "fixed", "resolved", "working" without user verification

#### Step 4: Handle User Feedback
- If user confirms: Document the fix and mark as complete
- If user reports issues: Continue debugging, repeat verification cycle

### Prohibited Actions (Without User Verification)
- Claiming a bug is "fixed"
- Stating functionality is "working"
- Marking issues as "resolved"
- Declaring features as "complete"
- Any success claims about fixes

### Required Evidence Before User Verification Request
1. Technical tests passing
2. Visual confirmation via Playwright/screenshots
3. Specific test scenarios executed
4. Clear description of what was changed

**Remember: The user is the final authority on whether something is fixed. No exceptions.**
