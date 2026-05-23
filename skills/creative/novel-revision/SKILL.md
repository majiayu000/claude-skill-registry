---
name: novel-revision
description: Manage multi-level novel revisions while preventing cascade problems. Use when editing novels, when changes at one level break things at others, when you need systematic change management for long-form fiction, or when revisions keep creating new problems.
license: MIT
metadata:
  author: jwynia
  version: "1.0"
---

# Novel Revision: Multi-Level Change Management Skill

You help writers manage revisions across multiple levels of abstraction while preventing unintended consequences from cascading through the narrative. Your role is to implement systematic change management that maintains story coherence.

## Core Principle: Cascade Awareness

**Any change at one level potentially affects all other levels.** Changes propagate both upward (prose discoveries revealing structural problems) and downward (structural changes requiring prose rewrites).

## The Three Levels

Every novel operates simultaneously across these levels:

### Thematic/Conceptual Level
- Core themes and meaning
- Character growth arcs
- Symbolic elements and motifs
- Overall message and emotional journey

### Structural Level
- Plot beats and story architecture
- Scene sequences and chapter organization
- Pacing and rhythm
- Tension patterns and resolution cycles

### Manuscript Level
- Actual prose and dialogue
- Descriptive passages
- Voice and style consistency
- Line-level craft elements

## Pre-Change Analysis Protocol

Before implementing any revision:

### 1. Identify the Change Level
- **Conceptual**: Changing themes, character motivations, meaning
- **Structural**: Altering plot beats, scene order, pacing
- **Prose**: Improving language, dialogue, descriptions

### 2. Map Forward Consequences
For each proposed change, document:
- **Immediate** (1-2 chapters): What must change next?
- **Medium-term** (3-5 chapters): What implications ripple forward?
- **Story-wide**: How might this affect ending or major plot points?

### 3. Create Monitoring Criteria
Define warning signs that indicate problems:
- Character behavior inconsistencies
- Plot logic gaps
- Pacing anomalies
- Thematic contradictions

## Change Implementation Workflow

### Phase 1: Impact Assessment
1. **Document current state**: Snapshot relevant story elements
2. **Project consequences**: Write expected chain of implications
3. **Set checkpoints**: Identify where you'll evaluate
4. **Define rollback triggers**: Clear criteria for aborting

### Phase 2: Controlled Implementation
1. **Make minimal viable change**: Smallest version that tests hypothesis
2. **Monitor immediately**: Check for local coherence problems
3. **Document observations**: Note unexpected effects
4. **Evaluate against projections**: Compare actual to predicted

### Phase 3: Ripple Management
1. **Identify required updates**: What else must change?
2. **Prioritize cascade tasks**: Order by importance and dependency
3. **Track completion**: Explicit lists of updated vs. pending
4. **Validate consistency**: Check updates work together

## Revision Types and Protocols

### Character Development Revisions
**Triggers**: Character feels flat, motivations unclear, arc incomplete

**Protocol**:
1. Map current character state across all chapters
2. Identify scenes where growth should be visible
3. Project how changes affect dialogue/actions later
4. Check consistency with other characters' responses

**Monitoring**: Does behavior remain believable? Do others respond appropriately?

### Plot Structure Revisions
**Triggers**: Pacing off, events disconnected, climax lacks impact

**Protocol**:
1. Create timeline of current plot beats
2. Identify specific structural elements to change
3. Map how timing changes affect tension
4. Check causality chains still hold

**Monitoring**: Does tension build? Do plot points feel connected and inevitable?

### Thematic Revisions
**Triggers**: Theme heavy-handed, unclear, or inconsistent

**Protocol**:
1. Audit current thematic elements throughout manuscript
2. Identify opportunities for subtler integration
3. Check character actions support thematic development
4. Ensure climax/resolution reinforce themes

**Monitoring**: Do themes emerge naturally? Does resolution feel thematically satisfying?

## Early Warning Signs

| Warning Sign | What It Indicates |
|--------------|-------------------|
| Character acts against personality without development | Consistency break |
| Events don't follow logically | Plot logic gap |
| Scenes feel rushed or drag unexpectedly | Pacing anomaly |
| Story events undermine themes | Thematic drift |

## Intervention Protocols

### When to Roll Back
- Multiple warning signs within 2 chapters
- Fundamental character or plot logic breaks
- Change creates more problems than it solves
- Cascade tasks become overwhelming

### Rollback Procedure
1. **Identify rollback point**: Return to last stable state
2. **Document lessons**: What went wrong and why
3. **Revise approach**: Alternative strategy based on learning
4. **Add safeguards**: Monitoring to prevent recurrence

### When to Push Forward
- Problems are localized and manageable
- Benefits clearly outweigh complications
- Cascade tasks are well-defined
- Core story logic remains intact

## Change Record Template

```markdown
# Revision: [Brief Description]

## Change Type
- [ ] Conceptual  - [ ] Structural  - [ ] Prose

## Rationale
[Why this change is needed]

## Predicted Consequences
- Immediate (1-2 chapters):
- Medium-term (3-5 chapters):
- Story-wide:

## Monitoring Criteria
- Warning sign 1:
- Warning sign 2:
- Success indicator 1:
- Success indicator 2:

## Implementation Status
- [ ] Initial change complete
- [ ] Cascade tasks identified
- [ ] Cascade tasks completed
- [ ] Validation complete

## Outcome Assessment
[Complete after implementation]
```

## Multi-Agent Collaboration

When working with multiple agents on revision:

### Role Boundaries
- **Structure Agent**: Plot architecture and pacing
- **Character Agent**: Development and consistency
- **Prose Agent**: Language and voice
- **Continuity Agent**: Cross-level consistency

### Communication Protocols
- Share intentions before implementation
- Report unexpected discoveries immediately
- Flag potential cross-level implications
- Coordinate cascade task assignments

### Conflict Resolution
1. Document what elements are in tension
2. Escalate to human for creative resolution
3. Explore alternative approaches
4. Prioritize based on story goals

## Best Practices

### Start Small
- Incremental changes over major overhauls
- Test one element at a time
- Build confidence through small wins

### Maintain Perspective
- Remember overall story goals
- Don't lose sight of what works
- Balance perfection with completion

### Document Everything
- Capture insights during revision
- Record what works and doesn't
- Build knowledge for future projects

### Trust the Process
- Allow time for changes to settle
- Don't rush to fix every minor issue
- Some problems resolve as story develops

## Diagnostic Questions

When revision feels stuck:

1. What level is this change really at?
2. Have I mapped forward consequences?
3. What would tell me this is working?
4. What would tell me to roll back?
5. Am I making minimal viable change?
6. What cascade tasks does this create?
7. Am I tracking completions explicitly?

## Output Persistence

### Output Discovery
1. Check for `context/output-config.md` in the project
2. If found, look for this skill's entry
3. If not found, ask user: "Where should I save revision tracking?"
4. Suggest: `revision/` or `explorations/revision/`

### Primary Output
- **Change records** - Using template for each significant change
- **Cascade task lists** - Secondary edits required by changes
- **Monitoring log** - Warning signs observed and addressed
- **Rollback points** - Snapshots of stable states

### File Naming
Pattern: `{novel-name}-revision-{date}.md`

## Verification (Oracle)

### What This Skill Can Verify
- **Impact assessment complete** - Were consequences mapped? (High confidence)
- **Cascade tracking** - Are secondary tasks documented? (High confidence)
- **Monitoring active** - Are warning signs being watched? (Medium confidence)

### What Requires Human Judgment
- **Change necessity** - Is this revision actually needed?
- **Rollback decision** - When problems outweigh benefits
- **Creative resolution** - When changes create conflicts

### Oracle Limitations
- Cannot assess whether changes improve the story
- Cannot predict creative success of revision approach

## Feedback Loop

### Session Persistence
- **Output location:** See `context/output-config.md`
- **What to save:** Change records, cascade tasks, monitoring log
- **Naming pattern:** `{novel-name}-revision-{date}.md`

### Cross-Session Learning
- Check for prior revision work on this novel
- Build on lessons from previous change attempts
- Failed revisions inform anti-patterns

## Design Constraints

### This Skill Assumes
- Novel draft exists to revise
- Changes potentially affect multiple levels
- Writer wants systematic change management

### This Skill Does Not Handle
- **Problem diagnosis** - Route to: story-sense
- **Scene-level revision** - Route to: revision
- **Prose-level editing** - Route to: prose-style

### Degradation Signals
- Unassessed changes (no consequence mapping)
- Warning sign blindness (ignoring red flags)
- Cascade debt (untracked secondary tasks)

## Reasoning Requirements

### Standard Reasoning
- Single change assessment
- Basic cascade identification
- Simple monitoring setup

### Extended Reasoning (ultrathink)
- **Multi-change coordination** - [Why: changes interact across levels]
- **Full cascade analysis** - [Why: secondary effects compound]
- **Rollback planning** - [Why: complex reversions need strategy]

**Trigger phrases:** "coordinate all revisions", "map full cascade", "plan the rollback"

## Execution Strategy

### Sequential (Default)
- Impact assessment before implementation
- Implementation before cascade tracking
- Cascade before validation

### Parallelizable
- Assessing multiple independent changes
- Tracking cascade tasks across different sections

### Subagent Candidates
| Task | Agent Type | When to Spawn |
|------|------------|---------------|
| Consistency check | Explore | When verifying changes across manuscript |
| Character tracking | general-purpose | When monitoring character consistency |

## Context Management

### Approximate Token Footprint
- **Skill base:** ~3.5k tokens (levels + protocols + workflow)
- **With template:** ~4.5k tokens
- **With best practices:** ~5k tokens

### Context Optimization
- Focus on current revision type and protocol
- Template is reference for documentation
- Multi-agent section is optional

### When Context Gets Tight
- Prioritize: Current revision protocol, active change record
- Defer: Full protocol list, multi-agent coordination
- Drop: Best practices, diagnostic questions

## Anti-Patterns

### 1. Unassessed Changes
**Pattern:** Making revisions without first analyzing what else might be affected—jumping straight to implementation.
**Why it fails:** Changes cascade. A character motivation change affects every scene where that character makes choices. Unassessed changes create problems you discover pages later, often after you've built on broken foundation.
**Fix:** Before every significant change, explicitly document: what must change as a result? What might break? Set monitoring criteria before implementation, not after.

### 2. Warning Sign Blindness
**Pattern:** Noticing that something feels off after a change but pushing forward anyway, trusting it will resolve itself.
**Why it fails:** Early warnings are cheap signals about expensive problems. Characters acting against established personality, plot logic gaps, pacing anomalies—these compound. The deeper you go, the more expensive the fix.
**Fix:** Treat early warnings as actionable information. Stop, evaluate, decide to either fix now or explicitly accept the risk. Don't let "I'll fix it later" accumulate.

### 3. Cascade Debt
**Pattern:** Making changes without tracking the secondary edits they require—accumulating a backlog of unaddressed implications.
**Why it fails:** Untracked cascade tasks become invisible technical debt. You think you made one change; you actually made one change and created ten unfixed inconsistencies.
**Fix:** Maintain explicit cascade task lists. When a change requires follow-up edits, write them down immediately. Track completion. Don't move on until cascade is resolved.

### 4. Sunk Cost Persistence
**Pattern:** Continuing with a problematic change because you've already invested significant effort, even when warning signs multiply.
**Why it fails:** The effort is gone either way. Continuing down a broken path just adds more lost effort. Multiple warning signs within two chapters usually indicate fundamental problems.
**Fix:** Define rollback triggers before implementation. When triggers fire, roll back. Document what you learned. The insight is valuable even if the change wasn't.

### 5. Activity Confusion
**Pattern:** Measuring progress by pages revised rather than by improvement achieved—conflating work with results.
**Why it fails:** You can revise extensively without making the story better. In fact, you can revise extensively and make it worse. Activity that doesn't serve story goals is waste.
**Fix:** Define what "better" means for each revision pass. Measure against that goal, not against pages touched. Sometimes the best revision is no revision.

## Integration

### Inbound (feeds into this skill)
| Skill | What it provides |
|-------|------------------|
| story-sense | Diagnosis of what needs revision |
| character-arc | Character consistency requirements |
| scene-sequencing | Pacing and structure requirements |

### Outbound (this skill enables)
| Skill | What this provides |
|-------|-------------|
| prose-style | Manuscript-level changes with cascade awareness |
| revision | Scene-level work with multi-level coordination |
| (completed novel) | Final product with maintained coherence |

### Complementary
| Skill | Relationship |
|-------|--------------|
| story-sense | Story-sense diagnoses problems; novel-revision manages the fix without creating new problems |
| revision | Revision handles sentence and scene level; novel-revision coordinates across the whole manuscript |
