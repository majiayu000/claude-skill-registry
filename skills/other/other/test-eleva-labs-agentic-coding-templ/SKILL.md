---
name: test
description: >-
  Execute mobile testing workflow for React Native/Expo apps.
  Use when running unit tests, component tests, integration tests,
  or performing manual testing on iOS and Android.
  Invoked by: "run tests", "test", "testing", "unit tests", "mobile testing".
---

# Mobile Testing Process SOP

**Version**: 1.0.0
**Last Updated**: 2026-01-11
**Status**: Active

---

## Overview

### Purpose
Systematic testing of React Native mobile app features with comprehensive validation across iOS and Android platforms. Covers unit tests, component tests, integration tests, and manual platform testing.

### When to Use
**ALWAYS**: Feature validation, bug verification, pre-merge testing, platform-specific testing, regression testing
**SKIP**: Documentation-only changes, config-only changes (unless config affects runtime)

---

## Quick Start

1. **Run all tests**: `pnpm test`
2. **Run with coverage**: `pnpm test --coverage`
3. **Test specific file**: `pnpm test path/to/test.ts`
4. **Manual iOS test**: `pnpm run ios:dev`
5. **Manual Android test**: `pnpm run android:dev`

See [Process Workflow](#process-workflow) for detailed testing phases.

---

## Process Workflow

### Flow Diagram
```
[Discovery] --> [Planning] --> [Environment Setup] --> [Execution] --> [Issue Resolution] --> [Documentation]
   30-60 min      1-2 hrs         15-30 min           2-6 hrs           Variable            30-60 min
```

### Phase Summary
| Phase | Duration | Deliverable |
|-------|----------|-------------|
| 1. Discovery | 30-60 min | Test plan, feature inventory |
| 2. Planning | 1-2 hours | Test plan with test cases |
| 3. Environment Setup | 15-30 min | Running app, test data |
| 4. Execution | 2-6 hours | Test results with findings |
| 5. Issue Resolution | Variable | Code fixes, regression tests |
| 6. Documentation | 30-60 min | Updated docs, committed changes |

**Total Duration**: 2-8 hours per feature area

---

## Key Principles

1. **Systematic Approach** - Follow 6 phases, document everything
2. **Test in Isolation** - Independent tests, clean up test data
3. **Document First** - Create test plan before executing
4. **Platform Coverage** - Always test on both iOS and Android
5. **Quality Over Speed** - Test error cases, validate all scenarios
6. **Mobile-Specific** - Consider safe areas, navigation, gestures, performance

---

## Test Types

### Unit Tests
- **What**: Individual functions, utilities, helpers
- **Location**: `src/**/*.test.ts`
- **Tools**: Jest
- **Command**: `pnpm test`

### Component Tests
- **What**: React components in isolation
- **Location**: `src/**/*.test.tsx`
- **Tools**: Jest + React Native Testing Library
- **Command**: `pnpm test`

### Integration Tests
- **What**: Redux state, navigation flows, API integration
- **Location**: `__tests__/`, `src/**/*.test.ts`
- **Tools**: Jest + Redux mock store
- **Command**: `pnpm test`

### Manual Tests
- **What**: Platform-specific behavior, UI/UX validation
- **Platforms**: iOS simulators, Android emulators, physical devices
- **Command**: `pnpm run ios:dev` or `pnpm run android:dev`

---

## Phase 1: Discovery

**Objective**: Understand current feature state and testing requirements

### Review Feature Implementation
**Locations**:
- Components: `src/components-next/`
- Screens: `src/screens/`
- Redux: `src/store/`
- Navigation: `src/navigation/`
- Types: `src/types/`

### Review Existing Tests
```bash
# Find test files
find . -name "*.test.ts*" -type f

# Review test coverage
pnpm test --coverage
```

### Identify Test Scenarios
- **Happy Path**: Normal user flows
- **Error Cases**: Network errors, validation errors
- **Edge Cases**: Empty states, boundary values
- **Platform-Specific**: iOS-only, Android-only behaviors

---

## Phase 2: Planning

**Objective**: Create detailed test plan with test cases

### Create Test Plan
**Location**: `docs/ignore/tests/mobile/<FEATURE>_TEST_PLAN.md`
**Template**: [TEST_PLAN_TEMPLATE.md](TEST_PLAN_TEMPLATE.md)

### Test Case Format
```markdown
### TC-001: Component Renders Correctly
**Component**: AIChatInterface
**Platform**: Both
**Priority**: High
**Steps**:
1. Render component with props
2. Verify component renders
**Expected**: Component displays correctly
```

---

## Phase 3: Environment Setup

**Objective**: Prepare clean testing environment

### Commands
```bash
# Install dependencies
pnpm install

# Start Metro bundler
pnpm start

# Start iOS simulator
pnpm run ios:dev

# Start Android emulator
pnpm run android:dev

# Verify environment
npx expo --version
node -v
xcrun simctl list devices
adb devices
```

---

## Phase 4: Execution

**Objective**: Execute tests systematically and track results

### Create Results Document
**Location**: `docs/ignore/tests/mobile/<FEATURE>_TEST_RESULTS.md`
**Template**: [TEST_RESULTS_TEMPLATE.md](TEST_RESULTS_TEMPLATE.md)

### Status Indicators
- Pending
- Pass
- Fail
- In Progress
- Partial

### Execute Tests
```bash
# Run all tests
pnpm test

# Run specific test file
pnpm test path/to/test.ts

# Run tests in watch mode
pnpm test --watch

# Run tests with coverage
pnpm test --coverage
```

See [TEST_GUIDE.md](TEST_GUIDE.md) for detailed testing methodology.

---

## Phase 5: Issue Resolution

**Objective**: Fix bugs systematically

### Debug and Fix
1. **Locate issue**: Search for component, screen, Redux slice
2. **Understand flow**: Component --> Screen --> Redux --> API
3. **Apply fix**: Follow React Native patterns
4. **Update tests**: Add/modify tests for the fix

### Re-test
```bash
# Re-run failed test
pnpm test path/to/test.ts

# Re-run all tests
pnpm test

# Re-test on platforms
pnpm run ios:dev
pnpm run android:dev
```

---

## Phase 6: Documentation

**Objective**: Record results and maintain documentation

### Update Documentation
- Test results document
- Test plan (mark completed)
- Feature documentation (if applicable)

### Commit Changes
```bash
# Commit code fixes
git add src/
git commit -m "fix: resolve [issue description]"

# Commit test documentation
git add docs/ignore/tests/mobile/
git commit -m "docs: add test results for [FEATURE]"
```

---

## Quick Reference

### Testing Commands
```bash
# Run all tests
pnpm test

# Run with coverage
pnpm test --coverage

# Run specific file
pnpm test path/to/test.ts

# Watch mode
pnpm test --watch

# Type checking
npx tsc --noEmit

# Linting
pnpm run lint
```

### Platform Testing
```bash
# iOS
pnpm run ios:dev
xcrun simctl list devices

# Android
pnpm run android:dev
adb devices
```

### Test File Patterns
```bash
# Find test files
find . -name "*.test.ts*" -type f

# Find test utilities
find __mocks__ -type f
```

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Tests won't run | Clear cache: `pnpm test --clearCache`, reinstall deps |
| iOS simulator issues | Check Xcode, verify simulator available |
| Android emulator issues | Check Android Studio, verify ADB connection |
| Tests fail intermittently | Reset state between tests, use unique test data |
| TypeScript errors in tests | Check types, run `npx tsc --noEmit` |
| Platform-specific failures | Test on both platforms, check safe areas |

---

## Related Skills

| Skill | Purpose | When to Use |
|-------|---------|-------------|
| `/dev-feature` | Feature workflow | During Phase 6 validation |
| `/review-code` | Code review | Before running tests |
| `/help` | Fix issues | When tests fail |

> **Note**: Skill paths (`/skill-name`) work after deployment. In the template repo, skills are in domain folders.

---

**End of SOP**
