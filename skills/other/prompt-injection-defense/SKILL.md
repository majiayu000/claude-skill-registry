---
name: prompt-injection-defense
description: Threat-model and harden AI agents, RAG systems, assistants, and tool-using workflows against direct, indirect, stored, cross-agent, and multimodal prompt injection. Use when reviewing an agent architecture, isolating untrusted content, constraining tools and egress, protecting secrets, adding injection-focused tests, investigating a suspected injection incident, or documenting residual prompt-injection risk.
---

# Prompt Injection Defense

Design for compromise of model reasoning. Prompt text and classifiers can reduce attack success, but they do not create a reliable security boundary. Keep consequential authority, authorization, validation, and policy enforcement outside the model.

## Inputs

Collect or infer, and label assumptions for:

- Agent purpose, system/developer instructions, models, memory, and orchestration
- Every input source, including users, web pages, email, documents, images, audio, tool results, RAG, and other agents
- Tool list, privileges, identities, targets, write effects, and network egress
- Secrets, private data, system prompts, policy data, and other protected assets
- Output sinks such as UI rendering, code execution, messages, databases, and downstream agents
- Authorization model, human gates, monitoring, incident history, and risk tolerance
- Representative benign tasks and a safe evaluation environment

Do not request production secrets or malicious artifacts in chat. Use redacted samples or synthetic fixtures.

## Output contract

Deliver:

1. A data-flow and trust-boundary map covering protected assets, all modalities, sinks, memory stores, agent hops, approved destinations, and credential boundaries
2. A threat model listing protected assets, attacker-controlled channels, injection paths, and security invariants
3. A prioritized defense plan that maps each path to preventive, limiting, detective, and recovery controls, each marked `missing`, `planned`, `implemented`, or `verified`
4. Code or configuration changes only within the user's authorized scope
5. A regression suite with safe direct, indirect, stored, encoded, cross-agent, and multimodal cases as applicable
6. Verification evidence, observed failures, and metrics rather than a blanket claim of prevention
7. Residual risk, operational monitoring, and an incident containment/recovery plan

Describe the architecture in a JSON boundary manifest and lint it with [scripts/audit_boundary_manifest.py](scripts/audit_boundary_manifest.py). Record every control's enforcement point, owner, evidence IDs, test IDs, and expiry when time-limited. A passing structural lint is not evidence that controls work. Read [references/defense-patterns.md](references/defense-patterns.md) for attack paths, control placement, and verification patterns.

## Workflow

### 1. Map instructions, data, authority, and sinks

Trace content from origin through parsing, retrieval, model context, memory, tools, renderers, output sinks, and downstream agents. Mark every attacker-controlled or mixed-trust source. Include hidden document text, metadata, code comments, OCR, images, audio, redirects, tool descriptions, and persisted memory. Inventory approved and denied destinations, each credential's holder/audience/storage boundary, and every point where content or authority crosses agents.

List assets and consequences: secret disclosure, private-data access, unauthorized tool calls, external communications, transactions, code execution, policy bypass, corrupted memory, or misleading output.

### 2. Define enforceable invariants

Express requirements in terms a deterministic component can enforce, for example:

- Retrieved content cannot grant permissions or change the tool allowlist.
- A support agent cannot read records outside the authenticated tenant.
- An email body cannot determine recipients for a send operation.
- Model output cannot execute as code or HTML without validation and safe handling.
- Secrets unavailable to the task never enter model context.

If an invariant exists only as a prompt instruction, record it as weak and move enforcement to code, policy, isolation, or human control.

### 3. Reduce exposed authority

Remove unused tools, broad tokens, ambient credentials, generic shells, arbitrary URL fetches, raw SQL, and unrestricted file access. Split read from write and preview from commit. Restrict identities by tenant, object, action, fields, time, and destination.

Keep secrets outside model context and tool results. Add network and data egress allowlists. Sandbox code, parsers, browsers, and file processing. Require independent authorization and, where warranted, action-specific approval immediately before consequential effects. A tool classified `critical` must not have confirmation mode `none`.

### 4. Separate control from untrusted content

Treat untrusted content as quoted data with provenance, never as authority. Preserve source boundaries through retrieval and agent handoffs. Use structured typed messages instead of concatenating instructions and data. Limit retrieved content, strip active content when safe, normalize supported formats, and render outputs with context-appropriate escaping.

Instruction hierarchy, delimiters, reminders, content classifiers, and injection detectors can be defense-in-depth signals. Do not depend on any of them as the sole control.

### 5. Validate every transition

Validate tool arguments against narrow schemas and policy before execution. Derive sensitive target identifiers from trusted application state rather than untrusted text where possible. Reauthorize at execution time. Validate and encode model outputs for their destination; never send them directly to shells, SQL, templates, URLs, or privileged APIs.

For multi-agent systems, authenticate senders, constrain delegation depth and budgets, pass structured claims with provenance, and recalculate permissions at each hop. Never inherit the broadest upstream privilege implicitly.

### 6. Test with safe adversarial cases

Use an isolated environment, synthetic accounts, benign canary secrets, inert destinations, and non-destructive tools. Test at least:

- Direct attempts to override instructions or elicit protected data
- Indirect instructions embedded in retrieved pages, email, documents, tool results, metadata, and memory
- Obfuscation, encoding, language changes, splitting across turns, and repeated attempts
- Cross-agent delegation and tainted summaries
- Hidden or alternate-modal content when images, audio, PDFs, HTML, or OCR are supported
- Tool-argument manipulation, target substitution, data exfiltration, and unauthorized egress
- False positives on representative benign content and normal task completion

Measure invariant violations, unauthorized tool attempts, canary exposure, successful benign tasks, false-positive rate, and containment behavior. A detector pass rate alone is insufficient. Promote a control to `verified` only when implementation evidence and named test evidence both exist; use `implemented` when code exists but the relevant tests have not established behavior.

### 7. Operate and recover

Log provenance, policy decisions, tool/target metadata, denials, and anomalous sequences without storing secrets or unnecessary content. Alert on canary access, repeated policy failures, new tool exposure, cross-tenant attempts, and unexpected egress.

For a suspected incident, stop or isolate the affected workflow, disable high-risk tools and egress, revoke or rotate exposed credentials, quarantine malicious sources, preserve redacted evidence, identify persisted memory/vector entries and downstream effects, restore clean state, and rerun regression tests before re-enabling access.

## Authorization and safety boundaries

- Do not test payloads against production, third-party, or user systems without explicit target-specific authorization.
- Do not trigger real transactions, messages, deletions, access changes, malware, or data exfiltration; use inert canaries and synthetic destinations.
- Never place real secrets, personal data, privileged system prompts, or live tokens in test corpora or logs.
- Do not claim that prompt injection has been eliminated. State tested scope, model/configuration, evidence, limitations, and residual risk.
- Do not silently delete potentially compromised memory, records, or evidence; quarantine first and follow the owner's retention and incident policy.
- Stop testing and escalate if scope is uncertain, a canary reaches an unintended system, real sensitive data appears, or an unexpected external effect occurs.

## Verification and recovery

Before completion, confirm that every protected asset, untrusted path, sink, memory store, agent hop, destination, and credential boundary is represented; every consequential effect has a non-model authority check; critical tools have confirmation; exposed privileges are minimized; and regression tests exercise both attack resistance and benign-task utility. Do not turn unknowns into unsupported all-true assertions: retain `missing` and `planned` controls as visible gaps. Re-run tests after model, prompt, parser, retrieval, tool, permission, or orchestration changes.

If a control causes unacceptable task failure, roll back that control in isolation, keep higher-risk tools disabled, preserve the failing case, and redesign the boundary. Do not restore broad authority simply to improve the success rate.

## Realistic examples

### Email triage agent

Treat subjects, bodies, attachments, and quoted threads as untrusted data. Let the model classify and draft, but derive mailbox and tenant from authenticated state. Separate draft from send, restrict recipient domains, require exact-message approval for external sends, and test an attachment containing an inert instruction to reveal a canary or change the recipient.

### Research agent with web access

Run browsing with no access to internal secrets. Allowlist required destinations, strip active content, retain page provenance, and prevent page text from expanding tools or changing the research goal. Test hidden page text, a malicious tool result, encoded instructions, and a normal page containing security-related phrases to measure false positives.

## Completion check

Finish only when architecture, controls, tests, and recovery cover the full data flow; evidence shows protected invariants hold in the tested environment; benign utility remains measured; and residual risk plus unverified surfaces are explicit.
