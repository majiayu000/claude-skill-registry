---
name: domain-management
description: Configure domain routing and Cloudflare DNS for sgcarstrends.com and subdomains. Use when adding new services, updating domain patterns, or debugging DNS issues.
allowed-tools: Read, Edit, Grep, Glob
---

# Domain Management Skill

This skill helps you manage domains and DNS configuration for the SG Cars Trends platform.

## When to Use This Skill

- Adding new subdomains
- Configuring SSL certificates
- Updating DNS records
- Debugging domain resolution issues
- Setting up custom domains for services
- Managing Cloudflare settings
- Troubleshooting SSL/TLS errors

## Domain Architecture

### Domain Structure

```
sgcarstrends.com                    # Production web app
staging.sgcarstrends.com            # Staging web app
dev.sgcarstrends.com                # Development web app

api.sgcarstrends.com                # Production API
api.staging.sgcarstrends.com        # Staging API
api.dev.sgcarstrends.com            # Development API

docs.sgcarstrends.com               # Documentation (future)
```

### Naming Convention

**Web Apps:**
- Production: Apex domain (`sgcarstrends.com`)
- Other envs: `{stage}.sgcarstrends.com`

**Backend Services:**
- Pattern: `{service}.{stage}.sgcarstrends.com`
- Production service: `{service}.sgcarstrends.com` (no stage prefix)

Examples:
```
api.sgcarstrends.com              # Production API
api.staging.sgcarstrends.com      # Staging API
websocket.sgcarstrends.com        # Production WebSocket service
websocket.dev.sgcarstrends.com    # Dev WebSocket service
```

## DNS Provider: Cloudflare

### Why Cloudflare?

- Free SSL certificates
- DDoS protection
- CDN capabilities
- Fast DNS propagation
- Analytics and logs
- Page Rules for optimization

### DNS Management

Cloudflare manages DNS records, AWS Route53 is for SSL certificate validation only.

## SST Domain Configuration

### DNS Stack

```typescript
// infra/dns.ts
import { StackContext } from "sst/constructs";
import * as route53 from "aws-cdk-lib/aws-route53";

export function DNS({ stack }: StackContext) {
  // Import existing hosted zone (created in Route53)
  const hostedZone = route53.HostedZone.fromLookup(stack, "HostedZone", {
    domainName: "sgcarstrends.com",
  });

  stack.addOutputs({
    HostedZoneId: hostedZone.hostedZoneId,
    HostedZoneName: hostedZone.zoneName,
  });

  return { hostedZone };
}
```

### Web App Domain

```typescript
// infra/web.ts
import { StackContext, NextjsSite, use } from "sst/constructs";
import { DNS } from "./dns";

export function Web({ stack, app }: StackContext) {
  const { hostedZone } = use(DNS);

  const web = new NextjsSite(stack, "web", {
    path: "apps/web",
    customDomain: {
      domainName: app.stage === "production"
        ? "sgcarstrends.com"                    // Apex domain for prod
        : `${app.stage}.sgcarstrends.com`,       // Subdomain for others
      hostedZone: hostedZone.zoneName,
    },
  });

  stack.addOutputs({
    WebUrl: web.url,
    WebDomain: web.customDomainUrl,
  });

  return { web };
}
```

### API Domain

```typescript
// infra/api.ts
import { StackContext, Function, use } from "sst/constructs";
import { DNS } from "./dns";

export function API({ stack, app }: StackContext) {
  const { hostedZone } = use(DNS);

  const api = new Function(stack, "api", {
    handler: "apps/api/src/index.handler",
    url: {
      domain: {
        domainName: app.stage === "production"
          ? "api.sgcarstrends.com"
          : `api.${app.stage}.sgcarstrends.com`,
        hostedZone: hostedZone.zoneName,
      },
    },
  });

  stack.addOutputs({
    ApiUrl: api.url,
    ApiDomain: api.url,
  });

  return { api };
}
```

## Cloudflare Configuration

### DNS Records

Cloudflare DNS records point to AWS CloudFront or Lambda Function URLs:

```
Type    Name                     Value                                   Proxy
CNAME   sgcarstrends.com        d111111abcdef8.cloudfront.net          ✓ Proxied
CNAME   staging                 d222222abcdef8.cloudfront.net          ✓ Proxied
CNAME   dev                     d333333abcdef8.cloudfront.net          ✓ Proxied
CNAME   api                     abc123.lambda-url.ap-southeast-1.on.aws  ✓ Proxied
CNAME   api.staging             def456.lambda-url.ap-southeast-1.on.aws  ✓ Proxied
```

### SSL/TLS Settings

**Encryption Mode**: Full (strict)
- Encrypts traffic from browser to Cloudflare
- Encrypts traffic from Cloudflare to origin (AWS)
- Validates origin certificate

**Edge Certificates**:
- Automatically provisioned by Cloudflare
- Covers `*.sgcarstrends.com` and `sgcarstrends.com`
- Auto-renewed

### Page Rules

```
Rule 1: Cache API responses
URL: api.sgcarstrends.com/*
Settings:
  - Cache Level: Standard
  - Edge Cache TTL: 1 hour

Rule 2: Always use HTTPS
URL: *sgcarstrends.com/*
Settings:
  - Always Use HTTPS: On

Rule 3: Security headers
URL: sgcarstrends.com/*
Settings:
  - Security Headers: On
  - HSTS: Enabled
```

## SSL Certificate Management

### AWS Certificate Manager

SST automatically requests certificates from ACM:

```typescript
// Automatic when using customDomain
const web = new NextjsSite(stack, "web", {
  customDomain: {
    domainName: "sgcarstrends.com",
    hostedZone: hostedZone.zoneName,
  },
});

// SST will:
// 1. Request certificate from ACM
// 2. Add DNS validation records to Route53
// 3. Wait for validation
// 4. Attach certificate to CloudFront/Lambda
```

### Manual Certificate Request

If needed:

```bash
# Request certificate
aws acm request-certificate \
  --domain-name sgcarstrends.com \
  --subject-alternative-names *.sgcarstrends.com \
  --validation-method DNS \
  --region us-east-1  # CloudFront requires us-east-1

# Get validation records
aws acm describe-certificate \
  --certificate-arn arn:aws:acm:... \
  --region us-east-1
```

Add validation CNAME records to Cloudflare DNS.

## Adding New Subdomains

### 1. Define in SST

```typescript
// infra/new-service.ts
import { StackContext, Function, use } from "sst/constructs";
import { DNS } from "./dns";

export function NewService({ stack, app }: StackContext) {
  const { hostedZone } = use(DNS);

  const service = new Function(stack, "new-service", {
    handler: "apps/new-service/src/index.handler",
    url: {
      domain: {
        domainName: app.stage === "production"
          ? "newservice.sgcarstrends.com"
          : `newservice.${app.stage}.sgcarstrends.com`,
        hostedZone: hostedZone.zoneName,
      },
    },
  });

  return { service };
}
```

### 2. Deploy

```bash
npx sst deploy --stage production
```

SST will:
1. Request ACM certificate
2. Create Route53 records for validation
3. Wait for validation
4. Create Lambda Function URL or CloudFront distribution
5. Output the AWS resource URL

### 3. Add Cloudflare DNS

Get the AWS URL from SST outputs, then:

1. Go to Cloudflare dashboard
2. Select `sgcarstrends.com` domain
3. Click "DNS" → "Add record"
4. Type: CNAME
5. Name: `newservice` (or `newservice.staging`)
6. Target: The AWS URL (CloudFront or Lambda)
7. Proxy status: Proxied (orange cloud)
8. TTL: Auto
9. Save

### 4. Verify

```bash
# Check DNS resolution
dig newservice.sgcarstrends.com

# Test HTTPS
curl -I https://newservice.sgcarstrends.com
```

## Debugging DNS Issues

### Check DNS Propagation

```bash
# Check Cloudflare DNS
dig @1.1.1.1 sgcarstrends.com
dig @1.1.1.1 api.sgcarstrends.com

# Check global propagation
dig sgcarstrends.com @8.8.8.8  # Google DNS
dig sgcarstrends.com @1.1.1.1  # Cloudflare DNS

# Or use online tools
# https://www.whatsmydns.net/#CNAME/api.sgcarstrends.com
```

### Check SSL Certificate

```bash
# Check certificate details
openssl s_client -connect sgcarstrends.com:443 -servername sgcarstrends.com

# Check certificate expiry
echo | openssl s_client -connect sgcarstrends.com:443 -servername sgcarstrends.com 2>/dev/null | openssl x509 -noout -dates
```

### Test Domain Resolution

```bash
# Test HTTP → HTTPS redirect
curl -I http://sgcarstrends.com

# Test HTTPS
curl -I https://sgcarstrends.com

# Test API endpoint
curl -I https://api.sgcarstrends.com/health
```

### Common Issues

**Issue**: DNS not resolving
**Solutions**:
1. Check Cloudflare DNS record exists
2. Verify record type (CNAME vs A)
3. Check proxy status (should be Proxied)
4. Wait for propagation (usually < 5 minutes)

**Issue**: SSL certificate error
**Solutions**:
1. Check Cloudflare SSL mode is "Full (strict)"
2. Verify ACM certificate is issued
3. Check certificate covers the subdomain
4. Verify Route53 has validation records

**Issue**: 522 error (Connection timed out)
**Solutions**:
1. Check Lambda/CloudFront is running
2. Verify security groups allow HTTPS
3. Check origin server is responding
4. Review Cloudflare → Origin connection

**Issue**: Redirecting to wrong domain
**Solutions**:
1. Check SST `customDomain` configuration
2. Verify Cloudflare page rules
3. Check application redirect logic

## CORS Configuration

When API and Web are on different domains:

```typescript
// apps/api/src/index.ts
import { Hono } from "hono";
import { cors } from "hono/cors";

const app = new Hono();

app.use("/*", cors({
  origin: [
    "https://sgcarstrends.com",
    "https://staging.sgcarstrends.com",
    "https://dev.sgcarstrends.com",
    "http://localhost:3001",  // Local development
  ],
  credentials: true,
}));
```

## Monitoring

### Cloudflare Analytics

1. Go to Cloudflare dashboard
2. Select domain
3. Click "Analytics & Logs"

View:
- Traffic stats
- Performance metrics
- Security events
- Cache analytics

### AWS Route53 Health Checks

```typescript
// infra/monitoring.ts
import { StackContext } from "sst/constructs";
import * as route53 from "aws-cdk-lib/aws-route53";

export function Monitoring({ stack }: StackContext) {
  new route53.CfnHealthCheck(stack, "ApiHealthCheck", {
    healthCheckConfig: {
      type: "HTTPS",
      fullyQualifiedDomainName: "api.sgcarstrends.com",
      port: 443,
      resourcePath: "/health",
      requestInterval: 30,
      failureThreshold: 3,
    },
  });
}
```

## Domain Migration

### Migrating to New Domain

1. **Set up new domain in Cloudflare**
2. **Deploy to new domain**:
   ```typescript
   customDomain: {
     domainName: "new-domain.com",
     hostedZone: newHostedZone.zoneName,
   }
   ```
3. **Test new domain thoroughly**
4. **Set up redirects from old to new**:
   ```typescript
   // Cloudflare page rule
   URL: old-domain.com/*
   Forwarding URL: 301 - https://new-domain.com/$1
   ```
5. **Update all references**
6. **Monitor traffic**
7. **Keep old domain for 6-12 months**

## Apex Domain Considerations

### Using Apex Domain

The project uses apex domain (`sgcarstrends.com`) for production:

**Advantages**:
- Shorter, cleaner URL
- Better for branding
- SEO benefits

**Challenges**:
- CNAME at apex not allowed by DNS spec
- Solution: Cloudflare CNAME flattening

### Cloudflare CNAME Flattening

Cloudflare automatically flattens CNAMEs at apex:

```
# This works with Cloudflare:
CNAME  sgcarstrends.com  →  d111111abcdef8.cloudfront.net

# Cloudflare resolves it to:
A      sgcarstrends.com  →  104.21.x.x
A      sgcarstrends.com  →  172.67.x.x
```

## Subdomain Strategy

### Current Subdomains

```
Web apps:
  sgcarstrends.com           # Production
  staging.sgcarstrends.com   # Staging
  dev.sgcarstrends.com       # Development

API:
  api.sgcarstrends.com       # Production
  api.staging...             # Staging
  api.dev...                 # Development

Future:
  docs.sgcarstrends.com      # Documentation
  status.sgcarstrends.com    # Status page
```

### Adding Future Services

Follow the pattern:
- **Production**: `{service}.sgcarstrends.com`
- **Non-production**: `{service}.{stage}.sgcarstrends.com`

## Security Headers

Configure in Cloudflare or application:

```typescript
// apps/web/next.config.js
const securityHeaders = [
  {
    key: "X-DNS-Prefetch-Control",
    value: "on",
  },
  {
    key: "Strict-Transport-Security",
    value: "max-age=63072000; includeSubDomains; preload",
  },
  {
    key: "X-Frame-Options",
    value: "SAMEORIGIN",
  },
  {
    key: "X-Content-Type-Options",
    value: "nosniff",
  },
  {
    key: "Referrer-Policy",
    value: "origin-when-cross-origin",
  },
];

const nextConfig = {
  async headers() {
    return [
      {
        source: "/:path*",
        headers: securityHeaders,
      },
    ];
  },
};
```

## References

- Cloudflare Docs: https://developers.cloudflare.com
- AWS Route53: https://docs.aws.amazon.com/route53
- SST Custom Domains: https://docs.sst.dev/custom-domains
- Related files:
  - `infra/dns.ts` - DNS configuration
  - `infra/CLAUDE.md` - Infrastructure documentation

## Best Practices

1. **Use Cloudflare Proxy**: Enable orange cloud for DDoS protection
2. **Full (Strict) SSL**: Always use strict SSL mode
3. **HTTPS Only**: Enforce HTTPS with page rules
4. **Consistent Naming**: Follow `{service}.{stage}.domain` pattern
5. **Certificate Management**: Let SST handle ACM certificates
6. **DNS TTL**: Use Auto for active development, higher for stable
7. **Monitoring**: Set up health checks for critical domains
8. **Documentation**: Document all subdomains and their purpose
