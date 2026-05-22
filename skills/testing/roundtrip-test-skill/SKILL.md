---
name: Roundtrip Test Skill
description: A test skill designed to validate the complete collection submission workflow roundtrip
author: dollhousemcp
version: 1.0.1
category: testing
created: 2025-08-11
updated: 2025-08-22
tags: [testing, integration, workflow, validation]
proficiency: intermediate
---

# Roundtrip Test Skill

This skill is specifically designed to test the complete DollhouseMCP collection workflow:
1. Download from collection repository
2. Modify locally
3. Submit to GitHub portfolio  
4. Re-submit to collection

## Purpose

You are a test skill that helps validate the entire collection submission workflow. Your role is to:
- Be downloaded from the collection
- Be modified by users
- Be uploaded to their GitHub portfolio
- Be re-submitted to the collection

## Test Scenarios

### Scenario 1: Basic Roundtrip
1. User downloads this skill from collection
2. User modifies the version number or description
3. User submits to their portfolio
4. User optionally submits back to collection

### Scenario 2: Enhanced Roundtrip
1. User downloads this skill
2. User adds new capabilities or parameters
3. User changes the name slightly (e.g., "Enhanced Roundtrip Test")
4. User submits to portfolio with auto-submit enabled
5. New issue created in collection showing the enhancement

## Validation Checklist

When testing with this skill, verify:
- [ ] Download from collection works
- [ ] Local modifications are preserved
- [ ] Portfolio upload succeeds
- [ ] GitHub portfolio shows correct content
- [ ] Collection submission creates proper issue
- [ ] Issue contains correct metadata
- [ ] Labels are applied correctly
- [ ] Author attribution is correct

## Test Parameters

These parameters can be modified during testing:

- **test_mode**: `basic` | `enhanced` | `stress`
- **iteration**: Track which test run this is
- **modified_by**: Username of tester
- **modification_date**: When the test was run
- **test_results**: Success/failure status

## Expected Behavior

### On Download
- Skill appears in local portfolio/skills directory
- Metadata is preserved
- Content is readable and valid

### On Modification
- Changes are saved locally
- Version number can be updated
- New parameters can be added

### On Portfolio Upload
- File uploaded to GitHub portfolio repository
- Correct path: `skills/roundtrip-test-skill.md`
- Commit message mentions the skill name

### On Collection Submission
- Issue created with title: `[skills] Add Roundtrip Test Skill by @{username}`
- Labels: `contribution`, `pending-review`, `skills`
- Issue body contains portfolio URL
- Metadata shown in formatted code block

## Test Instructions

```bash
# Step 1: Download this skill (simulate with copy)
cp library/skills/roundtrip-test-skill.md ~/.dollhouse/portfolio/skills/

# Step 2: Modify locally (add a timestamp)
echo "Modified: [current date]" >> ~/.dollhouse/portfolio/skills/roundtrip-test-skill.md

# Step 3: In Claude Desktop, submit to portfolio
submit_content "Roundtrip Test Skill"

# Step 4: Check portfolio
# Visit: https://github.com/{username}/dollhouse-portfolio/blob/main/skills/roundtrip-test-skill.md

# Step 5: If auto-submit enabled, check collection
# Visit: https://github.com/DollhouseMCP/collection/issues
```

## Success Metrics

The roundtrip is successful when:
1. ✅ Skill moves through all stages without errors
2. ✅ Modifications are preserved throughout
3. ✅ GitHub repositories update correctly
4. ✅ All metadata remains intact
5. ✅ User can track the skill's journey

## Notes

- This is a test skill - not for production use
- Can be safely deleted after testing
- Multiple versions can exist for different test runs
- Consider using timestamps in names for uniqueness

---

---

## Test Modification Log

- **Test ID**: 1755896229
- **Modified**: 2025-08-22 16:57:09
- **User**: mick@TheMachine.local
- **Version**: 1.0.0 → 1.0.1
- **Purpose**: Automated roundtrip workflow test
