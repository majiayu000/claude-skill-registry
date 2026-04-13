---
name: github-mcp
description: "GitHub MCP Server ile GitHub API erisimi. Repo, issue, PR, code search, release yonetimi."
---

# GitHub MCP Server

## GitHub MCP vs gh CLI

| Ozellik | GitHub MCP | gh CLI |
|---------|-----------|--------|
| Kurulum | MCP server config | brew install gh |
| Auth | PAT token (MCP env) | gh auth login (interactive) |
| Kullanim | Tool call (agent icinden) | Bash komutu |
| Rate limit | REST API limit (5000/h) | Ayni |
| Avantaj | Agent workflow icinde seamless | Terminal scripting |
| Dezavantaj | MCP server calisir olmali | Agent context'ten cikmak lazim |

### Ne Zaman Hangisi

```
GitHub MCP kullan:
  - Agent workflow icinde GitHub islemleri gerektiginde
  - Birden fazla API call zincirlenecekse
  - Structured data response lazimsa

gh CLI kullan:
  - Tek seferlik terminal islemleri
  - PR olusturma/merge (interaktif)
  - Git hook'lari icinde
  - Script/otomasyon icinde
```

## MCP Server Kurulumu

### 1. GitHub PAT Token Olustur

```
GitHub Settings > Developer Settings > Personal Access Tokens > Fine-grained
Gerekli permission'lar:
  - Repository: Read/Write
  - Issues: Read/Write
  - Pull Requests: Read/Write
  - Actions: Read/Write (workflow tetikleme)
  - Webhooks: Read/Write (webhook yonetimi)
  - Organization: Read (org API)
```

### 2. MCP Config (~/.mcp.json)

```json
{
  "mcpServers": {
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_PERSONAL_ACCESS_TOKEN": "<PAT_TOKEN>"
      }
    }
  }
}
```

### 3. Alternatif: Docker ile

```json
{
  "mcpServers": {
    "github": {
      "command": "docker",
      "args": ["run", "-i", "--rm", "-e", "GITHUB_PERSONAL_ACCESS_TOKEN", "ghcr.io/modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_PERSONAL_ACCESS_TOKEN": "<PAT_TOKEN>"
      }
    }
  }
}
```

## Repository Yonetimi

### Repo Olusturma

```
mcp_github.create_repository({
  name: "my-project",
  description: "Proje aciklamasi",
  private: true,
  auto_init: true  // README ile baslat
})
```

### Repo Bilgisi

```
mcp_github.get_repository({
  owner: "username",
  repo: "repo-name"
})
// Response: stars, forks, open_issues, default_branch, language
```

### Fork

```
mcp_github.fork_repository({
  owner: "original-owner",
  repo: "original-repo"
})
```

### Branch Yonetimi

```
// Branch olustur
mcp_github.create_branch({
  owner: "username",
  repo: "repo-name",
  branch: "feature/new-feature",
  from_branch: "main"
})

// Branch listele
mcp_github.list_branches({
  owner: "username",
  repo: "repo-name"
})
```

## Issue Yonetimi

### Issue Olusturma

```
mcp_github.create_issue({
  owner: "username",
  repo: "repo-name",
  title: "Bug: Login form broken",
  body: "## Steps to reproduce\n1. Go to /login\n2. Enter credentials\n3. Click submit\n\n## Expected\nRedirect to dashboard\n\n## Actual\n500 error",
  labels: ["bug", "P1"],
  assignees: ["developer-username"]
})
```

### Issue Listeleme / Filtreleme

```
mcp_github.list_issues({
  owner: "username",
  repo: "repo-name",
  state: "open",
  labels: "bug",
  sort: "created",
  direction: "desc"
})
```

### Issue Guncelleme

```
mcp_github.update_issue({
  owner: "username",
  repo: "repo-name",
  issue_number: 42,
  state: "closed",
  labels: ["bug", "resolved"]
})
```

### Issue Yorum

```
mcp_github.add_issue_comment({
  owner: "username",
  repo: "repo-name",
  issue_number: 42,
  body: "Fixed in PR #45"
})
```

## Pull Request Yonetimi

### PR Olusturma

```
mcp_github.create_pull_request({
  owner: "username",
  repo: "repo-name",
  title: "feat: Add user authentication",
  body: "## Summary\n- JWT auth implementation\n- Login/register endpoints\n\n## Test plan\n- [ ] Unit tests pass\n- [ ] Integration tests pass",
  head: "feature/auth",
  base: "main",
  draft: false
})
```

### PR Review

```
// Review olustur
mcp_github.create_review({
  owner: "username",
  repo: "repo-name",
  pull_number: 45,
  event: "APPROVE",  // APPROVE | REQUEST_CHANGES | COMMENT
  body: "LGTM! Clean implementation."
})
```

### PR Merge

```
mcp_github.merge_pull_request({
  owner: "username",
  repo: "repo-name",
  pull_number: 45,
  merge_method: "squash"  // merge | squash | rebase
})
```

### PR Dosya Degisiklikleri

```
mcp_github.get_pull_request_files({
  owner: "username",
  repo: "repo-name",
  pull_number: 45
})
// Response: filename, status (added/modified/removed), additions, deletions
```

## Code Search

### Repository Icinde Arama

```
mcp_github.search_code({
  query: "useEffect cleanup repo:username/repo-name",
  per_page: 10
})
```

### Global Arama

```
// Dil filtreyle
mcp_github.search_code({
  query: "rate limiter language:typescript stars:>100"
})

// Organizasyon icinde
mcp_github.search_code({
  query: "database migration org:my-org"
})
```

### Arama Operatorleri

```
repo:owner/name       # Spesifik repo
org:organization      # Organizasyon icinde
path:src/utils        # Path filtresi
filename:config.ts    # Dosya adi
extension:py          # Uzanti
language:typescript   # Dil
stars:>100            # Minimum star
size:>1000            # Minimum byte
```

## Actions Workflow

### Workflow Tetikleme

```
mcp_github.create_workflow_dispatch({
  owner: "username",
  repo: "repo-name",
  workflow_id: "deploy.yml",
  ref: "main",
  inputs: {
    environment: "production",
    version: "v1.2.3"
  }
})
```

### Workflow Runs Listeleme

```
mcp_github.list_workflow_runs({
  owner: "username",
  repo: "repo-name",
  workflow_id: "ci.yml",
  status: "completed",
  per_page: 5
})
```

### Workflow Run Loglari

```
mcp_github.get_workflow_run_logs({
  owner: "username",
  repo: "repo-name",
  run_id: 12345
})
```

## Release Management

### Release Olusturma

```
mcp_github.create_release({
  owner: "username",
  repo: "repo-name",
  tag_name: "v1.2.3",
  name: "Release v1.2.3",
  body: "## What's Changed\n- feat: User auth (#42)\n- fix: Login redirect (#45)\n\n## Breaking Changes\nNone",
  draft: false,
  prerelease: false
})
```

### Release Listeleme

```
mcp_github.list_releases({
  owner: "username",
  repo: "repo-name",
  per_page: 10
})
```

### Latest Release

```
mcp_github.get_latest_release({
  owner: "username",
  repo: "repo-name"
})
```

## Webhook Yonetimi

### Webhook Olusturma

```
mcp_github.create_webhook({
  owner: "username",
  repo: "repo-name",
  config: {
    url: "https://my-server.com/webhook",
    content_type: "json",
    secret: "webhook-secret-123"
  },
  events: ["push", "pull_request", "issues"],
  active: true
})
```

### Webhook Events

| Event | Ne Zaman | Kullanim |
|-------|----------|----------|
| push | Commit push | CI/CD tetikle |
| pull_request | PR acildi/kapandi | Review notify |
| issues | Issue degisti | Triage bot |
| release | Release yayinlandi | Deploy tetikle |
| workflow_run | Action tamamlandi | Status notify |
| star | Repo star'landi | Analytics |

## Organization & Team API

### Org Bilgisi

```
mcp_github.get_organization({
  org: "my-organization"
})
```

### Team Listeleme

```
mcp_github.list_teams({
  org: "my-organization"
})
```

### Team Members

```
mcp_github.list_team_members({
  org: "my-organization",
  team_slug: "backend-team"
})
```

### Org Repo'lari

```
mcp_github.list_org_repos({
  org: "my-organization",
  type: "all",
  sort: "updated"
})
```

## Rate Limiting

### Limitler

| Auth Tipi | Limit | Reset |
|-----------|-------|-------|
| PAT (authenticated) | 5000 req/h | 1 saat |
| Unauthenticated | 60 req/h | 1 saat |
| Search API | 30 req/min | 1 dakika |
| GraphQL | 5000 points/h | 1 saat |

### Rate Limit Kontrol

```
mcp_github.get_rate_limit()
// Response: { limit, remaining, reset_at }
```

### Best Practices

```
1. Conditional requests (If-None-Match header) kullan
2. Pagination ile kucuk sayfalarda cek (per_page: 30)
3. Search API'yi 30 req/min altinda tut
4. 403 + "rate limit exceeded" alirsan reset_at kadar bekle
5. Webhook kullan (polling yerine event-driven)
6. GraphQL kullan (birden fazla REST call yerine tek query)
```

## Workflow Ornekleri

### Yeni Feature Workflow

```
1. Issue olustur (task tanimla)
2. Branch olustur (feature/X)
3. Kod yaz, commit et
4. PR olustur (issue'ya referans ver)
5. Review iste
6. Merge et (squash)
7. Release olustur (tag ile)
```

### Bug Fix Workflow

```
1. Issue olustur (bug raporu)
2. Branch olustur (fix/X)
3. Fix yaz, test ekle
4. PR olustur (Fixes #issue-number)
5. CI gectigini dogrula
6. Merge et
7. Issue otomatik kapanir
```

### CI/CD Tetikleme

```
1. Push event -> CI workflow calisir
2. PR event -> Test + lint + security scan
3. Release event -> Deploy workflow calisir
4. Workflow dispatch -> Manuel deploy
```

## Anti-Patterns

| Anti-Pattern | Dogru Yol |
|-------------|-----------|
| PAT'i koda gomme | .env veya MCP config env |
| Tum permission'lari ver | Minimum gerekli scope |
| Polling ile status kontrol | Webhook kullan |
| Buyuk sayfa boyutu (100+) | per_page: 30, pagination |
| Rate limit'i yoksay | get_rate_limit ile kontrol |
| Force push main'e | Branch protection + PR |
