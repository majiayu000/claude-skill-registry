---
name: ios-build-test
description: Quick iOS build and test cycle with error detection
model: haiku
---

# iOS Build & Test Workflow

Execute a fast build and test cycle for the Leavn iOS app:

1. **Clean if needed:**
```bash
make clean
```

2. **Build for simulator:**
```bash
make sim-build 2>&1 | tee /tmp/build_output.txt
```

3. **Check for errors:**
```bash
grep -E "error:|BUILD FAILED" /tmp/build_output.txt
```

4. **If build succeeds, run tests:**
```bash
make test 2>&1 | tee /tmp/test_output.txt
```

5. **Report:**
- Build status (success/failure)
- Error count
- Test results (passed/failed/skipped)
- Time taken

**Return a concise summary with next steps if failures occur.**
