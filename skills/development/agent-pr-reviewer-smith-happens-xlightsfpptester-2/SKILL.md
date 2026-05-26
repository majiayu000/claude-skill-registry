---
skill_name: agent-pr-reviewer
activation_code: AGENT_PR_REVIEWER_V1
version: 1.0.0
phase: any
prerequisites:
  - PR URL or PR number
  - GitHub access (gh CLI authenticated)
outputs:
  - PR analysis report
  - Agent-generated recommendation
  - Structured summary for human review
description: |
  Evaluates PRs containing agent changes using specialized agents to analyze
  quality, compliance, and improvement value. Provides turbobeest with a
  structured recommendation to streamline human review.
---

# Agent PR Reviewer Skill

## Purpose

When contributors submit PRs with agent improvements to `turbobeest/dev-system`, this skill:

1. **Extracts** the agent changes from the PR
2. **Validates** against `-01-agent-formatting/` standards
3. **Analyzes** using specialized agents
4. **Summarizes** changes and impact
5. **Recommends** approve, request changes, or decline

## Activation

```
/agent-pr-reviewer pr=123
```

Or with full URL:
```
/agent-pr-reviewer pr=https://github.com/turbobeest/dev-system/pull/123
```

## Workflow

```
┌─────────────────────────────────────────────────────────────────────────┐
│                     PR REVIEW WORKFLOW                                  │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  Step 1: FETCH PR                                                       │
│  ├─ gh pr view {number} --json                                         │
│  ├─ Extract changed files                                              │
│  └─ Identify agent files (agents/**/*.md)                              │
│          ▼                                                              │
│  Step 2: VALIDATE STRUCTURE                                             │
│  ├─ Run agent-creation-validator on each changed agent                 │
│  ├─ Check tier compliance                                              │
│  └─ Verify required sections present                                   │
│          ▼                                                              │
│  Step 3: ANALYZE CHANGES                                                │
│  ├─ Diff analysis: what changed?                                       │
│  ├─ Knowledge sources: added/removed/modified?                         │
│  ├─ Instructions: improved or degraded?                                │
│  └─ Potential regressions flagged                                      │
│          ▼                                                              │
│  Step 4: AGENT EVALUATION                                               │
│  ├─ first-principles-engineer: Is this a good change?                  │
│  ├─ Domain expert (if applicable): Domain accuracy?                    │
│  └─ prd-auditor: Quality assessment                                    │
│          ▼                                                              │
│  Step 5: GENERATE RECOMMENDATION                                        │
│  ├─ Synthesize agent opinions                                          │
│  ├─ Flag concerns or conflicts                                         │
│  └─ Provide structured recommendation                                  │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

## Output Format

```
╔═══════════════════════════════════════════════════════════════════════╗
║              PR REVIEW: #{number}                                      ║
║              {pr-title}                                                ║
╠═══════════════════════════════════════════════════════════════════════╣
║                                                                        ║
║  Author: {author}                                                      ║
║  Branch: {head} → {base}                                              ║
║  Files Changed: {count} ({agent-count} agent files)                   ║
║                                                                        ║
╠═══════════════════════════════════════════════════════════════════════╣
║  AGENT CHANGES                                                         ║
╠═══════════════════════════════════════════════════════════════════════╣
║                                                                        ║
║  ┌────────────────────────────────────────────────────────────────┐   ║
║  │ MODIFIED: typescript-pro.md                                     │   ║
║  ├────────────────────────────────────────────────────────────────┤   ║
║  │ + Added 3 knowledge sources                                     │   ║
║  │ ~ Modified interpretive lens                                    │   ║
║  │ ~ Updated 4 instructions                                        │   ║
║  │ - Removed 1 deprecated reference                                │   ║
║  │                                                                 │   ║
║  │ Structure: ✓ Valid                                              │   ║
║  │ Tier: Expert (unchanged)                                        │   ║
║  │ Token Δ: +120 tokens (within budget)                           │   ║
║  └────────────────────────────────────────────────────────────────┘   ║
║                                                                        ║
║  ┌────────────────────────────────────────────────────────────────┐   ║
║  │ NEW: deno-expert.md                                             │   ║
║  ├────────────────────────────────────────────────────────────────┤   ║
║  │ Category: backend-ecosystems/javascript-runtimes               │   ║
║  │ Tier: Expert                                                    │   ║
║  │ Model: sonnet                                                   │   ║
║  │                                                                 │   ║
║  │ Structure: ✓ Valid                                              │   ║
║  │ Curation Record: ✓ Present                                      │   ║
║  │ Overlap Check: Low overlap with nodejs-expert                   │   ║
║  └────────────────────────────────────────────────────────────────┘   ║
║                                                                        ║
╠═══════════════════════════════════════════════════════════════════════╣
║  AGENT ANALYSIS                                                        ║
╠═══════════════════════════════════════════════════════════════════════╣
║                                                                        ║
║  first-principles-engineer:                                            ║
║    "The typescript-pro changes add authoritative sources from         ║
║     TypeScript's official handbook. The instruction modifications     ║
║     improve specificity without losing generality. Recommend merge."  ║
║    Confidence: HIGH                                                    ║
║                                                                        ║
║  typescript-pro (self-review of diff):                                ║
║    "New knowledge sources are accurate and high-authority.            ║
║     Instruction changes align with TypeScript 5.x patterns.           ║
║     No concerns."                                                      ║
║    Confidence: HIGH                                                    ║
║                                                                        ║
║  prd-auditor:                                                          ║
║    "Deno-expert is well-structured but missing explicit               ║
║     differentiation from nodejs-expert in Identity section.           ║
║     Minor improvement suggested."                                      ║
║    Confidence: MEDIUM                                                  ║
║                                                                        ║
╠═══════════════════════════════════════════════════════════════════════╣
║  CONCERNS                                                              ║
╠═══════════════════════════════════════════════════════════════════════╣
║                                                                        ║
║  [LOW] deno-expert could clarify differentiation from nodejs-expert   ║
║                                                                        ║
╠═══════════════════════════════════════════════════════════════════════╣
║  RECOMMENDATION                                                        ║
╠═══════════════════════════════════════════════════════════════════════╣
║                                                                        ║
║  ┌────────────────────────────────────────────────────────────────┐   ║
║  │  ✅ RECOMMEND APPROVE                                           │   ║
║  │                                                                 │   ║
║  │  • typescript-pro improvements are high-quality                │   ║
║  │  • deno-expert adds value with minor suggested tweak           │   ║
║  │  • All structure validations pass                              │   ║
║  │  • Curation records present                                    │   ║
║  └────────────────────────────────────────────────────────────────┘   ║
║                                                                        ║
║  Optional comment to author:                                           ║
║  "Consider adding explicit differentiation from nodejs-expert in      ║
║   deno-expert's Identity section (e.g., 'Deno-first approach with    ║
║   native TypeScript, secure-by-default permissions model')."          ║
║                                                                        ║
╚═══════════════════════════════════════════════════════════════════════╝
```

## Recommendation Categories

| Recommendation | Meaning | Action |
|----------------|---------|--------|
| **APPROVE** | High-quality changes, ready to merge | turbobeest merges |
| **APPROVE WITH SUGGESTIONS** | Good changes, minor improvements optional | Merge now or wait for tweaks |
| **REQUEST CHANGES** | Issues that should be addressed | Author revises, re-review |
| **DECLINE** | Doesn't meet standards or conflicts with philosophy | Close with explanation |

## Validation Checks

### Structure Validation
- [ ] Frontmatter complete (name, tier, model, tools, modes)
- [ ] Identity section with interpretive lens
- [ ] Instructions section with Always/Mode-specific/Never
- [ ] Specializations defined
- [ ] Knowledge sources documented
- [ ] Output format specified

### Quality Validation
- [ ] Tier classification appropriate
- [ ] Model selection justified
- [ ] Knowledge sources authoritative
- [ ] Instructions non-conflicting
- [ ] Vocabulary calibrated (15-20 terms)

### Contribution Validation
- [ ] Curation record present (for new agents)
- [ ] No duplicate agents without differentiation
- [ ] Follows `-01-agent-formatting/` standards
- [ ] PR description explains rationale

## Agent Panel

The review uses a panel of agents:

| Agent | Role | Focus |
|-------|------|-------|
| `first-principles-engineer` | Quality arbiter | Is this fundamentally a good change? |
| `{domain-expert}` | Domain accuracy | Are domain-specific details correct? |
| `prd-auditor` | Standards compliance | Does it meet quality standards? |
| `architect-reviewer` | Structural coherence | Does the agent fit the ecosystem? |

## Integration

### GitHub CLI Commands Used

```bash
# Fetch PR details
gh pr view {number} --json title,author,body,files,headRefName,baseRefName

# Get diff
gh pr diff {number}

# Add review comment (after human approval)
gh pr review {number} --approve --body "..."
gh pr review {number} --request-changes --body "..."
```

### Signals

| Signal | Meaning |
|--------|---------|
| `PR_REVIEW_STARTED` | Analysis begun |
| `PR_VALIDATION_COMPLETE` | Structure checks done |
| `PR_ANALYSIS_COMPLETE` | Agent analysis done |
| `PR_RECOMMENDATION_READY` | Ready for human review |

## Human Override

The skill provides a recommendation, but **turbobeest makes the final decision**.

After reviewing the analysis:
- `[A]` Accept recommendation and merge
- `[R]` Request changes (with specific feedback)
- `[D]` Decline PR
- `[O]` Override recommendation with rationale

All decisions are logged in `.claude/pr-reviews/` for accountability.
