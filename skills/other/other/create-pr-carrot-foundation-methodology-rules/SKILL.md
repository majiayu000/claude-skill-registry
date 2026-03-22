---
name: 'Create Pull Request'
description: 'Analyze changes and create a pull request using the gh CLI with repo conventions.'
---

1. **Analyze changes**: Review all commits on the branch since it diverged from main:

   ```bash
   git log main..HEAD --oneline
   git diff main...HEAD
   ```

2. **Push the branch** if it has not been pushed yet:

   ```bash
   git push -u origin HEAD
   ```

3. **Create the PR** using the `gh` CLI with the required repo flags:

   ```bash
   gh pr create \
     -a @me \
     -r @carrot-foundation/developers \
     --label <label> \
     -R carrot-foundation/methodology-rules \
     -t "<type>(<scope>): <description>"
   ```

   - **Labels**: `feature`, `bug`, `chore`, `docs`, `refactoring`
   - **Title**: Use conventional commit format matching the branch type
   - **Body**: Include a summary section, details of what changed, and a declaration checkbox

4. **Return the PR URL** to the user once created.
