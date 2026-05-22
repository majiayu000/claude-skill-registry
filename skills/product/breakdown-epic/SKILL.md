---
name: breakdown-epic
description: Break down epics into implementable user stories with acceptance criteria, estimates, dependencies, and sprint groupings. This skill should be used for epic planning and backlog grooming.
acceptance:
  - components_identified: "Major components and sub-features identified from epic"
  - stories_created: "User stories created in proper format with acceptance criteria"
  - estimates_provided: "Story points estimated using complexity/effort/risk"
  - dependencies_mapped: "Dependencies between stories identified and documented"
  - sprints_suggested: "Sprint groupings suggested based on dependencies and priorities"
inputs:
  epic_description:
    type: string
    required: true
    description: "Epic or feature description to break down"
  tech_stack:
    type: array
    required: false
    description: "Technology stack for technical considerations"
outputs:
  story_files:
    type: array
    description: "List of generated story file paths"
  epic_file:
    type: string
    description: "Path to generated epic summary file"
  total_points:
    type: number
    description: "Total story points across all stories"
  story_count:
    type: number
    description: "Number of stories created"
  sprint_count:
    type: number
    description: "Suggested number of sprints"
telemetry:
  emit: "skill.breakdown-epic.completed"
  track:
    - story_count
    - total_points
    - sprint_count
    - priority_distribution
    - dependency_count
    - duration_ms
---

# Breakdown Epic Skill

## Purpose

Transform high-level epics or features into detailed, actionable user stories ready for sprint planning and implementation.

**Core Capabilities:**
- Epic scope analysis and component identification
- User story creation (As a... I want... So that...)
- Story point estimation (complexity/effort/risk)
- Dependency mapping between stories
- Sprint grouping suggestions
- Story and epic file generation

## Prerequisites

- Configuration file (`.claude/config.yaml`) with planning settings
- Epic description (20+ words minimum)
- Story point scale defined (default: Fibonacci 1,2,3,5,8,13,21)

---

## Workflow

### Step 0: Load Configuration and Epic Description

**Action:** Load configuration and parse epic requirements.

**Load config:** Read `.claude/config.yaml` for planning settings (storiesLocation, epicsLocation, defaultVelocity, storyPointScale, techStack)

**Get epic description:** From user input (20+ words minimum), parse scope, business goals, technical requirements

**Prepare directories:** Create stories and epics directories

**See:** `references/templates.md#configuration-format` and `#step-0-configuration-loading` for details

**Halt if:**
- Configuration missing
- Epic description <20 words (too vague)
- Cannot create directories

**See:** `references/epic-analysis-guide.md` for scope analysis

---

### Step 1: Analyze Epic Scope

**Action:** Break down epic into major components and sub-features.

**Identify components:**
1. **Core Features** - What functionality is needed?
2. **User Types** - Who will use this?
3. **Technical Requirements** - What tech/integrations?
4. **Security Requirements** - What needs protection?
5. **Non-Functional Requirements** - Performance, scalability, etc.

**Output:** Epic analysis with major components, sub-features, user types, technical/security requirements, NFRs

**See:** `references/templates.md#step-1-epic-analysis-example` for complete analysis format

**Group by themes:**
- Related features together
- Similar technical complexity
- Common user journeys

**See:** `references/epic-analysis-guide.md` for detailed analysis techniques

---

### Step 2: Create User Stories

**Action:** Convert components into user stories with acceptance criteria.

**Story format:** "As a [user], I want [capability], So that [benefit]" with acceptance criteria, priority, component

**See:** `references/templates.md#step-2-user-story-format` for format and 5 complete examples

**Story quality checks:**
- Clear user perspective
- Specific, testable acceptance criteria (2-5 per story)
- Appropriate priority
- Properly scoped (not too large, not too small)

**See:** `references/story-creation-guide.md` for story writing best practices

---

### Step 3: Estimate Story Points

**Action:** Estimate each story using complexity, effort, and risk.

**Estimation factors:** Complexity (1-5), Effort (1-5), Risk (1-3)

**Calculate:** Story Points = Complexity + Effort + Risk, round to Fibonacci (1, 2, 3, 5, 8, 13, 21)

**See:** `references/templates.md#step-3-estimation-factors-template` for detailed scales and examples

**See:** `references/estimation-guide.md` for detailed estimation techniques

---

### Step 4: Identify Dependencies

**Action:** Map dependencies between stories.

**Dependency types:**

**1. Blocks:** Story A must complete before Story B can start
```
story-auth-001 (Signup) BLOCKS story-auth-003 (Email Verification)
```

**2. Related:** Stories share components but can be done in parallel
```
story-auth-001 (Signup) RELATED story-auth-002 (Login)
```

**Dependency rules:**
- Foundation before features (models before APIs)
- Authentication before authorization
- Core functionality before enhancements
- Infrastructure before applications

**Output:** Dependency graph with BLOCKS/REQUIRES/RELATED relationships, critical path identification

**See:** `references/templates.md#step-4-dependency-examples` for complete graph format

**See:** `references/dependency-mapping-guide.md` for dependency analysis

---

### Step 5: Suggest Sprint Groupings

**Action:** Group stories into sprints based on dependencies, priorities, and velocity.

**Grouping rules:**
1. **Priority first** - P0 stories in early sprints
2. **Dependencies respected** - Blocked stories after blockers
3. **Velocity constraints** - Don't exceed team capacity
4. **Logical grouping** - Related stories together

**Output:** Sprint groupings with story assignments, velocity constraints, dependency respect, logical grouping

**See:** `references/templates.md#step-5-sprint-grouping-example` for complete sprint plan format

---

### Step 6: Generate Story Files and Epic Summary

**Action:** Create story markdown files and epic summary.

**Generate files:** Use bmad-commands write_file for each story and epic summary

**Output:** Story files (complete format with user story, ACs, dependencies, estimation, DoD) and epic summary file

**See:** `references/templates.md#step-6-story-file-format-template` and `#step-6-epic-summary-file-format` for complete structures

---

### Step 7: Present Summary to User

**Action:** Present epic breakdown summary for review.

**Output:** Breakdown complete summary with story count, points, sprints, files, priorities, sprint plan, dependencies

**See:** `references/templates.md#step-7-summary-output-template` for complete format

---

## Output

Return structured JSON with story_files, epic_file, metrics (total_points, story_count, sprint_count), and telemetry

**See:** `references/templates.md#json-output-format` for complete structure

---

## Best Practices

1. **Epic Scope** - Keep epics focused (10-15 stories max)
2. **Story Size** - Target 3-8 points per story (not too large)
3. **Clear ACs** - 2-5 specific, testable acceptance criteria
4. **Priority Discipline** - Not everything can be P0
5. **Dependency Mapping** - Identify blockers early
6. **Velocity Reality** - Don't overcommit sprint capacity

**See:** `references/story-creation-guide.md` for best practices

---

## Routing Guidance

**Use this skill when:**
- Starting new epic or major feature
- During backlog grooming sessions
- Planning multiple sprints ahead
- Breaking down product requirements

**Always use before:**
- sprint-plan skill (sprint planning)
- refine-story skill (detailed story refinement)

**Feeds into:**
- create-task-spec skill (for implementation specs)

---

## Reference Files

Detailed documentation in `references/`:

- **templates.md**: All output formats, config examples, story/epic file templates
- **epic-analysis-guide.md**: Epic scope analysis, component identification
- **story-creation-guide.md**: User story format, acceptance criteria, best practices
- **estimation-guide.md**: Story point estimation techniques
- **dependency-mapping-guide.md**: Dependency types, mapping, sprint grouping

---

*Part of BMAD Enhanced Planning Suite*
