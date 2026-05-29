---
name: semantic-validation
description: GenAI-powered semantic validation - detects outdated docs, version mismatches, and architectural drift
version: 1.0.0
category: validation
auto_invoke: false
---

# Semantic Validation Skill

**Purpose**: Use GenAI to validate that documentation accurately reflects implementation, catching issues that structural validation misses.

---

## When to Use This Skill

**Auto-invoke triggers** (when implemented):

- `/align-project` command (Phase 2: Semantic Validation)
- After major code changes (10+ files modified)
- Before releases

**Manual invoke**:

- Investigating documentation accuracy
- After refactoring
- When documentation feels stale

---

## What This Skill Detects

### 1. Outdated Documentation

**Problem**: Documentation claims X, code implements Y

**Example**:

```markdown
# PROJECT.md:181

### Tool Calling (CRITICAL ISSUE)

Status: Still investigating duplicate tool calls
```

```typescript
// src/convert.ts:45 (committed 3 hours ago)
// SOLVED: Streaming tool parameters via input_json_delta
case "tool-input-delta": {
  controller.enqueue({ type: "input_json_delta", ... });
}
```

**Detection**: GenAI compares documented status with implementation reality.

### 2. Version Mismatches

**Problem**: Different versions across files

**Example**:

- `CHANGELOG.md:8` says `v2.0.0`
- `package.json:3` says `v1.0.0`
- `README.md:5` says `latest stable: 1.5.0`

**Detection**: Extract version numbers from all docs, flag inconsistencies.

### 3. Architecture Drift

**Problem**: Documented architecture doesn't match current structure

**Example**:

```markdown
# PROJECT.md:95

Architecture: Simple proxy server
```

```
# Actual codebase structure:
src/
├── translation-layers/  (5 different layers)
├── format-converters/
├── stream-handlers/
└── protocol-adapters/
```

**Detection**: Analyze file organization, compare to documented architecture.

### 4. Stale Claims

**Problem**: Documentation makes claims no longer true

**Example**:

```markdown
# README.md:8

"A simplified fork of anyclaude"
```

```
# Reality:
- 2000+ lines of custom code
- Complex 5-layer architecture
- Completely different from original
```

**Detection**: Look for words like "simple", "basic", "fork" and verify against codebase size/complexity.

### 5. Broken Promises

**Problem**: Documentation promises features not implemented

**Example**:

```markdown
# README.md:45

## Features

- ✅ Streaming support
- ✅ Tool calling
- ✅ Image attachments (coming soon)
```

```bash
# Search codebase for image handling
grep -r "image" src/  # No results
```

**Detection**: Extract claimed features, search codebase for implementation.

---

## Workflow

### Phase 1: Extract Documentation Claims

#### Step 1.1: Read PROJECT.md Sections

Extract these sections:

- **Architecture Overview** (lines 50-150)
- **Known Issues** (lines 180-250)
- **Feature List** (if present)
- **Status Claims** (SOLVED, IN PROGRESS, etc.)

**Parse format**:

```markdown
### Section Title (Status)

Status: CRITICAL ISSUE | HIGH | SOLVED
```

Create map:

```json
{
  "tool-calling": {
    "status": "CRITICAL ISSUE",
    "description": "Still investigating duplicate tool calls",
    "lines": "181-210"
  }
}
```

#### Step 1.2: Extract Versions

Search all documentation for version patterns:

- `v1.2.3`
- `version 1.2.3`
- `@latest`
- `stable: X.X.X`

Sources:

- `package.json` → `version` field
- `CHANGELOG.md` → `## [X.X.X]` headers
- `README.md` → version badges, mentions
- `pyproject.toml` → `version` field
- `Cargo.toml` → `version` field

Create version map:

```json
{
  "package.json": "1.0.0",
  "CHANGELOG.md": "2.0.0",
  "README.md": "1.5.0 (stable)"
}
```

#### Step 1.3: Extract Architecture Claims

Parse PROJECT.md "Architecture Overview":

- Pattern type (Translation Layer, MVC, Microservices, etc.)
- Component descriptions
- Complexity claims ("simple", "straightforward", "complex")

---

### Phase 2: Analyze Implementation Reality

#### Step 2.1: Search for Issue Resolutions

For each "CRITICAL ISSUE" or "HIGH" status in Known Issues:

```bash
# Search for resolution keywords in code
grep -r "SOLVED\|FIX\|RESOLVED" src/

# Search for the specific issue topic
grep -r "{issue_keyword}" src/

# Check git log for recent fixes
git log --oneline --since="1 week ago" | grep -i "{issue_keyword}"
```

**Signs of resolution**:

- Code comments with "SOLVED", "FIXED"
- Git commits with fix message
- Implementation of previously-missing feature
- Error handlers for previously-unhandled case

#### Step 2.2: Validate Architecture Claims

**If docs claim "simple" or "straightforward"**:

```bash
# Count files
FILE_COUNT=$(find src/ -type f | wc -l)

# Count lines of code
LOC=$(find src/ -name "*.ts" -o -name "*.js" | xargs wc -l | tail -1)

# Check for complex patterns
LAYERS=$(find src/ -type d -name "*layer*" | wc -l)
ADAPTERS=$(grep -r "adapter" src/ | wc -l)
CONVERTERS=$(grep -r "convert" src/ | wc -l)
```

**Complexity indicators**:

- Files > 50 → Not simple
- LOC > 1000 → Not simple
- Directories with "layer", "adapter", "converter" → Translation pattern, not simple
- Multiple service directories → Microservices, not monolithic

**If docs claim specific pattern**:

- **Translation Layer**: Look for convert/transform/adapter files
- **MVC**: Look for models/, views/, controllers/ directories
- **Microservices**: Look for services/, Docker files
- **Event-Driven**: Look for EventEmitter, pub/sub code

#### Step 2.3: Verify Feature Claims

For each claimed feature:

```bash
# Example: "Image attachments supported"
grep -r "image" src/
grep -r "attachment" src/
grep -r "file.*upload" src/

# If no results → Feature not implemented
```

**Verification levels**:

- ✅ Implemented: Code found
- ⚠️ Partial: Some code, not complete
- ❌ Missing: No code found
- 🔄 Coming Soon: No code but documented as future

---

### Phase 3: Semantic Comparison

#### Step 3.1: Compare Issue Status

For each documented issue:

**ALIGNED** if:

- Status = "SOLVED" AND code has implementation
- Status = "CRITICAL" AND code has no fix

**DIVERGENT** if:

- Status = "CRITICAL" BUT code has fix (outdated doc)
- Status = "SOLVED" BUT no implementation found (inaccurate claim)

**Output format**:

````
⚠️ DIVERGENT: Section "Tool Calling" (PROJECT.md:181-210)
   Severity: HIGH

   Documented Status: CRITICAL ISSUE - Still investigating
   Actual Status: SOLVED (commit 2e8237c, 3 hours ago)

   Evidence:
   - src/convert.ts:45-89 implements solution
   - Git commit: "fix: resolve tool calling duplication"
   - No TODO or FIXME comments in related code

   Fix: Update PROJECT.md section to:
   ```markdown
   ### Tool Calling (SOLVED)
   Status: SOLVED (2024-10-26)

   Problem: Duplicate tool calls in streaming mode
   Solution: Stream tool parameters via input_json_delta
   Implementation: src/convert.ts:45-89
````

```

#### Step 3.2: Compare Architecture Claims

**ALIGNED** if:
- Docs say "simple" AND codebase is simple (< 500 LOC, 1-2 layers)
- Docs say "Translation Layer" AND pattern detected in code
- Docs say "5 layers" AND 5 layer directories found

**DIVERGENT** if:
- Docs say "simple" BUT codebase is complex (2000+ LOC, 5+ layers)
- Docs say "proxy" BUT implements translation
- Docs say "fork of X" BUT substantial divergence

**Output format**:
```

⚠️ DIVERGENT: Architecture Description (PROJECT.md:95-120)
Severity: MEDIUM

Documented: "Simple proxy server"
Actual: Complex 5-layer translation architecture

Evidence:

- 2187 lines of code in src/
- 5 directories: translation-layers/, format-converters/, stream-handlers/, protocol-adapters/, validators/
- 12 adapter files
- Complex data flow with 5 transformation steps

Suggested Fix:
Update PROJECT.md architecture section to:
"Multi-Layer Translation Architecture - This project implements
a sophisticated 5-layer architecture for translating between
incompatible API formats while preserving streaming, tool calling,
and error handling semantics."

```

#### Step 3.3: Validate Version Consistency

**ALIGNED** if:
- All version numbers match across files

**DIVERGENT** if:
- Versions differ across documentation

**Output format**:
```

❌ VERSION MISMATCH (HIGH)

Found inconsistent versions:

- package.json:3 → "1.0.0"
- CHANGELOG.md:8 → "2.0.0"
- README.md:5 → "latest stable: 1.5.0"

Most recent:

- CHANGELOG.md last updated: 2 hours ago
- package.json last updated: 3 days ago

Likely correct: 2.0.0 (CHANGELOG is most recent)

Fixes needed:

1.  Update package.json:3
    "version": "2.0.0"

2.  Update README.md:5
    Latest stable: v2.0.0

```

---

### Phase 4: Generate Report

#### Output Format

```

🧠 Semantic Validation Report

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

SUMMARY
✅ Aligned: 3/5 major sections
⚠️ Divergent: 2/5 sections outdated
Overall: 60% accuracy → NEEDS ATTENTION

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

ALIGNED SECTIONS

✅ Authentication Flow (PROJECT.md:50-89)
Documented: OAuth2 with JWT tokens
Implemented: src/auth.ts:45-67
Evidence: Code matches description

✅ Database Schema (PROJECT.md:150-180)
Documented: PostgreSQL with Prisma ORM
Implemented: Correctly described

✅ Testing Strategy (PROJECT.md:310-340)
Documented: Unit + Integration tests
Implemented: tests/unit/ and tests/integration/ present

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

DIVERGENT SECTIONS

⚠️ CRITICAL: Known Issues Section (PROJECT.md:181-210)
Severity: HIGH
Age: 3 hours since resolution

Issue: Tool Calling marked as "CRITICAL ISSUE"
Reality: SOLVED in commit 2e8237c

Evidence:

- src/convert.ts:45-89 has solution
- Commit message: "fix: resolve tool duplication"
- No outstanding TODO comments

Recommended Fix:
Update status to SOLVED, document solution

⚠️ Architecture Description (PROJECT.md:95-120)
Severity: MEDIUM

Documented: "Simple proxy server"
Reality: Complex 5-layer translation

Evidence:

- 2187 LOC in src/
- 5 transformation layers
- 12 adapter files

Recommended Fix:
Rewrite architecture section to reflect complexity

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

VERSION MISMATCHES

❌ Inconsistent Versions Found

package.json: 1.0.0
CHANGELOG.md: 2.0.0 (most recent)
README.md: 1.5.0

Recommended: Update all to 2.0.0

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

RECOMMENDED ACTIONS

Priority 1 (Critical - Fix Today):

1. Update PROJECT.md:181-210 (Tool Calling section)
2. Fix version mismatches (package.json, README)

Priority 2 (High - Fix This Week): 3. Rewrite PROJECT.md:95-120 (Architecture section)

Priority 3 (Medium - Next Sprint):
(None)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

NEXT STEPS

Option 1: Auto-fix version mismatches
/align-project
→ Choose option 2 (Fix interactively)
→ Approve version sync

Option 2: Manual updates
vim PROJECT.md
vim package.json
vim README.md
git add .
git commit -m "docs: sync versions and update solved issues"

Option 3: Review only (no changes)
This report saved to: docs/alignment-report-{date}.md

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

````

---

## Edge Cases

### Case 1: "SOLVED" But Code Removed

```markdown
# PROJECT.md
Status: SOLVED - Fixed in v1.5
````

```bash
# Search for implementation
grep -r "{feature}" src/  # No results

# Check git history
git log --all --grep="{feature}"  # Feature was removed in v2.0
```

**Output**:

```
⚠️ REGRESSION: Feature claimed as SOLVED but no longer in codebase

   Documented: SOLVED in v1.5
   Reality: Removed in v2.0 (commit abc123)

   Options:
   1. Mark as REMOVED in Known Issues
   2. Reimplement feature
   3. Update docs to reflect removal
```

### Case 2: Multiple Conflicting Claims

```markdown
# README.md:8

Simple proxy server

# ARCHITECTURE.md:15

Complex multi-layer translation system

# PROJECT.md:95

Hybrid approach: proxy with translation capabilities
```

**Output**:

```
⚠️ CONFLICTING DOCUMENTATION

   README.md: "Simple proxy"
   ARCHITECTURE.md: "Complex translation"
   PROJECT.md: "Hybrid approach"

   Codebase analysis suggests: Complex translation (2000+ LOC, 5 layers)

   Recommended: Align all docs to match PROJECT.md (source of truth)
```

### Case 3: Recent Changes Not Yet Documented

```bash
# Git shows massive refactor 6 hours ago
git log --since="1 day ago" --oneline
# 10 commits, 500+ lines changed

# PROJECT.md last updated 3 days ago
```

**Output**:

```
⚠️ DOCUMENTATION LAG

   Last PROJECT.md update: 3 days ago
   Recent changes: 10 commits (6 hours ago)
   Lines changed: 500+

   Recommendation:
   Review recent commits and update PROJECT.md to reflect changes

   Recent commit themes:
   - Refactor: stream handling (5 commits)
   - Feature: Add timeout support (3 commits)
   - Fix: Error handling (2 commits)
```

---

## Success Criteria

After running semantic validation:

- ✅ All "CRITICAL ISSUE" statuses verified against code
- ✅ Version numbers consistent across all files
- ✅ Architecture claims match codebase reality
- ✅ Feature claims verified (implemented or marked "coming soon")
- ✅ Actionable fix suggestions provided with file:line references
- ✅ Report completes in < 30 seconds for medium projects (2000-5000 LOC)

---

## Limitations

**What this skill CAN'T detect**:

- Subtly incorrect explanations (if code exists)
- Performance claims (needs profiling)
- Scalability assertions (needs load testing)
- Security vulnerabilities (use security-auditor skill)

**Workarounds**:

- Performance: Use observability skill
- Security: Use security-patterns skill
- Scalability: Manual review + load testing

---

## Integration with /align-project

This skill is Phase 2 of `/align-project`:

**Phase 1**: Structural validation (files exist, directories correct)
**Phase 2**: Semantic validation (THIS SKILL - docs match reality)
**Phase 3**: Documentation currency (separate skill)
**Phase 4**: Cross-reference validation (separate skill)

**Invocation**:

```bash
/align-project
# After Phase 1 completes, Phase 2 runs automatically
# User sees combined report from all phases
```

---

## Output to User

Always provide:

1. **Severity levels** (CRITICAL, HIGH, MEDIUM, LOW)
2. **Evidence** (file:line references, commit SHAs)
3. **Suggested fixes** (exact text to replace)
4. **Priority ordering** (what to fix first)
5. **Auto-fix availability** (YES/NO for each issue)

Never:

- Claim something is wrong without evidence
- Provide vague suggestions ("update docs")
- Skip severity assessment
- Omit actionable fixes

---

**This skill transforms documentation validation from structural checking to semantic understanding, catching issues humans miss.**
