---
name: document
description: Create or update documentation for features, APIs, or components
argument-hint: <component or feature to document>
user-invocable: true
allowed-tools:
  - Read
  - Write
  - Grep
  - Glob
  - Bash
  - AskUserQuestion
context: fork
agent: tech-writer
---

# /document - Documentation Generation

Create or update documentation based on recent commits or specific components.

## Purpose

Maintain quality documentation by:
- Classifying changes by Area (what) and Criticality (severity)
- Determining documentation propagation paths
- Updating docs in correct order (entry point → downstream)
- Skipping levels with no impact

## Modes

| Mode | Trigger | Scope | Cost |
|------|---------|-------|------|
| **Incremental** (default) | `/document` | Commits since last docs update | ~2min, ~15k tokens |
| **Full Review** | `/document --full` | All docs consistency check | ~5min, ~70k tokens |

**Default behavior**: Analyze commits on current branch since the last documentation commit.

## Inputs

- `$ARGUMENTS`: Component, feature, or API to document (optional - if empty, analyze recent commits)
  - Use `--full` to trigger full consistency review across all documentation
- Source code for reference
- Existing docs in `docs/`
- `${PROJECT_NAME}`: Current project context

## Outputs

Documentation updates organized by impact area with propagation paths.

---

## Impact Classification (Orthogonal Dimensions)

### Areas (What Changed)

| Area | Boundary | Entry Point |
|------|----------|-------------|
| **System** | Core functionality broken (hooks, MCP, install, agents) | ISSUES |
| **Product** | Vision, goals, target users, success metrics | VISION |
| **Solution** | Capabilities, feature matrix, technical scope | BLUEPRINT |
| **Specification** | Features, requirements, user stories, acceptance criteria | PRD |
| **Architecture** | Components, patterns, dependencies, decisions | ARCHITECTURE |
| **Development** | Task organization, priorities, status | ROADMAP/BACKLOG |
| **Documentation** | All docs: arch docs, policies, knowledge, guides | Varies |

### Criticality (Severity - Independent of Area)

| Level | Definition | Response |
|-------|------------|----------|
| **CRITICAL** | Blocking, broken functionality, data loss risk | Immediate |
| **HIGH** | Significant impact, major feature affected | Current session |
| **MEDIUM** | Moderate impact, standard priority | Current sprint |
| **LOW** | Minor, cosmetic, can defer | Backlog |

### Propagation Paths by Area

```
SYSTEM        → ISSUES → BACKLOG
PRODUCT       → VISION → BLUEPRINT → PRD → ARCHITECTURE → ADR → ROADMAP → BACKLOG
SOLUTION      → BLUEPRINT → PRD → ARCHITECTURE → ADR → ROADMAP → BACKLOG
SPECIFICATION → PRD → ARCHITECTURE → ADR → ROADMAP → BACKLOG
ARCHITECTURE  → ARCHITECTURE → ADR → ROADMAP → BACKLOG
DEVELOPMENT   → ROADMAP → BACKLOG (or BACKLOG only)
DOCUMENTATION → Direct to target doc
```

---

## Workflow

### 0. Determine Mode and Scope

Check `$ARGUMENTS` for `--full` flag:
- **If `--full` present**: Full consistency review mode (step 0a)
- **Otherwise**: Incremental mode - commits since last docs update (step 0b)

#### 0a. Full Review Mode (--full only)

**Cost**: ~5min, ~70k tokens

Read current state of ALL key docs to detect cross-document inconsistencies:

- `docs/objectives/VISION.md`
- `docs/objectives/BLUEPRINT.md`
- `docs/architecture/PRD.md`
- `docs/architecture/ARCHITECTURE.md`
- `docs/development/BACKLOG.md`
- `docs/development/ISSUES.md`
- `README.md`
- `CLAUDE.md`

Then proceed to step 1 with full scope.

#### 0b. Incremental Mode (default)

**Cost**: ~2min, ~15k tokens

Only read docs that are directly affected by recent changes. Skip full consistency check.

### 1. Gather Changes

#### 1a. Find Last Documentation Commit

```bash
# Find the most recent commit that updated docs
LAST_DOCS_COMMIT=$(git log --oneline --all \
  --grep="^docs:" \
  --grep="^docs(" \
  -- README.md CLAUDE.md 'docs/**' '.claude/hooks/README.md' \
  -1 --format="%H" 2>/dev/null | head -1)

# If no docs commit found, use merge-base with main
if [ -z "$LAST_DOCS_COMMIT" ]; then
  LAST_DOCS_COMMIT=$(git merge-base HEAD main 2>/dev/null || echo "HEAD~10")
fi

echo "Analyzing commits since: $LAST_DOCS_COMMIT"
```

#### 1b. Get Commits Since Last Docs Update

```bash
# Get commits since last docs update
git log ${LAST_DOCS_COMMIT}..HEAD --oneline

# Get changed files in those commits
git diff ${LAST_DOCS_COMMIT}..HEAD --name-only
```

#### 1c. Include Uncommitted Changes (Optional)

If there are uncommitted changes, ask user:

```
AskUserQuestion:
  question: "Include uncommitted changes in documentation scope?"
  header: "Scope"
  options:
    - label: "Commits only (Recommended)"
      description: "Only analyze committed changes since last docs update"
    - label: "Include uncommitted"
      description: "Also include staged and unstaged changes"
```

If including uncommitted:
```bash
git status --porcelain
git diff --name-only          # Unstaged
git diff --cached --name-only # Staged
```

### 2. Classify Changes (Area × Criticality)

For each changed file/feature, determine BOTH dimensions:

#### Area Classification

| File Pattern | Area |
|--------------|------|
| `install.sh`, MCP config, hooks broken | **System** |
| `docs/objectives/VISION.md`, goals, OKRs | **Product** |
| `docs/objectives/BLUEPRINT.md`, capabilities, scope | **Solution** |
| `.claude/skills/` behavior, requirements | **Specification** |
| `docs/architecture/PRD.md`, user stories | **Specification** |
| `docs/architecture/ARCHITECTURE.md`, `adr/` | **Architecture** |
| `.claude/hooks/scripts/`, `.claude/agents/` structure | **Architecture** |
| `docs/objectives/ROADMAP.md`, `docs/development/` | **Development** |
| `README.md`, `CLAUDE.md` | **Documentation** |
| `docs/policy/`, `global/policy/` | **Documentation** |
| `docs/knowledge/` | **Documentation** |

#### Criticality Assessment

| Condition | Criticality |
|-----------|-------------|
| Functionality broken, blocking work | **CRITICAL** |
| Major feature change, significant impact | **HIGH** |
| Standard change, moderate impact | **MEDIUM** |
| Typo, cosmetic, minor improvement | **LOW** |

### 3. Group and Prioritize

Group by Area, sort by Criticality within each area:

```
┌─────────────────────────────────────────────────────────────────────┐
│ IMPACT ANALYSIS - Session Changes                                    │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│ SYSTEM                                                               │
│ └── [CRITICAL] Hooks broken after settings change                    │
│     Path: ISSUES → BACKLOG                                           │
│                                                                      │
│ PRODUCT                                                              │
│ └── [HIGH] New target user segment                                   │
│     Path: VISION → BLUEPRINT → PRD → ARCHITECTURE → BACKLOG          │
│                                                                      │
│ SOLUTION                                                             │
│ └── [HIGH] New /document skill capability                            │
│     Path: BLUEPRINT → PRD → ARCHITECTURE → BACKLOG                   │
│     Skip: ADR (no decision needed), ROADMAP (no milestone change)    │
│                                                                      │
│ SPECIFICATION                                                        │
│ └── [MEDIUM] Skill behavior change                                   │
│     Path: PRD → ARCHITECTURE → BACKLOG                               │
│                                                                      │
│ ARCHITECTURE                                                         │
│ └── [MEDIUM] New hook-utils.sh shared library                        │
│     Path: ARCHITECTURE → BACKLOG                                     │
│     Skip: ADR (minor structural), ROADMAP (no milestone)             │
│                                                                      │
│ DEVELOPMENT                                                          │
│ └── [LOW] Task status updates                                        │
│     Path: BACKLOG                                                    │
│                                                                      │
│ DOCUMENTATION                                                        │
│ └── [MEDIUM] BLUEPRINT refs moved to objectives/                     │
│     Path: Direct updates to affected docs                            │
│ └── [LOW] README typo                                                │
│     Path: README.md                                                  │
│                                                                      │
└─────────────────────────────────────────────────────────────────────┘
```

### 4. Detect Inconsistencies and Conflicts

**Full mode (`--full`)**: Proactively scan all docs for cross-document inconsistencies.

**Incremental mode (default)**: Only check for conflicts when updating specific docs. Read only the docs being modified and their direct references.

Detect conflicts between:
- **Doc ↔ Doc**: Docs contradict each other
- **Code ↔ Doc**: Implementation differs from documented behavior
- **New ↔ Old**: Recent changes contradict earlier decisions (ADRs, PRD)

#### Inconsistency Types

| Type | Example | Severity |
|------|---------|----------|
| **Decision Conflict** | New code contradicts ADR decision | HIGH |
| **Specification Drift** | Implementation differs from PRD | HIGH |
| **Cross-Doc Mismatch** | ARCHITECTURE says X, README says Y | MEDIUM |
| **Stale Reference** | Doc references removed component | MEDIUM |
| **Version Mismatch** | Changelog vs actual version | LOW |

#### When Inconsistencies Found

**NEVER silently overwrite.** Present each conflict to user:

```
AskUserQuestion:
  question: "Inconsistency detected: [describe conflict]. How should we resolve?"
  header: "Conflict"
  options:
    - label: "Update old to match new"
      description: "The new change is correct, update prior docs"
    - label: "Keep old, flag new"
      description: "The prior decision stands, new change needs review"
    - label: "Document both (tentative)"
      description: "Record conflict in ISSUES for later resolution"
    - label: "Pause for full review"
      description: "Stop and suggest appropriate agent for deep analysis"
```

#### If Decision Conflicts with ADR

When new changes contradict an existing ADR decision:

```
AskUserQuestion:
  question: "Change contradicts ADR-XXX: [summary]. This is a significant decision reversal."
  header: "ADR Conflict"
  options:
    - label: "Supersede ADR (Recommended)"
      description: "Create new ADR explaining why decision changed"
    - label: "Revert approach"
      description: "The ADR decision should stand, flag change for revision"
    - label: "Document conflict"
      description: "Record in ISSUES as unresolved architectural debt"
```

### 5. Handle Tentative or Rejected Decisions

If user selects "tentative", "pause", or rejects a proposed update:

#### Log to ISSUES.md

```markdown
## [DATE] Documentation Inconsistency - PENDING REVIEW

**Type**: [Decision Conflict | Specification Drift | Cross-Doc Mismatch]
**Severity**: [HIGH | MEDIUM | LOW]
**Session**: ${CLAUDE_SESSION_ID}

### Conflict Description
[Describe what contradicts what]

### Affected Documents
- doc1.md (line X): states "..."
- doc2.md (line Y): states "..."

### User Decision
- [ ] Tentative - needs review
- [ ] Rejected - requires architectural decision

### Recommended Resolution
**Agent**: [Architect | Business Analyst | Developer]
**Action**: [Suggest specific review action]
```

#### Suggest Appropriate Agent

| Conflict Type | Suggested Agent | Reason |
|---------------|-----------------|--------|
| ADR contradiction | `/design` (Architect) | Architectural decision needed |
| PRD specification drift | `/spec` (Business Analyst) | Requirements clarification needed |
| Implementation mismatch | `/implement` (Developer) | Code review needed |
| Cross-doc inconsistency | `/document` (Tech Writer) | Documentation alignment needed |

### 6. Present to User for Confirmation

After resolving all conflicts, present final update plan:

```
AskUserQuestion:
  question: "Proceed with documentation updates? [N resolved, M logged to ISSUES]"
  header: "Confirm"
  options:
    - label: "Proceed (Recommended)"
      description: "Update docs following propagation paths"
    - label: "Modify selection"
      description: "Let me adjust which items to update"
    - label: "Critical only"
      description: "Only address CRITICAL items now"
```

### 7. Execute Updates

For each Area (process CRITICAL items first across all areas):

1. **Update entry point document**
2. **Propagate downstream** (skip levels with no impact)
3. **Verify cross-references**

#### Update Order (Criticality First, Then by Area)

```
1. ALL CRITICAL items (any area)
   └── System: ISSUES.md → BACKLOG.md

2. ALL HIGH items
   └── Product: VISION → BLUEPRINT → PRD → ARCHITECTURE → BACKLOG
   └── Solution: BLUEPRINT → PRD → ARCHITECTURE → BACKLOG

3. ALL MEDIUM items
   └── Specification: PRD → ARCHITECTURE → BACKLOG
   └── Architecture: ARCHITECTURE.md → BACKLOG.md
   └── Documentation: Direct updates

4. ALL LOW items
   └── Development: BACKLOG.md
   └── Documentation: README.md typos
```

### 8. Validate

Check documentation quality:
- [ ] CRITICAL items addressed first
- [ ] Entry points updated before downstream
- [ ] Cross-references valid (for touched docs)
- [ ] No orphaned changes (all classified)
- [ ] Skipped levels justified
- [ ] **All detected inconsistencies resolved or logged to ISSUES**
- [ ] **No silent overwrites (user confirmed all conflicts)**
- [ ] **Tentative decisions documented with suggested agent**

**Full mode additional checks:**
- [ ] All cross-document references consistent
- [ ] No stale references to removed components
- [ ] Version numbers aligned across docs

---

## Area Boundaries (Detailed)

### System
**What belongs here:**
- Hooks not firing or erroring
- MCP servers failing to connect
- Install script broken
- Agents fail to spawn
- Skills fail to load

**Does NOT belong:**
- New hook added (→ Architecture)
- Hook behavior changed (→ Specification or Architecture)

### Product
**What belongs here:**
- Vision/goals changes
- Target user changes
- Success metrics changes
- OKR changes

**Does NOT belong:**
- Capability changes (→ Solution)
- Feature behavior (→ Specification)

### Solution
**What belongs here:**
- New capability in feature matrix
- Removing a capability
- Technical scope changes
- Feature matrix updates

**Does NOT belong:**
- How features behave (→ Specification)
- How it's implemented (→ Architecture)

### Specification
**What belongs here:**
- New user story
- Changed acceptance criteria
- New functional requirement
- Skill behavior changes
- Feature behavior details

**Does NOT belong:**
- How components interact (→ Architecture)
- Task tracking (→ Development)

### Architecture
**What belongs here:**
- New component added
- Design pattern change
- Dependency added/removed
- Hook system structure
- File structure changes
- Internal refactoring

**Does NOT belong:**
- What the component does for users (→ Specification)
- Task tracking (→ Development)

### Development
**What belongs here:**
- Task status updates
- Priority changes
- Sprint/milestone progress
- Work item details
- Blockers (non-system)

**Does NOT belong:**
- New requirements (→ Specification)
- Design decisions (→ Architecture)

### Documentation
**What belongs here:**
- README updates
- CLAUDE.md updates
- Architecture docs (ARCHITECTURE.md)
- Policy docs (PRINCIPLES, RULES, GUIDELINES)
- Knowledge base (docs/knowledge/)
- User guides
- API docs

**Includes both:**
- Specification docs (PRD, ARCHITECTURE, ADRs)
- Developer docs (README, CLAUDE.md, guides)

---

## Policy Locations

```
global/policy/        # SCZ framework policies (→ ~/.claude/policy/)
├── PRINCIPLES.md     # SW engineering principles (for SCZ)
├── RULES.md          # Behavioral rules (for SCZ)
└── GUIDELINES.md     # User guidance (for users)

docs/policy/          # Project-local policies (supplement global)
├── PRINCIPLES.md     # Project-specific principles
├── RULES.md          # Project-specific rules
└── GUIDELINES.md     # Project-specific user guidance
```

---

## Output Format

### Impact Analysis Report

```markdown
# Documentation Impact Analysis

**Session**: ${CLAUDE_SESSION_ID}
**Date**: $(date +%Y-%m-%d)
**Changes Analyzed**: N files

## Changes by Area × Criticality

### SYSTEM
| Change | Criticality | Path | Skip |
|--------|-------------|------|------|
| (none) | | | |

### PRODUCT
| Change | Criticality | Path | Skip |
|--------|-------------|------|------|
| (none) | | | |

### SOLUTION
| Change | Criticality | Path | Skip |
|--------|-------------|------|------|
| /document skill capability | HIGH | BLUEPRINT→PRD→ARCH→BACKLOG | ADR, ROADMAP |

### SPECIFICATION
| Change | Criticality | Path | Skip |
|--------|-------------|------|------|
| Skill behavior change | MEDIUM | PRD→ARCH→BACKLOG | ADR, ROADMAP |

### ARCHITECTURE
| Change | Criticality | Path | Skip |
|--------|-------------|------|------|
| hook-utils.sh library | MEDIUM | ARCH→BACKLOG | ADR, ROADMAP |

### DEVELOPMENT
| Change | Criticality | Path | Skip |
|--------|-------------|------|------|
| Task completions | LOW | BACKLOG | |

### DOCUMENTATION
| Change | Criticality | Path | Skip |
|--------|-------------|------|------|
| BLUEPRINT refs | MEDIUM | Direct | |
| README typo | LOW | Direct | |

## Recommended Update Order
1. [HIGH] BLUEPRINT.md - new capability
2. [HIGH] PRD.md - /document skill description
3. [MEDIUM] PRD.md - skill behavior change
4. [MEDIUM] ARCHITECTURE.md - hook utils section
5. [MEDIUM] Various docs - BLUEPRINT refs
6. [LOW] BACKLOG.md - task tracking
7. [LOW] README.md - typo fix
```

## Policy References

**Should-read** from `~/.claude/policy/RULES.md`:
- Professional Honesty - No marketing language, accurate claims
- File Organization - Purpose-based organization
