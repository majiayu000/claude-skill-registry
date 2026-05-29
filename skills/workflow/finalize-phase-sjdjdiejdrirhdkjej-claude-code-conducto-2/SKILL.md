---
name: finalize-phase
description: Completes feature/epic workflows after deployment with comprehensive walkthrough generation for epics (v5.0+), roadmap updates, artifact archival, documentation, and branch cleanup. Use after /ship-prod, /deploy-prod, or /build-local completes, or when user asks to finalize. (project)
---

<objective>
Complete feature/epic workflow, generate walkthrough (epics only), update roadmap, archive artifacts, and preserve knowledge after deployment. Ensures clean workflow closure with self-improving workflow system.

This skill orchestrates the /finalize phase, the final step after successful deployment to production, direct-prod, or local build.

**For Epic Workflows (v5.0+)**:

- Generate comprehensive walkthrough.md with velocity metrics, sprint results, lessons learned
- Run post-mortem audit with pattern detection (after 2-3 epics)
- Offer workflow healing with improvement recommendations
- Detect patterns for custom skills/commands generation

**For Feature Workflows**:

- Standard finalization (roadmap, artifacts, docs, branches)

Inputs: Deployed feature/epic, phase artifacts, ship report, state.yaml
Outputs: walkthrough.md (epics only), updated roadmap, archived artifacts, updated documentation
Expected duration: 10-15 minutes (features), 20-30 minutes (epics with walkthrough)
</objective>

<quick_start>
After deployment completes, finalize the workflow:

**Epic Workflows (NEW in v5.0)**: 0. Generate walkthrough - Comprehensive epic summary with velocity metrics, sprint results, lessons learned, pattern detection

1. Run post-mortem audit - Final effectiveness analysis with improvement recommendations
2. Offer workflow healing - Apply discovered improvements with user approval

**All Workflows** (features + epics):

1. Update roadmap - Move to "Shipped" with completion date, version, production URL
2. Archive artifacts - Verify all phase artifacts in specs/NNN-slug/ or epics/NNN-slug/
3. Update documentation - README, CHANGELOG, user guides (if applicable)
4. Clean up branches - Delete feature branch locally and remotely
5. Commit finalization - Small commit documenting workflow closure

Key principles:

- Clean closure preserves knowledge and enables learning
- Epic walkthroughs enable self-improving workflow system
- Pattern detection (after 2-3 epics) suggests custom automation
  </quick_start>

<prerequisites>
Before beginning finalization:
- Deployment completed successfully (/ship-prod, /deploy-prod, or /build-local done)
- Ship report generated (ship-summary.md exists)
- All phase artifacts present in specs/NNN-slug/
- Git working tree clean (all changes committed)

If deployment incomplete, return to /ship phase.
</prerequisites>

<workflow>
<step number="0">
**Epic Walkthrough Generation** (Epic workflows only - NEW in v5.0)

Detect epic vs feature workflow and generate comprehensive walkthrough for epics.

**Detection**:

```bash
if [ -f "epics/*/epic-spec.xml" ]; then
  WORKSPACE_TYPE="epic"
  EPIC_DIR=$(dirname "epics/*/epic-spec.xml")
else
  WORKSPACE_TYPE="feature"
  # Skip to Step 1 (standard finalization)
  continue
fi
```

**If feature workflow**: Skip this step entirely, proceed to Step 1

**If epic workflow**: Generate walkthrough before standard finalization

**Walkthrough Generation Pipeline**:

1. **Gather all epic artifacts**:

   - epic-spec.xml (epic specification)
   - research.xml (research phase output)
   - plan.xml (plan phase output with meta-prompting)
   - sprint-plan.xml (task breakdown with dependency graph)
   - state.yaml (state tracking across phases)
   - audit-report.xml (workflow effectiveness analysis)
   - preview-report.xml (manual testing decision)
   - Sprint results from epics/NNN-slug/sprints/\*/

2. **Calculate velocity metrics**:

   - Expected parallelization multiplier (from sprint-plan.xml)
   - Actual parallelization multiplier (from audit-report.xml)
   - Time saved in hours (parallel vs sequential execution)
   - Duration from start to completion

3. **Extract key information**:

   - Epic goal and success metrics
   - Phases completed with timestamps
   - Sprint execution results (status, tasks, duration, contracts, tests)
   - Validation results (optimization, preview decision)
   - Key files modified
   - Next steps (enhancements, technical debt, monitoring needs)

4. **Generate walkthrough.xml and walkthrough.md**:

   - Use template: `.spec-flow/templates/walkthrough.xml`
   - Populate with metrics, sprint results, lessons learned
   - Write both machine-readable (XML) and human-readable (Markdown) versions

5. **Run post-mortem audit**:

   - Invoke `/audit-workflow --post-mortem`
   - Analyze velocity accuracy (expected vs actual)
   - Detect bottlenecks and inefficiencies
   - Generate improvement recommendations

6. **Pattern detection** (if 2+ epics completed):

   - Analyze patterns across completed epics
   - Detect code generation patterns (service boilerplate repeated 3x)
   - Detect architectural patterns (all services use DI + Repository)
   - Detect workflow patterns (always clarify auth approach)
   - Suggest custom skills/commands if confidence ≥80%

7. **Offer workflow healing**:

   - Display immediate improvements from audit recommendations
   - Categorize by priority (immediate vs deferred)
   - Offer `/heal-workflow` to apply improvements
   - Save deferred improvements for pattern-based optimization

8. **Commit walkthrough**:

```bash
git add epics/*/walkthrough.xml
git add epics/*/walkthrough.md
git add epics/*/audit-report.xml

git commit -m "docs: generate epic walkthrough

[EPIC SUMMARY]
Epic: ${epic_slug}
Duration: ${duration_hours}h
Velocity: ${velocity_multiplier}x (saved ${time_saved}h)

[SPRINTS COMPLETED]
Total: ${total_sprints}
Execution: ${execution_strategy}
Tasks: ${tasks_completed}/${total_tasks}

[QUALITY METRICS]
Audit Score: ${audit_score}/100
Phase Efficiency: ${phase_efficiency}/100

[LESSONS LEARNED]
- What worked: ${what_worked_summary}
- What struggled: ${what_struggled_summary}

{IF recommendations > 0}
Improvement recommendations: ${recommendations_count}
Run /heal-workflow to apply improvements
{ENDIF}

🤖 Generated with Claude Code
Co-Authored-By: Claude <noreply@anthropic.com>"
```

9. **Present walkthrough summary** to user with:
   - Velocity metrics (expected vs actual, time saved)
   - Sprint results (status, tasks, duration, tests)
   - Quality metrics (audit score, phase efficiency, parallelization score)
   - What worked / what struggled / lessons learned
   - Improvement recommendations (if any)
   - Pattern detection results (if 2+ epics completed)

**After walkthrough complete**: Proceed to Step 1 (standard finalization)

**Validation**: For epics, walkthrough.xml and walkthrough.md exist in epics/NNN-slug/

See reference.md for epic walkthrough generation details.
</step>

<step number="1">
**Update Roadmap**

Move feature from "In Progress" to "Shipped" section in roadmap.

**Actions**:

1. Open `.spec-flow/memory/roadmap.md`
2. Find feature in "In Progress" section
3. Move to "Shipped" section with completion details

**Required information**:

- Completion date (deployment date)
- Version number (from CHANGELOG or ship report)
- Production URL (if applicable)
- Links to ship report and release notes

**Example**:

```markdown
## Shipped

### Student Progress Dashboard (v1.3.0) - Shipped 2025-10-21

- **Production URL**: https://app.example.com/students/progress
- **Ship Report**: specs/042-student-progress-dashboard/ship-summary.md
- **Release Notes**: CHANGELOG.md#v1.3.0
- **Impact**: Teachers can now track student progress with completion rates and time spent
```

**Validation**: Feature appears in "Shipped" section with all required details.

See reference.md for roadmap update checklist.
</step>

<step number="2">
**Archive Artifacts**

Verify all workflow artifacts archived in `specs/NNN-slug/` directory.

**Required artifacts checklist**:

- [ ] spec.md (feature specification)
- [ ] plan.md (implementation plan)
- [ ] tasks.md (task breakdown)
- [ ] optimization-report.md (quality gates results)
- [ ] preview-checklist.md (manual testing checklist - if applicable)
- [ ] ship-summary.md (deployment report)
- [ ] release-notes.md (user-facing release notes)
- [ ] state.yaml (workflow state tracking)

**Optional artifacts**:

- [ ] clarifications.md (if /clarify phase ran)
- [ ] analysis-report.md (if /validate phase ran)
- [ ] staging-ship-report.md (if staging deployment happened)

**Validation steps**:

```bash
# List all artifacts in feature directory
ls -la specs/NNN-slug/

# Should see all required files
# No temporary files (.tmp, .bak, etc.)
```

**If artifacts missing**:

- Check for artifacts in wrong locations (root directory, temp folders)
- Regenerate missing artifacts if possible
- Document missing artifacts in finalization commit message

See reference.md for complete artifact checklist.
</step>

<step number="3">
**Update Documentation**

Update user-facing documentation for shipped feature.

**README.md updates** (if user-facing feature):

```markdown
## Features

- **Student Progress Dashboard** - Track student completion rates and time spent
  - View individual student progress
  - Filter by class, subject, or time period
  - Export progress reports to CSV
```

**CHANGELOG.md updates**:

```markdown
## [1.3.0] - 2025-10-21

### Added

- Student progress dashboard with completion tracking
- CSV export for progress reports
- Filtering by class, subject, and time period

### Changed

- Improved dashboard load time from 3s to 1.2s

### Fixed

- Fixed timeout issue with large datasets (pagination added)
```

**User guides** (for complex features):

- Create docs/features/student-progress-dashboard.md
- Include screenshots, usage instructions, FAQs
- Link from README.md

**Validation**: Documentation accurately reflects shipped feature.

See reference.md for documentation standards.
</step>

<step number="4">
**Clean Up Branches**

Delete feature branch locally and remotely (if applicable).

**Local branch deletion**:

```bash
# Verify branch is merged
git branch --merged main | grep feature/042-student-progress-dashboard

# Delete local branch
git branch -d feature/042-student-progress-dashboard
```

**Remote branch deletion** (if pushed to remote):

```bash
# Delete remote branch
git push origin --delete feature/042-student-progress-dashboard

# Verify deletion
git branch -r | grep feature/042-student-progress-dashboard  # Should return nothing
```

**If branch not merged**:

- Verify feature deployed successfully
- If deployed, force delete: `git branch -D feature/...`
- Document why branch not merged in commit message

**Validation**: Feature branch no longer exists locally or remotely.

See reference.md for branch cleanup guidelines.
</step>

<step number="5">
**Commit Finalization**

Create small commit documenting workflow closure.

**Commit format**:

```bash
git add .spec-flow/memory/roadmap.md README.md CHANGELOG.md
git commit -m "chore: finalize student-progress-dashboard (v1.3.0)

Updated roadmap, README, and CHANGELOG
Archived artifacts in specs/042-student-progress-dashboard/"
```

**Commit message format**:

- Type: `chore` (finalization is housekeeping)
- Subject: `finalize [feature-name] ([version])`
- Body: List what was updated (roadmap, docs, etc.)

**Update state.yaml**:

```yaml
finalization:
  status: completed
  completion_date: 2025-10-21
  version: v1.3.0
  artifacts_archived: true
  documentation_updated: true
  branches_cleaned: true
```

**Validation**: Finalization commit pushed to main branch.

See reference.md for commit best practices.
</step>
</workflow>

<validation>
After finalization phase, verify:

- Roadmap updated (feature in "Shipped" section with completion date, version, URL)
- All artifacts archived (checklist 100% complete)
- Documentation updated (README, CHANGELOG, user guides if applicable)
- Branches cleaned up (feature branch deleted locally and remotely)
- Finalization committed (chore commit with workflow closure details)
- state.yaml updated (finalization.status = completed)

Workflow is now cleanly closed and ready for retrospective analysis.
</validation>

<anti_patterns>
<pitfall name="roadmap_not_updated">
**❌ Don't**: Skip roadmap update, leave feature in "In Progress"
**✅ Do**: Always move to "Shipped" with completion date and links

**Why**: Roadmap becomes stale and inaccurate. Team loses visibility into what shipped and when.

**Impact**:

- Historical tracking lost
- Roadmap doesn't reflect reality
- Hard to analyze velocity over time

**Example** (bad):

```
Feature deploys to production
/finalize skips roadmap update
Roadmap still shows feature "In Progress"
6 months later: "Did we ship this? When?"
```

**Example** (good):

```
Feature deploys to production
/finalize updates roadmap immediately
Roadmap shows "Shipped 2025-10-21, v1.3.0"
6 months later: Clear historical record
```

</pitfall>

<pitfall name="incomplete_documentation">
**❌ Don't**: Skip README/CHANGELOG updates for "small" features
**✅ Do**: Update all user-facing documentation for every shipped feature

**Why**: Knowledge loss compounds over time. Users can't discover features if not documented.

**Impact**:

- Feature discovery issues (users don't know feature exists)
- Onboarding friction (new team members confused)
- Version history unclear (what changed when?)

**Example** (bad):

```
Ship feature, skip README update
3 months later: User asks "Do we have progress tracking?"
Answer: "Yes, we shipped that 3 months ago" (not documented)
```

**Example** (good):

```
Ship feature, update README immediately
README: "Student Progress Dashboard - Track completion"
User discovers feature organically from README
```

</pitfall>

<pitfall name="branch_not_deleted">
**❌ Don't**: Leave feature branches around "just in case"
**✅ Do**: Delete merged feature branches immediately

**Why**: Branch clutter makes it hard to find active work.

**Impact**:

- Git branch list becomes unusable (100+ stale branches)
- Hard to identify active development
- Wastes storage (remote branches)

**Example** (bad):

```
git branch -a
# Shows 87 feature branches (only 3 active)
# Which branches are safe to delete? Unknown.
```

**Example** (good):

```
git branch -a
# Shows 3 feature branches (all active)
# Clear signal: current work only
```

</pitfall>

<pitfall name="no_finalization_commit">
**❌ Don't**: Update files without committing finalization
**✅ Do**: Create explicit finalization commit documenting closure

**Why**: Finalization changes should be tracked in git history.

**Impact**:

- Changes not backed up
- No clear signal when workflow closed
- Hard to audit finalization process

**Example** (bad):

```
Update roadmap, README, CHANGELOG
Git status: 3 modified files
Never commit (lose changes on machine wipe)
```

**Example** (good):

```
Update roadmap, README, CHANGELOG
git commit -m "chore: finalize feature (v1.3.0)"
Clear git history marker: finalization happened
```

</pitfall>

<pitfall name="artifacts_not_archived">
**❌ Don't**: Delete or lose phase artifacts after deployment
**✅ Do**: Archive all artifacts in specs/NNN-slug/ permanently

**Why**: Artifacts contain valuable context for future maintenance.

**Impact**:

- Context loss (why was feature built this way?)
- Hard to debug issues (no spec to reference)
- Can't analyze past decisions (no plan to review)

**Example** (bad):

```
Ship feature, delete spec.md and plan.md
6 months later: "Why did we implement it this way?"
Answer: Unknown (artifacts deleted)
```

**Example** (good):

```
Ship feature, archive all artifacts
6 months later: "Why did we implement it this way?"
Answer: Check specs/042-.../spec.md (clear rationale)
```

</pitfall>
</anti_patterns>

<best_practices>
<practice name="immediate_finalization">
Run /finalize immediately after deployment succeeds:

- Don't defer finalization "for later"
- Don't batch multiple finalizations
- Run while deployment fresh in memory

Result: Accurate documentation, fewer missed steps
</practice>

<practice name="complete_artifact_checklist">
Use complete artifact checklist from reference.md:

- Verify each artifact present
- Check for artifacts in wrong locations
- Document missing artifacts if any

Result: Complete archival, no lost context
</practice>

<practice name="user_facing_documentation">
Always update README and CHANGELOG for user-facing features:

- README: Feature list with one-line descriptions
- CHANGELOG: Version entry with Added/Changed/Fixed
- User guides: Detailed instructions for complex features

Result: Feature discoverability, clear version history
</practice>

<practice name="clean_branch_hygiene">
Delete merged branches immediately:

- Verify branch merged before deleting
- Delete local and remote branches
- Keep git branch list clean (active work only)

Result: Clear signal of active development, reduced clutter
</practice>

<practice name="explicit_finalization_commit">
Create explicit commit documenting workflow closure:

- Type: chore
- Subject: finalize [feature-name] ([version])
- Body: List updates (roadmap, docs, artifacts)

Result: Clear git history marker, auditable finalization
</practice>
</best_practices>

<success_criteria>
Finalization phase complete when:

- [ ] Roadmap updated (feature moved to "Shipped" with date, version, URL, links)
- [ ] All artifacts archived (100% checklist complete in specs/NNN-slug/)
- [ ] Documentation updated (README, CHANGELOG, user guides if applicable)
- [ ] Branches cleaned up (feature branch deleted locally and remotely)
- [ ] Finalization committed (chore commit documenting closure)
- [ ] state.yaml updated (finalization.status = completed)

Workflow is cleanly closed and ready for retrospective analysis.
</success_criteria>

<quality_standards>
**Good finalization**:

- Immediate (runs right after deployment)
- Complete (all artifacts archived, all docs updated)
- Clean (branches deleted, commit made)
- Documented (roadmap + README + CHANGELOG updated)

**Bad finalization**:

- Deferred (runs days/weeks later, details forgotten)
- Incomplete (missing artifacts, incomplete docs)
- Messy (branches not deleted, no commit)
- Undocumented (roadmap stale, README outdated)
  </quality_standards>

<troubleshooting>
**Issue**: Can't find feature in roadmap "In Progress" section
**Solution**: Check "Backlog" or "Planned" sections, or search entire roadmap file with grep

**Issue**: Missing artifacts (spec.md, plan.md, etc.)
**Solution**: Check root directory, temp folders, or regenerate if possible. Document missing in commit.

**Issue**: Feature branch won't delete (not merged)
**Solution**: Verify feature deployed successfully, then force delete with `git branch -D`. Document in commit.

**Issue**: Unclear what version to use
**Solution**: Check CHANGELOG for next version number, or use deployment date as version (v2025.10.21)

**Issue**: Don't know what to put in CHANGELOG
**Solution**: Review ship-summary.md and release-notes.md for user-facing changes. Focus on Added/Changed/Fixed.
</troubleshooting>

<reference_guides>
Finalization procedures:

- Roadmap Update Checklist (reference.md#roadmap-updates) - Required information and format
- Artifact Archival Guide (reference.md#artifact-archival) - Complete checklist and validation
- Documentation Standards (reference.md#documentation-updates) - README, CHANGELOG, user guide formats

Examples:

- Complete Finalization (examples.md#complete-finalization) - All steps done correctly
- Rushed Cleanup (examples.md#rushed-cleanup) - What happens when steps skipped

Workflow closure:
After finalization completes, feature workflow is closed. Retrospective analysis can begin to learn from past work.
</reference_guides>
