---
name: 'Create Branch'
description: 'Create a new git branch from latest main using the naming convention.'
---

1. **Pull latest main**:

   ```bash
   git fetch origin main
   git checkout main
   git pull origin main
   ```

2. **Create the branch** using the naming pattern `<type>/<short-description>`:

   ```bash
   git checkout -b <type>/<short-description>
   ```

   - Use kebab-case for the description
   - Types match conventional commit types: `feat`, `fix`, `docs`, `style`, `refactor`, `perf`, `test`, `chore`, `revert`
   - Examples:
     - `feat/add-vehicle-validation`
     - `fix/geolocation-precision-edge-case`
     - `chore/update-dependencies`
     - `refactor/extract-shared-helpers`

3. **Verify** you are on the new branch with `git branch --show-current`.
