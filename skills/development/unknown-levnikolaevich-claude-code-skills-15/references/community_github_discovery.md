<!-- SOURCE-OF-TRUTH: shared/references/community_github_discovery.md. Edit ONLY here; run `node tools/marketplace/shared.mjs sync` -->

# GitHub Discovery Protocol

Phase 0 reference for all community engagement skills.
Dynamically discovers repository context — no hardcoded IDs required.

## Step 1: Detect Repository

```bash
REPO_SLUG=$(gh repo view --json owner,name --jq '.owner.login + "/" + .name')
REPO_OWNER=$(echo "$REPO_SLUG" | cut -d'/' -f1)
REPO_NAME=$(echo "$REPO_SLUG" | cut -d'/' -f2)
```

**Gate:** If `gh` not found → block: "Install GitHub CLI: https://cli.github.com/"
**Gate:** If command fails → block: "Run `gh auth login` first."

## Step 2: Discover IDs, Categories, Authenticated User

```bash
gh api graphql -f query='
  query($owner: String!, $name: String!) {
    viewer { login }
    repository(owner: $owner, name: $name) {
      id
      hasDiscussionsEnabled
      discussionCategories(first: 20) {
        nodes { id name }
      }
    }
  }
' -f owner="$REPO_OWNER" -f name="$REPO_NAME"
```

## Step 3: Build Discovery Context

Parse the GraphQL response into a mental model:

| Field | Source | Used by |
|-------|--------|---------|
| `repo.owner` | Step 1 | All skills (URLs, `--repo` flag) |
| `repo.name` | Step 1 | All skills (URLs, `--repo` flag) |
| `repo.id` | `repository.id` | Mutation skills (GraphQL create/update) |
| `discussionsEnabled` | `repository.hasDiscussionsEnabled` | Gate check |
| `categories` | `discussionCategories.nodes[]` → map `{name: id}` | Announcer (Announcements), debater (Ideas, Polls) |
| `maintainer` | `viewer.login` | Triage skill (maintainer detection) |

## Step 4: Gate Checks

| Check | Condition | Action |
|-------|-----------|--------|
| Discussions enabled | `hasDiscussionsEnabled == false` | Block: "Enable Discussions at Settings > General > Features > Discussions" |
| Required category exists | Category name not in `nodes[]` | Warn: "Category '{name}' not found. Create it in repo Settings > Discussions > Categories" |
| gh authenticated | Step 1 fails | Block: "Run `gh auth login` first" |

## Step 5: Load Strategy

1. Check if `docs/community_engagement_strategy.md` exists in target project
2. If found → load as strategy source
3. If not found → load `references/community_strategy_template.md`

## Notes

- Discovery runs once per skill invocation (~1s total)
- `viewer.login` returns the authenticated GitHub user — in most cases this IS the maintainer
- If repo has multiple maintainers, override via project-local strategy doc
