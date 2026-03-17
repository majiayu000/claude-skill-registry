---
name: android-release-notes-structure
description: Create Play Store release notes directory structure with locale templates (Fastlane metadata)
category: android
version: 3.0.0
inputs:
  - locales: List of locales to support (default: en-US)
outputs:
  - fastlane/metadata/android/{locale}/changelogs/ directory structure
  - docs/PLAY_STORE_TRACKS.md
verify: "test -f fastlane/metadata/android/en-US/changelogs/default.txt"
---

# Android Release Notes Structure

Creates directory structure for Play Store release notes with multi-locale support.

## Prerequisites

- Android project

## Inputs

| Input | Required | Default | Description |
|-------|----------|---------|-------------|
| locales | No | en-US | Comma-separated locales (e.g., en-US,de-DE,es-ES) |

## Process

### Step 1: Create Release Notes Directory Structure

```bash
# Create base directory (Fastlane metadata standard structure)
mkdir -p fastlane/metadata/android

# Ask user which locales to support
# Default: en-US
# Common: en-US, de-DE, es-ES, fr-FR, it-IT, ja-JP, ko-KR, pt-BR, zh-CN, zh-TW

# Create changelogs directories for each locale
for locale in ${LOCALES}; do
  mkdir -p "fastlane/metadata/android/${locale}/changelogs"
done
```

### Step 2: Create Template Release Note Files

For each locale, create `fastlane/metadata/android/${LOCALE}/changelogs/default.txt`:

```bash
cat > fastlane/metadata/android/en-US/changelogs/default.txt << 'EOF'
- New: [Feature name]
- Improved: [Enhancement description]
- Fixed: [Bug fix description]

Note: Keep under 500 characters. Focus on user-visible changes.
EOF
```

### Step 3: Create Release Notes README

Create `fastlane/metadata/android/README.md`:

```markdown
# Play Store Release Notes

This directory contains release notes for Google Play Store deployments using Fastlane.

## Structure

Each locale has its own changelogs directory with a `default.txt` file:

```
metadata/android/
├── en-US/
│   └── changelogs/
│       └── default.txt
├── de-DE/
│   └── changelogs/
│       └── default.txt
└── [other locales]/
    └── changelogs/
        └── default.txt
```

## Format Guidelines

**File Requirements:**
- File name: `default.txt`
- Encoding: UTF-8
- Maximum: 500 characters
- Plain text only (no markdown/HTML)

**Content Guidelines:**
- Focus on user-visible changes
- List most important first
- Use bullet points (-, •, or *)
- Be concise and clear
- Avoid technical jargon

## Example Release Notes

**Good:**
```
- New dark mode for easier nighttime reading
- Improved app startup speed by 50%
- Fixed crash when uploading large photos
- Updated design for better accessibility
```

**Avoid:**
```
- Refactored codebase architecture
- Updated dependencies to latest versions
- Various bug fixes and improvements
- Performance optimizations
```

## Supported Locales

Current locales: ${LOCALES}

To add a locale:
1. Create directory: `mkdir -p fastlane/metadata/android/LOCALE-CODE/changelogs`
2. Create file: `echo "Release notes" > fastlane/metadata/android/LOCALE-CODE/changelogs/default.txt`
3. Add translated release notes

## Common Locales

- en-US: English (United States)
- de-DE: German (Germany)
- es-ES: Spanish (Spain)
- fr-FR: French (France)
- it-IT: Italian (Italy)
- ja-JP: Japanese (Japan)
- ko-KR: Korean (Korea)
- pt-BR: Portuguese (Brazil)
- zh-CN: Chinese (Simplified)
- zh-TW: Chinese (Traditional)

## Automation with Fastlane

Release notes are automatically included by Fastlane during deployment:

```ruby
# In fastlane/Fastfile
lane :deploy_internal do
  # Fastlane automatically looks for changelogs in fastlane/metadata/android/{locale}/changelogs/
  upload_to_play_store(
    track: "internal",
    aab: "app/build/outputs/bundle/release/app-release.aab"
  )
end
```

Deployment command:
```bash
bundle exec fastlane deploy_internal
```

## Updating Release Notes

Before each release:
1. Update `default.txt` files for all locales
2. Keep under 500 characters
3. Verify UTF-8 encoding
4. Test locally: `wc -m fastlane/metadata/android/en-US/changelogs/default.txt`
```

### Step 4: Create Tracks Documentation

Create `docs/PLAY_STORE_TRACKS.md`:

```markdown
# Google Play Store Release Tracks

Complete guide to Play Store release tracks and workflow.

## Track Types

### 1. Internal Testing
**Audience:** Up to 100 testers (team only)
**Review:** None (instant, < 1 minute)
**Best for:** Daily builds, CI/CD, quick iterations
**Access:** Email-based tester list

**Use when:**
- Testing new features rapidly
- Verifying CI/CD pipeline
- Quick bug fix validation

### 2. Closed Testing (Beta)
**Audience:** Unlimited invited testers
**Review:** Typically < 1 day
**Best for:** Beta program, QA team, stakeholders
**Access:** Email list or shareable link

**Use when:**
- Extended testing with real users
- Collecting feedback before public release
- Testing with diverse devices/OS versions

### 3. Open Testing
**Audience:** Anyone with the link
**Review:** 1-7 days (first submission)
**Best for:** Public beta, community testing
**Access:** Public Play Store link

**Use when:**
- Large-scale public beta
- Community-driven feature testing
- Stress testing infrastructure

### 4. Production
**Audience:** All users (or staged rollout)
**Review:** 1-7 days (first submission, then hours)
**Best for:** Official releases
**Rollout:** Staged (5% → 10% → 50% → 100%)

**Use when:**
- Ready for public release
- All testing complete
- Version approved for general availability

## Recommended Workflow

```
Development
    ↓
Push to main → Internal Testing (auto)
    ↓
Test & validate
    ↓
Deploy to Beta → Closed Testing (manual)
    ↓
Beta feedback (1-2 weeks)
    ↓
Tag release → Production (manual approval)
    ↓
Staged Rollout:
  Day 1: 5%  → Monitor crash-free rate
  Day 2: 20% → Monitor ANR rate
  Day 3: 50% → Monitor user feedback
  Day 5: 100% → Complete rollout
```

## Promotion Between Tracks

**Internal → Closed:**
- Manual promotion in Play Console
- Or automated via GitHub Actions workflow

**Closed → Production:**
- Always requires manual approval
- Create GitHub release tag
- Triggers production deployment workflow

**Emergency Halt:**
If issues detected:
1. Run manage-rollout workflow with "halt" action
2. Fix issue
3. Deploy new version
4. Resume or start new rollout

## Best Practices

1. **Always test in Internal first**
   - Never skip to production
   - Catch obvious issues early

2. **Use Closed Testing for Beta**
   - Get real user feedback
   - Test on diverse devices
   - Minimum 1 week beta period

3. **Staged Production Rollouts**
   - Start at 5-10%
   - Monitor for 24-48 hours
   - Only increase if crash-free rate > 99%

4. **Monitor Key Metrics**
   - Crash-free rate (target: > 99.5%)
   - ANR rate (target: < 0.5%)
   - User ratings
   - Install/uninstall rates

5. **Have Rollback Plan**
   - Keep previous version available
   - Can halt rollout anytime
   - Can decrease rollout percentage
```

## Verification

**MANDATORY:** Run these commands:

```bash
# Verify directory structure
test -d fastlane/metadata/android/en-US/changelogs && echo "✓ Release notes structure created"

# Verify default.txt files exist
ls fastlane/metadata/android/*/changelogs/default.txt && echo "✓ Release note files created"

# Verify documentation
test -f fastlane/metadata/android/README.md && echo "✓ README created"
test -f docs/PLAY_STORE_TRACKS.md && echo "✓ TRACKS guide created"

# Check character count (should be < 500)
wc -m fastlane/metadata/android/en-US/changelogs/default.txt
```

**Expected output:**
- ✓ Release notes structure created
- ✓ Release note files created
- ✓ README created
- ✓ TRACKS guide created
- Character count < 500

## Outputs

| Output | Location | Description |
|--------|----------|-------------|
| Release notes | fastlane/metadata/android/${LOCALE}/changelogs/ | Per-locale release notes |
| README | fastlane/metadata/android/README.md | Usage documentation |
| Tracks guide | docs/PLAY_STORE_TRACKS.md | Release workflow guide |

## Troubleshooting

### "Character limit exceeded"
**Cause:** default.txt file > 500 characters
**Fix:** Edit file to be more concise, focus on top 3-4 changes

### "Encoding issues"
**Cause:** Non-UTF-8 encoding
**Fix:** Save files as UTF-8: `iconv -f ISO-8859-1 -t UTF-8 default.txt`

## Completion Criteria

- [ ] `fastlane/metadata/android/` directory exists
- [ ] At least `en-US/changelogs/default.txt` file exists
- [ ] `fastlane/metadata/android/README.md` created
- [ ] `docs/PLAY_STORE_TRACKS.md` created
- [ ] All default.txt files are < 500 characters
