---
name: production-debugging-framework
description: Comprehensive production debugging and verification framework for Vue 3 + TypeScript applications. Use when facing any compilation errors, runtime issues, or need systematic debugging workflows.
---

# Production Debugging Framework

## Overview

A comprehensive debugging and verification framework that provides systematic workflows for resolving Vue 3 + TypeScript compilation and runtime errors. This skill transforms chaotic debugging sessions into structured, efficient problem-solving processes with zero-error tolerance.

## When to Use This Skill

**Immediate Activation Required:**
- TypeScript compilation errors (any type)
- Vite build failures
- Import/module resolution errors
- Component rendering issues
- Runtime errors in browser
- Test failures
- Any development blocker

**Preventive Use:**
- Before committing code
- Before creating pull requests
- After major refactoring
- During feature development
- Production deployment preparation

## Core Capabilities

### 1. Zero-Error Verification System
7-phase systematic verification before any development:
1. **Working Baseline** - Confirm recent passing state
2. **Clear All Errors** - Start with clean slate
3. **Partial Build Fix** - Fix surface-level issues first
4. **TypeScript Foundation** - Restore structural integrity
5. **CSS/Design System** - Fix styling inconsistencies
6. **Critical Functionality** - Restore core workflows
7. **Deep Error Resolution** - Handle remaining complex issues

### 2. Error-Specific Debugging Protocols

#### TypeScript Structural Errors (skill://ts-foundation-restorer)
**Trigger**: TS2339, TS2345, TS2322, TS7005, missing properties
**Protocol**:
- Read entire file context
- Cross-reference with interfaces/types
- Update ALL affected locations
- Validate with typecheck command

#### Import/Module Resolution Errors
**Trigger**: Module not found, import path failures
**Protocol**:
- Use `npm run validate:imports` for detection
- Check actual file paths vs imports
- Update import statements systematically
- Verify barrel exports consistency

#### Component Reference Errors
**Trigger**: Component failed to resolve, render failures
**Protocol**:
- Verify component registration
- Check import/export consistency
- Validate component naming conventions
- Test with explicit imports

### 3. Master Debugging Workflow

Copy and paste this master prompt whenever encountering errors:

```
I have a [ERROR TYPE] error in my Vue 3 + TypeScript project.

CONTEXT:
- Project: Pomo-Flow (Vue 3 + TypeScript + Vite + Pinia)
- Latest Working: [describe last working state]
- Current Error: [paste exact error message]
- Error Location: [file:line or component]
- Recent Changes: [what changed since working state]

DEBUGGING REQUIREMENTS:
1. Use production-debugging-framework skill
2. Follow 7-phase zero-error verification
3. Apply error-specific protocol for [ERROR TYPE]
4. Read full files for complete context
5. Document the fix and root cause
6. Verify fix with appropriate validation command
7. Confirm return to working state

ERROR DETAILS:
[Paste full error output with stack trace]
```

### 4. Production Stability Audit

5-phase comprehensive testing before deployment:

#### Phase 1: Zero-Error Validation
- All compilation errors resolved
- TypeScript compilation passes (`npm run typecheck`)
- No console errors in browser
- All linter issues resolved

#### Phase 2: Build Process Integrity
- Production build succeeds (`npm run build`)
- Bundle analysis shows no unexpected increases
- Critical dependencies are properly bundled
- No missing assets or broken imports

#### Phase 3: Core Functionality Testing
- Task creation workflow works
- Canvas interactions functional
- Timer operations stable
- Data persistence verified (IndexedDB)
- View switching works properly

#### Phase 4: Browser Compatibility
- Chrome/Chromium compatibility
- Firefox compatibility
- Safari/WebKit compatibility
- Mobile browser functionality
- Cross-tab synchronization

#### Phase 5: Performance Validation
- Application startup time < 3 seconds
- Memory usage stable during operations
- No memory leaks during extended use
- Canvas interactions remain responsive
- IndexedDB operations performant

### 5. Common Error Patterns and Solutions

#### Pattern 1: Cascading TypeScript Failures
**Symptoms**: 100+ TS errors after dependency update
**Solution**: Use ts-foundation-restorer skill immediately
**Protocol**: Restore foundation before fixing individual errors

#### Pattern 2: Vite Build Path Resolution
**Symptoms**: Module not found in production build
**Solution**: Verify import paths and barrel exports
**Protocol**: Use `npm run validate:imports` and check index.ts files

#### Pattern 3: Component Registration Failures
**Symptoms**: Component failed to resolve
**Solution**: Check component naming and import consistency
**Protocol**: Verify component registration and imports

#### Pattern 4: Canvas/Dragging Issues
**Symptoms**: Vue Flow interactions not working
**Solution**: Check Vue Flow parent-child relationships
**Protocol**: Verify extent constraints and event handling

### 6. Validation Commands

Use these commands systematically during debugging:

```bash
# TypeScript compilation
npm run typecheck

# Import validation
npm run validate:imports

# CSS validation
npm run validate:css

# Dependency checks
npm run validate:dependencies

# Full validation suite
npm run validate:all

# Production build test
npm run build

# Test suite
npm run test
```

### 7. Documentation Requirements

Every debugging session must include:

#### Before Fixing
- Exact error message and stack trace
- File and line location
- Recent changes that may have caused the issue
- Current working state (what works)

#### After Fixing
- Root cause analysis
- Specific change made
- Files affected
- Validation command used
- Confirmation of working state

#### Knowledge Transfer
- Update related documentation if needed
- Note any patterns discovered
- Record solutions for future reference

## Resources

### references/
Contains detailed debugging guides and protocols:

- `master-prompt.md` - Copy-paste debugging prompt template
- `zero-error-verification.md` - Detailed 7-phase verification process
- `production-audit.md` - 5-phase production stability checklist
- `error-guides/` - Specific protocols for each error type:
  - `typescript-structural.md` - TS2339, TS2345, TS2322 handling
  - `imports-modules.md` - Module resolution and import path fixes
  - `runtime-errors.md` - Browser runtime error debugging
  - `component-refs.md` - Component registration and resolution issues

### scripts/
Automation scripts for systematic debugging:

- `error-detector.py` - Automated error classification and routing
- `validation-runner.sh` - Sequential validation command execution
- `typescript-fixer.py` - Automated TypeScript structural repairs
- `import-fixer.py` - Import path resolution and correction

### assets/
Templates and checklists:

- `debugging-checklist.md` - Printable debugging workflow checklist
- `error-report-template.md` - Standardized error reporting format
- `production-audit-checklist.md` - Pre-deployment verification checklist

## Usage Examples

### Example 1: TypeScript Compilation Error
```
User: "I'm getting TS2339: Property 'tasks' does not exist on type..."

System: Activates production-debugging-framework
→ Applies TypeScript structural error protocol
→ Uses ts-foundation-restorer if cascade detected
→ Reads full file context
→ Updates all affected interfaces
→ Validates with npm run typecheck
→ Confirms working state restored
```

### Example 2: Build Process Failure
```
User: "Production build fails with module not found error"

System: Activates production-debugging-framework
→ Runs 7-phase zero-error verification
→ Uses import validation protocol
→ Checks barrel exports and file paths
→ Fixes import statements systematically
→ Validates with npm run build
→ Confirms build success
```

### Example 3: Runtime Component Error
```
User: "Component failed to resolve in browser console"

System: Activates production-debugging-framework
→ Applies component reference error protocol
→ Checks component registration and imports
→ Validates component naming conventions
→ Tests with explicit imports
→ Verifies in browser
→ Confirms resolution
```

## Integration With Other Skills

- **ts-foundation-restorer**: Automatic activation for TypeScript cascades
- **dev-debugging**: General Vue.js debugging techniques
- **dev-fix-pinia**: Store-specific debugging protocols
- **dev-fix-timer**: Timer component debugging
- **qa-testing**: Validation through automated testing

## Quality Assurance

### Success Criteria
- [ ] All errors completely resolved
- [ ] Application builds successfully
- [ ] Core functionality verified working
- [ ] No new issues introduced
- [ ] Documentation updated with fix details

### Failure Prevention
- Always use systematic verification
- Never skip validation steps
- Document all changes made
- Test with realistic scenarios
- Verify no regression in other areas

## Metrics and Monitoring

Track debugging effectiveness:
- Time to resolution
- Number of files affected
- Root cause categories
- Prevention opportunities
- Knowledge transfer value

---

**This skill transforms debugging from reactive problem-solving into systematic, zero-tolerance error resolution with complete documentation and prevention focus.**

---

## MANDATORY USER VERIFICATION REQUIREMENT

### Policy: No Fix Claims Without User Confirmation

**CRITICAL**: Before claiming ANY issue, bug, or problem is "fixed", "resolved", "working", or "complete", the following verification protocol is MANDATORY:

#### Step 1: Technical Verification
- Run all relevant tests (build, type-check, unit tests)
- Verify no console errors
- Take screenshots/evidence of the fix

#### Step 2: User Verification Request
**REQUIRED**: Use the `AskUserQuestion` tool to explicitly ask the user to verify the fix:

```
"I've implemented [description of fix]. Before I mark this as complete, please verify:
1. [Specific thing to check #1]
2. [Specific thing to check #2]
3. Does this fix the issue you were experiencing?

Please confirm the fix works as expected, or let me know what's still not working."
```

#### Step 3: Wait for User Confirmation
- **DO NOT** proceed with claims of success until user responds
- **DO NOT** mark tasks as "completed" without user confirmation
- **DO NOT** use phrases like "fixed", "resolved", "working" without user verification

#### Step 4: Handle User Feedback
- If user confirms: Document the fix and mark as complete
- If user reports issues: Continue debugging, repeat verification cycle

### Prohibited Actions (Without User Verification)
- Claiming a bug is "fixed"
- Stating functionality is "working"
- Marking issues as "resolved"
- Declaring features as "complete"
- Any success claims about fixes

### Required Evidence Before User Verification Request
1. Technical tests passing
2. Visual confirmation via Playwright/screenshots
3. Specific test scenarios executed
4. Clear description of what was changed

**Remember: The user is the final authority on whether something is fixed. No exceptions.**
