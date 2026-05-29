---
name: delivery.release_notes
phase: delivery
roles:
  - Product Manager
  - Product Marketing
description: Generate structured release notes tailored to the specified audience and highlighting value, rollout, and risks.
variables:
  required:
    - name: version
      description: Release version or identifier.
    - name: highlights
      description: Key features or changes included in the release.
    - name: audience
      description: Target audience such as customers, internal teams, or executives.
  optional:
    - name: rollout_plan
      description: Summary of rollout phases or flags.
    - name: risks
      description: Notable risks or watchpoints to communicate.
outputs:
  - Release summary and value statement.
  - Detailed change list grouped by theme.
  - Rollout, support, and risk communication sections.
---

# Purpose
Ensure release communications are consistent, customer-centric, and aligned with operational readiness plans.

# Pre-run Checklist
- ✅ Confirm feature list with engineering and QA.
- ✅ Gather customer-facing messaging from product marketing.
- ✅ Align with support and success teams on rollout logistics.

# Invocation Guidance
```bash
codex skills run delivery.release_notes \
  --vars "version={{version}}" \
         "highlights={{highlights}}" \
         "audience={{audience}}" \
         "rollout_plan={{rollout_plan}}" \
         "risks={{risks}}"
```

# Recommended Input Attachments
- Changelog or issue tracker export.
- Screenshots or GIFs of key features.
- Support playbooks or macros.

# Claude Workflow Outline
1. Summarize release context and audience needs.
2. Craft a value-oriented summary explaining why the release matters.
3. List changes grouped by theme, including links or callouts for visuals.
4. Outline rollout plan, support readiness, and success metrics.
5. Highlight risks, mitigations, and action items for partner teams.

# Output Template
```
# Release Notes — {{version}}

## Summary
...

## What's New
- Theme:
  - Change:

## Rollout & Enablement
- Rollout Plan:
- Success Metrics:
- Support Readiness:

## Risks & Watchpoints
- Risk:
- Mitigation:
- Owner:
```

# Follow-up Actions
- Share notes in the release communication channels and status pages.
- Update customer documentation or knowledge base articles.
- Collect feedback post-launch and iterate on messaging.
