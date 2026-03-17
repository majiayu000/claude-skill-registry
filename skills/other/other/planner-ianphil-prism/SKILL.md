---
name: planner
description: This skill should be used when the user asks to "plan a feature", "create feature plan", "start planning", "new feature", or wants comprehensive planning with analysis, spec, research, design, and TDD task breakdown.
---

# Feature Planning Session

Create a comprehensive feature planning artifact for: **$ARGUMENTS**

This planning session follows the Feature Planning Methodology documented in `aidocs/feature-planning-methodology.md`.

## Session Initialization

### Step 1: Determine Feature ID

Run this command to find the next feature number:

```bash
{ ls backlog/plans/ 2>/dev/null; ls backlog/plans/_completed/ 2>/dev/null; } | grep -E '^[0-9]{3}' | sort -r | head -1
```

The Feature ID format is `{NNN}-{slug}` where:
- `NNN` = 3-digit sequential number (001, 002, 003...)
- `slug` = lowercase, hyphenated descriptor (2-4 words)

### Step 2: Create Branch and Folder Structure

```bash
git checkout -b feature/{NNN}-{slug}
mkdir -p backlog/plans/{NNN}-{slug}/contracts
```

**Note**: When feature is complete, move folder to `backlog/plans/_completed/{NNN}-{slug}/`

### Step 3: Create Planning Artifacts

Create all artifacts in sequence using templates from `references/templates.md`.

---

## Planning Phases

### Phase 1: Analysis (`analysis.md`)

**Goal**: Understand the problem space, existing code, and patterns.

Key sections:
- Executive Summary with pattern/integration mapping
- Architecture Comparison (current vs target)
- Pattern Mapping from existing codebase
- What Exists vs What's Needed
- Key Insights (what works, gaps/limitations)

### Phase 2: Specification (`spec.md`)

**Goal**: Define requirements from user perspectives.

Key sections:
- Problem Statement and Solution Summary
- User Stories with Acceptance Criteria
- Functional Requirements (FR-1, FR-2, etc.)
- Non-Functional Requirements (performance, security)
- Scope (in/out/future)
- Success Criteria, Assumptions, Risks

### Phase 3: Research (`research.md`)

**Goal**: Validate design against external specifications, APIs, or standards.

Key sections:
- Conformance Analysis against external specs
- Gap identification
- Recommendations (critical, minor, future)

### Phase 4: Design

Create three artifacts:

**4a. Implementation Plan (`plan.md`)**
- Architecture diagrams (ASCII)
- Component responsibilities
- File structure with MODIFY/NEW annotations
- Key design decisions with rationale
- Risk mitigation

**4b. Data Model (`data-model.md`)**
- Entity definitions with fields/types
- Relationships and invariants
- State transitions
- Validation rules

**4c. Contracts (`contracts/`)**
- Interface definitions
- API schemas
- Configuration schemas

### Phase 5: Test Design

**5a. Spec Tests (`specs/tests/{NNN}-{slug}.md`)**

**CRITICAL**: Before writing spec tests, load the spec-tests skill:
```
Skill(skill="all-skills:spec-tests")
```

See `references/spec-tests-guide.md` for detailed writing guidance.

Key principles:
- Tests verified by reading code, not executing
- Intent explains WHY users/business care
- Assertions reference specific files and observable structures

**5b. Task Breakdown (`tasks.md`)**

Organize tasks by phase with TDD workflow:
- `[TEST]` tasks: Write failing tests first
- `[IMPL]` tasks: Implement to pass tests
- `[SPEC]` tasks: Run spec tests at phase boundaries

Include dependency diagram and task summary table.

---

## Session Workflow

### Execution Order

1. **Initialize**: Determine Feature ID, create branch and folders
2. **Phase 1**: Create `analysis.md` - understand problem space
3. **Phase 2**: Create `spec.md` - define requirements
4. **Phase 3**: Create `research.md` - validate against external specs (if applicable)
5. **Phase 4**: Create `plan.md`, `data-model.md`, `contracts/` - design
6. **Phase 5**: Create `specs/tests/{NNN}-{slug}.md` and `tasks.md` - test design
7. **Cleanup**: Remove the corresponding quick plan from `backlog/plans/` (e.g., `backlog/plans/YYYYMMDD-{slug}.md`) since the full planning artifacts supersede it

### Interactive Planning

As work progresses through each phase:
- Read relevant existing code to inform analysis
- Ask clarifying questions about requirements
- Research external APIs/specs as needed
- Validate design decisions with the user

### Output Summary

After completing all phases, summarize:

```
Feature: {NNN}-{slug}
Branch: feature/{NNN}-{slug}

Created Artifacts:
├── backlog/plans/{NNN}-{slug}/
│   ├── analysis.md      ✅
│   ├── spec.md          ✅
│   ├── research.md      ✅
│   ├── plan.md          ✅
│   ├── data-model.md    ✅
│   ├── tasks.md         ✅
│   └── contracts/
│       └── README.md    ✅
└── specs/tests/{NNN}-{slug}.md  ✅

Cleaned Up:
- Removed quick plan: backlog/plans/YYYYMMDD-{slug}.md  🗑️

Next Steps:
1. Review planning artifacts
2. Commit: git add backlog/plans/{NNN}-{slug} specs/tests/{NNN}-{slug}.md && git commit -m "feat: planning for {NNN}-{slug}"
3. Begin implementation: /work-plan {NNN}
4. When complete: mv backlog/plans/{NNN}-{slug} backlog/plans/_completed/
```

---

## Additional Resources

### Reference Files

For detailed templates and guidance, consult:
- **`references/templates.md`** - Full templates for all planning artifacts
- **`references/spec-tests-guide.md`** - Detailed spec test writing guidance

### External References

- [Feature Planning Methodology](../aidocs/feature-planning-methodology.md)
- [Developer Guide](../docs/developer-guide.md)
- [Example: 001-mcp-integration](../backlog/plans/_completed/001-mcp-integration/)
