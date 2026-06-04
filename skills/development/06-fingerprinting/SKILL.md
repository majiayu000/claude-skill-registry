---
name: fingerprinting
description: Identify exact technology stack, frameworks, versions, and CMS on live hosts. Use when the user has a live host list and needs to know what's running before choosing vuln classes to test.
metadata:
  type: skill
  phase: recon
  tools: [httpx, whatweb, wappalyzergo, retire.js, nuclei]
---

# Tech Stack Fingerprinting

> Knowing it's Spring Boot 2.5 → CVE-2022-22965 candidate. Knowing it's "Java" → useless.

## When to invoke

**Trigger phrases:**
- "what's running on X"
- "fingerprint this host"
- "tech stack of target"
- "version of framework"

## What we identify

| Layer | Signals | Tools |
|---|---|---|
| Web server | Nginx, Apache, IIS, Caddy | httpx, nmap, headers |
| Backend lang | Node, Python, Java, .NET, Go, PHP, Ruby | headers, cookies, errors |
| Framework | Express, Django, Spring, Rails, Laravel, FastAPI | error pages, default routes |
| CMS | WordPress, Drupal, Joomla, Ghost | paths, scripts, meta |
| Frontend | React, Vue, Angular, Svelte, Next.js | JS files, bundle structure |
| API style | REST, GraphQL, gRPC, SOAP | endpoints, schemas |
| Cloud provider | AWS, GCP, Azure, Cloudflare, Fastly | DNS, headers, error pages |
| WAF | Cloudflare, Akamai, Imperva, AWS WAF | headers, behavior |
| Dependencies | npm, JS libraries, CDN versions | retire.js |

## Step-by-Step Workflow

### 1. Quick scan with httpx

```bash
# tech-detect uses Wappalyzer logic
echo "https://app.target.com" | httpx -tech-detect -title -web-server -status-code -json | jq .

# Bulk on alive hosts:
cat live.txt | httpx -tech-detect -web-server -json | tee tech-detected.jsonl
```

Output sample:
```json
{
  "url": "https://app.target.com",
  "tech": ["React", "Next.js:13.4", "Cloudflare", "Webpack"],
  "webserver": "cloudflare",
  "title": "Target App"
}
```

### 2. Deep scan with WhatWeb

```bash
# WhatWeb has wider plugin DB than httpx
whatweb -v --color=never -a 3 "https://app.target.com"

# Aggression levels:
#  1 = passive (just GET /)
#  3 = standard (default)
#  4 = heavy (lots of requests)
```

### 3. Header forensics

```bash
# Manual but precise:
curl -sI "https://app.target.com" | grep -iE "server|x-powered-by|x-aspnet|x-runtime|via|cf-ray|x-amz-|x-azure-"

# Examples of what to look for:
# X-Powered-By: PHP/7.4.3
# X-AspNet-Version: 4.0.30319
# X-Runtime: 0.045821 → Ruby on Rails
# Server: nginx/1.18.0 (Ubuntu)
# Via: 1.1 vegur → Heroku
# X-Vercel-Id → Vercel hosting
# X-Amz-Cf-Id → AWS CloudFront
```

### 4. Cookie fingerprinting

```bash
curl -sI "https://app.target.com" | grep -i "set-cookie"

# Cookie names reveal stack:
# PHPSESSID → PHP
# JSESSIONID → Java
# .AspNet.ApplicationCookie → ASP.NET
# _csrf, _session → Rails
# laravel_session → Laravel
# connect.sid → Express
# session → Flask/generic
# next-auth.session-token → Next.js + NextAuth
```

### 5. Error page fingerprinting

```bash
# Common error-page paths to fingerprint stack
for path in "/foo/bar" "/api/random-uuid" "/404-this-doesnt-exist" "/.env" "/server-status"; do
    echo "=== $path ==="
    curl -s "https://app.target.com$path" | head -30
    echo
done

# Look for:
# - "Whitelabel Error Page" → Spring Boot
# - "Application Error" + heroku → Heroku app
# - "Cannot GET /foo" → Express
# - "DEBUG = True" Django stack trace → DEBUG mode (CRITICAL bug!)
# - "Internal Server Error" + Werkzeug → Flask
```

### 6. Frontend stack from JS bundle

```bash
# Get JS file URLs
curl -s "https://app.target.com" | grep -oE 'src="[^"]+\.js"' | sed 's/src="//;s/"$//'

# Check for framework fingerprints:
# react-dom.production.min.js → React
# vue.runtime.min.js → Vue
# @angular/core → Angular
# next/router → Next.js
# nuxt → Nuxt
# svelte → Svelte
# remix-run → Remix

# retire.js — find outdated JS libs
retire --jsrepo https://retirejs.github.io/retire.js/repository/jsrepo.json --js https://app.target.com
```

### 7. Nuclei tech-detect templates

```bash
# nuclei has hundreds of tech-detect templates
nuclei -u "https://app.target.com" -tags tech -silent

# Targeted: known versionable software
nuclei -u "https://app.target.com" -t http/technologies/ -silent

# Look for version disclosure
nuclei -u "https://app.target.com" -tags version -silent
```

### 8. Cloud / CDN detection

```bash
# DNS shows CNAME → CDN/provider
dig +short "app.target.com"

# Common CNAMEs:
# *.cloudfront.net → AWS CloudFront
# *.azureedge.net → Azure CDN
# *.fastly.net → Fastly
# *.cloudflare.com → Cloudflare (often via A record + IPs in CF range)
# *.ngrok.io → ngrok (developer tunnel — interesting!)
# *.herokuapp.com → Heroku
# *.vercel.app → Vercel
# *.netlify.app → Netlify
# *.s3.amazonaws.com → S3 bucket (check ownership = takeover candidate)
# *.github.io → GitHub Pages (takeover candidate)
```

### 9. WAF detection

```bash
# wafw00f
pip install wafw00f
wafw00f "https://app.target.com"

# Manual:
# - 403 with "challenge" page → Cloudflare
# - 403 + cf-ray header → Cloudflare
# - 403 + akamai-x-cache header → Akamai
# - 406 + X-Iinfo → Imperva
# - 403 + X-Sucuri-ID → Sucuri
```

## Output template

```yaml
target: app.target.com
fingerprint_date: 2026-06-02

infrastructure:
  cdn: Cloudflare
  ip: 104.21.x.x (CF IP)
  origin_ip: unknown (CF protected)
  waf: Cloudflare WAF

web_server:
  product: nginx
  version: 1.18 (inferred from defaults)
  os: Ubuntu 20.04 LTS

backend:
  language: Node.js
  framework: Next.js 13.4
  evidence: |
    - X-Powered-By: Next.js
    - JS bundle: _next/static/
    - Headers: x-vercel-id (suggests Vercel hosting backed by Next.js)

frontend:
  framework: React 18.2
  bundler: Webpack 5
  state_mgmt: Redux Toolkit (from JS analysis)

api:
  style: REST + GraphQL
  rest_base: /api/v3
  graphql_endpoint: /api/graphql
  evidence: discovered in main.js bundle

authentication:
  type: NextAuth.js with custom OAuth provider
  cookie: next-auth.session-token
  jwt: yes (verified via JWT decoding)

cms: none

interesting_tech:
  - GraphQL endpoint exposed (introspection?)
  - NextAuth handles session — check JWT signing
  - Vercel serverless — different attack surface (cold starts, env vars)
  - WebSocket on /api/ws — possible RT data exchange
```

## Tech → vuln class lookup

Use this to decide what to hunt next:

| Tech Found | Try These Skills |
|---|---|
| WordPress | nuclei wordpress templates, wpscan, REST API authcheck |
| GraphQL | `[[graphql]]` — introspection, batching, depth |
| JWT in cookies | `[[jwt-attacks]]` — alg=none, key confusion |
| OAuth visible | `[[oauth-oidc]]` — redirect_uri, state |
| File upload UI | `[[file-upload]]` |
| Multi-tenant URLs | `[[idor-hunting]]` |
| Search/filter inputs | `[[sqli]]`, `[[ssti]]` |
| URL fetcher / webhook | `[[ssrf]]` |
| Spring Boot | CVE checks (RCE history), actuator endpoints |
| Old Drupal | CVE-2018-7600 Drupalgeddon, etc. |
| Old WordPress plugins | nuclei wordpress-CVEs templates |
| Outdated jQuery | retire.js → CVEs |
| Exposed Swagger/OpenAPI | API enumeration goldmine |

## Cross-references

- `[[asset-discovery]]` — runs before this
- `[[js-analysis]]` — deeper JS endpoint mining
- `[[content-discovery]]` — fuzz paths based on tech
- `[[nuclei]]`-style scanning — match templates to fingerprinted stack

## Common pitfalls

1. **Trusting `Server:` header alone.** It's often reverse-proxy, not the actual app.
2. **Missing JS-based SPA detection.** SPA = different attack surface.
3. **Not checking *all* origin endpoints.** Same domain may have multiple stacks behind path-based routing.
4. **Treating Cloudflare as the app.** WAF can mislead — try origin IP if findable.
5. **Skipping the error pages.** Stack traces > Wappalyzer fingerprints any day.

## Pro tips

- **Bring up devtools in the browser.** Network tab shows headers + cookies in seconds.
- **Note `_next/`, `__nuxt/`, `_remix/` paths.** They signal SSR frameworks → unique bug classes.
- **Save fingerprint to `loot/<target>/fingerprint.yaml`.** Re-use for re-tests.
- **Run fingerprinting weekly on active targets.** Tech stack updates create new attack windows.
