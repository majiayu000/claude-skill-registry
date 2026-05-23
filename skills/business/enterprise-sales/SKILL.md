---
name: "enterprise-sales"
description: "Create an Enterprise Deal Execution Pack (buying committee map + champion enablement, “no decision” prevention plan + mutual action plan, procurement/security packet, and POC-as-business-case plan + ROI model). Use for enterprise sales, procurement, security reviews, and enterprise pilots/POCs. Category: Sales & GTM."
---

# Enterprise Sales

## Scope

**Covers**
- Running a single enterprise deal (mid-market → enterprise) from qualification to signature
- Mapping the buying committee and empowering a champion
- Preventing “no decision” outcomes (status quo / ghosting) with decision enablement + MAP
- Procurement + contracting workflows (forms, vendor onboarding, preferred-vendor objections)
- Security reviews + security questionnaires (packaging answers, coordinating stakeholders)
- POCs/pilots framed as a business case + ROI model (not just technical fit)
- Product-led sales escalation (self-serve usage → enterprise expansion narrative)

**When to use**
- “Build a mutual action plan for an enterprise deal.”
- “My deal is stuck in procurement/security—help me run it.”
- “We need a champion kit for IT/legal/economic buyer.”
- “They want a POC—help me scope it and build the ROI case.”
- “We have usage but can’t convert to enterprise—build an escalation story.”

**When NOT to use**
- You’re still validating ICP / first customers (use `founder-sales`)
- This is a transactional SMB sale without buying committee / procurement / security
- You need legal advice or final contract language (coordinate with counsel)
- You’re building a full sales org / forecasting system (use `building-sales-team`)

## Inputs

**Minimum required**
- Product + value: what it does, for whom, and the measurable outcome
- Account: company, segment, current state (existing tools/workflows), urgency/trigger
- Deal context: target package/ACV range, desired timeline, stage, and what “closed-won” means
- Stakeholders known so far: champion candidate, economic buyer, IT/security, legal/procurement, users
- Current friction: what is blocking progress (no decision risk, procurement, security, POC request, etc.)
- Constraints: what you can offer (pilot scope, services, security docs), internal resourcing, red lines

**Missing-info strategy**
- Ask up to 5 questions from [references/INTAKE.md](references/INTAKE.md).
- If answers aren’t available, proceed with explicit assumptions and label unknowns in **Assumptions & unknowns**, plus a short **Validation plan**.

## Outputs (deliverables)

Produce an **Enterprise Deal Execution Pack** in Markdown (in-chat; or as files if requested):

1) **Deal snapshot** (account, use case, stage, timeline, success definition)
2) **Buying committee map + champion plan** (roles, incentives, concerns, next actions)
3) **Champion enablement kit** (internal pitch + stakeholder one-pagers + objection answers)
4) **Decision enablement plan** (reduce “no decision”: do-nothing cost + decision guide + MAP)
5) **POC/pilot plan + ROI business case** (30-day plan; success metrics; ROI model; decision criteria)
6) **Procurement + security packet plan** (forms tracker, required docs, owners, timelines)
7) **Close + implementation handoff** (commercials, signature plan, kickoff + first value milestones)
8) **Risks / Open questions / Next steps** (always included)

Templates: [references/TEMPLATES.md](references/TEMPLATES.md)

## Workflow (7 steps)

### 1) Intake + enterprise qualification (what “enterprise” means here)
- **Inputs:** User context; [references/INTAKE.md](references/INTAKE.md).
- **Actions:** Confirm deal type (buying committee, procurement/security, ACV, timeline). Capture the core use case and desired business outcome. Identify the #1 stall risk (no decision vs procurement vs security vs POC).
- **Outputs:** Deal snapshot + assumptions/unknowns + validation plan.
- **Checks:** There is a clear outcome, buyer, and timeline (even if assumed).

### 2) Map the buying committee + pick the champion
- **Inputs:** Account org context; known stakeholders.
- **Actions:** Build a buying-committee map (5–7 common roles) and identify a champion (the person who can drive internal consensus). Define each stakeholder’s goals, risks, and required evidence.
- **Outputs:** Buying committee map + champion plan (what the champion needs next).
- **Checks:** A single “primary champion” is named (or a plan to find one within 1–2 calls).

### 3) Arm the champion (enable internal selling)
- **Inputs:** Use case, value narrative, stakeholder concerns.
- **Actions:** Produce a champion enablement kit: internal pitch memo, stakeholder one-pagers (IT/security, procurement, legal, economic buyer), and objection/FAQ answers. Include proof artifacts (case studies, security docs list, ROI assumptions).
- **Outputs:** Champion enablement kit.
- **Checks:** The champion can forward/share these materials without editing (copy/paste ready).

### 4) Beat “no decision” with decision enablement + MAP
- **Inputs:** Current stage; risks; target decision date.
- **Actions:** Make “do nothing” concrete (cost, risk, missed goals). Define the decision to be made, options, and decision criteria. Build a Mutual Action Plan (MAP) with dates, owners, and required outputs (incl. procurement/security milestones).
- **Outputs:** Decision enablement plan + MAP.
- **Checks:** MAP includes a decision meeting date and explicit buyer commitments (not just seller tasks).

### 5) Design the POC/pilot as a business case (not a feature test)
- **Inputs:** POC request; success criteria; data available; integration constraints.
- **Actions:** Reframe the POC as a 30-day pilot to co-create a business case/ROI model. Define measurable success metrics, required data, responsibilities, and decision criteria. If appropriate, propose a **paid** pilot/POC as a seriousness filter.
- **Outputs:** POC/pilot plan + ROI model + decision criteria.
- **Checks:** The pilot produces a decision-ready business case, not just “it works.”

### 6) Run procurement + security like a project (do the paperwork)
- **Inputs:** Procurement process; security requirements; contract constraints.
- **Actions:** Create a tracker for forms, security questionnaires, and vendor onboarding steps. Offer to pre-fill buyer forms to reduce their load. Prepare a minimal security packet checklist and coordinate internal SMEs. Consider contract structuring options (e.g., separate services vs software agreements) where appropriate—without giving legal advice.
- **Outputs:** Procurement/security tracker + packet checklist + comms plan.
- **Checks:** Owners and dates exist for every procurement/security task; blockers are explicit.

### 7) Quality gate + finalize (close-to-implementation)
- **Inputs:** Draft pack.
- **Actions:** Run [references/CHECKLISTS.md](references/CHECKLISTS.md) and score with [references/RUBRIC.md](references/RUBRIC.md). Add a signature plan (who signs, when) and an implementation handoff (kickoff, first value milestone). Always include **Risks / Open questions / Next steps**.
- **Outputs:** Final Enterprise Deal Execution Pack.
- **Checks:** Next steps are executable this week; assumptions are explicit; “no decision” risk is actively managed.

## Quality gate (required)
- Use [references/CHECKLISTS.md](references/CHECKLISTS.md) and [references/RUBRIC.md](references/RUBRIC.md).
- Always include: **Risks**, **Open questions**, **Next steps**.

## Examples

**Example 1 (procurement + security stall):**  
“Use `enterprise-sales`. We’re selling a workflow automation tool to a 5k-employee fintech. We have a champion in Ops, but procurement sent vendor onboarding forms and security wants a questionnaire + SOC 2. Output: an Enterprise Deal Execution Pack with a MAP, procurement/security tracker, and champion enablement one-pagers.”

**Example 2 (POC request, ROI focus):**  
“Use `enterprise-sales`. A healthcare enterprise wants a POC. ACV target $120k. They’re asking for a technical test, but we want to make it a business-case pilot. Output: a 30-day pilot plan with success metrics, ROI model, and a decision-ready business case.”

**Boundary example:**  
“Just write a generic enterprise sales script that closes anyone.”  
Response: explain this skill is deal-specific and evidence-driven; request account context + stakeholders and produce a tailored MAP, champion kit, and pilot/business-case plan instead.
