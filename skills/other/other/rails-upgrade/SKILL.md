---
name: rails-upgrade
description: Analyzes Rails applications and generates comprehensive upgrade reports with breaking changes, deprecations, and step-by-step migration guides for Rails 2.3 through 8.1. Use when upgrading Rails applications, planning multi-hop upgrades, or querying version-specific changes. Based on FastRuby.io methodology and "The Complete Guide to Upgrade Rails" ebook.
---

# Rails Upgrade Assistant Skill

## Skill Identity
- **Name:** Rails Upgrade Assistant
- **Purpose:** Intelligent Rails application upgrades from 2.3 through 8.1
- **Skill Type:** Modular with external workflows and examples
- **Upgrade Strategy:** Sequential only (no version skipping)
- **Methodology:** Based on FastRuby.io upgrade best practices and "The Complete Guide to Upgrade Rails" ebook
- **Attribution:** Content based on "The Complete Guide to Upgrade Rails" by FastRuby.io (OmbuLabs)

---

## Dependencies

- **dual-boot skill** ([github.com/ombulabs/claude-code_dual-boot-skill](https://github.com/ombulabs/claude-code_dual-boot-skill)) — Sets up and manages dual-boot environments using the `next_rails` gem. Covers setup, `NextRails.next?` code patterns, CI configuration, and post-upgrade cleanup. Must be installed for Step 2 of the upgrade workflow.
- **rails-load-defaults skill** ([github.com/ombulabs/claude-code_rails-load-defaults-skill](https://github.com/ombulabs/claude-code_rails-load-defaults-skill)) — Handles incremental `load_defaults` updates with tiered risk assessment (Tier 1: low-risk, Tier 2: needs codebase grep, Tier 3: requires human review). Used as the final step after the Rails version upgrade is complete.

---

## Core Methodology (FastRuby.io Approach)

This skill follows the proven FastRuby.io upgrade methodology:

1. **Incremental Upgrades** - Always upgrade one minor/major version at a time
2. **Assessment First** - Understand scope before making changes
3. **Dual-Boot Testing** - Test both versions during transition using `next_rails` gem
4. **Test Coverage** - Ensure adequate test coverage before upgrading (aim for 80%+)
5. **Gem Compatibility** - Check gem compatibility at each step using RailsBump
6. **Deprecation Warnings** - Address deprecations before upgrading
7. **Backwards Compatible Changes** - Deploy small changes to production before version bump

**Key Resources:**
- **DELEGATE** to the `dual-boot` skill for dual-boot setup with `next_rails` (see Dependencies)
- See `references/deprecation-warnings.md` for managing deprecations
- See `references/staying-current.md` for maintaining upgrades over time

---

## CRITICAL: Dual-Boot Code Pattern with `NextRails.next?`

When proposing code fixes that must work with both the current and target Rails versions (dual-boot), **always use `NextRails.next?` from the `next_rails` gem** — never use `respond_to?` or other feature-detection patterns.

**DELEGATE** to the `dual-boot` skill for:
- Setup and initialization (`next_rails --init`, `Gemfile.next`)
- `NextRails.next?` code patterns and examples
- CI configuration for dual-boot testing
- Post-upgrade cleanup (removing dual-boot branches)

**DEPENDENCY:** Requires the [dual-boot skill](https://github.com/ombulabs/claude-code_dual-boot-skill)

---

## Trigger Patterns

Claude should activate this skill when user says:

**Upgrade Requests:**
- "Upgrade my Rails app to [version]"
- "Help me upgrade from Rails [x] to [y]"
- "What breaking changes are in Rails [version]?"
- "Plan my upgrade from [x] to [y]"
- "What Rails version am I using?"
- "Analyze my Rails app for upgrade"
- "Find breaking changes in my code"
- "Check my app for Rails [version] compatibility"

**Specific Report Requests:**
- "Show me the app:update changes"
- "Preview configuration changes for Rails [version]"
- "Generate the upgrade report"
- "What will change if I upgrade?"

**Upgrade Cleanup Requests (delegate to the `upgrade-cleanup` plugin):**
- "Finish the upgrade"
- "Clean up after my Rails upgrade"
- "Remove the dual-boot setup"
- "Drop the NextRails branches"
- "We're done upgrading to Rails [version]"

---

## CRITICAL: Sequential Upgrade Strategy

### ⚠️ Version Skipping is NOT Allowed

Rails upgrades MUST follow a sequential path. Examples:

**For Rails 5.x to 8.x:**
```
5.0.x → 5.1.x → 5.2.x → 6.0.x → 6.1.x → 7.0.x → 7.1.x → 7.2.x → 8.0.x → 8.1.x
```

**You CANNOT skip versions.** Examples:
- ❌ 5.2 → 6.1 (skips 6.0)
- ❌ 6.0 → 7.0 (skips 6.1)
- ❌ 7.0 → 8.0 (skips 7.1 and 7.2)
- ✅ 5.2 → 6.0 (correct)
- ✅ 7.0 → 7.1 (correct)
- ✅ 7.2 → 8.0 (correct)

If user requests a multi-hop upgrade (e.g., 5.2 → 8.1):
1. Explain the sequential requirement
2. Break it into individual hops
3. Generate separate reports for each hop
4. Recommend completing each hop fully before moving to next

---

## Supported Upgrade Paths

### Legacy Rails (2.3 - 4.2)

| From | To | Difficulty | Key Changes | Ruby Required |
|------|-----|-----------|-------------|---------------|
| 2.3.x | 3.0.x | Very Hard | XSS protection, routes syntax | 1.8.7 - 1.9.3 |
| 3.0.x | 3.1.x | Medium | Asset pipeline, jQuery | 1.8.7 - 1.9.3 |
| 3.1.x | 3.2.x | Easy | Ruby 1.9.3 support | 1.8.7 - 2.0 |
| 3.2.x | 4.0.x | Hard | Strong Parameters, Turbolinks | 1.9.3+ |
| 4.0.x | 4.1.x | Medium | Spring, secrets.yml | 1.9.3+ |
| 4.1.x | 4.2.x | Medium | ActiveJob, Web Console | 1.9.3+ |
| 4.2.x | 5.0.x | Hard | ActionCable, API mode, ApplicationRecord | 2.2.2+ |

### Modern Rails (5.0 - 8.1)

| From | To | Difficulty | Key Changes | Ruby Required |
|------|-----|-----------|-------------|---------------|
| 5.0.x | 5.1.x | Easy | Encrypted secrets, yarn default | 2.2.2+ |
| 5.1.x | 5.2.x | Medium | Active Storage, credentials | 2.2.2+ |
| 5.2.x | 6.0.x | Hard | Zeitwerk, Action Mailbox/Text | 2.5.0+ |
| 6.0.x | 6.1.x | Medium | Horizontal sharding, strict loading | 2.5.0+ |
| 6.1.x | 7.0.x | Hard | Hotwire/Turbo, Import Maps | 2.7.0+ |
| 7.0.x | 7.1.x | Medium | Composite keys, async queries | 2.7.0+ |
| 7.1.x | 7.2.x | Medium | Transaction-aware jobs, DevContainers | 3.1.0+ |
| 7.2.x | 8.0.x | Very Hard | Propshaft, Solid gems, Kamal | 3.2.0+ |
| 8.0.x | 8.1.x | Easy | Bundler-audit, max_connections | 3.2.0+ |

---

## Available Resources

### Core Documentation
- `SKILL.md` - This file (entry point)

### Version-Specific Guides (Load as needed)

**Legacy Rails:**
- `version-guides/upgrade-3.2-to-4.0.md` - Rails 3.2 → 4.0 (Strong Parameters)
- `version-guides/upgrade-4.0-to-4.1.md` - Rails 4.0 → 4.1 (Spring, secrets.yml, enums)
- `version-guides/upgrade-4.1-to-4.2.md` - Rails 4.1 → 4.2 (ActiveJob, Web Console)
- `version-guides/upgrade-4.2-to-5.0.md` - Rails 4.2 → 5.0 (ApplicationRecord)

**Modern Rails:**
- `version-guides/upgrade-5.0-to-5.1.md` - Rails 5.0 → 5.1 (Encrypted secrets)
- `version-guides/upgrade-5.1-to-5.2.md` - Rails 5.1 → 5.2 (Active Storage, Credentials)
- `version-guides/upgrade-5.2-to-6.0.md` - Rails 5.2 → 6.0 (Zeitwerk)
- `version-guides/upgrade-6.0-to-6.1.md` - Rails 6.0 → 6.1 (Horizontal sharding)
- `version-guides/upgrade-6.1-to-7.0.md` - Rails 6.1 → 7.0 (Hotwire/Turbo)
- `version-guides/upgrade-7.0-to-7.1.md` - Rails 7.0 → 7.1 (Composite keys)
- `version-guides/upgrade-7.1-to-7.2.md` - Rails 7.1 → 7.2 (Transaction jobs)
- `version-guides/upgrade-7.2-to-8.0.md` - Rails 7.2 → 8.0 (Propshaft)
- `version-guides/upgrade-8.0-to-8.1.md` - Rails 8.0 → 8.1 (bundler-audit)

### Workflow Guides (Load when generating deliverables)
- `workflows/test-suite-verification-workflow.md` - **MANDATORY FIRST STEP** - How to run and verify test suite
- `workflows/direct-detection-workflow.md` - How to run breaking change detection directly
- `workflows/upgrade-report-workflow.md` - How to generate upgrade reports
- `workflows/gem-compatibility-workflow.md` - **Load in Step 4.5** - Per-lockfile gem compatibility check against the target Rails version. Documents both the primary (`next_rails` `bundle_report compatibility`) and the secondary (railsbump.org API) and the rules for when to escalate.
- `workflows/ci-sync-workflow.md` - **MANDATORY before opening the upgrade PR** - How to verify CI config matches the upgraded Gemfile
- `workflows/app-update-preview-workflow.md` - How to generate app:update previews
- **`upgrade-cleanup` companion plugin** - User-triggered. Removes dual-boot scaffolding and drops `NextRails.next?` / `NextRails.current?` branches. Deprecation triage stays with this skill for the next hop.

### Examples (Load when user needs clarification)
- `examples/simple-upgrade.md` - Single-hop upgrade example
- `examples/multi-hop-upgrade.md` - Multi-hop upgrade example

### External Dependencies
- **dual-boot skill** - Dual-boot setup and management with next_rails (Step 2) (https://github.com/ombulabs/claude-code_dual-boot-skill)
- **rails-load-defaults skill** - Incremental load_defaults alignment (Step 7, final step) (https://github.com/ombulabs/claude-code_rails-load-defaults-skill)

### Reference Materials
- `references/deprecation-warnings.md` - Finding and fixing deprecations
- `references/staying-current.md` - Keeping up with Rails releases
- `references/breaking-changes-by-version.md` - Quick lookup
- `references/multi-hop-strategy.md` - Multi-version planning
- `references/testing-checklist.md` - Comprehensive testing
- `references/gem-compatibility.md` - Gem update order and the "no compatible version" playbook (fork / vendor / replace). Load only when Step 4.5's compatibility check produced blockers.

### Detection Pattern Resources
- `detection-scripts/patterns/rails-*.yml` - Version-specific patterns for direct detection

### Report Templates
- `templates/upgrade-report-template.md` - Main upgrade report structure
- `templates/app-update-preview-template.md` - Configuration preview

---

## High-Level Workflow

When user requests an upgrade, follow this workflow:

### Step 0: Verify Latest Patch Version (MANDATORY PRE-STEP)
```
⚠️  THIS STEP IS REQUIRED BEFORE ANY OTHER WORK

1. Read Gemfile.lock to find exact current Rails version (e.g., 3.2.19)
2. Compare against latest patch for that series:
   - EOL series (≤ 7.1): use static table in references/multi-hop-strategy.md
   - Active series (≥ 7.2): query RubyGems API (see references/multi-hop-strategy.md for commands)
3. If current version < latest patch:
   - INFORM user: "Your app is on Rails X.Y.Z but the latest patch is X.Y.W"
   - Guide through Gemfile update and bundle update rails
   - Run test suite after patch upgrade
   - Deploy patch upgrade before proceeding
   - Do NOT proceed to next minor/major until on latest patch
4. If current version == latest patch:
   - Proceed to Step 1
```

**Why patch first:** Patch releases contain security fixes, bug fixes, and additional deprecation warnings. Starting the version hop on the latest patch is safer (the security fixes are already in production) and easier to debug (the new deprecation warnings surface issues that would otherwise show up mid-upgrade).

### Step 1: Run Test Suite (MANDATORY FIRST STEP)
```
⚠️  THIS STEP IS REQUIRED BEFORE ANY OTHER WORK

1. Read: workflows/test-suite-verification-workflow.md
2. Detect test framework (RSpec, Minitest, or both)
3. Run test suite with: bundle exec rspec OR bundle exec rails test
4. Capture results: total tests, passing, failing, pending
5. If ANY tests fail:
   - STOP the upgrade process
   - Report failing tests to user
   - Offer to help fix failing tests
   - Do NOT proceed until all tests pass
6. If all tests pass:
   - Record baseline metrics (test count, coverage if available)
   - Proceed to Step 2
```

### Step 2: Set Up Dual-Boot with next_rails (EARLY SETUP)
```
DELEGATE to the dual-boot skill for setup and initialization.
That skill handles:
- Checking if Gemfile.next already exists (to avoid duplicate `next?` method)
- Adding next_rails gem and running next_rails --init
- Installing dependencies for both Rails versions
- Configuring the Gemfile with `if next?` conditionals
```

### Step 3: Validate Upgrade Path
```
1. Check if upgrade is single-hop or multi-hop
2. If multi-hop, explain sequential requirement
3. Plan individual hops
```

### Step 4: Run Breaking Changes Detection (DIRECT)
```
Claude runs detection directly using tools - NO script generation needed

1. Read: workflows/direct-detection-workflow.md
2. Read: detection-scripts/patterns/rails-{VERSION}-patterns.yml
3. For each pattern in the patterns file:
   - Use Grep tool to search for the pattern
   - Collect file paths and line numbers
   - Store findings with context
4. Read: version-guides/upgrade-{FROM}-to-{TO}.md for context
5. Compile all findings into structured data
```

### Step 4.5: Check Gem Compatibility Against Target Rails
```
Determines which gems must be bumped before the Rails version change can resolve.

1. Read: workflows/gem-compatibility-workflow.md and follow it. The
   workflow documents the primary check (next_rails bundle_report),
   the conditions for escalating to the secondary (railsbump API),
   and the bucket mapping for both.
2. Pass the resulting three buckets — required bumps, blockers,
   already compatible — into Step 5's report so the gem-update
   section reflects real per-lockfile data.
3. If any blockers exist, load references/gem-compatibility.md for
   the fork/replace/vendor playbook and the gem update order. Skip
   otherwise.
```

### Step 5: Load Report Resources & Generate Reports
```
1. Read: templates/upgrade-report-template.md
2. Read: templates/app-update-preview-template.md
3. Read: workflows/upgrade-report-workflow.md
4. Read: workflows/app-update-preview-workflow.md
```

**Deliverable #1: Comprehensive Upgrade Report**
- **Input:** Direct detection findings + version guide data
- **Output:** A report covering breaking changes (with OLD vs NEW code examples taken from the user's actual files), custom-code warnings flagged with ⚠️, a step-by-step migration plan, a testing checklist, and a rollback plan.

**Deliverable #2: app:update Preview**
- **Input:** Actual config files + findings
- **Output:** A preview showing exact configuration file changes (OLD vs NEW), a list of new files that will be created, and a per-file impact assessment (HIGH / MEDIUM / LOW).

### Step 6: Present Reports & Implement Changes
```
1. Present Comprehensive Upgrade Report first
2. Present app:update Preview Report second
3. Implement breaking change fixes using `NextRails.next?` for dual-boot code
4. Update Gemfile to target Rails version
5. Run test suite against both versions
6. **Check CI config matches the upgraded Gemfile** — load `workflows/ci-sync-workflow.md`, fix any mismatches before proceeding
7. Deploy and verify
```

**Do not fix deprecations printed by the next version during this hop.** Those belong to the *next* upgrade cycle and will be addressed before the next version bump. Triaging them now expands the scope of the current hop and risks shipping a half-finished change.

### Step 7: Align load_defaults
```
⚠️  THIS STEP HAPPENS AFTER THE UPGRADE IS COMPLETE

1. DELEGATE to the rails-load-defaults skill
2. That skill walks through each config change one at a time, grouped by risk tier
3. Tests are re-run between each change
4. Consolidates into config/application.rb when done
```

### Step 8: Mention Cleanup (USER-TRIGGERED)
```
⚠️  DO NOT AUTO-RUN. Mention it; let the user decide.

1. Tell the user the cleanup option exists
2. Delegate to the upgrade-cleanup plugin only when the user explicitly asks
   ("finish the upgrade", "clean up dual-boot", "drop the NextRails branches")
3. The cleanup plugin removes NextRails.next? / NextRails.current? branches
   and retires dual-boot scaffolding. Deprecation triage stays with this
   skill for the next hop, not with cleanup.
```

**Sample wording the agent can crib from when prompting the user:**

> Rails X.Y is in. When you're ready to remove dual-boot scaffolding (drop `NextRails.next?` / `NextRails.current?` branches, retire `Gemfile.next`), ask me to clean up. If you're heading straight to the next hop, keeping dual-boot in place is also fine.

---

## Pre-Upgrade Checklist (FastRuby.io Best Practices)

Before starting ANY upgrade:

### 1. Test Coverage Assessment (AUTOMATED - Step 1 of Workflow)
- [x] Run test suite - all tests passing? **← Claude runs this automatically**
- [x] Check test coverage (aim for >70%) **← Claude captures this if SimpleCov is configured**
- [ ] Review critical paths have coverage

**Note:** This step is now automated. Claude will run the test suite and BLOCK the upgrade if any tests fail.

### 2. Dependency Audit
- [ ] Run `bundle outdated`
- [ ] Check gem compatibility with target Rails version
- [ ] Identify gems that need upgrading first

### 3. Database Backup
- [ ] Backup production database
- [ ] Backup development/staging databases
- [ ] Verify backup restore process works

### 4. Git Branch Strategy
- [ ] Create upgrade branch from main/master
- [ ] Set up CI for upgrade branch
- [ ] Plan merge strategy

### 5. Deprecation Warnings
- [ ] Run app with Rails deprecations turned on (configured in config/environment files)
- [ ] Address existing deprecation warnings
- [ ] Enable verbose deprecations in test environment

---

## Common Request Patterns

### Pattern 1: Full Upgrade Request
**User says:** "Upgrade my Rails app to 8.1"

**Action - Step 0 (MANDATORY: Verify Latest Patch):**
1. Read `Gemfile.lock` for exact Rails version
2. Compare against latest patch for that series (see `references/multi-hop-strategy.md`)
3. If not on latest patch → Guide user through patch upgrade first
4. If on latest patch → Proceed to Step 1

**Action - Step 1 (MANDATORY: Verify Tests Pass):**
1. Load: `workflows/test-suite-verification-workflow.md`
2. Detect test framework (RSpec or Minitest)
3. Run test suite: `bundle exec rspec` or `bundle exec rails test`
4. If tests FAIL → STOP and help fix tests first
5. If tests PASS → Record baseline and proceed

**Action - Step 2 (Set Up Dual-Boot):**
1. DELEGATE to the `dual-boot` skill for setup
2. Set up next_rails, Gemfile.next, and dual-boot CI

**Action - Step 3 (Validate Upgrade Path):**
1. Validate upgrade path (single-hop vs multi-hop)

**Action - Step 4 (Run Detection Directly):**
1. Load: `workflows/direct-detection-workflow.md`
2. Load: `detection-scripts/patterns/rails-{VERSION}-patterns.yml`
3. Use Grep/Glob/Read tools to search for each pattern
4. Collect findings with file:line references

**Action - Step 5 (Generate Reports):**
1. Load: `workflows/upgrade-report-workflow.md`
2. Load: `workflows/app-update-preview-workflow.md`
3. Generate Comprehensive Upgrade Report (using direct findings)
4. Generate app:update Preview (using actual config files)
5. Present both reports to user

**Action - Step 6 (Implement & Upgrade):**
1. Fix breaking changes using `NextRails.next?` for dual-boot code
2. Update Gemfile to target Rails version
3. Run tests against both versions
4. **Check CI config matches the upgraded Gemfile** (`workflows/ci-sync-workflow.md`) — fix any mismatches before declaring Step 6 complete
5. Deploy and verify

**Action - Step 7 (Align load_defaults - FINAL):**
1. DELEGATE to the `rails-load-defaults` skill
2. Walk through each config incrementally after the upgrade is complete

### Pattern 2: Multi-Hop Request
**User says:** "Help me upgrade from Rails 5.2 to 8.1"

**Action - Step 0 (MANDATORY: Verify Latest Patch):**
1. Check exact current version from `Gemfile.lock`
2. If not on latest patch of current series → Upgrade to latest patch first
3. For multi-hop: This check applies at the START and again after each hop

**Action - Step 1 (MANDATORY: Verify Tests Pass):**
1. Run test suite BEFORE planning any upgrade work
2. If tests fail → STOP and fix first
3. If tests pass → Proceed with planning

**Action - Step 2 (Set Up Dual-Boot):**
1. DELEGATE to the `dual-boot` skill for setup (if not already set up)
2. Dual-boot stays active throughout the multi-hop process

**Action - Step 3 (Plan & Execute):**
1. Explain sequential requirement
2. Calculate hops: 5.2 → 6.0 → 6.1 → 7.0 → 7.1 → 7.2 → 8.0 → 8.1
3. Reference: `references/multi-hop-strategy.md`
4. Follow Pattern 1 Steps 4-6 for FIRST hop (5.2 → 6.0)
5. After first hop complete, repeat for next hops
6. **IMPORTANT:** After each hop, align load_defaults to the new version before starting the next hop

### Pattern 3: Breaking Changes Analysis Only
**User says:** "What breaking changes affect my app for Rails 8.0?"

This pattern is analysis-only — it intentionally skips Step 2 (Dual-Boot setup) and Step 3 (Validate Upgrade Path) because the user is not yet committing to an upgrade.

**Action - Step 0 (MANDATORY: Verify Latest Patch):**
1. Check if on latest patch — warn if not, recommend patching first

**Action - Step 1 (MANDATORY: Verify Tests Pass):**
1. Run test suite first
2. If tests fail → Warn user and recommend fixing first
3. If tests pass → Proceed with analysis

**Action - Step 4 (Run Detection):**
1. Load: `workflows/direct-detection-workflow.md`
2. Run detection directly using tools
3. Present findings summary
4. Offer to generate full upgrade report

---

## Quality Checklist

Before delivering, verify:

**For Direct Detection:**
- [ ] All patterns from version-specific YAML file checked
- [ ] Grep/Glob tools used correctly for each pattern
- [ ] File:line references collected for all findings
- [ ] Context captured for each finding

**For Comprehensive Upgrade Report:**
- [ ] All {PLACEHOLDERS} replaced with actual values
- [ ] Used ACTUAL findings from direct detection (not generic examples)
- [ ] Breaking changes section includes real file:line references
- [ ] Custom code warnings based on actual detected issues
- [ ] Code examples use user's actual code from affected files
- [ ] Next steps clearly outlined

**For CI Config Check (Step 6, before opening the PR):**
- [ ] Every CI file in the repo enumerated (GitHub Actions, CircleCI, Jenkins, GitLab, etc.)
- [ ] Ruby version, Rails matrix, and service versions diffed against the upgraded Gemfile
- [ ] CI sync report produced with per-file verdict
- [ ] All DRIFT entries fixed; overall verdict is OK

**For app:update Preview:**
- [ ] All {PLACEHOLDERS} replaced with actual values
- [ ] File list matches user's actual config files
- [ ] Diffs based on real current config vs target version
- [ ] Next steps clearly outlined

---

## Key Principles

1. **ALWAYS Verify Latest Patch First** (MANDATORY - ensure app is on latest patch of current series before any version hop)
2. **ALWAYS Run Test Suite** (MANDATORY - no exceptions, no upgrade work until tests pass)
3. **Block on Failing Tests** (if tests fail, STOP and help fix them before any upgrade work)
4. **Set Up Dual-Boot Early** (dual-boot is Step 2, right after tests pass - run both versions during the entire transition)
5. **Run Detection Directly** (use Grep/Glob/Read tools - no script generation needed)
6. **Always Use Actual Findings** (no generic examples in reports)
7. **Always Flag Custom Code** (with ⚠️ warnings based on detected issues)
8. **Always Use Templates** (for consistency)
9. **Always Check Quality** (before delivery)
10. **Load Workflows as Needed** (don't hold everything in memory)
11. **Sequential Process is Critical** (patch check → tests → dual-boot → validate path → detection → reports → implement → load_defaults)
12. **Follow FastRuby.io Methodology** (incremental upgrades, assessment first)
13. **Always Use `NextRails.next?` for Dual-Boot Code** (NEVER use `respond_to?` for version branching. DELEGATE to the `dual-boot` skill for patterns and setup.)
14. **Check CI Config Before Opening the PR** (run `workflows/ci-sync-workflow.md` to make sure every CI file matches the upgraded Gemfile — stale CI is the most common cause of red builds on upgrade PRs)
15. **Align load_defaults After the Version Bump** (load_defaults update happens AFTER the Rails version upgrade is complete)
16. **Mention, Don't Auto-Run, Cleanup** (after the upgrade ships, mention the `upgrade-cleanup` plugin. Delegate to it only when the user explicitly asks: "finish the upgrade", "clean up dual-boot", "drop the NextRails branches". Cleanup removes `NextRails.next?` / `NextRails.current?` branches and retires dual-boot scaffolding. Deprecation triage stays with this skill for the next hop.)

---

## Success Criteria

A successful upgrade assistance session:

✅ **Verified latest patch version** (Step 0 - MANDATORY)
✅ **Upgraded to latest patch if needed** (before any minor/major hop)
✅ **Ran test suite** (Step 1 - MANDATORY)
✅ **Verified all tests pass** (blocked if tests failed)
✅ **Recorded baseline metrics** (test count, coverage)
✅ **Set up dual-boot** (Step 2 - early, before upgrading)
✅ **Validated upgrade path** (Step 3 - single-hop vs multi-hop, hops planned)
✅ **Ran detection directly** (using Grep/Glob/Read tools - no script)
✅ **Generated Comprehensive Upgrade Report** using actual findings
✅ **Generated app:update Preview** using actual config files
✅ Used user's actual code from findings (not generic examples)
✅ Flagged all custom code with ⚠️ warnings based on detected issues
✅ **Implemented changes and upgraded Rails version**
✅ **Verified CI config matches the upgraded Gemfile** (Ruby, Rails matrix, services — all mismatches fixed before opening the PR)
✅ **Aligned load_defaults** (after upgrade is complete)
✅ **Mentioned cleanup after the upgrade shipped** (pointed to the `upgrade-cleanup` plugin without auto-running it; delegated only when the user explicitly asked)
✅ Provided clear next steps
✅ Offered to help implement changes

---

See [CHANGELOG.md](CHANGELOG.md) for version history and current version.
