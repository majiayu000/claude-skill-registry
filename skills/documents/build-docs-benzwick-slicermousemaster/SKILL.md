---
name: build-docs
description: Generate reference docs, build Sphinx documentation, and review all screenshots
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - Glob
  - Grep
context: manual
---

# Build Documentation Skill

Generate all reference documentation from code, build Sphinx docs, capture tutorial screenshots, and review everything for issues.

## When to Use

- After making changes to actions, mouse profiles, or UI
- Before committing documentation changes
- When preparing a release
- When asked to "build the docs" or "generate documentation"

## Prerequisites

- Python environment with project dependencies (`uv sync`)
- For full generation: 3D Slicer installed with `SLICER_PATH` in `.env`
- For partial generation: Works without Slicer (mouse profiles only)

## Quick Start

### Minimal (No Slicer Required)

```bash
# Generate mouse profiles reference
python MouseMaster/Testing/Python/test_generate_mouse_profiles.py

# Build docs (will have placeholder for actions)
pip install -r docs/requirements.txt
sphinx-build -b html docs docs/_build/html
```

### Full Generation (Requires Slicer)

```bash
# Set Slicer path
export SLICER_PATH=/path/to/Slicer

# Generate all reference docs
python MouseMaster/Testing/Python/test_generate_mouse_profiles.py

$SLICER_PATH --no-splash \
  --python-script MouseMaster/Testing/Python/test_generate_actions_reference.py \
  --additional-module-paths $(pwd)/MouseMaster

# Generate tutorial screenshots
$SLICER_PATH --no-splash \
  --python-script MouseMaster/Testing/Python/test_tutorial_workflow.py \
  --additional-module-paths $(pwd)/MouseMaster

# Build docs
sphinx-build -b html docs docs/_build/html
```

## Step-by-Step Workflow

### Step 1: Generate Mouse Profiles Reference

This can run standalone without Slicer:

```bash
python MouseMaster/Testing/Python/test_generate_mouse_profiles.py
```

**Output**: `docs/reference/_generated/mouse-profiles.rst`

**Verify**:
```bash
cat docs/reference/_generated/mouse-profiles.rst | head -50
```

Should show all mouse profiles with button tables.

### Step 2: Generate Actions Reference (Requires Slicer)

```bash
$SLICER_PATH --no-splash \
  --python-script MouseMaster/Testing/Python/test_generate_actions_reference.py \
  --additional-module-paths $(pwd)/MouseMaster
```

**Output**: `docs/reference/_generated/actions.rst`

**Verify**:
```bash
cat docs/reference/_generated/actions.rst | head -50
```

Should show action categories with tables.

### Step 3: Generate Tutorial Screenshots (Requires Slicer)

```bash
mkdir -p docs/user-guide/_generated

$SLICER_PATH --no-splash \
  --python-script MouseMaster/Testing/Python/test_tutorial_workflow.py \
  --additional-module-paths $(pwd)/MouseMaster
```

**Output**:
- `docs/user-guide/_generated/*.png` - Tutorial screenshots
- `docs/user-guide/_generated/manifest.json` - Screenshot metadata
- `docs/user-guide/tutorial.rst` - Generated tutorial RST

**Verify**:
```bash
ls -la docs/user-guide/_generated/
cat docs/user-guide/_generated/manifest.json
```

### Step 4: Build Sphinx Documentation

```bash
pip install -r docs/requirements.txt
sphinx-build -b html docs docs/_build/html 2>&1 | tee sphinx-build.log
```

**Check for errors**:
```bash
grep -i "error\|warning" sphinx-build.log
```

**Preview** (if browser available):
```bash
python -m http.server 8000 -d docs/_build/html
# Open http://localhost:8000
```

### Step 5: Review Screenshots

Review each screenshot for issues:

```bash
# List all screenshots
find docs -name "*.png" -o -name "manifest.json"

# Read manifest for descriptions
cat docs/user-guide/_generated/manifest.json
```

For each screenshot, check:

#### Layout Issues
- [ ] Widgets properly aligned
- [ ] Spacing consistent
- [ ] No overlapping elements
- [ ] Text not truncated

#### Content Issues
- [ ] Correct module/panel shown
- [ ] Dropdowns expanded where expected
- [ ] Button states correct (enabled/disabled)
- [ ] Data displayed correctly

#### Documentation Suitability
- [ ] Screenshot clearly shows the feature
- [ ] No personal data visible
- [ ] Resolution adequate
- [ ] Screenshot matches documentation text

### Step 6: Fix Issues

If screenshots have problems:

1. **UI issues** - Edit `MouseMaster/MouseMaster.py` widget code
2. **Capture issues** - Edit `test_tutorial_workflow.py` capture sequence
3. **Missing screenshots** - Add new capture calls

After fixes, re-run from Step 3.

## Generated Files Summary

| File | Source | Requires Slicer |
|------|--------|-----------------|
| `docs/reference/_generated/mouse-profiles.rst` | JSON files | No |
| `docs/reference/_generated/actions.rst` | ActionRegistry | Yes |
| `docs/user-guide/_generated/*.png` | Tutorial test | Yes |
| `docs/user-guide/_generated/manifest.json` | Tutorial test | Yes |
| `docs/user-guide/tutorial.rst` | Tutorial test | Yes |

## Troubleshooting

### Slicer not found

```bash
# Check path
which Slicer || echo "Not in PATH"

# Set explicitly
export SLICER_PATH=/opt/Slicer/Slicer
```

### Module not loading

```bash
# Verify module path
ls MouseMaster/MouseMaster.py

# Check for syntax errors
python -m py_compile MouseMaster/MouseMaster.py
```

### Screenshots blank or wrong

Check if virtual display is needed (CI/headless):

```bash
# Start Xvfb
Xvfb :99 -screen 0 1920x1080x24 &
export DISPLAY=:99

# Then run Slicer
$SLICER_PATH --no-splash ...
```

### Sphinx build errors

```bash
# Check for missing files
grep "include" docs/reference/*.rst
ls docs/reference/_generated/

# Create placeholder if needed
echo ".. note:: Auto-generated content not available" > docs/reference/_generated/actions.rst
```

## CI Integration

The CI workflow runs these steps automatically:

```yaml
# From .github/workflows/tests.yml
- name: Generate reference documentation
  run: |
    python MouseMaster/Testing/Python/test_generate_mouse_profiles.py
    $SLICER_HOME/Slicer --python-script MouseMaster/Testing/Python/test_generate_actions_reference.py ...
```

## Related Skills

- `/generate-screenshots` - Capture Extension Index screenshots
- `/review-ui-screenshots` - Detailed UI review
- `/run-tests` - Run all tests including doc generators

## Verification Checklist

After building docs:

- [ ] `docs/reference/_generated/mouse-profiles.rst` exists and has content
- [ ] `docs/reference/_generated/actions.rst` exists (or placeholder)
- [ ] `docs/user-guide/_generated/` has PNG files
- [ ] `sphinx-build` completed without errors
- [ ] Screenshots show correct UI states
- [ ] Generated tutorial matches expected workflow
- [ ] All internal links work
