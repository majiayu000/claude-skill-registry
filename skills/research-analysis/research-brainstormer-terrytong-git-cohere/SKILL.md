---
name: research-brainstormer
description: Transform research ideas into actionable experiments with hypotheses, iteration rewards, and completion criteria. Use when brainstorming experiments, designing research plans, converting vague ideas into structured plans, or needing fast feedback signals for implementation. Triggers on phrases like "brainstorm experiments", "design an experiment", "what should I test", "turn this idea into an experiment", or "help me plan research".
---

# Research Brainstormer

Turn research ideas into rigorous, fast-iterating experimental designs with clear completion criteria.

## Workflow

```
1. Understand → 2. Assess Tractability → 3. Design Experiments →
4. Design Iteration Rewards → 5. Prioritize → 6. Create Tasks → 7. Save Plan
```

## Phase 1: Understand the Research Space

Ask clarifying questions **ONE AT A TIME** (prefer multiple choice):
- What sparked this idea? (intuition, observation, paper, failed experiment?)
- What would success look like?
- What's the fastest way to test if this has merit?

## Phase 2: Tractability Assessment

| Factor | Green | Yellow | Red |
|--------|-------|--------|-----|
| Experiment loop | < 1 day | 1-7 days | > 1 week |
| Data | Have it | Can generate | Need to collect |
| Tooling | Exists | Minor mods | Build from scratch |

**If Red flags dominate**: Consider pivoting. Low-hanging fruit is elsewhere.

## Phase 3: Design Experiments

For each experiment, define:

```markdown
## Experiment: {Name}

### Research Question
{One clear question this answers}

### Hypothesis
{Specific, falsifiable prediction}

### Variables
- **Independent**: {what you manipulate}
- **Dependent**: {what you measure}
- **Controls**: {what you hold constant}

### Methodology
1. {step-by-step procedure}
2. {data collection}
3. {analysis plan}
```

See [plan-template.md](references/plan-template.md) for full template.

## Phase 4: Design Iteration Rewards

**Goal: Never implement >30 min without feedback.**

For each experiment, define:

| Check | Time | Question |
|-------|------|----------|
| Smoke test | <1 min | Does anything run? |
| Shape check | <1 min | Are dimensions correct? |
| Quick metric | <5 min | Accuracy on 10-50 samples? |
| Progress signal | Ongoing | What to log? |
| Pivot indicator | <30 min | When to abandon? |

### Template

```markdown
## Iteration Rewards for: {experiment name}

**After 1 min**: {smoke test}
**After 5 min**: {quick metric on small sample}
**After 15 min**: {partial results expectation}
**After 30 min**: {pivot or persist decision}

**Progress signals to log**:
- {metric 1}
- {metric 2}

**Green flags (REQUIRED before done)**:
- [ ] {checkpoint 1 - must pass to be complete}
- [ ] {checkpoint 2}
- [ ] {checkpoint 3}

**Red flags (abandon immediately)**:
- {sign this approach won't work}
```

See [validation-patterns.md](references/validation-patterns.md) for examples.

## Phase 5: Prioritize

Rank by:
1. **Information / Time** - high info, low time first
2. **Dependencies** - what unblocks other experiments?
3. **Swamp risk** - safer bets early

## Phase 6: Create Tasks

Use `/todoist-task-creator` skill. Project IDs:
- Astra Research Todo: `2363714334`
- Research: `2363714490`

## Phase 7: Save Plan

**REQUIRED**: Write plan to `.claude/plans/research_tasks/plan-{N}.md`

1. Check existing: `ls .claude/plans/research_tasks/plan-*.md`
2. Create next numbered file
3. Use template from [plan-template.md](references/plan-template.md)

This queue feeds into `/research-executor` skill.

## Output Format

Present in sections (200-300 words each):
1. Context Summary
2. Tractability Assessment
3. Experiment Proposals (2-4, ranked)
4. Iteration Rewards (with green/red flags)
5. Recommended Path
6. Task Creation confirmation
7. Plan file location

After each section: "Does this look right so far?"

## Key Principles

- **One question at a time**, prefer multiple choice
- **YAGNI ruthlessly** - simpler experiments are better
- **Fast iteration > perfect design**
- **Green flags define "done"** - not done until all checked
- **Red flags mean pivot** - don't persist in swamps

## Related Skills

- `/research-methodology` - Ethan Perez's velocity tips
- `/todoist-task-creator` - structured task creation
- `/research-executor` - executes plans from queue
- `/statistical-analysis` - experiment design help
