---
name: test-strategy
description: Generate a test plan + scaffolding for unit/UI/accessibility/snapshot tests across iOS + watchOS.
allowed-tools: Read, Grep, Glob, Edit, Write
---

Load:
- @docs/testing/README.md
- @docs/testing/unit-tests.md
- @docs/testing/ui-tests.md
- @docs/testing/accessibility-audit.md
- @docs/testing/liquidglass-validation.md

Output:
- Test matrix by layer (HealthKit, WC, ML, UI)
- Recommended test scaffolding files
- Snapshot + accessibility audit steps
