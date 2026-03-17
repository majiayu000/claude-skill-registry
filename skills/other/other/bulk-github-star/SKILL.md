---
name: bulk-github-star
description: "Star all repositories from a GitHub user automatically. Use when: (1) Supporting open source creators, (2) Bulk discovery of useful projects, or (3) Automating GitHub engagement."
---

# Bulk GitHub Repository Starring

Automate starring all public repositories from any GitHub user with a single command.

## When to use

- User asks to star all repos from a specific GitHub user
- Bulk appreciation for open source contributors
- Discovering and saving all projects from a creator
- Automation workflows for GitHub engagement

## Required tools / APIs

- GitHub CLI (`gh`) with authentication
- No external API keys required (uses GitHub CLI token)

Install GitHub CLI:

```bash
# Ubuntu/Debian
sudo apt-get install -y gh

# macOS
brew install gh

# Alpine (Docker)
apk add github-cli

# Login required
gh auth login
```

## Skills

### star_all_user_repos

Star all public repositories from a GitHub user.

```bash
# Star all repos from a user
USER="besoeasy"
repos=$(gh repo list $USER --limit 100 | grep "^$USER/" | cut -f1)

for repo in $repos; do
  echo "Starring: $repo"
  gh api -X PUT /user/starred/$repo
done

echo "Starred $(echo "$repos" | wc -l) repositories"
```

**Node.js:**

```javascript
async function starAllUserRepos(username) {
  const { execSync } = require('child_process');
  
  // Get all repos for user
  const output = execSync(`gh repo list ${username} --limit 100 --json nameWithOwner`, { encoding: 'utf8' });
  const repos = JSON.parse(output);
  
  let starred = 0;
  for (const repo of repos) {
    const [owner, name] = repo.nameWithOwner.split('/');
    try {
      execSync(`gh api -X PUT /user/starred/${owner}/${name}`, { stdio: 'inherit' });
      console.log(`✓ Starred: ${repo.nameWithOwner}`);
      starred++;
    } catch (err) {
      console.error(`✗ Failed to star ${repo.nameWithOwner}:`, err.message);
    }
  }
  
  console.log(`\nCompleted: ${starred}/${repos.length} repositories starred`);
  return starred;
}

// Usage
// starAllUserRepos('besoeasy');
```

### star_with_filter

Star repos matching specific criteria (e.g., stars threshold, topic).

```bash
# Star only repos with >100 stars
USER="besoeasy"
MIN_STARS=100

gh repo list $USER --limit 100 --json nameWithOwner,stargazerCount | \
jq -r ".[] | select(.stargazerCount >= $MIN_STARS) | .nameWithOwner" | \
while read repo; do
  echo "Starring: $repo ($(gh api /repos/$repo | jq -r '.stargazers_count') stars)"
  gh api -X PUT /user/starred/$repo
done
```

## Rate limits / Best practices

- GitHub API: 5000 requests/hour for authenticated users
- Add delays between requests: `sleep 0.5` to avoid rate limits
- Respect GitHub ToS - don't use for spam or manipulation
- Consider starring selectively rather than bulk for better curation

## Agent prompt

```text
You can bulk star GitHub repositories. When a user asks to star all repos from a GitHub user:

1. Verify GitHub CLI is authenticated: gh auth status
2. Get the list: gh repo list <username> --limit 100
3. Star each using: gh api -X PUT /user/starred/<owner>/<repo>
4. Report count of starred repositories

Always confirm the exact username before executing.
Never star private repos (not accessible via public API anyway).
```

## Troubleshooting

**Error: "gh: command not found"**
- Install GitHub CLI first using package manager

**Error: "not logged in"**
- Run `gh auth login` and follow browser authentication

**Error: "API rate limit exceeded"**
- Wait 1 hour for rate limit reset
- Use `sleep 1` between requests to slow down

**Error: "Not Found"**
- Verify the username is correct
- Check if user exists: `gh user view <username>`

## See also

- [random-contributor](../random-contributor/SKILL.md) — find contributors to appreciate
- [file-tracker](../file-tracker/SKILL.md) — track file changes in starred repos
