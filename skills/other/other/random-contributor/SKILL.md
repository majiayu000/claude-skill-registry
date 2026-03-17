---
name: random-contributor
description: Pick a random contributor from a GitHub repository using the GitHub API or repository pages (no auth required for public repos).
---

# Random Contributor Skill

Purpose
- Select a uniformly random contributor from a public GitHub repository. Useful for sampling, shoutouts, delegation, or fair assignment among contributors.

What it does
- Uses GitHub REST API (public endpoints) to list contributors for a repo (handles pagination).
- Falls back to scraping the repository's contributors page if API rate limits or CORS prevent API use.
- Returns contributor info: login, name (if available), avatar URL, profile URL, contributions count.

When to use
- Pick a random maintainer or contributor for tasks like "who should review" or "who to credit".
- Should be used only on public repositories.

Prerequisites
- `curl` and `jq` for Bash examples, or Node.js 18+ for JS examples.
- Optional GitHub token (GH_TOKEN) increases rate limits; skill works without it for small repos.

Examples
--------

Bash (uses GitHub API; paginates with per_page=100):

```bash
REPO_OWNER=besoeasy
REPO_NAME=open-skills

# Fetch contributor list (public API). Uses optional GH_TOKEN env for higher rate limit.
AUTH_HEADER=""
if [ -n "${GH_TOKEN:-}" ]; then
  AUTH_HEADER="-H \"Authorization: token ${GH_TOKEN}\""
fi

# Get contributors (first page); for large repos you'd page. Here we do simple pagination loop.
contributors=()
page=1
while true; do
  out=$(eval "curl -fsS ${AUTH_HEADER} \"https://api.github.com/repos/${REPO_OWNER}/${REPO_NAME}/contributors?per_page=100&page=${page}\"")
  count=$(echo "$out" | jq 'length')
  if [ "$count" -eq 0 ]; then break; fi
  logins=$(echo "$out" | jq -r '.[].login')
  while read -r l; do contributors+=("$l"); done <<< "$logins"
  if [ "$count" -lt 100 ]; then break; fi
  page=$((page+1))
done

# Pick random
idx=$((RANDOM % ${#contributors[@]}))
selected=${contributors[$idx]}
echo "$selected"
```

Node.js (recommended: uses native fetch and handles pagination):

```javascript
async function getRandomContributor(owner, repo, token) {
  const headers = {};
  if (token) headers['Authorization'] = `token ${token}`;

  let page = 1;
  const per = 100;
  const all = [];

  while (true) {
    const url = `https://api.github.com/repos/${owner}/${repo}/contributors?per_page=${per}&page=${page}`;
    const res = await fetch(url, { headers });
    if (!res.ok) break;
    const data = await res.json();
    if (!Array.isArray(data) || data.length === 0) break;
    all.push(...data);
    if (data.length < per) break;
    page++;
  }

  if (!all.length) return null;
  const pick = all[Math.floor(Math.random() * all.length)];
  return {
    login: pick.login,
    avatar: pick.avatar_url,
    profile: pick.html_url,
    contributions: pick.contributions
  };
}

// Usage:
// getRandomContributor('besoeasy','open-skills', process.env.GH_TOKEN).then(console.log)
```

Agent prompt
------------

"Find a random contributor for {owner}/{repo}. Use the GitHub API; if API rate limits block you, fall back to scraping the contributors page. Return JSON: {login, name?, avatar, profile, contributions}."

Notes & Caveats
- For very large repos (>1000 contributors) consider streaming or reservoir sampling instead of fetching all contributors at once.
- Respect GitHub API rate limits; provide an option to use GH_TOKEN to increase limits.
- Public repos only; do not attempt to access private repos without appropriate credentials.

See also
- skills/check-crypto-address-balance (example of API usage patterns)

