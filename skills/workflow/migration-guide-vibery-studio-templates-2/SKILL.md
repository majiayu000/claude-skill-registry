---
name: migration-guide
description: >
  Generate step-by-step migration guides between tools, frameworks, or workflows.
  Outputs: Phase-by-phase migration plan, compatibility mapping, rollback strategy.
  Use when switching tools, upgrading frameworks, or adopting new workflows.
  Triggers: migrate from X to Y, switch to, upgrade from, moving from, /migrate
---

# Migration Guide

Transform tool/framework switches from risky leaps into controlled, reversible transitions.

## Purpose

Migrations fail when users try to switch everything at once. This skill creates phased migration plans that maintain productivity while transitioning, with rollback options at each phase.

## Migration Categories

```
1. Tool Migration:
   - IDE: Cursor → Claude Code
   - AI: Copilot → Claude
   - Bundler: Webpack → Vite

2. Framework Migration:
   - React → Next.js
   - Express → Fastify
   - REST → GraphQL

3. Workflow Migration:
   - Manual → Automated
   - Monolith → Microservices
   - Local → Cloud

4. Version Migration:
   - Major upgrades (v1 → v2)
   - Breaking changes
   - Deprecation handling
```

---

## Process

### Phase 1: Migration Assessment

#### Entry Check

```
IF user provided: current state + target state + reason
    → Proceed to Phase 2
ELSE
    → Assess migration scope first
```

#### Assessment Questions

| Question                           | Purpose             |
| ---------------------------------- | ------------------- |
| "What are you migrating from?"     | Identify source     |
| "What are you migrating to?"       | Identify target     |
| "Why are you migrating?"           | Validate motivation |
| "What's your timeline?"            | Scope the phases    |
| "Can you run both simultaneously?" | Determine strategy  |

#### Migration Type Detection

```
IF source and target can coexist:
    → Recommend: Parallel Migration (lowest risk)
    → Run both, gradually shift traffic/usage

IF must be atomic swap:
    → Recommend: Big Bang Migration (higher risk)
    → Requires thorough testing, clear rollback

IF partial migration possible:
    → Recommend: Strangler Fig Pattern
    → New features in new system, old stays
```

---

### Phase 2: Compatibility Mapping

#### Entry Check

```
IF migration assessed:
    → Map compatibility
ELSE
    → Return to Phase 1
```

#### Feature Mapping Table

```markdown
## Feature Compatibility

| Feature     | [Source]       | [Target]             | Migration Effort         |
| ----------- | -------------- | -------------------- | ------------------------ |
| [feature 1] | ✓ How it works | ✓ Equivalent         | Low/Med/High             |
| [feature 2] | ✓ How it works | ⚠ Different approach | Med                      |
| [feature 3] | ✓ How it works | ✗ Not available      | High (workaround needed) |
| [feature 4] | ✗ N/A          | ✓ New capability     | Gain                     |
```

#### Breaking Changes Identification

```
FOR each feature in source:
    Compare with target:

    IF identical API/behavior:
        → Mark: Direct migration

    IF different API, same result:
        → Mark: Adaptation needed
        → Document: transformation required

    IF no equivalent:
        → Mark: Blocker or accept loss
        → Document: workaround or alternative
```

#### Dependency Analysis

```
LIST all dependencies:
    - Which work with both?
    - Which need replacement?
    - Which are source-specific?
    - Which are target-specific?

OUTPUT:
| Dependency | Source | Target | Action |
|------------|--------|--------|--------|
| [dep] | v1.x | v2.x | Upgrade |
| [dep] | ✓ | ✗ | Replace with [alt] |
```

---

### Phase 3: Migration Plan Generation

#### Entry Check

```
IF compatibility mapped:
    → Generate phased plan
ELSE
    → Return to Phase 2
```

#### Phase Structure

```markdown
## Migration Plan: [Source] → [Target]

### Phase 0: Preparation (Before Starting)

**Duration:** [estimate]
**Risk:** Low

Actions:

- [ ] Document current configuration
- [ ] Create backup/snapshot
- [ ] Set up target environment
- [ ] Verify team readiness

Rollback: N/A (nothing changed yet)

---

### Phase 1: Parallel Setup

**Duration:** [estimate]
**Risk:** Low

Actions:

- [ ] Install [target] alongside [source]
- [ ] Configure [target] with basic settings
- [ ] Verify [target] works independently
- [ ] Keep using [source] for production work

Rollback: Remove [target], continue with [source]

Success Criteria:

- [Target] runs without errors
- No impact on [source] workflow

---

### Phase 2: Feature Migration

**Duration:** [estimate]
**Risk:** Medium

Actions:

- [ ] Migrate [feature 1] (easiest first)
- [ ] Test [feature 1] in [target]
- [ ] Migrate [feature 2]
- [ ] Test [feature 2] in [target]
- [ ] [Continue for each feature...]

Rollback: Switch back to [source] for migrated features

Success Criteria:

- All migrated features work in [target]
- No data loss or corruption

---

### Phase 3: Workflow Transition

**Duration:** [estimate]
**Risk:** Medium

Actions:

- [ ] Switch primary workflow to [target]
- [ ] Use [source] only for unsupported features
- [ ] Document any gaps or issues
- [ ] Adjust team processes

Rollback: Return to [source] as primary

Success Criteria:

- 80%+ of work done in [target]
- Team comfortable with new workflow

---

### Phase 4: Full Cutover

**Duration:** [estimate]
**Risk:** Low (if previous phases succeeded)

Actions:

- [ ] Disable/uninstall [source]
- [ ] Remove [source] configurations
- [ ] Update documentation
- [ ] Archive [source] backups

Rollback: Reinstall [source] from backup

Success Criteria:

- [Source] fully removed
- No references to [source] in workflow
```

---

### Phase 4: Specific Migration Guides

#### Tool-Specific Templates

##### Cursor → Claude Code Migration

````markdown
## Cursor → Claude Code

### What Changes

| Cursor         | Claude Code        |
| -------------- | ------------------ |
| GUI-based      | Terminal-based     |
| .cursorrules   | CLAUDE.md          |
| Cmd+K          | Direct prompt      |
| Tab completion | Different paradigm |

### Phase 1: Parallel (Keep Both)

1. Install Claude Code: `npm install -g @anthropic-ai/claude-code`
2. Run from project: `claude`
3. Use for multi-file tasks only

### Phase 2: Translate Configuration

Convert .cursorrules to CLAUDE.md:

```markdown
# From .cursorrules

[content]

# To CLAUDE.md

[translated content]
```
````

### Phase 3: Workflow Integration

- Keep Cursor for: Quick edits, tab completion
- Use Claude Code for: Complex tasks, multi-file, planning

### Phase 4: Optional Full Switch

Only if comfortable. Hybrid is valid long-term.

````

##### Copilot → Claude Migration
```markdown
## GitHub Copilot → Claude Code

### Paradigm Shift
- Copilot: Reactive (suggests next line)
- Claude: Agentic (executes full tasks)

### Phase 1: Keep Both
1. Keep Copilot active in IDE
2. Add Claude Code for tasks
3. Use Copilot for: Writing new code
4. Use Claude for: "Do X for me"

### Phase 2: Task Differentiation
````

Small (single line) → Copilot
Medium (function) → Either
Large (multi-file) → Claude Code
Planning → Claude Code (Plan Mode)

```

### Phase 3: Evaluate Value
After 2 weeks:
- Which saves more time?
- Which produces better code?
- TCO comparison

### Phase 4: Decide
- Keep both (common)
- Drop Copilot (if Claude covers needs)
- Drop Claude (if Copilot sufficient)
```

---

### Phase 5: Rollback Strategy

#### Entry Check

```
IF migration plan generated:
    → Add rollback details
ELSE
    → Return to Phase 3
```

#### Rollback Documentation

```markdown
## Rollback Strategy

### Checkpoints

| Phase | Checkpoint     | Rollback Command        |
| ----- | -------------- | ----------------------- |
| 1     | Before install | N/A                     |
| 2     | After config   | Restore [source] config |
| 3     | After workflow | Switch back to [source] |
| 4     | After cutover  | Reinstall [source]      |

### Data Preservation

- Backup location: [path]
- Backup command: [command]
- Restore command: [command]

### Emergency Rollback

If critical failure during migration:

1. Stop current action
2. Run: [rollback command]
3. Verify: [verification steps]
4. Document: What failed and why
```

---

## Self-Check (Read before every response)

□ Did I identify the migration type?
→ Parallel vs Big Bang vs Strangler changes everything

□ Is every phase reversible?
→ No rollback = no safety net

□ Did I map feature compatibility?
→ Surprise gaps kill migrations

□ Are phases small enough?
→ Large phases = large risks

□ Did I include success criteria?
→ "Done" must be measurable

□ Is the timeline realistic?
→ Rushed migrations fail

□ Did I account for team learning curve?
→ New tool = temporary slowdown

---

## Integration with Vibery

```
AFTER migration planned:
    Suggest relevant components:
    - "project-blueprint for new project setup"
    - "workflow-composer to automate new workflows"
    - "[target]-pro agent for learning new tool"
```
