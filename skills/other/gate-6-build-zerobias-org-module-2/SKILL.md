---
name: gate-6-build
description: Gate 6 validation: Build success and dependency locking
---

### Gate 6: Build

**STOP AND CHECK:**
```bash
# Build must succeed
npm run build
echo "Exit code: $?"
# Must be 0

# Distribution files created
ls dist/
# Must show compiled files

# Lock dependencies for npm package
npm run shrinkwrap
echo "Exit code: $?"
# Must be 0

# Verify shrinkwrap file created
ls npm-shrinkwrap.json
# Must exist
```

**PROCEED ONLY IF:**
- ✅ Build succeeds (exit code 0)
- ✅ No TypeScript errors
- ✅ No linting errors
- ✅ Distribution files created
- ✅ npm shrinkwrap completed successfully
- ✅ npm-shrinkwrap.json file created

**IF FAILED:** Fix build errors before completing.
