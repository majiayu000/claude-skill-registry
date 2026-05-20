---
name: debug
description: Debug a specific issue by reading logs and investigating code
argument-hint: "[issue description]"
allowed-tools:
  - Bash
  - Read
  - Grep
  - Glob
  - mcp__automation__screenshot
model: sonnet
---

# Debug GridRacer Issue

Investigate and diagnose a specific problem.

## Arguments
`$ARGUMENTS` - Description of the issue to debug

## Steps

### 1. Reproduce and Capture
```bash
# Launch with console logging
xcrun simctl launch --console booted trouarat.GridRacer 2>&1 | head -100
```

Or take a screenshot to see current state:
- Use `mcp__automation__screenshot` to capture the game

### 2. Gather Context
- Search codebase for related code
- Read relevant Swift files
- Check recent git changes: `git log --oneline -10`

### 3. Form Hypothesis
Based on:
- Error messages in console
- Visual state in screenshot
- Code analysis

### 4. Verify
- Add print statements or breakpoints conceptually
- Trace execution path
- Check edge cases

### 5. Report
Provide:
- **Root cause**: Why the bug occurs
- **Location**: File and line number
- **Fix**: Specific code change needed
- **Verification**: How to confirm the fix works

### 6. Create Issue (Optional)

After completing investigation, offer:

```
🐛 Investigation Complete

Root Cause: [Identified cause]
Location: [File:line]
Suggested Fix: [Proposed solution]

Create GitHub issue to track this bug? [Y/n]
```

If yes:
```bash
gh issue create \
  --title "BUG: [Short summary from investigation]" \
  --template bug_report.md \
  --label "bug" \
  --body "$(cat <<'EOF'
## Bug Analysis

**Root Cause**: [Identified cause from investigation]

**Location**: [File path and line number]

**Steps to Reproduce**:
1. [Step 1 from debugging]
2. [Step 2]

**Expected**: [What should happen]
**Actual**: [What happens]

**Suggested Fix**:
[Proposed solution with code snippet if applicable]

**Related Files**:
- `[file path]:[line]`

**Discovered via**: /debug skill

---
[Additional context from investigation]
EOF
)"
```

Output: "✓ Issue #N created. Start work with: /work-on N"

**Component Label Auto-Detection**:
Based on investigation findings, add relevant labels:
- Collision issues → add `collision-detection`
- SceneKit issues → add `scenekit`
- Game logic issues → add `game-logic`
- UI issues → add `ui`
