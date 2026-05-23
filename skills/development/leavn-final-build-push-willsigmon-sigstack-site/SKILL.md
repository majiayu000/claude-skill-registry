---
name: Leavn Final Build Push
description: Fix last few build errors aggressively, get clean build, commit everything, and prepare for ship in Leavn iOS app
allowed-tools: Read, Edit, Bash, Grep
---

# Leavn Final Build Push

## Instructions

Aggressively fix remaining errors to get clean build:

1. **Count errors**:
   ```bash
   xcodebuild build 2>&1 | grep -c "error:"
   ```

2. **If <10 errors - FIX DIRECTLY**:
   - Read error locations
   - Apply quick fixes
   - Comment out if too complex
   - Priority: BUILD SUCCEEDS

3. **Quick fix strategies**:
   - Missing property: Add stub or comment out usage
   - Binding error: Add @Bindable or remove binding
   - Type mismatch: Cast or change type
   - Actor isolation: Add nonisolated(unsafe)
   - Missing import: Add import

4. **Nuclear options** (if stuck):
   - Comment out broken features
   - Disable problematic files
   - Use `#if false` to guard code
   - Fix properly in next session

5. **Success criteria**:
   - `** BUILD SUCCEEDED **`
   - Commit immediately
   - Document TODOs for disabled code

Use this skill when: Almost at clean build, <10 errors left, need to ship, aggressive fixes needed
