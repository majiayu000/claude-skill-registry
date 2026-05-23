---
name: cube-iml
user_invocable: true
description: |
  Check and repair PyCharm/IntelliJ module configuration (.iml file).
  Triggered by "/cube-iml" or when user reports PyCharm doesn't recognize src/tests folders.
---

# Cube IML Skill

Check and repair the PyCharm/IntelliJ module configuration file.

## Trigger

Use when:
- User runs `/cube-iml` or asks about PyCharm/IntelliJ configuration
- User reports "module not configured" or import resolution issues
- User says PyCharm doesn't recognize src or tests folders

## Quick Check

Run this Python snippet to check the .iml file:

```bash
python -c "
from pathlib import Path
from xml.etree import ElementTree as ET

iml = Path('.idea/cube.iml')
if not iml.exists():
    print('MISSING: .idea/cube.iml does not exist')
    exit(1)

try:
    tree = ET.parse(iml)
    root = tree.getroot()
except ET.ParseError as e:
    print(f'CORRUPTED: XML parse error: {e}')
    exit(1)

# Check required elements
sources = tree.findall('.//sourceFolder')
has_src = any('src' in s.get('url', '') and s.get('isTestSource') == 'false' for s in sources)
has_tests = any('tests' in s.get('url', '') and s.get('isTestSource') == 'true' for s in sources)
has_sdk = tree.find('.//orderEntry[@type=\"jdk\"]') is not None

issues = []
if not has_src:
    issues.append('Missing src as source folder')
if not has_tests:
    issues.append('Missing tests as test source folder')
if not has_sdk:
    issues.append('Missing Python SDK configuration')

if issues:
    print('INCOMPLETE:')
    for i in issues:
        print(f'  - {i}')
    exit(1)

print('OK: cube.iml is valid and complete')
"
```

## Actions Based on Result

### If MISSING or CORRUPTED or INCOMPLETE

Ask the user:
```
The .idea/cube.iml file is [missing/corrupted/incomplete].

Would you like me to reconstruct it?
- Yes, reconstruct it
- No, I'll fix it manually
```

If user says yes, run:
```bash
python scripts/reconstruct_iml.py
```

### If OK

Report: "PyCharm configuration looks good. If you're still having issues, try:
1. File → Invalidate Caches and Restart
2. Right-click src folder → Mark Directory as → Sources Root"

## Manual Fix

If the script doesn't exist or fails, create the file manually:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<module type="PYTHON_MODULE" version="4">
  <component name="NewModuleRootManager">
    <content url="file://$MODULE_DIR$">
      <sourceFolder url="file://$MODULE_DIR$/src" isTestSource="false" />
      <sourceFolder url="file://$MODULE_DIR$/tests" isTestSource="true" />
    </content>
    <orderEntry type="jdk" jdkName="Python 3.14 (cubesolve)" jdkType="Python SDK" />
    <orderEntry type="sourceFolder" forTests="false" />
  </component>
</module>
```

Adjust the `jdkName` to match the user's Python interpreter name.
