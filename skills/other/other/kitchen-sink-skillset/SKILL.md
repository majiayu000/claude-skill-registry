---
name: kitchen-sink-skillset
description: Example Skillset that demonstrates inline + GitHub + registry dependencies.
version: 0.1.0
skillset: true
dependencies:
  # Inline (bundled) dependencies: installed inside this Skillset directory.
  - ./skills/hello-skill-inline
  - ./skills/echo-skill-inline

  # GitHub dependency (degit shorthand): installed as an external dependency at top-level.
  # This points back to this repo’s example skill, to keep the demo deterministic.
  - github:Peiiii/skild/examples/hello-skill

  # Registry dependency: replace __REGISTRY_SCOPE__ with your publisher handle (or let the smoke script do it).
  - "@__REGISTRY_SCOPE__/registry-dep-skill@^0.1.0"
---

# kitchen-sink-skillset (example)

This Skillset exists to exercise **all dependency types** in one place:

- Inline (relative) dependencies (bundled)
- GitHub dependencies
- Registry dependencies
