---
name: pm-improvement-self-improvement
description: Systematic improvement of PM agent's own coordination skills during retrospectives
category: improvement
---

# PM Self-Improvement

The PM agent must continuously improve its own coordination capabilities, not just worker agent skills. This skill defines the PM's self-improvement process during the `skill_research` phase.

## When to Use

Use this skill during the `skill_research` phase of each retrospective cycle. The PM must improve at least ONE of its own skills in addition to improving worker agent skills.

## PM Skill Improvement Areas

### 1. Task Selection Algorithms

**Goal**: Improve how the PM selects and assigns tasks from the PRD.

**Areas to Research**:
- Dependency graph analysis for optimal task ordering
- Risk-based task prioritization
- Agent capability matching
- Parallelization opportunities

**Research Sources**:
- BMAD-METHOD orchestration patterns
- Project management algorithms (CPM, PERT)
- Agile task refinement techniques

### 2. Risk Assessment

**Goal**: Better identify and mitigate project risks before they become blockers.

**Areas to Research**:
- Technical debt detection patterns
- Scope creep identification
- Integration risk analysis
- Bottleneck prediction

**Research Sources**:
- Software project risk management frameworks
- Technical debt metrics and quantification
- Dependency analysis tools and techniques

### 3. Stakeholder Communication

**Goal**: More effective coordination patterns between agents and with the human user.

**Areas to Research**:
- Message clarity and precision
- Status reporting granularity
- Expectation management
- Handoff protocols

**Research Sources**:
- Agent coordination protocols (agents.md, agent-skills.md)
- Distributed systems communication patterns
- Agile ceremony facilitation

### 4. Design Integration (GDD-to-PRD)

**Goal**: Better translate Game Design Documents into actionable PRD tasks.

**Areas to Research**:
- Design document parsing and comprehension
- Requirement extraction techniques
- Task decomposition patterns
- Design validation criteria

**Research Sources**:
- GDD creation best practices (Game Designer agent skills)
- Requirements engineering methodology
- User story decomposition techniques

### 5. Retrospective Facilitation

**Goal**: Run more effective retrospectives that generate actionable insights.

**Areas to Research**:
- Facilitation techniques for distributed agents
- Insight extraction patterns
- Action item prioritization
- Continuous improvement frameworks

**Research Sources**:
- Agile retrospective formats
- Kaizen and continuous improvement
- Team dynamics in distributed systems

### 6. Asset Coordination Risk Assessment (NEW - 2026-01-25)

**Goal**: Identify tasks involving external asset packs that require Developer-Tech Artist coordination.

**Areas to Research**:
- Asset pack scale compatibility patterns
- FBX vs GLTF format considerations
- When to involve Tech Artist in Developer tasks

**Risk Indicators** (add to scale-adaptive.md):
- Task mentions "FBX", "asset pack", or external model sources
- Previous tasks had scale-related issues (0.015 vs 0.15 confusion)
- Weapons/items require bone attachment to animated characters

**Research Sources**:
- React Three FBX scale documentation
- Three.js asset scale best practices
- Project retrospective history for asset-related pain points

**Learned from feat-tps-005 and bugfix-tps-001 retrospectives (2026-01-25)**:
- Blaster Kit FBX models require 0.015 scale (not 0.15) - 10x difference
- Asset scale confusion causes repeated rework
- Tasks involving external assets require Tech Artist involvement for scale validation
- PM should flag "asset pack" keywords for multi-agent coordination

### 7. Parallel Bugfix Assignment (NEW - 2026-01-26)

**Goal**: Identify independent bugfixes that can be assigned to multiple agents simultaneously.

**Areas to Research**:
- Task dependency analysis for parallelization opportunities
- Multi-agent coordination for independent bugfixes
- Risk assessment for parallel work

**Parallel Assignment Criteria**:
```markdown
Bugfixes can be parallelized if ALL conditions met:
1. No shared files between bugfixes
2. No dependencies between bugfixes
3. Different agents available (or git worktree support)
4. No integration risk between fixes
```

**Dependency Check Pattern**:
```javascript
// For each bugfix, check:
const filesChanged = bugfix.verificationSteps.filter(s =>
  s.includes('src/') || s.includes('server/')
);

// Compare against other bugfixes
const hasOverlap = (bugfixA, bugfixB) => {
  const filesA = new Set(bugfixA.files);
  const filesB = new Set(bugfixB.files);
  return [...filesA].some(f => filesB.has(f));
};
```

**Learned from retrospective (bugfix-unit-001, bugfix-e2e-001, bugfix-e2e-002, 2026-01-26)**:
- bugfix-unit-001 (GameRoom mock) was independent of E2E fixes
- All three bugfixes were done sequentially - wasted opportunity
- Parallel assignment would have saved ~1 iteration
- PM must evaluate independence before sequential assignment

### 8. Playtest Phase Decision Framework (NEW - 2026-01-27)

**Goal**: Avoid wasting Game Designer time on non-gameplay features that don't need playtest validation.

**Playtest SKIP Criteria** (feat-tps-003 precedent):
- ❌ Camera distance adjustments
- ❌ Visual-only changes (shader tweaks, material updates)
- ❌ Bug fixes (non-gameplay related)
- ❌ Test infrastructure (CI/CD, tooling)
- ❌ Backend-only changes without visual impact
- ❌ Documentation-only changes

**Playtest REQUIRED for:**
- ✅ Gameplay mechanics (movement, shooting, physics, friction)
- ✅ Visual features affecting gameplay (shaders, materials, VFX)
- ✅ UI/UX changes (HUD, menus, interaction design)
- ✅ Character/weapon behavior changes
- ✅ Multiplayer features

**Decision Framework:**
```javascript
function shouldPlaytest(task) {
  // SKIPPED categories
  const skipCategories = ['bugfix', 'test_scene', 'documentation'];
  if (skipCategories.includes(task.category)) return false;

  // Camera-only tasks
  if (task.title.includes('Camera') && !task.title.includes('Controller')) return false;
  if (task.title.includes('Shader') && !task.title.includes('Gameplay')) return false;

  // Required categories
  const playtestCategories = ['functional', 'gameplay', 'ui', 'visual'];
  if (playtestCategories.includes(task.category)) {
    // Further filter: is it gameplay-affecting?
    const gameplayKeywords = ['friction', 'movement', 'shooting', 'weapon', 'input'];
    if (gameplayKeywords.some(k => task.title.includes(k) || task.description.includes(k))) {
      return true;
    }
  }

  return false;
}
```

**Rationale:** Playtesting is time-consuming and should be focused on features that directly impact player experience. Technical fixes can be validated through code review and automated tests.

### 10. Test Coverage for Architectural Tasks (NEW - 2026-01-28)

**Goal**: Ensure minimal E2E test coverage is created even for foundational architectural tasks.

**Problem Identified (arch-001 retrospective):**
- Architectural tasks (R3F Canvas setup) had limited E2E test coverage
- No error boundary testing established upfront
- Performance monitoring not set up before optimization needs arise

**Test Coverage Requirements for Architectural Tasks:**
```markdown
For ANY architectural task (arch-*, integration):
1. WebGL context verification test
2. Console error check (with WebGL headless filtering)
3. Component renders without crashes test
4. Error boundary exists (if applicable)
```

**QA Agent Instructions (add to task assignment):**
- For architectural tasks: Create basic E2E tests verifying setup
- For state management tasks: Expose stores for testing, verify state updates
- Document test coverage gaps in retrospective for future improvement

**Performance Monitoring Setup:**
- Add Stats.js from drei for all R3F tasks
- Establish FPS, draw call, and triangle count baselines
- Create performance checkpoints before adding complex features

**Developer Agent Instructions:**
- Add ErrorBoundary wrapper to App.tsx during initial Canvas setup
- Expose Zustand stores to `window.__ZUSTAND__` in development builds
- Add `data-ready="1"` attribute to Canvas when scene initializes

### 11. GDD-to-PRD Validation Gap Prevention (NEW - 2026-01-28)

**Goal**: Ensure PRD tasks derived from GDD include acceptance criteria and test plans.

**Problem:** Some tasks have minimal acceptance criteria, making validation difficult for QA.

**When creating PRD tasks from GDD:**
```markdown
For each task extracted from GDD sections:
1. Define at least 3 specific acceptance criteria
2. Include verification steps for each criterion
3. Reference specific GDD sections
4. Consider testability during task creation
```

**Acceptance Criteria Quality Checklist:**
- [ ] Each criterion is objectively verifiable (pass/fail)
- [ ] Criteria can be tested via automation or manual verification
- [ ] Visual criteria include reference images or descriptions
- [ ] Performance criteria include measurable thresholds (FPS, ms)
- [ ] Behavior criteria include expected user actions and responses

### 12. State Management Testing Requirements (NEW - 2026-01-28)

**Goal**: Ensure state management tasks have comprehensive test coverage including integration tests.

**Problem Identified (arch-002 retrospective):**
- State management tasks need both unit tests (store slices) AND integration tests (React re-renders)
- Mock patterns must be reusable across test files
- DevTools exposure required for debugging

**State Management Task Requirements:**
```markdown
For ANY state management task (Zustand, Redux, Context):
1. Unit tests for each store slice (connection, player, match, ui)
2. Integration tests verifying React component re-renders on state changes
3. Mock factory pattern for consistent test data
4. DevTools middleware configured (development builds)
5. Expose stores to window.__ZUSTAND__ for debugging
```

**QA Validation Checklist for State Tasks:**
- [ ] All store slices have unit tests
- [ ] Integration tests verify React re-renders
- [ ] TypeScript types defined for all state
- [ ] Zero @ts-ignore or dangerous any types
- [ ] DevTools middleware working
- [ ] State updates trigger UI changes

**Developer Implementation Checklist:**
- [ ] Separate slice files for clear separation of concerns
- [ ] Shared types.ts file for cross-store interfaces
- [ ] JSDoc documentation on all exports
- [ ] Barrel export pattern (@/store) for convenient importing
- [ ] Mock store factory in tests for isolated setups

**Sources:**
- https://zustand.docs.pmnd.rs/guides/advanced-typescript
- https://github.com/pmndrs/zustand

### 9. Tech Artist Retrospective Excusal Criteria (NEW - 2026-01-27)

**Goal**: Avoid blocking Tech Artist from TIER_0_BLOCKER work for non-visual retrospectives.

**Excusal Decision Framework:**
```javascript
function shouldExcuseTechArtist(task, techArtistStatus) {
  // Check if Tech Artist working on TIER_0_BLOCKER
  if (techArtistStatus.currentTaskId?.tier !== 'TIER_0_BLOCKER') return false;

  // Check if current retrospective is visual/non-visual
  const visualKeywords = ['shader', 'material', 'model', 'vfx', 'particle', 'texture'];
  const isVisualTask = visualKeywords.some(k =>
    task.title.includes(k) || task.description.includes(k)
  );

  // Excuse if: Tech Artist on blocker AND task is non-visual
  return !isVisualTask;
}
```

**Example from feat-tps-004:**
- Tech Artist working on: `bugfix-shader-001` (TIER_0_BLOCKER)
- Retrospective task: `feat-tps-004` (Camera Shoulder Offset Fix)
- Task type: Camera value adjustment (non-visual)
- Decision: EXCUSE Tech Artist from retrospective

**When NOT to excuse:**
- Task involves shaders, materials, 3D models, VFX
- Tech Artist contributed to implementation
- Tech Artist has no blocking tasks

**Retrospective template with excusal:**
```markdown
### Tech Artist Perspective

**EXCUSED** - Tech Artist is working on {blocker-task} (TIER_0_BLOCKER)
This task has no visual/shader component requiring Tech Artist input.
```

## PM Self-Improvement Process

During `skill_research` phase:

### Step 1: Analyze PM Performance

Review the retrospective for PM-specific issues:

```powershell
# PM Performance Questions
1. Was task assignment optimal? (task-selection.md)
2. Did I anticipate risks that materialized? (risk assessment)
3. Were messages clear and timely? (communication)
4. Did I extract tasks from GDD properly? (design integration)
5. Was the retrospective synthesis comprehensive? (facilitation)
```

### Step 2: Identify Priority Improvement

Select ONE PM skill area with the highest impact:

```markdown
| Impact | Skill Area               | Trigger Questions                          |
|--------|--------------------------|--------------------------------------------|
| HIGH   | Task Selection           | Tasks blocked, wrong agent assigned?       |
| HIGH   | Design Integration       | PRD gaps vs GDD?                           |
| MEDIUM | Risk Assessment          | Surprises/blockers occurred?               |
| MEDIUM | Retrospective Facilitation | Insights missed or shallow?              |
| LOW    | Communication           | Messages misunderstood or delayed?         |
```

### Step 3: Research PM Knowledge

Use MCP tools to research:

```powershell
# Research via MCP GitHub
- bmad-code-org/BMAD-METHOD: orchestration patterns

# Research via MCP Web Search
- "AI agent orchestration best practices"
- "multi-agent PM coordination"
- "requirements extraction from design docs"

# Internal Analysis
- Review past retrospectives in .claude/session/retrospective-history/
- Identify patterns in PM decisions that could be improved
```

### Step 4: Update PM Skill File

Apply findings to the relevant PM skill:

```powershell
# Files to Update (PICK ONE)
- agents/pm/skills/task-selection.md
- agents/pm/skills/prd-reorganization.md
- agents/pm/skills/retrospective.md
- agents/pm/skills/scale-adaptive.md
- agents/pm/AGENT.md

# Commit Pattern
git add agents/pm/skills/[updated-file].md
git commit -m "Retrospective [N]: Improved PM [skill-area] skill"
```

### Step 5: Update PM Behavior (if needed)

If the improvement requires AGENT.md changes:

```powershell
# Update AGENT.md with new:
- State flow changes
- Message type handling
- Coordination patterns
- Decision criteria
```

## PM Skill Quality Checklist

After each self-improvement, verify:

- [ ] The updated skill has measurable improvement criteria
- [ ] The skill includes concrete examples or patterns
- [ ] The improvement is integrated into AGENT.md if needed
- [ ] The change is committed with descriptive message
- [ ] Next retrospective will validate the improvement

## PM Skill Improvement Examples

### Example 1: Task Selection Improvement

**Issue Found**: Developer got stuck because task required design approval first.

**Improvement**: Add prerequisite check to task-selection.md

```markdown
## Dependency Verification

Before assigning a task:
1. Check all dependencies are in `passed` or `completed` status
2. Verify no tasks with `priority: high` are blocking
3. Confirm Game Designer has approved design-dependent tasks
```

### Example 2: Design Integration Improvement

**Issue Found**: PRD missing tasks for GDD section on multiplayer sync.

**Improvement**: Add GDD scanning pattern to prd-reorganization.md

```markdown
## GDD-to-PRD Extraction Pattern

For each GDD section:
1. Identify "must have" features
2. Create at least one PRD task per feature
3. Set priority: high for core gameplay, medium for polish
4. Add gddReference field linking back to source
```

### Example 3: Risk Assessment Improvement

**Issue Found**: Physics integration delayed due to Rapier version conflict.

**Improvement**: Add dependency risk check to scale-adaptive.md

```markdown
## Risk Indicators

Red flags before task assignment:
- Package version conflicts
- Missing MCP tools for required research
- Agent skill gaps for task complexity
```

## Minimum Self-Improvement Per Retrospective

**REQUIRED**: At least ONE PM skill file updated per retrospective cycle.

This ensures the PM agent improves at the same rate as worker agents.

## Reference

- [pm-improvement-skill-research](../pm-improvement-skill-research/SKILL.md) — Overall skill improvement coordination
- [pm-retrospective-facilitation](../pm-retrospective-facilitation/SKILL.md) — When self-improvement occurs
- [pm-organization-task-selection](../pm-organization-task-selection/SKILL.md) — Core PM capability
- [pm-organization-prd-reorganization](../pm-organization-prd-reorganization/SKILL.md) — Design integration
