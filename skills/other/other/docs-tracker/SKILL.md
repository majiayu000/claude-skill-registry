---
name: docs-tracker
description: Automates documentation maintenance. Detects modified files via git diff, creates docs for new files, updates docs for modified files, generates changelog. Use after implementation to keep docs current.
allowed-tools: Read, Glob, Grep, Bash
---

# Docs Tracker - Automatic Documentation System

## Purpose

This skill automates documentation maintenance:

- **Detects** modified files via git diff
- **Compares** with existing documentation
- **Creates** docs for new files
- **Updates** docs for modified files
- **Removes** docs for deleted files
- **Generates** automatic changelog

---

## Execution Flow

```
1. DETECT CHANGES → git diff --name-status
        ↓
2. CLASSIFY CHANGES → A=Added, M=Modified, D=Deleted
        ↓
3. CHECK EXISTING DOCS → docs/, codebase-knowledge/domains/
        ↓
4. EXECUTE ACTIONS → Create, update, or remove docs
```

---

## Detection Commands

### Changes Since Last Commit

```bash
git diff --name-status HEAD~1
```

### Changes vs Main

```bash
git diff --name-status main..HEAD
```

### Added Files

```bash
git diff --name-status main..HEAD | grep "^A"
```

### Modified Files

```bash
git diff --name-status main..HEAD | grep "^M"
```

### Deleted Files

```bash
git diff --name-status main..HEAD | grep "^D"
```

### Detailed File Diff

```bash
git diff main..HEAD -- path/to/file.ts
```

---

## File → Doc Mapping

| File Type             | Related Documentation                         |
| --------------------- | --------------------------------------------- |
| `server/routers/*.ts` | `codebase-knowledge/domains/[domain].md`      |
| `server/models/*.ts`  | `codebase-knowledge/domains/[domain].md`      |
| `app/**/page.tsx`     | `docs/flows/[feature].md`                     |
| `components/**/*.tsx` | `docs/components/[component].md` (if complex) |
| `lib/**/*.ts`         | `docs/utils/[lib].md` (if exported)           |

---

## Update Rules

### CREATE Doc When:

- [ ] New file in `server/routers/` → Update domain
- [ ] New file in `server/models/` → Update domain
- [ ] New page in `app/` → Create flow doc if complex
- [ ] New complex component → Consider doc

### UPDATE Doc When:

- [ ] tRPC procedure changed signature
- [ ] Model changed schema
- [ ] Page changed main flow
- [ ] Connections between domains changed

### REMOVE Doc When:

- [ ] File was deleted
- [ ] Feature was completely removed
- [ ] Component was discontinued

---

## Changelog Template

```markdown
## [Unreleased] - YYYY-MM-DD

### Added

- New feature X in `path/to/file.ts`
- New component Y

### Changed

- Changed behavior of Z
- Refactored module W

### Fixed

- Fixed bug in A
- Resolved issue #123

### Removed

- Removed obsolete feature B

### Docs Updated

- Updated `codebase-knowledge/domains/[domain].md`
- Created `docs/flows/[feature].md`
```

---

## Pre-Commit Checklist

### 1. Detect Changes

```bash
git diff --name-status --cached
```

### 2. For Each Modified File

- [ ] Which domain does it belong to?
- [ ] Is domain updated in `codebase-knowledge/domains/`?
- [ ] Has flow doc in `docs/flows/`? Needs update?
- [ ] Commit hash will be added to domain?

### 3. For Added Files

- [ ] Which domain? Add to file list
- [ ] Needs own doc or just update domain?
- [ ] Connections with other domains?

### 4. For Deleted Files

- [ ] Remove from `codebase-knowledge/domains/`
- [ ] Remove flow doc if exists
- [ ] Update connections in related domains

---

## Integration with Codebase-Knowledge

### Update Domain After Change

```markdown
## Domain Update: [name]

### Changes Detected

| File         | Status   | Description    |
| ------------ | -------- | -------------- |
| path/file.ts | Modified | [what changed] |

### Required Updates in domains/[domain].md

- [ ] Update "Last Update" with date and commit
- [ ] Add/remove files from list
- [ ] Update "Recent Commits"
- [ ] Check "Connections" if integration changed
- [ ] Update "Attention Points" if applicable
```

---

## Output Format

```markdown
## DOCS TRACKER - Report

### Changes Detected

- **Added:** X files
- **Modified:** Y files
- **Deleted:** Z files

### Docs That Need Update

| Doc              | Type   | Action | Priority |
| ---------------- | ------ | ------ | -------- |
| domains/auth.md  | domain | update | HIGH     |
| flows/feature.md | flow   | create | MEDIUM   |

### Actions Executed

- [x] Updated `domains/auth.md` with commit abc123
- [x] Created `flows/new-feature.md`
- [x] Removed `flows/obsolete.md`

### Changelog Generated

[changelog preview]
```

---

## Critical Rules

1. **ALWAYS run before commit** - Outdated docs are technical debt
2. **NEVER ignore new files** - Every file deserves documentation
3. **KEEP changelog updated** - Facilitates releases
4. **SYNC with codebase-knowledge** - It's the source of truth

---

## Version

- **v2.0.0** - Generic template
