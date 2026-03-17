---
name: hello-skillset
description: Example Skillset that bundles two minimal skills for testing.
version: 0.1.0
skillset: true
dependencies:
  - ./skills/hello-skill-inline
  - ./skills/echo-skill-inline
---

# hello-skillset (example)

This is an **example Skillset**. Installing it should also install its bundled dependencies inside the Skillset folder.

## Try it locally

```bash
skild install ./examples/hello-skillset
```

