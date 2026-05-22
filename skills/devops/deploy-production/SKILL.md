---
name: deploy-production
description: "Deploy to production environments with safety checks. Use when releasing code to production. Not for staging deploys or local builds unless specifically requested."
disable-model-invocation: true
user-invocable: true
context: fork
agent: Plan
allowed-tools: Read, Bash(docker:*), Bash(kubectl:*)
---

# Deploy to Production

<mission_control>
<objective>Deploy application to production with comprehensive safety checks and emergency rollback capability</objective>
<success_criteria>Deployment succeeds with zero downtime, all health checks pass, rollback procedure documented and tested</success_criteria>
</mission_control>

<safety_gate type="blocking" phase="pre_deployment">
<purpose>Prevent deployment if ANY check fails. These are non-negotiable requirements.</purpose>

<checks>
- <check id="tests_pass">
  <command>npm test</command>
  <expected>Exit code 0, all tests pass</expected>
  <failure_mode>BLOCK deployment</failure_mode>
  </check>

- <check id="code_review">
  <requirement>Recent commits reviewed and approved</requirement>
  <verification>Check PR approval status in git log</verification>
  <failure_mode>BLOCK deployment</failure_mode>
  </check>

- <check id="migrations_tested">
  <requirement>Database migrations tested in staging</requirement>
  <verification>Run migrations on staging database</verification>
  <failure_mode>BLOCK deployment</failure_mode>
  </check>

- <check id="backups_current">
  <requirement>Backups current and tested (within 24h)</requirement>
  <verification>Check backup timestamp and restore test log</verification>
  <failure_mode>BLOCK deployment</failure_mode>
  </check>

- <check id="deployment_plan">
  <requirement>Deployment plan documented in runbook</requirement>
  <verification>Review docs/deployments/YYYY-MM-DD-plan.md</verification>
  <failure_mode>BLOCK deployment</failure_mode>
  </check>

- <check id="rollback_ready">
  <requirement>Rollback procedure prepared and tested</requirement>
  <verification>Confirm rollback script exists and was tested</verification>
  <failure_mode>BLOCK deployment</failure_mode>
  </check>

- <check id="monitoring_configured">
  <requirement>Monitoring and alerting configured for new deployment</requirement>
  <verification>Verify alerts exist in monitoring system</verification>
  <failure_mode>BLOCK deployment</failure_mode>
  </check>

- <check id="team_notified">
    <requirement>Team notified of deployment window</requirement>
    <verification>Check deployment calendar or Slack announcement</verification>
    <failure_mode>BLOCK deployment</failure_mode>
    </check>
  </checks>

<gate_validation>
MANDATORY: Run each check sequentially. If ANY check fails, STOP and resolve before continuing.
DO NOT PROCEED unless ALL items are verified.
</gate_validation>
</safety_gate>

## Deployment Process

<logic_flow>
digraph Deployment {
rankdir=TD;
node [shape=box];
Verify [label="1. Verify Checklist"];
Build [label="2. Build & Test"];
Docker [label="3. Build Docker"];
Push [label="4. Push Registry"];
Deploy [label="5. Apply K8s"];
Check [label="6. Verify Health"];
Success [label="Deployment Success" style=filled fillcolor=lightgreen];
Rollback [label="Rollback Procedure" style=filled fillcolor=lightpink];

    Verify -> Build;
    Build -> Docker;
    Docker -> Push;
    Push -> Deploy;
    Deploy -> Check;
    Check -> Success [label="Health OK"];
    Check -> Rollback [label="Errors"];
    Rollback -> Verify [label="Fix & Retry"];

}
</logic_flow>

### 1. Pre-Deployment Verification

Complete the checklist above and verify all systems are ready.

### 2. Build Application

```bash
npm run build
npm test
```

### 3. Build Docker Image

```bash
docker build -t myapp:$VERSION .
docker tag myapp:$VERSION myapp:latest
```

### 4. Push to Registry

```bash
docker push myapp:$VERSION
docker push myapp:latest
```

### 5. Deploy to Kubernetes

```bash
kubectl apply -f manifests/production/
kubectl rollout status deployment/myapp
```

### 6. Verify Deployment

- [ ] Health checks passing
- [ ] Logs show no errors
- [ ] Metrics within normal range
- [ ] Smoke tests pass

### 7. Post-Deployment

- [ ] Update documentation
- [ ] Notify team of successful deployment
- [ ] Monitor for 30 minutes
- [ ] Update deployment tracker

## Safety Features

This skill includes:

- **Manual-only invocation** - Cannot be auto-triggered
- **XML-defined safety gates** - Blocking checks with machine-readable validation
- **Emergency rollback** - Automated rollback procedure in XML
- **Verification steps** - Ensures deployment success

## Rollback Procedure

<rollback_procedure>
<purpose>Emergency rollback when deployment fails or health checks fail</purpose>
<trigger_conditions>

- <condition>Health checks fail after 5 minutes</condition>
- <condition>Error rate exceeds 5% for 2 minutes</condition>
- <condition>Manual abort triggered</condition>
- <condition>Database migration failures</condition>
  </trigger_conditions>

<steps sequential="true">
<step id="1" action="immediate_rollback">
<command>kubectl rollout undo deployment/myapp</command>
<timeout>30 seconds</timeout>
<expected>Rollback initiated, previous version restored</expected>
</step>

<step id="2" action="verify_rollback">
<command>kubectl rollout status deployment/myapp</command>
<timeout>120 seconds</timeout>
<expected>Rollback complete, deployment healthy</expected>
</step>

<step id="3" action="investigate_root_cause">
<investigation>
- Check logs: `kubectl logs -f deployment/myapp --tail=100`
- Review metrics: Error rates, latency, CPU/memory
- Identify: What changed, why it failed
- Document: Create incident report
</investigation>
</step>

<step id="4" action="prepare_fix">
<actions>
- Fix the issue in code
- Test in staging environment
- Update deployment plan with lessons learned
- Get approval for re-deployment
</actions>
</step>

<step id="5" action="redeploy">
<actions>
- Follow full deployment process again
- All safety gates MUST pass
- Enhanced monitoring for first hour
</actions>
</step>
</steps>
</rollback_procedure>

## Integration

This skill integrates with:

- `ci-pipeline-manager` - CI/CD pipeline integration
- `backend-patterns` - Deployment best practices

---

## Absolute Constraints (Non-Negotiable)

<critical_constraint>
**MANDATORY: ALL safety gates MUST pass before deployment**

- Run each check sequentially
- If ANY check fails, STOP and resolve
- NO exceptions, NO "looks good" rationalization
- Document why gate failed and how it was fixed

**MANDATORY: Rollback procedure MUST be tested before deployment**

- Verify rollback script exists
- Test rollback in staging
- Confirm previous version is stable
- Document rollback success criteria

**MANDATORY: Monitor deployment for 30 minutes after success**

- Health checks must remain passing
- Error rates must stay below threshold
- Logs must show no errors
- Team must be available for immediate response

**MANDATORY: Document ALL deployments**

- Update deployment tracker
- Document any issues or deviations
- Create incident report if rollback occurred
- Share lessons learned with team

**DANGER ZONE: Production deployment is irreversible without rollback**

- Treat every deployment as potentially breaking
- Assume rollback will be needed (hope for best, prepare for worst)
- Never deploy Friday afternoon or before holidays
- Always have team on standby during deployment window

**No exceptions. No short-cuts. Production is not a place for "good enough."**
</critical_constraint>

---

## Genetic Code

This component carries essential Seed System principles for context: fork isolation:

<critical_constraint>
MANDATORY: All components MUST be self-contained (zero .claude/rules dependency)
MANDATORY: Achieve 80-95% autonomy (0-5 AskUserQuestion rounds per session)
MANDATORY: Description MUST use What-When-Not format in third person
MANDATORY: No component references another component by name in description
MANDATORY: Progressive disclosure - references/ for detailed content
MANDATORY: Use XML for control (mission_control, critical_constraint), Markdown for data
No exceptions. Portability invariant must be maintained.
</critical_constraint>

**Delta Standard**: Good Component = Expert Knowledge − What Claude Already Knows

**Recognition Questions**:

- "Would Claude know this without being told?" → Delete (zero delta)
- "Can this work standalone?" → Fix if no (non-self-sufficient)
- "Did I read the actual file, or just see it in grep?" → Verify before claiming

---
