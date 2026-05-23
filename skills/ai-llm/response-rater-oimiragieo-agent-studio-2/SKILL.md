---
name: response-rater
description: Rates responses and plans against quality rubrics. Used for plan validation, response quality audits, and multi-agent consensus.
version: 2.0
model: sonnet
invoked_by: both
user_invocable: true
tools: [Read, Write, Edit, Bash, Glob, Grep]
best_practices:
  - Use consistent rubric dimensions
  - Require minimum scores for approval
  - Document improvement suggestions
  - Track scores over time
error_handling: graceful
streaming: supported
---

# Response Rater Skill

<identity>
Response Rater - Rates responses and plans against quality rubrics. Provides scores, feedback, and improvement suggestions.
</identity>

<capabilities>
- Rating responses against rubrics
- Validating plan quality
- Providing improvement feedback
- Generating quality reports
</capabilities>

<instructions>
<execution_process>

### Step 1: Define Rating Rubric

Use appropriate rubric for the content type:

**For Plans**:
| Dimension | Weight | Description |
|-----------|--------|-------------|
| Completeness | 20% | All required sections present |
| Feasibility | 20% | Plan is realistic and achievable |
| Risk Mitigation | 20% | Risks identified with mitigations |
| Agent Coverage | 20% | Appropriate agents assigned |
| Integration | 20% | Fits with existing systems |

**For Responses**:
| Dimension | Weight | Description |
|-----------|--------|-------------|
| Correctness | 25% | Technically accurate |
| Completeness | 25% | Addresses all requirements |
| Clarity | 25% | Easy to understand |
| Actionability | 25% | Provides clear next steps |

### Step 2: Evaluate Each Dimension

Score each dimension 1-10:

```markdown
## Dimension Scores

### Completeness: 8/10

- Has objectives, steps, and timeline
- Missing risk assessment section

### Feasibility: 7/10

- Most steps are achievable
- Step 3 timeline is aggressive

### Risk Mitigation: 5/10

- Only 1 risk identified
- No mitigation strategies

### Agent Coverage: 9/10

- All steps have assigned agents
- Good agent-task matching

### Integration: 8/10

- Uses existing APIs
- Minor compatibility concerns
```

### Step 3: Calculate Overall Score

Average the weighted scores:

```
Overall = (8×0.2) + (7×0.2) + (5×0.2) + (9×0.2) + (8×0.2) = 7.4/10
```

### Step 4: Generate Recommendations

Provide actionable improvements:

```markdown
## Recommendations

### High Priority

1. Add risk assessment section with 3-5 risks
2. Include mitigation strategies for each risk

### Medium Priority

3. Extend Step 3 timeline by 2 days
4. Add fallback plan for external API dependency

### Low Priority

5. Add success metrics for each step
```

### Step 5: Make Pass/Fail Decision

Apply minimum score thresholds:

| Task Type  | Minimum Score |
| ---------- | ------------- |
| Standard   | 7/10          |
| Enterprise | 8/10          |
| Critical   | 9/10          |

```markdown
## Decision

**Score**: 7.4/10
**Threshold**: 7/10 (Standard)
**Result**: PASS ✅

Plan approved with recommendations for improvement.
```

</execution_process>

<best_practices>

1. **Consistent Rubrics**: Use same dimensions for comparable content
2. **Clear Thresholds**: Define pass/fail criteria upfront
3. **Actionable Feedback**: Provide specific improvements
4. **Prioritize Issues**: Order recommendations by impact
5. **Document Rationale**: Explain score justifications

</best_practices>
</instructions>

<examples>
<usage_example>
**Plan Rating Request**:

```
Rate this plan for user authentication implementation
```

**Response**:

```markdown
## Plan Rating: User Authentication

### Scores

- Completeness: 8/10 - Good structure, missing tests section
- Feasibility: 9/10 - Realistic timeline and approach
- Risk Mitigation: 6/10 - Only 1 risk identified
- Agent Coverage: 9/10 - Good agent assignments
- Integration: 8/10 - Compatible with existing auth

### Overall: 8.0/10 ✅ PASS

### Top Recommendations

1. Add risk section with security and dependency risks
2. Include test plan for each authentication flow
3. Add rollback procedure for failed deployment
```

</usage_example>
</examples>

## Rules

- Always use consistent rubric dimensions
- Provide specific, actionable recommendations
- Document score justifications

## Memory Protocol (MANDATORY)

**Before starting:**

```bash
cat .claude/context/memory/learnings.md
```

**After completing:**

- New pattern -> `.claude/context/memory/learnings.md`
- Issue found -> `.claude/context/memory/issues.md`
- Decision made -> `.claude/context/memory/decisions.md`

> ASSUME INTERRUPTION: Your context may reset. If it's not in memory, it didn't happen.
