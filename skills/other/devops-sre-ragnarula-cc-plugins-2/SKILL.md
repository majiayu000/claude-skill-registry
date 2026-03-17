---
name: devops-sre
description: Use this skill when designing or reviewing CI/CD pipelines, deployment strategies, observability systems, incident response, or any system involving production operations and reliability. Applies operational thinking to specifications, designs, and implementations.
version: 0.1.0
---

# DevOps & SRE Engineering

## When to Apply

Use this skill when the system involves:
- CI/CD pipelines and deployment automation
- Production deployments and rollback strategies
- Monitoring, alerting, and observability
- Incident response and on-call procedures
- SLOs, SLIs, and error budgets
- Capacity planning and performance management

## Mindset

DevOps/SRE engineers think about the entire lifecycle from commit to production and beyond.

**Questions to always ask:**
- How do we deploy this safely? How do we roll back?
- How do we know it's working? What do we alert on?
- What's the SLO? What happens when we miss it?
- How do we debug this in production?
- What's the on-call burden? Is this operable at 3am?
- How do we handle traffic spikes? Gradual degradation?
- What's the blast radius of a bad deploy?

**Assumptions to challenge:**
- "It works on my machine" - Production is different. Test in production-like environments.
- "We'll monitor it later" - If you can't observe it, you can't operate it.
- "Deploys are safe" - Any change can break things. Deploy progressively.
- "More alerts are better" - Alert fatigue is real. Alert on symptoms, not causes.
- "We'll scale when needed" - Know your limits before you hit them.
- "Rollback is easy" - Is it? Have you tested it? What about data migrations?

## Practices

### CI/CD Pipeline
Automate everything from commit to deploy. Fast feedback loops (< 10 min to know if broken). Reproducible builds. Immutable artifacts. **Don't** have manual steps in the pipeline, slow feedback loops, or build differently for different environments.

### Deployment Strategy
Use progressive rollouts (canary, blue-green, rolling). Define rollback triggers and automate rollback. Separate deploy from release (feature flags). **Don't** deploy 100% immediately, rely on manual rollback, or couple deploy with feature enablement.

### Observability
Instrument the four golden signals: latency, traffic, errors, saturation. Use structured logging with correlation IDs. Implement distributed tracing. **Don't** rely on logs alone, use unstructured logs, or skip tracing in distributed systems.

### Alerting
Alert on symptoms (SLO breach), not causes. Page only for actionable, urgent issues. Route non-urgent to tickets. Include runbook links in alerts. **Don't** alert on every metric, page for non-actionable issues, or have alerts without runbooks.

### SLOs & Error Budgets
Define SLOs based on user experience. Measure SLIs accurately. Use error budget to balance velocity and reliability. **Don't** set arbitrary SLOs, measure proxies instead of user experience, or ignore error budget burn.

### Incident Response
Have clear escalation paths. Blameless postmortems. Document incidents and learnings. Practice incident response regularly. **Don't** blame individuals, skip postmortems, or let learnings rot in docs.

### Runbooks
Document common operational tasks. Include debugging steps for known failure modes. Keep runbooks next to alerts. **Don't** rely on tribal knowledge, write runbooks that assume context, or let runbooks go stale.

### Capacity Planning
Know your limits before you hit them. Load test regularly. Plan for peak, not average. Have scaling playbooks ready. **Don't** discover limits in production, test with unrealistic load, or assume linear scaling.

## Vocabulary

Use precise terminology:

| Instead of | Say |
|------------|-----|
| "reliable" | "99.9% availability SLO" / "< 1% error rate" |
| "monitored" | "SLI dashboards" / "alerting on p99 > 500ms" |
| "deployed" | "canary at 5%" / "blue-green with instant rollback" |
| "fast deploys" | "< 15 min commit-to-prod" / "10 deploys/day" |
| "observable" | "traces, metrics, structured logs with correlation" |
| "on-call" | "PagerDuty rotation" / "< 5 pages/week" |

## SDD Integration

**During Specification:**
- Define SLOs based on user-facing requirements
- Identify operational requirements (deployment frequency, rollback needs)
- Clarify observability requirements
- Establish on-call expectations

**During Design:**
- Design for observability from the start
- Specify deployment strategy and rollback approach
- Document what metrics/logs/traces each component emits
- Plan for graceful degradation
- Identify what runbooks will be needed

**During Review:**
- Verify observability is instrumented
- Check deployment strategy is progressive
- Confirm rollback is automated and tested
- Validate alerts are actionable with runbooks
- Ensure SLIs actually measure SLOs
