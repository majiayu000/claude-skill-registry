---
name: fde
description: Keeps the engagement record for client work. Use when they name a client or stakeholder. Use when they debrief a meeting or paste notes. Use when they ask what was agreed. Use when they run a POC, change the client's codebase, prove it on their staging, go live, or need evals before a model acts. Use when they prep a readout, when trust shifts, or they say @fde. Route and run the local fde CLI (or npx --yes fdeops). Never ask them to type commands. Not for ordinary code edits in an unbound repo.
---

# @fde

## Purpose

Coordinate customer work from the first brief through implementation, verification and handoff. Choose the relevant task; never make the user pick a phase. All task skills also work individually. Reuse the customer's tools, decisions and operating process.

## Task entry

Read `references/task-context.md` for authority, data boundaries, CLI availability and evidence rules. An explicitly selected task runs directly without another coordinator entry.

- **Standalone request:** use supplied permitted context and the selected method. Do not initialize `.fde/`, preferences or records just to draft, analyze or change code. Ordinary code edits in an unbound repository do not automatically trigger `@fde`.
- **Ongoing engagement:** use the supplied customer binding. If none exists, use the supplied name or ask once, then run `fde resume --init <client-name>`. Two possible customers require a binding decision before reads or writes.
- **Ready to build:** use the existing outcome, constraints and verification path. Discover or plan only for material gaps. Audit inherited claims on a takeover.

## Human surface vs agent plumbing

The human asks in ordinary language or invokes a task skill. You run the required CLI commands. Never tell the FDE to type commands; never ask them to run the CLI. Follow the permitted fallback in task context, including `npx --yes fdeops` when downloads are authorized.

## Entry (every session)

For record-backed work only:

1. Before client reads, run `fde setup --show` and verify `fde privacy` support. If setup is unconfigured or the user requests preferences, follow `references/record-setup.md`. Setup does not authorize sharing customer data.
2. Use a fresh `fde resume` packet for this turn/task. Reuse a current session-hook packet only when its visible `ENGAGEMENT:` matches the binding and its freshness is certain. Refresh after binding, masking or record changes, or when the user asks where things stand. Do not reuse an earlier turn's packet or repeat the same entry solely because another method loaded.
3. Read policy, signer, goals, risks and current work. Retrieve omitted or disputed evidence, saved lessons and dated retrospectives with `fde recall <topic>`; never replace this with raw or recursive record reads. Resume defaults to 16 KiB (4 KiB in compact setup); `--max-bytes 4096` reduces it, and `--full` is for explicitly needed complete context.
4. For interrupted implementation, inspect the saved checkpoint and follow `references/verification.md#recoverable-checkpoint` before acting. A checkpoint is a dated claim, not a fresh test or permission to execute. For a returning or closed engagement, apply the reopening check in `references/land.md` before relying on historical access, owners or deployment evidence.
5. Give a brief playback and load the relevant method below. `hygiene:` means offer `fde doctor`; never auto-rewrite.

The CLI uses local files and Git, without network calls. Install it on the FDE's own machine, never customer infrastructure. The AI host's permissions and provider policy remain separate.

## Engineering and delivery

Use `build` for implementation, `integrate` for system boundaries, `debug` for failures and `qa` for the delivered journey. Their shared verification method binds claims to actual evidence; another skill pack is not required.

For a bound engagement, connect the existing plan or bounded experiment to characterization of the customer's code, relevant checks, a replayable delivery checkpoint and a confirmed receipt. Reuse their tests and runner. Where a model acts or judges, follow `references/eval-pack.md` and `references/ai.md` before release. Use `ship` for release authority, recovery and operating evidence.

Scale this to the work: routine fixes reuse agreed scope, signer and acceptance criteria. They do not require a new sponsor decision per edit. Keep implemented, verified, deployed, measured and accepted separate. A local pass is not a customer outcome.

## Record commands

| They say | You run |
|----------|---------|
| where are we | `fde resume` |
| outcome / Friday status | `fde status` |
| day-1 look at the repo | `fde scan` |
| debrief / pasted notes for a bound record | `fde debrief --smart` → agent reconciliation → one plain-English review → Save this update? → `--apply`. `--smart` is a gate, not a brain. `references/debrief.md` |
| prep me for … | `fde prep "<label>"` |
| did we agree / who decided / why did we | `fde receipts <term>` |
| sponsor update / defend the number | `fde defend` |
| successor / rotation / portable handoff | `fde handoff` (stdout; `--out new-file.md` only after export requested) |
| they went quiet | Review evidence with `references/rescue.md`; confirm a signal change before `fde log contact "…" --signal amber\|green\|red` |
| fieldbook page | `fde dashboard` (`--all` portfolio, `--open` to open the file) |
| clean up the fieldbook | `fde doctor` - never auto-rewrite |
| scrub a secret | `fde redact <term>` then `--apply` after confirm |
| pull Granola/Slack/transcript | capability check → `fde ingest stage` → confirm → apply. Never auto-apply. `references/ingest.md` |
| connect an MCP | `references/connect.md` |
| Obsidian / one window | `fde vault` (`--redacted` for a shared screen) |

## The memory contract

- Deliver the requested artifact; save consequential engagement judgments only under the confirmation rules in task context. No supplied source means a decision or measurement remains CLAIM. ON RECORD means a source was supplied, not authenticated or customer-approved. Never invent people, meetings, numbers or acceptance.
- For bound meeting updates: `fde debrief --smart` prepares a proposal; reconcile it, run `fde debrief --review`, show one concise review, then apply only after confirmation and verify saved facts. Standalone meeting analysis uses the review-only path in `references/debrief.md`.
- Keep one customer per folder. Never drop `## Signal history` or `## Retired` when editing. Preserve existing decisions and scope when updating progress.
- Keep a **session digest** at a meaningful pause or before a PR: relevant conclusions, not a transcript dump. Confirm consequential judgments before writing. The session-stop hook captures filesystem facts; it does not replace your digest or infer completed work.

| Digest beat | Destination |
|-------------|-------------|
| TL;DR, gotchas, pivot | `context.md` |
| Key decisions & why | `decisions.md`, when there are decisions |
| Scope and verification | `delivery.md`, when applicable |
| Next action | Replace the existing `## Next action`; never append a second heading |
| Interrupted implementation | Optional `## Implementation checkpoint` in existing `context.md`, summarized from the existing task record under `references/verification.md` |

## Voice

Be direct, use the customer's terms, and act after a short playback. Ask one sharp question only when missing information changes the next action. State uncertainty rather than guessing. Choose brief for a new engagement or audit for a takeover; never run a phase-picker interview. Engagement size changes depth, not the available skills.

## Routing - 6 stages

Work names (engage, diagnose, align, deliver, realize, transfer) are the same map. Read **one** reference and follow it. Do not improvise from memory.

### Land

| You hear | Skill | Reference |
|----------|-------|-----------|
| Engage, onboarding, starting fresh, new customer, first meeting, just got the brief, set product strategy, define success metrics, scope the brief | brief | `references/land.md` |
| Taking over, previous consultant left, joining mid-project | audit | `references/audit.md` |
| Need to understand who matters, who decides, map decision rights, who blocks quietly | who-decides | `references/who-decides.md` |
| Need to earn access, navigate AI policy, build credibility | earn-trust | `references/earn-trust.md` |
| "Also can you…", scope expanding, timeline unchanged, hold scope, scope the brief after kickoff | scope | `references/hold-scope.md` |

### Discover

| You hear | Skill | Reference |
|----------|-------|-----------|
| Diagnose, don't know the real problem, brief feels wrong, shadow processes, frame discovery, understand the problem space, data not ready, data estate, catalog the data, parts of the problem, decompose | discover | `references/discover.md` |
| The brief feels too neat, assumptions untested, "we just need…", test assumptions, inherited convention, why do we always | test-assumptions | `references/test-assumptions.md` |
| Multiple use cases competing, "we want to do everything", score use cases | score-use-cases | `references/score-use-cases.md` |
| Need to validate a direction, prototype, demo to de-risk, **POC**, spike, killer assumption, validate the solution, build prototype | poc | `references/poc.md` |

### Plan

| You hear | Skill | Reference |
|----------|-------|-----------|
| Align, break this down, what order, sequence the delivery, align the plan | plan | `references/plan.md` |
| Sponsor needs justification, need to defend budget or timeline, build the business case | business-case | `references/business-case.md` |
| Significant decision, multiple approaches, "what should we do?", generate solutions, generate options, not the playbook, from the surviving facts | options | `references/three-options.md` |
| 20 things are "urgent," need to pick the 3 that matter, prioritize three | prioritize | `references/pick-three.md` |

### Ship

| You hear | Skill | Reference |
|----------|-------|-----------|
| What could go wrong, touching shared infrastructure, need to assess impact, assess impact, provision, IaC, shared infra | what-breaks | `references/what-breaks.md` |
| Production down, urgent, fix a prod bug, resolve incident, restore service - OR stakeholder gone quiet, trust slipping | rescue | `references/rescue.md` |
| Deliver, start building, update their checkout, first module, their tests, build the increment, design their UI | build | `references/build.md` |
| Customer API, connector, data mapping, write-back, import, upstream integration | integrate | `references/integrate.md` |
| Reproduce a failure, unexpected output, regression, debug a connector | debug | `references/debug.md` |
| Exercise the customer journey, browser acceptance, functional QA | qa | `references/qa.md` |
| Ready to deploy, going live, pre-flight, release the verified increment | ship | `references/ship.md` |
| Review this change, review the pull request, is it safe, does it match what we agreed | review | `references/review.md` |
| Evaluate model answers, retrieval or agent actions against representative cases | evaluate | `references/eval-pack.md` |
| Diff grew / scope creep in the PR / "did we only build what we said" / KEEP JUSTIFY SPLIT DROP | review (+ ship if going live) | `references/review.md` Stage 1 · `references/ship.md` Intent vs diff |
| Wrap the session / share the thinking / catch teammates up / before I open the PR | (memory contract - session digest) | SKILL.md **Session digest** - write TL;DR + decisions/why into `.fde/`; no transcript sync |
| "We can always revert" - need to actually test the escape route, rehearse rollback | rollback | `references/rollback.md` |

### Outcome

| You hear | Skill | Reference |
|----------|-------|-----------|
| Realize, weekly update due, "need to send the sponsor something", report the outcome | readout | `references/readout.md` |
| Demo coming up, show-and-tell, exec walkthrough, prepare the demo | demo-prep | `references/demo-prep.md` |
| Just out of a meeting, raw notes, "they said…", "debrief", user interviews, workshop notes, capture the meeting | debrief | `references/debrief.md`; review-only for standalone notes, CLI review/apply for a bound record |
| Make sure we're up to date, pull what's relevant, fetch from Granola/Slack/Gmail/transcript | ingest | `references/ingest.md` (capability check → stage → propose → confirm → apply) |
| Connect a new MCP / connect Granola Slack or Notion / what can you pull | connect | `references/connect.md` (+ `references/source-setup.md`) |
| Prep me for a meeting / walk-in brief / "what should I know before I talk to…" | - | run `fde prep "<label>"`, present in plain language |
| Sponsor's boss needs a summary, board update, brief the board, justify continued investment | board-memo | `references/board-memo.md` |
| Status across all my customers, view the portfolio | dashboard | `references/dashboard.md` |

### Close

| You hear | Skill | Reference |
|----------|-------|-----------|
| Juggling 2+ customers, losing track, context-switching, switch engagements | switch-clients | `references/switch-clients.md` |
| Transfer, wrapping up, handoff, making yourself replaceable, transfer operations | handoff | `references/close.md` |
| Engagement ending, team needs to operate without you, write the runbook | runbook | `references/runbook.md` |
| Something worked well and will apply to future engagements, encode the pattern | feedback | `references/encode-pattern.md` |
| "Red-team this," "stress-test my plan," poke holes, challenge the plan, what am I missing | red-team | `references/red-team.md` |
| "Did we agree to X?", "Who decided?", "Why did we choose X?", scope dispute | - | run `fde receipts <term>`; return the decision, person, date, source and later changes; use targeted recall for missing context |

**Overlays - activate alongside any skill on signal, don't wait to be told:**

| Signal | Overlay |
|--------|---------|
| AI, ML, LLM, model, embeddings, RAG, agents, fine-tuning, inference, drift, train the model | `references/ai.md` |
| Golden set, eval suite, eval pack, pass/fail before AI ship, HITL gate for model, POC the model | `references/eval-pack.md` (+ `ai.md`) |
| Deck, slides, report, governance framework, compliance pack, ADR, PDF | `references/artifacts.md` |
| Patient data, PHI, HIPAA, EHR, clinical | `references/healthcare.md` |
| Payments, cardholder data, PCI-DSS, anything that moves money | `references/fintech.md` |
| Government agency, FedRAMP, ATO, CUI, classified | `references/gov.md` |

Ready to build: check that the supplied facts establish the outcome, constraints and verification path. Use discover or plan only for material gaps. On a takeover, audit inherited claims that affect the task. Two customers in one message: confirm which folder.

## Principles

- Follow the selected method and relevant overlays; do not load every reference.
- Reuse approved plans and applicable evidence instead of inventing parallel process.
- A missing record or check is an explicit gap, not a reason to fabricate facts or restart discovery.
- Confirm consequential record changes; use customer policy and actual decision authority for external actions.
- Report what was achieved, its evidence and remaining limits. Never equate implementation with deployment or acceptance.

### Keep open work visible

For confirmed follow-ups, maintain `## Commitments` and `## Open questions` in the existing `context.md`. Use unchecked bullets for unresolved items and check them only after confirmed resolution. A commitment says who owes what to whom; include a source and `due: YYYY-MM-DD` or `review: YYYY-MM-DD` only when agreed. Preserve unresolved `unknown - ask:` questions here when they affect the next decision. Do not infer a promise from a suggestion. `resume` and `prep` surface these entries with sources; dates prompt a status check, not an invented escalation. For a meeting, select relevant entries and use targeted recall for supporting evidence. Users describe the follow-up naturally; maintain the record for them.

### Answer from the record

A receipt is dated evidence for a claim, not automatic customer approval. For agreement questions, distinguish proposed work, an agreed decision, a later withdrawal and acceptance of a delivered result. Attribute the decision and rationale only when recorded; the person who wrote a note is not necessarily the decision-maker. If the search finds no agreement evidence, say “I found no recorded agreement in the material checked,” show relevant claims as claims, and name who can clarify only when their authority is known. Do not invent a rationale or treat absence as “never agreed.”

For meeting preparation, use `fde prep` as the starting packet, then select unresolved questions and commitments relevant to the meeting's purpose and participants. Include the recorded owner, due/review date and source where available; mark missing fields unknown. Retrieve supporting or conflicting context with targeted recall. Do not turn every old unknown into an agenda item, infer an overdue date, or hide a material blocker merely because its wording does not match the meeting label.
