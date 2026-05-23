---
name: planning
description: >
  Generate and optimize PRDs, Implementation Plans, and Progress Tracking
  documents optimized as AI artifacts for development agents. Use when
  creating new feature plans, breaking down long planning docs (>800 lines),
  or setting up progress tracking. Supports: 1) Create PRD from feature
  request, 2) Create Implementation Plan from PRD with phase breakdown and
  subagent assignments, 3) Optimize existing plans by breaking into
  phase-specific files, 4) Create progress tracking with task assignments.
  Example: "Create a PRD for user authentication feature" or "Break down the
  sidebar-polish implementation plan into phase files" or "Create progress
  tracking for data-layer-fixes PRD".
---

# Planning Skill

## About This Skill

The Planning Skill generates and optimizes Product Requirements Documents (PRDs) and Implementation Plans as AI artifacts - file-based context caches optimized for AI agent consumption rather than human reading.

### Purpose

- Generate comprehensive PRDs from feature requests following MP template
- Create phased Implementation Plans with subagent task assignments
- Optimize existing planning docs by breaking into token-efficient files
- Set up progress tracking structures for multi-phase implementations

### Key Benefits

- **Token Efficiency**: Max ~800 lines per file for optimal AI context loading
- **Progressive Disclosure**: Summary → Detail pattern with linked files
- **Subagent Integration**: Automatic task assignment to appropriate specialists
- **MP Architecture Compliance**: Plans follow layered architecture (routers → services → repositories → DB)
- **Structured Tracking**: One progress file per phase following CLAUDE.md policy

### When to Use This Skill

- Creating PRDs for new features or enhancements
- Generating detailed implementation plans from PRDs
- Breaking down long planning documents (>800 lines) into manageable files
- Setting up progress tracking for multi-phase work
- Optimizing existing plans for better AI agent consumption

## Quick Start

### Create PRD from Feature Request

```bash
# User provides feature description
User: "Create a PRD for advanced filtering on the prompts page"

# Skill generates PRD at:
# docs/project_plans/PRDs/[category]/advanced-filtering-v1.md
```

### Create Implementation Plan from PRD

```bash
# Provide PRD path
User: "Create implementation plan for docs/project_plans/PRDs/harden-polish/advanced-filtering-v1.md"

# Skill generates:
# - Main plan: docs/project_plans/implementation_plans/harden-polish/advanced-filtering-v1.md
# - Phase files (if needed): docs/project_plans/implementation_plans/harden-polish/advanced-filtering-v1/phase-[N]-[name].md
```

### Optimize Existing Plan

```bash
# Provide existing plan path
User: "Optimize docs/project_plans/implementation_plans/harden-polish/sidebar-polish-v1.md"

# Skill:
# 1. Analyzes plan length (e.g., 1200 lines)
# 2. Breaks into phase-specific files (~400 lines each)
# 3. Updates parent plan with links to phase files
```

### Create Progress Tracking

```bash
# Provide PRD or Implementation Plan
User: "Create progress tracking for data-layer-fixes PRD"

# Skill generates:
# .claude/progress/[feature-name]/all-phases-progress.md
# With task breakdown, subagent assignments, completion tracking
```

## Core Workflows

### Workflow 1: Create PRD from Feature Request

**Input**: Feature description or request from user

**Process**:

1. **Analyze Request**
   - Extract feature name, scope, goals
   - Identify related systems and components
   - Determine priority and complexity

2. **Structure PRD**
   - Use template: `./templates/prd-template.md`
   - Follow MP architecture patterns (see `./references/mp-architecture.md`)
   - Include frontmatter with proper metadata
   - Organize into standard PRD sections

3. **Add Implementation Context**
   - Break into phased approach
   - Identify architectural layers involved
   - Note dependencies and risks
   - Define success criteria and acceptance tests

4. **Determine Location**
   - Category: `docs/project_plans/PRDs/[category]/`
   - Categories: `harden-polish`, `features`, `enhancements`, `refactors`
   - Naming: `[feature-name]-v1.md` (kebab-case)

5. **Generate File**
   - Write PRD to determined location
   - Include YAML frontmatter with metadata
   - Link to related docs (ADRs, guides, etc.)
   - Add to project tracking if needed

**Output**:
- PRD file at: `docs/project_plans/PRDs/[category]/[feature-name]-v1.md`
- Follows template structure
- Ready for implementation planning

**Example**:

```markdown
Input: "Add real-time collaboration features to prompt editing"

Output Location: docs/project_plans/PRDs/features/realtime-collaboration-v1.md

Sections:
1. Executive Summary - Real-time collaborative editing
2. Context & Background - Current single-user editing limitations
3. Problem Statement - Users can't collaborate on prompts
4. Goals & Success Metrics - Multiple concurrent editors, conflict resolution
5. Requirements - WebSocket connections, operational transforms, presence indicators
6. Implementation Phases - Phase 1: Backend infrastructure, Phase 2: Frontend integration
... (full PRD structure)
```

### Workflow 2: Create Implementation Plan from PRD

**Input**: Path to existing PRD or newly created PRD

**Process**:

1. **Analyze PRD**
   - Read full PRD content
   - Extract key requirements
   - Identify architectural layers needed
   - Determine phase breakdown strategy

2. **Plan Phase Structure**
   - Follow MP layered architecture: routers → services → repositories → DB
   - Group related tasks into phases
   - Common phases: Database → Repository → Service → API → UI → Testing → Docs → Deployment
   - Consider parallel work opportunities
   - Identify critical path

3. **Generate Task Breakdown**
   - Use template: `./templates/implementation-plan-template.md`
   - Create tasks for each phase
   - Format: Task tables with ID, Name, Description, Acceptance Criteria, Estimate
   - Include quality gates for each phase

4. **Assign Subagents**
   - Use reference: `./references/subagent-assignments.md`
   - Assign based on task type:
     - Database: `data-layer-expert`
     - Backend API: `python-backend-engineer`, `backend-architect`
     - Frontend: `ui-engineer-enhanced`, `frontend-developer`
     - UI Components: `ui-designer`, `ui-engineer`
     - Testing: appropriate testing agents
     - Docs: `documentation-writer`, `documentation-complex`
   - Add to each task: "Assigned Subagent(s): agent-1, agent-2"

5. **Optimize for Token Efficiency**
   - If total plan >800 lines: break into phase-specific files
   - Pattern: `[feature-name]-v1/phase-[N]-[name].md`
   - Parent plan links to phase files
   - Each phase file <800 lines
   - See `./references/optimization-patterns.md`

6. **Generate Files**
   - Main plan: `docs/project_plans/implementation_plans/[category]/[feature-name]-v1.md`
   - Phase files (if needed): `docs/project_plans/implementation_plans/[category]/[feature-name]-v1/phase-[N]-[name].md`
   - Link phase files from parent plan

**Output**:
- Implementation Plan at determined location
- Phase breakdown with subagent assignments
- Linked phase files if plan >800 lines
- Quality gates and success criteria per phase

**Example**:

```markdown
Input PRD: docs/project_plans/PRDs/features/realtime-collaboration-v1.md

Output:
Main Plan: docs/project_plans/implementation_plans/features/realtime-collaboration-v1.md

Phase Breakdown:
- Phase 1: Database Layer (websocket_sessions, edit_locks tables) - data-layer-expert
- Phase 2: Repository Layer (session management, lock management) - python-backend-engineer
- Phase 3: Service Layer (operational transforms, conflict resolution) - backend-architect
- Phase 4: API Layer (WebSocket endpoints, presence API) - python-backend-engineer
- Phase 5: UI Layer (collaborative editor, presence indicators) - ui-engineer-enhanced, frontend-developer
- Phase 6: Testing (unit, integration, E2E conflict scenarios) - testing agents
- Phase 7: Documentation (API docs, user guides) - documentation-writer
- Phase 8: Deployment (feature flags, monitoring) - DevOps

Phase Files (if plan >800 lines):
- realtime-collaboration-v1/phase-1-database.md
- realtime-collaboration-v1/phase-2-repository.md
- realtime-collaboration-v1/phase-3-5-backend.md (grouped related phases)
- realtime-collaboration-v1/phase-6-8-validation.md (grouped related phases)
```

### Workflow 3: Optimize Existing Plans

**Input**: Path to existing PRD or Implementation Plan that's >800 lines

**Process**:

1. **Analyze Plan**
   - Read full plan
   - Count total lines
   - Identify natural break points (phases, sections)
   - Determine optimal split strategy

2. **Determine Breakout Strategy**
   - Primary: Break by phase (most common)
   - Secondary: Break by domain (backend vs frontend)
   - Tertiary: Break by task type (implementation vs testing)
   - Goal: Each file <800 lines, logically cohesive

3. **Create Breakout Files**
   - Pattern: `[plan-name]/phase-[N]-[name].md`
   - Alternative: `[plan-name]/[domain]-tasks.md`
   - Each file includes:
     - Phase/section overview
     - Relevant tasks with subagent assignments
     - Quality gates for that section
     - Links back to parent plan

4. **Update Parent Plan**
   - Add table of contents linking to breakout files
   - Keep executive summary and overview in parent
   - Replace detailed sections with links:
     ```markdown
     ## Phase 2: Repository Layer
     See [Phase 2 Implementation Details](./[plan-name]/phase-2-repository.md)
     ```
   - Maintain quality gates summary in parent

5. **Validate Optimization**
   - Each file <800 lines ✓
   - All content preserved ✓
   - Links work correctly ✓
   - Logical grouping maintained ✓
   - Progressive disclosure achieved ✓

**Output**:
- Optimized parent plan (summary + links)
- Breakout files for detailed content
- Improved token efficiency (95%+ reduction in single-load context)

**Example**:

```markdown
Input: docs/project_plans/implementation_plans/harden-polish/sidebar-polish-v1.md (1200 lines)

Analysis:
- 8 phases, ~150 lines each
- Can group related phases: 1-3 (backend), 4-5 (frontend), 6-8 (validation)

Output:
Parent: sidebar-polish-v1.md (200 lines - summary + links)
Phase Files:
- sidebar-polish-v1/phase-1-3-backend.md (450 lines)
- sidebar-polish-v1/phase-4-5-frontend.md (400 lines)
- sidebar-polish-v1/phase-6-8-validation.md (350 lines)

Token Efficiency:
- Before: Load 1200 lines for any query
- After: Load 200-line summary, then specific phase (450 max) = 67% reduction
```

### Workflow 4: Create Progress Tracking

**Input**: PRD or Implementation Plan

**Process**:

Utilize artifact-tracking skill to create progress tracking and context artifacts per the skill instructions.

You should NOT create these files from this skill, as there are specific optimizations and structures required by the artifact-tracking skill.

## Templates Reference

### prd-template.md

**Location**: `./templates/prd-template.md`

**Based On**: `/docs/docs-v2/templates/PRD-TEMPLATE.md`

**Purpose**: Standard PRD structure for MeatyPrompts features

**Key Sections**:
- Feature Brief & Metadata (name, date, author, related docs)
- Executive Summary (1-2 paragraphs)
- Context & Background (problem space, current state)
- Problem Statement (clear gap or pain point)
- Goals & Success Metrics (measurable outcomes)
- Requirements (functional and non-functional)
- Scope (in-scope vs out-of-scope)
- Dependencies & Assumptions
- Risks & Mitigations
- Target State (post-implementation)
- Acceptance Criteria (definition of done)
- Implementation (phased breakdown with tasks)

**When to Use**: Creating any new PRD

### implementation-plan-template.md

**Location**: `./templates/implementation-plan-template.md`

**Based On**: `/claude-export/templates/pm/implementation-plan-template.md`

**Purpose**: Detailed phased implementation with task breakdown

**Key Sections**:
- Executive Summary (approach, milestones, success criteria)
- Implementation Strategy (architecture sequence, parallel work, critical path)
- Phase Breakdown (8 standard phases with task tables)
- Risk Mitigation (technical and schedule risks)
- Resource Requirements (team composition, skills, infrastructure)
- Success Metrics (delivery, business, technical)
- Communication Plan (status reporting, escalation)
- Post-Implementation Plan (monitoring, maintenance)

**When to Use**: Creating implementation plan from PRD

### phase-breakdown-template.md

**Location**: `./templates/phase-breakdown-template.md`

**Purpose**: Template for individual phase files when breaking up long plans

**Key Sections**:
- Phase overview (duration, dependencies, team)
- Task breakdown table (ID, name, description, acceptance criteria, estimate, assignee)
- Subagent assignments
- Quality gates
- Key files and integration points
- Link back to parent plan

**When to Use**: Breaking long implementation plans into phase-specific files

## Scripts Reference

All scripts are in `./scripts/` directory and use Node.js (NOT Python).

### generate-prd.sh

**Purpose**: Generate PRD from feature request

**Usage**:
```bash
./scripts/generate-prd.sh "Feature description" "category"
```

**Process**:
1. Parse feature description
2. Determine category and filename
3. Load PRD template
4. Generate PRD content
5. Write to `docs/project_plans/PRDs/[category]/[feature-name]-v1.md`

**Output**: PRD file path

### generate-impl-plan.sh

**Purpose**: Generate implementation plan from PRD

**Usage**:
```bash
./scripts/generate-impl-plan.sh "path/to/prd.md"
```

**Process**:
1. Read PRD content
2. Extract requirements and phases
3. Generate task breakdown
4. Add subagent assignments
5. Determine if plan needs breakout (>800 lines)
6. Write main plan and phase files

**Output**: Implementation plan file path(s)

### optimize-plan.sh

**Purpose**: Break long plan into phase-specific files

**Usage**:
```bash
./scripts/optimize-plan.sh "path/to/plan.md"
```

**Process**:
1. Read plan and count lines
2. Determine optimal breakout strategy
3. Create phase-specific files
4. Update parent plan with links
5. Validate all content preserved

**Output**: List of created phase files

## References

### subagent-assignments.md

**Location**: `./references/subagent-assignments.md`
**Purpose**: Mapping of task types to appropriate subagents
**Used By**: Implementation planning, progress tracking creation

### file-structure.md

**Location**: `./references/file-structure.md`
**Purpose**: Directory structure conventions for plans and progress
**Naming Conventions**:
- PRDs: `[feature-name]-v1.md` (kebab-case)
- Implementation Plans: `[feature-name]-v1.md`
- Phase Files: `phase-[N]-[name].md` or `phase-[N]-[M]-[name].md` (grouped)
**Used By**: File creation, optimization

### optimization-patterns.md

**Location**: `./references/optimization-patterns.md`

**Purpose**: Patterns for breaking up long files into token-efficient chunks

**Content**:

**Pattern 1: Break by Phase** (Most Common)
- Split implementation plan by phase (1-3, 4-5, 6-8)
- Each phase file <800 lines
- Parent links to phase files
- Progressive disclosure: Load summary, then specific phase

**Pattern 2: Break by Domain**
- Backend phases (Database, Repository, Service, API)
- Frontend phases (UI, Components, State)
- Validation phases (Testing, Docs, Deployment)

**Pattern 3: Break by Task Type**
- Implementation tasks
- Testing tasks
- Documentation tasks
- Deployment tasks

**Pattern 4: Keep Together**
- Always keep in parent plan:
  - Executive summary
  - Phase overview table
  - Risk mitigation summary
  - Success metrics overview
- Move to phase files:
  - Detailed task breakdowns
  - Specific acceptance criteria
  - Technical implementation notes

**Token Efficiency Gains**:
- Before: Load entire 1200-line plan
- After: Load 200-line summary + 400-line phase = 50% reduction
- For targeted queries: Load only relevant phase = 67%+ reduction

**Used By**: Plan optimization workflow

## Best Practices

### File Size Management

**Guideline**: No file should exceed ~800 lines

**Rationale**:
- Optimal token efficiency for AI context loading
- Enables progressive disclosure pattern
- Reduces cognitive load for agents
- Faster file parsing and analysis

**Strategies**:
1. Break plans by phase when >800 lines
2. Group short related phases (1-3, 4-5)
3. Keep summaries in parent, details in phase files
4. Use links for cross-references

### Naming Conventions

**PRDs**: `[feature-name]-v1.md`
- Use kebab-case (lowercase with hyphens)
- Include version number (-v1, -v2)
- Descriptive name (e.g., `advanced-filtering-v1.md`)

**Implementation Plans**: `[feature-name]-v1.md`
- Match PRD naming
- Same category as PRD
- Version synchronized with PRD

**Phase Files**: `phase-[N]-[name].md`
- Sequential numbering (phase-1, phase-2)
- Can group: `phase-1-3-backend.md`
- Descriptive name (database, repository, frontend)

### Directory Organization

**PRDs**:
- `docs/project_plans/PRDs/[category]/`
- Categories: `harden-polish`, `features`, `enhancements`, `refactors`

**Implementation Plans**:
- `docs/project_plans/implementation_plans/[category]/`
- Match PRD category
- Phase breakouts in subdirectory: `[plan-name]/`

### Token Efficiency Tips

**Progressive Disclosure**:
1. Summary in parent plan (200 lines)
2. Link to detailed phase files (400 lines each)
3. Agent loads summary first, then specific phase as needed
4. 50-67% token reduction

**Structured References**:
- Link to ADRs instead of duplicating architecture info
- Reference existing docs rather than repeating
- Use relative paths for phase file links

**Chunk by Logical Units**:
- Keep related tasks together
- Don't split mid-phase
- Group short phases if logical
- Maintain quality gates with phases

### YAML Frontmatter

**PRDs**:
```yaml
---
title: "Feature Name - PRD"
description: "Brief summary (1-2 sentences)"
audience: [ai-agents, developers]
tags: [relevant, tags, for, search]
created: 2025-11-11
updated: 2025-11-11
category: "product-planning"
status: draft|published
related:
  - /docs/architecture/ADRs/relevant-adr.md
  - /docs/guides/relevant-guide.md
---
```

**Implementation Plans**:
```yaml
---
title: "Feature Name - Implementation Plan"
description: "Brief summary of implementation approach"
audience: [ai-agents, developers]
tags: [implementation, planning, phases]
created: 2025-11-11
updated: 2025-11-11
category: "product-planning"
status: draft|in-progress|published
related:
  - /docs/project_plans/PRDs/category/feature-name-v1.md
---
```

## Examples

### Example 1: Create PRD for Advanced Filtering

**Input**:
```
User: "Create a PRD for adding advanced filtering to the prompts page. Users need to filter by multiple criteria: model, provider, date range, tags, and favorites."
```

**Process**:
1. Extract feature name: "Advanced Filtering"
2. Determine category: "features"
3. Generate PRD using template
4. Structure sections:
   - Problem: Users can only filter by single criteria
   - Goals: Multi-criteria filtering, saved filter sets
   - Requirements: UI for filter builder, backend filter query support
   - Phases: Phase 1 (Backend), Phase 2 (Frontend), Phase 3 (Saved Filters)

**Output**:
```
File: docs/project_plans/PRDs/features/advanced-filtering-v1.md

# Advanced Filtering - PRD

**Feature Name**: Advanced Filtering
**Date**: 2025-11-11
**Author**: Claude (Sonnet 4.5)
**Related**: Filtering guides, search ADRs

## 1. Executive Summary
Enable users to filter prompts by multiple criteria simultaneously (model, provider, date range, tags, favorites) with the ability to save and reuse filter sets.

## 2. Context & Background
Current filtering supports single criteria only. Users frequently need to filter by combinations (e.g., "OpenAI models from last week tagged 'production'").

... (full PRD structure)
```

### Example 2: Create Implementation Plan with Phase Breakout

**Input**:
```
User: "Create implementation plan for docs/project_plans/PRDs/features/advanced-filtering-v1.md"
```

**Process**:
1. Read PRD, extract requirements
2. Plan 7 phases following MP architecture
3. Generate task breakdown with estimates
4. Assign subagents to each task
5. Calculate total: 1100 lines → needs breakout
6. Create phase files:
   - phase-1-3-backend.md (500 lines)
   - phase-4-5-frontend.md (400 lines)
   - phase-6-7-validation.md (300 lines)
7. Update parent plan with links (200 lines)

**Output**:
```
Main Plan: docs/project_plans/implementation_plans/features/advanced-filtering-v1.md (200 lines)

# Implementation Plan: Advanced Filtering

## Phase Overview
| Phase | Title | Effort | Files |
|-------|-------|--------|-------|
| 1-3 | Backend Implementation | 18 pts | [Details](./advanced-filtering-v1/phase-1-3-backend.md) |
| 4-5 | Frontend Implementation | 12 pts | [Details](./advanced-filtering-v1/phase-4-5-frontend.md) |
| 6-7 | Validation & Deployment | 8 pts | [Details](./advanced-filtering-v1/phase-6-7-validation.md) |

... (executive summary, strategy)

---

Phase Files Created:
- advanced-filtering-v1/phase-1-3-backend.md (500 lines)
  - Phase 1: Database (filter_sets table, indexes)
  - Phase 2: Repository (query builder, filter sets repo)
  - Phase 3: Service (filter validation, DTO mapping)

- advanced-filtering-v1/phase-4-5-frontend.md (400 lines)
  - Phase 4: API (filter endpoints, saved sets API)
  - Phase 5: UI (filter builder component, saved sets UI)

- advanced-filtering-v1/phase-6-7-validation.md (300 lines)
  - Phase 6: Testing (unit, integration, E2E)
  - Phase 7: Deployment (feature flags, monitoring)
```

### Example 3: Optimize Existing Long Plan

**Input**:
```
User: "Optimize docs/project_plans/implementation_plans/harden-polish/sidebar-polish-v1.md - it's 1200 lines"
```

**Process**:
1. Read plan: 8 phases, ~150 lines each
2. Determine breakout: Group 1-3 (backend), 4-5 (frontend), 6-8 (validation)
3. Create phase files:
   - phase-1-3-backend.md (450 lines)
   - phase-4-5-frontend.md (400 lines)
   - phase-6-8-validation.md (350 lines)
4. Update parent plan: Keep summary, add links to phase files (200 lines)

**Output**:
```
Updated: docs/project_plans/implementation_plans/harden-polish/sidebar-polish-v1.md (200 lines)

Created Phase Files:
- sidebar-polish-v1/phase-1-3-backend.md (450 lines)
  Phase 1: Database - Sidebar state, user preferences
  Phase 2: Repository - State management, RLS
  Phase 3: Service - Preference sync, DTOs

- sidebar-polish-v1/phase-4-5-frontend.md (400 lines)
  Phase 4: API - Endpoints for sidebar state
  Phase 5: UI - Sidebar component, animations

- sidebar-polish-v1/phase-6-8-validation.md (350 lines)
  Phase 6: Testing - Unit, integration, visual
  Phase 7: Documentation - Component docs, API docs
  Phase 8: Deployment - Feature flags, rollout

Token Efficiency: 67% reduction for targeted queries
```

## Integration with Project Standards

### Architecture Compliance

All plans follow project layered architecture.

### Subagent Ecosystem

Plans integrate with 50+ project subagents:

**Architecture**: lead-architect, backend-architect, data-layer-expert
**Development**: python-backend-engineer, frontend-developer, ui-engineer-enhanced
**UI/UX**: ui-designer, ux-researcher
**Review**: code-reviewer, task-completion-validator
**Documentation**: documentation-writer, documentation-complex
**Testing**: testing specialists
**Performance**: react-performance-optimizer, web-accessibility-checker

### Documentation Policy

Follows CLAUDE.md documentation policy:
- PRDs are product-planning docs (allowed)
- Implementation Plans are product-planning docs (allowed)
- NO reports, summaries, etc unless explicitly requested

### File Organization

**PRDs**: `/docs/project_plans/PRDs/[category]/[feature-name]-v1.md`
**Plans**: `/docs/project_plans/implementation_plans/[category]/[feature-name]-v1.md`
**Phase Files**: `[plan-name]/phase-[N]-[name].md`

## Advanced Usage

### Customizing Templates

Edit templates in `./templates/` to match project needs:

1. **PRD Template Customization**:
   - Add project-specific sections
   - Adjust success metrics format
   - Include standard acceptance criteria

2. **Implementation Plan Template Customization**:
   - Add/remove phases
   - Adjust quality gates
   - Customize risk categories

3. **Progress Tracking Template Customization**:
   - Add project-specific status values
   - Adjust completion tracking format
   - Include team-specific metadata

### Multi-PRD Planning

For complex initiatives spanning multiple PRDs:

1. Create parent epic document
2. Generate individual PRDs for each component
3. Link PRDs to parent epic
4. Create unified progress tracking across PRDs

### Spike Integration

For research-heavy features:

1. Create SPIKE document first (using spike-writer agent)
2. Use SPIKE to inform PRD generation
3. Reference SPIKE in PRD "Context & Background"
4. Link SPIKE from Implementation Plan

### Continuous Optimization

Regularly optimize plans as work progresses:

1. Update progress tracking with actual completion
2. Adjust estimates based on learnings
3. Break out new sections if plan grows >800 lines
4. Archive completed phases

## Related Skills

- **artifact-tracking**: Create progress tracking and context artifacts
- **skill-builder**: Create new custom skills
- **symbols**: Token-efficient codebase indexing
- **codebase-explorer**: Fast pattern discovery
- **explore**: Deep codebase analysis

## Related Agents

- **lead-pm**: SDLC orchestration
- **prd-writer**: PRD creation
- **implementation-planner**: Detailed implementation planning
- **task-decomposition-expert**: Task breakdown
- **lead-architect**: Architecture planning assistance, task delegation
- **documentation-writer**: Documentation for plans

## Version History

- **2025-11-11**: Initial skill creation
  - 4 core workflows (PRD, Plan, Optimize, Progress)
  - 4 templates (PRD, Plan, Progress, Phase)
  - 5 scripts (generate-prd, generate-impl-plan, optimize-plan, assign-subagents, create-progress-tracking)
  - 4 references (architecture, subagents, file-structure, optimization-patterns)
- **2025-12-01**: Remove Tracking Creation from this skill; delegate to artifact-tracking skill
