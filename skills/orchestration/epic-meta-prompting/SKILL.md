# Epic Meta-Prompting Skill

Generate research and planning prompts for epic workflows using isolated sub-agents.

## Purpose

Use meta-prompting to create research and planning pipelines via `/create-prompt` and `/run-prompt`, preventing context pollution through isolated execution.

## When to Invoke

- During `/epic` Step 3 (Research & Planning phase)
- After epic specification is complete and reviewed
- Skip if resuming past the planning phase

## Research Prompt Generation

```bash
/create-prompt "Research technical approach for: [epic objective]"
```

**The create-prompt skill will:**

1. Detect purpose: Research
2. Ask contextual questions (depth, sources, output format)
3. Generate research prompt in `.prompts/001-[epic-slug]-research/`
4. Reference relevant project docs (@docs/project/tech-stack.md)
5. Specify XML output format with metadata

**Auto-execute research prompt:**

```bash
/run-prompt 001-[epic-slug]-research
```

**Research outputs:**

- `.prompts/001-[epic-slug]-research/research.md`
- Contains: findings, confidence levels, dependencies, open questions, assumptions

## Copy and Commit Research

```bash
# Copy research.md to epic directory
cp .prompts/001-${EPIC_SLUG}-research/research.md epics/${EPIC_SLUG}/research.md

# Extract metadata for commit message
FINDINGS_COUNT=$(xmllint --xpath 'count(//finding)' epics/${EPIC_SLUG}/research.md)
CONFIDENCE=$(xmllint --xpath 'string(//confidence_level)' epics/${EPIC_SLUG}/research.md)
OPEN_QUESTIONS=$(xmllint --xpath 'count(//open_question)' epics/${EPIC_SLUG}/research.md)

# Commit research
git add .prompts/001-${EPIC_SLUG}-research/
git add epics/${EPIC_SLUG}/research.md
git commit -m "docs(epic-research): complete technical research for ${EPIC_SLUG}

Findings: ${FINDINGS_COUNT}
Confidence: ${CONFIDENCE}
Open questions: ${OPEN_QUESTIONS}

Next: Planning phase"
```

**Alternative:** `/meta:enforce-git-commits --phase "epic-research"`

## Planning Prompt Generation

```bash
/create-prompt "Create implementation plan based on research"
```

**The create-prompt skill will:**

1. Detect purpose: Plan
2. Reference research.md from step above
3. Generate plan prompt in `.prompts/002-[epic-slug]-plan/`
4. Specify plan.md output with phases, tasks, constraints

**Auto-execute plan prompt:**

```bash
/run-prompt 002-[epic-slug]-plan
```

**Plan outputs:**

- `.prompts/002-[epic-slug]-plan/plan.md`
- Contains: architecture decisions, implementation phases, dependencies, risks

## Copy and Commit Plan

```bash
# Copy plan.md to epic directory
cp .prompts/002-${EPIC_SLUG}-plan/plan.md epics/${EPIC_SLUG}/plan.md

# Extract metadata for commit message
ARCH_DECISIONS=$(xmllint --xpath 'count(//architecture_decision)' epics/${EPIC_SLUG}/plan.md)
PHASE_COUNT=$(xmllint --xpath 'count(//phase)' epics/${EPIC_SLUG}/plan.md)
DEPENDENCY_COUNT=$(xmllint --xpath 'count(//dependency)' epics/${EPIC_SLUG}/plan.md)
RISK_COUNT=$(xmllint --xpath 'count(//risk)' epics/${EPIC_SLUG}/plan.md)

# Commit plan
git add .prompts/002-${EPIC_SLUG}-plan/
git add epics/${EPIC_SLUG}/plan.md
git commit -m "docs(epic-plan): create implementation plan for ${EPIC_SLUG}

Architecture decisions: ${ARCH_DECISIONS}
Phases: ${PHASE_COUNT}
Dependencies: ${DEPENDENCY_COUNT}
Risks: ${RISK_COUNT}

Next: Sprint breakdown"
```

**Alternative:** `/meta:enforce-git-commits --phase "epic-plan"`

## Auto-Mode Handling

**If auto-mode enabled:**

- Skip PAUSE points (spec review, plan review)
- Auto-execute `/run-prompt` after `/create-prompt`
- Update phases status automatically in state.yaml

**If interactive mode:**

- PAUSE: "Plan review complete. Continue to sprint breakdown? (y/n)"
- Update state.yaml with approval status

## State Updates

After plan review (interactive):

```yaml
manual_gates:
  plan_review:
    status: approved
    approved_at: { ISO_TIMESTAMP }
    approved_by: user

phases:
  research:
    status: completed
    completed_at: { ISO_TIMESTAMP }
  planning:
    status: completed
    completed_at: { ISO_TIMESTAMP }
```

## Velocity Benefit

- Research phase: 1-2 hours (vs 4+ hours manual research)
- Planning phase: 1-2 hours (vs 3+ hours manual planning)
- Total: 3-4x faster with meta-prompting
