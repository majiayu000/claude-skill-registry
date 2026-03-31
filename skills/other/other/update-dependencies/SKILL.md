---
name: update-dependencies
description: "Upgrade project dependencies with breaking change research for major version updates. Use when the user asks to \"update dependencies\", \"upgrade packages\", \"upgrade dependencies\", \"update deps\", \"upgrade deps\", \"update npm deps\", \"update Swift packages\", \"cargo update\", \"go get updates\", \"bundle update\", or \"pip upgrade\"."
argument-hint: "[package-filter]"
---

# Update Dependencies

Upgrade project dependencies, researching breaking changes for major version updates.

Optional filter: `$ARGUMENTS` (e.g., `react`, `Alamofire`, `serde tokio`)

## Phase 1: Review Dependencies

Run the `/review-dependencies` skill to detect package managers and discover available updates. If no updates are available, stop.

## Phase 2: User Strategy Selection

Present a summary showing:
- Count and list of major updates (with current → target versions)
- Count of minor updates
- Count of patch updates

Use AskUserQuestion for upgrade strategy:

**Header**: "Strategy"
**Options**:
- **Cautious** — Upgrade minor/patch first, then major one-by-one with research
- **All at once** — Research all major changes, then upgrade everything together
- **Skip major** — Only upgrade minor and patch versions
- **Interactive** — Ask for each major update individually

## Phase 3: Research Breaking Changes

For **each package with a major version update**:

### Step 1: Calculate Version Gap

Identify all major versions between current and target. For example:
- `react: 17.0.2 → 19.0.0` → research v18 AND v19 breaking changes
- `Alamofire: 4.9.1 → 6.0.0` → research v5 AND v6 breaking changes

### Step 2: Research Each Major Version

Search for migration documentation:

```
WebSearch: "[package-name] v[X] migration guide"
WebSearch: "[package-name] v[X] breaking changes"
```

Common sources: GitHub releases page, official docs, changelog files.

### Step 3: Extract Key Breaking Changes

Identify: API changes (renamed/removed functions), configuration changes, peer/transitive dependency requirements, behavioral changes, deprecated features now removed.

### Step 4: Search Codebase for Affected Code

Use Grep to find usage of deprecated or changed APIs. Document which files are affected and what changes are needed.

## Phase 4: User Confirmation

For each major update, present:
- Package name and version transition
- Breaking changes found (summarized)
- Files potentially affected (count and list)

Use AskUserQuestion to confirm:

**Header**: "Confirm"
**Options**:
- **Proceed** — Continue with upgrades and migrations
- **Show details** — Display detailed breaking changes for review
- **Skip package** — Exclude a specific package from upgrade
- **Abort** — Cancel the upgrade process

If "Show details" selected, display full migration research, then ask again.

## Phase 5: Execute Upgrades

### Cautious Strategy

First upgrade minor and patch only using the package manager's semver-respecting update command, then run tests. If tests fail, stop before proceeding with major upgrades.

### Major Version Upgrades

Update the manifest file (version constraint) and run the install/resolve command. For package managers with a dedicated upgrade command, use it. For others (Swift PM, Maven, Gradle), edit the manifest directly.

## Phase 6: Apply Migrations

### Step 1: Run Codemods (if Available)

Some ecosystems provide automated migration tools:

| Ecosystem | Migration tools |
|---|---|
| React | `npx react-codemod [transform]` |
| Next.js | `npx @next/codemod [transform]` |
| Jest | `npx jest-codemods` |
| Angular | `npx ng update` |
| Rust | `cargo fix` for edition migrations |
| Python | `pyupgrade`, `python-modernize` |

### Step 2: Manual Code Changes

For changes requiring manual intervention:
1. Read the affected file
2. Apply the necessary transformation using Edit
3. Show the user what changed

### Step 3: Update Configuration Files

If configuration format changed, read current config, transform to new format, write updated config.

## Phase 7: Verification

Run the project's test, build, and lint commands. Detect which commands are available from the project's config files and scripts. Use project-level task runners when present (`Makefile`, `Taskfile`, `justfile`, npm scripts, etc.).

### Report Results

Summarize: packages upgraded (count), breaking changes addressed (count), files modified (count), test results, remaining manual tasks.

### Recommend Next Steps

If any migrations could not be automated:
- List specific changes the user needs to review
- Highlight deprecated patterns that need attention
- Note any runtime behavior changes to watch for

## Error Handling

### Discovery Tool Not Available

If the discovery tool is not installed, `/review-dependencies` will note it. Fall back to manual version checking via WebSearch.

### Network Errors During Research

If WebSearch/WebFetch fails: retry with alternative search terms, provide manual research links, proceed with caution warning that migration research may be incomplete.

### Test Failures After Upgrade

- Stop the upgrade process
- Suggest rollback: restore manifest and lockfile from git, then reinstall
- Identify which package likely caused the failure

### Migration Research Incomplete

If official migration docs are not found: check the package's repository for issues and discussions, note as "migration research incomplete — proceed with caution."
