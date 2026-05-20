---
name: release-stable
description: Create a stable production release with intelligent detection (finalize beta or direct release). Use when publishing stable releases, finalizing beta versions, or creating production releases.
---

# Create Stable Production Release

Create a **STABLE release** for production use.

Current version: Check `package.json` for current version.

## ⚠️ CRITICAL TAG FORMAT RULE

**NEVER use 'v' prefix in git tags!**

- ✅ CORRECT: `1.5.0`
- ❌ WRONG: `v1.5.0`

The GitHub workflows expect tags WITHOUT 'v' prefix. Using 'v' will cause workflow failures.
All scripts (`bump-version.sh`, `create-release.sh`) already create tags without 'v'.
**Never create tags manually** - always use the scripts.

## Intelligent Workflow

The workflow adapts automatically based on the current version:

**From beta** (1.5.0-beta.3 → 1.5.0) → Automatic finalization, no analysis needed
**Direct stable release** (1.4.0 → 1.5.0) → AI analyzes commits and suggests version type with warning

---

## Phase 1: Release Type Detection

**Automatically detect release scenario:**

1. **Detect release scenario:**
   - Current version: `1.5.0-beta.3` → **Finalize beta** (automatic, no validation)
   - Current version: `1.4.0` (stable) → **Direct release** (requires AI analysis + warning)

2. **For finalize beta:**
   - Strip `-beta.N` suffix automatically
   - Skip commit analysis (already done during beta)
   - Faster workflow (3-5 min)

3. **For direct stable release:**
   - Show **WARNING** about skipping beta testing (risky)
   - Run commit analysis: `npm run analyze:commits`
   - Analyze commit types (feat, fix, BREAKING CHANGE)
   - Determine version bump type (patch/minor/major)
   - Present detailed validation with option to create beta instead

---

## Phase 2A: Finalize Beta (Automatic)

**Current: 1.5.0-beta.3 → Stable: 1.5.0**

Present automatic finalization message:
- Current version and target stable version
- Note that version type was already determined during beta
- No additional analysis or validation required
- Proceed automatically to release notes and validation

**No user validation required** → Proceeds directly to Phase 3

---

## Phase 2B: Direct Stable Release (Requires Validation)

**Current: 1.4.0 → Proposed: 1.5.0**

### Beta Testing Warning

Present warning about direct stable release:
- Risks: No community feedback, untested in real environments, bugs reach production, harder rollback
- Recommendation: Create beta first
- User options:
  - [1] YES - Continue with direct release (risky)
  - [2] CREATE BETA INSTEAD - Safer approach
  - [3] CANCEL - Abort

**If user chooses [2] CREATE BETA:** Stop and use release-beta skill

**If user chooses [1] PROCEED:** Show detailed AI analysis

### AI Semantic Analysis (Direct Release Only)

Present detailed analysis with:
- Current version and proposed version
- Warning about skipping beta
- Commit breakdown (feat, fix, breaking, etc.)
- AI reasoning with confidence level
- Recommendation to test as beta first
- Key commits (most impactful)
- User decision options:
  - [1] APPROVE - Proceed with AI suggestion (skipping beta)
  - [2] DOWNGRADE TO PATCH - Override AI (skipping beta)
  - [3] UPGRADE TO MAJOR - Override AI (skipping beta)
  - [4] CREATE BETA INSTEAD - Safer approach (recommended)
  - [5] VIEW COMMITS - Show full commit list
  - [6] CANCEL - Abort safely

---

## Phase 3: Release Notes Generation & Editing

**Automatically:**

1. **Generate release notes** (`bash scripts/generate-release-notes.sh`)
2. **AI-powered editing:**
   - Remove noise (version bumps, merges, CI commits, deps updates)
   - Enhance features/fixes (bold title + detailed description)
   - Translate to French (same detail level)
   - Remove beta testing section (not needed for stable)
   - Add upgrade instructions if needed
   - Remove TODO markers
3. **Format for GitHub** (`bash scripts/format-release-notes.sh`)

---

## Phase 4: Quality Validation (BLOCKING)

**All must pass:**

**A. Release notes validation** (`scripts/validate-release-notes.sh`)
- Required sections EN/FR
- No TODO
- No beta testing section
- Bold features

**B. Code quality (17 checks)** (`scripts/check-release-ready.sh`)
1. Git clean 2. Branch main 3. Up-to-date 4. Deps installed 5. Lint 6. Type-check 7. Build 8. Version consistency 9. No FIXME 10. CHANGELOG 11. manifest.json 12. hacs.json 13. No secrets 14. Python syntax 15. README 16. LICENSE 17. Smoke tests ready

**C. Smoke tests (15 tests)** (`npm run test:smoke`)

---

## Phase 5: Final Approval & Publication

**For finalize beta:**

Present approval with:
- Version and finalization info
- Note that beta testing completed successfully
- Changes summary (features, bug fixes) since last stable
- Validation results
- What happens if approved

User options:
- [1] APPROVE - Publish stable release
- [2] REQUEST CHANGES - Modify release notes
- [3] VIEW FULL NOTES - See complete file
- [4] CANCEL - Abort

**For direct stable release:**

Present approval with:
- Version and bump type
- Warning about skipping beta testing
- Changes summary
- Validation results
- Reminder to monitor closely

User options:
- [1] APPROVE - Publish stable release (skipping beta)
- [2] CREATE BETA INSTEAD - Safer approach
- [3] REQUEST CHANGES - Modify release notes
- [4] VIEW FULL NOTES - See complete file
- [5] CANCEL - Abort

---

## Phase 6: Publication (Only after approval)

**For finalize beta (automatic version):**

1. **Bump version** (`bash scripts/bump-version.sh release`)
   - Strips `-beta.N`: 1.5.0-beta.3 → 1.5.0
2. **Update release notes** with final version
3. **Commit + tag** (`git commit` + `git tag`)
4. **Push** (`git push && git push --tags`)
5. **Report success** with forum links

**For direct stable release (explicit version type):**

1. **Bump version** (`bash scripts/bump-version.sh release <patch|minor|major>`)
   - Example: `bash scripts/bump-version.sh release minor` → 1.5.0
2. **Update release notes** with final version
3. **Commit + tag** (`git commit` + `git tag`)
4. **Push** (`git push && git push --tags`)
5. **Report success** with forum links

**GitHub Actions automatically:**
- Builds project
- Runs smoke tests
- Creates ZIP
- Creates stable release
- Sends Discord notification (public announcement)
- Cleans up RELEASE_NOTES.md

**Manual step:**
- Open forum threads: `npm run forums:open`
- Post release announcement (templates provided)

---

## Quality Standards

**Release notes:** EN+FR equal quality, no TODO, detailed explanations, user-focused, clean, no beta testing section

**Code:** 17 checks passed, 15 smoke tests passed, lint+type-check passed, build succeeded

**Version decision:**
- Finalize beta: Automatic, no validation
- Direct release: AI analyzes commits, warns about skipping beta, requires user validation

---

## Options

### Dry Run
```
--dry-run
```
Runs everything, creates commit+tag locally, **STOPS before push**. Nothing published.
To undo: `git reset HEAD~1 && git tag -d X.Y.Z`

### Skip Approval (Final approval only)
```
--skip-approval
```
Shows summary but **auto-approves final publication**. Still shows warning and requires version decision for direct releases. ⚠️ Use with extreme caution.

---

## Logs

Every release logged to: `.opencode/logs/release-stable-{timestamp}.log`

Contains: timestamps, detection logic, commit analysis (if direct), AI reasoning, warnings shown, user decisions, git hashes, URLs, duration

---

## Common Errors

**Validation fails** → Fix issues, re-run command
**Smoke tests fail** → Check `npm run test:smoke`, fix, re-run
**Build fails** → Run `npm run build`, fix errors, re-run
**Push fails** → `git pull --rebase`, re-run
**Tag exists** → `git tag -d X.Y.Z` then re-run
**Ambiguous commits** (direct release) → AI asks you to decide manually
**Beta recommended** → Use release-beta skill first for safer release

---

## Related Commands

**Before stable release:**
- Recommended: Use release-beta skill (test first)
- Check status: Use release-check skill

**After stable release:**
- Hotfix needed → Use release-stable skill again (creates patch: 1.5.0 → 1.5.1)
- Critical issue → Use release-rollback skill
- Announce → `npm run forums:open`

---

## Release Type Detection Logic

| Current Version | Detection | AI Analysis | Beta Warning | User Validation | Result |
|----------------|-----------|-------------|--------------|-----------------|--------|
| `1.5.0-beta.3` | Finalize | ❌ No | ❌ No | ❌ Not required | `1.5.0` (stable) |
| `1.4.0` (stable) | Direct | ✅ Yes | ✅ Yes | ✅ Required | `1.5.0` (if MINOR) |

---

## Important

- **Finalize beta:** Automatic and fast (no validation, already tested)
- **Direct stable:** Requires AI analysis + shows warning about skipping beta + requires your validation
- **Best practice:** Always test with beta first (release-beta → test → release-stable)
- All validations are blocking (must pass)
- Idempotent (safe to re-run)
- Logs everything
- Time: 3-5 min (finalize) or 5-10 min (direct release)

**Scripts Used:**
- `scripts/analyze-commits.sh` - Commit analysis (direct release only)
- `scripts/bump-version.sh release [patch|minor|major]` - Version bumping
- `scripts/generate-release-notes.sh` - Release notes generation
- `scripts/format-release-notes.sh` - Formatting
- `scripts/validate-release-notes.sh` - Validation
- `scripts/check-release-ready.sh` - Code quality checks

**Forum Announcement:**
After successful release, use `npm run forums:open` to announce on Home Assistant Community Forum and HACF.
