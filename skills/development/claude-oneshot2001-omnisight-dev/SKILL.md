---
name: claude-oneshot2001-omnisight-dev
description: '> Claude Skill for OMNISIGHT ACAP Development'
---

# OMNISIGHT Development Skill

> **Claude Skill for OMNISIGHT ACAP Development**
> Version: 1.0
> Last Updated: November 3, 2025

## Skill Purpose

This skill guides Claude through OMNISIGHT-specific development workflows, including ACAP packaging, camera deployment, troubleshooting, and phase management.

## Core Principles

### 1. Camera Compatibility First
**ALWAYS** check camera compatibility before recommending packages:

| Camera Model | ARTPEC | Python 3 | Required Package |
|--------------|--------|----------|------------------|
| **M4228-LVE** | ARTPEC-8 | ✅ Yes | v0.4.2 (works with any) |
| **P3285-LVE** | ARTPEC-9 | ❌ No | v0.4.2 (Native only) |
| **P3265-LVE** | ARTPEC-9 | ❌ No | v0.4.2 (Native only) |
| **Unknown** | Any | Unknown | v0.4.2 (safest choice) |

**Rule**: When in doubt, recommend Phase 4 V3 (v0.4.2) - it works on ALL cameras.

### 2. Package Verification
Before recommending deployment, ALWAYS verify:
```bash
# Check package contents
tar tzf <package.eap> | grep -E "omnisight|manifest.json|index.html"

# Must contain:
# - ./omnisight (executable wrapper)
# - ./manifest.json (ACAP manifest)
# - ./html/index.html (web interface)
# - ./package.conf (package config)
```

### 3. Log Analysis Protocol
When analyzing deployment issues:

1. **Extract error context** (10 lines before/after error)
2. **Identify error category**:
   - Missing file: `No such file or directory`
   - Missing interpreter: `python3: not found`
   - Permission: `Permission denied`
   - Manifest: `Failed to convert string to integer`
3. **Check package version** in logs (search for upload.cgi)
4. **Verify file installation** path: `/usr/local/packages/omnisight/`
5. **Propose specific fix** with verification steps

## Workflow: Deployment Troubleshooting

### Step 1: Analyze Logs
```bash
# Search for OMNISIGHT errors
grep -i "omnisight" system_log.txt | grep -E "ERR|WARN"

# Check package upload
grep -i "upload.cgi" system_log.txt | grep ".eap"

# Verify service status
grep -i "sdkomnisight.service" system_log.txt
```

### Step 2: Identify Root Cause

**Pattern Recognition**:

| Error Pattern | Root Cause | Solution |
|--------------|------------|----------|
| `python3: not found` | Missing Python 3 | Deploy v0.4.2 |
| `No such file or directory` (omnisight) | Wrong package version | Verify tar contents |
| `Failed to convert string to integer for appId` | Manifest appId is string | Fix to numeric |
| `Couldn't find page` | runMode: "never" or service crashed | Change to "respawn" |
| No "Open" button | Missing settingPage or service not running | Check manifest + service |

### Step 3: Provide Solution

**Template**:
```markdown
## 🔴 Problem Identified

[Clear description of what went wrong]

**Evidence from logs**:
```
[Relevant log excerpts]
```

## ✅ Solution

**Deploy**: [Specific package version and location]

**Steps**:
1. [Action 1]
2. [Action 2]
3. [Action 3]

**Expected Result**:
✅ [What should happen]

**Verification**:
- [ ] Check system log for errors
- [ ] Verify service running
- [ ] Confirm "Open" button appears
- [ ] Test web interface
```

## Workflow: Building Packages

### Decision Tree

```
Is this for testing/development?
├─ YES → Use build-stub.sh (fast, no camera needed)
└─ NO → Is Python available on target camera?
    ├─ UNKNOWN → Use build-phase4-v3-native-eap.sh (universal)
    ├─ NO → Use build-phase4-v3-native-eap.sh (native)
    └─ YES → Use build-phase4-v3-native-eap.sh (works on both)
```

**Default Recommendation**: `./scripts/build-phase4-v3-native-eap.sh`

### Build Verification Checklist

After building, ALWAYS verify:
```bash
# 1. Package created
ls -lh output/*.eap

# 2. Package size reasonable (>100KB, <500KB for Phase 4)
du -h output/*.eap

# 3. Contains required files
tar tzf output/*.eap | grep -E "omnisight|manifest|html/index.html"

# 4. Manifest is valid JSON
tar xzf output/*.eap manifest.json -O | python3 -m json.tool

# 5. Wrapper script has shebang
tar xzf output/*.eap omnisight -O | head -1
# Should show: #!/bin/sh
```

## Workflow: Documentation Updates

### When to Create New Documentation

**Critical Issues** (always document):
- Deployment failures that took >30 minutes to diagnose
- Camera-specific incompatibilities discovered
- Package bugs affecting multiple users
- Breaking changes in ACAP SDK

**Location Mapping**:
```
Critical deployment fix → docs/troubleshooting/deployment-fixes/
User guide → docs/guides/
Phase-specific → docs/phase{1-4}/
ACAP platform info → docs/acap/
Architecture changes → docs/development/
```

### Documentation Template

**For Deployment Fixes**:
```markdown
# [Camera Model] [Issue Description]

**Date**: [YYYY-MM-DD]
**Camera Model**: [Model]
**Package Version**: [Version]
**Issue**: [One-line summary]

## Problem Identified

[Detailed description with log evidence]

## Root Cause

[Technical explanation]

## Solution

[Step-by-step fix]

## Prevention

[How to avoid this in future]

## Related Documentation

- [Link to related docs]
```

## Workflow: Phase Management

### Phase Status Tracking

**Phase 1** (Stub Implementation - 60% complete):
- Focus: Simulation and testing without hardware
- Deliverables: Stub implementations, demo mode
- Build: `./scripts/build-stub.sh`

**Phase 2** (API Server - 100% complete):
- Focus: Flask REST API with IPC to C core
- Deliverables: Working API endpoints, React dashboard
- Build: `./scripts/deprecated/build-phase2-eap.sh` (requires Python)

**Phase 3** (Hardware Integration - In Progress):
- Focus: VDO API, Larod API, MQTT swarm
- Deliverables: Real camera integration
- Requirements: Physical camera required

**Phase 4** (Claude Flow + Universal Packaging - 100% complete):
- Focus: Distributed AI coordination + Universal builds
- Deliverables: v0.4.2 native package
- Build: `./scripts/build-phase4-v3-native-eap.sh` ✅

### Phase Transition Checklist

Before moving to next phase:
- [ ] All phase deliverables complete
- [ ] Tests passing
- [ ] Documentation updated
- [ ] Package built and tested
- [ ] Known issues documented
- [ ] Next phase prerequisites verified

## Common Patterns

### 1. Quick Diagnosis

When user reports "no Open button":
```bash
# Check these in order:
1. What package version was deployed? (check logs for upload.cgi)
2. Is service running? (check systemd status)
3. Does manifest have settingPage? (check manifest.json)
4. Are files in /usr/local/packages/omnisight/?
5. Any errors in system log?
```

### 2. Package Recommendation

When user asks "which package should I use?":
```markdown
**Recommended Package**: Phase 4 V3 (v0.4.2)

**Location**: `packages/current/OMNISIGHT_-_Precognitive_Security_042_aarch64.eap`

**Why**: Works on all cameras regardless of Python availability

**Camera Compatibility**: Universal ✅
- ARTPEC-8 with Python: ✅ Works
- ARTPEC-8 without Python: ✅ Works
- ARTPEC-9 with Python: ✅ Works
- ARTPEC-9 without Python: ✅ Works
```

### 3. Build Script Selection

When user asks "how to build?":
```markdown
**For deployment**: `./scripts/build-phase4-v3-native-eap.sh`
- Universal compatibility
- No Python dependency
- Includes web interface
- Ready for production

**For testing**: `./scripts/build-stub.sh`
- Fast compilation
- No camera needed
- Demo mode included
- Development only
```

## Error Recovery Patterns

### Pattern: Python Not Found

**Symptoms**:
```
python3: not found
exit code 127
```

**Immediate Action**:
```markdown
This camera doesn't have Python 3 installed.

✅ **Solution**: Deploy v0.4.2 (Native build)

Package: `packages/current/OMNISIGHT_-_Precognitive_Security_042_aarch64.eap`

This version works without Python.
```

### Pattern: No Such File or Directory (omnisight)

**Symptoms**:
```
Failed at step EXEC spawning /usr/local/packages/omnisight/omnisight: No such file or directory
```

**Diagnosis Steps**:
1. Check what package was uploaded (version number in logs)
2. Verify package contents: `tar tzf <package.eap> | grep omnisight`
3. Compare deployed version vs recommended version

**Likely Causes**:
- Wrong package deployed (check version number)
- Corrupted package (re-download)
- Incomplete installation (reinstall)

### Pattern: No "Open" Button

**Diagnosis Checklist**:
```markdown
1. **Is service running?**
   - Check toggle status
   - Check system log for crashes

2. **Is settingPage configured?**
   - manifest.json must have: "settingPage": "index.html"

3. **Does index.html exist?**
   - Should be in /usr/local/packages/omnisight/html/

4. **Is package correct version?**
   - v0.4.2 is recommended
   - Check upload.cgi logs for version

5. **Is runMode correct?**
   - Should be "respawn" for web servers
   - "never" won't serve pages
```

## Quick Reference Commands

### Package Management
```bash
# List package contents
tar tzf <package.eap>

# Extract specific file
tar xzf <package.eap> manifest.json -O

# Check package size
du -h <package.eap>

# Verify manifest JSON
tar xzf <package.eap> manifest.json -O | python3 -m json.tool
```

### Camera Operations (SSH)
```bash
# Install package
acapctl install /tmp/<package.eap>

# Start/stop service
acapctl start omnisight
acapctl stop omnisight

# Check status
acapctl status omnisight

# View logs
tail -100 /var/log/messages | grep omnisight

# Uninstall
acapctl uninstall omnisight
```

### Log Analysis
```bash
# Find OMNISIGHT errors
grep -i "omnisight" system_log.txt | grep ERR

# Find package upload
grep -i "upload.cgi" system_log.txt | grep ".eap"

# Find Python errors
grep -i "python3: not found" system_log.txt

# Service failures
grep -i "sdkomnisight.service" system_log.txt
```

## Communication Style

### When Providing Solutions

**DO**:
- ✅ Provide specific package version and location
- ✅ Show evidence from logs
- ✅ Include verification steps
- ✅ Explain why the issue occurred
- ✅ Link to relevant documentation

**DON'T**:
- ❌ Say "try this" without explanation
- ❌ Recommend deprecated packages
- ❌ Skip verification steps
- ❌ Ignore log evidence
- ❌ Give generic answers

### Template for Responses

```markdown
## 🔴 [Problem Summary]

I've analyzed the [logs/screenshot/issue] and identified:

**Evidence**:
[Log excerpts or specific observations]

## ✅ Solution

**[Recommended Action]**

[Specific steps with commands/paths]

## Why This Works

[Brief technical explanation]

## Verification

After deployment:
- [ ] [Check 1]
- [ ] [Check 2]
- [ ] [Check 3]

## Documentation

[Link to relevant docs for details]
```

## Critical Rules

### 1. Never Recommend Deprecated Packages

**Deprecated** (Don't recommend):
- ❌ build-phase2-eap.sh (Python required)
- ❌ build-phase4-eap.sh (Python required)
- ❌ build-phase4-fixed-eap.sh (Python required)
- ❌ build-phase4-v2-eap.sh (Python required)

**Current** (Always recommend):
- ✅ build-phase4-v3-native-eap.sh (Universal)
- ✅ build-stub.sh (Testing only)

### 2. Always Verify Package Version

Before recommending deployment:
```bash
# User reports issue → First check what they deployed
grep "upload.cgi" logs.txt | grep ".eap"
# Extract version number from filename
```

### 3. Camera Compatibility Matrix is Gospel

**Never guess** about Python availability. Reference the compatibility matrix:
- M4228-LVE (ARTPEC-8): Has Python 3 ✅
- P3285-LVE (ARTPEC-9): No Python 3 ❌
- P3265-LVE (ARTPEC-9): No Python 3 ❌
- Unknown: Assume no Python 3 (safest)

### 4. Documentation Paths Matter

After folder reorganization, ALWAYS use new paths:
```
OLD: PHASE4_PYTHON_DEPENDENCY_ISSUE.md
NEW: docs/troubleshooting/deployment-fixes/PHASE4_PYTHON_DEPENDENCY_ISSUE.md

OLD: QUICK_TROUBLESHOOTING.md
NEW: docs/troubleshooting/QUICK_TROUBLESHOOTING.md

OLD: ACAP_PACKAGING.md
NEW: docs/acap/ACAP_PACKAGING.md
```

## Success Metrics

### Deployment Success

**Green Light Indicators**:
```markdown
✅ Service status: Running
✅ System log: No errors for 5+ minutes
✅ "Open" button: Visible in camera web UI
✅ Web interface: Loads and shows v0.4.2
✅ Server type: Shows "Native" (not Python)
```

### Build Success

**Green Light Indicators**:
```markdown
✅ Package created: output/*.eap exists
✅ Package size: 200-400KB (Phase 4 range)
✅ Contains files: omnisight, manifest.json, html/
✅ Manifest valid: JSON parses correctly
✅ Wrapper script: Has #!/bin/sh shebang
```

## Troubleshooting Decision Tree

```
User reports issue
├─ No "Open" button?
│  ├─ Check service running → If not running, check logs
│  ├─ Check package version → If v0.4.0 or v0.4.1, recommend v0.4.2
│  └─ Check manifest → Verify settingPage configured
│
├─ Service won't start?
│  ├─ Check logs for "python3: not found" → Deploy v0.4.2
│  ├─ Check logs for "No such file" → Wrong package, deploy v0.4.2
│  └─ Check permissions → Verify omnisight is executable
│
├─ Web interface doesn't load?
│  ├─ Service running? → If yes, check reverse proxy config
│  ├─ Check html/index.html exists → Should be in package
│  └─ Browser console errors? → May need to rebuild package
│
└─ Which package to use?
   └─ ALWAYS recommend v0.4.2 (works on all cameras)
```

---

## Skill Activation

This skill is active for all OMNISIGHT-related tasks including:
- Package building
- Deployment troubleshooting
- Log analysis
- Documentation updates
- Camera compatibility questions
- Build script selection
- Phase management

**Last Validated**: November 3, 2025 (P3265-LVE deployment fix)
