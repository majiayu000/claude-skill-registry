---
name: production-deployment-phase
description: Executes production deployment workflow by promoting validated staging builds to production with semantic versioning, health checks, and release tagging. Use when running /ship-prod command, deploying to production after staging validation, or promoting staging builds to production environment.
---

<objective>
Execute production deployment workflow by promoting validated staging builds to production with semantic versioning, health checks, release tagging, and comprehensive monitoring.
</objective>

<quick_start>
<production_deployment_workflow>
**Prerequisite-driven production promotion:**

1. **Verify staging validation**: Check state.yaml manual_gates.staging_validation.status = approved
2. **Bump semantic version**: Update package.json/version files (major.minor.patch)
3. **Create release tag**: Tag git commit with new version
4. **Deploy to production**: Push to production branch or trigger deployment
5. **Run health checks**: Verify endpoints, databases, services operational
6. **Generate ship report**: Document deployment artifacts and metadata
7. **Monitor post-deploy**: Watch logs, metrics, alerts for 15-30 minutes

**Example workflow:**

```
Verifying staging validation complete... ✅
Current version: 2.6.0
Bump type: minor (new features added)
New version: 2.7.0

Creating git tag v2.7.0... ✅
Pushing to production branch... ✅
Triggering production deployment... ✅

Health checks:
  API endpoints: 200 OK ✅
  Database connections: healthy ✅
  Cache: operational ✅
  CDN: propagated ✅

Production deployment successful!
Release: https://github.com/user/repo/releases/tag/v2.7.0
Ship report: specs/NNN-slug/production-ship-report.md
```

</production_deployment_workflow>

<trigger_conditions>
**Auto-invoke when:**

- `/ship-prod` command executed
- User mentions "deploy to production", "ship to prod", "production release"
- state.yaml shows current_phase: ship-prod

**Prerequisites required:**

- Staging validation approved (manual_gates.staging_validation.status = approved)
- Rollback gate passed (quality_gates.rollback.status = passed)
- Git repository has remote configured
- Production deployment configuration exists
  </trigger_conditions>
  </quick_start>

<workflow>
<step_1_verify_staging>
**1. Verify Staging Validation Complete**

Check workflow state for staging validation approval:

```bash
# Read workflow state
STATE_FILE="specs/$(ls -t specs/ | head -1)/state.yaml"

STAGING_STATUS=$(grep -A2 "staging_validation:" "$STATE_FILE" | grep "status:" | awk '{print $2}')

if [ "$STAGING_STATUS" != "approved" ]; then
  echo "❌ BLOCKED: Staging validation not approved"
  echo "Current status: $STAGING_STATUS"
  echo "Run: /validate-staging to complete manual validation"
  exit 1
fi

echo "✅ Staging validation approved"
```

**Blocking conditions:**

- Staging validation status ≠ approved
- Rollback gate status ≠ passed
- No staging deployment exists
  </step_1_verify_staging>

<step_2_bump_version>
**2. Bump Semantic Version**

Determine version bump type and update version files:

```bash
# Read current version
CURRENT_VERSION=$(node -p "require('./package.json').version")

# Determine bump type from CHANGELOG or git commits
# - major: Breaking changes
# - minor: New features (backward compatible)
# - patch: Bug fixes only

# Use npm version or manual update
npm version minor -m "chore: bump version to %s for production release"

NEW_VERSION=$(node -p "require('./package.json').version")

echo "Version bumped: $CURRENT_VERSION → $NEW_VERSION"
```

**Semantic versioning rules:**

- **Major (X.0.0)**: Breaking changes, API contract changes
- **Minor (0.X.0)**: New features, backward compatible
- **Patch (0.0.X)**: Bug fixes, no new features

**Files to update:**

- package.json (version field)
- CHANGELOG.md (unreleased → version section)
- Any version constants in code
  </step_2_bump_version>

<step_3_create_release_tag>
**3. Create Git Release Tag**

Tag the commit and push to remote:

```bash
# Create annotated tag
git tag -a "v${NEW_VERSION}" -m "Release v${NEW_VERSION}

$(sed -n "/## \[${NEW_VERSION}\]/,/## \[/p" CHANGELOG.md | head -n -1)"

# Push tag to remote
git push origin "v${NEW_VERSION}"

echo "✅ Tag created and pushed: v${NEW_VERSION}"
```

**Tag format:**

- Annotated tags required (not lightweight)
- Prefix with "v" (e.g., v2.7.0)
- Include CHANGELOG excerpt in tag message
  </step_3_create_release_tag>

<step_4_deploy_production>
**4. Deploy to Production**

Trigger production deployment based on deployment model:

```bash
# Model 1: Git push to production branch
git push origin main:production

# Model 2: GitHub Actions deployment
gh workflow run deploy-production.yml \
  -f version="${NEW_VERSION}" \
  -f environment=production

# Model 3: Direct deployment platform (Vercel, Netlify, etc.)
vercel --prod --yes
```

**Deployment verification:**

- Wait for deployment to complete
- Check deployment platform status
- Verify deployment ID/URL returned
- Record deployment metadata
  </step_4_deploy_production>

<step_5_health_checks>
**5. Run Production Health Checks**

Verify all critical services operational:

```bash
echo "Running production health checks..."

# API endpoints
for ENDPOINT in /health /api/status /api/version; do
  STATUS=$(curl -s -o /dev/null -w "%{http_code}" "https://production.example.com$ENDPOINT")
  if [ "$STATUS" = "200" ]; then
    echo "  ✅ $ENDPOINT: $STATUS OK"
  else
    echo "  ❌ $ENDPOINT: $STATUS FAILED"
    HEALTH_FAILED=true
  fi
done

# Database connectivity
# (Run via deployment platform or SSH to production)

# Cache/Redis
# CDN propagation
# Background jobs

if [ "$HEALTH_FAILED" = "true" ]; then
  echo "❌ Health checks failed - initiate rollback"
  exit 1
fi

echo "✅ All health checks passed"
```

**Critical checks:**

- API endpoints return 200 OK
- Database connections healthy
- Cache/Redis operational
- CDN serving latest assets
- Background jobs processing
  </step_5_health_checks>

<step_6_generate_ship_report>
**6. Generate Production Ship Report**

Create production-ship-report.md with deployment metadata:

```bash
cat > specs/$FEATURE_SLUG/production-ship-report.md <<EOF
# Production Ship Report: $FEATURE_SLUG

## Deployment Summary
- **Version**: v${NEW_VERSION}
- **Deployed at**: $(date -Iseconds)
- **Deployment ID**: ${DEPLOYMENT_ID}
- **Production URL**: https://production.example.com
- **Release URL**: https://github.com/user/repo/releases/tag/v${NEW_VERSION}

## Health Checks
- API endpoints: ✅ All passing
- Database: ✅ Healthy
- Cache: ✅ Operational
- CDN: ✅ Propagated

## Deployment Artifacts
- Git tag: v${NEW_VERSION}
- Commit SHA: ${COMMIT_SHA}
- Deployment platform: ${PLATFORM}

## Rollback Procedure
1. Revert git tag: git tag -d v${NEW_VERSION} && git push origin :refs/tags/v${NEW_VERSION}
2. Deploy previous version: git push origin v${PREVIOUS_VERSION}:production
3. Monitor health checks
EOF

echo "✅ Ship report generated"
```

**Report contents:**

- Deployment metadata (version, time, ID, URLs)
- Health check results
- Rollback procedure
- Post-deployment monitoring plan
  </step_6_generate_ship_report>

<step_7_monitor_post_deploy>
**7. Monitor Post-Deployment**

Watch production for 15-30 minutes after deployment:

```bash
echo "Monitoring production (15-30 minutes)..."
echo "Watch for:"
echo "  - Error rate spikes"
echo "  - Performance degradation"
echo "  - User reports/support tickets"
echo "  - Background job failures"

# Monitor logs (varies by platform)
# - Vercel: vercel logs --follow
# - Heroku: heroku logs --tail
# - AWS: CloudWatch logs
# - Netlify: Netlify UI

echo "Monitor dashboard: https://monitoring.example.com/dashboard"
```

**Monitoring checklist:**

- [ ] Error rates normal (<1% increase)
- [ ] Response times acceptable (<10% degradation)
- [ ] No critical alerts triggered
- [ ] Background jobs processing normally
- [ ] No user-reported issues in first 30 minutes

**If issues detected:**

1. Assess severity (critical vs minor)
2. Initiate rollback if critical
3. Apply hotfix if minor and fixable quickly
4. Document incident for post-mortem
   </step_7_monitor_post_deploy>
   </workflow>

<anti_patterns>
**Avoid these production deployment mistakes:**

<pitfall name="deploy_without_staging_validation">
**❌ Deploying to production before staging validation**
```bash
# BAD: Skip staging validation
/ship-prod  # Staging not validated yet
```
**✅ Always verify staging validation approved**
```bash
# GOOD: Check workflow state first
grep -A2 "staging_validation:" state.yaml
# Ensure status: approved before proceeding
```
**Impact**: Untested code reaches production, high risk of incidents
</pitfall>

<pitfall name="missing_rollback_verification">
**❌ Not verifying rollback procedure before deploy**
```bash
# BAD: Deploy without testing rollback
git push origin main:production
# Hope rollback works if needed
```
**✅ Verify rollback gate passed**
```bash
# GOOD: Ensure rollback tested on staging
grep -A2 "rollback:" state.yaml | grep "status: passed"
# Confidence that rollback works if needed
```
**Impact**: Unable to recover quickly if deployment fails
</pitfall>

<pitfall name="insufficient_health_checks">
**❌ Deploying without comprehensive health checks**
```bash
# BAD: Only check homepage
curl https://production.example.com/  # 200 OK, ship it!
```
**✅ Check all critical endpoints and services**
```bash
# GOOD: Verify API, database, cache, background jobs
curl /health && curl /api/status && check-db && check-redis
```
**Impact**: Silent failures in critical services not detected
</pitfall>

<pitfall name="no_post_deploy_monitoring">
**❌ Deploying and immediately moving to next task**
```bash
# BAD: Deploy and forget
git push origin production
# Move on to next feature immediately
```
**✅ Monitor production for 15-30 minutes after deploy**
```bash
# GOOD: Watch logs and metrics
vercel logs --follow &
watch -n 10 'curl -s https://production.example.com/health'
# Wait 30 minutes before declaring success
```
**Impact**: Issues discovered hours later instead of minutes
</pitfall>

<pitfall name="wrong_version_bump">
**❌ Using wrong semantic version bump type**
```bash
# BAD: Minor bump for breaking change
npm version minor  # But API contract changed!
```
**✅ Follow semantic versioning strictly**
```bash
# GOOD: Major bump for breaking changes
# Breaking change in API → major bump
npm version major -m "chore: bump to %s (breaking: API v2)"
```
**Impact**: Users experience unexpected breaking changes
</pitfall>

<pitfall name="missing_git_tag">
**❌ Deploying without creating git release tag**
```bash
# BAD: Just push to production branch
git push origin main:production
# No tag created for version tracking
```
**✅ Always create annotated tag before deploy**
```bash
# GOOD: Tag first, then deploy
git tag -a "v2.7.0" -m "Release v2.7.0"
git push origin v2.7.0
git push origin main:production
```
**Impact**: Cannot easily track what code is in production, rollback difficult
</pitfall>
</anti_patterns>

<success_criteria>
**Production deployment successful when:**

- ✓ Staging validation approved (state.yaml verified)
- ✓ Rollback gate passed (confidence in recovery procedure)
- ✓ Version bumped correctly (semantic versioning followed)
- ✓ Git tag created and pushed (v${VERSION} format)
- ✓ Production deployment triggered and completed
- ✓ Health checks passing (all critical services operational)
- ✓ Ship report generated (production-ship-report.md created)
- ✓ Post-deployment monitoring complete (15-30 minutes, no issues)
- ✓ Release URL accessible (GitHub release created)
- ✓ Deployment metadata recorded (ID, URLs, timestamps)

**Quality gates passed:**

- No critical errors in first 30 minutes
- Error rate <1% increase from baseline
- Response times <10% degradation
- No user-reported critical issues
- All background jobs processing normally
  </success_criteria>
