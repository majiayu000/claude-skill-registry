---
name: ios-feature-audit
description: Audit a specific iOS feature for bugs, dead code, and improvements
model: sonnet
---

# iOS Feature Audit

Comprehensive audit of a specific feature (Bible, Search, Community, etc.):

## Inputs
- Feature name (e.g., "Bible", "Search", "Community")

## Audit Checklist

1. **Code Health:**
   - Find feature directory in `LeavnApp/Sources/Shared/Features/[Feature]/`
   - Check for:
     - Dead code (`#if false`, deprecated markers)
     - TODOs and FIXMEs
     - TCA remnants (old Reducer/Store patterns)
     - Unused imports

2. **ViewModel Analysis:**
   - Check if using `@Observable` (modern) or `ObservableObject` (old)
   - Look for memory leaks (retain cycles)
   - Verify async/await usage (not Combine)

3. **Test Coverage:**
   - Find tests in `Tests/` directories
   - Count test functions
   - Identify missing test scenarios

4. **UI/UX Review:**
   - Check for SwiftLint violations
   - Look for accessibility issues
   - Verify responsive design

5. **Dependencies:**
   - Check service usage via `DIContainer.shared`
   - Verify proper error handling
   - Check for hardcoded values

**Return:**
- Bug count and severity
- Dead code to delete
- Test coverage gaps
- Recommended fixes prioritized by impact
