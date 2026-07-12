---
name: 057-design-feature-toggles
description: Use when designing, implementing, reviewing, testing, or cleaning up feature toggles, feature flags, kill switches, runtime configuration gates, canary controls, staged rollouts, experiments, or temporary compatibility switches in Java enterprise systems. This should trigger for requests such as Design a feature toggle strategy; Review this feature flag; Add a kill switch safely; Test toggle on and off paths; Clean up an expired feature toggle; Plan controlled rollout and rollback behavior. Part of Plinth Toolkit
license: Apache-2.0
metadata:
  author: Juan Antonio Breña Moral, Sangwon Park
  version: 0.17.0
---
# Feature Toggles Design

Guide Java Enterprise developers through safe feature toggle design and lifecycle management. **This is an interactive SKILL**.

**What is covered in this Skill?**

- Deciding when a feature toggle is appropriate versus a branch, configuration change, deployment change, or parallel change
- Classifying release toggles, operational kill switches, experiment toggles, permission toggles, and migration toggles
- Designing typed toggle ownership, defaults, evaluation scope, fallback behavior, observability, and rollback controls
- Implementing toggles in Java services without scattering flag checks or creating hidden long-term complexity
- Reviewing toggles for release, rollback, security, privacy, concurrency, and maintenance risk
- Testing both enabled and disabled paths, configuration failure behavior, rollout rules, and cleanup readiness

## Constraints

Use feature toggles as explicit, owned runtime control points rather than hidden conditional complexity.

- **MUST** read `references/057-design-feature-toggles.md` before applying feature toggle guidance
- **MUST** classify the toggle type, owner, expected lifetime, default state, rollout audience, and removal trigger before recommending implementation
- **MUST** design safe defaults, fallback behavior, observability, and rollback behavior for runtime evaluation failures
- **MUST** keep toggle evaluation centralized, typed, and testable instead of scattering raw configuration lookups through business logic
- **MUST** include cleanup expectations for temporary toggles before implementation is considered complete
- **MUST NOT** use feature toggles to hide incomplete design decisions, weaken security controls, or leave permanent branches without explicit ownership

## When to use this skill

- Design a feature toggle strategy
- Review this feature flag implementation
- Add a kill switch safely
- Plan a canary or staged rollout in a Java service
- Test toggle on and off paths
- Clean up an expired feature toggle
- Decide whether this runtime behavior change needs a toggle

## Workflow

1. **Classify the Toggle Need**

Read `references/057-design-feature-toggles.md`, then identify the runtime behavior change, rollout risk, rollback expectation, affected users, operational owner, and whether a feature toggle is the smallest safe control mechanism.

2. **Design the Toggle Contract**

Define the toggle type, stable name, typed decision API, default state, evaluation context, fallback behavior, audit needs, metrics, logs, and cleanup trigger. Prefer one decision point per behavior over repeated raw flag checks.

3. **Plan Implementation Boundaries**

Place toggle evaluation near an application service, adapter, strategy selector, or request boundary. Keep domain code explicit, avoid secret or personal data in rules, and preserve consistent decisions across a request, transaction, message, or batch item.

4. **Review Release and Rollback Safety**

Check whether disabled behavior preserves the current production contract, enabled behavior has rollout guardrails, operational teams can disable the behavior quickly, and cleanup will not break old deployments, data, or integrations.

5. **Test and Observe Both Paths**

Test disabled, enabled, fallback, configuration failure, rollout targeting, and cleanup scenarios. Add metrics, logs, alerts, or dashboards that show toggle state, decision volume, error rate, latency impact, and kill-switch activation.

6. **Report the Toggle Plan**

Report the decision, toggle contract, implementation boundary, test matrix, observability plan, rollout and rollback steps, cleanup owner, removal trigger, skipped checks, and remaining risks.

## Reference

For detailed guidance, examples, and constraints, see [references/057-design-feature-toggles.md](references/057-design-feature-toggles.md).
