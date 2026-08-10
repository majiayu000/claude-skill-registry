---
name: human-in-the-loop
description: Design and verify auditable human oversight, approval gates, escalation paths, and safe state transitions for AI agent workflows. Use when deciding which agent actions require review, adding approve/reject or dual-control flows, preventing unauthorized autonomous effects, creating decision records, reducing rubber-stamping, or recovering safely from rejected, expired, or failed actions.
---

# Human in the Loop

Place human judgment at the decision point where it changes risk. A confirmation dialog alone is not oversight: bind an authorized decision to an understandable, immutable action and preserve evidence of what happened.

## Inputs

Collect or infer, and label assumptions for:

- Agent goal, workflow states, and every action it can propose or execute
- Effect type, reversibility, value, affected people, and worst credible impact
- Data sensitivity, regulatory or contractual duties, and organizational risk tolerance
- Stable requester and approver subject identities, role assignments, policy owner, separation-of-duties rules, and coverage hours
- Required response time, timeout behavior, escalation contacts, and availability target
- Evidence an approver needs, including provenance, uncertainty, and alternatives
- Existing identity, policy, audit, ticketing, and notification systems
- Failure, retry, cancellation, compensation, and incident paths

Do not invent approver authority or organizational policy. If missing information affects a consequential action, produce a proposed policy and mark it for owner approval.

## Output contract

Deliver:

1. An action inventory and rationale-backed risk tier for each action
2. A gate policy defining validated predicates, eligible approver roles and distinct subjects, quorum, evidence, expiry, timeout, structured escalation, audit-outage behavior, execution-time reauthorization, compensation, break-glass, and separation of duties
3. A state machine for prepare, review, decision, execution, failure, and recovery
4. An approval experience that shows the exact action, material effects, uncertainty, provenance, alternatives, and safe reject/edit paths
5. An append-only decision record schema and retention/redaction requirements
6. Implementation or a file-level plan, plus policy and concurrency tests
7. Verification evidence, unresolved policy decisions, residual risk, and an operational recovery plan

Start from [assets/approval-policy-template.json](assets/approval-policy-template.json) when a machine-readable policy helps. Validate it with [scripts/validate_gate_policy.py](scripts/validate_gate_policy.py). Read [references/gate-design-guide.md](references/gate-design-guide.md) for risk-tier and state-machine guidance.

## Workflow

### 1. Inventory decisions and effects

List each agent action and the object it affects. Separate drafting, previewing, recommending, and reading from committing, sending, publishing, purchasing, deleting, granting access, executing code, or making a high-impact decision.

Record reversibility, scale, sensitivity, external visibility, financial value, time pressure, affected rights, and whether a mistaken action can be contained.

### 2. Assign the lightest sufficient oversight

Choose one control per risk:

- **Autonomous with audit:** bounded, reversible, low-impact actions
- **Notify after action:** low-impact actions where rapid awareness is sufficient
- **Review before action:** consequential or externally visible actions
- **Step-up approval:** value, sensitivity, confidence, anomaly, or scope crosses a threshold
- **Dual control:** critical, irreversible, privileged, or regulated actions; require at least two distinct approver subjects by default
- **Prohibited:** action exceeds policy or cannot be made acceptably safe

Do not gate every trivial step; excess prompts train users to approve reflexively. Never remove a required gate merely to meet a latency target. Treat critical single-control and requester self-approval as invalid by default. Permit either only through a time-bounded waiver that names the gate and exception type, includes the policy owner's stable subject ID and approval reference, documents rationale and compensating controls, and is explicitly referenced by the gate.

### 3. Specify the decision package

Show the approver:

- Plain-language intent and why the gate triggered
- Target identity and normalized parameters
- Before/after diff or exact proposed payload
- Expected effects, affected parties, cost, and reversibility
- Evidence sources, provenance, freshness, uncertainty, and known gaps
- Policy basis, alternatives, and what reject, edit, or timeout will do

Hide secrets and minimize personal data. Make the primary reject/cancel path as usable as approve.

### 4. Bind identity and approval to the action

Authenticate the approver and authorize their role independently of the model. Model roles and stable approver subjects separately so a two-role requirement cannot silently resolve to one person. Create a canonical representation or digest of actor, tenant, action, target, material parameters, policy version, expiry, and nonce. Approval applies only to that immutable proposal.

Invalidate approval after any material edit, expiry, policy change, target change, or relevant state change. Prevent self-approval where separation of duties applies. Do not interpret silence, message receipt, or a generic prior consent as approval.

### 5. Implement a safe state machine

Use explicit transitions such as:

`prepared -> pending_review -> approved | rejected | expired | cancelled`

`approved -> executing -> completed | failed | compensation_pending`

Make transitions atomic and idempotent. Recheck authorization and preconditions immediately before execution. Consume one-time approvals exactly once. Handle concurrent approvers, duplicate callbacks, stale screens, retries, and partial downstream failures.

### 6. Add escalation and recovery

Define machine-readable reminders, escalation subjects or roles, maximum attempts, maximum wait, exhaustion behavior, and out-of-office coverage. Default timeouts to deny, cancel, or escalate—not approve. Specify whether an audit-store outage fails closed or uses a short, signed buffer; critical actions fail closed. Reauthorize identity, role, policy, proposal digest, target state, and expiry immediately before execution.

Define compensation as automatic, manual, required-but-unavailable, or not-applicable, with an owner and procedure reference. Treat break-glass as a distinct, strongly authenticated path with at least two named subjects, narrow scope, short expiry, reason capture, immediate alerting, and after-action review.

For rejection, preserve the proposal and reason without executing. For execution failure, stop unsafe retries, mark the true state, invoke a tested compensating action when one exists, notify the owner, and preserve redacted evidence.

### 7. Verify the controls

Test:

- Each action lands in the expected risk tier and gate
- Unauthorized, wrong-tenant, and self-approving actors are denied
- Approval fails after parameter, target, state, policy, or expiry changes
- Duplicate approvals and callbacks cannot execute twice
- Reject, edit, cancel, timeout, escalation, and unavailable-approver paths
- Quorum, distinct-subject, self-approval, owner-waiver, and separation-of-duties behavior under concurrent decisions
- Execution-time reauthorization and changed preconditions
- Escalation exhaustion, audit-storage outage, partial failure, compensation, break-glass, and incident notification
- Decision records contain required evidence but no secrets
- Usability with representative approvers, including comprehension and error rates

Report commands, simulations, and observed results. Do not claim that human review is effective without exercising both policy logic and the approval experience.

## Authorization and safety boundaries

- Designing a gate does not authorize the underlying action; do not execute, send, publish, deploy, purchase, delete, or grant access unless separately authorized.
- Never allow a model to fabricate, impersonate, or infer a human approval.
- Enforce identity, authorization, quorum, and approval binding outside model-generated text.
- Do not expose secrets or unnecessary personal data to approvers, logs, notifications, or test fixtures.
- Fail closed for missing identity, ambiguous or malformed predicates, stale state, expired approval or waiver, wrong tenant, invalid quorum, insufficient distinct subjects, or unavailable audit storage on high-risk actions.
- Avoid dark patterns, preselected approval, urgency manipulation, and bundles that hide materially different actions.
- Do not use human review to legitimize discriminatory, unlawful, or otherwise prohibited decisions.

## Realistic examples

### Refund agent

Allow autonomous refunds below $50 only for verified duplicate charges. Require a support manager above $50 and finance plus support above $1,000. Show order history, policy basis, amount, destination, and fraud signals. Bind approval to order, amount, destination, and policy version; test duplicates, changed payment destination, timeout, and partial processor failure.

### Communications agent

Let the agent draft customer updates but require the account owner to approve the exact recipients, subject, body digest, attachments, and send time. Any edit invalidates approval. A rejected draft returns to editing; an expired approval cannot send. Audit the decision without storing attachment contents in the decision log.

## Completion check

Finish only when every consequential action has a documented policy, predicates are structurally validated, approver roles resolve to sufficient distinct subjects, critical single-control or self-approval is rejected unless an active owner-approved waiver exists, approvals cannot be replayed or silently broadened, escalation/audit-outage/reauthorization/compensation/break-glass paths work, and the audit trail plus residual risk are explicit.
