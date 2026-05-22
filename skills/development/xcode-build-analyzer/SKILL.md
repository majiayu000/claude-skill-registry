---
name: Xcode Build Analyzer
description: Analyze Xcode build failures, categorize errors by type, identify cascade issues, and provide systematic fix plan for Leavn iOS app
allowed-tools: Bash, Read, Grep
---

# Xcode Build Analyzer

## Instructions

Systematically analyze and fix Xcode build errors:

1. **Get error summary**:
   ```bash
   xcodebuild -project Leavn.xcodeproj -scheme Leavn -destination 'platform=iOS Simulator,name=LeavnTest' build 2>&1 | grep "error:" | cut -d: -f4- | sort -u
   ```

2. **Categorize by type**:
   - **Import issues**: Missing SwiftData, UIKit, etc.
   - **Type mismatches**: Wrong return types, protocol conformances
   - **Actor isolation**: @MainActor property access from nonisolated
   - **Property wrappers**: @ObservedObject on @Observable types
   - **Missing types**: Deleted files still referenced
   - **Binding issues**: $var on non-@Bindable types

3. **Identify cascade errors**:
   - One missing type → 50 errors
   - One @Observable migration → 10 binding errors
   - Find the root cause, fix once

4. **Priority fix order**:
   - Missing imports (unlock many files)
   - Missing types (cascade fixes)
   - Property wrappers (mechanical fixes)
   - Actor isolation (add nonisolated)
   - Complex type inference (last)

5. **Quick wins**:
   - Count errors between fixes
   - Commit when 50%+ reduction achieved
   - Disable broken code temporarily if needed

Use this skill when: Build fails with many errors, refactoring breaks build, need systematic error fixing
