---
name: release
description: Detect changes in skills/agents, ask about version bumps, update frontmatter versions, and deploy individual repos to GitHub.
---

# Release Workflow

Detect changes, bump versions, and deploy individual plugin repos.

## Step 1: Generate dist-repos

```bash
./scripts/generate-individual-repos.sh
```

## Step 2: Detect changes

Compare each generated repo against the last deployed state in `.repo-cache/`:

```bash
for repo_dir in dist-repos/*/; do
  repo_name=$(basename "$repo_dir")
  cache_dir=".repo-cache/$repo_name"
  if [ -d "$cache_dir" ]; then
    changes=$(diff -rq --exclude='.git' "$cache_dir" "$repo_dir" 2>/dev/null)
    if [ -n "$changes" ]; then
      echo "CHANGED: $repo_name"
      echo "$changes"
    fi
  else
    echo "NEW: $repo_name"
  fi
done
```

If no repos have changes, tell the user "Nothing to release" and stop.

## Step 3: Show change summary

For each changed repo, show a brief summary of what changed (files added/modified/removed).

## Step 4: Ask about version bumps

For each changed repo, use AskUserQuestion to ask the user what kind of version bump to apply:

- **patch** (1.0.0 -> 1.0.1): Bug fixes, minor content updates
- **minor** (1.0.0 -> 1.1.0): New content, features, or significant updates
- **major** (1.0.0 -> 2.0.0): Breaking changes or complete rewrites

## Step 5: Update source frontmatter

For each repo that needs a bump, update the `version` field in the source file:

- Skills: `skills/<name>/SKILL.md`
- Agents: `agents/<name>.md`

Use the Edit tool to change the `version:` line in the YAML frontmatter.

Compute the new version by parsing the current `version: X.Y.Z` and incrementing the appropriate part:

- patch: increment Z
- minor: increment Y, reset Z to 0
- major: increment X, reset Y and Z to 0

## Step 6: Bump main plugin.json

Ask the user if they want to bump the main `.claude-plugin/plugin.json` version too (patch/minor/major/skip). Update the `"version"` field if they choose to bump.

## Step 7: Regenerate dist-repos

Run the generate script again so dist-repos picks up the new versions:

```bash
./scripts/generate-individual-repos.sh
```

## Step 8: Commit version bumps

Stage and commit all version changes in the main repo:

```bash
git add skills/ agents/ .claude-plugin/plugin.json
git commit -m "Bump versions for release

Co-Authored-By: Claude <noreply@anthropic.com>"
```

## Step 9: Deploy

Run the deploy script to push individual repos to GitHub:

```bash
./scripts/deploy-individual-repos.sh
```

## Step 10: Push main repo

```bash
git push origin main
```

Show the user a summary of what was released with the new version numbers.
