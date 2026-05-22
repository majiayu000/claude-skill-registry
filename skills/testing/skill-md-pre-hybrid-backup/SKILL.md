---
name: frontend-qc
description: Performs comprehensive frontend quality assurance reviews using browser automation. Systematically tests UI elements, discovers and reports bugs to GitHub Issues, and provides improvement recommendations. Uses Chrome DevTools MCP for interactive testing. This skill should be used when performing quality assurance reviews of frontend UI components, testing user interfaces for bugs or usability issues, validating frontend implementations before deployment, or conducting systematic UI testing across multiple components.
allowed-tools: mcp__chrome-devtools__*, Skill(report-bug), Skill(email), Read, Write
---

# Frontend Quality Assurance

## Overview

Autonomous frontend quality assurance agent that performs comprehensive UI testing, bug discovery, and automated reporting using browser automation. Systematically validates UI elements, identifies issues, creates GitHub bug reports, and provides improvement recommendations.

## Core Workflow

Execute quality assurance testing through six systematic phases:

### Phase 0: Validate Prerequisites

**Before starting QA testing, verify all required tools and services:**

1. **Chrome DevTools MCP Connection**
   - List available pages: `mcp__chrome-devtools__list_pages`
   - If fails: STOP immediately - user must configure Chrome DevTools MCP server
   - Load troubleshooting if needed: `Read(@references/troubleshooting.md)`

2. **Application Accessibility**
   - Navigate to application URL (provided or default: http://localhost:4000)
   - If fails: STOP immediately - user must start application
   - Document error for troubleshooting

3. **Required Skills Availability**
   - Verify `report-bug` skill exists: Check `~/.claude/skills/report-bug/`
   - Verify `email` skill exists: Check `~/.claude/skills/email/`
   - If missing: Warn user, continue without GitHub/email features

**Progress Logging:**
- Create progress log file: `Write(@~/.claude/skills/frontend-qc/progress.log)` at start
- Update log after each phase with timestamp, phase name, status, and findings
- Log format: `[YYYY-MM-DD HH:MM:SS] PHASE_NAME: STATUS - Details`
- On error/interruption: Log current state for resumption
- Final log entry: Complete summary with all results

**Validation Results:**
- ✅ All checks pass → Log `PHASE_0_VALIDATION: PASSED` → Proceed to Phase 1
- ❌ Critical failure (MCP or app) → Log `PHASE_0_VALIDATION: FAILED - [error]` → STOP
- ⚠️ Warning (missing skills) → Log `PHASE_0_VALIDATION: WARNING - [missing features]` → Continue with limited features

### Phase 1: Gather Requirements

**Log Entry**: `[timestamp] PHASE_1_REQUIREMENTS: STARTED`

**If UI elements not specified:**
- STOP and ask user: Which elements/pages to test? Application URL? Test scenarios? Bug priority?

**Collect:**
- Target UI elements/pages to test
- Expected behaviors and acceptance criteria
- Test credentials (or use defaults from `Read(@references/test-credentials.md)`)

**For SoftTrak-specific testing:**
- Load SoftTrak workflows and scenarios: `Read(@references/softtrak-scenarios.md)`
- Contains: Critical user journeys, known issue areas, role-based testing, regression priorities

**Log Entry**: `[timestamp] PHASE_1_REQUIREMENTS: COMPLETED - Testing [N] elements: [element list]`

### Phase 2: Setup & Authenticate

**Log Entry**: `[timestamp] PHASE_2_SETUP: STARTED - URL: [app_url]`

Execute setup sequence:
1. Launch browser page with Chrome DevTools MCP
2. Navigate to application URL
3. Authenticate with test credentials
4. Take baseline screenshot for reference
5. Verify dashboard access and application state

**For detailed Chrome DevTools commands:**
- Load command reference as needed: `Read(@references/devtools-commands.md)`

**Log Entry**: `[timestamp] PHASE_2_SETUP: COMPLETED - Authentication: [SUCCESS/FAILED], Dashboard: [ACCESSIBLE/INACCESSIBLE]`

### Phase 3: Systematic Testing

**Log Entry**: `[timestamp] PHASE_3_TESTING: STARTED - Element [N of M]: [element_name]`

**For EACH UI element specified:**

1. **Navigate**: Go to element, take screenshot, verify load
2. **Test**: Apply appropriate testing checklist based on element type
3. **Monitor**: Check console errors throughout interaction
4. **Document**: Capture evidence of any issues discovered

**Load testing checklists as needed:**
- Forms: `Read(@references/form-testing.md)`
- Tables/Grids: `Read(@references/table-testing.md)`
- Modals/Dialogs: `Read(@references/modal-testing.md)`
- Navigation: `Read(@references/navigation-testing.md)`
- General accessibility: `Read(@references/accessibility-testing.md)`

**Log Entry per element**: `[timestamp] PHASE_3_TESTING: ELEMENT_COMPLETE - [element_name]: [PASS/ISSUES_FOUND] - [issue_count] issues, [console_error_count] console errors`

**Log Entry**: `[timestamp] PHASE_3_TESTING: COMPLETED - Tested [N] elements, Found [M] total issues`

### Phase 4: Report Bugs

**Log Entry**: `[timestamp] PHASE_4_BUG_REPORTING: STARTED - [M] issues to report`

**For EACH discovered issue:**

1. Capture evidence (screenshot, console output, reproduction steps)
2. Classify issue (severity, type, impact)
3. Load bug template: `Read(@references/bug-template.md)`
4. Create GitHub issue using `Skill(report-bug)`

**Log Entry per bug**: `[timestamp] PHASE_4_BUG_REPORTING: BUG_REPORTED - Issue #[number]: [title] (Severity: [severity])`

**Log Entry**: `[timestamp] PHASE_4_BUG_REPORTING: COMPLETED - Created [N] GitHub issues`

### Phase 5: Document Improvements

**Log Entry**: `[timestamp] PHASE_5_IMPROVEMENTS: STARTED - [K] enhancement opportunities identified`

After testing each element:

1. Compile usability/accessibility/performance recommendations
2. Load feature request template: `Read(@references/feature-template.md)`
3. Create feature request using `Skill(report-bug)` with enhancement labels

**Log Entry per improvement**: `[timestamp] PHASE_5_IMPROVEMENTS: ENHANCEMENT_DOCUMENTED - Issue #[number]: [title] (Impact: [impact])`

**Log Entry**: `[timestamp] PHASE_5_IMPROVEMENTS: COMPLETED - Created [K] enhancement requests`

### Phase 6: Generate Summary

**Log Entry**: `[timestamp] PHASE_6_SUMMARY: STARTED - Compiling final report`

After all elements tested:

1. Compile comprehensive summary (elements reviewed, bugs found, recommendations)
2. Send email report using `Skill(email)` with:
   - Executive summary with key findings
   - Links to all created GitHub issues
   - Recommended next steps and priorities

**Log Entry**: `[timestamp] PHASE_6_SUMMARY: COMPLETED - Email sent, Session complete`

**Final Log Summary**:
```
[timestamp] QA_SESSION_COMPLETE
Elements Tested: [N]
Bugs Found: [M] (Critical: [X], High: [Y], Medium: [Z], Low: [W])
Enhancements: [K]
GitHub Issues Created: [M+K]
Email Sent: YES
Status: SUCCESS
```

## Error Handling

**Authentication fails**: Document as bug, try alternatives, request user guidance
**Navigation fails**: Document routing bug, try alternatives, continue with accessible elements
**Chrome DevTools connection lost**: Document failure point, attempt reconnect, save progress to log

**For troubleshooting help:**
- Load troubleshooting guide: `Read(@references/troubleshooting.md)`

## Success Criteria

- ✅ All specified UI elements tested systematically
- ✅ All bugs reported to GitHub with evidence
- ✅ Improvement recommendations documented
- ✅ Summary email sent to user with links
- ✅ No critical bugs left undocumented
- ✅ Progress log complete with session summary

## Resources

### references/

Documentation and testing checklists that inform the QA process:

- `accessibility-testing.md` - WCAG compliance and accessibility validation checklist
- `bug-template.md` - Structured template for bug report creation
- `devtools-commands.md` - Chrome DevTools MCP command reference
- `feature-template.md` - Enhancement request template for improvements
- `form-testing.md` - Comprehensive form element testing checklist
- `modal-testing.md` - Modal/dialog interaction testing checklist
- `navigation-testing.md` - Navigation and routing validation checklist
- `table-testing.md` - Data table/grid testing checklist
- `test-credentials.md` - Project-specific test account credentials
- `softtrak-scenarios.md` - SoftTrak-specific testing scenarios and workflows
- `troubleshooting.md` - Common issues and resolution strategies
