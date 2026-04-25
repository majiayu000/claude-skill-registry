---
name: motherduck-security-governance
description: Explain MotherDuck security, governance, and access-control patterns. Use when a security_compliance_owner, technical_owner, or application_builder is asking about residency, access boundaries, service accounts, isolation, sharing, or governance posture.
license: MIT
---

# Security and Governance

Use this skill when the user is evaluating whether MotherDuck can meet their security, governance, and deployment requirements. This is a workflow skill focused on control boundaries and safe patterns.

## Source Of Truth

- Prefer current MotherDuck public trust, security, pricing, and product documentation.
- If the MotherDuck MCP `ask_docs_question` feature is available, use it first.
- Verify claims against live public materials before making compliance or commercial assertions.

## Default Posture

- Prefer service accounts for production systems, not personal tokens.
- Keep credentials in backend-controlled secrets, not browsers or hardcoded notebooks.
- Prefer structural isolation over query-time tenant filtering for serious B2B or CFA workloads.
- Treat region and residency as first-class architectural constraints that require current public confirmation.
- Be explicit about whether the boundary is a share, a Dive, a database, or a full application.
- Separate documented product guarantees from architectural recommendations and assumptions in the final answer.

## Workflow

1. Identify where credentials live and who administers them.
2. Define the actual isolation boundary: account, database, schema, or query filter.
3. Determine who can read, write, share, or administer the data.
4. Check whether residency, compliance, or contractual guarantees are part of the requirement.
5. Use only publicly documented security anchors unless the user has current commercial documentation in hand.

## Open Next

- `references/SECURITY_GOVERNANCE_PLAYBOOK.md` for public security anchors, service-account posture, residency framing, sharing boundaries, and what not to overstate

## Related Skills

- `motherduck-connect` for secure token handling and endpoint selection
- `motherduck-explore` when governance depends on what data is actually present and how it is partitioned
- `motherduck-share-data` when the design includes governed data distribution
