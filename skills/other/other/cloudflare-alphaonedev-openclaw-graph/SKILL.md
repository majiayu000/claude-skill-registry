---
name: cloudflare
cluster: core-openclaw
description: "Cloudflare API: DNS, Zones, Pages, Access, Workers, R2. Account ID: <your-account-id>"
tags: ["cloudflare","dns","cdn","access","pages","workers"]
dependencies: []
composes: []
similar_to: []
called_by: []
authorization_required: false
scope: general
model_hint: claude-sonnet
embedding_hint: "cloudflare dns zone pages access workers api r2"
---

# cloudflare

## Purpose
This skill provides programmatic access to Cloudflare's API for managing DNS records, zones, Pages sites, Access policies, Workers scripts, and R2 storage. It uses the specified account ID (YOUR_CLOUDFLARE_ACCOUNT_ID) to perform operations securely.

## When to Use
Use this skill for automating infrastructure tasks like updating DNS records during deployments, securing applications with Access, deploying static sites via Pages, running edge compute with Workers, managing object storage in R2, or creating/deleting zones. Apply it in scripts, CI/CD pipelines, or when integrating Cloudflare with other services.

## Key Capabilities
- DNS: Manage records (A, CNAME, TXT) within zones.
- Zones: Create, list, update, or delete zones using the account ID.
- Pages: Deploy and manage static sites with custom domains.
- Access: Enforce policies for authentication and authorization.
- Workers: Script edge logic for requests and responses.
- R2: Handle object storage operations like uploads and deletions.
Authentication requires an API token set as `$CLOUDFLARE_API_TOKEN`; include the account ID in API requests.

## Usage Patterns
Always authenticate requests with `$CLOUDFLARE_API_TOKEN`. Use HTTP headers for API calls (e.g., `Authorization: Bearer $CLOUDFLARE_API_TOKEN`). For CLI, install Wrangler and log in with `wrangler login`. Structure requests with JSON payloads and handle responses via status codes. Prefix API endpoints with `https://api.cloudflare.com/client/v4` and include the account ID in paths, like `/accounts/YOUR_CLOUDFLARE_ACCOUNT_ID/zones`.

## Common Commands/API
- DNS Update: Use PUT to `/zones/{zone_id}/dns_records/{record_id}` with JSON body like `{"type":"A","name":"example.com","content":"192.0.2.1","ttl":3600}`.
- Zone Creation: POST to `/zones` with body `{"name":"example.com","account":{"id":"YOUR_CLOUDFLARE_ACCOUNT_ID"}}`.
- Pages Deployment: Use Wrangler CLI: `wrangler pages deploy ./build --project-name=my-site`.
- Access Policy: POST to `/access/policies` with body `{"name":"Block IP","precedence":1,"decision":"deny","request":{"ip":"1.1.1.1"}}`.
- Workers Script: Upload via PUT to `/accounts/YOUR_CLOUDFLARE_ACCOUNT_ID/workers/scripts/my-worker` with script content.
- R2 Object Upload: PUT to `/accounts/YOUR_CLOUDFLARE_ACCOUNT_ID/r2/buckets/my-bucket/objects/my-file` with file data.
Code snippet for DNS update:
```
curl -X PUT "https://api.cloudflare.com/client/v4/zones/zone_id/dns_records/record_id" \
  -H "Authorization: Bearer $CLOUDFLARE_API_TOKEN" \
  -H "Content-Type: application/json" \
  --data '{"type":"A","name":"example.com","content":"192.0.2.1"}'
```
Config format: Store API token in `.env` as `CLOUDFLARE_API_TOKEN=your_token`, and load it in scripts.

## Integration Notes
Integrate by exporting `$CLOUDFLARE_API_TOKEN` in your environment. For Node.js, use the `@cloudflare/workers` SDK: install via `npm i @cloudflare/workers`, then import and initialize with the token. In Python, use `cloudflare` library: `pip install cloudflare`, and authenticate with `Cloudflare(api_token=os.environ['CLOUDFLARE_API_TOKEN'])`. Always validate responses for the account ID to avoid cross-account errors. For Wrangler, run `wrangler whoami` to verify login before commands.

## Error Handling
Check HTTP status codes: 200-299 for success, 4xx for client errors (e.g., 401 Unauthorized if token is invalid), and 5xx for server issues. For API errors, parse the JSON response body for "errors" array, e.g., `{"errors":[{"code":1000,"message":"Bad request"}]}`. Retry transient errors (e.g., 429 Rate Limit) with exponential backoff. In scripts, wrap calls in try-catch blocks:
```
try {
  const response = await fetch('https://api.cloudflare.com/client/v4/...', { headers: { Authorization: `Bearer ${process.env.CLOUDFLARE_API_TOKEN}` } });
  if (!response.ok) throw new Error(`HTTP error: ${response.status}`);
} catch (error) {
  console.error('API call failed:', error.message);
}
```
Log detailed error messages including the endpoint and parameters for debugging.

## Concrete Usage Examples
1. Update a DNS A record for a domain: First, get the zone ID via GET `/zones?name=example.com`. Then, use the record ID to update: PUT `/zones/zone_id/dns_records/record_id` with body `{"content":"new_ip_address"}`. This ensures the domain points to the latest server IP.
2. Deploy a Workers script: Write your script in `worker.js`, then run `wrangler publish --name my-worker`. For API integration, upload via PUT `/accounts/YOUR_CLOUDFLARE_ACCOUNT_ID/workers/scripts/my-worker` with the script content, then bind it to a route with POST `/zones/zone_id/workers/routes`.

## Graph Relationships
- Related to: core-openclaw (cluster), skills like "dns" for record management, "workers" for edge computing, and "access" for security policies.
- Dependencies: Requires authentication via Cloudflare API; integrates with external skills like "github" for deployment triggers or "aws" for R2 data syncing.
