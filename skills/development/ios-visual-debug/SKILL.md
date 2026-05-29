---
name: ios-visual-debug
description: Capture and analyze iOS simulator screenshots for visual debugging
model: haiku
---

# iOS Visual Debugging Workflow

Capture and analyze the current state of the iOS app in simulator:

1. **Check if app is running:**
```bash
ps aux | grep "com.leavn.app" | grep -v grep
```

2. **Capture screenshot:**
```bash
xcrun simctl io booted screenshot ~/Desktop/debug_$(date +%s).png
```

3. **Read and analyze the screenshot** using Claude's vision capabilities

4. **Check recent logs:**
```bash
xcrun simctl spawn booted log show --predicate 'process == "Leavn"' --last 30s --info
```

5. **Report findings:**
- What's visible on screen
- Any UI issues (layout, missing content, errors)
- Recent log errors
- Recommended next steps

**Return screenshot path and analysis.**
