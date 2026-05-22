---
name: writing-specs
description: Complete spec workflow - generates Run ID, creates isolated worktree, brainstorms requirements, writes lean spec documents that reference constitutions, validates architecture quality, and reports completion
---

# Writing Specifications

## Overview

A **specification** defines WHAT to build and WHY. It is NOT an implementation plan.

**Core principle:** Reference constitutions, link to docs, keep it lean. The `/plan` command handles task decomposition.

**Spec = Requirements + Architecture**
**Plan = Tasks + Dependencies**

## When to Use

Use this skill when:
- Invoked from `/spectacular:spec` slash command
- Creating a new feature specification from scratch
- Need the complete spec workflow (Run ID, worktree, brainstorm, spec, validation)

Do NOT use for:
- Implementation plans with task breakdown - Use `/spectacular:plan` instead
- API documentation - Goes in code comments or separate docs
- Runbooks or operational guides - Different document type

**Announce:** "I'm using the writing-specs skill to create a feature specification."

## Workspace Detection

Before starting the spec workflow, detect the workspace mode:

```bash
# Detect workspace mode
REPO_COUNT=$(find . -maxdepth 2 -name ".git" -type d 2>/dev/null | wc -l | tr -d ' ')
if [ "$REPO_COUNT" -gt 1 ]; then
  echo "Multi-repo workspace detected ($REPO_COUNT repos)"
  WORKSPACE_MODE="multi-repo"
  WORKSPACE_ROOT=$(pwd)
  # List detected repos
  find . -maxdepth 2 -name ".git" -type d | xargs -I{} dirname {} | sed 's|^\./||'
else
  echo "Single-repo mode"
  WORKSPACE_MODE="single-repo"
fi
```

**Single-repo mode (current behavior):**
- Specs stored in `specs/{runId}-{feature}/spec.md` at repo root
- Worktree created at `.worktrees/{runId}-main/`
- Constitution referenced from `@docs/constitutions/current/`

**Multi-repo mode (new behavior):**
- Specs stored in `./specs/{runId}-{feature}/spec.md` at WORKSPACE root
- NO worktree created (specs live at workspace level, not inside any repo)
- Each repo's constitution referenced separately

## Constitution Adherence

**All specifications MUST follow**: @docs/constitutions/current/
- architecture.md - Layer boundaries, project structure
- patterns.md - Mandatory patterns (next-safe-action, ts-pattern, etc.)
- schema-rules.md - Database design philosophy
- tech-stack.md - Approved libraries and versions
- testing.md - Testing requirements

## The Process

### Step 0: Generate Run ID

**First action**: Generate a unique run identifier for this spec.

```bash
# Generate 6-char hash from feature name + timestamp
TIMESTAMP=$(date +%s)
RUN_ID=$(echo "{feature-description}-$TIMESTAMP" | shasum -a 256 | head -c 6)
echo "RUN_ID: $RUN_ID"
```

**CRITICAL**: Execute this entire block as a single multi-line Bash tool call. The comment on the first line is REQUIRED - without it, command substitution `$(...)` causes parse errors.

**Store for use in:**
- Spec directory name: `specs/{run-id}-{feature-slug}/`
- Spec frontmatter metadata
- Plan generation
- Branch naming during execution

**Announce:** "Generated RUN_ID: {run-id} for tracking this spec run"

### Step 0.5: Create Isolated Worktree

**Announce:** "Creating isolated worktree for this spec run..."

**Multi-repo mode:** Skip worktree creation. Specs live at workspace root, not inside any repo.

```bash
if [ "$WORKSPACE_MODE" = "multi-repo" ]; then
  echo "Multi-repo mode: Specs stored at workspace root, no worktree needed"
  mkdir -p specs/${RUN_ID}-${FEATURE_SLUG}
  # Skip to Step 1 (brainstorming)
fi
```

**Single-repo mode:** Continue with worktree creation as normal.

**Create worktree for isolated development:**

1. **Create branch using git-spice**:
   - Use `using-git-spice` skill to create branch `{runId}-main` from current branch
   - Branch name format: `{runId}-main` (e.g., `abc123-main`)

2. **Create worktree**:
   ```bash
   # Create worktree at .worktrees/{runId}-main/
   git worktree add .worktrees/${RUN_ID}-main ${RUN_ID}-main
   ```

3. **Error handling**:
   - If worktree already exists: "Worktree {runId}-main already exists. Remove it first with `git worktree remove .worktrees/{runId}-main` or use a different feature name."
   - If worktree creation fails: Report the git error details and exit

**Working directory context:**
- All subsequent file operations happen in `.worktrees/{runId}-main/`
- Brainstorming and spec generation occur in the worktree context
- Main repository working directory remains unchanged

**Announce:** "Worktree created at .worktrees/{runId}-main/ - all work will happen in isolation"

### Step 0.6: Install Dependencies in Worktree

**REQUIRED**: Each worktree needs dependencies installed before work begins.

1. **Check CLAUDE.md for setup commands**:

   Look for this pattern in the project's CLAUDE.md:
   ```markdown
   ## Development Commands

   ### Setup

   - **install**: `bun install`
   - **postinstall**: `npx prisma generate`
   ```

2. **If setup commands found, run installation**:

   ```bash
   # Navigate to worktree
   cd .worktrees/${RUN_ID}-main

   # Check if dependencies already installed (handles resume)
   if [ ! -d node_modules ]; then
     echo "Installing dependencies..."
     {install-command}  # From CLAUDE.md (e.g., bun install)

     # Run postinstall if defined
     if [ -n "{postinstall-command}" ]; then
       echo "Running postinstall (codegen)..."
       {postinstall-command}  # From CLAUDE.md (e.g., npx prisma generate)
     fi
   else
     echo "Dependencies already installed"
   fi
   ```

3. **If setup commands NOT found in CLAUDE.md**:

   **Error and instruct user**:
   ```markdown
   Setup Commands Required

   Worktrees need dependencies installed to run quality checks and codegen.

   Please add to your project's CLAUDE.md:

   ## Development Commands

   ### Setup

   - **install**: `bun install` (or npm install, pnpm install, etc.)
   - **postinstall**: `npx prisma generate` (optional - for codegen)

   Then re-run: /spectacular:spec {feature-description}
   ```

**Announce:** "Dependencies installed in worktree - ready for spec generation"

### Step 1: Brainstorm Requirements

**Context:** All brainstorming happens in the context of the worktree (`.worktrees/{runId}-main/`)

**Announce:** "I'm brainstorming the design using Phases 1-3 (Understanding, Exploration, Design Presentation)."

**Create TodoWrite checklist:**

```
Brainstorming for Spec:
- [ ] Phase 1: Understanding (purpose, constraints, criteria)
- [ ] Phase 2: Exploration (2-3 approaches proposed)
- [ ] Phase 3: Design Presentation (design validated)
- [ ] Proceed to Step 2: Generate Specification
```

#### Phase 1: Understanding

**Goal:** Clarify scope, constraints, and success criteria.

1. Check current project state in working directory (note: we're in the worktree)
2. Read @docs/constitutions/current/ to understand constraints:
   - architecture.md - Layer boundaries
   - patterns.md - Mandatory patterns
   - tech-stack.md - Approved libraries
   - schema-rules.md - Database rules
3. Ask ONE question at a time to refine the idea
4. Use AskUserQuestion tool for multiple choice options
5. Gather: Purpose, constraints, success criteria

**Constitution compliance:**
- All architectural decisions must follow @docs/constitutions/current/architecture.md
- All pattern choices must follow @docs/constitutions/current/patterns.md
- All library selections must follow @docs/constitutions/current/tech-stack.md

#### Phase 2: Exploration

**Goal:** Propose and evaluate 2-3 architectural approaches.

1. Propose 2-3 different approaches that follow constitutional constraints
2. For each approach explain:
   - Core architecture (layers, patterns)
   - Trade-offs (complexity vs features)
   - Constitution compliance (which patterns used)
3. Use AskUserQuestion tool to present approaches as structured choices
4. Ask partner which approach resonates

#### Phase 3: Design Presentation

**Goal:** Present detailed design incrementally and validate.

1. Present design in 200-300 word sections
2. Cover: Architecture, components, data flow, error handling, testing
3. After each section ask: "Does this look right so far?" (open-ended)
4. Use open-ended questions for freeform feedback
5. Adjust design based on feedback

**After Phase 3:** Mark TodoWrite complete and proceed immediately to Step 2.

### Step 2: Generate Specification

**Announce:** "Generating the specification document..."

**Task:**
- Feature: {feature-description}
- Design context: {summary from brainstorming}
- RUN_ID: {run-id from Step 0}
- Output location: `.worktrees/{run-id}-main/specs/{run-id}-{feature-slug}/spec.md`
- **Constitution**: All design decisions must follow @docs/constitutions/current/
- Analyze codebase for task-specific context:
  - Existing files to modify
  - New files to create (with exact paths per @docs/constitutions/current/architecture.md)
  - Dependencies needed (must be in @docs/constitutions/current/tech-stack.md)
  - Schema changes required (following @docs/constitutions/current/schema-rules.md)
- Follow all Iron Laws (see below):
  - Reference constitutions, don't duplicate
  - Link to SDK docs, don't embed examples
  - No implementation plans (that's `/spectacular:plan`'s job)
  - Keep it lean (<300 lines)

**Spec frontmatter must include:**
```yaml
---
runId: {run-id}
feature: {feature-slug}
created: {date}
status: draft
---
```

**Use the Spec Structure template below to generate the document.**

### Step 2.5: Commit Spec to Worktree

**After spec generation completes, commit the spec to the worktree branch:**

```bash
cd .worktrees/${RUN_ID}-main
git add specs/
git commit -m "spec: add ${feature-slug} specification [${RUN_ID}]"
```

**Announce:** "Spec committed to {runId}-main branch in worktree"

### Step 3: Architecture Quality Validation

**CRITICAL**: Before reporting completion, validate the spec against architecture quality standards.

**Announce:** "Validating spec against architecture quality standards..."

Read the generated spec and check against these dimensions:

#### 3.1 Constitution Compliance
- [ ] **Architecture**: All components follow layer boundaries (@docs/constitutions/current/architecture.md)
  - Models - Services - Actions - UI (no layer violations)
  - Server/Client component boundaries respected
- [ ] **Patterns**: All mandatory patterns referenced (@docs/constitutions/current/patterns.md)
  - next-safe-action for server actions
  - ts-pattern for discriminated unions
  - Zod schemas for validation
  - routes.ts for navigation
- [ ] **Schema**: Database design follows rules (@docs/constitutions/current/schema-rules.md)
  - Proper indexing strategy
  - Naming conventions
  - Relationship patterns
- [ ] **Tech Stack**: All dependencies approved (@docs/constitutions/current/tech-stack.md)
  - No unapproved libraries
  - Correct versions specified
- [ ] **Testing**: Testing strategy defined (@docs/constitutions/current/testing.md)

#### 3.2 Specification Quality (Iron Laws)
- [ ] **No Duplication**: Constitution rules referenced, not recreated
- [ ] **No Code Examples**: External docs linked, not embedded
- [ ] **No Implementation Plans**: Focus on WHAT/WHY, not HOW/WHEN
- [ ] **Lean**: Spec < 300 lines (if longer, likely duplicating constitutions)

#### 3.3 Requirements Quality
- [ ] **Completeness**: All FRs and NFRs defined, no missing scenarios
- [ ] **Clarity**: All requirements unambiguous and specific (no "fast", "good", "better")
- [ ] **Measurability**: All requirements have testable acceptance criteria
- [ ] **Consistency**: No conflicts between sections
- [ ] **Edge Cases**: Boundary conditions and error handling addressed
- [ ] **Dependencies**: External dependencies and assumptions documented

#### 3.4 Architecture Traceability
- [ ] **File Paths**: All new/modified files have exact paths per architecture.md
- [ ] **Integration Points**: How feature integrates with existing system clear
- [ ] **Migration Impact**: Schema changes and data migrations identified
- [ ] **Security**: Auth/authz requirements explicit

#### 3.5 Surface Issues

If ANY checks fail, create `.worktrees/{run-id}-main/specs/{run-id}-{feature-slug}/clarifications.md` with:

```markdown
# Clarifications Needed

## [Category: Constitution/Quality/Requirements/Architecture]

**Issue**: {What's wrong}
**Location**: {Spec section reference}
**Severity**: [BLOCKER/CRITICAL/MINOR]
**Question**: {What needs to be resolved}

Options:
- A: {Option with trade-offs}
- B: {Option with trade-offs}
- Custom: {User provides alternative}
```

**Iteration limit**: Maximum 3 validation cycles. If issues remain after 3 iterations, escalate to user with clarifications.md.

### Step 4: Report Completion

**IMPORTANT**: After reporting completion, **STOP HERE**. Do not proceed to plan generation automatically. The user must review the spec and explicitly run `/spectacular:plan` when ready.

After validation passes OR clarifications documented, report to user:

**If validation passed (single-repo mode):**
```
Feature Specification Complete & Validated

RUN_ID: {run-id}
Worktree: .worktrees/{run-id}-main/
Branch: {run-id}-main
Location: .worktrees/{run-id}-main/specs/{run-id}-{feature-slug}/spec.md

Constitution Compliance: PASS
Architecture Quality: PASS
Requirements Quality: PASS

Note: Spec is in isolated worktree, main repo unchanged.

Next Steps (User Actions - DO NOT AUTO-EXECUTE):
1. Review the spec: .worktrees/{run-id}-main/specs/{run-id}-{feature-slug}/spec.md
2. When ready, create implementation plan: /spectacular:plan @.worktrees/{run-id}-main/specs/{run-id}-{feature-slug}/spec.md
```

**If validation passed (multi-repo mode):**
```
Feature Specification Complete & Validated

RUN_ID: {run-id}
Workspace: {workspace-root}
Location: specs/{run-id}-{feature-slug}/spec.md

Repos affected:
- backend: @backend/docs/constitutions/current/
- frontend: @frontend/docs/constitutions/current/

Constitution Compliance: PASS
Architecture Quality: PASS
Requirements Quality: PASS

Note: Spec is at workspace root, affecting multiple repos.

Next Steps (User Actions - DO NOT AUTO-EXECUTE):
1. Review the spec: specs/{run-id}-{feature-slug}/spec.md
2. When ready, create plan: /spectacular:plan @specs/{run-id}-{feature-slug}/spec.md
```

**If clarifications needed (single-repo mode):**
```
Feature Specification Complete - Clarifications Needed

RUN_ID: {run-id}
Worktree: .worktrees/{run-id}-main/
Branch: {run-id}-main
Location: .worktrees/{run-id}-main/specs/{run-id}-{feature-slug}/spec.md
Clarifications: .worktrees/{run-id}-main/specs/{run-id}-{feature-slug}/clarifications.md

Note: Spec is in isolated worktree, main repo unchanged.

Next Steps:
1. Review spec: .worktrees/{run-id}-main/specs/{run-id}-{feature-slug}/spec.md
2. Answer clarifications: .worktrees/{run-id}-main/specs/{run-id}-{feature-slug}/clarifications.md
3. Once resolved, re-run: /spectacular:spec {feature-description}
```

**If clarifications needed (multi-repo mode):**
```
Feature Specification Complete - Clarifications Needed

RUN_ID: {run-id}
Workspace: {workspace-root}
Location: specs/{run-id}-{feature-slug}/spec.md
Clarifications: specs/{run-id}-{feature-slug}/clarifications.md

Repos affected:
- backend: @backend/docs/constitutions/current/
- frontend: @frontend/docs/constitutions/current/

Note: Spec is at workspace root, affecting multiple repos.

Next Steps:
1. Review spec: specs/{run-id}-{feature-slug}/spec.md
2. Answer clarifications: specs/{run-id}-{feature-slug}/clarifications.md
3. Once resolved, re-run: /spectacular:spec {feature-description}
```

---

## Spec Structure

```markdown
# Feature: {Feature Name}

**Status**: Draft
**Created**: {date}

## Problem Statement

**Current State:**
{What exists today and what's missing/broken}

**Desired State:**
{What we want to achieve}

**Gap:**
{Specific problem this feature solves}

## Requirements

> **Note**: All features must follow @docs/constitutions/current/

### Functional Requirements
- FR1: {specific requirement}
- FR2: {specific requirement}

### Non-Functional Requirements
- NFR1: {performance/security/DX requirement}
- NFR2: {performance/security/DX requirement}

## Architecture

> **Layer boundaries**: @docs/constitutions/current/architecture.md
> **Required patterns**: @docs/constitutions/current/patterns.md

### Components

**New Files:**
- `src/lib/models/{name}.ts` - {purpose}
- `src/lib/services/{name}-service.ts` - {purpose}
- `src/lib/actions/{name}-actions.ts` - {purpose}

**Modified Files:**
- `{path}` - {what changes}

### Dependencies

**New packages:**
- `{package}` - {purpose}
- See: {link to official docs}

**Schema changes:**
- {migration name} - {purpose}
- Rules: @docs/constitutions/current/schema-rules.md

### Integration Points

- Auth: Uses existing Auth.js setup
- Database: Prisma client per @docs/constitutions/current/tech-stack.md
- Validation: Zod schemas per @docs/constitutions/current/patterns.md

## Acceptance Criteria

**Constitution compliance:**
- [ ] All patterns followed (@docs/constitutions/current/patterns.md)
- [ ] Architecture boundaries respected (@docs/constitutions/current/architecture.md)
- [ ] Testing requirements met (@docs/constitutions/current/testing.md)

**Feature-specific:**
- [ ] {criterion for this feature}
- [ ] {criterion for this feature}
- [ ] {criterion for this feature}

**Verification:**
- [ ] All tests pass
- [ ] Linting passes
- [ ] Feature works end-to-end

## Open Questions

{List any unresolved questions or decisions needed}

## References

- Architecture: @docs/constitutions/current/architecture.md
- Patterns: @docs/constitutions/current/patterns.md
- Schema Rules: @docs/constitutions/current/schema-rules.md
- Tech Stack: @docs/constitutions/current/tech-stack.md
- Testing: @docs/constitutions/current/testing.md
- {External SDK}: {link to official docs}
```

### Multi-Repo Spec Template Addition

For multi-repo features, add this section to the spec:

```markdown
## Constitutions

This feature must comply with constitutions from each affected repo:

**backend**: @backend/docs/constitutions/current/
- architecture.md - Backend layer boundaries
- patterns.md - Backend patterns (next-safe-action, etc.)
- schema-rules.md - Database design rules

**frontend**: @frontend/docs/constitutions/current/
- architecture.md - Frontend component structure
- patterns.md - Frontend patterns (React Query, etc.)

**shared-lib**: @shared-lib/docs/constitutions/current/
- (if applicable)
```

When brainstorming in multi-repo mode:
- Read constitutions from ALL relevant repos
- Note which repo each architectural decision applies to
- Ensure cross-repo consistency (e.g., API contracts)

## Iron Laws

### 1. Reference, Don't Duplicate

**NEVER recreate constitution rules in the spec**

<Bad>
```markdown
## Layered Architecture

The architecture has three layers:
- Models: Data access with Prisma
- Services: Business logic
- Actions: Input validation with Zod
```
</Bad>

<Good>
```markdown
## Architecture

> **Layer boundaries**: @docs/constitutions/current/architecture.md

Components follow the established 3-layer pattern.
```
</Good>

### 2. Link to Docs, Don't Embed Examples

**NEVER include code examples from external libraries**

<Bad>
```markdown
### Zod Validation

```typescript
import { z } from 'zod';

export const schema = z.object({
  name: z.string().min(3),
  email: z.string().email()
});
```
```
</Bad>

<Good>
```markdown
### Validation

Use Zod schemas per @docs/constitutions/current/patterns.md

See: https://zod.dev for object schema syntax
```
</Good>

### 3. No Implementation Plans

**NEVER include task breakdown or migration phases**

<Bad>
```markdown
## Migration Plan

### Phase 1: Database Schema
1. Create Prisma migration
2. Run migration
3. Verify indexes

### Phase 2: Backend Implementation
...
```
</Bad>

<Good>
```markdown
## Dependencies

**Schema changes:**
- Migration: `init_rooms` - Add Room, RoomParticipant, WaitingListEntry models

Implementation order determined by `/plan` command.
```
</Good>

### 4. No Success Metrics

**NEVER include adoption metrics, performance targets, or measurement strategies**

<Bad>
```markdown
## Success Metrics

1. Adoption: 80% of users use feature within first month
2. Performance: Page loads in <500ms
3. Engagement: <5% churn rate
```
</Bad>

<Good>
```markdown
## Non-Functional Requirements

- NFR1: Page load performance <500ms (measured per @docs/constitutions/current/testing.md)
- NFR2: Support 1000 concurrent users
```
</Good>

## Common Mistakes

| Mistake | Why It's Wrong | Fix |
|---------|---------------|-----|
| Including full Prisma schemas | Duplicates what goes in code | List model names + purposes, reference schema-rules.md |
| Writing test code examples | Shows HOW not WHAT | List what to test, reference testing.md for how |
| Explaining ts-pattern syntax | Already in patterns.md | Reference patterns.md, list where pattern applies |
| Creating `/notes` subdirectory | Violates single-file principle | Keep spec lean, remove supporting docs |
| Adding timeline estimates | That's project management | Focus on requirements and architecture |

## Rationalization Table

| Excuse | Reality |
|--------|---------|
| "Thorough means showing complete code" | Thorough = complete requirements. Code = implementation. |
| "Spec needs examples so people understand" | Link to docs. Don't copy-paste library examples. |
| "Migration plan shows full picture" | `/plan` command handles decomposition. Spec = WHAT not HOW. |
| "Include constitutions for context" | Constitutions exist to avoid duplication. Reference, don't recreate. |
| "Testing code shows approach" | testing.md shows approach. Spec lists WHAT to test. |
| "Metrics demonstrate value" | NFRs show requirements. Metrics = measurement strategy (different doc). |
| "More detail = more helpful" | More detail = harder to maintain. Lean + links = durable. |

## Red Flags - STOP and Fix

Seeing any of these? Delete and reference instead:

- Full code examples from libraries (Zod, Prisma, Socket.io, etc.)
- Migration phases or implementation steps
- Success metrics or adoption targets
- Recreated architecture explanations
- Test implementation code
- Files in `specs/{run-id}-{feature-slug}/notes/` directory
- Spec > 300 lines (probably duplicating constitutions)

**All of these mean: Too much implementation detail. Focus on WHAT not HOW.**

## Quality Checklist

Before finalizing spec:

- [ ] Problem statement shows current - desired state gap
- [ ] All FRs and NFRs are testable/verifiable
- [ ] Architecture section lists files (not code examples)
- [ ] All constitution rules referenced (not recreated)
- [ ] All external libraries linked to docs (not copied)
- [ ] No implementation plan (saved for `/spectacular:plan`)
- [ ] No success metrics or timelines
- [ ] Single file at `specs/{run-id}-{feature-slug}/spec.md`
- [ ] Spec < 300 lines (if longer, check for duplication)

## Error Handling

### Worktree Creation Fails
- Check `.worktrees/` is in `.gitignore`
- Run `git worktree prune` to clean stale entries
- Verify working directory is clean

### Git-Spice Errors
- Run `gs repo init` to initialize repository
- Check `gs ls` to view current stack
- See `using-git-spice` skill for troubleshooting

### Setup Commands Missing
- Project MUST define setup commands in CLAUDE.md
- See error message for required format
- Re-run spec command after adding commands

### Validation Failures
- Maximum 3 iteration cycles
- If issues persist, escalate via clarifications.md
- Do not skip validation - it catches real problems

## The Bottom Line

**Specs define WHAT and WHY. Plans define HOW and WHEN.**

Reference heavily. Link to docs. Keep it lean.

If you're copy-pasting code or recreating rules, you're writing the wrong document.
