<!-- ⚠️ STARTERPACK CORE — DO NOT MODIFY. This file is managed by the starterpack. -->
---
name: upgrade-starterpack
description: Upgrade the starterpack with AI assistance
---

# Upgrade Starterpack

Run the starterpack upgrade with AI-assisted conflict resolution.

## Steps

1. Run the analyze command:
   ```bash
   bash scripts/_core/core-update.sh --analyze
   ```

2. Review the output for:
   - Version change (current → target)
   - Breaking changes in upgrade notes
   - Local modifications that will be overwritten
   - Required migrations

3. If local modifications exist:
   - Note which files have local changes
   - Determine if changes should be preserved
   - Plan to re-apply them after upgrade

4. Enter plan mode to create upgrade plan for user approval

5. After user approves, execute:
   - Run `bash scripts/_core/core-update.sh` to apply upgrade
   - Re-apply preserved local modifications
   - Run validation commands

6. Post-upgrade validation:
   ```bash
   npm run lint:frontend && npm run lint:backend
   npm run typecheck:frontend
   bash scripts/_core/validate-core-files.sh
   ```
