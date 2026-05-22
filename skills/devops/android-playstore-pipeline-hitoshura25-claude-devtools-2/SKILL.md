---
name: android-playstore-pipeline
description: Complete end-to-end Android Play Store deployment pipeline setup in one command
category: android
version: 1.0.0
---

# Android Play Store Pipeline

This skill orchestrates all five Android deployment skills to create a complete, production-ready Play Store deployment pipeline in one command.

## What This Does

This is the **"easy button"** for Android deployment. It runs all five prerequisite skills in the correct order and creates a complete CI/CD pipeline from scratch.

### Complete Pipeline Setup

1. **Release Build Configuration** (android-release-build-setup)
   - Generate production and local dev keystores
   - Configure ProGuard/R8 with safe defaults
   - Setup signing configuration
   - Update .gitignore for security

2. **E2E Testing Setup** (android-e2e-testing-setup)
   - Add Espresso dependencies
   - Create test directory structure
   - Generate sample tests (smoke, navigation, interaction)
   - Setup CI/CD test integration

3. **Release Validation** (android-release-validation)
   - Create validation workflows
   - Setup E2E testing on release builds
   - Configure quality gates
   - Generate validation reports

4. **Play Console Integration** (android-playstore-setup)
   - Guide service account creation
   - Enable Play Developer API
   - Setup release notes structure
   - Document GitHub Secrets

5. **CI/CD Deployment** (android-playstore-publishing)
   - Generate deployment workflows
   - Configure multi-track deployment
   - Setup staged rollouts
   - Create rollout management

## Prerequisites

**Absolutely Required:**
- Android project with Gradle wrapper
- Package name decided (e.g., com.example.app)
- Google Play Developer account ($25, one-time)
- Admin access to Google Play Console

**Nice to Have:**
- Git repository initialized
- GitHub repository (for CI/CD)
- Basic familiarity with Android development

**You DON'T Need:**
- Existing keystore (we'll create it)
- Existing tests (we'll generate samples)
- CI/CD experience (we'll set it up)
- Play Console experience (we'll guide you)

## Parameters

None required - this skill will ask for everything it needs through an interactive questionnaire.

## Interactive Questionnaire

The skill will ask strategic questions once, then execute all five skills with your answers:

### 1. Project Information
- "What is your Android project directory?" (default: current directory)
- "What is your app's package name?" (e.g., com.example.app)
- "What is your app name?" (for documentation)
- "What is your organization name?" (for keystore)

### 2. Keystore Configuration
- "Organization unit?" (e.g., Engineering)
- "City/Locality?" (e.g., San Francisco)
- "State/Province?" (e.g., California)
- "Country code?" (e.g., US)

### 3. Testing Configuration
- "What is your main activity class name?" (e.g., MainActivity)
- "Which locales for release notes?" (default: en-US)
- "Enable test orchestrator?" (recommended: yes)

### 4. Deployment Configuration
- "Which deployment tracks to enable?"
  - [ ] Internal (continuous deployment)
  - [ ] Beta (alpha/beta testing)
  - [ ] Production (staged rollout)
- "Enable manual approval for production?" (recommended: yes)

### 5. Play Console Setup
- "Do you have a Google Play Developer account?" (guide if no)
- "Is your app created in Play Console?" (guide if no)
- "Run Play Console setup now or later?" (can defer to manual)

## Step-by-Step Execution

### Phase 1: Information Gathering

Collect all information upfront so user doesn't need to answer questions five times:

```
=== Android Play Store Pipeline Setup ===

This will configure your complete Android deployment pipeline.
You'll be asked questions once, then everything will be set up automatically.

Time estimate: 15-20 minutes (mostly waiting for builds)

Press Enter to begin...
```

Run through questionnaire, validate answers, confirm before proceeding.

### Phase 2: Release Build Setup

Execute android-release-build-setup skill:

```
=== Step 1/5: Release Build Configuration ===

Setting up keystores and signing...
  ✓ Generated production keystore
  ✓ Generated local dev keystore
  ✓ Configured ProGuard/R8
  ✓ Updated build.gradle.kts
  ✓ Updated .gitignore
  ✓ Created keystore documentation

Keystores created:
  - keystores/production-release.jks (gitignored)
  - keystores/local-dev-release.jks (gitignored)
  - keystores/KEYSTORE_INFO.txt (gitignored, SAVE SECURELY!)

⏱ Time: 2 minutes
```

**Outputs:**
- Production keystore for CI/CD
- Local dev keystore for testing
- ProGuard configuration
- Signing configuration in build.gradle.kts
- Keystore info file with passwords

### Phase 3: E2E Testing Setup

Execute android-e2e-testing-setup skill:

```
=== Step 2/5: E2E Testing Setup ===

Setting up Espresso testing...
  ✓ Added Espresso dependencies
  ✓ Created test directory structure
  ✓ Generated BaseTest class
  ✓ Created smoke tests
  ✓ Created navigation tests
  ✓ Added test utilities
  ✓ Created GitHub Actions workflow

Tests created:
  - ExampleInstrumentedTest (smoke test)
  - MainActivityTest (navigation test)
  - TestUtils (custom matchers)
  - ScreenshotUtil (failure screenshots)

⏱ Time: 3 minutes
```

**Outputs:**
- Espresso dependencies
- Test directory structure
- Sample tests
- Test utilities
- CI/CD test workflow

### Phase 4: Release Validation

Execute android-release-validation skill:

```
=== Step 3/5: Release Validation Setup ===

Setting up release validation...
  ✓ Created validation script
  ✓ Created validation workflow
  ✓ Configured quality gates

Validation configured:
  - Build APK/AAB with ProGuard
  - Run E2E tests on release
  - Verify signing
  - Check ProGuard mapping
  - Analyze APK contents

⏱ Time: 2 minutes
```

**Outputs:**
- Validation bash script
- GitHub Actions validation workflow
- Quality gate configuration

### Phase 5: Play Console Setup

Execute android-playstore-setup skill:

```
=== Step 4/5: Play Console Integration ===

Setting up Play Console access...
  ✓ Created release notes structure
  ✓ Generated release notes templates
  ✓ Documented track types
  ✓ Created GitHub Secrets guide
  ✓ Generated validation script

Manual steps required:
  1. Create service account in Google Cloud
  2. Enable Play Developer API
  3. Link to Play Console
  4. Add SERVICE_ACCOUNT_JSON_PLAINTEXT to GitHub Secrets

See: distribution/PLAY_CONSOLE_SETUP.md for detailed guide

⏱ Time: 5 minutes (+ 10 minutes manual setup)
```

**Outputs:**
- Release notes directory structure
- Track configuration docs
- GitHub Secrets documentation
- Play Console setup guide
- API validation script

**Interactive Guide:**
Optionally walk through service account creation if user wants to do it now.

### Phase 6: CI/CD Deployment

Execute android-playstore-publishing skill:

```
=== Step 5/5: CI/CD Deployment Workflows ===

Creating deployment workflows...
  ✓ Created deploy-internal.yml
  ✓ Created deploy-beta.yml
  ✓ Created deploy-production.yml
  ✓ Created manage-rollout.yml
  ✓ Created workflow documentation
  ✓ Created version increment script

Workflows created:
  - Internal: Auto-deploy on push to main
  - Beta: Manual deploy to alpha/beta
  - Production: Staged rollout with approval
  - Rollout: Manage production rollout

⏱ Time: 3 minutes
```

**Outputs:**
- Four GitHub Actions workflows
- Workflow documentation
- Version management script

### Phase 7: Final Configuration

```
=== Finalizing Setup ===

Running final checks...
  ✓ All files created
  ✓ Project structure validated
  ✓ Git repository ready
  ✓ Documentation generated

Generating summary...
```

### Phase 8: Validate Complete Pipeline (MANDATORY)

**CRITICAL: This step is MANDATORY and must pass before completing the skill.**

Validate the entire pipeline end-to-end:

```bash
# 1. REQUIRED: Verify all 5 prerequisite skills completed their criteria

echo "Checking Skill 1: Release Build Setup"
./gradlew assembleRelease && echo "✓ Release build works" || echo "✗ Skill 1 incomplete"

echo "Checking Skill 2: E2E Testing"
./gradlew connectedDebugAndroidTest && echo "✓ E2E tests work" || echo "✗ Skill 2 incomplete"

echo "Checking Skill 3: Release Validation"
./gradlew connectedReleaseAndroidTest && echo "✓ Release validation works" || echo "✗ Skill 3 incomplete"

echo "Checking Skill 4: Play Console Setup"
python3 scripts/validate-playstore.py <service-account.json> <package-name> && echo "✓ Play Console works" || echo "✗ Skill 4 incomplete"

echo "Checking Skill 5: Publishing Workflows"
yamllint .github/workflows/deploy-*.yml && echo "✓ Workflows valid" || echo "✗ Skill 5 incomplete"

# 2. REQUIRED: Verify all required files exist
[ -f "keystores/KEYSTORE_INFO.txt" ] || echo "✗ Missing keystore info"
[ -d "app/src/androidTest" ] || echo "✗ Missing tests"
[ -f ".github/workflows/deploy-internal.yml" ] || echo "✗ Missing workflows"
[ -f "distribution/GITHUB_SECRETS.md" ] || echo "✗ Missing secrets doc"

# 3. REQUIRED: Check .gitignore includes keystores
grep -q "keystores/" .gitignore && echo "✓ Keystores gitignored" || echo "✗ Keystores not in .gitignore"

# 4. REQUIRED: Verify documentation exists
[ -f "distribution/PLAY_CONSOLE_SETUP.md" ] || echo "⚠ Play Console setup guide missing"
[ -f ".github/workflows/README.md" ] || echo "✗ Workflow README missing"
```

**Expected output:**
- All 5 skills verified: ✓ Each skill's completion criteria met
- All files exist: ✓ No missing files
- .gitignore configured: ✓ Keystores excluded
- Documentation complete: ✓ All guides present

**If ANY fail:**
1. DO NOT complete pipeline skill
2. Go back to the failing skill
3. Complete that skill's criteria
4. Re-run pipeline validation
5. Only complete when ALL pass

**This is the orchestration skill - it MUST verify all prerequisites.**

### Phase 9: Comprehensive Summary

```
╔════════════════════════════════════════════════════════════════╗
║  🎉 Android Play Store Pipeline Setup Complete! 🎉           ║
╚════════════════════════════════════════════════════════════════╝

⏱  Total Time: ~15 minutes

📦 What Was Created:

  Release Build Configuration:
    ✓ Production keystore (CI/CD)
    ✓ Local dev keystore (testing)
    ✓ ProGuard/R8 configuration
    ✓ Signing setup in build.gradle.kts

  E2E Testing:
    ✓ Espresso dependencies
    ✓ 3 sample test classes
    ✓ Test utilities and helpers
    ✓ CI/CD test workflow

  Release Validation:
    ✓ Validation script
    ✓ Quality gate workflow
    ✓ E2E tests on release builds

  Play Console:
    ✓ Release notes structure
    ✓ Track documentation
    ✓ GitHub Secrets guide
    ✓ Setup instructions

  CI/CD Deployment:
    ✓ 4 deployment workflows
    ✓ Rollout management
    ✓ Version scripts

📋 Next Steps (in order):

  ⚠️  CRITICAL - Secure Your Keystores:
    1. Open: keystores/KEYSTORE_INFO.txt
    2. Copy passwords to password manager
    3. Store file in secure location (NOT git!)
    4. Back up keystores to secure location
    5. NEVER commit keystores to git

  🔐 Setup GitHub Secrets:
    1. Go to: Repository → Settings → Secrets → Actions
    2. Add SERVICE_ACCOUNT_JSON_PLAINTEXT (see guide below)
    3. Add signing secrets:
       - SIGNING_KEY_STORE_BASE64
       - SIGNING_KEY_ALIAS
       - SIGNING_STORE_PASSWORD
       - SIGNING_KEY_PASSWORD
    
    See: distribution/GITHUB_SECRETS.md for detailed instructions

  🎮 Setup Play Console (10-15 minutes):
    1. Create service account in Google Cloud
    2. Enable Play Developer API
    3. Link to Play Console
    4. Grant permissions
    5. Download JSON key
    
    See: distribution/PLAY_CONSOLE_SETUP.md for step-by-step guide

  🏗️  Setup GitHub Environment:
    1. Go to: Repository → Settings → Environments
    2. Create "production" environment
    3. Add required reviewers
    4. Save protection rules

  ✅ Test the Pipeline:
    1. Update release notes: fastlane/metadata/android/en-US/changelogs/default.txt
    2. Commit and push to main:
       git add .
       git commit -m "Add Play Store deployment pipeline"
       git push origin main
    3. Watch GitHub Actions deploy to internal track
    4. Test on device via Play Console internal testing link

  🚀 First Production Release:
    1. Test thoroughly in internal track
    2. Deploy to beta: Actions → Deploy to Beta
    3. Collect feedback from beta testers
    4. Tag for production:
       git tag v1.0.0
       git push origin v1.0.0
    5. Approve in GitHub Actions
    6. Monitor staged rollout

📂 Files Created:

  Keystores (SECURE THESE!):
    • keystores/production-release.jks
    • keystores/local-dev-release.jks
    • keystores/KEYSTORE_INFO.txt

  Build Configuration:
    • app/build.gradle.kts (updated)
    • app/proguard-rules.pro
    • gradle.properties.template

  Tests:
    • app/src/androidTest/.../ExampleInstrumentedTest.kt
    • app/src/androidTest/.../base/BaseTest.kt
    • app/src/androidTest/.../screens/MainActivityTest.kt
    • app/src/androidTest/.../utils/TestUtils.kt
    • app/src/androidTest/.../utils/ScreenshotUtil.kt

  Release Notes:
    • fastlane/metadata/android/en-US/changelogs/default.txt
    • fastlane/metadata/android/README.md
    • docs/PLAY_STORE_TRACKS.md

  Documentation:
    • PLAY_CONSOLE_SETUP.md (project root)
    • GITHUB_SECRETS.md (if needed)
    • .github/workflows/README.md

  Workflows:
    • .github/workflows/deploy-internal.yml
    • .github/workflows/deploy-beta.yml
    • .github/workflows/deploy-production.yml
    • .github/workflows/manage-rollout.yml
    • .github/workflows/android-test.yml
    • .github/workflows/release-validation.yml

  Scripts:
    • scripts/validate-playstore.py
    • scripts/increment-version.sh
    • scripts/validate-release.sh

🔗 Important Links:

  📖 Documentation:
    - Play Console Setup: distribution/PLAY_CONSOLE_SETUP.md
    - GitHub Secrets: distribution/GITHUB_SECRETS.md
    - Workflow Usage: .github/workflows/README.md
    - Release Tracks: distribution/TRACKS.md

  🌐 External Resources:
    - Play Console: https://play.google.com/console/
    - Google Cloud: https://console.cloud.google.com/
    - GitHub Actions: https://github.com/{org}/{repo}/actions

⚠️  Important Reminders:

  Security:
    ⚠️  NEVER commit keystores to git
    ⚠️  Store keystore passwords securely
    ⚠️  Rotate service account keys annually
    ⚠️  Review Play Console audit logs

  First Upload:
    ⚠️  First Play Store upload MUST be manual
    ⚠️  Create app in Play Console first
    ⚠️  Upload one APK/AAB manually
    ⚠️  Then automated uploads will work

  Version Management:
    ⚠️  Version code must increase each upload
    ⚠️  Use scripts/increment-version.sh
    ⚠️  Keep mapping files for each release

  Monitoring:
    ⚠️  Monitor crash-free rate (target: >99%)
    ⚠️  Use staged rollouts (start 5-10%)
    ⚠️  Review user feedback actively
    ⚠️  Be ready to halt rollout if needed

📊 Pipeline Overview:

  Development → Push to main
                    ↓
            Internal Testing (automatic)
                    ↓
          Test on device, fix bugs
                    ↓
     Manual: Deploy to Beta Track
                    ↓
       Beta Testing (1-2 weeks)
                    ↓
         Collect feedback, fix
                    ↓
        Tag version: v1.0.0
                    ↓
    Production Deployment (requires approval)
                    ↓
       5% Rollout (monitor 24-48h)
                    ↓
      Increase to 20% (if stable)
                    ↓
      Increase to 50% (if stable)
                    ↓
       Complete to 100%

🎓 Learning Resources:

  If you're new to any of these concepts:
    - ProGuard/R8: See app/proguard-rules.pro comments
    - Espresso Testing: See app/src/androidTest/README.md
    - GitHub Actions: See .github/workflows/README.md
    - Play Console: See distribution/PLAY_CONSOLE_SETUP.md
    - Staged Rollouts: See distribution/TRACKS.md

💬 Need Help?

  Common issues and solutions:
    - "Build fails": Check signing secrets are correct
    - "Tests fail": Review test logs in GitHub Actions
    - "Upload fails": Verify service account permissions
    - "Version error": Run scripts/increment-version.sh

  Resources:
    - GitHub Actions logs (detailed error messages)
    - Play Console support (console help)
    - Documentation in this repository

╔════════════════════════════════════════════════════════════════╗
║  Your Android deployment pipeline is ready! 🚀                ║
║                                                                 ║
║  Start with the "Next Steps" section above.                   ║
║  Questions? Check the documentation files created.             ║
╚════════════════════════════════════════════════════════════════╝
```

## Error Handling

### Prerequisites Not Met

**No Android project found:**
```
❌ Error: Not an Android project

This directory doesn't appear to be an Android project.
Expected: app/build.gradle.kts or app/build.gradle

Solution: Run this skill from your Android project root directory.
```

**No package name in build.gradle:**
```
❌ Error: Cannot determine package name

Could not find package name in app/build.gradle.kts

Solution: Add namespace or applicationId to your build file:
  android {
      namespace = "com.example.app"
  }
```

**Git not initialized:**
```
⚠️  Warning: Git repository not initialized

This is not a git repository. The pipeline works best with git.

Continue anyway? (y/n)
```

### Skill Execution Failures

**Skill 1 fails (keystore generation):**
```
❌ Error in Step 1/5: Release Build Setup

Failed to generate keystore.

Possible causes:
  - keytool not found (JDK not installed)
  - Insufficient permissions
  - Directory doesn't exist

Fix: Install JDK 17 and try again
```

**Skill 2 fails (test setup):**
```
❌ Error in Step 2/5: E2E Testing Setup

Failed to add Espresso dependencies.

Possible causes:
  - build.gradle.kts has syntax errors
  - File is read-only

Fix: Check build.gradle.kts is valid and writable
```

**Recovery:**
- Pipeline stops at failed step
- Shows detailed error message
- User can fix issue and re-run
- Already completed steps are preserved (unless --clean flag used)

### User Cancellation

```
Pipeline setup cancelled by user.

Completed steps:
  ✓ Step 1/5: Release Build Setup
  ✓ Step 2/5: E2E Testing Setup
  ✗ Step 3/5: Cancelled

To resume:
  Run the skill again - completed steps will be detected
  Or run individual skills:
    - android-release-validation
    - android-playstore-setup
    - android-playstore-publishing
```

## Advanced Options

### Selective Execution

**Skip completed steps:**
```
--resume    Resume from last failed step
--skip=1,2  Skip steps 1 and 2 (already done)
```

**Clean slate:**
```
--clean     Remove all generated files and start fresh
```

**Dry run:**
```
--dry-run   Show what would be done without making changes
```

### Configuration File

**Save configuration for re-use:**

`.android-pipeline.yml`:
```yaml
project:
  package_name: com.example.app
  app_name: MyApp
  main_activity: MainActivity

organization:
  name: Example Corp
  unit: Engineering
  city: San Francisco
  state: California
  country: US

testing:
  locales:
    - en-US
    - de-DE
    - es-ES
  test_orchestrator: true

deployment:
  tracks:
    internal: true
    beta: true
    production: true
  production_approval: true
```

**Use saved config:**
```
--config=.android-pipeline.yml
```

## Integration Test

After pipeline setup, run integration test:

```bash
# Integration test script
./scripts/test-pipeline.sh

# Tests:
# 1. Build debug APK (should succeed)
# 2. Run unit tests (should pass)
# 3. Build release APK (should succeed with ProGuard)
# 4. Verify ProGuard mapping exists
# 5. Check signing configuration
# 6. Verify GitHub Actions workflows syntax
# 7. Validate release notes format
```

## Files Created/Modified

**Created:**
All files from Skills 1-5 plus:
- `.android-pipeline.yml` - Configuration (optional)
- `PIPELINE_SETUP.md` - This complete guide
- `scripts/test-pipeline.sh` - Integration test

**Modified:**
- `.gitignore` - Add keystore patterns
- `app/build.gradle.kts` - Signing, ProGuard, test dependencies
- `README.md` - Add deployment instructions (optional)

## Completion Criteria (ALL MUST PASS)

Do NOT mark this skill as complete unless ALL of the following are verified:

✅ **All 5 prerequisite skills completed**
  - [ ] Skill 1 (android-release-build-setup) completion criteria met
  - [ ] Skill 2 (android-e2e-testing-setup) completion criteria met
  - [ ] Skill 3 (android-release-validation) completion criteria met
  - [ ] Skill 4 (android-playstore-setup) completion criteria met
  - [ ] Skill 5 (android-playstore-publishing) completion criteria met

✅ **MANDATORY: End-to-end validation**
  - [ ] `./gradlew assembleRelease` succeeds
  - [ ] `./gradlew connectedDebugAndroidTest` succeeds
  - [ ] `./gradlew connectedReleaseAndroidTest` succeeds
  - [ ] Play Console API connection validated
  - [ ] All workflow YAML files valid

✅ **Security checklist**
  - [ ] keystores/ in .gitignore
  - [ ] KEYSTORE_INFO.txt never committed
  - [ ] gradle.properties not committed (if contains secrets)
  - [ ] Service account JSON not committed

✅ **Documentation complete**
  - [ ] All prerequisite skills generated their documentation
  - [ ] Pipeline-level README or guide exists
  - [ ] Next steps clearly documented

**If ANY checkbox is unchecked, the skill is NOT complete.**

**SPECIAL NOTE:** This skill orchestrates all 5 others. If this skill's criteria pass, the user has a COMPLETE, production-ready Android Play Store deployment pipeline.

## Expected Outcomes

After running this skill successfully:

✅ **Complete deployment pipeline** ready to use
✅ **All 5 skills executed** in correct order
✅ **Security configured** properly (keystores, secrets)
✅ **Tests created** and ready to extend
✅ **CI/CD workflows** ready for GitHub Actions
✅ **Documentation** comprehensive and clear
✅ **Ready for first deployment** after manual setup steps

## Next Skills (Dependencies)

This skill DEPENDS on ALL FIVE prerequisite skills:
- `android-release-build-setup` - REQUIRED
- `android-e2e-testing-setup` - REQUIRED
- `android-release-validation` - REQUIRED
- `android-playstore-setup` - REQUIRED
- `android-playstore-publishing` - REQUIRED

This is the ORCHESTRATION skill. It runs all 5 in sequence and validates the complete pipeline.

Do NOT run this skill unless you want to set up the ENTIRE pipeline from scratch.
If you only need part of the pipeline, run individual skills instead.

This skill has NO downstream dependencies - it's the final step in the complete setup.

## Security Checklist

Before first deployment:

- [ ] Keystore passwords stored in password manager
- [ ] Keystores backed up to secure location
- [ ] .gitignore includes keystore patterns
- [ ] GitHub Secrets added (all 5 required)
- [ ] Service account JSON stored securely (NOT in git)
- [ ] Production environment created with approvers
- [ ] Reviewed all generated files for sensitive data

## Troubleshooting

### "Pipeline setup incomplete"
→ Check error messages for which step failed
→ Fix the issue and re-run with --resume

### "Keystores not secure"
→ Verify .gitignore includes keystore patterns
→ Check keystores/ directory not in git

### "GitHub Actions syntax error"
→ Validate YAML syntax online
→ Check package name replaced correctly

### "First upload fails"
→ Must upload APK/AAB manually to Play Console first
→ Create app in Play Console before automated uploads

## Best Practices

1. **Run in clean project** first time
2. **Save configuration** for future use
3. **Test locally** before pushing to GitHub
4. **Read documentation** generated
5. **Follow security checklist** completely

## References

- Individual skills documentation in skills/ directory
- GitHub Actions: https://docs.github.com/en/actions
- Play Console: https://support.google.com/googleplay/android-developer
- ProGuard: https://www.guardsquare.com/manual/home
- Espresso: https://developer.android.com/training/testing/espresso
