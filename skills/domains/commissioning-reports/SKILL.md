---
name: commissioning-reports
description: Building commissioning workflows including MBCx procedures, testing protocols, report generation, and energy conservation measure verification following ASHRAE Guideline 0 and NEBB standards
---

# Commissioning Reports Skill

This skill provides comprehensive guidance for building commissioning and retro-commissioning projects.

## Core Capabilities

### Commissioning Process
- MBCx planning and scoping
- Systems investigation procedures
- Testing and verification protocols
- Implementation tracking and verification

### Documentation and Reporting
- Commissioning plan development
- Test procedure creation
- Issues list management
- Final report generation

### Standards Compliance
- ASHRAE Guideline 0 procedures
- NEBB testing standards
- Local utility program requirements
- Energy savings verification

## Available Scripts
- scripts/test_scheduler.py: Generate testing schedules
- scripts/issues_tracker.py: Manage commissioning issues
- scripts/savings_calculator.py: Calculate energy savings

## Reference Materials
- eferences/ashrae_guideline0.md: ASHRAE Guideline 0 requirements
- eferences/test_procedures.md: Standard test procedures
- eferences/nebb_standards.md: NEBB testing standards

## Asset Templates
- ssets/commissioning_plan_template.docx: Standard Cx plan format
- ssets/test_forms/: Equipment testing forms
- ssets/report_template.docx: Final commissioning report template

## Usage Examples
- "Create a commissioning plan for this office building"
- "Generate test procedures for VAV box verification"
- "Calculate energy savings from this ECM implementation"
- "Track and manage commissioning issues list"


## Saving Next Steps

When commissioning-reports work is complete or paused:

```bash
node .claude/skills/work-command-center/tools/add-skill-next-steps.js \
  --skill "commissioning-reports" \
  --content "## Priority Tasks
1. Complete functional testing protocol
2. Document MBCx findings and recommendations
3. Generate commissioning report deliverable"
```

See: `.claude/skills/work-command-center/skill-next-steps-convention.md`
