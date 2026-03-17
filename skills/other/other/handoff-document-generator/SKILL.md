---
name: handoff-document-generator
description: Generates standardized agent handoff documents for phase transitions. Ensures critical information is preserved and passed between agents during workflow orchestration. Automates handoff creation to prevent implementation failures from missing context.
---

# Handoff Document Generator Skill

**Purpose**: Automate creation of standardized handoff documents between agents and phases.

**When to Use**: At every phase transition to ensure context preservation.

## Why Handoffs Matter

**Critical Finding**: 90%+ of implementation failures traced to missing handoff documents.

**Problem**: Agents starting work without context make wrong assumptions.

**Solution**: Mandatory handoff documents at every transition.

## Handoff Types

### 1. Phase → Phase Handoffs
- Requirements → Design
- Design → Implementation
- Implementation → Testing
- Testing → Finalization

### 2. Agent → Agent Handoffs
- business-requirements → functional-spec
- functional-spec → database-designer
- database-designer → backend-developer
- ui-designer → react-developer

## Handoff Template

Location: `/docs/functional-areas/[feature]/new-work/[date]/handoffs/[source]-to-[target]-handoff.md`

```markdown
# Agent Handoff: [Source] → [Target]

**Date**: YYYY-MM-DD HH:MM
**Source Agent**: [agent-name]
**Target Agent**: [agent-name]
**Phase Transition**: [Phase X] → [Phase Y]
**Feature**: [Feature Name]
**Work Type**: Feature|Bug|Hotfix|Docs|Refactor

---

## Executive Summary
[2-3 sentences: What was completed, what's next, critical decisions]

## Completed Work
### Primary Deliverables
- [ ] [Deliverable 1] - Location: /path/to/file
- [ ] [Deliverable 2] - Location: /path/to/file

### Quality Gate Score
- Score: XX/YY (ZZ%)
- Required: AA%
- Status: PASS|FAIL

## Critical Decisions Made
1. **[Decision Topic]**
   - Decision: [What was decided]
   - Rationale: [Why this was chosen]
   - Impact: [Implications for next phase]
   - Alternatives Considered: [What was rejected and why]

## Context for Next Agent
### Must Read
- [ ] File: /path/to/requirements.md
- [ ] File: /path/to/design.md
- [ ] Lessons: /docs/lessons-learned/[agent]-lessons-learned.md

### Key Insights
- [Critical insight 1]
- [Critical insight 2]

### Assumptions Made
- [Assumption 1 - target agent must validate]
- [Assumption 2 - may need adjustment]

## Technical Specifications
### Architecture Decisions
- [ADR or architectural pattern chosen]
- [Technology stack decisions]

### Data Models
```
[Key schemas, types, or data structures]
```

### API Contracts
| Endpoint | Method | Purpose | Status |
|----------|--------|---------|--------|
| /api/... | GET | ... | Designed |

## Dependencies & Blockers
### Dependencies Required
- [ ] [Dependency 1] - Status: Ready|Pending
- [ ] [Dependency 2] - Status: Ready|Pending

### Known Blockers
- [Blocker if any - NONE is valid]

## Security & Privacy
- [Security requirements]
- [Data privacy considerations]
- [Auth/authz requirements]

## Testing Requirements
### Test Cases Needed
- [ ] [Test case 1]
- [ ] [Test case 2]

### Acceptance Criteria
- [ ] [Criteria 1]
- [ ] [Criteria 2]

## Questions for Target Agent
- [ ] [Question needing clarification]
- [ ] [Decision target agent should make]

## Files Created/Modified
| File | Action | Purpose |
|------|--------|---------|
| /path/to/file.md | CREATED | [purpose] |

## Next Steps
1. [Step 1 for target agent]
2. [Step 2 for target agent]
3. [Step 3 for target agent]

## Validation Checklist
- [ ] All deliverables complete
- [ ] Quality gate passed
- [ ] Decisions documented
- [ ] Context provided
- [ ] Dependencies identified
- [ ] Files logged in registry
- [ ] Next steps clear

---

**Target Agent**: Read this entire handoff before starting work. Validate all assumptions.
```

---

## How to Use This Skill

### From Command Line

```bash
# Generate handoff from business requirements to functional spec
bash .claude/skills/handoff-document-generator/execute.sh \
  business-requirements \
  functional-spec \
  user-management \
  Feature

# Generate handoff from functional spec to react developer
bash .claude/skills/handoff-document-generator/execute.sh \
  functional-spec \
  react-developer \
  user-management \
  Feature

# Generate handoff for bug fix
bash .claude/skills/handoff-document-generator/execute.sh \
  backend-developer \
  test-executor \
  api-fixes \
  Bug

# Show help and usage information
bash .claude/skills/handoff-document-generator/execute.sh --help
```

### From Claude Code

```
Use the handoff-document-generator skill to create handoff from [source-agent] to [target-agent] for [feature-name]
```

### Common Usage Patterns

**At phase transition (orchestrator-automated):**
```bash
bash .claude/skills/handoff-document-generator/execute.sh \
  business-requirements \
  functional-spec \
  user-management \
  Feature
```

**From agent (self-service):**
```bash
# Before completing my work, generate handoff for next agent
bash .claude/skills/handoff-document-generator/execute.sh \
  my-role \
  next-agent-role \
  feature-name \
  Feature
```

---

## Usage Examples (Legacy - For Reference)

### From Orchestrator (Automated)
```
Use the handoff-document-generator skill to create handoff from business-requirements to functional-spec
```

### Manual Generation
```bash
# Create handoff document
bash .claude/skills/handoff-document-generator.md \
  business-requirements \
  functional-spec \
  user-management \
  Feature
```

### From Agent (Self-Service)
```
Before completing my work, I'll use the handoff-document-generator skill to create a handoff document for the next agent.
```

## Handoff Scenarios

### Requirements → Design
**Source**: business-requirements
**Target**: functional-spec, database-designer, ui-designer
**Critical Context**: User stories, business rules, success metrics
**Decisions**: Feature scope, user roles affected, priority

### Design → Implementation
**Source**: functional-spec, database-designer, ui-designer
**Target**: react-developer, backend-developer
**Critical Context**: Architecture, data models, API contracts
**Decisions**: Tech stack, component structure, database schema

### Implementation → Testing
**Source**: react-developer, backend-developer
**Target**: test-executor
**Critical Context**: What was implemented, where, how to test
**Decisions**: Test approach, fixtures needed, edge cases

### Testing → Finalization
**Source**: test-executor
**Target**: librarian, git-manager
**Critical Context**: Test results, coverage, blockers
**Decisions**: Deployment readiness, rollback plan

## Enforcement Rules

### Mandatory Handoffs
**REQUIRED at these transitions:**
- business-requirements → functional-spec (MANDATORY)
- functional-spec → database-designer (if DB changes)
- functional-spec → react-developer (MANDATORY)
- database-designer → backend-developer (MANDATORY)
- ui-designer → react-developer (if new UI)
- backend-developer → test-executor (MANDATORY)
- react-developer → test-executor (MANDATORY)
- test-executor → git-manager (MANDATORY)

### Orchestrator Enforcement
```
Before transitioning from Phase X to Phase Y:
1. Check if handoff exists
2. Verify handoff is complete (no TODO sections)
3. Require target agent to acknowledge reading handoff
4. Block transition if handoff missing
```

## Output Format

```json
{
  "handoff": {
    "source": "business-requirements",
    "target": "functional-spec",
    "feature": "user-management",
    "workType": "Feature",
    "phaseTransition": "Phase 1 → Phase 2",
    "file": "/docs/functional-areas/.../handoffs/business-requirements-to-functional-spec-handoff.md",
    "status": "created",
    "todoSectionsRemaining": 8,
    "complete": false
  },
  "nextSteps": [
    "business-requirements agent: Complete all TODO sections",
    "Run phase-1-validator to get quality gate score",
    "functional-spec agent: Read handoff before starting"
  ]
}
```

## Common Issues

### Issue: Handoff Not Created
**Symptom**: Agent completes work but creates no handoff
**Impact**: Next agent starts with zero context
**Solution**: Orchestrator must REQUIRE handoff creation

### Issue: Incomplete Handoff
**Symptom**: TODO sections not filled in
**Impact**: Next agent has template but no real information
**Solution**: Phase validators check for complete handoffs

### Issue: Handoff Not Read
**Symptom**: Target agent asks questions already answered in handoff
**Impact**: Wasted time, repeated mistakes
**Solution**: Require agents to acknowledge reading handoff

## Integration with Lessons Learned

**Handoffs are NOT lessons learned:**
- Handoffs = Context for THIS feature NOW
- Lessons = Patterns for FUTURE features ALWAYS

**When to promote handoff content to lessons:**
- Decision pattern used repeatedly
- Common pitfall discovered
- Successful approach worth standardizing

## Progressive Disclosure

**Initial Context**: Show handoff location and whether it exists
**On Request**: Generate template with TODOs
**On Completion**: Show next agent what to read
**On Failure**: Show which sections are incomplete

---

**Remember**: Handoff documents are the memory system for multi-agent workflows. Without them, agents work in isolation and fail. With them, agents build on each other's work successfully.
