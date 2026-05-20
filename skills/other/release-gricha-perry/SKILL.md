---
name: release
description: Cut a new release - bump version, commit, tag, and push to trigger CI publish
---

# Release Skill

Cut a new Perry release. CI builds and publishes on `v*` tags.

## Steps

1. **Update version** in `package.json`

2. **Commit and push**:
   ```bash
   git add package.json
   git commit -m "release v<x.y.z>"
   git push origin main
   ```

3. **Tag and push**:
   ```bash
   git tag v<x.y.z>
   git push origin v<x.y.z>
   ```

That's it. CI handles validation, build, and publish.
