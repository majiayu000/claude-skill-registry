---
description: Discover and use existing scripts from the script library before writing new code
tags: [scripts, reuse, deployment, testing, automation]
techStack: [powershell, javascript, dotnet]
appliesTo: ["deploy", "test", "validate", "diagnose", "setup"]
alwaysApply: true
---

# script-aware

> **Category**: Context Loading (Always-Apply)
> **Last Updated**: December 2025

---

## Purpose

Prevent Claude Code from re-engineering or rewriting commonly reused scripts by proactively checking the script library before implementation.

**Problem this solves**: Claude Code often writes new scripts for tasks that already have tested, working scripts in `scripts/`.

**Solution**: Load script registry context before coding tasks that involve deployment, testing, validation, or automation.

---

## When to Apply

This skill is **always-apply** and triggers when:

1. **Task tags include**: `deploy`, `test`, `validate`, `diagnose`, `setup`, `automation`
2. **Task steps mention**: deployment, testing, validation, health checks, diagnostics
3. **User requests**: "deploy to...", "test the...", "validate...", "check..."
4. **Creating new scripts**: Before writing any `.ps1`, `.js`, or automation script

---

## Script Discovery Protocol

### Step 1: Load Script Registry

```
READ scripts/README.md

EXTRACT:
  - Script categories (Deployment, Testing, Setup, Diagnostics)
  - Script names and purposes
  - Usage frequency (Active/Occasional/Archive)
  - Dependencies and prerequisites
```

### Step 2: Match Task to Scripts

```
FOR current task/request:
  IDENTIFY keywords: deploy, test, validate, PCF, API, Dataverse, SPE, etc.

  SEARCH scripts/README.md for matching scripts:
    - By category (Deployment, Testing, etc.)
    - By target (PCF, API, custom page, etc.)
    - By action (deploy, test, validate, export, import)

IF matching script found:
  → USE existing script (invoke or reference)
  → DO NOT rewrite equivalent functionality

IF no matching script:
  → PROCEED with implementation
  → CONSIDER creating new script (see Script Creation below)
```

### Step 3: Script Invocation

```
WHEN invoking a script:
  1. READ the script file to understand parameters
  2. CHECK prerequisites (PAC CLI auth, az login, etc.)
  3. INVOKE with appropriate parameters
  4. HANDLE output and errors

COMMON PATTERNS:
  - PCF deployment: .\Deploy-PCFWebResources.ps1 -ControlName "X"
  - API testing: .\Test-SdapBffApi.ps1 -Environment "dev"
  - Health check: node test-sdap-api-health.js <url>
```

---

## Script Categories Quick Reference

### Deployment Scripts (Use for: PCF, Custom Pages, Web Resources)

| Script | Purpose | When to Use |
|--------|---------|-------------|
| `Deploy-PCFWebResources.ps1` | Deploy PCF to Dataverse | After `npm run build` |
| `Deploy-CustomPage.ps1` | Deploy custom pages | After custom page changes |
| `Deploy-ThemeIcons.ps1` | Deploy theme icons | After icon updates |
| `Deploy-SubgridCommands.ps1` | Deploy subgrid commands | After ribbon changes |

### Testing Scripts (Use for: API validation, Health checks)

| Script | Purpose | When to Use |
|--------|---------|-------------|
| `Test-SdapBffApi.ps1` | Comprehensive API test | After API deployment |
| `test-sdap-api-health.js` | Quick health check | Quick validation |
| `test-dataverse-connection.cs` | Test Dataverse connectivity | Connection issues |

### Diagnostic Scripts (Use for: Troubleshooting)

| Script | Purpose | When to Use |
|--------|---------|-------------|
| `Diagnose-AiSummaryService.ps1` | Debug AI summary issues | AI feature problems |
| `Debug-RegistrationFailure.ps1` | Debug SPE registration | SPE setup issues |
| `Check-ContainerType-Registration.ps1` | Verify CT registration | SPE validation |

### Export/Import Scripts (Use for: Ribbon, Solution work)

| Script | Purpose | When to Use |
|--------|---------|-------------|
| `Export-EntityRibbon.ps1` | Export entity ribbon XML | Before ribbon edits |
| `Export-ThemeRibbon.ps1` | Export theme ribbon | Theme customization |

---

## Script Creation Protocol

### When to Create a New Script

Create a new script when:

1. **Repeated task**: Same sequence of commands used 3+ times
2. **Complex automation**: Multi-step process that benefits from encapsulation
3. **Reusable utility**: Functionality useful across multiple projects/tasks
4. **No existing script**: Checked registry, nothing matches

### Script Creation Checklist

```
BEFORE creating new script:
  [ ] Searched scripts/README.md - no existing match
  [ ] Task is repeatable (not one-time)
  [ ] Script adds value over inline commands

WHEN creating new script:
  1. Follow naming convention: Action-Target-Method.ps1
  2. Add inline documentation (synopsis, parameters, examples)
  3. Add entry to scripts/README.md with:
     - Purpose
     - Usage frequency (likely: Active/Occasional)
     - Lifecycle status (Maintained)
     - Dependencies
     - When to use
     - Command example
  4. Place in appropriate location:
     - General: scripts/
     - Project-specific: projects/{name}/scripts/
     - Module-specific: src/{module}/scripts/

AFTER creating new script:
  [ ] README.md entry added
  [ ] Script tested and working
  [ ] Dependencies documented
```

### Script Template

```powershell
<#
.SYNOPSIS
    Brief description of what this script does

.DESCRIPTION
    Detailed description including:
    - What problem it solves
    - Prerequisites
    - Expected outcomes

.PARAMETER ParameterName
    Description of the parameter

.EXAMPLE
    .\Script-Name.ps1 -Parameter "value"
    Description of what this example does

.NOTES
    Author: Claude Code
    Created: YYYY-MM-DD
    Dependencies: List any required tools (PAC CLI, az, etc.)
#>

param(
    [Parameter(Mandatory=$true)]
    [string]$RequiredParam,

    [Parameter(Mandatory=$false)]
    [string]$OptionalParam = "default"
)

# Implementation
```

---

## Script Maintenance Protocol

### After Task Completion

```
IF task involved using a script:
  VERIFY script still works as expected
  IF script needed modifications:
    UPDATE the script file
    UPDATE scripts/README.md if behavior changed

IF task created reusable automation:
  EVALUATE: Should this become a script?
  IF yes: Follow Script Creation Protocol
```

### Script Registry Maintenance

```
WHEN working with scripts:
  CHECK scripts/README.md is accurate:
    - Last Used dates current
    - Usage frequency reflects reality
    - Deprecated scripts marked

  UPDATE if needed:
    - Add new scripts created
    - Mark unused scripts as Archive
    - Update dependencies if changed
```

---

## Integration with Other Skills

### task-execute Integration

The `task-execute` skill should:
1. Load this skill's context for tasks with deployment/testing tags
2. Check script registry before coding automation steps
3. Update script registry after task completion if scripts were created/modified

### project-pipeline Integration

The `project-pipeline` skill should:
1. Discover relevant scripts during resource discovery (Step 1)
2. Include applicable scripts in PLAN.md "Discovered Resources"
3. Reference scripts in generated task files where applicable

### dataverse-deploy Integration

The `dataverse-deploy` skill should:
1. Reference deployment scripts rather than inline commands
2. Use `Deploy-PCFWebResources.ps1` for PCF deployment
3. Use `Test-SdapBffApi.ps1` for post-deployment validation

---

## Example: Task with Script Awareness

**Task**: Deploy updated AISummaryPanel PCF control

**Without script-aware**:
```
Claude writes new deployment commands inline...
```

**With script-aware**:
```
1. CHECK scripts/README.md for deployment scripts
2. FIND: Deploy-PCFWebResources.ps1 matches "PCF deployment"
3. READ script to understand parameters
4. INVOKE: .\scripts\Deploy-PCFWebResources.ps1 -ControlName "AISummaryPanel"
5. VERIFY deployment with Test-SdapBffApi.ps1
```

---

## Failure Modes to Avoid

| Failure | Cause | Prevention |
|---------|-------|------------|
| Rewrote existing script | Didn't check registry | ALWAYS read scripts/README.md first |
| Script not found | Registry out of date | Keep README.md updated |
| Wrong script used | Misunderstood purpose | READ script file, not just name |
| Script failed | Missing prerequisites | CHECK dependencies before invoking |

---

## Related Files

- **Script Registry**: `scripts/README.md`
- **Script Location**: `scripts/` (general), `projects/*/scripts/` (project-specific)
- **task-execute**: `.claude/skills/task-execute/SKILL.md`
- **dataverse-deploy**: `.claude/skills/dataverse-deploy/SKILL.md`

---

*This skill ensures Claude Code reuses existing automation rather than reinventing it, and maintains the script library for future use.*
