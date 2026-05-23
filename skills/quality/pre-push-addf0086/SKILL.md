---
name: pre-push
description: Quick validation checklist before pushing changes. Use when about to push, before git push, or to validate changes.
---

# Pre-Push Validation Checklist

Quick validation before pushing changes to the repository.

## Instructions

Run through this checklist:

### 1. Manifest Validation
- Read `custom_components/sl_departures/manifest.json`
- Verify required fields: domain, name, version, codeowners, config_flow, iot_class
- Check version is appropriate for the changes

### 2. Translation Completeness
- Compare `strings.json` keys with `translations/en.json`
- Check `translations/sv.json` has matching keys

### 3. Import Validation
Run:
```bash
python -c "import sys; sys.path.insert(0, '.'); from custom_components.sl_departures import const"
```

### 4. Git Status Review
- Run `git status` and `git diff --staged`
- Ensure no sensitive files (.env, credentials) are staged
- Summarize what's being pushed

### 5. Quick Code Scan
Check for:
- `print()` statements (should use `_LOGGER`)
- Hardcoded credentials or API keys
- TODO/FIXME comments that need addressing

## Output Format

Report each check as **PASS** or **FAIL** with details:

```
1. Manifest:     PASS/FAIL - details
2. Translations: PASS/FAIL - details
3. Imports:      PASS/FAIL - details
4. Git Status:   X files staged
5. Code Scan:    PASS/FAIL - details

Ready to push: YES/NO
```
