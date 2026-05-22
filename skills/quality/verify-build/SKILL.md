---
name: verify-build
description: Verify the application builds successfully and check for type errors. Use when finished with changes, before committing, or when asked to check/verify work.
---

Run the build verification sequence for the Weekly Report Builder:

1. **Run the build:**
   ```bash
   cd client && npm run build
   ```
   - Must complete without errors
   - Note any warnings

2. **Check for `any` types:**
   - Search for explicit `any` usage in `client/src/`
   - Minimize use of `any` - suggest proper types where possible

3. **Run tests:**
   ```bash
   npm test
   ```
   - All tests should pass

4. **Report results:**
   - Summarize build status (pass/fail)
   - List any TypeScript errors
   - List any `any` types found
   - List test results
