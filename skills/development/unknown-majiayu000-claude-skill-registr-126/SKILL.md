---
name: plan
description: "Create PLAN.md file with phase-based breakdown for issues. Use after creating an issue with /issue to break down work into phases."
model: claude-opus-4-5-20251101
allowed-tools: Read, Write, Edit, Glob, Grep
---

# /plan

Create PLAN.md with phase-based breakdown for tasks, spikes, and bugs.

## Usage

```bash
/plan 001                    # Create plan for issue 001 (auto-detect project)
/plan 001 --project coordinatr  # Explicit project
/plan SPIKE-003              # Plan for a spike (creates exploration plans)
/plan 003 --second-opinion   # Get peer review from Gemini CLI before finalizing
```

## Issue Type Detection

| Issue Type | Plan Structure | File Created |
|------------|---------------|--------------|
| Task (TASK.md) | Sequential phases with checkpoints | PLAN.md |
| Bug (BUG.md) | Investigation → Fix phases | PLAN.md |
| Spike (SPIKE.md) | Exploration phases per approach | PLAN-1.md, PLAN-2.md, ... |

## Execution Flow

### For Task/Bug

1. **Load Context**:
   ```bash
   Read: ideas/[project]/issues/###-*/TASK.md (or BUG.md)
   Read: spaces/[project]/docs/specs/*.md (if implements: field exists)
   Glob: spaces/[project]/docs/adrs/ADR-*.md
   Glob: resources/research/*.md
   ```

   If the issue has an `implements:` field, load that specific spec section:
   ```bash
   Read: spaces/[project]/docs/specs/required-features.md  # Extract relevant section
   ```

2. **Cross-Project Pattern Search**:
   ```bash
   # Search other projects for similar implementations
   Grep: spaces/*/src/ for relevant patterns
   ```

   Include relevant references in plan:
   ```markdown
   ## Related Implementations

   Found similar patterns in other projects:
   - `spaces/yourbench/src/auth/clerk.ts` - Clerk auth setup
   - `spaces/coordinatr/src/lib/session.ts` - Session handling
   ```

3. **Library Documentation** (automatic for integrations):

   **MANDATORY when task involves:**
   - Installing/configuring external libraries or SDKs
   - Framework integrations (auth providers, databases, APIs)
   - Third-party services (Clerk, Stripe, AWS services, etc.)

   **Process:**
   ```bash
   # 1. Resolve library ID
   mcp__context7__resolve-library-id: {libraryName}

   # 2. Fetch current documentation
   mcp__context7__query-docs: {context7CompatibleLibraryID}

   # 3. Search for recent patterns/best practices
   WebSearch: "{library} {framework} integration 2026"
   ```

   **Document findings:**
   ```markdown
   ## Library Documentation Validation

   **{Library Name}** (validated YYYY-MM-DD):
   - Current version: X.Y.Z
   - Key integration patterns: [summary]
   - Recommended approach: [based on current docs]
   ```

4. **Generate Plan**:
   - Break work into logical phases
   - Each phase has clear deliverables
   - Include checkpoints between phases
   - Add "Done When" criteria

5. **Write PLAN.md**:
   - Present phases, estimated effort, dependencies
   - Include "Library Documentation Validation" section (if applicable)
   - Include "Second Opinion Analysis" section (if requested)

6. **Commit Suggestion**:
   - Ask: "Commit PLAN.md to ideas repo? (yes/no)"

### For Spike (Exploration)

1. **Load Context**: Read SPIKE.md (questions, success criteria, time box)

2. **Gather Approaches**:
   - Ask: "How many approaches to explore?" → N
   - For each: "Describe approach N?"

3. **Generate**: Create PLAN-N.md for each approach

4. **Commit Suggestion**: Ask to commit all plan files

## Task Plan Example

```markdown
# Implementation Plan: 001 Research Auth Patterns

## Overview
Research authentication patterns for Coordinatr's multi-tenant architecture.

## Phase 1: Survey Existing Solutions

### 1.1 - Research Auth Libraries
- [ ] Review Better Auth documentation
- [ ] Compare with Auth.js and Lucia
- [ ] Document trade-offs

### 1.2 - Multi-Tenant Patterns
- [ ] Research team-based auth patterns
- [ ] Review how Slack, Linear handle it
- [ ] [CHECKPOINT] Summary document complete

## Phase 2: Architecture Proposal

### 2.1 - Draft Architecture
- [ ] Create architecture diagram
- [ ] Document token strategy
- [ ] Define permission model

### 2.2 - Review
- [ ] Self-critique against requirements
- [ ] [CHECKPOINT] Architecture doc complete

## Done When
- [ ] Auth library recommendation documented
- [ ] Architecture proposal in ideas/coordinatr/docs/
- [ ] Trade-offs and risks identified
```

## Second Opinion Feature

**What**: Optional peer review from Gemini CLI before finalizing plans.

**Usage**: Pass `--second-opinion` flag to trigger Gemini review with Context7 validation.

**Process**:
1. Send plan to Gemini CLI for review
2. Validate each recommendation against Context7 docs
3. Claude makes final decision on each:
   - ✅ **ACCEPT**: Recommendation validated AND improves plan
   - ⚠️ **MODIFY**: Good idea but needs adjustment
   - ❌ **REJECT**: Invalid or not applicable
4. Document all decisions in "Second Opinion Analysis" section

**Requirements**:
- Gemini CLI installed and functional
- `--second-opinion` flag explicitly passed

**Graceful degradation**: If Gemini unavailable, proceeds with Claude-only plan.

## Workflow

```
/spec → /issue → /plan {ID} → (work phases) → /complete {ID}
                    ↓
          Load spec section from implements: field
```

**Creates:**
- Task/Bug: `ideas/{project}/issues/###-*/PLAN.md`
- Spike: `ideas/{project}/issues/###-*/PLAN-1.md`, `PLAN-2.md`, etc.
