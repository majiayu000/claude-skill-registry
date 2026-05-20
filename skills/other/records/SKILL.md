# Record 039: User Stories Skill

## Status

Designed

---

## Problem

When using `/design` (Step 4: User Stories) or writing stories manually, there's no built-in guidance for story quality. During Record 038 (Agent Teams), an external agile-product-owner skill was used ad-hoc. The user story writing patterns (INVEST, Given-When-Then) should be available as a built-in skill.

## Solution

Add a focused `user-stories` skill (command type) that covers:

- User Story Templates (As a/I want/So that)
- Story Types (Feature, Improvement, Bug Fix, Enabler)
- Persona Reference
- INVEST Criteria Validation
- Acceptance Criteria with Given-When-Then patterns
- AC Checklist (Happy Path, Validation, Error Handling, Performance, Accessibility)
- Minimum Criteria by Story Size

No sprint planning, velocity tracking, or epic breakdown (out of scope).

### /design Integration

The `/design` command loads this skill automatically in Step 4 (User Stories) if installed. Instruction added to `commands/design.md`:

> If user-stories skill is installed (`~/.claude/skills/user-stories/SKILL.md` exists), read it before this step. Apply INVEST criteria and Given-When-Then acceptance criteria patterns.

### Attribution

Source: [agile-product-owner](https://github.com/alirezarezvani/claude-skills/tree/main/product-team/agile-product-owner) by [alirezarezvani](https://github.com/alirezarezvani) (MIT License). Adapted and reduced to user story focus only.

## User Stories

### Story 1: Create user-stories skill
**As a** Claude Code user
**I want** a built-in user stories skill
**So that** I get INVEST-compliant stories with proper acceptance criteria

**Acceptance Criteria:**
- [ ] `skills/user-stories/SKILL.md` exists with correct frontmatter (name, type: command, source, author)
- [ ] Content covers: story template, story types, personas, INVEST, Given-When-Then, AC checklist
- [ ] References section attributes alirezarezvani with link (MIT)
- [ ] No sprint planning, velocity, or epic breakdown content

**Priority:** High

### Story 2: Integrate with /design command
**As a** Claude Code user running `/design`
**I want** user story guidance loaded automatically in Step 4
**So that** stories written during design follow INVEST and Given-When-Then patterns

**Acceptance Criteria:**
- [ ] `commands/design.md` Step 4 includes skill loading instruction
- [ ] Loading is conditional (only if skill is installed)
- [ ] Story capture format in design aligns with skill templates

**Priority:** High

### Story 3: Tests, docs, version bump
**As a** maintainer
**I want** the skill properly tested and documented
**So that** it follows project conventions

**Acceptance Criteria:**
- [ ] Test scenario `tests/scenarios/25-user-stories.sh` (file structure, frontmatter, installation)
- [ ] README.md updated (Tool Skills table)
- [ ] CHANGELOG.md v49 entry
- [ ] `templates/VERSION` incremented to 49
- [ ] README badge updated to v49
- [ ] All existing tests still pass

**Priority:** Medium
