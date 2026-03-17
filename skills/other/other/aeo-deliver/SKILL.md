---
name: aeo-deliver
description: Full AEO client delivery pipeline using agent teams. Coordinates audit, playbook, content optimization, and reporting with persistent context.
disable-model-invocation: true
---

# AEO Client Delivery Pipeline

Run the full client delivery pipeline using an agent team. Each worker keeps their context so findings can be clarified without restarting.

## Team Structure

Create an agent team called "aeo-delivery" with these teammates:

### auditor (general-purpose agent)
**Role:** Run full AEO audit with 10-run consistency tests.
**Skills to preload:** Load the aeo-auditor agent instructions.
**MCP servers needed:** aeo-audit
**Tasks:**
1. Read `aeo-protocol-sop.md` (lines 1-200 for methodology, 850-900 for First 50 Words, 3348-3432 for consistency test)
2. Collect brand info and dream queries from the lead
3. Run the full 8-query brand audit via `run_brand_audit` MCP tool
4. Run 10-run consistency tests on the top 3-5 dream queries
5. Check the brand's website for First 50 Words compliance
6. Write the audit report to `clients/[client]/[client]-aeo-audit.md`
7. Report key findings to the team

### strategist (general-purpose agent)
**Role:** Convert audit findings into executable playbook.
**Skills to preload:** Load the playbook-creator agent instructions.
**Tasks (run AFTER auditor completes):**
1. Read the audit report
2. Message the auditor if any findings are unclear
3. Create a prioritized, week-by-week implementation playbook
4. Group actions by type (technical, content, citations, monitoring)
5. Write playbook to `clients/[client]/[client]-aeo-playbook.md`
6. Report the playbook summary to the team

### writer (general-purpose agent)
**Role:** Optimize website copy per the playbook.
**Skills to preload:** Load the content-optimizer agent instructions.
**Tasks (run AFTER strategist completes):**
1. Read the playbook
2. Message the strategist about content priorities
3. Check the client's sitemap for existing pages
4. Optimize/rewrite pages following the First 50 Words Rule
5. Write copy files to `clients/[client]/pages/`
6. Create comparison pages (vs-[competitor].md) if recommended

## Workflow

1. Client intake done first (you collect dream queries + brand facts)
2. Create the team: auditor runs the full audit
3. When audit completes, strategist creates the playbook
4. When playbook is ready, writer optimizes content pages
5. Review everything, then run `/client-report` for the final deliverable

## Input

Provide the brand name, website URL, category, and any dream queries:

$ARGUMENTS
