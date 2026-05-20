---
name: ralph-skill-review-loop
description: Self-improving review loop for Ralph Wiggum skills. Reviews skills against best practices, implements improvements, and continues until two consecutive clean reviews. Use when validating or improving the ralph-prompt-* skill suite.
---

# Ralph Skill Review Loop

## Overview

A meta-skill that uses the Ralph Wiggum technique to review and improve the Ralph Wiggum prompt generator skills themselves. Runs a continuous improvement loop until skills pass review twice consecutively with no recommendations.

## Quick Start

Copy and run this prompt in a Ralph loop:

```bash
/ralph-wiggum:ralph-loop "[paste prompt below]" --completion-promise "RALPH_SKILLS_PERFECTED" --max-iterations 100
```

---

## THE SELF-IMPROVING REVIEW LOOP PROMPT

```markdown
# Task: Self-Improving Review of Ralph Wiggum Skills

## Objective
Review and improve the Ralph Wiggum prompt generator skills until they pass two consecutive reviews with zero improvement recommendations.

## Target Skills
1. ralph-prompt-builder (Master orchestrator)
2. ralph-prompt-single-task (Single task generator)
3. ralph-prompt-multi-task (Multi-task generator)
4. ralph-prompt-project (Project generator)
5. ralph-prompt-research (Research generator)

Location: .claude/skills/ralph-prompt-*/SKILL.md

## Reference Materials
- RALPH-WIGGUM-TECHNIQUE-COMPREHENSIVE-RESEARCH.md (12,000+ words of best practices)
- skill-builder-package/research/ (skill building best practices)
- skill-builder-package/examples/ (production skill patterns)

---

## STATE MANAGEMENT

### Required State Files
Create these files to track progress:

**RALPH_REVIEW_STATE.json**:
```json
{
  "current_iteration": 1,
  "consecutive_clean_reviews": 0,
  "skills_reviewed": [],
  "improvements_made": [],
  "last_review_timestamp": "",
  "status": "IN_PROGRESS"
}
```

**RALPH_REVIEW_LOG.md**:
```markdown
# Ralph Skills Review Log

## Iteration History
[Append each iteration's findings here]
```

---

## STEP 1: ORIENTATION (Every Iteration)

Read current state:
```bash
cat RALPH_REVIEW_STATE.json
cat RALPH_REVIEW_LOG.md | tail -50
git log --oneline -5
ls -la .claude/skills/ralph-prompt-*/
```

Check: How many consecutive clean reviews do we have?
- If 2 or more: Output <promise>RALPH_SKILLS_PERFECTED</promise>
- If less than 2: Continue to Step 2

---

## STEP 2: COMPREHENSIVE SKILL REVIEW

### Review Framework
For EACH skill in ralph-prompt-*, evaluate against:

#### 2.1 Ralph Technique Alignment (from research)
- [ ] Clear completion criteria defined
- [ ] Includes self-verification commands
- [ ] Has TDD/iteration approach
- [ ] Includes "If Stuck" guidance
- [ ] Uses <promise> completion tags correctly
- [ ] Recommends appropriate max-iterations
- [ ] Follows "deterministically bad" philosophy (failures are fixable)

#### 2.2 Skill Structure Quality
- [ ] YAML frontmatter complete (name, description with triggers)
- [ ] Progressive disclosure (overview → details → examples)
- [ ] Quick Start section exists and is actionable
- [ ] Examples are realistic and complete
- [ ] Best practices section included
- [ ] Integration with Ralph loop documented

#### 2.3 Content Completeness
- [ ] All sections properly filled (no placeholders)
- [ ] Examples match the skill type
- [ ] Verification commands are real and runnable
- [ ] Edge cases addressed
- [ ] Cross-references to related skills

#### 2.4 Prompt Template Quality
- [ ] Templates follow research best practices
- [ ] Success criteria are measurable
- [ ] Phase structure is clear (for multi-phase)
- [ ] State tracking included
- [ ] Progress tracking pattern included

### Review Process
For each skill:
1. Read the SKILL.md file completely
2. Compare against RALPH-WIGGUM-TECHNIQUE-COMPREHENSIVE-RESEARCH.md
3. Check against all 16 criteria above
4. Document findings in REVIEW_FINDINGS.md

### Review Output Format
Create/update **REVIEW_FINDINGS.md**:
```markdown
# Review Findings - Iteration [N]

## Summary
- Skills reviewed: [count]
- Total issues found: [count]
- Critical issues: [count]
- Improvements needed: [count]

## ralph-prompt-builder
### Passing
- [x] Criterion that passes

### Issues Found
- [ ] [CRITICAL/HIGH/MEDIUM/LOW] Issue description
  - Location: [section/line]
  - Current: [what exists]
  - Should be: [what it should be]
  - Fix: [specific fix]

## ralph-prompt-single-task
[... same format]

## ralph-prompt-multi-task
[... same format]

## ralph-prompt-project
[... same format]

## ralph-prompt-research
[... same format]

## Recommendations Summary
### Must Fix (Critical/High)
1. [Recommendation 1]
2. [Recommendation 2]

### Should Fix (Medium)
1. [Recommendation 3]

### Nice to Have (Low)
1. [Recommendation 4]

## Review Result
- [ ] CLEAN (zero recommendations)
- [ ] NEEDS_WORK (has recommendations)
```

---

## STEP 3: IMPLEMENT IMPROVEMENTS

If REVIEW_FINDINGS.md shows NEEDS_WORK:

### 3.1 Prioritize Fixes
Work in this order:
1. Critical issues (breaks functionality)
2. High issues (significantly impacts quality)
3. Medium issues (improves quality)
4. Low issues (polish)

### 3.2 Implement Each Fix
For each recommendation:

1. Read the target skill file
2. Implement the specific fix
3. Verify the fix addresses the issue
4. Commit the change:
```bash
git add .claude/skills/ralph-prompt-[name]/SKILL.md
git commit -m "Improve ralph-prompt-[name]: [brief description]

- [Change 1]
- [Change 2]

Part of Ralph skills self-improvement loop iteration [N]"
```

### 3.3 Track Improvements
Update RALPH_REVIEW_STATE.json:
```json
{
  "improvements_made": [
    {
      "iteration": N,
      "skill": "ralph-prompt-X",
      "issue": "description",
      "fix": "what was done"
    }
  ]
}
```

---

## STEP 4: POST-IMPROVEMENT VERIFICATION

After implementing fixes:

### 4.1 Verify Each Skill Still Works
For each modified skill:
- [ ] YAML frontmatter is valid
- [ ] All sections render correctly
- [ ] Examples are syntactically correct
- [ ] No broken references

### 4.2 Check for Regressions
- [ ] No content accidentally deleted
- [ ] Cross-references still valid
- [ ] Templates still complete

### 4.3 Run Syntax Check
```bash
# Verify YAML frontmatter
for f in .claude/skills/ralph-prompt-*/SKILL.md; do
  head -20 "$f" | grep -E "^(name:|description:)"
done
```

---

## STEP 5: UPDATE STATE

Update RALPH_REVIEW_STATE.json:

If review was CLEAN (zero recommendations):
```json
{
  "consecutive_clean_reviews": [previous + 1],
  "last_review_result": "CLEAN",
  "last_review_timestamp": "[timestamp]"
}
```

If review was NEEDS_WORK:
```json
{
  "consecutive_clean_reviews": 0,
  "last_review_result": "NEEDS_WORK",
  "improvements_this_iteration": [count],
  "last_review_timestamp": "[timestamp]"
}
```

Update RALPH_REVIEW_LOG.md:
```markdown
## Iteration [N] - [timestamp]

### Review Result
[CLEAN/NEEDS_WORK]

### Issues Found
- [Issue 1]
- [Issue 2]

### Fixes Applied
- [Fix 1]
- [Fix 2]

### State After
- Consecutive clean reviews: [N]
- Total improvements to date: [N]
```

---

## STEP 6: LOOP DECISION

### Check Termination Condition
Read RALPH_REVIEW_STATE.json:

```bash
cat RALPH_REVIEW_STATE.json | jq '.consecutive_clean_reviews'
```

### If consecutive_clean_reviews >= 2:
Skills have passed two consecutive reviews with zero recommendations.

Create RALPH_SKILLS_VALIDATION_COMPLETE.md:
```markdown
# Ralph Skills Validation Complete

## Summary
- Total iterations: [N]
- Total improvements made: [count]
- Final state: All skills validated

## Skills Validated
1. ralph-prompt-builder - PASSED
2. ralph-prompt-single-task - PASSED
3. ralph-prompt-multi-task - PASSED
4. ralph-prompt-project - PASSED
5. ralph-prompt-research - PASSED

## Validation Criteria Met
All 16 review criteria passing for all 5 skills.

## Timestamp
[ISO timestamp]
```

Output: <promise>RALPH_SKILLS_PERFECTED</promise>

### If consecutive_clean_reviews < 2:
Continue to next iteration (loop back to STEP 1)

---

## REVIEW CRITERIA REFERENCE (Quick Check)

### Ralph Technique Alignment
1. Clear completion criteria
2. Self-verification commands
3. TDD/iteration approach
4. "If Stuck" guidance
5. <promise> tags used correctly
6. Appropriate max-iterations recommendations
7. Deterministically bad philosophy

### Skill Structure Quality
8. Complete YAML frontmatter
9. Progressive disclosure
10. Actionable Quick Start
11. Realistic examples
12. Best practices section
13. Ralph loop integration docs

### Content Completeness
14. No placeholders
15. Matching examples
16. Real verification commands

---

## ESCAPE HATCH

If stuck after 50 iterations without reaching 2 consecutive clean reviews:

1. Document the recurring issues in RALPH_REVIEW_BLOCKERS.md
2. List which criteria keep failing
3. Identify if criteria are too strict
4. Output: <promise>RALPH_REVIEW_BLOCKED</promise>

---

## PROGRESS TRACKING

Every 5 iterations, summarize:
```
PROGRESS SUMMARY - Iteration [N]
================================
Started: [timestamp]
Current: [timestamp]
Consecutive clean reviews: [N]/2

Skills Status:
- ralph-prompt-builder: [X/16 criteria passing]
- ralph-prompt-single-task: [X/16 criteria passing]
- ralph-prompt-multi-task: [X/16 criteria passing]
- ralph-prompt-project: [X/16 criteria passing]
- ralph-prompt-research: [X/16 criteria passing]

Improvements made: [total count]
Remaining issues: [count]
```

---

## COMPLETION CONDITIONS

Output <promise>RALPH_SKILLS_PERFECTED</promise> ONLY when:
- [ ] All 5 skills reviewed
- [ ] All 16 criteria checked per skill
- [ ] Zero recommendations in current review
- [ ] Zero recommendations in previous review
- [ ] consecutive_clean_reviews >= 2 in state file
- [ ] RALPH_SKILLS_VALIDATION_COMPLETE.md created
- [ ] All changes committed

---

## SAFETY LIMITS

- Maximum iterations: 100
- Expected completion: 20-40 iterations
- Budget alert: If > 50 iterations, evaluate if criteria are too strict
```

---

## Usage Instructions

### 1. Initialize State Files

Before running, create the initial state:

```bash
# Create state file
cat > RALPH_REVIEW_STATE.json << 'EOF'
{
  "current_iteration": 0,
  "consecutive_clean_reviews": 0,
  "skills_reviewed": [],
  "improvements_made": [],
  "last_review_timestamp": "",
  "status": "NOT_STARTED"
}
EOF

# Create log file
cat > RALPH_REVIEW_LOG.md << 'EOF'
# Ralph Skills Review Log

## Overview
Self-improving review loop for Ralph Wiggum prompt generator skills.

## Target: Two consecutive clean reviews

---

## Iteration History

EOF
```

### 2. Run the Loop

```bash
/ralph-wiggum:ralph-loop "[THE PROMPT ABOVE]" \
  --completion-promise "RALPH_SKILLS_PERFECTED" \
  --max-iterations 100
```

### 3. Monitor Progress

```bash
# Check current state
cat RALPH_REVIEW_STATE.json | jq '.'

# See recent activity
tail -30 RALPH_REVIEW_LOG.md

# Check how many clean reviews
cat RALPH_REVIEW_STATE.json | jq '.consecutive_clean_reviews'
```

### 4. After Completion

Review the outputs:
- `RALPH_REVIEW_STATE.json` - Final state
- `RALPH_REVIEW_LOG.md` - Complete history
- `REVIEW_FINDINGS.md` - Last review details
- `RALPH_SKILLS_VALIDATION_COMPLETE.md` - Success certificate
- Git log - All improvements committed

---

## Why This Works

1. **State Tracking**: JSON state file persists across iterations
2. **Clear Criteria**: 16 specific, measurable review criteria
3. **Self-Correction**: Each iteration reads previous results and fixes issues
4. **Termination Condition**: Two consecutive clean reviews ensures stability
5. **Evidence-Based**: All findings documented, all fixes tracked
6. **Git Integration**: Every improvement committed for auditability

---

## Expected Behavior

**Iteration 1-5**: Discovery phase
- Identify initial issues across all skills
- Begin fixing critical issues

**Iteration 6-15**: Improvement phase
- Systematic fixes
- Quality improvements
- Cross-consistency

**Iteration 16-25**: Stabilization phase
- Fewer issues found
- Polish and edge cases
- Approaching clean reviews

**Iteration 26-40**: Validation phase
- First clean review achieved
- Verify no regressions
- Second clean review achieved
- Completion

---

## Customization

### Stricter Review
Add more criteria to the review framework.

### Faster Completion
Reduce to "one clean review" by changing:
```
consecutive_clean_reviews >= 1
```

### Focus on Specific Skills
Modify the target skills list in the prompt.
