---
name: cloudflare-management
description: |
  Use when working with Cloudflare services (Workers, Pages, R2, D1, KV, DNS, SSL, WAF, Zero Trust, etc.).
  Provides comprehensive management via Wrangler CLI (primary) and direct REST API access for services
  not covered by Wrangler (DNS, SSL certificates, load balancers, security rules, analytics).
  Triggers: "deploy worker", "manage cloudflare", "cloudflare dns", "wrangler setup", "r2 bucket",
  "d1 database", "cloudflare api", "cf pages", "cloudflare ssl", "waf rules".
---

# Cloudflare Management

Comprehensive Cloudflare service management using **Wrangler CLI** (primary tool) and **REST API** (for advanced/non-Wrangler services).

## Tool Selection

| Service | Primary Tool | Alternative |
|---------|--------------|-------------|
| Workers, Pages, KV, R2, D1, Queues, AI, Vectorize, Hyperdrive | **Wrangler CLI** | - |
| DNS, SSL/TLS, Zones, Load Balancers | **REST API scripts** | Terraform |
| WAF, Rate Limiting, Firewall Rules, Bot Management | **REST API scripts** | Terraform |
| Zero Trust, Access, Tunnels | **cloudflared CLI** + REST API | - |
| Analytics, Logs | **GraphQL API** + REST API | Dashboard |

**Decision Flow**:
1. **Developer Platform** (Workers/Pages/Storage) → Use Wrangler
2. **DNS/Zone/SSL** → Use `cf-zone-management.sh` script
3. **Security (WAF/Firewall)** → Use `cf-security.sh` script
4. **Custom/Advanced** → Use `cf-api.sh` script with REST API

## Quick Start

### 1. Install Wrangler

```bash
# Check if installed
which wrangler

# If not installed (or outdated)
npm install -g wrangler@latest

# Verify
wrangler --version
```

### 2. Authenticate

**Interactive (recommended for local dev)**:
```bash
wrangler login
# Opens browser for OAuth
```

**API Token (recommended for CI/CD)**:
```bash
# Set environment variables (see references/authentication.md for token creation)
export CLOUDFLARE_API_TOKEN="your_token_here"
export CLOUDFLARE_ACCOUNT_ID="your_account_id"

# Verify
wrangler whoami
```

### 3. Common Workflows

**Deploy a Worker**:
```bash
# Create new project
npm create cloudflare@latest my-worker

# Or deploy existing
cd my-worker
wrangler deploy
```

**Manage KV Storage**:
```bash
# Create namespace
wrangler kv namespace create MY_KV

# Add to wrangler.toml, then:
wrangler kv key put --namespace-id=<id> "mykey" "myvalue"
wrangler kv key get --namespace-id=<id> "mykey"
```

**Deploy to Pages**:
```bash
wrangler pages deploy ./dist
```

**R2 Bucket Operations**:
```bash
# Create bucket
wrangler r2 bucket create my-bucket

# Upload object
wrangler r2 object put my-bucket/path/file.txt --file=./local-file.txt

# List objects
wrangler r2 object list my-bucket
```

**D1 Database**:
```bash
# Create database
wrangler d1 create my-database

# Run migrations
wrangler d1 migrations apply my-database

# Execute SQL
wrangler d1 execute my-database --command="SELECT * FROM users"
```

## Architecture

```
Cloudflare Management Skill
│
├── Wrangler CLI (Primary)
│   ├── Workers & Pages
│   ├── Storage (KV, R2, D1, Queues)
│   ├── AI & Vectorize
│   └── Development tools (dev, tail, secrets)
│
├── REST API Scripts (Secondary)
│   ├── cf-api.sh (generic wrapper)
│   ├── cf-zone-management.sh (DNS, SSL, zones)
│   └── cf-security.sh (WAF, firewall, rate limits)
│
└── References
    ├── api-surface.md (all 14 API categories)
    ├── wrangler-commands.md (comprehensive CLI reference)
    ├── authentication.md (token setup)
    └── service-guides.md (quick-start patterns)
```

## Wrangler Core Commands

| Command | Purpose | Example |
|---------|---------|---------|
| `wrangler init` | Create new project | `wrangler init my-project` |
| `wrangler dev` | Local development | `wrangler dev` |
| `wrangler deploy` | Deploy to production | `wrangler deploy` |
| `wrangler tail` | Stream logs | `wrangler tail my-worker` |
| `wrangler secret put` | Add secret | `wrangler secret put API_KEY` |
| `wrangler publish` | Legacy deploy (use `deploy`) | - |
| `wrangler whoami` | Check auth | `wrangler whoami` |

For complete command reference, see [references/wrangler-commands.md](references/wrangler-commands.md).

## REST API Access (Non-Wrangler Services)

For services not covered by Wrangler (DNS, SSL, WAF, etc.), use the provided scripts:

### Zone Management
```bash
# List all zones
bash scripts/cf-zone-management.sh zones list

# Create a new zone
bash scripts/cf-zone-management.sh zones create example.com

# Delete a zone
bash scripts/cf-zone-management.sh zones delete example.com

# Get zone details
bash scripts/cf-zone-management.sh zone get example.com

# Get all zone settings
bash scripts/cf-zone-management.sh zone settings example.com

# Purge zone cache
bash scripts/cf-zone-management.sh zone purge-cache example.com
```

### DNS Management
```bash
# List DNS records
bash scripts/cf-zone-management.sh dns list example.com

# Create A record
bash scripts/cf-zone-management.sh dns create example.com A "api" "192.0.2.1"

# Update record
bash scripts/cf-zone-management.sh dns update example.com <record-id> A "api" "192.0.2.2"

# Delete record
bash scripts/cf-zone-management.sh dns delete example.com <record-id>
```

### SSL Certificate Management
```bash
# List certificates
bash scripts/cf-zone-management.sh ssl list example.com

# Get SSL settings
bash scripts/cf-zone-management.sh ssl settings example.com

# Update SSL mode (off, flexible, full, strict)
bash scripts/cf-zone-management.sh ssl update example.com strict
```

### Security Rules
```bash
# List firewall rules
bash scripts/cf-security.sh firewall list example.com

# Create rate limit rule
bash scripts/cf-security.sh ratelimit create example.com "/api/*" 100

# List WAF rules
bash scripts/cf-security.sh waf list example.com
```

### Generic API Calls
```bash
# GET request
bash scripts/cf-api.sh GET zones

# POST request with data
bash scripts/cf-api.sh POST zones/<zone-id>/dns_records '{"type":"A","name":"test","content":"192.0.2.1"}'

# PATCH request
bash scripts/cf-api.sh PATCH zones/<zone-id>/settings/ssl '{"value":"strict"}'
```

## Configuration

### wrangler.toml Structure

See [assets/wrangler.toml.template](assets/wrangler.toml.template) for a comprehensive template.

**Basic structure**:
```toml
name = "my-worker"
main = "src/index.ts"
compatibility_date = "2024-01-01"

# KV namespaces
[[kv_namespaces]]
binding = "MY_KV"
id = "your_namespace_id"

# R2 buckets
[[r2_buckets]]
binding = "MY_BUCKET"
bucket_name = "my-bucket"

# D1 databases
[[d1_databases]]
binding = "DB"
database_name = "my-database"
database_id = "your_database_id"

# Environment variables
[vars]
ENVIRONMENT = "production"

# Routes
routes = [
  { pattern = "example.com/*", zone_name = "example.com" }
]
```

### Environment Variables

Required for authentication (see [references/authentication.md](references/authentication.md)):

```bash
CLOUDFLARE_API_TOKEN=your_token_here
CLOUDFLARE_ACCOUNT_ID=your_account_id
CLOUDFLARE_ZONE_ID=your_zone_id  # For zone-specific operations
```

## Common Patterns

### Multi-Environment Deployment

```toml
# wrangler.toml
[env.staging]
name = "my-worker-staging"
vars = { ENVIRONMENT = "staging" }

[env.production]
name = "my-worker-production"
vars = { ENVIRONMENT = "production" }
```

```bash
# Deploy to staging
wrangler deploy --env staging

# Deploy to production
wrangler deploy --env production
```

### Secret Management

```bash
# Add secret (interactive)
wrangler secret put API_KEY

# Add secret for specific environment
wrangler secret put API_KEY --env production

# List secrets (names only, values never exposed)
wrangler secret list
```

### Local Development with Bindings

```bash
# wrangler.toml configured with KV/R2/D1 bindings

# Start local dev server (bindings available locally)
wrangler dev

# Access bindings in code:
# env.MY_KV.get("key")
# env.MY_BUCKET.get("file.txt")
# env.DB.prepare("SELECT * FROM users").all()
```

### Remote Development (Wrangler v4+)

```bash
# Use REMOTE bindings instead of local stubs
wrangler dev --remote

# Useful for testing with production data
```

## Service-Specific Guides

For detailed quick-start patterns for each service:
- [references/service-guides.md](references/service-guides.md) - Workers, Pages, R2, D1, KV, Queues, AI

For complete API surface coverage:
- [references/api-surface.md](references/api-surface.md) - All 14 API categories

## Rate Limits & Quotas

**Wrangler operations**: Subject to account tier limits (Free/Pro/Business/Enterprise)

**API operations**:
- Client API per user/account token: 1,200 requests per 5 minutes
- Client API per IP: 200 requests per second
- GraphQL: 320 requests per 5 minutes (variable by query cost)

**Best practices**:
- Use Wrangler for bulk operations (built-in rate limit handling)
- For direct API calls, implement exponential backoff on 429 responses
- Cache API responses where appropriate (zone configs, etc.)

## Troubleshooting

### Common Issues

**Authentication fails**:
```bash
# Check token validity
wrangler whoami

# Re-authenticate
wrangler login

# Verify environment variables
echo $CLOUDFLARE_API_TOKEN
echo $CLOUDFLARE_ACCOUNT_ID
```

**Deploy fails**:
```bash
# Check syntax
wrangler deploy --dry-run

# View detailed logs
wrangler tail my-worker

# Check wrangler.toml syntax
wrangler config
```

**KV/R2/D1 not accessible**:
```bash
# Verify bindings in wrangler.toml
# Verify namespace/bucket/database exists
wrangler kv namespace list
wrangler r2 bucket list
wrangler d1 list
```

**Script errors**:
```bash
# Ensure CLOUDFLARE_API_TOKEN is set
export CLOUDFLARE_API_TOKEN="your_token"

# Ensure jq is installed (scripts use it for JSON parsing)
which jq || brew install jq  # or apt-get install jq
```

## Migration from Legacy Tools

### From `cf-cli` or `flarectl`
Both are deprecated. Migrate to:
- **Wrangler** for Workers/Pages/Storage
- **REST API scripts** (this skill) for DNS/SSL/Security
- **Terraform provider** for infrastructure-as-code

### From Cloudflare Dashboard
Export existing configs:
```bash
# DNS records
bash scripts/cf-zone-management.sh dns export example.com > dns-records.json

# Firewall rules
bash scripts/cf-security.sh firewall export example.com > firewall-rules.json
```

## Resources

- **Wrangler Docs**: https://developers.cloudflare.com/workers/wrangler/
- **API Docs**: https://developers.cloudflare.com/api/
- **Workers Examples**: https://developers.cloudflare.com/workers/examples/
- **Community Discord**: https://discord.gg/cloudflaredev

## Next Steps

1. Install Wrangler: `npm install -g wrangler@latest`
2. Authenticate: `wrangler login`
3. Create your first Worker: `npm create cloudflare@latest`
4. Explore service guides: [references/service-guides.md](references/service-guides.md)
5. Review API surface: [references/api-surface.md](references/api-surface.md)
