---
name: execute-checklist
description: Use to systematically validate documents, stories, or processes against defined checklists. Ensures quality and completeness.
version: 1.0.0
---
<!-- Powered by PRISMâ„¢ Core -->

# Execute Checklist Task

## Purpose

Systematically validate documents, stories, or processes against defined checklists to ensure quality and completeness.

## Available Checklists

Check ../checklists/ folder for:
- story-dod-checklist.md - Story definition of done
- story-draft-checklist.md - Story draft validation  
- sprint-planning-checklist.md - Sprint planning completeness
- retrospective-checklist.md - Retrospective effectiveness
- strangler-migration-checklist.md - Legacy migration validation

## Instructions

### 1. Initial Assessment

**Determine Checklist:**
- If user provides checklist name, fuzzy match it
- If multiple matches, ask for clarification
- If none specified, list available options
- Load checklist from ../checklists/

**Choose Processing Mode:**
- **Interactive**: Section by section with discussion
- **YOLO** (recommended): Process all at once, summary at end

### 2. Document Gathering

Each checklist specifies required artifacts:
- Stories may need: PRD, architecture, epics
- Sprint planning needs: backlog, velocity data
- Retrospective needs: sprint metrics, burndown

Locate documents per checklist requirements.

### 3. Checklist Processing

**Interactive Mode:**
For each section:
- Review all items per section instructions
- Check against documentation/artifacts
- Present findings (warnings, errors, N/A items)
- Get confirmation before proceeding
- Halt on major issues if needed

**YOLO Mode:**
- Process all sections sequentially
- Create comprehensive report
- Present complete analysis
- Highlight critical issues

### 4. Validation Approach

For each item:
```yaml
validation:
  item: "Checklist item text"
  status: "[x] Complete | [ ] Missing | [!] Warning | [N/A] Not Applicable"
  finding: "What was found or missing"
  severity: "Critical | Major | Minor | Info"
  recommendation: "Specific action if needed"
  evidence: "Link to doc/section supporting status"
```

### 5. Scoring (If Applicable)

Some checklists include scoring:
```yaml
scoring:
  section_scores:
    requirements: 8/10
    design: 7/10
    testing: 9/10
  total_score: 24/30 (80%)
  threshold: 75% (PASS/FAIL)
  confidence: "High | Medium | Low"
```

### 6. Generate Report

**Report Structure:**
```markdown
# Checklist Validation Report

## Summary
- Checklist: {name}
- Document: {what was validated}
- Date: {timestamp}
- Mode: {Interactive|YOLO}
- Overall Status: {PASS|FAIL|CONDITIONAL}

## Critical Findings
[List any blockers or critical issues]

## Section Results

### Section 1: {Name}
- Items Checked: X
- Passed: Y
- Warnings: Z
- Not Applicable: W

Key Findings:
- [Finding 1]
- [Finding 2]

### Section 2: {Name}
[Continue for all sections]

## Recommendations

### Immediate Actions
1. {Critical fix needed}
2. {Blocker to resolve}

### Improvements
1. {Enhancement suggestion}
2. {Process improvement}

## Metrics
- Total Items: X
- Compliance Rate: Y%
- Critical Issues: Z
- Estimated Fix Time: {hours}

## Next Steps
1. Address critical issues
2. Review with team
3. Update documentation
4. Re-run validation
```

### 7. PSP/TSP Integration

For story checklists, include:
- Estimation accuracy check
- Size category validation
- Time tracking fields present
- Historical proxy appropriateness

For sprint checklists:
- Team role assignments complete
- Velocity goals defined
- Quality metrics established  
- Measurement plan in place

### 8. Follow-Up Actions

Based on validation results:

**If PASS:**
- Document approval
- Proceed with next phase
- Archive validation report

**If CONDITIONAL:**
- List specific conditions
- Set review checkpoint
- Assign resolution owners

**If FAIL:**
- Stop progression
- Document blockers
- Create fix tasks
- Schedule re-validation

## Success Criteria

- [ ] Checklist fully processed
- [ ] All items validated with evidence
- [ ] Report generated with findings
- [ ] Recommendations documented
- [ ] Next steps clear
- [ ] Stakeholders informed

## Output

- Validation report (markdown)
- Updated checklist with statuses
- Action items if needed
- Metrics for tracking
