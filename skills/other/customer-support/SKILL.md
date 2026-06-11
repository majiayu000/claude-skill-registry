---
name: customer-support
description: Customer support workflows — ticket triage, response drafting, knowledge base articles, escalation handling, customer research. Use when triaging support tickets, drafting customer responses, creating KB articles, managing escalations, or researching customer context.
routing:
  triggers:
    - "customer support"
    - "ticket triage"
    - "support response"
    - "knowledge base"
    - "KB article"
    - "escalation"
    - "customer research"
  category: business
  force_route: false
  pairs_with:
    - csuite
user-invocable: true
---

# Customer Support

Umbrella skill for customer-facing support workflows: triage incoming tickets, draft calibrated responses, convert resolutions into KB articles, package escalations, and research customer context. Each mode loads its own reference files on demand.

**Scope**: Customer-facing support work. Use professional-communication for internal business formats, csuite for strategic decisions, pr-workflow for code PRs.

---

## Mode Detection

Classify the request into exactly one mode. If the request spans modes, choose the primary and note the secondary.

| Mode | Signal Phrases | Core Output |
|------|---------------|-------------|
| **TRIAGE** | New ticket, categorize, prioritize, route, P1-P4, severity, SLA | Structured triage assessment with priority, routing, initial response |
| **RESPOND** | Draft response, reply to customer, follow up, de-escalate, bad news, decline | Customer-facing message with tone calibration and internal notes |
| **KB** | Knowledge base, document this, FAQ, write article, how-to guide, troubleshooting doc | Publish-ready KB article with metadata and search optimization |
| **ESCALATE** | Escalate, engineering attention, SLA breach, churn risk, multiple customers, leadership | Structured escalation brief with impact assessment and repro steps |
| **RESEARCH** | Look up, investigate, what did we tell them, has this been reported, check history | Research brief with source attribution and confidence scoring |

---

## Reference Loading Table

Load only the references required by the detected mode.

| Mode | Reference |
|------|-----------|
| TRIAGE | `references/triage-methodology.md` |
| RESPOND | `references/response-drafting.md` |
| KB | `references/knowledge-base.md` |
| ESCALATE | `references/triage-methodology.md`, `references/response-drafting.md` |
| RESEARCH | `references/knowledge-base.md` |
| Any mode | `references/llm-support-failure-modes.md` (always load -- LLM failure awareness is non-negotiable in support) |

---

## Mode: TRIAGE

**Framework**: PARSE -> CLASSIFY -> ROUTE -> RESPOND

**Phase 1: PARSE** -- Extract the actual problem from the ticket.

- Core problem vs. stated symptom (customers describe symptoms, not root causes)
- Urgency signals: production down, data loss, blocked, multiple users, time-sensitive
- Emotional state: frustrated, confused, matter-of-fact, escalating
- Customer context: account tier, history, previous tickets if available

**Phase 2: CLASSIFY** -- Assign category and priority.

Apply the category taxonomy from `references/triage-methodology.md`:

| Category | When |
|----------|------|
| Bug | "It used to work and now it doesn't" |
| How-to | "How do I make it work?" |
| Feature request | "I want it to work differently" |
| Billing | Payment, subscription, invoice, refund |
| Account | Login, permissions, SSO, access |
| Integration | API, webhook, third-party, sync |
| Security | Data exposure, unauthorized access, compliance |
| Performance | Slow, timeout, degraded, unavailable |

Assign priority P1-P4. When in doubt, err higher -- easier to de-escalate than recover from a missed SLA.

| Priority | Criteria | SLA Response |
|----------|----------|-------------|
| P1 Critical | Production down, data loss, security breach, all users | 1 hour |
| P2 High | Major feature broken, no workaround, many users | 4 hours |
| P3 Medium | Partial break, workaround exists, small impact | 1 business day |
| P4 Low | Cosmetic, feature request, general question | 2 business days |

**Phase 3: ROUTE** -- Determine the right team.

| Route to | When |
|----------|------|
| Tier 1 | How-to, known issues with docs, billing inquiries, password resets |
| Tier 2 | Bugs needing investigation, complex config, integration troubleshooting |
| Engineering | Confirmed bugs needing code fixes, infrastructure, performance degradation |
| Product | Feature requests with demand, design decisions, workflow gaps |
| Security | Data access concerns, vulnerability reports, compliance (bypasses tier progression) |

**Phase 4: RESPOND** -- Draft initial response using the category templates from `references/triage-methodology.md`.

**Gate**: Triage output includes: category, priority with justification, routing recommendation, suggested initial response, internal notes.

---

## Mode: RESPOND

**Framework**: CONTEXT -> CALIBRATE -> DRAFT -> VERIFY

**Phase 1: CONTEXT** -- Understand the full situation before writing a word.

- Who: customer name, account tier, relationship stage (new/established/frustrated)
- What: situation type (question, issue, escalation, bad news, good news, decline)
- Channel: email, ticket, chat (adjusts length and formality)
- Stakeholder level: end user, manager, executive, technical
- History: previous communications, commitments made, tone of thread

**Phase 2: CALIBRATE** -- Select tone from `references/response-drafting.md`.

| Situation | Tone | Key Characteristic |
|-----------|------|--------------------|
| Good news | Celebratory | Forward-looking, enthusiastic |
| Routine update | Professional | Clear, concise, friendly |
| Technical response | Precise | Accurate, patient, structured |
| Delayed delivery | Accountable | Honest, action-oriented |
| Bad news / won't-fix | Candid | Direct, empathetic, alternative-offering |
| Issue / outage | Urgent | Transparent, actionable, reassuring |
| Escalation | Executive | Composed, ownership-taking, plan-presenting |
| Billing | Precise | Factual, resolution-focused |

Adjust by relationship stage:
- **New customer**: More formal, extra context, proactive help
- **Established**: Warm, direct, reference shared history
- **Frustrated**: Extra empathy first, concrete plan, shorter feedback loops

**Phase 3: DRAFT** -- Write the response following the structure:

1. **Acknowledgment** (1-2 sentences) -- show you understand their situation
2. **Core message** (1-3 paragraphs) -- the actual answer, update, or information
3. **Next steps** (1-3 bullets) -- what you will do, what they need to do, when they hear from you
4. **Close** (1 sentence) -- warm, professional, available

**Phase 4: VERIFY** -- Run the quality checks before presenting.

- [ ] Tone matches situation and relationship stage
- [ ] No unauthorized commitments (timelines, features, exceptions)
- [ ] No product roadmap details that shouldn't be external
- [ ] Clear ownership and next steps
- [ ] Appropriate length for channel
- [ ] No corporate jargon, no passive voice to dodge accountability

**Gate**: Draft includes internal notes covering: rationale for tone, facts to verify before sending, risk factors, follow-up actions needed.

---

## Mode: KB

**Framework**: SOURCE -> STRUCTURE -> DRAFT -> OPTIMIZE

**Phase 1: SOURCE** -- Understand what you're documenting.

- Original problem, question, or error
- Resolution, workaround, or answer
- Who this affects (user type, plan level, configuration)
- Frequency: one-off or recurring
- Article type: how-to, troubleshooting, FAQ, known issue, reference

**Phase 2: STRUCTURE** -- Choose the right template from `references/knowledge-base.md`.

| Type | Purpose | Structure |
|------|---------|-----------|
| How-to | Step-by-step task completion | Prerequisites -> Steps -> Verify -> Common Issues |
| Troubleshooting | Diagnose and fix a problem | Symptoms -> Cause -> Solution(s) -> Prevention |
| FAQ | Quick answer to common question | Direct Answer -> Details -> Related Questions |
| Known issue | Document a bug with workaround | Status -> Symptoms -> Workaround -> Fix Timeline |

**Phase 3: DRAFT** -- Write the article following formatting standards.

- Title: specific, searchable, uses customer language ("How to configure SSO with Okta" not "SSO Setup")
- Opening sentence: restate the problem in plain language
- Headers for scannability. Numbered lists for sequences. Bullet lists for non-sequential items.
- Code blocks for commands, error messages, configuration values
- Short paragraphs (2-4 sentences max). One idea per section.

**Phase 4: OPTIMIZE** -- Search optimization and metadata.

- Include exact error messages (customers copy-paste into search)
- Use customer language, not internal jargon
- Add common synonyms (delete/remove, dashboard/home page, export/download)
- Tag with product areas matching customer mental models
- Set review date and identify SME for technical verification

**Gate**: Article includes metadata (title, type, category, tags, audience), full content, publishing notes (source, related articles, review needed, suggested review date).

---

## Mode: ESCALATE

**Framework**: CONFIRM -> GATHER -> ASSESS -> PACKAGE

**Phase 1: CONFIRM** -- Verify this warrants escalation.

Escalate when:
- Bug confirmed, needs code fix
- Multiple customers affected (3+ = pattern)
- Production down or data at risk
- SLA breach imminent or occurred
- Customer threatening churn
- Requires access or authority beyond support tier

Handle in support when:
- Documented solution or workaround exists
- Configuration or setup issue you can resolve
- Known limitation with documented alternative

**Phase 2: GATHER** -- Pull together all context.

- Timeline: when it started, how long the customer has waited
- What's been tried: troubleshooting steps and results
- Reproduction steps (for bugs): from clean state, specific values, environment details, frequency, evidence
- Related tickets and pattern detection

**Phase 3: ASSESS** -- Quantify business impact.

| Dimension | Assess |
|-----------|--------|
| Breadth | How many customers/users? Growing? |
| Depth | Blocked vs. inconvenienced? |
| Duration | How long? Getting worse? |
| Revenue | ARR at risk? Deals affected? |
| Contractual | SLA breach? Contractual obligations? |

Severity shorthand:
- **Critical**: Production down, data at risk, security breach. Immediate attention.
- **High**: Major function broken, key customer blocked, SLA at risk. Same day.
- **Medium**: Significant issue with workaround, important but not urgent. This week.

**Phase 4: PACKAGE** -- Structure the escalation brief.

Determine target:
- **Engineering**: confirmed bugs, infrastructure, code changes needed
- **Product**: feature gaps, design decisions, competing priorities
- **Security**: data exposure, vulnerability, compliance (bypasses normal tier progression)
- **Leadership**: high-revenue churn risk, SLA breach on critical account, policy exception needed

Include: severity, target team, impact summary, issue description, what's been tried, reproduction steps, customer communication status, specific ask with deadline, supporting context.

**Gate**: Escalation brief complete. Follow-up cadence set (Critical: every 2h internal / 2-4h customer. High: every 4h / 4-8h. Medium: daily / 1-2 business days).

---

## Mode: RESEARCH

**Framework**: SCOPE -> SEARCH -> SYNTHESIZE -> CAPTURE

**Phase 1: SCOPE** -- Define what you're looking for.

Research types:
- **Customer question**: needs a factual answer
- **Issue investigation**: has this been reported, what's the workaround
- **Account context**: what was previously communicated
- **Topic research**: best practices, general domain knowledge

Clarify: factual vs. contextual, audience (internal vs. customer), scope boundaries.

**Phase 2: SEARCH** -- Work through source tiers systematically.

| Tier | Source Type | Confidence |
|------|------------|------------|
| 1 | Official docs, KB, policies | High |
| 2 | CRM, support tickets, meeting notes | Medium-High |
| 3 | Chat, email, calendar | Medium |
| 4 | Web, forums, third-party docs | Low-Medium |
| 5 | Inference, analogies, best practices | Low -- flag explicitly |

Cross-reference across multiple sources.

**Phase 3: SYNTHESIZE** -- Compile findings with attribution.

- Lead with the bottom-line answer
- Assign confidence level (High / Medium / Low / Unable to Determine)
- Attribute every finding to its source
- Note contradictions explicitly -- present both sides, recommend the conservative answer for customer-facing use
- Identify gaps and unknowns

**Phase 4: CAPTURE** -- Suggest knowledge preservation.

If the research took significant effort, was a common question, or corrected a misunderstanding, offer to create a KB article or FAQ entry. Knowledge capture prevents duplicate research.

**Gate**: Research brief includes: direct answer, confidence level, key findings with source attribution, gaps and unknowns, recommended next steps.

---

## Cross-Mode Patterns

These apply regardless of mode. Internalize them.

**Empathy is not performance.** Acknowledge the customer's situation genuinely. "I understand how frustrating this must be" is fine when they're frustrated. The same phrase when they asked a simple how-to question is patronizing. Match the emotional register. Read `references/llm-support-failure-modes.md` on tone mismatch.

**Own it.** Active voice. "We" not "the system." "I'll investigate" not "this will be investigated." Take responsibility where appropriate. Take ownership in all customer-facing communication.

**Specificity over reassurance.** "I'll update you by Friday at 3pm" beats "I'll get back to you soon." Concrete details build trust. Vague reassurance erodes it.

**Close the loop.** Every interaction ends with clear next steps: what you will do, what they need to do, when they hear from you next.

**Confirm feature existence before stating it.** Say 'let me check' when uncertain. A wrong answer that sends a customer down a dead-end path is worse than "let me check and get back to you." See `references/llm-support-failure-modes.md`.

**Limit commitments to actions within your authority.** No timeline commitments on behalf of engineering. No policy exceptions without approval. No "we'll definitely build that." The trust cost of a broken promise exceeds the short-term relief of making one.
