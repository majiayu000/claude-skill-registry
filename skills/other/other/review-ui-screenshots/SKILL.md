---
name: review-ui-screenshots
description: Analyze UI screenshots to identify issues and suggest improvements
allowed-tools:
  - Bash
  - Read
  - Glob
  - Grep
  - Edit
context: manual
---

# Review UI Screenshots Skill

Analyze UI screenshots captured during testing to identify visual issues, UX problems, and suggest improvements.

## When to Use

- After `/download-ci-artifacts` retrieves screenshots
- After running Slicer integration tests locally
- When asked to "review the UI"
- When asked to "improve the widget"

## Screenshot Location

```bash
# From CI artifacts
ls ci-artifacts/screenshots/
cat ci-artifacts/screenshots/manifest.json

# From local test run
ls MouseMaster/Testing/Python/screenshots/
cat MouseMaster/Testing/Python/screenshots/manifest.json
```

## Manifest Format

```json
{
  "screenshots": [
    {
      "filename": "001.png",
      "description": "[MouseMaster] Initial state",
      "group": "full_workflow",
      "capture_type": "widget",
      "metadata": {"widget_class": "QWidget"}
    }
  ]
}
```

## Analysis Workflow

### 1. Read the manifest

```bash
cat ci-artifacts/screenshots/manifest.json | python -m json.tool
```

### 2. Review each screenshot

For each screenshot, Claude Code can view the image:

```bash
# View screenshot (Claude Code can read images)
# Just provide the path and Claude will analyze it
```

### 3. Check for issues

#### Layout Issues
- [ ] Widgets properly aligned
- [ ] Spacing consistent
- [ ] No overlapping elements
- [ ] Responsive to window size

#### Text Issues
- [ ] Labels readable
- [ ] No truncated text
- [ ] Proper capitalization
- [ ] Consistent terminology

#### State Issues
- [ ] Correct enabled/disabled states
- [ ] Selection highlighting visible
- [ ] Error states clear
- [ ] Loading indicators present

#### Usability Issues
- [ ] Controls discoverable
- [ ] Actions have feedback
- [ ] Navigation intuitive
- [ ] Error messages helpful

### 4. Document findings

```markdown
## Screenshot Review: [filename]

**Description**: [from manifest]
**Workflow Step**: [what user just did]

### Issues Found
- [ ] Issue 1 description
- [ ] Issue 2 description

### Recommendations
1. Recommendation 1
2. Recommendation 2

### Code Changes Needed
- `MouseMaster.py:line` - Change X to Y
```

## Common UI Fixes

### Alignment issues
```python
# Use layouts instead of absolute positioning
layout = qt.QVBoxLayout()
layout.addWidget(self.label)
layout.addWidget(self.combo)
```

### Text truncation
```python
# Set minimum width
self.comboBox.setMinimumWidth(200)

# Or use elide mode
self.label.setTextElideMode(qt.Qt.ElideRight)
```

### Disabled state unclear
```python
# Add tooltip explaining why disabled
self.button.setToolTip("Select a mouse first")
```

### Missing feedback
```python
# Add status message
slicer.util.showStatusMessage("Preset saved", 2000)
```

## Workflow Comparison

Compare sequential screenshots to verify:

1. **State transitions** - UI updates after actions
2. **Data persistence** - Selections maintained
3. **Error recovery** - UI recovers from errors

## Integration with Code

After identifying issues, edit the widget code:

```python
# MouseMaster/MouseMaster.py - MouseMasterWidget class

def setup(self):
    # Apply fixes here
    pass
```

## Report Format

```markdown
## UI Screenshot Review Report

**Screenshots Analyzed**: X
**Issues Found**: Y

### Critical Issues (fix immediately)
| Screenshot | Issue | Fix |
|------------|-------|-----|
| 003.png | Button truncated | Increase min width |

### Minor Issues (nice to have)
| Screenshot | Issue | Recommendation |
|------------|-------|----------------|
| 005.png | Inconsistent spacing | Use standard margins |

### Positive Observations
- Widget layout is clean
- Color scheme consistent

### Recommended Changes
1. File: line - Change
2. File: line - Change
```

## Verification

After making changes:

1. Run Slicer integration tests
2. Compare new screenshots to old
3. Verify issues resolved

## Related Skills

- `/download-ci-artifacts` - Get screenshots
- `/analyze-test-results` - Fix test failures
- `/generate-screenshots` - Capture new screenshots
