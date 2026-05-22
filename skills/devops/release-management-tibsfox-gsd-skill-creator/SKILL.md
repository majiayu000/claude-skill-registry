---
name: release-management
description: Provides release management strategies including deployment patterns, version control, and rollback procedures. Use when planning releases, managing deployments, or when user mentions 'release', 'canary', 'blue-green', 'rollback', 'feature flag', 'release train', 'semantic versioning', 'changelog', 'migration'.
---

# Release Management

Best practices for shipping software reliably through structured release processes, deployment strategies, and rollback automation.

## Deployment Strategy Comparison

Choosing the right deployment strategy depends on risk tolerance, infrastructure budget, and rollback requirements.

| Strategy | Zero Downtime | Rollback Speed | Infrastructure Cost | Complexity | Best For |
|----------|--------------|----------------|--------------------:|------------|----------|
| Blue-Green | Yes | Instant (switch) | 2x | Medium | Critical services, compliance |
| Canary | Yes | Fast (route away) | 1.05-1.5x | High | High-traffic user-facing apps |
| Rolling | Yes | Slow (re-deploy) | 1x | Low | Stateless microservices |
| Recreate | No (brief outage) | Slow (re-deploy) | 1x | Low | Dev/staging, batch jobs |
| A/B Testing | Yes | Fast (route away) | 1.2-1.5x | High | Feature experimentation |
| Shadow/Dark | Yes | N/A (no user impact) | 1.5-2x | Very High | ML models, data pipelines |

### Decision Matrix

```
Is the service stateful?
  YES --> Can you afford 2x infrastructure?
            YES --> Blue-Green
            NO  --> Rolling (with drain + health checks)
  NO  --> Is it high-traffic (>1000 rps)?
            YES --> Canary (gradual rollout)
            NO  --> Rolling (simple, cost-effective)
```

## Canary Deployment Configuration

### Kubernetes Canary with Argo Rollouts

```yaml
# argo-rollout.yaml -- Progressive canary with automated analysis
apiVersion: argoproj.io/v1alpha1
kind: Rollout
metadata:
  name: payment-service
  namespace: production
spec:
  replicas: 10
  revisionHistoryLimit: 3
  selector:
    matchLabels:
      app: payment-service
  strategy:
    canary:
      # Canary traffic steps with pause for analysis
      steps:
        - setWeight: 5
        - pause: { duration: 5m }    # 5% for 5 minutes
        - analysis:
            templates:
              - templateName: canary-success-rate
            args:
              - name: service-name
                value: payment-service
        - setWeight: 20
        - pause: { duration: 10m }   # 20% for 10 minutes
        - analysis:
            templates:
              - templateName: canary-success-rate
        - setWeight: 50
        - pause: { duration: 10m }   # 50% for 10 minutes
        - setWeight: 80
        - pause: { duration: 5m }    # 80% for 5 minutes
        # 100% happens automatically after final step

      # Auto-rollback on failure
      abortScaleDownDelaySeconds: 30
      dynamicStableScale: true

      # Traffic management via Istio
      trafficRouting:
        istio:
          virtualServices:
            - name: payment-service-vsvc
              routes:
                - primary
          destinationRule:
            name: payment-service-destrule
            canarySubsetName: canary
            stableSubsetName: stable

      # Analysis template for canary health
      analysis:
        templates:
          - templateName: canary-success-rate
        startingStep: 2
        args:
          - name: service-name
            value: payment-service

  template:
    metadata:
      labels:
        app: payment-service
    spec:
      containers:
        - name: payment-service
          image: registry.example.com/payment-service:v2.3.1
          ports:
            - containerPort: 8080
          readinessProbe:
            httpGet:
              path: /healthz
              port: 8080
            initialDelaySeconds: 5
            periodSeconds: 10
          resources:
            requests:
              cpu: 250m
              memory: 256Mi
            limits:
              cpu: 500m
              memory: 512Mi

---
# Analysis template -- Prometheus-based success rate check
apiVersion: argoproj.io/v1alpha1
kind: AnalysisTemplate
metadata:
  name: canary-success-rate
spec:
  args:
    - name: service-name
  metrics:
    - name: success-rate
      interval: 60s
      count: 5
      successCondition: result[0] >= 0.99
      failureLimit: 2
      provider:
        prometheus:
          address: http://prometheus.monitoring:9090
          query: |
            sum(rate(http_requests_total{
              service="{{args.service-name}}",
              status=~"2..",
              canary="true"
            }[2m])) /
            sum(rate(http_requests_total{
              service="{{args.service-name}}",
              canary="true"
            }[2m]))
    - name: p99-latency
      interval: 60s
      count: 5
      successCondition: result[0] <= 500
      failureLimit: 2
      provider:
        prometheus:
          address: http://prometheus.monitoring:9090
          query: |
            histogram_quantile(0.99,
              sum(rate(http_request_duration_ms_bucket{
                service="{{args.service-name}}",
                canary="true"
              }[2m])) by (le)
            )
```

## Feature Flag Implementation

### LaunchDarkly Pattern with Gradual Rollout

```typescript
// feature-flags.ts -- Structured feature flag management
import * as LaunchDarkly from "@launchdarkly/node-server-sdk";

// --- Flag Configuration Types ---

interface FlagConfig {
  key: string;
  description: string;
  type: "boolean" | "multivariate" | "percentage";
  owner: string;           // Team responsible
  createdAt: string;       // For cleanup tracking
  maxAge: string;          // Expected lifetime: "temporary" | "permanent"
  cleanupTicket?: string;  // JIRA ticket to remove flag
}

// Registry prevents flag sprawl -- all flags must be declared
const FLAG_REGISTRY: Record<string, FlagConfig> = {
  "new-checkout-flow": {
    key: "new-checkout-flow",
    description: "Redesigned checkout with one-page form",
    type: "percentage",
    owner: "checkout-team",
    createdAt: "2025-11-01",
    maxAge: "temporary",
    cleanupTicket: "CHECKOUT-1234",
  },
  "payment-v2-api": {
    key: "payment-v2-api",
    description: "Route payments through v2 processor",
    type: "boolean",
    owner: "payments-team",
    createdAt: "2025-10-15",
    maxAge: "temporary",
    cleanupTicket: "PAY-567",
  },
};

// --- Client Initialization ---

let ldClient: LaunchDarkly.LDClient;

export async function initFeatureFlags(): Promise<void> {
  ldClient = LaunchDarkly.init(process.env.LAUNCHDARKLY_SDK_KEY!);

  await ldClient.waitForInitialization({ timeout: 10 });
  console.log("LaunchDarkly client initialized");
}

// --- Flag Evaluation with Fallback ---

export async function isEnabled(
  flagKey: string,
  context: LaunchDarkly.LDContext,
  defaultValue = false
): Promise<boolean> {
  // Validate flag is registered
  if (!FLAG_REGISTRY[flagKey]) {
    console.warn(`Unknown flag: ${flagKey}. Returning default.`);
    return defaultValue;
  }

  try {
    const value = await ldClient.variation(flagKey, context, defaultValue);
    return Boolean(value);
  } catch (err) {
    // Flag evaluation failure should never break the app
    console.error(`Flag evaluation failed for ${flagKey}:`, err);
    return defaultValue;
  }
}

// --- Usage in Route Handler ---

export async function checkoutHandler(req: Request, res: Response) {
  const userContext: LaunchDarkly.LDContext = {
    kind: "user",
    key: req.user.id,
    email: req.user.email,
    custom: {
      plan: req.user.plan,       // Target by plan tier
      region: req.user.region,   // Target by geography
      company: req.user.orgId,   // Target by organization
    },
  };

  const useNewCheckout = await isEnabled("new-checkout-flow", userContext);

  if (useNewCheckout) {
    return renderNewCheckout(req, res);
  }
  return renderLegacyCheckout(req, res);
}

// --- Stale Flag Detection ---

export function getStaleFlags(maxAgeDays = 90): FlagConfig[] {
  const now = Date.now();
  return Object.values(FLAG_REGISTRY).filter((flag) => {
    if (flag.maxAge === "permanent") return false;
    const age = now - new Date(flag.createdAt).getTime();
    return age > maxAgeDays * 24 * 60 * 60 * 1000;
  });
}
```

## Database Migration Strategy

### Safe Migration Workflow

Database migrations during releases require special care because they cannot be rolled back as easily as code.

| Migration Type | Risk Level | Rollback Strategy | Requires Downtime |
|---------------|-----------|-------------------|-------------------|
| Add column (nullable) | Low | Drop column | No |
| Add column (NOT NULL + default) | Medium | Drop column | No (with care) |
| Drop column | High | Cannot undo | No (expand-contract) |
| Rename column | High | Cannot undo easily | No (expand-contract) |
| Add index | Medium | Drop index | No (CONCURRENTLY) |
| Change column type | High | Revert type | Sometimes |
| Add table | Low | Drop table | No |
| Drop table | Critical | Restore from backup | No |

### Expand-Contract Migration Pattern

```sql
-- Phase 1: EXPAND (deploy with old code still running)
-- Add new column alongside old one
ALTER TABLE users ADD COLUMN email_normalized VARCHAR(255);

-- Backfill data (run as background job, not in migration)
UPDATE users SET email_normalized = LOWER(TRIM(email))
WHERE email_normalized IS NULL
LIMIT 10000;  -- Batch to avoid locking

-- Phase 2: MIGRATE (deploy new code that writes to both columns)
-- Application writes to BOTH email and email_normalized
-- Application reads from email_normalized with fallback to email

-- Phase 3: CONTRACT (after all code uses new column)
-- Only after verifying no code reads the old column
ALTER TABLE users DROP COLUMN email;
ALTER TABLE users RENAME COLUMN email_normalized TO email;
```

### Migration Runner with Safety Checks

```bash
#!/usr/bin/env bash
# migrate.sh -- Safe migration runner with pre-flight checks
set -euo pipefail

DB_NAME="${DB_NAME:?DB_NAME required}"
MIGRATION_DIR="${MIGRATION_DIR:-./migrations}"
DRY_RUN="${DRY_RUN:-false}"

# Pre-flight checks
preflight_check() {
  echo "=== Pre-flight checks ==="

  # 1. Check for pending transactions that could block
  BLOCKED=$(psql -d "$DB_NAME" -t -c \
    "SELECT count(*) FROM pg_stat_activity
     WHERE state = 'idle in transaction'
     AND query_start < now() - interval '5 minutes';")

  if [ "$BLOCKED" -gt 0 ]; then
    echo "ERROR: $BLOCKED long-running idle transactions detected"
    echo "These may block DDL operations. Investigate before proceeding."
    exit 1
  fi

  # 2. Check disk space (migrations can temporarily double table size)
  DISK_FREE=$(df -BG /var/lib/postgresql | tail -1 | awk '{print $4}' | tr -d 'G')
  if [ "$DISK_FREE" -lt 20 ]; then
    echo "ERROR: Only ${DISK_FREE}GB free. Migrations may need more space."
    exit 1
  fi

  # 3. Verify backup is recent (within last hour)
  LAST_BACKUP=$(psql -d "$DB_NAME" -t -c \
    "SELECT pg_last_xact_replay_timestamp();" 2>/dev/null || echo "N/A")
  echo "Last backup/replica sync: $LAST_BACKUP"

  echo "=== Pre-flight passed ==="
}

# Run migrations
run_migrations() {
  for migration in "$MIGRATION_DIR"/*.sql; do
    MIGRATION_NAME=$(basename "$migration")

    # Check if already applied
    APPLIED=$(psql -d "$DB_NAME" -t -c \
      "SELECT count(*) FROM schema_migrations
       WHERE name = '$MIGRATION_NAME';")

    if [ "$APPLIED" -gt 0 ]; then
      echo "SKIP: $MIGRATION_NAME (already applied)"
      continue
    fi

    echo "APPLYING: $MIGRATION_NAME"

    if [ "$DRY_RUN" = "true" ]; then
      echo "  DRY RUN -- would execute:"
      head -20 "$migration"
      continue
    fi

    # Apply with statement timeout to prevent long locks
    psql -d "$DB_NAME" \
      -v ON_ERROR_STOP=1 \
      -c "SET statement_timeout = '30s';" \
      -f "$migration"

    # Record migration
    psql -d "$DB_NAME" -c \
      "INSERT INTO schema_migrations (name, applied_at)
       VALUES ('$MIGRATION_NAME', now());"

    echo "  APPLIED: $MIGRATION_NAME"
  done
}

preflight_check
run_migrations
echo "=== Migrations complete ==="
```

## Rollback Automation

### Automated Rollback Script

```bash
#!/usr/bin/env bash
# rollback.sh -- Automated release rollback with verification
set -euo pipefail

SERVICE="${1:?Usage: rollback.sh <service> [target-version]}"
TARGET_VERSION="${2:-}"  # If empty, rolls back to previous
ENVIRONMENT="${ENVIRONMENT:-production}"
NAMESPACE="${NAMESPACE:-production}"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

log() { echo -e "${GREEN}[ROLLBACK]${NC} $*"; }
warn() { echo -e "${YELLOW}[WARNING]${NC} $*"; }
err() { echo -e "${RED}[ERROR]${NC} $*" >&2; }

# Step 1: Determine rollback target
if [ -z "$TARGET_VERSION" ]; then
  # Get previous revision from Kubernetes
  TARGET_VERSION=$(kubectl rollout history "deployment/$SERVICE" \
    -n "$NAMESPACE" | tail -3 | head -1 | awk '{print $1}')
  log "Auto-detected previous revision: $TARGET_VERSION"
fi

# Step 2: Create rollback record (audit trail)
ROLLBACK_ID="rb-$(date +%Y%m%d-%H%M%S)-${SERVICE}"
log "Rollback ID: $ROLLBACK_ID"

# Step 3: Notify team
curl -s -X POST "$SLACK_WEBHOOK_URL" \
  -H 'Content-Type: application/json' \
  -d "{
    \"text\": \"ROLLBACK INITIATED: ${SERVICE} in ${ENVIRONMENT}\",
    \"blocks\": [{
      \"type\": \"section\",
      \"text\": {
        \"type\": \"mrkdwn\",
        \"text\": \"*Rollback:* ${ROLLBACK_ID}\n*Service:* ${SERVICE}\n*Target:* revision ${TARGET_VERSION}\n*Initiated by:* $(whoami)\"
      }
    }]
  }" 2>/dev/null || warn "Slack notification failed (non-blocking)"

# Step 4: Execute rollback
log "Rolling back $SERVICE to revision $TARGET_VERSION..."
kubectl rollout undo "deployment/$SERVICE" \
  -n "$NAMESPACE" \
  --to-revision="$TARGET_VERSION"

# Step 5: Wait for rollout
log "Waiting for rollback to complete..."
if ! kubectl rollout status "deployment/$SERVICE" \
  -n "$NAMESPACE" --timeout=300s; then
  err "Rollback did not complete within 5 minutes"
  err "Manual intervention required"
  exit 1
fi

# Step 6: Verify health
log "Verifying service health..."
sleep 10  # Allow metrics to settle

HEALTH_URL="https://${SERVICE}.${ENVIRONMENT}.example.com/healthz"
HTTP_STATUS=$(curl -s -o /dev/null -w "%{http_code}" "$HEALTH_URL" || echo "000")

if [ "$HTTP_STATUS" != "200" ]; then
  err "Health check failed: HTTP $HTTP_STATUS"
  err "Service may need manual investigation"
  exit 1
fi

log "Health check passed (HTTP $HTTP_STATUS)"
log "Rollback $ROLLBACK_ID completed successfully"
```

## Release Train Schedule

A release train ships on a fixed cadence regardless of what features are ready. Features that miss the train wait for the next one.

### Cadence Options

| Cadence | Suitable For | Trade-offs |
|---------|-------------|------------|
| Daily | SaaS, internal tools | Fast feedback, high automation needed |
| Weekly | B2B products | Balanced pace, manageable testing |
| Bi-weekly | Regulated industries | More testing time, slower delivery |
| Monthly | Enterprise, on-prem | Maximum stability, slow feedback |

### Weekly Release Train Example

```
Monday    | Feature freeze for this week's release
            Code complete -- all PRs merged to release branch
            Automated regression suite runs

Tuesday   | QA validation day
            Manual exploratory testing on staging
            Performance benchmarks compared to baseline

Wednesday | Release candidate tagged (e.g., v2.4.0-rc.1)
            Deploy to pre-production / canary
            Stakeholder sign-off window opens

Thursday  | Production deploy (canary -> full rollout)
            Monitoring period (4 hours minimum)
            Incident response team on standby

Friday    | Retrospective and metrics review
            Hotfix window (if needed)
            No new releases on Friday afternoon
```

## Semantic Versioning and Changelog Automation

### SemVer Rules

```
MAJOR.MINOR.PATCH (e.g., 2.4.1)

MAJOR: Breaking changes (removed API, changed behavior)
MINOR: New features (backward compatible)
PATCH: Bug fixes (backward compatible)

Pre-release: 2.4.1-beta.1, 2.4.1-rc.1
Build metadata: 2.4.1+build.123
```

| Change Type | Version Bump | Example |
|-------------|-------------|---------|
| Removed endpoint | MAJOR | v2.0.0 -> v3.0.0 |
| Changed response format | MAJOR | v2.0.0 -> v3.0.0 |
| New endpoint added | MINOR | v2.3.0 -> v2.4.0 |
| New optional parameter | MINOR | v2.3.0 -> v2.4.0 |
| Fixed validation bug | PATCH | v2.3.1 -> v2.3.2 |
| Performance improvement | PATCH | v2.3.1 -> v2.3.2 |

### Automated Changelog with Conventional Commits

```yaml
# .github/workflows/release.yml
name: Release

on:
  push:
    branches: [main]

permissions:
  contents: write
  pull-requests: write

jobs:
  release:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0  # Full history for changelog generation

      - uses: googleapis/release-please-action@v4
        id: release
        with:
          release-type: node
          # Conventional Commits -> automatic version bumps
          # feat: -> MINOR
          # fix:  -> PATCH
          # feat!: or BREAKING CHANGE: -> MAJOR

      - if: ${{ steps.release.outputs.release_created }}
        run: |
          echo "Release v${{ steps.release.outputs.major }}.${{ steps.release.outputs.minor }}.${{ steps.release.outputs.patch }} created"
          # Trigger deploy workflow, publish packages, etc.
```

## Release Readiness Review

### Go/No-Go Criteria

| Category | Criteria | Status Check |
|----------|---------|-------------|
| Testing | All CI tests pass on release branch | Automated |
| Testing | No P0/P1 bugs open against release | JIRA query |
| Testing | Performance benchmarks within 10% of baseline | Automated |
| Security | No critical/high vulnerabilities in scan | Automated |
| Security | Dependency audit clean | Automated |
| Operations | Runbook updated for new features | Manual review |
| Operations | Monitoring dashboards cover new endpoints | Manual review |
| Operations | Rollback procedure tested in staging | Manual verification |
| Compliance | Change request approved (if required) | Ticketing system |
| Compliance | Data migration verified on staging data copy | Manual verification |

## Anti-Patterns

| Anti-Pattern | Problem | Fix |
|--------------|---------|-----|
| Friday afternoon deploys | No one available if things break | Deploy early in the week; freeze Friday PM |
| No rollback plan | Stuck with broken release | Always have one-command rollback tested in staging |
| Big-bang releases | Too many changes, impossible to isolate failures | Small, frequent releases behind feature flags |
| Skipping staging | Production becomes the test environment | Always deploy to staging first with same process |
| Manual deployment steps | Human error, inconsistent process | Automate everything; deploy via CI pipeline only |
| Feature flags never cleaned up | Flag spaghetti, dead code, maintenance burden | Set expiry dates; track flags in registry with cleanup tickets |
| Database migration in deploy script | Coupled rollback; can't roll back code without rolling back data | Separate migration pipeline; expand-contract pattern |
| No deploy metrics | Cannot tell if release caused degradation | Compare error rates, latency, throughput before/after |
| Shared staging environment | Teams block each other; dirty state | Per-PR or per-team ephemeral environments |
| Version pinning to latest | Builds break when dependencies update | Pin exact versions; use lockfiles; update deliberately |
| No release notes | Users and support team blindsided by changes | Automate changelog from conventional commits |
| Hotfix bypasses process | Introduces new bugs under pressure | Hotfix follows same pipeline, just expedited |

## Release Readiness Checklist

- [ ] All automated tests pass on the release branch
- [ ] No open P0/P1 bugs targeting this release
- [ ] Performance benchmarks are within acceptable thresholds
- [ ] Security scan shows no critical or high vulnerabilities
- [ ] Database migrations tested on staging with production-like data
- [ ] Rollback procedure tested and documented
- [ ] Feature flags configured for gradual rollout where appropriate
- [ ] Monitoring dashboards and alerts configured for new functionality
- [ ] Changelog and release notes generated and reviewed
- [ ] Stakeholder sign-off obtained (if required)
- [ ] On-call team briefed on release contents and known risks
- [ ] Deploy window scheduled outside peak traffic hours
- [ ] Communication plan ready (status page, customer notification)
- [ ] Post-deploy smoke tests defined and ready to run
