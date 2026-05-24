---
name: codex-brainstorm
description: Adversarial brainstorming. Claude and Codex independently research then debate until Nash equilibrium. For solution exploration, feasibility analysis, exhaustive enumeration.
allowed-tools: mcp__codex__codex, mcp__codex__codex-reply, Read, Grep, Glob
---

# Codex Brainstorm Skill

## Trigger

- Keywords: brainstorm, exhaust possibilities, explore solutions, deep discussion, feasibility analysis, solution exploration, Nash equilibrium

## When NOT to Use

- Simple technical Q&A (answer directly)
- Already have a clear solution (implement directly)
- Only need code review (use `/codex-review`)

## Core Principle

```
⚠️ Independent Research → Adversarial Debate → Nash Equilibrium ⚠️

Nash Equilibrium = Neither party can unilaterally change strategy to achieve a better outcome
```

## Workflow

| Phase | Action                                                  | Output                      |
| ----- | ------------------------------------------------------- | --------------------------- |
| 1     | **Claude independent research** + analysis, forms Position A | Claude's optimal hypothesis |
| 2     | **Codex independent research** + analysis, forms Position B | Codex's optimal hypothesis  |
| 3     | Multi-round adversarial debate, mutual attacks          | Debate exchange record      |
| 4     | Check equilibrium, no further improvements possible     | Equilibrium or divergence   |
| 5     | Output final report                                     | Nash Equilibrium report     |

### Phase 2: Codex Independent Research (Critical)

**⚠️ Must let Codex research independently; do NOT feed Claude's analysis results ⚠️**

```typescript
mcp__codex__codex({
  prompt: `You are a senior architect. Conduct an **independent analysis** of the following topic.

## Topic
${TOPIC}

## Constraints
${CONSTRAINTS}

## ⚠️ Important: You must research independently ⚠️
Before forming conclusions, you **must** first:
1. Run \`ls src/\` to understand the directory structure
2. Search related code: \`grep -r "keyword" src/ --include="*.ts" -l | head -10\`
3. Read relevant files to confirm existing implementations

## Output Requirements
1. Research summary (related modules, existing patterns)
2. Your position + supporting arguments
3. Potential risks`,
  sandbox: 'read-only',
  'approval-policy': 'on-failure',
});
```

### Phase 3: Adversarial Debate

Structure per round:

1. Claude attacks flaws in Codex's proposal
2. Codex rebuts or updates position
3. Equilibrium check: Can either side raise new attacks?

### Termination Conditions

| Condition         | Description                              | Result              |
| ----------------- | ---------------------------------------- | ------------------- |
| Nash Equilibrium  | Neither side can raise new attacks       | Output equilibrium  |
| Convergence       | Both positions converge                  | Output consensus    |
| Max rounds        | 5 rounds reached with remaining divergence | Output divergence report |

## Verification

- [ ] Claude formed an independent position (not following Codex)
- [ ] Codex performed code research (not speculating)
- [ ] At least 3 rounds of adversarial debate
- [ ] Each round has clear attack/defense records
- [ ] Final report indicates equilibrium status

## References

| File             | Purpose                        |
| ---------------- | ------------------------------ |
| `templates.md`   | Claude/debate/report templates |
| `techniques.md`  | Attack/defense techniques      |
| `equilibrium.md` | Equilibrium determination flow |

## Example

```
Input: What implementation approaches are available for this requirement?

Phase 1: Claude independent research → Position A (Solution X is optimal)
Phase 2: Codex independent research → Position B (Solution Y is optimal)
Phase 3: Adversarial debate
  - R1: Claude attacks Y's scalability / Codex attacks X's complexity
  - R2: Claude rebuts / Codex concedes and updates position
  - R3: Both converge to Solution Z, no further attacks → Equilibrium
Phase 4: Output Nash Equilibrium = Solution Z
```
