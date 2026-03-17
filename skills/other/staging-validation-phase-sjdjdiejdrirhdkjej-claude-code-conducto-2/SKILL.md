---
name: staging-validation-phase
description: Guides manual staging validation before production deployment through smoke tests, critical user flow testing, data migration verification, and rollback capability checks. Use when validating staging deployments, running pre-production tests, or preparing for production promotion in staging-prod deployment model. (project)
---

<objective>
Validate staging deployment before promoting to production through systematic manual testing, automated smoke tests, data migration verification, and rollback capability testing. Ensures production deployments are safe, functional, and meet quality standards.

This skill orchestrates the staging validation phase, which occurs after /ship-staging and before /ship-prod in the staging-prod deployment workflow.

**Core responsibilities**:

- Run automated smoke tests on staging environment
- Test critical user flows manually (authentication, core features, payments)
- Verify data migrations executed successfully
- Test rollback capability (actual rollback + roll-forward)
- Document sign-off decision (approve/reject with justification)
- Update state.yaml with validation results

Inputs: Staging deployment (URL, deployment ID, migration results)
Outputs: Validation report, sign-off decision, state.yaml update
Expected duration: 30-60 minutes
</objective>

<quick_start>
Execute staging validation in 5 steps:

1. **Run smoke tests** - Execute automated smoke test suite on staging URL

   ```bash
   npm run test:smoke -- --url=$STAGING_URL
   ```

   Verify: homepage loads (200), API health endpoint (200), database connection

2. **Test critical user flows** - Manual testing of core functionality

   - Authentication (login, logout, password reset)
   - Primary user workflow (feature-specific)
   - Payment processing (if applicable)
   - Data CRUD operations

3. **Verify data migrations** - Check staging database for migration results

   ```bash
   # Connect to staging database
   psql $STAGING_DATABASE_URL -c "SELECT version FROM alembic_version;"
   # Verify tables, columns, constraints match expectations
   ```

4. **Test rollback capability** - Execute actual rollback test

   ```bash
   # Rollback to previous deployment
   vercel rollback $PREVIOUS_DEPLOYMENT_ID
   # Verify previous version is live
   # Roll forward to current deployment
   vercel promote $CURRENT_DEPLOYMENT_ID
   ```

5. **Document sign-off** - Update state.yaml
   ```yaml
   manual_gates:
     staging_validation:
       status: approved # or rejected
       approver: "Your Name"
       timestamp: "2025-11-19T10:30:00Z"
       blockers: [] # or list of issues if rejected
   ```

Key principle: Test as if this is production. All failures must be fixed before production deployment.
</quick_start>

<prerequisites>
<environment_checks>
Before running staging validation:
- [ ] Staging deployment completed successfully (from /ship-staging)
- [ ] Staging URL is live and accessible
- [ ] Deployment ID available (for rollback testing)
- [ ] Previous deployment ID available (for rollback test)
- [ ] Database migration logs available
- [ ] Test credentials available (for authentication flows)
</environment_checks>

<knowledge_requirements>
Required understanding before validation:

- **Smoke tests**: What automated tests exist, how to run them, what they verify
- **Critical user flows**: Which workflows are essential for production (auth, core feature, payments)
- **Data migrations**: What schema changes were made, how to verify them
- **Rollback procedure**: How to rollback deployment, how to verify previous version, how to roll forward
- **Sign-off criteria**: What constitutes approval vs rejection (all tests pass, no blocking bugs)

See deployment-strategy.md in project docs for platform-specific rollback procedures.
</knowledge_requirements>

<warnings>
- **Skip at your own risk**: Staging validation is the last quality gate before production. Skipping it risks deploying broken code to users.
- **Insufficient smoke tests**: Testing only homepage is inadequate. Must verify API, database, authentication, core features.
- **Assumed rollback works**: Must actually test rollback, not assume it works. Many rollback failures discovered during tests.
- **Vague sign-off**: "Looks good" is not a documented sign-off. Must update state.yaml with name, timestamp, decision.
</warnings>
</prerequisites>

<workflow>
<step number="1">
**Run Automated Smoke Tests**

Execute smoke test suite on staging environment.

**Smoke Test Suite**:

```bash
# Run smoke tests against staging URL
npm run test:smoke -- --url=$STAGING_URL

# Typical smoke tests include:
# - Homepage loads (HTTP 200, no errors in console)
# - API health endpoint responds (GET /api/health → 200)
# - Database connection established (health check includes DB ping)
# - Static assets load (CSS, JS, images)
# - Authentication page accessible (GET /login → 200)
```

**Success Criteria**:

- All smoke tests pass (0 failures)
- No 500 errors in server logs
- No console errors in browser DevTools
- Response times <2s for all endpoints

**If smoke tests fail**:

1. Document failures in validation report
2. Mark sign-off as "rejected" with blocker list
3. Return to /implement to fix issues
4. Re-deploy to staging
5. Re-run validation

**Quality Check**: Smoke tests provide quick confidence that deployment is functional, not a comprehensive test.
</step>

<step number="2">
**Test Critical User Flows**

Manually test essential user journeys on staging.

**Authentication Flow**:

```
1. Navigate to staging URL
2. Click "Login" or navigate to /login
3. Enter test credentials (test@example.com / test-password)
4. Verify successful login (redirects to dashboard, user menu shows)
5. Click "Logout"
6. Verify successful logout (redirects to homepage, user menu gone)
7. Test password reset flow (request reset, receive email, change password)
```

**Core Feature Flow** (feature-specific):

```
Example for "Student Progress Dashboard" feature:
1. Login as teacher
2. Navigate to /dashboard
3. Verify student list loads (check for >0 students)
4. Click on student name
5. Verify progress details load (completion rate, lessons, grades)
6. Test filters (by class, by date range)
7. Verify data accuracy (spot-check 3 students against database)
```

**Payment Processing Flow** (if applicable):

```
1. Add item to cart
2. Proceed to checkout
3. Enter test payment credentials (Stripe test mode)
4. Submit payment
5. Verify success confirmation
6. Verify order appears in user account
7. Verify payment recorded in admin panel
```

**Data CRUD Operations**:

```
1. Create: Add new entity (student, lesson, order)
2. Read: View entity details
3. Update: Edit entity details, save changes
4. Delete: Remove entity, verify removal
5. Verify persistence: Reload page, confirm changes persisted
```

**Success Criteria**:

- All critical flows complete without errors
- UI displays correctly (no layout issues, missing data)
- Data persists correctly (create/update/delete operations work)
- No JavaScript errors in console
- Performance acceptable (pages load <3s, interactions responsive)

**Quality Check**: Test flows that represent 80% of user activity. Don't test every edge case.
</step>

<step number="3">
**Verify Data Migrations**

Check that database migrations executed successfully in staging.

**Migration Verification**:

```bash
# Connect to staging database
psql $STAGING_DATABASE_URL

# Check migration version
SELECT version FROM alembic_version;
# Expected: Latest migration version (e.g., 4f3a2b1c5d6e)

# Verify schema changes
\d+ users  # Describe users table
# Check for expected columns, constraints, indexes

# Verify data migrations
SELECT COUNT(*) FROM users WHERE email_verified IS NOT NULL;
# Check backfill operations completed
```

**Schema Validation**:

- [ ] New tables exist (if migrations added tables)
- [ ] New columns exist with correct types (if migrations added columns)
- [ ] Constraints applied (NOT NULL, UNIQUE, FOREIGN KEY)
- [ ] Indexes created (check EXPLAIN ANALYZE on critical queries)
- [ ] Old columns removed (if migrations dropped columns)

**Data Validation**:

- [ ] Backfill operations completed (if migrations populated data)
- [ ] Default values applied (if migrations set defaults)
- [ ] Data integrity maintained (no orphaned records, referential integrity)

**Success Criteria**:

- Migration version matches expected version
- All schema changes present in staging database
- Data migrations completed (if applicable)
- No migration errors in deployment logs

**If migrations failed**:

1. Check deployment logs for migration errors
2. Document failure in validation report
3. Mark sign-off as "rejected"
4. Return to /implement to fix migration scripts
5. Re-deploy to staging (may require manual database cleanup)

**Quality Check**: Migrations are critical. A failed migration in production is catastrophic.
</step>

<step number="4">
**Test Rollback Capability**

Execute actual rollback test to verify production safety net.

**Rollback Test Procedure**:

**Step 4a: Identify Previous Deployment**:

```bash
# For Vercel deployments
vercel list --limit=5
# Find previous production deployment ID

# Store IDs
CURRENT_DEPLOYMENT_ID="<current-staging-deployment>"
PREVIOUS_DEPLOYMENT_ID="<previous-production-deployment>"
```

**Step 4b: Execute Rollback**:

```bash
# Rollback to previous deployment
vercel rollback $PREVIOUS_DEPLOYMENT_ID --yes

# Or via CLI:
vercel alias set $PREVIOUS_DEPLOYMENT_ID <staging-alias>
```

**Step 4c: Verify Previous Version Live**:

```
1. Navigate to staging URL
2. Verify previous version is live (check version number, feature presence)
3. Test critical flow to confirm functionality
4. Document: "Rollback successful, previous version ($PREVIOUS_DEPLOYMENT_ID) is live"
```

**Step 4d: Roll Forward**:

```bash
# Restore current deployment
vercel alias set $CURRENT_DEPLOYMENT_ID <staging-alias>
```

**Step 4e: Verify Current Version Restored**:

```
1. Navigate to staging URL
2. Verify current version is live (feature present)
3. Test critical flow to confirm functionality
4. Document: "Roll-forward successful, current version ($CURRENT_DEPLOYMENT_ID) is live"
```

**Success Criteria**:

- Rollback completed in <2 minutes
- Previous deployment verified live and functional
- Roll-forward completed successfully
- No data loss during rollback/roll-forward
- No downtime >30 seconds

**If rollback test fails**:

1. Document failure (which step failed, error message)
2. Mark sign-off as "rejected" with blocker: "Rollback capability not verified"
3. **BLOCK production deployment** - DO NOT proceed to /ship-prod
4. Fix rollback procedure (check deployment IDs, alias configuration, DNS)
5. Re-test rollback on staging

**Quality Check**: Rollback capability is the safety net for production. Must work reliably.
</step>

<step number="5">
**Document Sign-Off Decision**

Update state.yaml with validation results and approval decision.

**Approval Criteria**:

```
Sign-off as "approved" ONLY if:
- All smoke tests pass (0 failures)
- All critical user flows complete without errors
- Data migrations verified successfully
- Rollback test succeeds (rollback + roll-forward verified)
- No blocking bugs found during manual testing
```

**Rejection Criteria**:

```
Sign-off as "rejected" if ANY of:
- Smoke tests fail
- Critical user flows broken (authentication fails, core feature broken)
- Data migrations failed or incomplete
- Rollback test fails
- Blocking bugs found (security issue, data corruption, critical UX bug)
```

**state.yaml Update**:

**Approval Example**:

```yaml
manual_gates:
  staging_validation:
    status: approved
    approver: "Jane Smith"
    timestamp: "2025-11-19T14:30:00Z"
    validation_summary:
      smoke_tests: "All passed (8/8)"
      critical_flows: "All verified (authentication, dashboard, payments)"
      migrations: "Version 4f3a2b verified, schema changes confirmed"
      rollback_test: "Successful (rollback to dpl_abc123, roll-forward to dpl_xyz789)"
    blockers: []
```

**Rejection Example**:

```yaml
manual_gates:
  staging_validation:
    status: rejected
    approver: "Jane Smith"
    timestamp: "2025-11-19T14:30:00Z"
    validation_summary:
      smoke_tests: "1 failure (API health endpoint returned 503)"
      critical_flows: "Authentication broken (login redirects to 404)"
      migrations: "Verified"
      rollback_test: "Not attempted (smoke tests failed)"
    blockers:
      - "API health endpoint failing (503 error)"
      - "Login flow broken (404 on redirect)"
```

**Next Steps After Sign-Off**:

- If approved → Run `/ship-prod` to deploy to production
- If rejected → Return to `/implement`, fix blockers, re-deploy to staging, re-run validation

**Quality Check**: Sign-off must be explicit, documented, and traceable. No verbal approvals.
</step>
</workflow>

<validation>
<phase_checklist>
**Pre-validation checks**:
- [ ] Staging deployment completed (URL live)
- [ ] Deployment IDs available (current and previous)
- [ ] Test credentials available
- [ ] Database migration logs accessible

**During validation**:

- [ ] Smoke tests executed and passed
- [ ] Authentication flow tested (login, logout, password reset)
- [ ] Core feature flow tested (feature-specific)
- [ ] Payment flow tested (if applicable)
- [ ] Data migrations verified (schema + data)
- [ ] Rollback test executed (rollback + roll-forward)
- [ ] No blocking bugs found

**Post-validation**:

- [ ] state.yaml updated with sign-off
- [ ] Validation summary documented
- [ ] Blockers listed (if rejected)
- [ ] Next steps clear (ship-prod or return to implement)
      </phase_checklist>

<quality_standards>
**Good staging validation**:

- All smoke tests pass (automated verification)
- Critical flows tested thoroughly (manual verification)
- Data migrations verified (database inspection)
- Rollback tested (actual rollback, not assumed)
- Sign-off documented (state.yaml with approver, timestamp)
- Duration: 30-60 minutes (efficient but thorough)

**Bad staging validation**:

- Only homepage tested (insufficient coverage)
- Rollback assumed to work (not actually tested)
- Verbal approval only (no documented sign-off)
- Blocking bugs ignored ("we'll fix in production")
- Rushed (<15 minutes, corners cut)
  </quality_standards>
  </validation>

<anti_patterns>
<pitfall name="insufficient_smoke_tests">
**Impact**: Deploys broken code to production

**Scenario**:

```
Tester: "I checked the homepage, looks good!"
Reality: API returns 500 errors, authentication broken, database connection failing
Result: Production deployment breaks core functionality
```

**Prevention**:

- Run full smoke test suite (homepage, API, database, authentication)
- Verify automated tests pass, not just manual homepage check
- Check server logs for errors, not just UI
- Test critical endpoints (health check, auth, core API)

**Good Practice**:

```bash
npm run test:smoke -- --url=$STAGING_URL
# Verifies: homepage (200), API health (200), DB connection (success), auth page (200)
```

</pitfall>

<pitfall name="unclear_sign_off">
**Impact**: No accountability, unclear approval state

**Scenario**:

```
Slack message: "Staging looks good 👍"
Result: No documented approval, unclear who approved, no timestamp, no validation summary
```

**Prevention**:

- Always update state.yaml with sign-off
- Include approver name, timestamp, validation summary
- Document blockers if rejected
- Make approval explicit and traceable

**Good Practice**:

```yaml
manual_gates:
  staging_validation:
    status: approved
    approver: "Jane Smith"
    timestamp: "2025-11-19T14:30:00Z"
    validation_summary: "All tests pass, rollback verified"
```

</pitfall>

<pitfall name="skipped_rollback_test">
**Impact**: Rollback fails in production when needed

**Scenario**:

```
Tester: "Rollback should work, Vercel has rollback feature"
Reality: Rollback deployed but DNS not updated, or deployment ID incorrect, or database migration not reversible
Result: Production incident, attempted rollback fails, extended downtime
```

**Prevention**:

- **Always test rollback** on staging before production deployment
- Execute actual rollback (change alias/DNS)
- Verify previous version is live
- Test roll-forward to confirm current version restored
- Document rollback + roll-forward success

**Good Practice**:

```bash
# Actual rollback test
vercel rollback $PREVIOUS_ID
# Verify previous version live (manual test)
vercel alias set $CURRENT_ID staging
# Verify current version restored (manual test)
```

</pitfall>

<pitfall name="ignored_blocking_bugs">
**Impact**: Deploys known bugs to production

**Scenario**:

```
Tester: "Login is broken but we'll fix it in a hotfix"
Result: Production users cannot login, support tickets spike, revenue impacted
```

**Prevention**:

- Mark validation as "rejected" for any blocking bug
- Blocking bugs: authentication broken, core feature broken, data corruption, security issue
- Fix blocking bugs before production deployment
- No "we'll fix it later" for critical issues

**Good Practice**:

```yaml
status: rejected
blockers:
  - "Login redirects to 404 (critical - blocks all users)"
next_steps: "Fix login redirect, re-deploy to staging, re-validate"
```

</pitfall>

<pitfall name="rushed_validation">
**Impact**: Misses critical bugs, false confidence

**Scenario**:

```
Tester: "Validated in 10 minutes, good to go"
Reality: Only tested happy path, missed edge cases, didn't verify migrations
Result: Production deployment fails on edge cases (null values, missing data, concurrent users)
```

**Prevention**:

- Allocate 30-60 minutes for thorough validation
- Test critical flows completely (not just happy path)
- Verify data migrations (schema + data)
- Test rollback capability
- Don't rush the last quality gate before production

**Good Practice**:

```
30-60 minute validation:
- 10 min: Smoke tests
- 15 min: Critical user flows (auth, core feature, payments)
- 10 min: Data migration verification
- 10 min: Rollback test
- 5 min: Document sign-off
```

</pitfall>
</anti_patterns>

<best_practices>
<smoke_test_automation>
**When to use**: Always, for every staging deployment

**Approach**:

1. Create smoke test suite that runs against any URL
2. Include tests for: homepage, API health, database connection, authentication page
3. Run via npm script: `npm run test:smoke -- --url=$STAGING_URL`
4. Verify all tests pass before manual testing

**Benefits**:

- Catches deployment issues immediately (before manual testing)
- Automated, repeatable, fast (2-3 minutes)
- Provides confidence baseline for manual testing

**Example**:

```javascript
// tests/smoke.test.js
describe("Smoke Tests", () => {
  const baseURL = process.env.TEST_URL || "http://localhost:3000";

  test("homepage loads", async () => {
    const response = await fetch(baseURL);
    expect(response.status).toBe(200);
  });

  test("API health endpoint responds", async () => {
    const response = await fetch(`${baseURL}/api/health`);
    expect(response.status).toBe(200);
    const data = await response.json();
    expect(data.database).toBe("connected");
  });
});
```

</smoke_test_automation>

<critical_flow_checklist>
**When to use**: Every staging validation

**Approach**:

1. Identify 3-5 critical user flows (authentication, core feature, payments)
2. Create checklist for each flow
3. Test each flow manually on staging
4. Document results in validation summary

**Benefits**:

- Ensures essential functionality works before production
- Catches UX bugs that automated tests miss
- Provides structured testing approach (no guessing)

**Example Checklist**:

```markdown
Authentication Flow:

- [ ] Login with valid credentials succeeds
- [ ] Login with invalid credentials fails (shows error)
- [ ] Logout succeeds (session cleared)
- [ ] Password reset email sent
- [ ] Password reset link works
- [ ] New password accepted
```

</critical_flow_checklist>

<rollback_test_discipline>
**When to use**: Every staging validation (non-negotiable)

**Approach**:

1. Identify previous production deployment ID
2. Execute rollback to previous deployment
3. Verify previous version is live (manual test)
4. Execute roll-forward to current deployment
5. Verify current version restored (manual test)
6. Document rollback + roll-forward success

**Benefits**:

- Verifies safety net works before production deployment
- Builds muscle memory for production rollback procedure
- Identifies rollback issues in safe environment (staging)

**Example**:

```bash
# Rollback test
PREVIOUS_ID=$(vercel list --limit=5 | grep production | head -1 | awk '{print $1}')
vercel rollback $PREVIOUS_ID
# Manual verification: Navigate to staging, confirm previous version live
vercel alias set $CURRENT_ID staging
# Manual verification: Navigate to staging, confirm current version live
```

</rollback_test_discipline>
</best_practices>

<success_criteria>
Staging validation phase complete when:

- [ ] All smoke tests pass (0 failures)
- [ ] All critical user flows verified (authentication, core feature, payments)
- [ ] Data migrations verified (schema + data correct)
- [ ] Rollback test succeeds (rollback + roll-forward verified)
- [ ] Sign-off documented in state.yaml (approver, timestamp, validation summary)
- [ ] Decision is "approved" (ready for production) OR "rejected" (blockers documented, return to implement)

Ready to proceed when:

- If approved → Run `/ship-prod` to deploy to production
- If rejected → Return to `/implement`, fix blockers, re-deploy to staging, re-run validation
  </success_criteria>

<troubleshooting>
**Issue**: Smoke tests failing on staging
**Solution**: Check deployment logs for errors, verify environment variables set, check database connection, re-deploy if necessary

**Issue**: Critical user flow broken (authentication, core feature)
**Solution**: Mark validation as "rejected", document blocker, return to /implement to fix, re-deploy to staging, re-validate

**Issue**: Data migrations not showing in staging database
**Solution**: Check deployment logs for migration errors, verify migration scripts syntax, manually run migrations on staging if needed

**Issue**: Rollback test fails (previous version not live)
**Solution**: Verify deployment IDs correct, check alias/DNS configuration, test rollback procedure manually, update deployment scripts if needed

**Issue**: Unclear what to test (no critical flows documented)
**Solution**: Review spec.md for feature requirements, identify essential user workflows (authentication always critical), create flow checklist, document for future validations

**Issue**: Validation taking >90 minutes (too long)
**Solution**: Focus on critical flows only (don't test every edge case), automate smoke tests (don't test manually), parallelize testing where possible, skip exhaustive testing (save for QA phase)
</troubleshooting>

<reference_guides>
For detailed documentation:

**Deployment Procedures**: Project-specific deployment documentation

- Vercel deployment: See `.github/workflows/deploy-staging.yml` for deployment automation
- Rollback procedures: See `docs/project/deployment-strategy.md` for platform-specific rollback steps
- Database migrations: See `alembic/README.md` for migration best practices

**Testing Guides**:

- Smoke tests: See `tests/smoke/README.md` for smoke test suite documentation
- Critical flow testing: See spec.md for feature-specific critical flows
- Performance testing: See `docs/performance-budgets.md` for performance targets

**Quality Gates**:

- Pre-flight validation: Completed in /optimize phase (performance, accessibility, security)
- Staging validation: This skill (manual testing, smoke tests, rollback capability)
- Production validation: Post-deployment verification in /ship-prod (health checks, smoke tests on production)

Next phase after staging validation:

- If approved → `/ship-prod` (deploy to production, run production smoke tests, finalize)
- If rejected → `/implement` (fix blockers, re-deploy to staging, re-run /validate-staging)
  </reference_guides>
