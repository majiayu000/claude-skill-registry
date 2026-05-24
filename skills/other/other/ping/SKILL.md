---
name: ping
description: Smoke-test skill that confirms the Mycelium plugin loaded correctly. Returns a deterministic marker string for plugin-shape validation. Not for end-user invocation in normal use.
---

# Ping (smoke-test only)

When invoked, respond with exactly this single line and nothing else:

```
MYCELIUM_PLUGIN_LOAD_OK
```

This is a plugin-shape marker, not a version assertion — it confirms the plugin packaging works end-to-end (manifest → marketplace → install → namespaced invocation). The version a user is actually running comes from `/plugin list` or `plugin.json#version`, not this marker. (The marker was previously version-suffixed, which created drift: it stayed pinned at `_v0.20.0` while plugin.json moved through 10 patches. Detected during 2026-05-09 dogfood.)

For real Mycelium skills, see the parent `skills/` directory once migration completes.
