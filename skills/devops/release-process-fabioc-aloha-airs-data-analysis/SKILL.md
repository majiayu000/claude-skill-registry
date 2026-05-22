---
name: "Release Process Skill"
description: "Complete release automation for VS Code Marketplace publishing"
---

# Release Process Skill

**Classification**: Master-Only Skill | Process Automation
**Activation**: release, publish, marketplace, vsix, version bump, pre-release
**Inheritance**: master-only (contains PAT handling, marketplace credentials)

---

## Purpose

Comprehensive knowledge for releasing Alex Cognitive Architecture to VS Code Marketplace and managing version lifecycle.

---

## Quick Reference

### Release Commands

```powershell
# From repo root
.\scripts\release-vscode.ps1 -BumpType patch              # Stable release
.\scripts\release-vscode.ps1 -BumpType minor -PreRelease  # Pre-release
.\scripts\release-vscode.ps1 -BumpType patch -DryRun      # Test without publishing
```

### Manual Publishing

```powershell
cd platforms/vscode-extension
npx vsce publish --pre-release  # Pre-release
npx vsce publish                # Stable release
```

---

## PAT (Personal Access Token) Setup

> ⚠️ **IMPORTANT**: PATs expire frequently and may only work for a single publish session.
> Always create a fresh PAT before each release to avoid 401 errors.

### Creating a New PAT

1. **Via Marketplace** (Recommended):
   - Go to: https://marketplace.visualstudio.com/manage/publishers/
   - Click your publisher name
   - Click "..." menu → "Generate new token"
   - Copy the token immediately (shown only once)

2. **Via Azure DevOps**:
   - Go to: https://dev.azure.com/
   - Click User Settings (gear icon) → Personal Access Tokens
   - Click "New Token"
   - Name: `vsce-marketplace` (or similar)
   - Organization: `All accessible organizations`
   - Expiration: Set appropriate duration (max 1 year)
   - Scopes: Select `Marketplace` → `Manage`
   - Click Create, copy token

### Storing the PAT

**Option 1: Environment Variable** (Session only)
```powershell
$env:VSCE_PAT = "your-token-here"
```

**Option 2: .env File** (Persistent, gitignored)
```
# platforms/vscode-extension/.env
VSCE_PAT=your-token-here
```

**Option 3: System Environment** (Persistent)
```powershell
[Environment]::SetEnvironmentVariable("VSCE_PAT", "your-token", "User")
```

### PAT Troubleshooting

| Error | Cause | Solution |
|-------|-------|----------|
| 401 Unauthorized | PAT expired or invalid | Create new PAT |
| 401 Unauthorized | Wrong scope | Ensure "Marketplace (Manage)" scope |
| 403 Forbidden | Not publisher owner | Check publisher membership |
| Token not found | .env not loaded | Check file path, run preflight |

---

## Version Strategy

### Semantic Versioning

```
MAJOR.MINOR.PATCH
  │     │     └── Bug fixes, docs
  │     └──────── New features, non-breaking
  └────────────── Breaking changes
```

### Pre-Release vs Stable

| Type | Flag | Visibility | Use Case |
|------|------|------------|----------|
| Pre-release | `--pre-release` | Opt-in only | Beta testing |
| Stable | (none) | Everyone | Production ready |

**VS Code Marketplace Rule**: Pre-release versions must use the `--pre-release` flag, NOT semver suffixes like `-beta.1`.

### Version Files to Update

When bumping version, these files need synchronization:

1. `platforms/vscode-extension/package.json` → `version` field
2. `platforms/vscode-extension/.github/copilot-instructions.md` → `**Version**:` line
3. `CHANGELOG.md` → New `## [X.Y.Z]` section

The `release-vscode.ps1` script handles all of these automatically.

---

## Release Workflow

### Automated (Recommended)

```
┌─────────────────────────────────────────────────────────────────┐
│  .\scripts\release-vscode.ps1 -BumpType patch -PreRelease       │
└─────────────────────────────────────────────────────────────────┘
         │
         ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│ 0. PAT Check    │───▶│ 1a. Sync Heir   │───▶│ 1b. Preflight   │
│ - Load .env     │    │ - build-pkg.ps1 │    │ - Version sync  │
│ - Validate      │    │ - Master→Heir   │    │ - Build/Lint    │
│                 │    │                 │    │ - Manifest check│
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │
         ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│ 2. Version Bump │───▶│ 3. CHANGELOG    │───▶│ 4. Git Commit   │
│ - package.json  │    │ - Add entry     │    │ - Commit        │
│ - heir version  │    │ - Date stamp    │    │ - Tag           │
│                 │    │                 │    │ - Push          │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │
         ▼
┌─────────────────┐
│ 5. Publish      │
│ - vsce publish  │
│ - --pre-release │
└─────────────────┘
```

### Definition of Done Verification

**Before publishing**, verify ALL 8 criteria from ROADMAP-UNIFIED.md:

| # | Criterion | Validation Method |
|---|-----------|-------------------|
| 1 | Builds clean | `npm run compile` exits 0 with zero errors |
| 2 | No dead code | All imports resolve, no orphaned modules |
| 3 | Counts match reality | Slash commands, tools, skills, trifectas in docs = actual code |
| 4 | F5 smoke test passes | Extension activates, welcome view renders, 3 random commands work |
| 5 | Version aligned | package.json = CHANGELOG = copilot-instructions |
| 6 | Heir sync clean | `sync-architecture.js` runs with 0 errors, no contamination |
| 7 | No non-functional features | If in UI/command palette, it works. If broken, removed. |
| 8 | CHANGELOG documents delta | Every user-visible change has a line item |

**Pattern**: Use regression checklist as DoD tracker:
- Create `alex_docs/operations/VXXX-REGRESSION-CHECKLIST.md`
- Track verification status for each criterion
- Document evidence (commit hashes, test counts, sync output)
- Automated tests provide objective quality signal (test count = confidence metric)

**Quality Gate**: If ANY criterion fails, DO NOT publish. Fix first.

### Manual Checklist

If not using the script:

- [ ] Run preflight: `.\scripts\release-preflight.ps1 -Package`
- [ ] Bump version in `package.json`
- [ ] Update heir `copilot-instructions.md` version
- [ ] Add CHANGELOG entry
- [ ] Commit: `git commit -m "chore: release vX.Y.Z"`
- [ ] Tag: `git tag vX.Y.Z`
- [ ] Push: `git push && git push --tags`
- [ ] Publish: `npx vsce publish [--pre-release]`

---

## Preflight Checks

The `release-preflight.ps1` script validates:

| Check | What It Does |
|-------|--------------|
| PAT | Verifies VSCE_PAT is available in env or .env |
| Version Sync | package.json = CHANGELOG = Master instructions = heir instructions |
| BUILD-MANIFEST | Checks heir was synced recently (warns if > 24h old) |
| README Skill Count | Verifies documented skill count matches actual |
| ROADMAP Version | Warns if ROADMAP-UNIFIED.md version differs |
| Build | `npm run compile` succeeds |
| Lint | `npm run lint` passes |
| Tests | `npm test` passes (can skip with `-SkipTests`) |
| Git Status | Shows uncommitted changes |
| Git Tags | Warns if tag already exists |
| Package | Creates VSIX (with `-Package` flag) |

---

## File Structure

```
Alex_Plug_In/
├── scripts/
│   ├── release-preflight.ps1    # Pre-release validation
│   ├── release-vscode.ps1       # Full release automation
│   └── build-extension-package.ps1  # Heir sync
├── platforms/vscode-extension/
│   ├── package.json             # Version source of truth
│   ├── .env                     # PAT storage (gitignored)
│   ├── .github/
│   │   └── copilot-instructions.md  # Heir version
│   └── *.vsix                   # Built packages
└── CHANGELOG.md                 # Version history
```

---

## Common Issues

### "The pre-release version is not valid"

**Cause**: Used semver suffix like `3.7.4-beta.1`

**Solution**: Use plain version `3.7.4` with `--pre-release` flag

### "401 Unauthorized"

**Cause**: PAT expired, invalid, or wrong scope

**Solution**:
1. Create new PAT at marketplace.visualstudio.com/manage/publishers
2. Ensure "Marketplace (Manage)" scope
3. Update .env or environment variable

### "Version already exists"

**Cause**: Trying to publish same version twice

**Solution**: Bump version first, or delete existing version from marketplace

### Build succeeds but publish fails

**Cause**: Often network or auth issues

**Solution**:
1. Check internet connection
2. Verify PAT is valid
3. Try `npx vsce login <publisher-name>` first

---

## Links

- [VS Code Publishing Guide](https://code.visualstudio.com/api/working-with-extensions/publishing-extension)
- [Marketplace Publisher Portal](https://marketplace.visualstudio.com/manage/publishers/)
- [Azure DevOps PAT Docs](https://learn.microsoft.com/en-us/azure/devops/organizations/accounts/use-personal-access-tokens-to-authenticate)
- [VSCE CLI Reference](https://github.com/microsoft/vscode-vsce)
