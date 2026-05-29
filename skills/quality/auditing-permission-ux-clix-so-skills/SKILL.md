---
name: auditing-permission-ux
display-name: Auditing Permission UX
short-description: Permission UX audit
description: Audits notification permission request flows. Use when reviewing or improving permission prompts, settings paths, or denial handling.
user-invocable: true
---

# Auditing Permission UX

Use this skill to audit how a mobile app requests notification permission and guides
users to settings, then produce actionable improvements based on Apple and Android
best practices.

## What this skill does

- Reviews permission timing, context, and explanation quality
- Checks denial handling and settings recovery paths
- Flags platform-specific risks (iOS vs Android)
- Produces a structured audit report with fixes

## Workflow

```
Permission UX audit progress:

- [ ] 1) Confirm minimum inputs (platforms, flow, current UX)
- [ ] 2) Audit current flow (map prompts, copy, and settings paths)
- [ ] 3) Produce audit report (findings + fixes)
- [ ] 4) Verify improvements (ensure UX changes align with platform rules)
```

## 1) Confirm the minimum inputs

Ask only what is needed:

- **Platforms**: iOS, Android, or both
- **Entry points**: where the app asks for permission
- **Prompt timing**: first launch, after action, onboarding step, etc.
- **Primer**: is there an in-app explanation before the system prompt
- **Settings path**: how users enable later after denial
- **Denial handling**: how the app behaves if permission is denied

## 2) Audit the current flow

Document the current permission flow directly from the app:

- Where the permission prompt appears and what precedes it
- What copy is shown to explain value
- How the app behaves after deny or dismiss
- How users can enable notifications later

## 3) Produce the audit report

Output a concise report in markdown with:

- **Findings**: each gap mapped to best practice
- **Risk**: what the user impact is
- **Fix**: concrete UX change
- **Platform notes**: iOS-only or Android-only specifics

Optional: generate a report template:

```bash
bash skills/auditing-permission-ux/scripts/generate-permission-ux-audit-report.sh .mobile/permission-ux-audit.md
```

## 4) Verify improvements

Confirm:

- Prompt timing is contextual (not forced on first launch)
- Primer explains value clearly and is dismissible
- Denied users can still use the app
- Settings path is discoverable and clear
- Android importance/channel strategy is not misleading

## Progressive Disclosure

- **Level 1**: This `SKILL.md`
- **Level 2**: `references/`
- **Level 3**: `examples/` (optional)
- **Level 4**: `scripts/` (execute; do not load)

## References

- `references/permission-ux-best-practices.md`
