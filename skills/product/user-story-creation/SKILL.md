---
name: user-story-creation
description: Guide user story creation using the standard template. User stories contain acceptance criteria, agent assignments, and technical details. Use when BA agent extracts stories from PRD, creates new stories, or validates story structure.
owner: business-analyst-agent
---

# User Story Creation Skill

**Purpose:** Guide user story creation following the standard template
**Trigger:** When BA agent extracts stories from PRD or creates new user stories
**Output:** Well-structured user stories ready for execution planning

---

## Template Reference

**ALWAYS read the template before creating user stories:**

```
templates/user-story-template.md
```

The template contains required frontmatter, story format, acceptance criteria structure, technical details sections, and Definition of Done checklist.

---

## Workflow

1. **Read template:** Load `templates/user-story-template.md`
2. **Gather inputs:** Read PRD, identify epic boundaries, review existing stories
3. **Draft sections:** Story statement, acceptance criteria, files to create/modify
4. **Assign agent:** Use full subagent_type paths (see `/skill agent-selection`)
5. **Validate:** Run checklist below, fix any issues
6. **Save:** Write to `{epicFolder}/user-stories/{app}-{epic}-{NNN}-{desc}.md`

---

## File Naming Convention

**Epic folder:** `docs/epics/{app}-{epic}-{description}/`
**Story file:** `{app}-{epic}-{NNN}-{description}.md`

| Component | Format              | Example       |
| --------- | ------------------- | ------------- |
| app       | 3 letters lowercase | msm, crm, api |
| epic      | 3 letters lowercase | wkr, aut, prh |
| NNN       | 3-digit number      | 001, 002, 015 |
| desc      | kebab-case          | create-skill  |

**Epic folder example:** `docs/epics/msm-wkr-workflow-refactor/`
**Story file example:** `msm-wkr-007-create-user-story-creation-skill.md`

---

## Frontmatter Requirements

| Field        | Format                               | Example                            |
| ------------ | ------------------------------------ | ---------------------------------- |
| story_id     | `{app}-{epic}-{NNN}`                 | `msm-wkr-007`                      |
| epic_id      | `{app}-{epic}`                       | `msm-wkr`                          |
| title        | Brief description                    | `Create user-story-creation-skill` |
| status       | pending/in-progress/complete/blocked | `pending`                          |
| complexity   | 1-10 score                           | `3`                                |
| wave         | Wave number (0 if unassigned)        | `2`                                |
| agent        | Full subagent_type                   | `core-claude-plugin:generic:coder` |
| dependencies | Story ID array                       | `["MSM-WKR-001"]`                  |
| created      | YYYY-MM-DD                           | `2024-12-29`                       |
| updated      | YYYY-MM-DD                           | `2024-12-29`                       |

**Agent format:** `{plugin}:{category}:{agent-name}` or `{plugin}:{category}:{subcategory}:{agent-name}`

---

## Agent Name Validation

Before writing story, validate agent assignment against known agent patterns.

### Valid Agent Patterns

| Pattern                                       | Example                                             |
| --------------------------------------------- | --------------------------------------------------- |
| `core-claude-plugin:generic:{name}`           | `core-claude-plugin:generic:coder`                  |
| `core-claude-plugin:domain:{domain}:{name}`   | `core-claude-plugin:domain:backend:api-dev`         |
| `core-claude-plugin:config:{category}:{name}` | `core-claude-plugin:config:build-tools:vite-config` |

### Validation Process

1. **Read story agent field** from frontmatter
2. **Check against patterns above** - must match one of the three formats
3. **If invalid:** Return error with suggestion
   - `backend-dev` → suggest `core-claude-plugin:generic:backend-dev`
   - `coder` → suggest `core-claude-plugin:generic:coder`
   - `vite-config` → suggest `core-claude-plugin:config:build-tools:vite-config`
4. **If valid:** Continue story creation

### Common Invalid Names

| Invalid Name   | Suggested Correction                      |
| -------------- | ----------------------------------------- |
| `backend-dev`  | `core-claude-plugin:generic:backend-dev`  |
| `frontend-dev` | `core-claude-plugin:generic:frontend-dev` |
| `coder`        | `core-claude-plugin:generic:coder`        |
| `skill-author` | `core-claude-plugin:generic:skill-author` |
| `agent-author` | `core-claude-plugin:generic:agent-author` |

**Reference:** Use `/skill agent-selection` to find valid agent names for specific task types.

---

## Story Format

```markdown
**As a** {role/persona}
**I want** {feature/capability}
**So that** {benefit/value}
```

| Component | Guidance                                 |
| --------- | ---------------------------------------- |
| Role      | Who benefits (user, developer, BA agent) |
| Want      | Specific capability or feature           |
| So that   | Business value or outcome                |

---

## Acceptance Criteria Guidelines

| Rule                | Example                                    |
| ------------------- | ------------------------------------------ |
| Be specific         | "API returns 200 status" not "API works"   |
| Be testable         | "File exists at path X" not "File created" |
| Include edge cases  | "Handles empty input gracefully"           |
| Reference artifacts | "Matches schema in template.md"            |

---

## Validation Checklist

### Frontmatter

- [ ] `story_id` present (format: `{app}-{epic}-{NNN}` e.g., `msm-wkr-007`)
- [ ] `epic_id`, `title`, `status`, `complexity`, `wave` present
- [ ] `agent` present with full subagent_type path
- [ ] `dependencies` array present (empty `[]` if none)
- [ ] `created` and `updated` dates present (YYYY-MM-DD)

### User Story Statement

- [ ] "As a" specifies clear role/persona
- [ ] "I want" describes specific capability
- [ ] "So that" explains business value

### Acceptance Criteria

- [ ] At least 3 testable/measurable criteria defined
- [ ] Criteria use checkbox format `- [ ]`
- [ ] Edge cases considered

### Technical Details

- [ ] Location section identifies repo and package
- [ ] Files to Create/Modify tables populated (if applicable)
- [ ] Implementation notes provide guidance

### File Naming

- [ ] Filename matches pattern: `{app}-{epic}-{NNN}-{desc}.md`
- [ ] Filename matches story_id in frontmatter

---

## Example

**Input:** PRD requires "Create user-story-creation skill"

**Process:**

1. BA reads template from `templates/user-story-template.md`
2. BA drafts frontmatter with `story_id: msm-wkr-007`, `agent: core-claude-plugin:generic:skill-author`
3. BA writes story: "As a BA agent, I want a user-story-creation skill..."
4. BA validates against checklist
5. BA saves to `docs/epics/msm-wkr-workflow-refactor/user-stories/msm-wkr-007-create-user-story-creation-skill.md`

**Output:** Complete user story ready for wave assignment

---

## Validation Gate

After all stories are written, spawn reviewer for mandatory quality gate:

**Spawn:** `core-claude-plugin:generic:reviewer`
**Input:** Stories folder path, validation type `user-story`
**Expected Output:**

```json
{
  "result": "PASS" | "FAIL",
  "issues": []
}
```

| Result | Action                                                      |
| ------ | ----------------------------------------------------------- |
| PASS   | Continue to execution-plan-creation phase                   |
| FAIL   | Return issues to business-analyst, fix stories, re-validate |

**Validation Loop:**

1. Reviewer checks all stories against checklist criteria
2. On FAIL: Issues array contains specific story IDs and problems
3. BA agent fixes affected stories only
4. Re-spawn reviewer until PASS received
5. On PASS: Phase transition allowed

---

## Integration

**Called by:** requirements-phase, business-analyst agent, /build command
**Calls:** Read tool (for template), Write tool (for saving)
**References:**

- `/skill prd-creation` - PRD context (previous step)
- `/skill agent-selection` - Agent assignment guidance
- `/skill execution-plan-creation` - Wave planning (next step)
