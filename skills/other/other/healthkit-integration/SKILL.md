---
name: healthkit-integration
description: HealthKit setup: entitlements, Info.plist strings, authorization, queries, workouts, background delivery.
allowed-tools: Read, Grep, Glob, Edit, Write
---

Load:
- @docs/healthkit/README.md
- @docs/healthkit/authorization.md
- @docs/healthkit/queries.md
- @templates/healthkit-entitlements.entitlements
- @templates/Info.plist.healthkit.md

Output:
- Required entitlements + Info.plist keys
- Swift code for authorization flow (async/await)
- Query patterns (stats / anchored / observer)
- Workout session guidance (if needed)
- Review-safe wording + checklist
