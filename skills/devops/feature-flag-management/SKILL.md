---
name: feature-flag-management
description: Automate the complete lifecycle of feature flags in Saberloop, following Epic 10 hygiene standards
version: 1.0.0
author: Saberloop Project
usage: |
  Use this skill when working with feature flags:
  - Creating new feature flags for gradual rollout
  - Updating flag phases (DISABLED → SETTINGS_ONLY → ENABLED)
  - Removing deprecated flags following hygiene standards
  - Adding flag documentation
  
  Examples:
  "Create a new FEATURE_NAME flag using the feature-flag-management skill"
  "Remove the OLD_FEATURE flag using the feature-flag-management skill"
  "Update FEATURE_NAME to SETTINGS_ONLY phase using the feature-flag-management skill"

# Feature Flag Management Skill

## Overview

This skill automates the complete lifecycle of feature flags in Saberloop, following the established patterns from Epic 10 hygiene processes.

## Flag Lifecycle

```
DISABLED → SETTINGS_ONLY → ENABLED → REMOVED
```

### Phase Definitions

| Phase | Description | User Visibility | Typical Duration |
|--------|-------------|------------------|------------------|
| DISABLED | Code deployed but inactive | None | Testing phase |
| SETTINGS_ONLY | Available in Settings page only | Settings page | User testing |
| ENABLED | Available everywhere | Full app | Production |

## When to Create a Flag

Create a flag when ALL of these are true:
- [ ] New feature needs gradual rollout
- [ ] Feature is risky and might need quick rollback
- [ ] Feature will be A/B tested
- [ ] Rollout plan exists with success metrics

## When to Remove a Flag

Remove a flag when ALL of these are true:
- [ ] Stable in production for 2+ weeks
- [ ] Always enabled (no plan to disable)
- [ ] Not user-configurable preference
- [ ] Not tied to future feature (premium tier, etc.)

## Implementation Templates

### Step 1: Create the Flag

**File:** `src/core/features.js`

```javascript
export const FEATURE_FLAGS = {
  // Existing flags...
  
  NEW_FEATURE: {
    phase: 'DISABLED',  // Start with DISABLED for new features
    description: 'Brief description of what the feature does'
  }
};
```

**Description Guidelines:**
- Max 100 characters
- Clear what/why, not how
- Include user benefit if applicable

### Step 2: Update Flag Usage

```javascript
import { isFeatureEnabled } from '@/core/features.js';

// In components/views
if (isFeatureEnabled('NEW_FEATURE', 'home')) {
  // Show feature on home page
}

// In services
if (isFeatureEnabled('NEW_FEATURE')) {
  // Enable backend behavior
}
```

**Context Parameters:**
- `'default'` - General usage (most common)
- `'settings'` - Settings page only
- `'home'` - Home page specific
- `'welcome'` - Onboarding flow

### Step 3: Add Tests

**Test File:** `src/core/features.test.js`

```javascript
describe('NEW_FEATURE Flag', () => {
  it('should return false when DISABLED', () => {
    expect(isFeatureEnabled('NEW_FEATURE')).toBe(false);
  });
  
  it('should return true when ENABLED', () => {
    // Mock flag as ENABLED
    vi.stubGlobal('localStorage', {
      getItem: () => 'ENABLED'
    });
    
    expect(isFeatureEnabled('NEW_FEATURE')).toBe(true);
  });
  
  it('should respect SETTINGS_ONLY phase', () => {
    // Mock flag as SETTINGS_ONLY
    vi.stubGlobal('localStorage', {
      getItem: () => 'SETTINGS_ONLY'
    });
    
    expect(isFeatureEnabled('NEW_FEATURE', 'settings')).toBe(true);
    expect(isFeatureEnabled('NEW_FEATURE', 'home')).toBe(false);
  });
});
```

### Step 4: Create Documentation

**File:** `docs/learning/epic10_hygiene/FLAG_NEW_FEATURE.md`

```markdown
# NEW_FEATURE Feature Flag

**Status:** DISABLED
**Created:** YYYY-MM-DD
**Phase:** DISABLED → SETTINGS_ONLY → ENABLED → REMOVED
**Remove When:** Feature is stable for 2+ weeks

## Purpose
Brief description of why this flag exists.

## Success Metrics
- [ ] Feature works as intended
- [ ] No performance impact
- [ ] User feedback positive
- [ ] Telemetry shows usage

## Removal Plan
When this flag is removed:
- [ ] Remove isFeatureEnabled() checks
- [ ] Simplify conditional logic
- [ ] Update/remove related tests
- [ ] Archive this documentation
```

### Step 5: Update Epic Documentation

**File:** `docs/learning/epic10_hygiene/EPIC10_HYGIENE_PLAN.md`

Add to "Future Flag Cleanup" table if applicable:
```markdown
| Flag | Status | Remove When | Document |
|------|--------|-------------|----------|
| NEW_FEATURE | DISABLED | 2 weeks after ENABLED | FLAG_NEW_FEATURE.md |
```

## Phase Updates

### Moving from DISABLED to SETTINGS_ONLY

1. **Update flag phase:**
```javascript
NEW_FEATURE: {
  phase: 'SETTINGS_ONLY',  // Updated
  description: '...'
}
```

2. **Add Settings UI:**
```javascript
// In SettingsView.js
if (isFeatureEnabled('NEW_FEATURE', 'settings')) {
  // Add settings toggle for user testing
}
```

3. **Update tests** for SETTINGS_ONLY behavior

4. **Update documentation** with test plan

### Moving from SETTINGS_ONLY to ENABLED

1. **Update flag phase:**
```javascript
NEW_FEATURE: {
  phase: 'ENABLED',  // Updated
  description: '...'
}
```

2. **Remove Settings-only guard** (make available everywhere)

3. **Update tests** for ENABLED behavior

4. **Update documentation** with success metrics

## Flag Removal Process (Hygiene Task)

Follow Epic 10 hygiene standards:

### Pre-Removal Checklist

- [ ] Flag has been ENABLED for 2+ weeks
- [ ] No issues reported in telemetry
- [ ] Feature is working as intended
- [ ] No plan to disable this feature
- [ ] Not a user preference setting

### Step 1: Create Hygiene Branch

```bash
# From main repo directory
git worktree add ../saberloop-hygiene hygiene/remove-new-feature-flag

cd ../saberloop-hygiene
npm install
```

### Step 2: Remove Flag Code

1. **Remove from features.js:**
```javascript
export const FEATURE_FLAGS = {
  // Remove NEW_FEATURE entry
};
```

2. **Remove isFeatureEnabled() calls:**
```javascript
// Before
if (isFeatureEnabled('NEW_FEATURE')) {
  doSomething();
}

// After
doSomething(); // Always execute
```

3. **Simplify conditional logic:**
```javascript
// Before
if (isFeatureEnabled('NEW_FEATURE')) {
  return enhancedVersion();
} else {
  return basicVersion();
}

// After
return enhancedVersion(); // Always use enhanced
```

### Step 3: Update Tests

1. **Remove flag-specific tests** from features.test.js
2. **Update integration tests** to expect new behavior
3. **Run full test suite** to ensure no regressions

### Step 4: Documentation Updates

1. **Archive flag documentation:** Move to completed folder
2. **Update Epic 10 plan** with removal date
3. **Create learning notes:** `docs/learning/epic10_hygiene/PHASE*_LEARNING_NOTES.md`

### Step 5: Quality Checks

Run complete hygiene checklist:

```bash
npm test                    # Unit tests
npm run test:e2e            # E2E tests
npm run test:mutation        # Mutation testing
npm run arch:test           # Architecture validation
npm run typecheck           # TypeScript checking
```

### Step 6: Commit and Merge

```bash
git add -A
git commit -m "refactor(hygiene): remove NEW_FEATURE feature flag

- Remove isFeatureEnabled() checks for NEW_FEATURE
- Simplify conditional logic in [files]
- Remove flag from FEATURE_FLAGS object
- Update/remove related tests
- Archive flag documentation"

git push -u origin hygiene/remove-new-feature-flag

# Create PR after review
gh pr create --title "chore: remove NEW_FEATURE feature flag"
```

### Step 7: Cleanup

```bash
# From main repo
git worktree remove ../saberloop-hygiene
git branch -d hygiene/remove-new-feature-flag
```

## Common Patterns

### Gradual Rollout Pattern

```javascript
// Phase 1: Settings only (user testing)
if (isFeatureEnabled('NEW_FEATURE', 'settings')) {
  showSettingsToggle();
}

// Phase 2: Limited exposure (telemetry gathering)
if (isFeatureEnabled('NEW_FEATURE', 'home')) {
  showFeatureOnHomePage();
}

// Phase 3: Full release
if (isFeatureEnabled('NEW_FEATURE')) {
  enableFeature();
}
```

### Safe Removal Pattern

```javascript
// Use feature flag as guard during development
const enhancedFlow = isFeatureEnabled('NEW_FEATURE') 
  ? newEnhancedImplementation() 
  : existingImplementation();

// After flag removal, the enhanced implementation becomes default
const enhancedFlow = newEnhancedImplementation();
```

## Testing Guidelines

### Unit Testing Requirements

Every flag needs these tests:

```javascript
describe('FEATURE_NAME Flag', () => {
  it('should return false when DISABLED', () => {
    // Test default behavior
  });
  
  it('should return true when ENABLED', () => {
    // Test enabled behavior
  });
  
  it('should respect SETTINGS_ONLY phase', () => {
    // Test settings-only behavior
  });
  
  it('should handle test overrides', () => {
    // Test localStorage override capability
  });
});
```

### Integration Testing

- Test flag behavior in actual components
- Verify Settings UI shows/hides correctly
- Confirm feature works in each phase
- Check telemetry tracks flag usage

### E2E Testing

Add Playwright tests for critical flags:

```javascript
test('feature flag settings toggle', async ({ page }) => {
  await page.goto('/settings');
  
  // Test settings-only flag visibility
  const toggle = page.locator('[data-testid="new-feature-toggle"]');
  await expect(toggle).toBeVisible();
  
  // Test toggle functionality
  await toggle.click();
  // Verify behavior changes
});
```

## Troubleshooting

### Flag Not Working

1. **Check import path:** `@/core/features.js`
2. **Verify flag name** matches FEATURE_FLAGS object
3. **Check context parameter** if using SETTINGS_ONLY
4. **Test localStorage override** for debugging

### Test Override Not Working

```javascript
// For debugging, force a flag state
localStorage.setItem('__test_feature_NEW_FEATURE', 'ENABLED');
// Then test isFeatureEnabled('NEW_FEATURE')
```

### Removal Breaks Something

1. **Check for missed isFeatureEnabled() calls**
2. **Verify conditional logic was properly simplified**
3. **Run tests with --run flag** (not watch mode)
4. **Check git diff** for unintended changes

## Quality Metrics

Track these metrics for flag management:

| Metric | Target | How to Measure |
|--------|--------|-----------------|
| Flag creation time | < 30 min | From skill start to tests passing |
| Flag removal time | < 2 hours | From hygiene branch to merge |
| Test coverage | 100% | All flag paths tested |
| Documentation completeness | 100% | All fields filled in |
| Zero regressions | Required | All tests pass after removal |

## Related Files

- `src/core/features.js` - Main flag definitions
- `src/core/features.test.js` - Flag tests
- `docs/learning/epic10_hygiene/EPIC10_HYGIENE_PLAN.md` - Epic tracking
- Individual flag documentation files
- Test files for components using flags

## Integration with Other Skills

This skill integrates with:
- **epic-hygiene-process** - For removal procedures
- **testing-suite-management** - For test creation and validation
- **architecture-compliance** - For validating flag usage patterns

---

**Version:** 1.0.0  
**Last Updated:** 2026-01-15  
**Compatible with:** Saberloop v2.0.0+