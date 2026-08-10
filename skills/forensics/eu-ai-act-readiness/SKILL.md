---
name: eu-ai-act-readiness
description: Build a preliminary, evidence-based EU AI Act readiness assessment across AI-system inventory, territorial scope, operator roles, prohibited-practice screening, risk classification, transparency, high-risk controls, general-purpose AI obligations, governance, and implementation milestones. Use when an organization needs to triage an AI use case, vendor, model, product, or portfolio for Regulation (EU) 2024/1689; prepare an AI inventory, gap register, implementation roadmap, or counsel briefing; assess provider, deployer, importer, distributor, product-manufacturer, authorised-representative, or GPAI-provider responsibilities; or re-check readiness after regulatory or product changes.
---

# EU AI Act Readiness

Produce operational triage, not a legal opinion. The AI Act changes through amendments, delegated/implementing acts, guidance, standards, and national enforcement practice; verify the law and dates at the start of every assessment.

## Inputs

Collect or state:

- Assessment date, target EU/EEA countries, organization locations, customer/user locations, and where system outputs are used.
- Each AI system/model's purpose, intended use, use-case screen, reasonably foreseeable misuse, lifecycle status, exact system/model versions, launch/change dates, material modifications, and affected people.
- Organization role(s) for each system: provider, deployer, importer, distributor, product manufacturer, authorised representative, or GPAI model provider.
- Model/vendor chain, branding, fine-tuning or substantial modifications, integrations, data sources, and contract allocation.
- Jurisdictions, decision domain, degree of automation, human-oversight design/authority, outputs, transparency interface, monitoring, incidents, complaint/appeal paths, and explicit reassessment triggers.
- Existing risk, quality, privacy, security, accessibility, procurement, recordkeeping, and AI-literacy evidence.

Use the blank [AI system inventory template](assets/ai-system-inventory-template.csv) when no reliable inventory exists.

## Output contract

Return:

1. Assessment date, last-verified legal-source date, jurisdictions, official sources, assumptions, and limitations.
2. An inventory with jurisdiction, system/model version, preliminary EU nexus, operator role, use-case screen, foreseeable misuse, material modifications, automation/oversight, risk-status hypothesis, classification basis/confidence, and reassessment triggers.
3. A gap register mapping provision/topic, applicable milestone, current evidence, gap, priority, owner, target date, and verification method.
4. Separate sections for prohibited-practice escalation, Article 50 transparency, high-risk systems, GPAI models, and broadly applicable governance such as AI literacy.
5. A 30/60/90-day implementation plan plus questions requiring qualified EU counsel or a competent authority.

Use `preliminary`, `potential`, or `counsel review required`; do not label an organization “compliant,” provide a definitive legal classification, or promise regulator acceptance.

## Workflow

### 1. Verify law, jurisdiction, and date

Open [current-law-and-sources.md](references/current-law-and-sources.md), then check the linked EUR-Lex legislation and European Commission/AI Act Service Desk pages for changes since `2026-08-09`. Read Regulation (EU) 2024/1689 together with Regulation (EU) 2026/1744 and any later amendments or consolidated text.

Record the access date and governing language/version. Confirm whether later delegated acts, implementing acts, Commission guidelines, harmonised standards, common specifications, codes, court decisions, or national rules affect the issue. If current official sources cannot be checked, mark the legal timeline stale and stop before making a deadline or classification conclusion.

Determine the relevant EU nexus and role under Articles 2 and 3. Consider EU market placement, EU-based deployment, and outputs used in the EU, as well as exclusions and sector-specific law. Territorial scope and exemptions are legal questions; route uncertainty to counsel.

### 2. Build and structurally check the inventory

Create one record per materially distinct system/model/use. Run the bundled completeness checker from this skill directory:

```bash
python3 scripts/check_ai_inventory.py assets/ai-system-inventory-template.csv --as-of 2026-08-09 --pretty
python3 scripts/check_ai_inventory.py /path/to/populated-inventory.csv --as-of YYYY-MM-DD --pretty
python3 scripts/check_ai_inventory.py /path/to/populated-inventory.csv --as-of YYYY-MM-DD --output /path/to/check.json --pretty
```

The checker uses standard-library heuristics, emits no legal classification, and labels its output `structural/completeness screening only—not semantic fact verification or legal verification`. It reports system IDs, missing fields, invalid controlled-vocabulary values, date issues, age/event status, and keyword-derived signals; it does not copy other source row values. With `--output`, it refuses inventory aliases and non-regular destinations, then atomically creates or replaces the report via a sibling temporary file. Use its controlled values for `article_50_status` and `counsel_status`; manually verify every source fact and signal. Include shadow AI, pilots, employee tools, vendor features, embedded models, legacy systems, and retired systems with continuing effects.

The default 365-day staleness flag is an administrative prompt, not a statutory deadline. Reassess sooner whenever a recorded trigger occurs, including a new use, system/model version, vendor, geography, role, material modification, incident, or legal update. A recent assessment can therefore still be due immediately.

### 3. Screen urgent exclusions and prohibited practices

First confirm whether the item is an AI system or GPAI model within the Act's definitions. Screen intended use and foreseeable operation against Article 5, including amendments. If a potential prohibited practice appears, stop routine scoring, preserve evidence, recommend a pause on deployment/expansion, and escalate to qualified counsel and the accountable owner. Do not pause or alter a live system unless the agent has explicit authority to do so. Do not attempt to redesign or conceal the use to evade scope.

Separately identify employment, education, biometrics, critical infrastructure, essential services, law enforcement, migration/border, justice, elections, health/safety, minors, and vulnerable-person contexts. These are escalation signals, not automatic classifications.

### 4. Determine role and preliminary risk path

For each system, document the facts supporting:

- Out of scope or an exclusion, with the exact basis requiring counsel confirmation.
- Prohibited-practice concern under Article 5.
- Potential high risk under Article 6 with Annex I or Annex III, including any exception and its documentation conditions.
- Article 50 transparency obligations.
- GPAI model obligations under Chapter V, including possible systemic-risk analysis.
- Minimal/other risk with voluntary controls and any other applicable EU or national law.

Roles can overlap and can change through rebranding, placing on the market, substantial modification, or changing intended purpose. Do not rely solely on a vendor's label or contract.

### 5. Map duties and milestones

Read [assessment-checklist.md](references/assessment-checklist.md). Map only duties supported by a preliminary scope/role analysis, and cite the relevant article/annex. At minimum assess:

- AI literacy and accountable governance.
- Provider/deployer transparency and affected-person notices.
- High-risk risk management, data governance, technical documentation, records/logging, instructions, human oversight, accuracy, robustness, cybersecurity, quality management, conformity/registration, monitoring, incident response, and fundamental-rights impact assessment where applicable.
- Deployer operating controls, input-data relevance, log retention, worker information, monitoring, human oversight, and impact/notification duties where applicable.
- GPAI technical documentation, downstream information, copyright policy, training-content summary, and additional systemic-risk duties where applicable.

Use the applicable date from verified current law, not a remembered deadline or an undated checklist.

### 6. Test evidence, not policy language

For each control, request an existing artifact and test whether it covers the exact system, version, role, purpose, jurisdiction, and lifecycle stage. Examples include approved inventory entries, risk records, dataset provenance, evaluation reports, logs, model/system cards, user instructions, human-oversight tests, security evidence, change records, contracts, transparency notices, incident exercises, training records, and decision/appeal procedures.

Mark `implemented` only when evidence is current and tested. Otherwise use `partial`, `planned`, `missing`, `not assessed`, or `not applicable—basis pending counsel`.

### 7. Prioritize and brief counsel

Prioritize potential prohibitions, already-applicable duties, live high-impact systems, misleading transparency, missing monitoring, and material incidents. Build a 30/60/90-day plan with accountable owners, dependencies, acceptance evidence, and legal decision gates.

Give counsel a concise fact pattern and explicit questions rather than asking for a generic review. Use exact intended use, role, affected people, dates, change history, and disputed provisions.

## Safety and permission boundaries

- This skill provides operational readiness support, not legal advice or representation. Require qualified EU counsel for territorial scope, exemptions, role, prohibited/high-risk classification, conformity routes, filings, enforcement exposure, or interpretation disputes.
- Do not contact authorities, submit registrations/notifications, sign codes, make conformity claims, or publish notices without explicit authorization and legal review.
- Minimize personal and special-category data. Use system IDs and aggregated evidence; do not copy production datasets into the assessment.
- Do not infer protected traits, perform biometric categorisation, or run risky system tests on people to complete the checklist.
- Preserve privilege labels and access controls, but do not promise legal privilege.
- Treat suspected prohibited use, serious incidents, rights impacts, misleading disclosures, or missed applicable deadlines as urgent escalation items.
- Check GDPR, product safety, employment, consumer, equality, accessibility, cybersecurity, copyright, sectoral, and Member State law separately; AI Act readiness does not replace them.

## Verification and sign-off

- Re-open every cited official source and capture the access date.
- Cross-check amendments against the base regulation and use the operative legal text over summaries.
- Trace each classification hypothesis to facts, role, article/annex, version, and counsel question.
- Sample evidence against the live system and verify owners/dates rather than accepting policy assertions.
- Have system owners validate facts, security/privacy owners validate controls, and qualified counsel validate legal conclusions.
- Record unresolved uncertainty and the event that triggers reassessment: new use, model/vendor/version, geography, role, material change, incident, or legal update. Treat the age threshold as a backstop, not a substitute for event-triggered review.

## Recovery

If an assessment used stale law, wrong jurisdiction, wrong system version, or an unsupported classification, withdraw the affected conclusion, identify downstream plans/notices/filings that relied on it, preserve the prior report, and issue a dated correction after counsel review. Do not silently rewrite the record. If potential prohibited use or a serious incident emerges, stop further rollout where authorized, preserve evidence, and escalate through the organization's legal and incident-response process.

## Examples

### Hiring assistant

Request: “Assess our résumé-ranking assistant before EU rollout.”

Document provider/deployer roles and EU nexus, screen Article 5 and Annex III employment use, verify current application dates, map high-risk and transparency evidence, identify human-oversight and worker-notice gaps, and send classification and rollout gates to counsel rather than declaring compliance.

### Customer-service chatbot

Request: “What must change in our support bot now that Article 50 applies?”

Verify the current Article 50 text and guidance, determine provider/deployer roles and whether users are already clearly informed, test disclosure timing and accessibility, document synthetic-content features separately, and produce evidence requirements plus counsel questions.

### AI portfolio inventory

Request: “Create a 90-day AI Act readiness plan for our 60 vendor and in-house systems.”

Structurally check the inventory, manually verify its facts, triage urgent/prohibited and already-applicable duties first, group systems by role/use/risk hypothesis, sample evidence, assign owners, and create a risk-based roadmap with legal gates and reassessment triggers.
