---
name: ios-quick-fix
description: Fast diagnosis and fix for common iOS build/runtime issues
model: sonnet
---

# iOS Quick Fix Protocol

Diagnose and fix common iOS development issues:

1. **Run diagnostic:**
```bash
make verify
```

2. **Check for common issues:**
- SPM package resolution failures → `make spm-reset`
- Derived data corruption → `make clean`
- Simulator issues → `xcrun simctl list devices`
- Missing dependencies → `make resolve`

3. **Fix based on error type:**
- **Build errors:** Clean + rebuild
- **Test failures:** Check test file locations
- **Runtime crashes:** Check simulator logs
- **Missing symbols:** Resolve dependencies

4. **Verify fix:**
```bash
make build
```

**Return what was broken and how it was fixed.**
