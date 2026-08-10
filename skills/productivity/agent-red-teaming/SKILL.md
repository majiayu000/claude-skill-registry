---
name: agent-red-teaming
description: Plan, execute, document, and retest authorized security assessments of AI agents and multi-agent workflows using safe adversarial cases, synthetic identities, canaries, and evidence-based findings. Use when defining red-team rules of engagement, assessing prompt injection or excessive agency, testing tool and identity boundaries, evaluating memory or cross-agent attacks, scoring a campaign, or verifying remediation in an approved environment.
---

# Agent Red Teaming

Find exploitable control failures without creating uncontrolled harm. Treat written authorization and rules of engagement as prerequisites for execution, not paperwork to complete afterward.

## Inputs

Collect:

- Named target owner and explicit authorization for the exact systems to be tested
- Target identifiers, environment, accounts, endpoints, models, versions, and a reproducible configuration digest
- Start/end time, tester identities, source addresses, rate and cost limits, and emergency contact
- In-scope objectives and out-of-scope systems, tenants, data, techniques, and effects
- Agent architecture, tools, privileges, memory, retrieval, handoffs, identities, and external integrations
- Protected assets, security requirements, prior incidents, existing controls, and expected benign tasks
- Approved synthetic data, canary values, test destinations, cleanup plan, and evidence-handling rules

If target-specific authorization or scope is missing, stop at a non-executable assessment plan. Do not probe a live target to infer scope.

## Output contract

Deliver:

1. Signed-off or explicitly pending rules of engagement with scope, constraints, stop conditions, contacts, and cleanup duties
2. A system and privilege map plus prioritized threat hypotheses
3. A machine-readable, owner-approved campaign plan with unique case IDs, targets, environment, configuration digest, tester subjects, authorization reference, time window, limits, stop conditions, cleanup duties, protected invariants, and safe oracles
4. Execution records tied to an approved case ID and unique test ID, with matching target/configuration, timestamps, observed limits, structured evidence, and cleanup traceability
5. Deduplicated findings with reproducibility, evidence, impact, likelihood, preconditions, root control failure, and remediation
6. Plan-denominator campaign metrics that distinguish passes, failures, blocked cases, errors, missing records, and tests not run
7. Retest results, residual risk, cleanup confirmation, and any incident or scope deviation

Use [assets/campaign-plan-template.md](assets/campaign-plan-template.md) for the human-readable working plan and [assets/campaign-plan-template.json](assets/campaign-plan-template.json) for the machine-readable authorization record. Read [references/test-taxonomy.md](references/test-taxonomy.md) when selecting cases. Validate and summarize JSONL results against the approved JSON plan with `score_campaign.py PLAN.json RESULTS.jsonl`.

## Workflow

### 1. Establish rules of engagement

Verify owner, authority, authorization reference, exact targets, environment, configuration digest, tester subjects, time window, allowed techniques, prohibited actions, rate/cost ceilings, data-handling requirements, stop conditions, emergency contact, and cleanup owner. Separate production from staging explicitly. Mark each case `approved: true` only after the owner-approved plan contains it.

Use unique synthetic accounts and inert destinations. Define benign canary values that are recognizable but grant no access. Confirm how to disable tools, revoke test credentials, restore fixtures, and report an unexpected effect before testing begins.

### 2. Map the attack surface and authority

Trace every path through user input, system instructions, retrieval, memory, tools, code execution, browsers, MCP or plugins, other agents, human approvals, and output sinks. Build a privilege graph showing identities, scopes, tenants, objects, networks, and delegation.

Prioritize hypotheses by credible impact and exposed authority, not novelty. Write each hypothesis as: attacker-controlled source + control weakness + attempted action + observable safe oracle.

### 3. Build a safe test matrix

Cover relevant categories:

- Direct, indirect, stored, encoded, and multimodal instruction attacks
- Tool misuse, target substitution, excessive agency, unsafe chaining, and external effects
- Authentication, authorization, tenant isolation, approval binding, and confused-deputy paths
- Sensitive-data disclosure, output handling, egress, and canary exposure
- Memory, RAG, training-data, configuration, tool-metadata, and dependency poisoning
- Cross-agent impersonation, delegation escalation, tainted summaries, and cascading failure
- Resource exhaustion and cost amplification within strict budgets
- Monitoring, containment, credential revocation, and recovery

Include benign controls and normal tasks to measure false positives and retained utility. Use one primary variable per case where possible. Avoid weaponized payloads when an inert instruction, fake secret, or mock tool proves the same control failure.

### 4. Execute incrementally

Begin with offline or mocked components, then staging, then any separately authorized higher-risk environment. Run low-impact cases first. Capture campaign and authorization references, approved case ID, unique test ID, tester subject, target and environment, configuration digest, start/end/record timestamps, input provenance, tool trace, policy decisions, observed rate/cost/time, result, structured evidence objects, and cleanup status.

Respect rate, cost, and time limits. Do not evade monitoring or controls outside the approved hypothesis. Pause after any unexpected cross-tenant access, real secret, external effect, service degradation, or scope ambiguity.

### 5. Triage findings

Reproduce safely, then distinguish:

- A confirmed invariant violation
- A blocked attack showing the expected control
- A test harness or environment error
- An observation needing more evidence

Rate severity from demonstrated impact, likelihood, prerequisites, affected scope, detectability, and reversibility. Do not rate from prompt wording alone. A pass requires the protected invariant to hold; a failure requires it not to hold and cannot be informational. Blocked, errored, and not-run records have no invariant verdict and no finding severity. Deduplicate findings by root control failure and retain affected variants as evidence.

For every finding, provide the minimum safe reproduction, expected versus observed behavior, evidence, affected configuration, immediate containment, durable remediation, detection opportunity, and a regression case.

### 6. Remediate and retest

Prefer architectural fixes: reduce privilege, enforce authorization outside the model, constrain tools and egress, isolate untrusted content, validate outputs, bind approvals, and protect memory provenance. Prompts and detectors may add defense in depth but should not be the sole fix for consequential effects.

Retest the original case, close variants, and representative benign tasks. Record whether the finding is fixed, partially mitigated, accepted, transferred, or open, with owner and evidence.

### 7. Close and recover

Remove synthetic records, restore approved fixtures, disable test endpoints, revoke test credentials, and confirm no jobs or callbacks remain. Preserve evidence according to retention policy and delete unnecessary sensitive copies.

If testing causes an unexpected effect, stop, notify the emergency contact, contain access, preserve redacted evidence, support restoration, and document the scope deviation. Incident response takes precedence over campaign completion.

## Authorization and safety boundaries

- Execute tests only against named targets for which the user or designated owner has explicit authority; public reachability is not permission.
- Do not test production, third parties, other tenants, employees, or real users unless each is explicitly included in approved rules of engagement.
- Do not use real secrets, personal data, malware, persistence, destructive actions, uncontrolled propagation, social engineering, denial of service, or real transactions when synthetic or inert proof is sufficient.
- Do not bypass rate/cost ceilings or continue after a stop condition.
- Do not publish vulnerabilities, evidence, system prompts, or sensitive architecture without the owner's disclosure authorization.
- Keep finding evidence minimal, access-controlled, redacted, and traceable.
- If authorization cannot be verified, produce planning, threat modeling, and non-executable test designs only.

## Verification

Before reporting completion, confirm:

- Every submitted result maps to an approved campaign-plan case ID, authorization reference, target, environment, configuration digest, time window, and tester identity
- The test matrix covers exposed privilege and highest-impact credible paths
- Each result has an observable oracle and evidence, not only a model judgment
- Findings reproduce on the recorded configuration and have a regression case
- Benign-task utility and false positives were measured alongside attack cases
- Blocked, errored, missing, and unrun cases are not counted as passes or observed coverage
- Retests cover both the original finding and nearby variants
- Cleanup, credential revocation, and unexpected-effect checks are complete

Use `score_campaign.py` to summarize results against the approved plan. Its percentages use all approved case IDs as the denominator, not only submitted records. Treat structural errors and severity/invariant inconsistencies as failed validation. Do not substitute its weighted score for professional impact analysis or present any summary as proof of security, campaign success, or certification.

## Realistic examples

### Internal support agent assessment

In an isolated tenant, test whether a synthetic customer email can make the agent read another synthetic tenant, alter a refund destination, reveal a fake API token, or send to an unapproved domain. Use a mock refund tool and sink mailbox. Verify object-level authorization, approval binding, egress controls, canary alerts, and normal ticket triage.

### Multi-agent release workflow

Test whether a tainted issue description can escalate from planner to coding agent to deployment agent, expand the tool allowlist, change the repository or environment target, or reuse an expired approval. Use a disposable repository and no live cloud credentials. Retest with structured handoffs, per-agent identities, exact-action approvals, and a restricted deployment mock.

## Completion check

Finish only when executed work is authorized and traceable to approved case IDs, high-risk paths have structured safe evidence, finding severity agrees with the observed invariant, remediation is retested, benign utility is measured, limits and cleanup are evidenced, and residual, missing, or untested risk is explicit. Never declare the target secure or certified from campaign results.
