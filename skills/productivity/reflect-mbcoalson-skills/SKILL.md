---

name: reflect
description: Use this skill when capturing user corrections, feedback, or learnings from a session to permanently improve other skills. This includes when users correct skill selection, suggest better approaches, validate successful patterns, or identify mistakes that should never be repeated. Invoked automatically by work-command-center at session end when feedback is detected.
---

# Reflect - Continuous Skill Improvement System

## Philosophy: "Correct Once, Never Again"

This meta-skill embodies a core principle: AI should learn from corrections rather than repeating mistakes across sessions. Reflect captures human guidance during sessions and permanently encodes it into skill definitions, creating a self-improving orchestration system.

## How It Works

### Three-Level Confidence System

Reflect analyzes session conversations and classifies feedback into three confidence levels:

**HIGH Confidence (Critical Corrections)**
- Pattern: "Use X instead of Y", "Never do Z", "Always check A before B"
- Creates: "Critical Corrections" section in target skill
- Example: "Always validate with OpenStudio docs first, not Unmet Hours"

**MEDIUM Confidence (Best Practices)**
- Pattern: "Yes, perfect!", "Exactly right", "This is the correct approach"
- Creates: "Best Practices" section in target skill
- Example: "User confirmed: Running energyplus-assistant for QA/QC before simulation works well"

**LOW Confidence (Considerations)**
- Pattern: "Have you considered...", "Might want to...", "Could also..."
- Creates: "Considerations" section in target skill
- Example: "User suggested: Check for HVAC autosizing before running simulation"

### Learning Storage Architecture

Each skill can have a companion `.reflect.yaml` file storing accumulated learnings:

```yaml
skill_name: energyplus-assistant
last_updated: 2026-01-12T10:30:00Z

critical_corrections:
  - pattern: "User corrected: Always validate with OpenStudio docs first"
    fix: "Check OpenStudio 3.9 docs BEFORE Unmet Hours forums"
    timestamp: 2026-01-12T10:30:00Z
    session_id: "20260112-0930"

best_practices:
  - pattern: "User approved: QA/QC workflow finds 90% of issues"
    practice: "Run validation checklist: geometry → HVAC → schedules → constructions"
    timestamp: 2026-01-12T11:15:00Z
    session_id: "20260112-0930"

orchestration_learnings:
  - task_description: "validate energy model"
    skill_chosen: running-openstudio-models
    outcome: wrong_skill
    correct_skill: energyplus-assistant
    reasoning: "Running models is for simulations, validation is assistant's job"
    timestamp: 2026-01-12T10:45:00Z
```

## When to Use This Skill

**Automatic Invocation (Primary):**
- work-command-center invokes Reflect at session end
- WCC asks: "Any corrections or learnings to capture from this session?"
- If yes → Reflect analyzes conversation → Proposes updates

**Manual Invocation (Secondary):**
- User explicitly says "reflect on this" or "capture that learning"
- After receiving significant correction mid-session
- When user wants to codify a new best practice immediately

**DO NOT Use For:**
- General conversation or questions (not corrections)
- One-off situational advice (not repeatable patterns)
- User expressing preferences without correction context

## Integration with Work-Command-Center

Reflect is deeply integrated into WCC's session lifecycle:

### Session End Protocol (WCC Integration Point)

Added to WCC's session-end protocol as step 2.5:

```markdown
2.5. **Invoke Reflect (if feedback detected)**:
   - Ask: "Any corrections or learnings to capture from this session?"
   - If yes: Invoke reflect skill
   - Reflect proposes skill updates → user approves → skills improve
```

### Orchestration Learning

Reflect can learn from WCC's delegation decisions:

**Pattern Detected:**
```
User: "validate the energy model"
WCC: Delegates to running-openstudio-models
User: "No, I need validation, not simulation"
WCC: Corrects to energyplus-assistant
```

**Learning Captured:**
```yaml
orchestration_learnings:
  - keywords: ["validate", "energy model"]
    incorrect_skill: running-openstudio-models
    correct_skill: energyplus-assistant
    disambiguation: "validate = QA/QC (assistant), simulate = run (models)"
```

## Technical Workflow

### Step 1: Pattern Detection

Reflect analyzes conversation transcript:

```javascript
// reflect-engine.js analyzes chat messages
const patterns = detectFeedbackPatterns(transcript);
// Returns: [
//   { type: 'correction', confidence: 'HIGH', skill: 'energyplus-assistant', ... },
//   { type: 'approval', confidence: 'MEDIUM', skill: 'writing-proposals', ... }
// ]
```

### Step 2: YAML Generation

Creates learning entries:

```javascript
// skill-updater.js generates YAML
const learning = {
  skill_name: 'energyplus-assistant',
  critical_corrections: [
    {
      pattern: "User corrected: Check OpenStudio docs first",
      fix: "Always consult OpenStudio 3.9 docs before Unmet Hours",
      timestamp: new Date().toISOString()
    }
  ]
};
```

### Step 3: Skill Update Proposal

Proposes SKILL.md diff:

```diff
# energyplus-assistant

## Critical Corrections

+### Always Validate with Official Documentation First
+Before consulting community resources like Unmet Hours, check:
+1. OpenStudio 3.9 official documentation
+2. EnergyPlus Engineering Reference
+3. NREL measure documentation
+
+Community forums are helpful but official docs are authoritative.
+(Learned: 2026-01-12, Session: 20260112-0930)

## Core Workflow
...
```

### Step 4: User Approval

Shows proposed changes:
- Displays diff
- Explains reasoning
- Asks for approval

### Step 5: Application

If approved:
1. Writes `.reflect.yaml` (learning storage)
2. Updates skill's SKILL.md (human-readable)
3. Creates Git commit with learning description
4. Preserves timestamped backup

## File Structure

```
.claude/skills/reflect/
├── SKILL.md                           # This file
├── reflect-engine.js                  # Pattern detection engine
├── skill-updater.js                   # Applies learnings to skills
├── learning-schema.yaml               # YAML structure specification
└── templates/
    └── skill-learning-template.yaml   # Template for new learnings
```

### Skill Learning Storage (Per-Skill)

```
.claude/skills/energyplus-assistant/
├── SKILL.md                    # Main skill definition
└── .reflect.yaml               # Accumulated learnings (optional)
```

## Usage Examples

### Example 1: Correction (HIGH Confidence)

**Conversation:**
```
User: "Run the energy model validation"
WCC: [Delegates to running-openstudio-models]
User: "No, I don't want to run it, I want to validate the IDF file"
WCC: [Corrects to energyplus-assistant]
[Later at session end]
WCC: "Any learnings to capture?"
User: "Yes, capture that validation vs running distinction"
```

**Reflect Action:**
- Detects correction: validation → energyplus-assistant (not running-openstudio-models)
- Creates orchestration learning in WCC's .reflect.yaml
- Updates skill-orchestration-guide.md with disambiguation
- Next session: WCC correctly suggests energyplus-assistant for "validation"

### Example 2: Approval (MEDIUM Confidence)

**Conversation:**
```
User: "Create energy audit proposal"
WCC: [Delegates to writing-proposals]
Writing-Proposals: [Generates proposal with pricing from service-types.md]
User: "Perfect! That's exactly the format I needed"
[Later at session end]
WCC: "Any learnings to capture?"
User: "Yes, that proposal workflow was spot-on"
```

**Reflect Action:**
- Detects approval: writing-proposals workflow validated
- Adds to best_practices in writing-proposals/.reflect.yaml
- Updates SKILL.md with "Validated Workflow" example
- Reinforces existing approach

### Example 3: Consideration (LOW Confidence)

**Conversation:**
```
User: "Diagnose this energy model error"
Diagnosing-Energy-Models: [Runs diagnostics]
User: "Have you considered checking the weather file compatibility first? That's caught me before"
```

**Reflect Action:**
- Detects suggestion: check weather file compatibility early
- Adds to considerations in diagnosing-energy-models/.reflect.yaml
- Updates SKILL.md with "Additional Checks" section
- Doesn't override existing workflow, adds to checklist

## Safety & Validation

### Safeguards

1. **User Approval Required:** No skill changes without explicit user confirmation
2. **Git Commits:** Every change committed with descriptive message
3. **Timestamped Backups:** Original skill files preserved with timestamps
4. **YAML Validation:** Schema validation before applying changes
5. **Rollback Support:** Git history enables easy rollback

### Validation Checklist

Before applying learning:
- [ ] Pattern confidence level assigned correctly
- [ ] Target skill identified accurately
- [ ] Proposed change preserves existing SKILL.md structure
- [ ] YAML syntax valid (if creating .reflect.yaml)
- [ ] User has reviewed and approved diff
- [ ] Git commit message explains learning clearly

## Reflect Engine Commands

### Analyze Session

```bash
node .claude/skills/reflect/reflect-engine.js analyze \
  --transcript path/to/conversation.json \
  --output path/to/learnings.yaml
```

### Propose Update

```bash
node .claude/skills/reflect/skill-updater.js propose \
  --skill energyplus-assistant \
  --learning path/to/learnings.yaml \
  --show-diff
```

### Apply Learning

```bash
node .claude/skills/reflect/skill-updater.js apply \
  --skill energyplus-assistant \
  --learning path/to/learnings.yaml \
  --commit-message "Learn: Always check OpenStudio docs first"
```

## Integration with Skill Development

### Skill-Builder Integration

When creating new skills, skill-builder should:
1. Include placeholder sections for learnings
2. Document Reflect integration points
3. Explain how skill will learn over time

### Learning Sections in Skills

Skills updated by Reflect should have sections:

```markdown
## Critical Corrections

(Learned patterns from user corrections)

## Best Practices

(Validated approaches from user approvals)

## Considerations

(Suggestions to keep in mind)
```

## Performance Metrics

Track learning effectiveness:

- **Learning Rate:** % of corrections successfully captured
- **Application Rate:** % of learnings applied after approval
- **Repetition Reduction:** % decrease in repeated mistakes
- **User Satisfaction:** Feedback on learning accuracy

Target metrics:
- 80%+ correction detection
- 90%+ user approval of proposed updates
- 50%+ reduction in repeated corrections over 3 months

## Future Enhancements

Potential improvements:
- Cross-skill pattern detection (learning applies to multiple skills)
- Confidence adjustment (learn from false positives/negatives)
- Automatic testing (verify learnings don't break existing functionality)
- Learning export/import (share learnings across teams)
- AI-generated learning summaries (weekly digest of improvements)

- Consider: Add learning confidence threshold setting where users could control which confidence levels get auto-applied vs requiring approval

## Saving Next Steps

When Reflect work is complete or paused:

```bash
node .claude/skills/work-command-center/tools/add-skill-next-steps.js \
  --skill "reflect" \
  --content "## Priority Tasks
1. Review pending learning proposals
2. Apply approved learnings to skills
3. Test updated skills"
```

See: `.claude/skills/work-command-center/skill-next-steps-convention.md`

---

## Quick Reference

**Detect correction:** Look for "use X instead", "never do Y", "always check Z"
**Detect approval:** Look for "perfect!", "exactly right", "that worked well"
**Detect suggestion:** Look for "consider...", "might want to...", "could also..."

**Store learning:** `.reflect.yaml` per skill
**Update skill:** SKILL.md sections (Critical Corrections, Best Practices, Considerations)
**Commit change:** Git with descriptive message
**Validate:** User approval required always

---

Last Updated: 2026-01-12